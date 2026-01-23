# backward_to_query_magnet.py 改进总结

**日期**: 2026-01-08
**修改文件**: `/data/lhy/datasets/graph-Toucan/src/backward_to_query_magnet.py`

---

## 📋 修改背景

### 初始问题

在测试生成的 `fsp_v2_queries.jsonl` 数据时，发现了两个主要问题：

1. **英文生成不一致**：部分生成的 query 是中文而非英文（如 12306 火车票查询场景）
2. **chose_func 和 functions 数量不匹配**：`merged_with_insert` 类型的 turn 中，模型只返回了部分函数

### 根本原因

1. **英文要求不够强**：Prompt 中的英文要求不够醒目和强制
2. **merged_with_insert 没有专门处理**：`build_prompt_for_turn()` 没有 `merged_with_insert` 分支，导致使用了 normal 分支
3. **显式/隐式函数区分不清**：没有明确告诉模型哪些函数应该在 query 中提及，哪些不应该提及

---

## 🔧 核心修改

### 1. 强化所有 Prompt 的英文生成要求

**修改位置**: 所有 turn 类型的 prompt（9处）

**修改前**:
```python
**IMPORTANT: Generate the user query in English.**
```

**修改后**:
```python
**CRITICAL: You MUST generate the user query in English, regardless of function names or descriptions.**
```

**改进点**:
- `IMPORTANT` → `CRITICAL`：提升紧急程度
- `Generate` → `You MUST generate`：更强制性的语气
- 添加 `regardless of function names or descriptions`：明确即使函数名或描述是中文也要生成英文

**影响的 turn 类型**:
- empty (line 776)
- merged (line 808)
- merged_with_insert (line 848)
- insert_short (line 888)
- insert_long (line 924)
- insert_mixed (line 970)
- normal - first turn (line 967)
- normal - non-first turn (line 986)
- generate_single_func_params (line 1267)

---

### 2. 添加函数签名参数 `turn_operations`

**修改位置**:
- `build_prompt_for_turn()` (line 665-685)
- `generate_query_for_turn_magnet()` (line 1027-1056)

**目的**: 传递 turn 的操作信息（merge_info, insert_info），用于区分显式和隐式函数

**新增参数**:
```python
turn_operations: Optional[Dict[str, Any]] = None
```

**数据结构**:
```python
{
    "operations": ["merge", "insert_short"],
    "merge_info": {
        "merged_functions": ["func1", "func2"]
    },
    "insert_info": [
        {
            "inserted_function": "func3",
            "insert_type": "short_dependency"  # or "long_dependency"
        }
    ]
}
```

---

### 3. 添加 Long Dependency 明确定义

#### 3.1 insert_long 分支 (lines 910-958)

**添加内容**:

1. **LONG DEPENDENCY Definition**:
   - 使用代词和间接引用
   - 不重复具体值或 ID
   - 自然对话风格

2. **代词引用模式**:
   ```
   - "that <noun>" → "that distance", "that booking"
   - "those <noun>" → "those records", "those cities"
   - "the previous <noun>" → "the previous search"
   - "my <noun>" → "my trip", "my reservation"
   ```

3. **Good/Bad Examples**:
   ```
   ✓ "Using that distance, find nearby cities"
   ✗ "Using 25.4 kilometers, find cities"  ← 不要重复具体值
   ```

#### 3.2 insert_mixed 分支 (lines 986-1030)

**强化 long dependency 指导**:
- 明确区分 long dependency（代词引用）和 short dependency（隐式）
- 提供混合场景的 Good/Bad Examples

---

### 4. 正确区分显式/隐式函数（核心修复）

#### 4.1 merged_with_insert 分支 (lines 835-901)

**关键改进**: 区分**三类**函数，而不是两类

**修改前**:
```python
# ❌ 把所有 inserted 函数都当作隐式
merged_funcs = []
inserted_funcs = []  # 全部隐式！
```

**修改后**:
```python
# ✅ 区分三类函数
merged_funcs = []        # 显式：merged 的函数
long_dep_funcs = []      # 显式但用代词：long_dependency insert
short_dep_funcs = []     # 隐式：short_dependency insert

if turn_operations:
    # 从 merge_info 提取 merged 函数
    merge_info = turn_operations.get("merge_info")
    if merge_info:
        merged_funcs = merge_info.get("merged_functions", [])

    # 从 insert_info 提取并区分 long/short dependency
    insert_info_list = turn_operations.get("insert_info", [])
    for insert_info in insert_info_list:
        inserted_func = insert_info.get("inserted_function")
        insert_type = insert_info.get("insert_type")

        if inserted_func:
            if insert_type == "long_dependency":
                long_dep_funcs.append(inserted_func)  # 显式，代词引用
            else:
                short_dep_funcs.append(inserted_func)  # 隐式
```

