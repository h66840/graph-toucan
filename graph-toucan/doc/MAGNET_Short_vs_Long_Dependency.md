# MAGNET: Short Dependency vs. Long Dependency 详解

## 📋 文档概述

**目的**：深入理解MAGNET论文中Insert操作的两种形式：Short Dependency和Long Dependency

**基于**：MAGNET论文 (arXiv:2503.07826v1) Section 3.4 - Node OP #1: Insert

**核心区别**：数据依赖发生在**同一turn内部**还是**跨多个turn**

---

## 🎯 核心概念定义

### Short Dependency（短依赖）

**定义**：
- 嵌套函数在**同一turn内**立即使用前一个函数的输出
- 用户的单一意图需要多个函数协作完成
- 数据流动是**即时的、同步的**

**论文原文**（Section 3.4）：
> "Insert will also be useful for creating examples covering the long dependency challenge. For example, we could add another cities_by_range in a few rounds later which reuses the outputs from get_distance."
>
> "We may also insert c_hk as an individual turn after a **random later turn** to reflect long dependency."

**特征**：
```
Turn N: [func1, func2_nested]
        └──────┬──────┘
           立即依赖
```

### Long Dependency（长依赖）

**定义**：
- 嵌套函数在**后续的独立turn**中使用更早turn的输出
- 用户在稍后的对话中引用之前的结果
- 数据流动是**延迟的、异步的**

**论文原文**（Section 3.4）：
> "We may also insert c_hk as an **individual turn after a random later turn** to reflect long dependency."

**特征**：
```
Turn 1: [func1]
        输出: value_x

Turn 2: [other_func]
Turn 3: [other_func]

Turn 4: [func2_nested]
        需要: value_x ← 从Turn 1获取（跨越3个turn）
```

---

## 📊 核心差异对比表

| 维度 | Short Dependency | Long Dependency |
|------|------------------|-----------------|
| **时间跨度** | 同一turn内 | 跨多个turn |
| **数据流动** | 即时传递 | 延迟使用 |
| **用户意图** | 单一原子操作 | 两个独立但相关的操作 |
| **函数位置** | 在同一turn的函数列表中 | 在不同turn中 |
| **Query风格** | 只提最终目标，不提中间步骤 | 引用历史结果（"that", "the previous"） |
| **模型挑战** | 理解隐式需求 | 长期记忆管理 |
| **实现方式** | `turn.append(nested_func)` | `later_turn.insert(nested_func)` |
| **论文示例** | get_distance + convert_unit | get_distance → cities_by_range |

---

## 🔍 详细对比分析

### 1. 时间与空间维度

#### Short Dependency
```
时间轴：
├─ Turn 1: [func_A, func_B]  ← 在同一时刻
│          ↓      ↑
│          └──────┘ 即时依赖

空间：在同一个turn的数据结构中
```

#### Long Dependency
```
时间轴：
├─ Turn 1: [func_A] ────┐
│         输出: X       │
├─ Turn 2: [func_C]     │
│                       │ 跨时间的依赖
├─ Turn 3: [func_D]     │
│                       │
├─ Turn 4: [func_B] ────┘
│         需要: X

空间：在不同turn的数据结构中
```

### 2. 用户感知

#### Short Dependency
```
用户视角：一个操作
"给我查询从SF到SM多少公里"
    ↓
系统执行：
1. get_distance() → 返回miles
2. convert_unit() → miles转km
    ↓
用户感知：直接得到公里数（不知道中间转换）
```

#### Long Dependency
```
用户视角：两个独立操作

对话开始：
用户: "查询从SF到SM的距离"
系统: "距离是25.5公里"

...中间可能有其他对话...

几轮之后：
用户: "用那个距离查找附近的城市"
系统: （记住25.5km）"找到5个城市..."
```

### 3. Query的语言模式

#### Short Dependency Query特征

**模板**：
```
"获取<最终结果>"
"查询<end goal>"
"Get <final output>"
```

