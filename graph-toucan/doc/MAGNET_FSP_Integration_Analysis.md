# MAGNET FSP 集成分析报告

## 📋 执行摘要

本报告分析了 `backward_to_query.py` 的核心方法（Backward 和 Forward），并提供了集成 MAGNET 论文中 Merge、Insert、Split 操作的详细方案。

---

## 🔍 当前实现分析

### 1. Backward 方法：`generate_query_for_turn()`

**功能**: 从函数签名生成自然语言查询（函数 → Query）

**输入参数**:
```python
- history_turns: List[List[str]]           # 历史轮次的函数列表
- last_round_functions: List[str]          # 上一轮的函数列表
- last_round_outputs: List[Dict]           # 上一轮的输出
- candidate_functions: List[str]           # 候选函数列表（当前turn要调用）
- tool_schemas: Dict[str, Dict]            # 工具 schema
- error_feedback: Optional[str]            # 错误反馈（用于重试）
```

**输出**:
```python
{
    "ok": bool,
    "user_query": str,              # 生成的自然语言查询
    "chose_func": List[str],        # 模型选择的函数列表
    "reason": str,                  # 选择原因
    "raw_output": str,              # LLM原始输出
    "token_usage": dict             # Token使用统计
}
```

**核心逻辑**:
1. **构建 Prompt** (通过 `build_prompt_for_turn`)
   - 历史函数调用信息
   - 上一轮函数及其输出
   - 候选函数文档
   - 错误反馈（如果有）

2. **生成规则** (关键约束):
   ```
   - Query 必须包含所有必需参数的具体值
   - 不能显式提到函数名
   - 使用具体日期而非模糊表达
   - 对于多函数：同一 step 内无绝对参数依赖
   ```

3. **LLM 调用**:
   ```python
   model: DEFAULT_MODEL
   temperature: 1
   max_tokens: 512
   ```

**当前假设**:
- ✅ 每个 turn 只有一个 step
- ✅ Turn 内的多个函数**并行调用**（无依赖）
- ✅ 参数来自 query 或上一轮输出，不来自同 turn 内其他函数

---

### 2. Forward 方法：`forward_to_fc_params()`

**功能**: 从查询生成带参数的函数调用（Query → Function Calls）

**输入参数**:
```python
- this_round_query: str                    # 当前查询
- last_round_outputs: List[Dict]           # 上一轮输出
- last_round_functions: List[str]          # 上一轮函数列表
- this_round_functions: List[str]          # 当前要调用的函数
- tool_schemas: Dict[str, Dict]            # 工具 schema
```

**输出**:
```python
{
    "think": str,                   # 推理过程（CoT）
    "tool_calls": [                 # 函数调用列表
        {
            "function": str,
            "parameters": dict,
            "params_source": dict    # 参数来源标注
        }
    ],
    "token_usage": dict
}
```

**核心逻辑**:
1. **参数提取来源**:
   - 用户查询（`user_query`）
   - 上一轮输出（`last_round_output`）
   - 默认值/推断值

2. **参数来源标注** (`params_source`):
   ```json
   {
       "location": "user_query",
       "adults": "user_query"
   }
   ```
   或 `"EMPTY"` (全部为推断/默认)

3. **LLM 调用**:
   ```python
   model: DEFAULT_MODEL
   temperature: 0.3
   max_tokens: 1024
   ```

**当前假设**:
- ✅ 为所有 `this_round_functions` 生成调用
- ✅ 参数只能来自 query 或上一轮输出
- ✅ **不支持**同 turn 内函数间的参数传递

---

## 🎯 当前数据流

### Pipeline 概览
```
FSP Path (扁平)：[f1, f2, f3, f4, f5]
       ↓
转换为 Turns：[[f1], [f2], [f3], [f4], [f5]]  # 每个节点 = 1 turn
       ↓
对每个 Turn 执行：
       ↓
Turn 0: [f1]
  → Backward: 生成 query_0 (基于 f1 的schema)
  → Forward:  生成 f1(params)
  → Execute:  获取 output_0
       ↓
Turn 1: [f2]
  → Backward: 生成 query_1 (基于 f2 + output_0)
  → Forward:  生成 f2(params)  # params 可能来自 output_0
  → Execute:  获取 output_1
       ↓
...
```