**Prompt 指导**:
```python
**Function Classification**:
- MERGED functions (explicit intents): {merged_funcs}
- LONG-DEPENDENCY functions (explicit, reference history): {long_dep_funcs}
- SHORT-DEPENDENCY helpers (implicit, do NOT mention): {short_dep_funcs}

**Critical Instructions**:
1. MERGED functions: Express clearly
2. LONG-DEPENDENCY functions: Express with pronouns ("that", "those")
3. SHORT-DEPENDENCY helpers: DO NOT mention
```

**预期效果示例**:
```
Functions: ["get_weather_forecast", "cities_by_range", "get_live_temp"]
- merged_funcs: ["get_weather_forecast"]
- long_dep_funcs: ["cities_by_range"]  # 引用之前的距离
- short_dep_funcs: ["get_live_temp"]   # 隐式 helper

✓ Query: "Get weather forecast for Shanghai and find cities within that distance"
✗ Query: "Get weather and also get live temperature and find cities within 25.4km"
```

---

#### 4.2 insert_short 分支 (lines 883-936)

**改进**: 从 turn_operations 提取准确的主函数和插入函数

**修改前**:
```python
# ❌ 假设第一个是主函数
primary_func = turn_functions[0]
nested_funcs = turn_functions[1:]
```

**修改后**:
```python
# ✅ 从 turn_operations 提取
primary_funcs = []
inserted_funcs = []

if turn_operations:
    insert_info_list = turn_operations.get("insert_info", [])
    for insert_info in insert_info_list:
        inserted_func = insert_info.get("inserted_function")
        if inserted_func:
            inserted_funcs.append(inserted_func)

    # 主函数 = 所有函数 - 插入的函数
    primary_funcs = [f for f in turn_functions if f not in inserted_funcs]
```

**Prompt 明确列出**:
```python
**PRIMARY function(s) to mention in query**: {primary_funcs}
**IMPLICIT nested/helper function(s) (do NOT mention)**: {inserted_funcs}
```

---

#### 4.3 insert_mixed 分支 (lines 960-1030)

**改进**: 只提取 short_dependency 作为隐式函数

```python
primary_funcs = []
inserted_short_funcs = []

if turn_operations:
    insert_info_list = turn_operations.get("insert_info", [])
    for insert_info in insert_info_list:
        # 只有 short dependency 的函数才是隐式的
        if insert_info.get("insert_type") == "short_dependency":
            inserted_func = insert_info.get("inserted_function")
            if inserted_func:
                inserted_short_funcs.append(inserted_func)

    # 主函数 = 所有函数 - short dependency 的插入函数
    primary_funcs = [f for f in turn_functions if f not in inserted_short_funcs]
```

**Note**: long_dependency 的函数不是隐式的，它们应该在 query 中用代词引用

---

### 5. 改进 merged 分支的 Prompt (lines 793-833)

**问题**: merged 分支的 prompt 不够详细，主要依赖 STYLE_INSTRUCTIONS

**添加内容**:

1. **MERGED Definition**:
   ```
   - Multiple functions in the SAME turn with potential SHORT DEPENDENCY
   - Output of one function may feed as input to the next
   - User EXPLICITLY mentions ALL actions/intents
   - Use connecting words: "and", "then", "after that"
   ```

2. **Critical Instructions** (5条):
   ```
   1. EXPLICITLY mention ALL intents/actions in your query
   2. Use connecting words: "and", "then", "after that"
   3. Make the data flow clear if functions have dependencies
   4. Each function should be reflected in the query
   5. Natural combination of multiple explicit intents
   ```

3. **Contrast with Insert Short**:
   ```
   - Insert Short: "Navigate to San Mateo" (only final goal, distance is implicit)
   - Merged: "Find the distance to San Mateo and set up navigation" (both steps explicit)
   ```

---

### 6. 更新 STYLE_INSTRUCTIONS

#### 6.1 merged_with_insert (lines 367-405)

**修改前**:
```python
- Some functions are IMPLICIT (from insert)  ❌
- Inserted/helper functions → keep implicit  ❌ 没区分 long/short
```

**修改后**:
```python
- **THREE types of functions**:
  1. MERGED functions: Explicit intents
  2. LONG-DEPENDENCY inserts: Explicit (use pronouns)
  3. SHORT-DEPENDENCY inserts: Implicit helpers

**Examples**:
✓ "Get weather forecast for Shanghai and check that distance"
✗ "Get weather and also get live temperature and convert units"
```

---

### 7. 添加专门的 Examples

#### 7.1 merged_with_insert Examples (lines 577-612)

**添加 3 个专门的例子**，展示三种函数类型的混合：