**示例**：
```
✓ "查询从SF到SM多少公里"
  （不说"查询距离并转换成公里"）

✓ "预订从LA到NYC的航班"
  （不说"先查价格再预订"）

✓ "获取Q4报告的PDF版本"
  （不说"获取报告并格式化成PDF"）
```

**特征**：
- ✅ 简洁、直接
- ✅ 只描述最终目标
- ✅ 不提及中间步骤
- ✅ 符合用户自然表达

#### Long Dependency Query特征

**模板**：
```
"用<代词>..." → "用那个结果..."
"基于<指代>..." → "基于之前的信息..."
"对<之前的事物>..." → "对刚才的预订..."
```

**示例**：
```
✓ "用那个距离查找附近城市"
  （不说"用25.5公里查找"）

✓ "取消我的纽约行程"
  （不说"取消预订3426812"）

✓ "用刚才的搜索结果发邮件"
  （不说"用[result_id]发邮件"）
```

**特征**：
- ✅ 使用代词和指代
- ✅ 引用历史上下文
- ✅ 不重复具体值
- ✅ 自然的对话延续

---

## 💡 完整示例对比

### 示例1：距离查询场景

#### Short Dependency版本

```
═══════════���═══════════════════════════════════════════════
Turn 1: 查询公里数
═══════════════════════════════════════════════════════════

FSP: [get_distance, convert_unit]
Operation: Insert (short_dependency)

User Query:
"How many kilometers from San Francisco to San Mateo?"

执行流程：
Step 1: get_distance(from='San Francisco', to='San Mateo')
        → Output: {"distance": 15.8, "unit": "miles"}

Step 2: convert_unit(value=15.8, from_unit='miles', to_unit='km')
        → Output: {"distance": 25.4, "unit": "km"}

Response:
"The distance from San Francisco to San Mateo is 25.4 kilometers."

关键特征：
- ✅ 用户只说"多少公里"，没提单位转换
- ✅ convert_unit是隐式需要的
- ✅ 两个函数在同一turn内执行
- ✅ 数据立即传递（miles → km）
```

#### Long Dependency版本

```
═══════════════════════════════════════════════════════════
Turn 1: 查询距离
═══════════════════════════════════════════════════════════

FSP: [get_distance, convert_unit]
Operation: Insert (short_dependency)

User Query:
"How many kilometers from San Francisco to San Mateo?"

Output: {"distance": 25.4, "unit": "km"}

Response:
"The distance is 25.4 kilometers."

═══════════════════════════════════════════════════════════
Turn 2: 发送消息（中间操作）
═══════════════════════════════════════════════════════════

FSP: [send_message]

User Query:
"Send this information to my colleague via email."

═══════════════════════════════════════════════════════════
Turn 3: 查找范围内城市（Long Dependency!）
═══════════════════════════════════════════════════════════

FSP: [cities_by_range]
Operation: Insert (long_dependency) - 使用Turn 1的distance

User Query:
"Using that distance, find all cities within that range
from San Francisco."

执行流程：
cities_by_range(
    center='San Francisco',
    range_km=25.4  ← 从Turn 1的输出获取！
)
→ Output: {"cities": ["Palo Alto", "Redwood City", ...]}

Response:
"Found 5 cities within 25.4km of San Francisco:
Palo Alto, Redwood City, San Carlos, Belmont, San Mateo."

关键特征：
- ✅ Turn 3引用Turn 1的结果（跨2个turn）
- ✅ 用户说"that distance"（代词引用）
- ✅ 模型需要从历史中提取25.4km
- ✅ cities_by_range与get_distance在不同turn
```

---

### 示例2：航班预订场景（基于论文Figure 1）

#### Short Dependency版本