### 关键特点
1. **线性依赖链**: Turn N 只依赖 Turn N-1
2. **单步处理**: 每个 turn 独立处理
3. **无嵌套**: 不支持 turn 内函数的输出作为同 turn 内其他函数的输入

---

## ⚠️ 与 MAGNET FSP v2 的差异

### FSP v2 数据结构
```python
fsp_final = [
    [f1, f2],           # Turn 0: Merge 后，2 个函数
    [f3, f4, f5],       # Turn 1: Merge + Insert，3 个函数
    [],                 # Turn 2: Split 插入的空 turn
    [f6]                # Turn 3
]
```

### 三种操作的挑战

#### 1. **Merge 操作** (多意图场景)
```python
Turn: [get_distance, set_navigation]
```

**问题**:
- 当前 Backward 假设 turn 内函数**并行调用**，无依赖
- 但 Merge 后的函数可能有**顺序依赖**（如 `set_navigation` 需要 `get_distance` 的输出）

**当前代码行为**:
```python
# generate_query_for_turn 生成的 query:
"查询从SF到SM的距离，并用这个距离设置导航"

# forward_to_fc_params 生成的调用:
# ❌ 问题：set_navigation 的 distance 参数无法从同 turn 的 get_distance 获取
# 只能从 query 或 last_round_output 获取
get_distance(from="SF", to="SM")
set_navigation(destination="SM", distance=???)  # distance 参数缺失！
```

#### 2. **Insert 操作** (嵌套函数)

**短依赖**:
```python
Turn: [get_distance, convert_unit]  # convert_unit 是 Insert 添加的
```

**问题**:
- `convert_unit` 的参数**必须**来自 `get_distance` 的输出
- 但当前 `forward_to_fc_params` 不支持同 turn 内的参数传递

**当前代码行为**:
```python
# Backward 生成的 query:
"查询从SF到SM多少公里"  # 用户只提到"公里"，未明确说"miles→km"

# Forward 生成的调用:
# ❌ 问题：convert_unit 的 miles 参数无法从 get_distance 获取
get_distance(from="SF", to="SM")  # 返回 miles
convert_unit(value=???, from_unit="miles", to_unit="km")  # value 缺失！
```

**长依赖**:
```python
Turn 2: [send_email, convert_unit]  # convert_unit 从 Turn 0 获取输入
```

**问题**:
- 当前代码只记录 `last_round_outputs`（Turn 1）
- 不支持跨多个 turn 的历史输出查找

#### 3. **Split 操作** (信息缺失)
```python
Turn 2: []  # 空 turn，标记为 miss_func 或 miss_params
```

**问题**:
- 当前代码假设每个 turn 至少有一个函数
- 遇到空 turn 会崩溃或跳过

**期望行为**:
```python
# Backward 应该生成：
query = "获取我的发票"

# Forward 应该输出：
{
    "think": "User requests invoice retrieval, but no retrieve_invoice function is available.",
    "tool_calls": []  # 空列表
}
```

---

## 🔧 适配方案

### 方案 A：最小改动（推荐用于快速验证）

**核心思路**: 将 turn 内的多个函数**拆分成多个 sub-steps**，保持当前线性流程

#### 1. 修改数据预处理
```python
def convert_fsp_to_linear_steps(fsp: List[List[int]]) -> List[List[int]]:
    """
    将 FSP 转换为线性 steps（每个 step 只有 1 个函数）

    输入: [[f1, f2], [f3], [], [f4]]
    输出: [[f1], [f2], [f3], [], [f4]]
    """
    linear_steps = []
    for turn in fsp:
        if not turn:  # 空 turn (Split 操作)
            linear_steps.append([])
        else:
            for func in turn:
                linear_steps.append([func])
    return linear_steps
```