| Example | Query | 函数分类 |
|---------|-------|---------|
| Weather & Distance | "Get weather forecast and find cities within **that distance**" | merged: weather_forecast<br>long-dep: cities_by_range<br>short-dep: get_live_temp |
| Flight & Cancel | "Book flight and cancel **my previous trip**" | merged: book_flight<br>long-dep: cancel_booking<br>short-dep: calculate_refund |
| Hotels & Export | "Search hotels and export **those records**" | merged: search_hotels<br>long-dep: export_to_pdf<br>short-dep: format_report |

**Example 结构**:
```python
{
    "name": "Weather Forecast and Distance Check",
    "history": "Turn 0: Get distance from SF to SM (25.4 km)",
    "functions": ["get_weather_forecast", "cities_by_range", "get_live_temp"],
    "merged_funcs": ["get_weather_forecast"],      # 显式
    "long_dep_funcs": ["cities_by_range"],         # 显式，代词引用
    "short_dep_funcs": ["get_live_temp"],          # 隐式
    "query": "Get weather forecast for Shanghai and find cities within that distance",
    "explanation": "...",
    "anti_example": "Get weather forecast and also get live temperature and find cities within 25.4km",
}
```

---

#### 7.2 insert_mixed Examples (lines 614-660)

**添加 4 个专门的例子**，展示 long + short dependency 的混合：

| Example | Query | 函数分类 |
|---------|-------|---------|
| Area Calculation | "Using **that distance**, calculate area in square meters" | primary: calculate_area<br>long-dep: from Turn 0<br>short-dep: convert_to_square_meters |
| Restaurant Search | "Find restaurants within **that budget** in Euros" | primary: search_restaurants<br>long-dep: from Turn 0<br>short-dep: convert_currency |
| Route Planning | "Plan route to **those coordinates**" | primary: plan_route<br>long-dep: from Turn 0<br>short-dep: get_distance_in_km |
| Visualization | "Create chart showing **those figures** as percentages" | primary: create_bar_chart<br>long-dep: from Turn 0<br>short-dep: format_to_percentage |

**Example 结构**:
```python
{
    "name": "Area Calculation with Historical Distance",
    "history": "Turn 0: Get distance from SF to SM (25.4 km)",
    "functions": ["calculate_area", "convert_to_square_meters"],
    "primary_funcs": ["calculate_area"],
    "long_dep_context": "uses 'that distance' from Turn 0 as length parameter",
    "short_dep_funcs": ["convert_to_square_meters"],
    "query": "Using that distance, calculate the area in square meters",
    "explanation": "...",
    "anti_example": "Using 25.4km, calculate area and convert to square meters",
}
```

---

#### 7.3 更新 select_examples() (lines 692-700)

**修改前**:
```python
elif primary_style == "merged_with_insert":
    # 混合：1 short + 1 long + 1 sequential
    examples.extend(random.sample(EXAMPLES["short_dependency"], 1))
    examples.extend(random.sample(EXAMPLES["long_dependency"], 1))
    examples.extend(random.sample(EXAMPLES["sequential"], 1))
```

**修改后**:
```python
elif primary_style == "merged_with_insert":
    # 使用专门的 merged_with_insert examples
    examples = random.sample(EXAMPLES["merged_with_insert"],
                            min(num_examples, len(EXAMPLES["merged_with_insert"])))

elif primary_style == "insert_mixed":
    # 使用专门的 insert_mixed examples
    examples = random.sample(EXAMPLES["insert_mixed"],
                            min(num_examples, len(EXAMPLES["insert_mixed"])))
```

---

#### 7.4 更新 format_examples_for_prompt() (lines 708-794)

**添加对新 example 格式的支持**:

1. **merged_with_insert format**:
   ```python
   if "merged_funcs" in ex and "long_dep_funcs" in ex and "short_dep_funcs" in ex:
       formatted = f"""
   Example {i}: {ex['name']} (Merged + Insert Mix)

   Functions:
   - MERGED (explicit): {merged_funcs}
   - LONG-DEP (explicit, pronoun): {long_dep_funcs}
   - SHORT-DEP (implicit): {short_dep_funcs}

   User Query: "{query}"
   Why this works: {explanation}
   ❌ Bad Example: "{anti_example}"
   """
   ```

2. **insert_mixed format**:
   ```python
   elif "primary_funcs" in ex and "long_dep_context" in ex and "short_dep_funcs" in ex:
       formatted = f"""
   Example {i}: {ex['name']} (Mixed Dependencies)

   Functions:
   - PRIMARY (explicit): {primary_funcs}
   - LONG-DEP context: {long_dep_context}
   - SHORT-DEP helpers (implicit): {short_dep_funcs}

   User Query: "{query}"
   Why this works: {explanation}
   ❌ Bad Example: "{anti_example}"
   """
   ```

---

## 📊 修改统计

### 代码修改