```
═══════════════════════════════════════════════════════════
Turn 1: 预订航班
═══════════════════════════════════════════════════════════

FSP: [get_flight_cost, book_flight]
Operation: Insert (short_dependency)

User Query:
"I'm planning a journey from Los Angeles to New York on the
morning of April 15th 2024, preferring to fly business class.
Arrange this flight using my pre-linked credit card."

执行流程：
Step 1: get_flight_cost(
            from='LAX',
            to='JFK',
            date='2024-04-15',
            travel_class='business'
        )
        → Output: {"travel_cost_list": [2400.0]}

Step 2: book_flight(
            from='LAX',
            to='JFK',
            date='2024-04-15',
            travel_class='business',
            travel_cost=2400.0,  ← 使用Step 1的输出
            card_id='card_123456789'
        )
        → Output: {
            "booking_id": "3426812",
            "transaction_id": "45451592",
            "booking_status": true
          }

Response:
"Your flight from LAX to JFK on April 15, 2024 has been booked.
Your booking ID is 3426812 and the transaction ID is 45451592."

关键特征：
- ✅ 用户只说"预订航班"，没说"先查价格"
- ✅ get_flight_cost是隐式前提（必须知道价格才能预订）
- ✅ 价格立即传递给book_flight
- ✅ 同一turn内完成
```

#### Long Dependency版本

```
═══════════════════════════════════════════════════════════
Turn 1: 预订航班
═══════════════════════════════════════════════════════════

FSP: [get_flight_cost, book_flight]
Operation: Insert (short_dependency)

[同上...]

Output: {
    "booking_id": "3426812",
    "transaction_id": "45451592",
    "booking_status": true
}

Response:
"Your flight has been booked. Booking ID: 3426812."

═══════════════════════════════════════════════════════════
Turn 2: 购买保险
═══════════════════════════════════════════════════════════

FSP: [purchase_insurance]

User Query:
"With my flight now secured, I need to purchase insurance
for this trip."

═══════════════════════════════════════════════════════════
Turn 3: 发送消息给朋友
═══════════════════════════════════════════════════════════

FSP: [send_message]

User Query:
"Please message my friend Joey about this recent trip."

═══════════════════════════════════════════════════════════
Turn 4: 取消航班（Long Dependency!）
═══════════════════════════════════════════════════════════

FSP: [cancel_booking]
Operation: Insert (long_dependency) - 使用Turn 1的booking_id

User Query:
"I've reached the decision to cancel my New York trip due to
unforeseen personal circumstances. Could you proceed with the
cancellation process as soon as possible?"

常见错误（论文Figure 1展示）：
❌ Error: "I need the booking ID to cancel the trip."
    → 模型忘记了Turn 1的booking_id

正确执行：
✓ cancel_booking(booking_id='3426812')  ← 从Turn 1提取
  → Output: {"message": "Booking 3426812 cancelled."}

Response:
"Your flight booking has been successfully cancelled."

关键特征：
- ✅ Turn 4引用Turn 1的结果（跨3个turn）
- ✅ 用户说"my New York trip"（指代引用）
- ✅ 用户不会记得booking_id（自然）
- ✅ 模型需要长期记忆管理
- ✅ 测试模型的上下文追踪能力
```

---

### 示例3：数据库查询场景

#### Short Dependency版本

```
═══════════════════════════════════════════════════════════
Turn 1: 获取格式化的用户记录
═══════════════════════════════════════════════════════════

FSP: [query_database, format_json_to_table]
Operation: Insert (short_dependency)

User Query:
"Get user records from the customers table in a readable
table format."

执行流程：
Step 1: query_database(table='customers')
        → Output: {
            "data": [
                {"id": 1, "name": "Alice", "email": "alice@..."},
                {"id": 2, "name": "Bob", "email": "bob@..."}
            ]
          }

Step 2: format_json_to_table(data=<from Step 1>)
        → Output: {
            "formatted_table": "
            | ID | Name  | Email        |
            |----|-------|--------------|
            | 1  | Alice | alice@...    |
            | 2  | Bob   | bob@...      |
            "
          }

Response:
[Displays the formatted table]

关键特征：
- ✅ 用户要"表格格式"，不说"先查询再格式化"
- ✅ format_json_to_table是隐式的格式转换
- ✅ 数据立即格式化
```

#### Long Dependency版本