**优点**:
- ✅ 无需修改 Backward/Forward 逻辑
- ✅ 保持参数依赖链完整

**缺点**:
- ❌ 丢失了 Merge 的**多意图**语义
- ❌ 生成的 query 是多个 atomic query，不是单个 merged query

---

### 方案 B：增强 Forward（支持同 turn 内依赖）

**核心思路**: 修改 `forward_to_fc_params` 支持同 turn 内的参数传递

#### 1. 引入执行顺序推断
```python
async def forward_to_fc_params_with_intra_turn_deps(
    this_round_query: str,
    last_round_outputs: List[Dict],
    this_round_functions: List[str],
    tool_schemas: Dict,
) -> Dict:
    """
    增强版 Forward：支持 turn 内函数的顺序执行和参数传递
    """
    # Step 1: 推断函数执行顺序
    execution_order = infer_execution_order(this_round_functions, tool_schemas)
    # 例如: [get_distance, convert_unit, set_navigation]

    # Step 2: 逐个生成函数调用，累积 turn 内输出
    turn_outputs = []
    tool_calls = []

    for func_name in execution_order:
        # 构建可用上下文：last_round + turn 内已执行的输出
        available_outputs = last_round_outputs + turn_outputs

        # 为单个函数生成参数
        tool_call = await generate_single_func_call(
            query=this_round_query,
            func_name=func_name,
            available_outputs=available_outputs,
            tool_schemas=tool_schemas
        )
        tool_calls.append(tool_call)

        # 立即执行获取输出（用于后续函数）
        output = await execute_function_call(tool_call)
        turn_outputs.append(output)

    return {
        "think": "...",
        "tool_calls": tool_calls,
        "turn_outputs": turn_outputs
    }
```

#### 2. 执行顺序推断
```python
def infer_execution_order(
    functions: List[str],
    tool_schemas: Dict,
) -> List[str]:
    """
    基于函数的输入输出类型推断执行顺序

    简单策略：按依赖关系拓扑排序
    """
    # 构建依赖图
    deps = {}
    for func in functions:
        deps[func] = find_dependencies(func, functions, tool_schemas)

    # 拓扑排序
    return topological_sort(deps)
```

**优点**:
- ✅ 支持 Merge 和 Insert 的参数依赖
- ✅ 生成的数据更接近真实场景

**缺点**:
- ❌ 需要立即执行函数（可能影响性能）
- ❌ 增加代码复杂度

---

### 方案 C：分阶段生成（论文原始方法）

**核心思路**: 严格按照 MAGNET 论文的 Back-and-Forth Translation 流程

#### 1. 修改 Backward（支持多意图）
```python
def build_prompt_for_merged_turn(
    turn_functions: List[str],  # 可能有多个函数
    last_round_outputs: List[Dict],
    tool_schemas: Dict,
    turn_type: str,  # "normal", "merged", "insert_short", "insert_long"
) -> str:
    """
    根据 turn 类型调整 prompt
    """
    if turn_type == "merged":
        # Merge 场景：生成多意图 query
        prompt = f"""
Generate a user query that naturally leads to calling multiple functions:
{', '.join(turn_functions)}

The query should express multiple intents in a single statement.
Example: "Search for flights from SF to NYC and book the cheapest one"
        """
    elif turn_type == "insert_short":
        # Insert 短依赖：生成隐式需求的 query
        prompt = f"""
Generate a user query that implicitly requires calling:
Primary function: {turn_functions[0]}
Nested function: {turn_functions[1]} (user doesn't explicitly mention this)

Example: User asks "How many km from SF to NYC"
→ Implicitly needs: get_distance (returns miles) + convert_unit (miles→km)
        """
    # ...
```