| 类型 | 数量 | 说明 |
|------|------|------|
| **函数签名修改** | 2 | build_prompt_for_turn, generate_query_for_turn_magnet |
| **Prompt 分支修改** | 4 | merged, merged_with_insert, insert_short, insert_mixed |
| **Long dependency 定义** | 2 | insert_long, insert_mixed |
| **英文要求强化** | 9 | 所有 turn 类型的 prompt |
| **STYLE_INSTRUCTIONS** | 1 | merged_with_insert |
| **新增 Examples** | 7 | 3个 merged_with_insert + 4个 insert_mixed |
| **函数修改** | 2 | select_examples, format_examples_for_prompt |

### 影响范围

| 组件 | 影响 |
|------|------|
| **Prompt 生成** | ✅ 所有 turn 类型都有更明确的指导 |
| **函数分类** | ✅ 正确区分显式/隐式/代词引用 |
| **Examples 库** | ✅ 添加 7 个混合场景的专门示例 |
| **代词引用** | ✅ 明确的 long dependency 定义和模式 |

---

## 🎯 预期效果

### 修复前的问题

| 问题 | 示例 |
|------|------|
| **中文 query** | "我想查一下明天从北京到上海的火车票" ❌ |
| **chose_func 不匹配** | functions: 3个，chose_func: 1个 ❌ |
| **隐式性不清** | "Get weather and also get live temperature" ❌<br>（提到了 short-dep helper） |
| **重复具体值** | "Find cities within 25.4km" ❌<br>（应该用 "that distance"） |

### 修复后的预期效果

| 场景 | 预期结果 |
|------|---------|
| **12306 查询** | "Search for train tickets from Beijing to Shanghai tomorrow" ✅ |
| **merged_with_insert** | chose_func 和 functions 数量匹配 ✅ |
| **隐式性** | "Get weather forecast for Shanghai" ✅<br>（不提 get_live_temp helper） |
| **long dependency** | "Find cities within that distance" ✅<br>（用代词，不重复值） |

---

## 🔍 关键概念澄清

### Turn 类型与函数处理

| Turn Type | 显式函数 | 隐式函数 | 代词引用 |
|-----------|---------|---------|---------|
| **normal** | 所有函数 | - | - |
| **merged** | 所有函数 | - | - |
| **insert_short** | 主函数 | 插入的 helper | - |
| **insert_long** | 所有函数 | - | ✅ 用代词引用历史 |
| **insert_mixed** | 主函数 | short-dep helper | ✅ long-dep 用代词 |
| **merged_with_insert** | merged + long-dep | short-dep helper | ✅ long-dep 用代词 |

### Dependency 类型

| Type | 定义 | Query 特征 | 示例 |
|------|------|-----------|------|
| **Short Dependency** | 同 turn 内的函数依赖 | 只提最终目标，helper 隐式 | "Get kilometers from A to B"<br>（convert_unit 隐式） |
| **Long Dependency** | 跨 turn 的函数依赖 | 使用代词引用历史 | "Using **that distance**, find cities"<br>（引用之前的距离） |

---

## 📝 测试建议

### 重点测试场景

1. **中文函数名场景**（如 12306）:
   - 验证生成的 query 是否为英文
   - 即使函数描述是中文，query 也应该是英文

2. **merged_with_insert 场景**:
   - 验证 chose_func 和 functions 数量匹配
   - 验证 query 中：
     - ✅ 提到了 merged 函数
     - ✅ 用代词引用了 long-dep 函数
     - ❌ 没有提到 short-dep helper

3. **insert_long 场景**:
   - 验证 query 使用代词（"that", "those", "my"）
   - 验证 query 不重复具体值或 ID

4. **insert_mixed 场景**:
   - 验证 query 表达了主函数
   - 验证 query 用代词引用了历史
   - 验证 query 没有提到 short-dep helper

---

## 🔄 后续优化方向

### 可选的进一步改进

1. **Few-shot Examples 数量调优**:
   - 当前每种类型选择 2 个 examples
   - 可以根据模型表现调整数量

2. **添加更多特定领域的 examples**:
   - 如旅行场景、电商场景、数据分析场景
   - 帮助模型更好地理解不同领域的表达方式

3. **Error Feedback 机制**:
   - 当前有 error_feedback 参数
   - 可以添加更智能的重试逻辑

4. **Prompt 模板优化**:
   - 根据实际生成质量，继续优化 prompt 措辞
   - A/B 测试不同的 prompt 变体

---

## 📚 相关文档

- **MAGNET Paper**: arXiv:2503.07826v1
- **Short vs Long Dependency**: `MAGNET_Short_vs_Long_Dependency.md`
- **FSP Integration**: `MAGNET_FSP_Integration_Analysis.md`

---

**修改完成时间**: 2026-01-08
**修改者**: Claude Sonnet 4.5
**代码状态**: ✅ 已完成，待测试