```
═══════════════════════════════════════════════════════════
Turn 1: 查询用户记录
═══════════════════════════════════════════════════════════

FSP: [query_database, format_json_to_table]
Operation: Insert (short_dependency)

[同上...]

Output: {"formatted_table": "...", "raw_data": [...]}

═══════════════════════════════════════════════════════════
Turn 2: 分析数据
═══════════════════════════════════════════════════════════

FSP: [analyze_data]

User Query:
"Analyze the user distribution by registration date."

═══════════════════════════════════════════════════════════
Turn 3: 导出报告（Long Dependency!）
═══════════════════════════════════════════════════════════

FSP: [export_to_pdf]
Operation: Insert (long_dependency) - 使用Turn 1的data

User Query:
"Export those user records to a PDF report."

执行流程：
export_to_pdf(
    data=<from Turn 1's raw_data>,  ← 从Turn 1提取
    format='report'
)
→ Output: {"pdf_path": "/reports/users_2024.pdf"}

Response:
"User records have been exported to PDF: users_2024.pdf"

关键特征：
- ✅ Turn 3引用Turn 1的数据
- ✅ 用户说"those user records"（指代）
- ✅ 跨越Turn 2的分析操作
```

---

## 🏗️ 在FSP中的表示

### Short Dependency的FSP结构

```python
# 初始FSP（random walk生成）
initial_fsp = [
    [func_A],  # Turn 0
    [func_B],  # Turn 1
    [func_C],  # Turn 2
]

# 应用Insert (short dependency)
# 在Turn 1后检测到func_D与func_B嵌套
enhanced_fsp = [
    [func_A],              # Turn 0
    [func_B, func_D],      # Turn 1 ← func_D添加到同一turn
    [func_C],              # Turn 2
]

# 数据结构
{
    "turn_idx": 1,
    "functions": ["func_B", "func_D"],
    "operations": ["insert_short"],
    "insert_info": {
        "source_func": "func_B",
        "nested_func": "func_D",
        "insert_type": "short_dependency"
    }
}
```

### Long Dependency的FSP结构

```python
# 初始FSP
initial_fsp = [
    [func_A],  # Turn 0
    [func_B],  # Turn 1
    [func_C],  # Turn 2
    [func_E],  # Turn 3
]

# 应用Insert (long dependency)
# 检测到func_D与func_A嵌套，但插入到后续turn
enhanced_fsp = [
    [func_A],              # Turn 0 ← 产生输出X
    [func_B],              # Turn 1
    [func_C],              # Turn 2
    [func_E, func_D],      # Turn 3 ← func_D添加到后续turn，使用X
]

# 数据结构
{
    "turn_idx": 3,
    "functions": ["func_E", "func_D"],
    "operations": ["insert_long"],
    "insert_info": {
        "source_func": "func_A",  # 在Turn 0
        "source_turn": 0,
        "nested_func": "func_D",
        "insert_type": "long_dependency",
        "dependency_distance": 3  # 跨越3个turn
    }
}
```

---

## 🎯 实现关键点

### 1. 操作检测

```python
def detect_insert_type(
    source_turn_idx: int,
    target_turn_idx: int
) -> str:
    """
    判断是short还是long dependency
    """
    if source_turn_idx == target_turn_idx:
        return "short_dependency"
    else:
        return "long_dependency"
```

### 2. Query生成的风格指导

#### Short Dependency的Prompt

```python
STYLE_INSTRUCTIONS["insert_short"] = """
**IMPORTANT - Query Style for Nested Functions (Short Dependency)**:

Characteristics:
- User has a SINGLE, CLEAR GOAL
- Intermediate/helper functions are IMPLICIT and automatic
- Query only mentions the FINAL outcome the user wants

Examples:
✓ "Get kilometers from A to B"
   (NOT "Get miles and convert to kilometers")

✓ "Book a flight from LA to NYC"
   (NOT "Check flight cost and book")

✓ "Get Q4 report in PDF"
   (NOT "Fetch report and format to PDF")

Rules:
- Focus on the end result
- Don't mention intermediate steps
- Keep it natural and concise
"""
```