#### 2. 分步执行 + 参数传递
```python
async def process_turn_with_intra_deps(
    turn_functions: List[str],
    turn_type: str,
    last_round_outputs: List[Dict],
) -> Dict:
    """
    处理有内部依赖的 turn
    """
    # Step 1: Backward - 生成 query
    query = await generate_query_for_merged_turn(
        turn_functions, turn_type, last_round_outputs
    )

    # Step 2: Forward - 逐个生成 + 执行
    tool_calls = []
    turn_outputs = []

    for i, func in enumerate(turn_functions):
        # 为当前函数生成参数
        available_context = last_round_outputs + turn_outputs

        tool_call = await generate_func_params(
            query=query,
            func=func,
            context=available_context
        )
        tool_calls.append(tool_call)

        # 立即执行
        output = await execute_function(tool_call)
        turn_outputs.append(output)

    return {
        "query": query,
        "tool_calls": tool_calls,
        "outputs": turn_outputs
    }
```

**优点**:
- ✅ 完全符合 MAGNET 论文
- ✅ 保留 Merge/Insert/Split 的语义
- ✅ 生成的数据质量最高

**缺点**:
- ❌ 需要大幅重构代码
- ❌ 需要实时执行函数（增加耗时）

---

### 方案 D：后处理标注（最简单）

**核心思路**: 保持当前流程，只在最后标注 turn 类型

```python
def annotate_turn_operations(
    path_data: Dict,
    fsp_v2_metadata: Dict,
) -> Dict:
    """
    为生成的数据添加操作标注
    """
    for turn_idx, turn_data in enumerate(path_data["turns"]):
        # 从 FSP v2 metadata 获取操作信息
        operations = fsp_v2_metadata["turns"][turn_idx]["operations"]

        turn_data["annotations"] = {
            "has_merge": bool(operations.get("merge_logs")),
            "has_insert": bool(operations.get("insert_logs")),
            "has_split": bool(operations.get("split_logs")),
            "operation_types": operations.keys()
        }

    return path_data
```

**优点**:
- ✅ 无需修改核心逻辑
- ✅ 快速实现

**缺点**:
- ❌ 只是标注，不影响生成质量
- ❌ 无法修复参数依赖问题

---

## 📊 方案对比

| 方案 | 实现难度 | 数据质量 | 论文符合度 | 性能影响 | 推荐度 |
|------|---------|---------|-----------|---------|--------|
| **A. 拆分为线性** | ⭐ 极低 | ⭐⭐ 低 | ⭐ 低 | ✅ 无 | 🔧 快速验证 |
| **B. 增强 Forward** | ⭐⭐⭐ 中 | ⭐⭐⭐⭐ 高 | ⭐⭐⭐ 中 | ⚠️ 中等 | ⭐ 推荐 |
| **C. 完整重构** | ⭐⭐⭐⭐⭐ 极高 | ⭐⭐⭐⭐⭐ 最高 | ⭐⭐⭐⭐⭐ 完全 | ⚠️⚠️ 高 | 🎯 长期目标 |
| **D. 后处理标注** | ⭐ 极低 | ⭐ 极低 | ⭐ 低 | ✅ 无 | ❌ 不推荐 |

---

## 🎯 推荐实施路径

### 阶段 1：快速验证 (1-2天)
**目标**: 验证 FSP v2 数据是否可用

**方案**: 方案 A - 拆分为线性
```python
# 在 process_single_path_v1 开头添加：
if "fsp_final" in path_data:
    fsp = path_data["fsp_final"]
    linear_steps = convert_fsp_to_linear_steps(fsp)
    path_data["turns"] = linear_steps
```

**验证指标**:
- ✅ 代码能运行
- ✅ 生成的 query 合理
- ✅ 参数能正确提取

### 阶段 2：增强参数传递 (3-5天)
**目标**: 支持 turn 内函数依赖

**方案**: 方案 B - 增强 Forward
1. 实现 `infer_execution_order()`
2. 修改 `forward_to_fc_params()` 支持顺序执行
3. 添加 turn 内输出累积

**验证指标**:
- ✅ Merge 场景的参数正确传递
- ✅ Insert 短依赖的参数正确获取
- ✅ 生成数据通过人工检查

### 阶段 3：完整实现 (1-2周)
**目标**: 完全符合 MAGNET 论文

