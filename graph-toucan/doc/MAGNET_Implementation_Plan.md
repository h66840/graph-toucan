# MAGNET Query 生成实现方案

## 📋 文档概述

**目的**：设计一个完整的实现方案，解决 MAGNET 论文中 Insert 和 Merge 操作的 query 生成风格区分问题。

**基于研究**：[MAGNET_Insert_Merge_Query_Generation_Analysis.md](./MAGNET_Insert_Merge_Query_Generation_Analysis.md)

**核心挑战**：当一个 turn 经过 Merge 和/或 Insert 操作后，如何生成符合预期风格的 query？

---

## 🎯 设计目标

### 主要目标

1. **风格区分**：Insert 生成隐式 query，Merge 生成显式 query
2. **复合操作支持**：正确处理同时有 Merge + Insert 的 turn
3. **鲁棒性**：即使风格不完美，也能生成合理的训练数据
4. **可验证性**：便于分析生成的 query 质量

### 次要目标

1. 代码清晰可维护
2. 便于调试和迭代
3. 性能合理（避免过多 LLM 调用）
4. 兼容论文的其他部分（Forward、Split 等）

---

## 🔍 核心问题分析

### 问题1：Turn 类型的多样性

**现状**：
```
Turn 可能的状态：
- Normal: 单个函数，无特殊操作
- Merged: 2+ 函数，经过 Merge 操作
- Insert Short: 2+ 函数，有短依赖 Insert
- Insert Long: 2+ 函数，有长依赖 Insert
- Merged + Insert: 2+ 函数，同时有 Merge 和 Insert ⚠️ 复杂！
- Empty: 空 turn，Split 操作
```

**当前实现问题**：
- `detect_turn_type()` 只返回第一个匹配的类型
- 会遗漏复合操作（Merge + Insert）

**解决方案**：
- 改为 `detect_turn_operations()`，返回**所有操作**的列表
- 同时返回 `primary_style` 用于选择 prompt 模板

---

### 问题2：Query 风格的定义

**Insert (隐式风格)**：
```
示例：
Functions: [get_distance(), convert_unit()]
Query: "查询从SF到SM多少公里"
      ↑ 只提到最终目标（公里数）
      ↑ 不提单位转换

特征：
- 用户只关心最终结果
- 中间步骤是隐式的、自动的
- Nested function 不在 query 中体现
```

**Merge (显式风格)**：
```
示例：
Functions: [get_distance(), set_navigation()]
Query: "查询SF到SM的距离并用这个距离设置导航"
      ↑ 明确提到两个动作

特征：
- 用户有多个明确意图
- 所有函数都在 query 中体现
- 用 "并且"/"然后" 等连接词
```

**Merged + Insert (混合风格)**：
```
示例：
Functions: [get_weather_forecast(), get_weather(), get_live_temp()]
           ↑ merge           ↑ merge    ↑ insert

Query: "查询天气预报和当前天气"
      ↑ forecast 和 weather 显式
      ↑ live_temp（温度转换）隐式

规则：
- Merged 的函数 → 显式提到
- Inserted 的函数 → 隐式（不提或简略）
```

---

### 问题3：如何让 LLM 区分这些风格？

**论文的模糊性**：
- ✅ 提到了 "examples"
- ❌ 没有展示具体的 examples
- ❌ 没有说明如何标记操作类型

**我们的推断（可能性排序）**：
1. **In-Context Learning (70%)** - 通过 few-shot examples
2. **语义自动推断 (20%)** - LLM 自然理解函数关系
3. **多样性接受 (10%)** - 不严格控制，接受各种风格

**我们的选择**：
- 主要使用 **In-Context Learning**
- 辅助使用 **显式风格指导**
- 接受 **一定程度的多样性**

---

## 🏗️ 实现架构

### 整体流程