#### Long Dependency的Prompt

```python
STYLE_INSTRUCTIONS["insert_long"] = """
**IMPORTANT - Query Style for Long Dependency (Cross-Turn Reference)**:

Characteristics:
- User references PREVIOUS results from earlier turns
- Uses PRONOUNS and INDIRECT REFERENCES
- Does NOT repeat specific values or IDs

Examples:
✓ "Using that distance, find nearby cities"
   (NOT "Using 25.4km, find cities")

✓ "Cancel my New York trip"
   (NOT "Cancel booking 3426812")

✓ "Export those results to PDF"
   (NOT "Export [specific data] to PDF")

Referencing Patterns:
- "that <noun>" → "that distance", "that booking"
- "the previous <noun>" → "the previous search"
- "my <noun>" → "my trip", "my reservation"
- "those <noun>" → "those results", "those records"

Rules:
- Reference history naturally
- Use context-aware language
- Assume the model remembers
"""
```

### 3. Examples设计

#### Short Dependency Examples

```python
SHORT_DEPENDENCY_EXAMPLES = [
    {
        "scenario": "Unit Conversion",
        "functions": ["get_distance", "convert_unit"],
        "dependency": "convert_unit needs output from get_distance",
        "query": "How many kilometers from San Francisco to San Mateo?",
        "explanation": "User wants kilometers. The miles→km conversion is implicit.",
        "anti_example": "Get the distance in miles and convert it to kilometers"
    },
    {
        "scenario": "Price Check + Booking",
        "functions": ["get_flight_cost", "book_flight"],
        "dependency": "book_flight needs cost from get_flight_cost",
        "query": "Book a business class flight from LA to NYC on April 15th",
        "explanation": "User wants to book. Price check is automatic prerequisite.",
        "anti_example": "Check flight prices and then book the flight"
    },
    {
        "scenario": "Data Formatting",
        "functions": ["query_database", "format_json_to_table"],
        "dependency": "format needs data from query",
        "query": "Get customer records in a readable table format",
        "explanation": "User wants formatted output. JSON→table conversion is implicit.",
        "anti_example": "Query the database and format the results as a table"
    }
]
```

#### Long Dependency Examples

```python
LONG_DEPENDENCY_EXAMPLES = [
    {
        "scenario": "Distance → Range Search",
        "history": [
            {
                "turn": 0,
                "query": "How many kilometers from SF to SM?",
                "functions": ["get_distance", "convert_unit"],
                "output": {"distance": 25.4, "unit": "km"}
            },
            {
                "turn": 1,
                "query": "Send this info to my colleague",
                "functions": ["send_email"]
            }
        ],
        "current_turn": 2,
        "functions": ["cities_by_range"],
        "dependency": "cities_by_range needs distance from Turn 0",
        "query": "Using that distance, find all cities within that range from SF",
        "explanation": "References Turn 0's distance (25.4km) without repeating the value",
        "anti_example": "Find cities within 25.4 kilometers from San Francisco"
    },
    {
        "scenario": "Booking → Cancellation",
        "history": [
            {
                "turn": 0,
                "query": "Book a flight to NYC on April 15th",
                "functions": ["get_flight_cost", "book_flight"],
                "output": {"booking_id": "3426812"}
            },
            {
                "turn": 1,
                "query": "Message my friend about the trip",
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
        "dependency": "cancel_booking needs booking_id from Turn 0",
        "query": "Cancel my New York trip due to unforeseen circumstances",
        "explanation": "References Turn 0's booking using 'my New York trip', not the ID",
        "anti_example": "Cancel booking 3426812"
    },
    {
        "scenario": "Query → Export",
        "history": [
            {
                "turn": 0,
                "query": "Get all customer records",
                "functions": ["query_database", "format_json"],
                "output": {"records": [...], "count": 150}
            },
            {
                "turn": 1,
                "query": "Analyze registration patterns",
                "functions": ["analyze_data"]
            }
        ],
        "current_turn": 2,
        "functions": ["export_to_pdf"],
        "dependency": "export needs records from Turn 0",
        "query": "Export those customer records to a PDF report",
        "explanation": "Uses 'those records' to reference Turn 0's data",
        "anti_example": "Export the 150 customer records to PDF"
    }
]
```