**方案**: 方案 C - 分阶段生成
1. 重构 Backward 支持多意图
2. 实现分步执行 + 参数传递
3. 添加 Split 操作的特殊处理

---

## 🚨 特殊情况处理

### 1. Split 操作（空 turn）
```python
def handle_empty_turn(
    turn_idx: int,
    last_round_outputs: List[Dict],
    miss_type: str,  # "miss_func" or "miss_params"
) -> Dict:
    """
    处理 Split 插入的空 turn
    """
    if miss_type == "miss_func":
        query = generate_missing_function_query()
        # 例如: "获取我的发票"

        return {
            "query": query,
            "tool_calls": [],
            "response": "I don't have a function to retrieve invoices. Could you clarify..."
        }
    elif miss_type == "miss_params":
        query = generate_missing_params_query()
        # 例如: "预订酒店"（缺少 location, date 等参数）

        return {
            "query": query,
            "tool_calls": [],
            "response": "To book a hotel, I need more information: location, check-in date..."
        }
```

### 2. 长依赖 Insert
```python
def handle_long_dependency_insert(
    turn_idx: int,
    nested_func: str,
    source_turn_idx: int,
    all_turn_outputs: List[List[Dict]],
) -> Dict:
    """
    处理长依赖的 Insert（函数从几个 turn 前获取输入）
    """
    # 获取源 turn 的输出
    source_outputs = all_turn_outputs[source_turn_idx]

    # 生成参数时包含源 turn 的输出
    tool_call = generate_func_call(
        func=nested_func,
        context=source_outputs,
        note=f"Uses output from Turn {source_turn_idx}"
    )

    return tool_call
```

---

## 📝 代码修改清单

### 必须修改的函数

#### 1. `process_single_path_v1()`
```python
# 当前: 假设 path 是扁平列表
path = path_data["path"]

# 修改后: 支持 FSP 格式
if "fsp_final" in path_data:
    fsp = path_data["fsp_final"]
    turns = fsp  # 直接使用 FSP
else:
    # 向后兼容
    path = path_data["path"]
    turns = [[f] for f in path]
```

#### 2. `generate_query_for_turn()`
```python
# 添加参数: turn_type
def generate_query_for_turn(
    ...,
    turn_type: Optional[str] = None,  # 新增
    turn_metadata: Optional[Dict] = None,  # 新增
):
    # 根据 turn_type 调整 prompt
    if turn_type == "merged":
        prompt = build_merged_turn_prompt(...)
    elif turn_type == "insert_short":
        prompt = build_insert_short_prompt(...)
    # ...
```

#### 3. `forward_to_fc_params()`
```python
# 修改: 支持顺序执行
async def forward_to_fc_params(
    ...,
    execution_mode: str = "parallel",  # 新增: "parallel" | "sequential"
):
    if execution_mode == "sequential":
        return await forward_with_intra_turn_deps(...)
    else:
        # 当前逻辑（并行）
        ...
```

### 新增的函数

```python
def convert_fsp_to_linear_steps(fsp: List[List[int]]) -> List[List[int]]:
    """拆分 FSP 为线性 steps"""
    pass

def infer_execution_order(functions: List[str], tool_schemas: Dict) -> List[str]:
    """推断函数执行顺序"""
    pass

async def forward_with_intra_turn_deps(...) -> Dict:
    """支持 turn 内依赖的 Forward"""
    pass

def handle_empty_turn(...) -> Dict:
    """处理 Split 操作的空 turn"""
    pass
```

---

## 🔗 相关文件

需要同步修改的文件：
1. `backward_to_query.py` - 主要修改
2. `generate_fsp_v2.py` - 确保输出格式兼容
3. `random_walker.py` - 提供 FSP 操作的元数据

---

## 📚 参考资料

- **MAGNET 论文**: Section 3.3 (Node Operations)
  - Merge: Section 3.3.2
  - Insert: Section 3.3.1
  - Split: Section 3.3.3
- **Back-and-Forth Translation**: Section 3.4

---

**报告生成时间**: 2026-01-07
**作者**: Claude Sonnet 4.5