```
┌─────────────────────────────────────────────────────────┐
│  输入：FSP v2 数据                                       │
│  - fsp_final: List[List[int]]                           │
│  - merge_logs, insert_logs, split_logs                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  步骤1：检测 Turn 操作                                   │
│  detect_turn_operations(turn_idx, path_data)            │
│                                                          │
│  输出：                                                  │
│  {                                                       │
│    "operations": ["merge", "insert_short"],             │
│    "primary_style": "merged_with_insert",               │
│    "merge_info": {...},                                 │
│    "insert_info": [{...}]                               │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  步骤2：选择 Examples 和风格指导                         │
│  select_examples_and_instructions(turn_operations)      │
│                                                          │
│  - 根据 primary_style 选择相应的 examples               │
│  - 添加明确的风格指导语句                               │
│  - 复合情况使用混合 examples                            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  步骤3：构建 Prompt                                      │
│  build_prompt_for_turn(                                 │
│      turn_operations,                                   │
│      turn_functions,                                    │
│      history,                                           │
│      examples,                                          │
│      style_instruction                                  │
│  )                                                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  步骤4：调用 LLM 生成 Query                              │
│  generate_query_for_turn_magnet()                       │
│                                                          │
│  输出：                                                  │
│  {                                                       │
│    "user_query": "...",                                 │
│    "chose_func": [...],                                 │
│    "reason": "...",                                     │
│    "style_metadata": {  ← 新增                          │
│        "expected_style": "implicit",                    │
│        "operations": [...]                              │
│    }                                                     │
│  }                                                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  步骤5（可选）：风格验证                                 │
│  verify_query_style(query, turn_operations)             │
│                                                          │
│  - 检查是否符合预期风格                                 │
│  - 不符合时重试（最多1-2次）                            │
│  - 记录不匹配的案例供分析                               │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  步骤6：Forward 执行（顺序 + 参数传递）                  │
│  forward_with_sequential_execution()                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📐 详细设计

### 设计1：Turn 操作检测

#### 函数签名

```python
def detect_turn_operations(
    turn_idx: int,
    turn_functions: List[str],
    path_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    检测 turn 应用了哪些操作

    返回格式：
    {
        "operations": List[str],           # 所有操作：["merge", "insert_short"]
        "primary_style": str,              # 主要风格："merged_with_insert"
        "merge_info": Dict or None,        # Merge 的详细信息
        "insert_info": List[Dict],         # Insert 的详细信息（可能多个）
        "is_empty": bool,                  # 是否是空 turn
    }
    """
```

#### 实现逻辑

```python
# 1. 检查是否是空 turn
if not turn_functions:
    return {
        "operations": ["split"],
        "primary_style": "empty",
        "is_empty": True,
        ...
    }

# 2. 收集所有操作
operations = []

# 检查 merge
for log in path_data["merge_logs"]:
    if log["turn_idx"] == turn_idx:
        operations.append("merge")
        merge_info = log

# 检查 insert（可能有多个）
insert_info = []
for log in path_data["insert_logs"]:
    if log["target_turn_idx"] == turn_idx:
        if log["insert_type"] == "long_dependency":
            operations.append("insert_long")
        else:
            operations.append("insert_short")
        insert_info.append(log)

# 3. 确定主要风格
primary_style = determine_primary_style(operations)
```

#### Primary Style 决策树

```
operations 包含哪些？
├─ []                     → "normal"
├─ ["merge"]              → "merged"
├─ ["insert_short"]       → "insert_short"  (隐式风格)
├─ ["insert_long"]        → "insert_long"   (隐式风格)
├─ ["merge", "insert_*"]  → "merged_with_insert" (混合风格)
└─ ["insert_short", "insert_long"] → "insert_mixed" (隐式风格)
```

---

### 设计2：Examples 库

#### Examples 结构

```python
EXAMPLES = {
    # Short Dependency: 同turn内的嵌套函数
    "short_dependency": [
        {
            "name": "Unit Conversion",
            "functions": ["get_distance(from, to)", "convert_unit(value, from, to)"],
            "query": "How many kilometers from San Francisco to San Mateo?",
            "explanation": "User wants kilometers. The miles→km conversion is implicit.",
            "anti_example": "Get the distance in miles and convert it to kilometers",
            "tags": ["implicit", "utility_function", "same_turn"]
        },
        {
            "name": "Price Check before Booking",
            "functions": ["get_flight_cost(from, to)", "book_flight(cost, from, to)"],
            "query": "Book a business class flight from LA to NYC on April 15th",
            "explanation": "User wants to book. Price check is automatic prerequisite.",
            "anti_example": "Check flight prices and then book the flight",
            "tags": ["implicit", "prerequisite", "same_turn"]
        },
        {
            "name": "Data Formatting",
            "functions": ["query_database(table)", "format_json_to_table(data)"],
            "query": "Get customer records in a readable table format",
            "explanation": "User wants formatted output. JSON→table conversion is implicit.",
            "anti_example": "Query the database and format the results as a table",
            "tags": ["implicit", "formatting", "same_turn"]
        },
    ],

    # Long Dependency: 跨turn引用历史
    "long_dependency": [
        {
            "name": "Distance → Range Search",
            "history_turns": [
                {
                    "turn": 0,
                    "query": "How many kilometers from SF to San Mateo?",
                    "functions": ["get_distance", "convert_unit"],
                    "output": {"distance": 25.4, "unit": "km"}
                },
                {
                    "turn": 1,
                    "query": "Send this information to my colleague",
                    "functions": ["send_email"]
                }
            ],
            "current_turn": 2,
            "functions": ["cities_by_range"],
            "query": "Using that distance, find all cities within that range from San Francisco",
            "explanation": "References Turn 0's distance (25.4km) using 'that distance' instead of repeating the value.",
            "anti_example": "Find cities within 25.4 kilometers from San Francisco",
            "key_reference": "that distance",
            "dependency_source": "Turn 0, distance output",
            "tags": ["cross_turn", "pronoun_reference", "long_dependency"]
        },
        {
            "name": "Booking → Cancellation",
            "history_turns": [
                {
                    "turn": 0,
                    "query": "Book a flight to NYC on April 15th",
                    "functions": ["get_flight_cost", "book_flight"],
                    "output": {"booking_id": "3426812", "status": true}
                },
                {
                    "turn": 1,
                    "query": "Message my friend Joey about the trip",
                    "functions": ["send_message"]
                },
                {
                    "turn": 2,
                    "query": "Book a hotel near Times Square",
                    "functions": ["search_hotels", "book_hotel"]
                }
            ],
            "current_turn": 3,
            "functions": ["cancel_booking"],
            "query": "Cancel my New York trip due to unforeseen circumstances",
            "explanation": "References Turn 0's booking using 'my New York trip', not the booking ID.",
            "anti_example": "Cancel booking 3426812",
            "key_reference": "my New York trip",
            "dependency_source": "Turn 0, booking_id",
            "tags": ["cross_turn", "contextual_reference", "long_dependency"]
        },
        {
            "name": "Query → Export",
            "history_turns": [
                {
                    "turn": 0,
                    "query": "Get all customer records from the database",
                    "functions": ["query_database", "format_json"],
                    "output": {"records": [...], "count": 150}
                },
                {
                    "turn": 1,
                    "query": "Analyze the registration date patterns",
                    "functions": ["analyze_data"]
                }
            ],
            "current_turn": 2,
            "functions": ["export_to_pdf"],
            "query": "Export those customer records to a PDF report",
            "explanation": "Uses 'those records' to reference Turn 0's data without repeating details.",
            "anti_example": "Export the 150 customer records to PDF",
            "key_reference": "those customer records",
            "dependency_source": "Turn 0, records data",
            "tags": ["cross_turn", "demonstrative_reference", "long_dependency"]
        },
    ],

    # Merged: 多意图并列
    "sequential": [
        {
            "name": "Distance and Navigation",
            "functions": ["get_distance(from, to)", "set_navigation(distance)"],
            "query": "Find the distance from SF to SM and set up navigation",
            "explanation": "Two explicit intents: find distance AND set navigation.",
            "tags": ["explicit", "multiple_intents"]
        },
        {
            "name": "Search and Share",
            "functions": ["search_flights(from, to)", "send_message(content, to)"],
            "query": "Search flights to NYC and send the results to my friend",
            "explanation": "Two independent actions the user wants to do.",
            "tags": ["explicit", "independent_actions"]
        },
        {
            "name": "Book and Insure",
            "functions": ["book_hotel(location, date)", "purchase_insurance(booking_id)"],
            "query": "Book a hotel in Paris for next week and get travel insurance",
            "explanation": "Both actions explicitly mentioned.",
            "tags": ["explicit", "related_tasks"]
        },
    ],
}
```

#### Examples 选择策略

```python
def select_examples(primary_style: str, num_examples: int = 3) -> str:
    """
    根据 primary_style 选择合适的 examples

    策略：
    - insert_short → short_dependency examples (同turn内嵌套)
    - insert_long → long_dependency examples (跨turn引用)
    - merged → sequential examples (多意图并列)
    - merged_with_insert → 混合 examples
    - normal → 不提供 examples（或通用 examples）
    """

    if primary_style == "insert_short":
        # 选择 short dependency examples
        examples = random.sample(EXAMPLES["short_dependency"], num_examples)

    elif primary_style == "insert_long":
        # 选择 long dependency examples
        # ⚠️ 注意：long dependency 的 examples 包含历史上下文
        examples = random.sample(EXAMPLES["long_dependency"], num_examples)

    elif primary_style == "merged":
        # 选择 sequential examples
        examples = random.sample(EXAMPLES["sequential"], num_examples)

    elif primary_style == "merged_with_insert":
        # 混合：1 short + 1 long + 1 sequential
        examples = (
            random.sample(EXAMPLES["short_dependency"], 1) +
            random.sample(EXAMPLES["long_dependency"], 1) +
            random.sample(EXAMPLES["sequential"], 1)
        )

    else:  # normal
        examples = []

    return format_examples_for_prompt(examples)


def format_examples_for_prompt(examples: List[Dict]) -> str:
    """
    格式化 examples 为 prompt 文本

    ⚠️ Long dependency examples 需要特殊格式化（包含历史）
    """
    formatted_parts = []

    for i, ex in enumerate(examples, 1):
        # 检查是否是 long dependency example
        if "history_turns" in ex:
            # 格式化历史上下文
            history_str = "\n".join([
                f"  Turn {h['turn']}: {h['query']}\n"
                f"  Functions: {h['functions']}\n"
                f"  Output: {h['output']}"
                for h in ex["history_turns"]
            ])

            formatted = f"""
Example {i}: {ex['name']} (Long Dependency)

Previous Conversation:
{history_str}

Current Turn {ex['current_turn']}:
Functions: {ex['functions']}
Query: "{ex['query']}"

Why: {ex['explanation']}
Key Reference: "{ex['key_reference']}" → {ex['dependency_source']}

❌ Bad: "{ex['anti_example']}"
"""
        else:
            # 普通 example（short dependency 或 sequential）
            formatted = f"""
Example {i}: {ex['name']}

Functions: {ex['functions']}
Query: "{ex['query']}"

Why: {ex['explanation']}

{f"❌ Bad: \"{ex['anti_example']}\"" if "anti_example" in ex else ""}
"""

        formatted_parts.append(formatted)

    return "\n".join(formatted_parts)
```

---

### 设计3：风格指导语句

#### 指导语句库

```python
STYLE_INSTRUCTIONS = {
    "insert_short": """
**IMPORTANT - Query Style for Nested Functions (Short Dependency)**:

Characteristics:
- User has a SINGLE, CLEAR GOAL
- Intermediate/helper functions are IMPLICIT and automatic
- Query only mentions the FINAL outcome the user wants
- All functions execute in the SAME turn

Examples:
✓ "Get kilometers from San Francisco to San Mateo"
   (NOT "Get miles and convert to kilometers")

✓ "Book a business class flight from LA to NYC"
   (NOT "Check flight cost and book")

✓ "Get customer records in table format"
   (NOT "Query database and format to table")

Rules:
- Focus on the end result
- Don't mention intermediate steps
- Keep it natural and concise
- Assume helper functions are automatic
""",

    "insert_long": """
**IMPORTANT - Query Style for Long Dependency (Cross-Turn Reference)**:

Characteristics:
- User references PREVIOUS results from earlier turns
- Uses PRONOUNS and INDIRECT REFERENCES
- Does NOT repeat specific values or IDs
- The referenced output is from a DIFFERENT turn (not current)

Referencing Patterns:
- "that <noun>" → "that distance", "that booking"
- "the previous <noun>" → "the previous search"
- "my <noun>" → "my trip", "my reservation"
- "those <noun>" → "those results", "those records"

Examples:
✓ "Using that distance, find cities within that range"
   (NOT "Using 25.4km, find cities within 25.4km")

✓ "Cancel my New York trip"
   (NOT "Cancel booking 3426812")

✓ "Export those customer records to PDF"
   (NOT "Export the 150 records to PDF")

Rules:
- Reference history naturally
- Use context-aware language
- Assume the model remembers previous outputs
- Don't repeat specific values
- Make it sound like a natural conversation continuation
""",

    "merged": """
**IMPORTANT - Query Style for Multiple Intents**:

Characteristics:
- User has MULTIPLE EXPLICIT intents
- All actions are clearly mentioned
- Uses connecting words

Examples:
✓ "Find the distance from SF to SM and set up navigation"
✓ "Search for flights to NYC and send results to my friend"
✓ "Book a hotel in Paris and get travel insurance"

Rules:
- Explicitly mention ALL actions/intents
- Use connecting words: "and", "then", "also", "after that"
- All functions should be reflected in the query
- Both/all actions are user's explicit goals
""",

    "merged_with_insert": """
**IMPORTANT - Query Style for Merged with Nested Functions**:

Characteristics:
- Some functions are EXPLICIT (from merge)
- Some functions are IMPLICIT (from insert)
- Merged functions → mention explicitly
- Inserted/helper functions → keep implicit

Example:
✓ "Get weather forecast and current temperature"
   → "forecast" and "temperature" are explicit (merged)
   → unit conversion is implicit (inserted)

Rules:
- Mention merged functions explicitly
- Keep helper/utility functions implicit
- Use connecting words for merged functions
- Natural combination of explicit and implicit
""",

    "normal": """
**Query Style**:
- Generate a natural query for the given function(s)
- Provide all necessary parameter information
- Keep the query concise and user-friendly
""",
}
```

#### 使用方式

```python
def get_style_instruction(primary_style: str) -> str:
    """获取风格指导语句"""
    return STYLE_INSTRUCTIONS.get(primary_style, STYLE_INSTRUCTIONS["normal"])
```

---

### 设计4：Prompt 构建

#### 完整 Prompt 结构

```markdown
[System Instructions]
- 角色定义
- 基本规则

[Previous Turn History]  (如果不是第一个 turn)
- Turn 0: ...
- Turn 1: ...
- Last Turn Outputs: ...

[Examples]  ← 根据 primary_style 动态选择
Example 1: ...
Example 2: ...
Example 3: ...

[Style Instruction]  ← 根据 primary_style 动态选择
**IMPORTANT - Query Style**:
...

[Current Turn]
Functions: [func1, func2, ...]
Required Parameters: ...
Optional Parameters: ...

[Output Format]
user query: ...
chose func: ...
reason: ...
```

#### 实现函数

```python
def build_prompt_for_turn(
    turn_idx: int,
    turn_operations: Dict[str, Any],  # 从 detect_turn_operations 获取
    turn_functions: List[str],
    all_turn_outputs: List[List[Dict]],
    tool_schemas: Dict[str, Dict],
    error_feedback: Optional[str] = None,
) -> str:
    """
    构建完整的 prompt
    """

    # 1. 基础指令
    system_instructions = get_system_instructions()

    # 2. 历史信息
    history_block = build_history_block(turn_idx, all_turn_outputs)

    # 3. Examples（根据 primary_style）
    primary_style = turn_operations["primary_style"]
    examples_block = select_examples(primary_style, num_examples=3)

    # 4. 风格指导
    style_instruction = get_style_instruction(primary_style)

    # 5. 当前 turn 信息
    current_turn_block = build_current_turn_block(
        turn_functions,
        tool_schemas
    )

    # 6. 错误反馈（如果有）
    error_block = build_error_feedback_block(error_feedback)

    # 7. 组装
    prompt = f"""
{system_instructions}

{history_block}

{examples_block}

{style_instruction}

{current_turn_block}

{error_block}

Output format (strictly follow):
user query: <your natural language query here>
chose func: <comma-separated function names>
reason: <explanation of your choices and how they relate to the query style>
"""

    return prompt
```

---

### 设计5：风格验证（可选）

#### 验证策略

**目标**：检查生成的 query 是否符合预期风格

**方法**：轻量级的规则检查 + LLM 验证

#### 规则检查

```python
def quick_style_check(
    query: str,
    turn_functions: List[str],
    primary_style: str,
) -> bool:
    """
    快速风格检查（基于规则）
    """

    if primary_style in ["insert_short", "insert_long"]:
        # 检查是否过度显式
        # 如果 query 中明确提到了第二个函数的名字 → 不符合
        nested_func = turn_functions[-1]  # 最后一个是 inserted
        func_keywords = extract_keywords(nested_func)

        # 简单检查：第二个函数的关键词是否出现在 query 中
        for keyword in func_keywords:
            if keyword.lower() in query.lower():
                return False  # 过度显式
        return True

    elif primary_style == "merged":
        # 检查是否明确提到多个意图
        # 至少应该有连接词：and, then, also, after
        connectors = ["and", "then", "also", "after", "并", "然后", "还要", "接着"]
        has_connector = any(conn in query.lower() for conn in connectors)

        return has_connector

    else:
        return True  # 其他情况不检查
```

#### LLM 验证（可选，成本高）

```python
async def llm_style_verification(
    query: str,
    turn_functions: List[str],
    primary_style: str,
) -> Tuple[bool, str]:
    """
    使用 LLM 验证风格（可选，仅用于关键 turn）
    """

    verification_prompt = f"""
You are a query style checker.

Query: "{query}"
Functions: {turn_functions}
Expected Style: {primary_style}

Question: Does the query match the expected style?
- If style is "insert/nested": Query should only mention final goal, not intermediate steps
- If style is "merged/sequential": Query should explicitly mention all actions

Answer: yes/no
Reason: (brief explanation)
"""

    result = await call_llm(
        verification_prompt,
        model="gpt-4o-mini",  # 使用更便宜的模型
        temperature=0,
        max_tokens=100,
    )

    is_valid = "yes" in result["content"].lower()
    reason = result["content"]

    return is_valid, reason
```

#### 重试机制

```python
async def generate_query_with_validation(
    turn_operations: Dict,
    turn_functions: List[str],
    ...,
    max_retries: int = 1,  # 适度重试，避免过多成本
    enable_llm_verification: bool = False,
) -> Dict[str, Any]:
    """
    生成 query 并验证风格
    """

    primary_style = turn_operations["primary_style"]

    for attempt in range(max_retries + 1):
        # 生成 query
        query_result = await generate_query_for_turn_magnet(...)
        user_query = query_result["user_query"]

        # 不需要验证的场景
        if primary_style in ["normal", "empty"]:
            return query_result

        # 快速规则检查
        is_valid_quick = quick_style_check(
            user_query,
            turn_functions,
            primary_style
        )

        if not is_valid_quick:
            print(f"[Style Check] Quick check failed at attempt {attempt+1}")
            if attempt < max_retries:
                continue  # 重试

        # LLM 验证（可选）
        if enable_llm_verification and primary_style in ["insert_short", "merged"]:
            is_valid_llm, reason = await llm_style_verification(
                user_query,
                turn_functions,
                primary_style,
            )

            if not is_valid_llm:
                print(f"[Style Check] LLM verification failed: {reason}")
                if attempt < max_retries:
                    continue  # 重试

        # 通过验证或最后一次尝试
        return query_result

    # 都失败了，接受最后一次的结果
    return query_result
```

---

## 📊 数据结构

### 增强的返回格式

```python
# generate_query_for_turn_magnet 的返回格式
{
    "user_query": "查询从SF到SM多少公里",
    "chose_func": ["get_distance", "convert_unit"],
    "reason": "User wants distance in kilometers...",
    "raw_output": "...",
    "token_usage": {...},

    # 新增：风格元数据
    "style_metadata": {
        "operations": ["insert_short"],
        "primary_style": "insert_short",
        "expected_style": "implicit",
        "style_check_passed": True,
        "style_check_attempts": 1,
    }
}
```

### 最终保存格式

```json
{
  "path_idx": 0,
  "turns": [
    {
      "turn_idx": 0,
      "turn_type": "normal",
      "operations": [],
      "functions": ["func1"],
      "user_query": "...",
      "chose_func": ["func1"],
      "reason": "...",
      "tool_calls": [...],
      "outputs": [...]
    },
    {
      "turn_idx": 1,
      "turn_type": "merged_with_insert",
      "operations": ["merge", "insert_short"],
      "functions": ["func2", "func3", "func4"],
      "user_query": "...",
      "chose_func": ["func2", "func3", "func4"],
      "reason": "...",
      "style_metadata": {
        "primary_style": "merged_with_insert",
        "expected_style": "mixed",
        "merge_info": {...},
        "insert_info": [{...}]
      },
      "tool_calls": [...],
      "outputs": [...]
    }
  ],
  "token_usage": {...},
  "statistics": {...}
}
```

---

## 🎬 实施计划

### 阶段1：最小可行方案 (MVP)

**目标**：快速验证基本流程能跑通

**实现内容**：
1. ✅ 修改 `detect_turn_operations()` - 返回完整操作信息
2. ✅ 添加简单的风格指导语句（不用 examples）
3. ✅ 在 prompt 中直接添加风格指导
4. ⏭️ 跳过验证机制
5. ✅ 测试 5-10 个路径，观察生成效果

**预期效果**：
- 能区分不同的 primary_style
- query 生成的风格有明显差异
- 数据格式正确

**成功标准**：
- 代码能运行不报错
- 生成的 query 在风格上有区分（目测）
- 至少 60% 的 query 符合预期风格

**时间估计**：2-3 小时

---

### 阶段2：加入 Examples

**目标**：通过 in-context learning 提升风格一致性

**实现内容**：
1. ✅ 设计 3-5 个高质量的 nested examples
2. ✅ 设计 3-5 个高质量的 sequential examples
3. ✅ 实现 `select_examples()` 逻辑
4. ✅ 修改 `build_prompt_for_turn()` 加入 examples
5. ✅ 测试 20-30 个路径，对比有无 examples 的差异

**预期效果**：
- query 风格更加一致
- 隐式/显式的区分更加明显
- 减少边界情况的错误

**成功标准**：
- 80%+ 的 insert turns 生成隐式 query
- 80%+ 的 merged turns 生成显式 query
- 人工检查 50 个 query，质量满意

**时间估计**：3-4 小时

---

### 阶段3：复合操作优化

**目标**：正确处理 Merged + Insert 的复杂场景

**实现内容**：
1. ✅ 设计混合 examples（merged_with_insert）
2. ✅ 优化 `determine_primary_style()` 逻辑
3. ✅ 添加特殊的风格指导（区分哪些显式、哪些隐式）
4. ✅ 测试只包含复合操作的路径

**预期效果**：
- 复合操作的 turn 生成合理的 query
- Merged 的函数显式，Inserted 的函数隐式
- 不会过度复杂或混乱

**成功标准**：
- 复合操作的 query 人工检查满意
- 至少 70% 的复合 turn 风格正确

**时间估计**：2-3 小时

---

### 阶段4：验证和质量控制（可选）

**目标**：添加自动化的质量检查

**实现内容**：
1. ✅ 实现 `quick_style_check()` 规则检查
2. ⚠️ 实现重试机制（max_retries=1）
3. ⏭️ 可选：LLM 验证（仅用于难例）
4. ✅ 添加风格统计和分析工具
5. ✅ 批量测试，生成质量报告

**预期效果**：
- 自动过滤明显不符合风格的 query
- 统计数据：X% insert 隐式，Y% merge 显式
- 识别需要改进的 cases

**成功标准**：
- 验证通过率 > 90%
- 不符合的 cases 有记录供分析
- 重试不超过 10% 的 turns

**时间估计**：3-4 小时

---

### 阶段5：大规模生成和分析

**目标**：生成完整的训练数据

**实现内容**：
1. ✅ 处理全部 4,163 条路径
2. ✅ 生成完整的 JSONL 数据
3. ✅ 统计分析：
   - 各种操作类型的分布
   - 风格一致性统计
   - Token 使用量
4. ✅ 质量抽样检查（随机 100 条）
5. ✅ 与论文的数据对比（如果有参考）

**时间估计**：取决于 LLM API 速度，预计 4-8 小时

---

## 🔧 代码修改清单

### 需要修改的函数

#### 1. `detect_turn_operations()` (新函数，替代 `detect_turn_type`)

```python
位置：backward_to_query_magnet.py, ~line 100

修改：
- 检测所有操作，不只是第一个
- 返回完整的操作信息字典
- 处理复合操作

新增字段：
- operations: List[str]
- primary_style: str
- merge_info: Dict
- insert_info: List[Dict]
```

#### 2. `build_prompt_for_turn()` (大幅修改)

```python
位置：backward_to_query_magnet.py, ~line 200

修改：
- 接受 turn_operations 参数（而非 turn_type）
- 动态选择 examples
- 动态选择风格指导
- 区分不同的 primary_style

新增参数：
- turn_operations: Dict
```

#### 3. `generate_query_for_turn_magnet()` (小修改)

```python
位置：backward_to_query_magnet.py, ~line 400

修改：
- 参数从 turn_type 改为 turn_operations
- 返回值添加 style_metadata

新增返回字段：
- style_metadata: Dict
```

#### 4. `process_single_fsp_path()` (小修改)

```python
位置：backward_to_query_magnet.py, ~line 800

修改：
- 调用 detect_turn_operations() 而非 detect_turn_type()
- 传递完整的 turn_operations 给后续函数
- 保存操作信息到输出
```

### 需要新增的函数

```python
# 1. Examples 管理
def get_nested_examples() -> List[Dict]
def get_sequential_examples() -> List[Dict]
def select_examples(primary_style: str, num: int) -> str
def format_examples_for_prompt(examples: List[Dict]) -> str

# 2. 风格指导
def get_style_instruction(primary_style: str) -> str

# 3. 风格检查（可选）
def quick_style_check(query: str, functions: List[str], style: str) -> bool
async def llm_style_verification(...) -> Tuple[bool, str]
async def generate_query_with_validation(...) -> Dict

# 4. 辅助函数
def determine_primary_style(operations: List[str]) -> str
def extract_keywords(func_name: str) -> List[str]
```

---

## ❓ 待讨论的问题

### 问题1：Examples 的数量和质量

**问题**：
- 每个类型应该准备多少个 examples？
- Examples 应该多详细？（函数签名、参数、输出？）
- Examples 应该多样化（不同领域）还是同质化（同一领域）？

**选项**：
- A. 少而精：每类 3 个，极高质量
- B. 多而全：每类 5-8 个，覆盖各种情况
- C. 动态选择：根据当前函数的类别选择相关的 examples

**我的建议**：先 A，然后根据效果扩展到 C

---

### 问题2：验证的必要性

**问题**：
- 是否需要验证机制？会增加成本和复杂度
- 如果验证，应该多严格？
- 是否接受一定比例的"不完美"数据？

**选项**：
- A. 不验证，接受多样性（符合论文可能的做法）
- B. 轻量级规则检查（快速、无成本）
- C. LLM 验证（准确但成本高）

**我的建议**：阶段1-2 用 A，阶段3-4 加入 B，C 仅用于难例或最终质量检查

---

### 问题3：Merged + Insert 的处理策略

**问题**：
- 如何判断哪些函数应该显式、哪些隐式？
- 如果有 3+ 个函数，其中 2 个是 merge，1 个是 insert，怎么区分？

**当前方案**：
```
规则：
- Merge 的函数 → 显式
- Insert 的函数 → 隐式

实现：
- 从 merge_logs 获取哪些函数是 merged
- 从 insert_logs 获取哪些函数是 inserted
- 在 prompt 中明确标注
```

**潜在问题**：
- 如果一个函数同时在 merge 和 insert log 中？（理论上不应该出现）
- 如果 insert 的函数恰好是 merge 的一部分？

**需要确认**：查看实际数据中是否存在这些边界情况

---

### 问题4：Long Dependency Insert 的特殊处理 ⚠️ 关键问题

**问题**：
- Long dependency insert 和 short dependency 在 query 生成上有**显著区别**
- 需要完全不同的 examples 和风格指导

**重要差异**（基于 MAGNET_Short_vs_Long_Dependency.md）：

| 维度 | Short Dependency | Long Dependency |
|------|------------------|-----------------|
| **时间跨度** | 同一turn内 | 跨多个turn |
| **Query风格** | "查询公里数" | "用那个距离查找城市" |
| **参数来源** | 同turn的前一个函数 | 历史turn的输出 |
| **用户表达** | 单一目标 | 引用历史（代词） |

**必须修改**：
- ✅ 分开 SHORT_DEPENDENCY_EXAMPLES 和 LONG_DEPENDENCY_EXAMPLES
- ✅ 不同的风格指导（short: 隐式最终目标，long: 代词引用历史）
- ✅ Long dependency 需要完整的历史上下文
- ✅ Forward 执行时从 all_turn_outputs 查找参数

---

### 问题5：Empty Turn 的生成策略

**问题**：
- 空 turn 应该生成什么样的 query？
- miss_func 和 miss_params 是否需要不同的处理？

**当前实现**：
- 随机选择 miss_type
- 生成一个"看起来合理但无法满足"的 query

**改进想法**：
- 根据上下文生成更自然的 query
- 模拟真实场景中用户的模糊请求

---

## 📈 评估指标

### 自动化指标

1. **风格一致性**：
   ```
   Insert Implicit Rate = (insert turns 生成隐式 query 的数量) / (总 insert turns)
   Merge Explicit Rate = (merge turns 生成显式 query 的数量) / (总 merge turns)

   目标：> 80%
   ```

2. **生成成功率**：
   ```
   Success Rate = (成功生成的 turns) / (总 turns)

   目标：> 95%
   ```

3. **Token 使用量**：
   ```
   平均 Token per Turn
   总 Token 使用量

   用于成本估算
   ```

### 人工评估指标

1. **Query 质量**（随机抽样 100 条）：
   - 语法正确性
   - 语义合理性
   - 风格符合性
   - 参数完整性

2. **风格符合度**（随机抽样每种类型 20 条）：
   - Insert: 是否隐式？
   - Merge: 是否显式？
   - Mixed: 是否正确区分？

3. **边界情况处理**：
   - 复合操作是否合理？
   - 空 turn 是否自然？
   - 长依赖是否正确引用历史？

---

## 📝 输出示例

### 示例1：Insert Short Dependency

**输入**：
```python
turn_idx = 1
turn_functions = ["get_distance", "convert_unit"]
turn_operations = {
    "operations": ["insert_short"],
    "primary_style": "insert_short",
    "insert_info": [{
        "source_func": "get_distance",
        "nested_func": "convert_unit",
        "insert_type": "short_dependency"
    }]
}
```

**生成的 Query**：
```
"How many kilometers from San Francisco to San Mateo?"
```

**说明**：
- ✅ 只提到最终目标（公里数）
- ✅ 没有提到单位转换
- ✅ 隐式风格正确

---

### 示例2：Merged

**输入**：
```python
turn_idx = 2
turn_functions = ["get_distance", "set_navigation"]
turn_operations = {
    "operations": ["merge"],
    "primary_style": "merged",
    "merge_info": {
        "merged_turn_indices": [2, 3],
        "turn_0_functions": ["get_distance"],
        "turn_1_functions": ["set_navigation"]
    }
}
```

**生成的 Query**：
```
"Check the distance from SF to SM and set up navigation with that distance"
```

**说明**：
- ✅ 明确提到两个动作
- ✅ 使用连接词 "and"
- ✅ 显式风格正确

---

### 示例3：Merged + Insert

**输入**：
```python
turn_idx = 1
turn_functions = ["get_weather_forecast", "get_weather", "get_live_temp"]
turn_operations = {
    "operations": ["merge", "insert_short"],
    "primary_style": "merged_with_insert",
    "merge_info": {...},  # func1, func2 merged
    "insert_info": [{...}]  # func3 inserted
}
```

**生成的 Query**：
```
"Get the weather forecast and current temperature for San Francisco"
```

**说明**：
- ✅ 明确提到 forecast 和 temperature（merged）
- ✅ 没有提到 get_live_temp（inserted, 隐式）
- ✅ 混合风格正确

---

### 示例4：Long Dependency ⭐ 新增

**输入**：
```python
turn_idx = 3
turn_functions = ["cancel_booking"]
turn_operations = {
    "operations": ["insert_long"],
    "primary_style": "insert_long",
    "insert_info": [{
        "source_turn_idx": 0,
        "source_func": "book_flight",
        "nested_func": "cancel_booking",
        "insert_type": "long_dependency",
        "dependency_distance": 3
    }]
}

# 历史上下文
all_turn_outputs = [
    # Turn 0
    [{
        "function": "book_flight",
        "output": {"booking_id": "3426812", "destination": "NYC"}
    }],
    # Turn 1
    [{"function": "send_message", "output": {"status": "sent"}}],
    # Turn 2
    [{"function": "book_hotel", "output": {"hotel_id": "H789"}}],
]
```

**生成的 Query**：
```
"Cancel my New York trip due to unforeseen personal circumstances"
```

**Forward 执行**：
```python
# cancel_booking 需要 booking_id 参数
# 从 Turn 0 的输出中查找
params = {
    "booking_id": "3426812"  # ← 从 all_turn_outputs[0] 提取
}

cancel_booking(booking_id="3426812")
```

**说明**：
- ✅ 使用 "my New York trip" 引用 Turn 0 的预订
- ✅ 没有重复 booking_id（"3426812"）
- ✅ 跨 3 个 turn 引用（Turn 0 → Turn 3）
- ✅ 长依赖风格正确
- ✅ Forward 能从历史中正确提取参数

---

## 🔗 Long Dependency 实现要点 ⭐ 新增章节

### 核心差异总结

| 维度 | Short Dependency | Long Dependency |
|------|------------------|-----------------|
| **时间跨度** | 同一 turn | 跨多个 turn |
| **Query 风格** | 隐式最终目标 | 代词引用历史 |
| **Examples** | short_dependency | long_dependency（含历史）|
| **历史信息** | 可选 | **必需且详细** |
| **参数来源** | 同 turn 前一个函数 | all_turn_outputs 历史查找 |

### 1. 历史上下文的完整性

Long Dependency **必须**提供完整且详细的历史信息：

```python
def build_prompt_for_turn(
    turn_idx: int,
    turn_operations: Dict,
    all_turn_outputs: List[List[Dict]],
    ...
):
    primary_style = turn_operations["primary_style"]

    # ⚠️ 对于 Long Dependency，历史信息至关重要
    if primary_style == "insert_long":
        # 构建详细的历史块，包含所有输出
        history_block = f"""
[Previous Conversation History]
"""
        for h_idx in range(turn_idx):
            h_outputs = all_turn_outputs[h_idx]
            for output in h_outputs:
                func = output.get("function", "unknown")
                result = output.get("output", {})
                history_block += f"""
Turn {h_idx}:
  Function: {func}
  Output: {format_tool_output(result)}
"""

        # 强调可引用的关键信息
        insert_info = turn_operations.get("insert_info", [{}])[0]
        source_turn = insert_info.get("source_turn_idx", 0)
        history_block += f"""
⚠️ Note: The current turn may reference outputs from Turn {source_turn}
"""
```

### 2. Forward 执行的参数查找

Long Dependency 需要从**完整历史**中查找参数（而非仅 last_round）：

```python
async def forward_with_long_dependency(
    turn_idx: int,
    turn_functions: List[str],
    all_turn_outputs: List[List[Dict]],
    turn_operations: Dict,
    tool_schemas: Dict,
):
    """
    Long dependency 特殊处理：从历史中查找参数
    """
    insert_info = turn_operations.get("insert_info", [{}])[0]
    source_turn_idx = insert_info.get("source_turn_idx", 0)

    tool_calls = []

    for func_name in turn_functions:
        # 生成基础参数（从 query）
        params = await generate_params_from_query(...)

        # 检查缺失的参数
        required_params = tool_schemas[func_name].get("required", [])
        missing_params = [p for p in required_params if p not in params]

        # 从指定的 source turn 获取参数
        if missing_params:
            print(f"[Long Dep] Looking for {missing_params} in Turn {source_turn_idx}")

            source_outputs = all_turn_outputs[source_turn_idx]
            for output in source_outputs:
                output_data = output.get("output", {})

                for param_name in missing_params[:]:  # 复制列表
                    if param_name in output_data:
                        params[param_name] = output_data[param_name]
                        missing_params.remove(param_name)
                        print(f"[Long Dep] ✓ Found {param_name}={output_data[param_name]} from Turn {source_turn_idx}")

        # 如果还有缺失，从整个历史搜索
        if missing_params:
            for h_idx in range(turn_idx):
                if h_idx == source_turn_idx:
                    continue  # 已经搜索过

                for output in all_turn_outputs[h_idx]:
                    output_data = output.get("output", {})

                    for param_name in missing_params[:]:
                        if param_name in output_data:
                            params[param_name] = output_data[param_name]
                            missing_params.remove(param_name)
                            print(f"[Long Dep] ✓ Found {param_name} from Turn {h_idx} (fallback)")

        tool_calls.append({
            "function": func_name,
            "parameters": params,
            "params_source": "long_dependency_history"
        })

    return tool_calls
```

### 3. Examples 必须包含历史对话

Long Dependency examples 的特殊格式：

```python
LONG_DEPENDENCY_EXAMPLE = {
    "name": "Booking → Cancellation",
    "history_turns": [  # ← 必须有！
        {
            "turn": 0,
            "query": "Book a flight to NYC on April 15th",
            "functions": ["get_flight_cost", "book_flight"],
            "output": {"booking_id": "3426812"}  # ← 被引用的数据
        },
        {
            "turn": 1,
            "query": "Message my friend about the trip"
        },
        {
            "turn": 2,
            "query": "Book a hotel near Times Square"
        }
    ],
    "current_turn": 3,
    "functions": ["cancel_booking"],
    "query": "Cancel my New York trip",  # ← 使用代词引用
    "key_reference": "my New York trip",  # ← 指代 Turn 0
    "dependency_source": "Turn 0, booking_id"
}
```

### 4. Prompt 构建的关键差异

```python
# Short Dependency - 简洁的指导
if primary_style == "insert_short":
    instruction = "Only mention the final goal, intermediate steps are implicit"

# Long Dependency - 详细的历史 + 引用指导
elif primary_style == "insert_long":
    instruction = """
IMPORTANT: This turn references previous conversation.
- Use pronouns like "that", "my", "those"
- Reference the output from earlier turns naturally
- Don't repeat specific values or IDs

Available history for reference:
{detailed_history}
"""
```

---

## 🎯 总结

### 核心设计决策

1. **使用 In-Context Learning**：通过精心设计的 examples 让 LLM 学会区分风格
2. **显式风格指导**：在 prompt 中明确说明预期的 query 风格
3. **区分 Short 和 Long Dependency** ⭐：
   - Short: 同 turn 内嵌套，隐式最终目标，simple examples
   - Long: 跨 turn 引用，代词指代，history-rich examples
4. **多样性容错**：接受一定比例的不完美数据，提升鲁棒性
5. **分阶段实施**：从简单到复杂，逐步优化

### 关键创新点

1. **完整的操作检测**：不只检测第一个操作，而是所有操作
2. **Primary Style 概念**：为复合操作定义主要风格
3. **Short vs Long Dependency 区分** ⭐：
   - 不同的 Examples 库（short_dependency / long_dependency）
   - 不同的风格指导（隐式 vs 代词引用）
   - 不同的参数查找策略（同 turn vs 历史查找）
4. **动态 Examples 选择**：根据 turn 类型选择最相关的 examples
5. **元数据追踪**：记录风格信息，便于后续分析

### 预期效果

- ✅ 80%+ 的 query 符合预期风格
- ✅ 复合操作得到正确处理
- ✅ 生成的数据质量高，适合训练
- ✅ 代码清晰可维护，便于迭代

---

## 📚 相关资源

- 研究报告：[MAGNET_Insert_Merge_Query_Generation_Analysis.md](./MAGNET_Insert_Merge_Query_Generation_Analysis.md)
- 论文分析：[MAGNET_Paper_Summary.md](./MAGNET_Paper_Summary.md)
- 集成分析：[MAGNET_FSP_Integration_Analysis.md](./MAGNET_FSP_Integration_Analysis.md)
- 实现代码：[backward_to_query_magnet.py](./src/backward_to_query_magnet.py)

---

**文档创建时间**：2026-01-07
**作者**：Claude Sonnet 4.5
**状态**：待讨论和优化
**下一步**：讨论待定问题，优化设计，开始实施阶段1