### 4. Forward执行的参数传递

#### Short Dependency

```python
def forward_short_dependency(
    turn_functions: List[str],
    tool_schemas: Dict,
    conversation_history: List
):
    """
    短依赖：同turn内的顺序执行
    """
    turn_outputs = []

    for i, func_name in enumerate(turn_functions):
        params = extract_params_from_query(...)

        # 如果是第二个函数，可能需要第一个的输出
        if i > 0:
            prev_output = turn_outputs[i-1]
            # 检查并填充依赖参数
            params = fill_dependent_params(
                params,
                prev_output,
                func_name
            )

        # 执行
        result = execute_function(func_name, params)
        turn_outputs.append(result)

    return turn_outputs
```

#### Long Dependency

```python
def forward_long_dependency(
    current_turn_idx: int,
    turn_functions: List[str],
    all_turn_outputs: List[List[Dict]],
    tool_schemas: Dict
):
    """
    长依赖：从历史turn中查找参数
    """
    turn_outputs = []

    for func_name in turn_functions:
        params = extract_params_from_query(...)
        required_params = get_required_params(func_name)

        # 检查缺失的参数
        missing_params = find_missing_params(params, required_params)

        # 从历史中查找
        for param_name in missing_params:
            # 遍历所有历史turn
            for past_turn_idx in range(current_turn_idx):
                for output in all_turn_outputs[past_turn_idx]:
                    # 检查是否有这个参数
                    if param_name in output:
                        params[param_name] = output[param_name]
                        print(f"[Long Dep] Found {param_name} from Turn {past_turn_idx}")
                        break

        # 执行
        result = execute_function(func_name, params)
        turn_outputs.append(result)

    return turn_outputs
```

---

## 📊 训练数据的分布建议

### 数据比例

基于论文的设计理念，建议的数据分布：

```python
{
    "short_dependency": {
        "count": 4000,      # ~50%
        "ratio": 0.50,
        "purpose": "训练隐式函数调用理解"
    },
    "long_dependency": {
        "count": 2000,      # ~25%
        "ratio": 0.25,
        "purpose": "训练长期记忆和上下文追踪"
    },
    "normal": {
        "count": 1500,      # ~19%
        "ratio": 0.19,
        "purpose": "基础单函数调用"
    },
    "merged": {
        "count": 500,       # ~6%
        "ratio": 0.06,
        "purpose": "多意图并行处理"
    }
}
```

### 复杂度分布

#### Short Dependency

```python
short_examples = {
    "simple": {
        "count": 2400,  # 60%
        "example": "A + B (2 functions)",
        "turns": 1
    },
    "moderate": {
        "count": 1200,  # 30%
        "example": "A + B + C (3 functions)",
        "turns": 1
    },
    "complex": {
        "count": 400,   # 10%
        "example": "A + B + C + D (4+ functions)",
        "turns": 1
    }
}
```

#### Long Dependency

```python
long_examples = {
    "near": {
        "count": 1000,  # 50%
        "dependency_distance": "1-2 turns",
        "example": "Turn 0 → Turn 1/2"
    },
    "medium": {
        "count": 700,   # 35%
        "dependency_distance": "3-4 turns",
        "example": "Turn 0 → Turn 3/4"
    },
    "far": {
        "count": 300,   # 15%
        "dependency_distance": "5+ turns",
        "example": "Turn 0 → Turn 5+"
    }
}
```

---

## 🎯 模型训练的目标

### Short Dependency训练目标

**能力要求**：
1. ✅ 识别用户的最终目标
2. ✅ 理解隐式的中间步骤需求
3. ✅ 正确组合嵌套函数
4. ✅ 按正确顺序执行

**常见错误**（训练要避免）：
```
❌ 漏调用嵌套函数
   User: "Get kilometers from A to B"
   Model: get_distance() only ← 忘记convert_unit

❌ 幻觉参数
   User: "Book flight to NYC"
   Model: book_flight(cost=1000.0) ← 幻觉的价格

❌ 顺序错误
   User: "Book flight"
   Model: book_flight(), get_flight_cost() ← 顺序反了
```

### Long Dependency训练目标

**能力要求**：
1. ✅ 维护长期对话历史
2. ✅ 识别代词和指代
3. ✅ 从历史中提取正确的值
4. ✅ 跨turn的数据依赖管理

**常见错误**（训练要避免）：
```
❌ 忘记历史信息
   Turn 0: booking_id = "3426812"
   Turn 3: "Cancel my trip"
   Model: "I need the booking ID" ← 忘记了

❌ 使用错误的历史值
   Turn 0: distance = 25km
   Turn 1: price = $500
   Turn 2: "Find cities in that range"
   Model: cities_by_range(range=500) ← 用错了值

❌ 要求用户重复信息
   Turn 0: "Book hotel X"
   Turn 3: "Cancel that hotel"
   Model: "Which hotel?" ← 不应该问
```

---

## 💡 实现检查清单

### Short Dependency实现

- [ ] **操作检测**
  - [ ] 识别同turn内的嵌套函数
  - [ ] 判断source_turn == target_turn
  - [ ] 标记为"insert_short"

- [ ] **Query生成**
  - [ ] 使用nested examples
  - [ ] 添加"只提最终目标"的指导
  - [ ] 验证query不包含中间步骤

- [ ] **Forward执行**
  - [ ] 顺序执行同turn内的函数
  - [ ] 第N个函数可访问第N-1个的输出
  - [ ] 参数自动传递

### Long Dependency实现

- [ ] **操作检测**
  - [ ] 识别跨turn的嵌套函数
  - [ ] 判断source_turn < target_turn
  - [ ] 标记为"insert_long"
  - [ ] 记录dependency_distance

- [ ] **Query生成**
  - [ ] 使用long dependency examples
  - [ ] 添加"使用代词引用"的指导
  - [ ] 包含history context
  - [ ] 验证query使用了指代

- [ ] **Forward执行**
  - [ ] 从all_turn_outputs中查找参数
  - [ ] 支持跨turn的参数传递
  - [ ] 处理参数未找到的情况
  - [ ] 记录依赖关系用于调试

---

## 📚 参考资源

- **论文原文**: arXiv:2503.07826v1, Section 3.4
- **Figure 1**: 展示了Turn 4的Long Dependency错误示例
- **相关分析**: MAGNET_Insert_Merge_Query_Generation_Analysis.md
- **实现方案**: MAGNET_Implementation_Plan.md

---

## 🔚 总结

### 核心要点

**Short Dependency（短依赖）**:
- ⏱️ 同turn内立即依赖
- 🎯 单一用户意图
- 💬 Query只提最终目标
- 🔄 数据即时传递
- 📍 函数在同一turn列表中

**Long Dependency（长依赖）**:
- ⏱️ 跨turn的延迟依赖
- 🎯 两个独立但相关的意图
- 💬 Query使用代词引用历史
- 🔄 数据延迟使用
- 📍 函数在不同turn中

### 实现关键

1. **准确的操作检测**：判断source和target turn的关系
2. **针对性的Examples**：short用nested，long用cross-turn
3. **不同的风格指导**：明确区分query的表达方式
4. **正确的参数传递**：short同turn，long跨turn查找

### 训练价值

- Short Dependency → 教会模型**隐式推理**
- Long Dependency → 教会模型**长期记忆**
- 两者结合 → 完整的**多轮对话能力**

---

**文档创建时间**：2026-01-07
**基于论文**：MAGNET (arXiv:2503.07826v1)
**作者**：Claude Sonnet 4.5
