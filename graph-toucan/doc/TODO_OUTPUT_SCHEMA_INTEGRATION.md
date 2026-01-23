# TODO: 引入 Output Schema 到 Query 生成

## 问题描述

根据 MAGNET_Insert_Merge_Query_Generation_Analysis.md 对 Insert 操作的定义，**Insert（嵌套）关系**的核心特征是：

1. 第二个函数的核心参数来自第一个函数的输出
2. 第二个函数是完成第一个函数目标的必要手段
3. 用户不关心中间步骤，Query 只描述最终目标

**当前问题**：模型无法理解为什么两个函数能构成 Insert 关系，因为：
- ❌ 不知道第一个函数的输出是什么（类型、字段、含义）
- ❌ 不知道第二个函数需要什么输入
- ❌ 无法判断数据如何从输出流向输入
- ❌ 无法区分"工具性函数"（utility）和"独立意图"（independent intent）

## 具体案例

### 案例 1：单位转换（Insert）

**没有 Output Schema**：
```python
Functions: get_distance_miles(), convert_to_km()
Data Flow: get_distance_miles → convert_to_km

模型看到的：
- PRIMARY: get_distance_miles (Get distance between two points)
- IMPLICIT: convert_to_km (Convert value to kilometers)
- Data Flow: get_distance_miles → convert_to_km

模型困惑：
- get_distance_miles 返回什么？数字？对象？
- convert_to_km 需要什么输入？
- 为什么 convert_to_km 是"必要手段"？
```

**有 Output Schema**：
```python
get_distance_miles:
  Output: {"distance": float, "unit": "miles"}

convert_to_km:
  Input: {"miles": float}
  Output: {"distance": float, "unit": "km"}

Data Flow:
  get_distance_miles.distance (15.5 miles) → convert_to_km.miles

模型理解：
- 第一个函数返回英里数
- 第二个函数接收英里数，转换为公里
- convert_to_km 是单位转换工具（utility）
- 用户最终目标：获取公里数
- Query: "Get distance in kilometers" ✓
```

### 案例 2：数学计算（Insert）

**没有 Output Schema**：
```python
Functions: add(15, 25), divide(?, 4)
Data Flow: add → divide

当前生成的 Query (错误):
"Add 15 and 25, then divide by 4"  ← 明确提到了两个操作

期望的 Query:
"Divide the sum of 15 and 25 by 4"  ← 只描述最终目标
或: "What's (15+25) divided by 4?"
```

**有 Output Schema**：
```python
add(a: int, b: int):
  Output: {"result": int}  # 40

divide(a: int, b: int):
  Input: {"a": int, "b": int}
  Output: {"result": int}  # 10

Data Flow: add.result (40) → divide.a

模型理解：
- add 计算 15+25=40
- divide 需要这个 40 作为被除数
- add 是获取被除数的工具（implicit helper）
- Query: "What's (15+25) divided by 4?" ✓
```

### 案例 3：天气查询（Insert with Long-Dependency）

**没有 Output Schema**：
```python
Turn 0: get_weather(Shanghai)
Turn 2: get_live_temp(?, ?)
Data Flow: Turn 0 → Turn 2

当前生成的 Query (错误):
"Get the live temperature for Shanghai"  ← 模糊

期望的 Query:
"Get current temperature at those coordinates" ← 明确引用 Turn 0 的坐标输出
```

**有 Output Schema**：
```python
Turn 0: get_weather(city: string):
  Output: {
    "temperature": float,
    "location": {"lat": float, "lng": float}
  }

Turn 2: get_live_temp(lat: float, lng: float):
  Input: {"lat": float, "lng": float}
  Output: {"temperature": float}

Cross-turn Data Flow:
  Turn 0: get_weather.location → Turn 2: get_live_temp(lat, lng)

模型理解：
- Turn 0 返回城市的坐标（location 对象）
- Turn 2 需要这些坐标来获取实时温度
- 应该用代词引用 "those coordinates"
- Query: "Get live temperature at those coordinates" ✓
```

## Output Schema 的价值分析

| 场景 | 当前问题严重性 | Output Schema 帮助程度 | 优先级 |
|------|--------------|---------------------|--------|
| **Insert 关系理解** | 🔴 高 | 🟢 高（80-90%） | ⭐⭐⭐⭐⭐ |
| **Long-Dependency 代词引用** | 🟡 中 | 🟢 高（70%） | ⭐⭐⭐⭐ |
| **类型不匹配预警** | 🟡 中 | 🟢 中（40%） | ⭐⭐⭐ |
| **Reason 解释质量** | 🟢 低 | 🟢 高（80%） | ⭐⭐ |
| **Short-Dep 标注错误** | 🔴 高 | 🟡 低（10%） | ❌ 需要修复数据标注 |

**核心价值**：Output Schema 能让模型理解**数据如何流动**，从而判断**哪些函数是工具，哪些是目标**。

## 实施方案

### 方案 1：最小化 Schema（推荐首先实施）

**优点**：
- ✅ Token 消耗少
- ✅ 实施简单
- ✅ 核心信息完整

**实施**：
在 prompt 的 dependency_info 部分添加类型信息：

```python
dependency_info = """
**Data Flow with Types**:
  - source_func: output_field (type) → target_func: input_param (type)

Example:
  - get_distance_miles: distance (float, miles) → convert_to_km: miles (float)

Analysis:
  - Output type: float (distance in miles)
  - Input type: float (expects miles)
  - Function type: convert_to_km is a utility (unit conversion)
  - User goal: Get distance in kilometers (final result)
  - Query style: Express final goal only, don't mention helper
"""
```

**修改位置**：
- `src/backward_to_query_magnet.py`
  - insert_short 分支 (lines 1077-1145)
  - insert_long 分支 (lines 1147-1223)
  - insert_mixed 分支 (lines 1225-1331)
  - merged_with_insert 分支 (lines 950-1075)

### 方案 2：完整 Output Schema（如果 token 允许）

**优点**：
- ✅ 信息最完整
- ✅ 模型理解最准确
- ✅ 可以处理复杂嵌套对象

**实施**：
```python
**Function Schemas**:

Function: get_distance_miles
  Description: Get distance between two points
  Output Schema:
    {
      "distance": float,     # Distance value
      "unit": "miles",       # Always in miles
      "from": string,        # Starting point
      "to": string          # Destination
    }

Function: convert_to_km
  Description: Convert miles to kilometers
  Input Schema:
    {
      "miles": float        # Distance in miles
    }
  Output Schema:
    {
      "distance": float,    # Distance value
      "unit": "km"         # Always in kilometers
    }

**Data Flow Analysis**:
  get_distance_miles.distance (miles) → convert_to_km.miles

  Reasoning:
  - get_distance_miles provides the miles value
  - convert_to_km is a utility function (unit conversion)
  - User's final goal: distance in kilometers
  - Query should express final goal, not intermediate steps
```

### 方案 3：语义标注（辅助方案）

**优点**：
- ✅ 帮助模型识别函数类型
- ✅ Token 消耗很少

**实施**：
```python
**Function Semantic Types**:
  - get_distance_miles: [data_retrieval, measurement]
  - convert_to_km: [utility, unit_conversion]

Guideline:
  - [utility] functions are typically implicit helpers
  - [data_retrieval] functions are typically primary intents
```

## 实施步骤

### Phase 1: 准备工作

1. **提取 Output Schema**
   - 从函数定义中提取输出 schema
   - 格式化为易读的字符串
   - 处理缺失 schema 的情况

2. **设计 Schema 格式**
   - 决定使用完整 schema 还是简化版
   - 设计 prompt 中的展示格式
   - 考虑 token 限制

### Phase 2: 修改代码

**文件**: `src/backward_to_query_magnet.py`

**需要修改的函数**：
1. `build_prompt_for_turn()` - 添加 output_schema 参数
2. 四个 turn type 分支的 prompt 构建逻辑

**修改示例（insert_short）**：

```python
# 当前代码 (lines 1078-1092)
if turn_operations:
    insert_info_list = turn_operations.get("insert_info", [])
    for insert_info in insert_info_list:
        nested_func_name = insert_info.get("nested_func_name")
        source_func_name = insert_info.get("source_func_name")

        if nested_func_name:
            inserted_funcs.append(nested_func_name)
            if source_func_name:
                dependencies.append(f"{source_func_name} → {nested_func_name}")

# 修改后 (添加 schema 信息)
if turn_operations:
    insert_info_list = turn_operations.get("insert_info", [])
    for insert_info in insert_info_list:
        nested_func_name = insert_info.get("nested_func_name")
        source_func_name = insert_info.get("source_func_name")

        if nested_func_name:
            inserted_funcs.append(nested_func_name)
            if source_func_name:
                # 获取 output schema
                source_output = get_function_output_schema(source_func_name, tool_schemas)
                target_input = get_function_input_schema(nested_func_name, tool_schemas)

                # 构建详细的依赖关系说明
                dependencies.append({
                    'source': source_func_name,
                    'target': nested_func_name,
                    'output_type': source_output.get('type'),
                    'input_type': target_input.get('type'),
                    'flow': f"{source_func_name}.{source_output.get('field')} ({source_output.get('type')}) → {nested_func_name}.{target_input.get('field')} ({target_input.get('type')})"
                })

# 构建 dependency_info 时包含 schema
dependency_info = ""
if dependencies:
    dependency_info = "\n**Data Flow with Schema**:\n"
    for dep in dependencies:
        dependency_info += f"  - {dep['flow']}\n"
    dependency_info += f"\nAnalysis: {analyze_dependency_semantics(dependencies)}\n"
```

### Phase 3: 添加辅助函数

```python
def get_function_output_schema(func_name: str, tool_schemas: Dict) -> Dict:
    """从 tool_schemas 中提取函数的输出 schema"""
    schema = tool_schemas.get(func_name, {})
    output_schema = schema.get('output_schema', {})

    # 提取关键信息
    return {
        'type': output_schema.get('type', 'unknown'),
        'field': list(output_schema.get('properties', {}).keys())[0] if output_schema.get('properties') else 'result',
        'description': output_schema.get('description', '')
    }

def get_function_input_schema(func_name: str, tool_schemas: Dict) -> Dict:
    """从 tool_schemas 中提取函数的输入 schema"""
    schema = tool_schemas.get(func_name, {})
    params = schema.get('parameters', {})

    # 找到第一个非默认参数
    for param_name, param_info in params.items():
        if not param_info.get('optional', False):
            return {
                'type': param_info.get('type', 'unknown'),
                'field': param_name,
                'description': param_info.get('description', '')
            }

    return {'type': 'unknown', 'field': 'input', 'description': ''}

def analyze_dependency_semantics(dependencies: List[Dict]) -> str:
    """分析依赖关系的语义"""
    analysis = []

    for dep in dependencies:
        # 判断是否是 utility function
        target = dep['target']
        if any(keyword in target.lower() for keyword in ['convert', 'format', 'parse', 'validate', 'transform']):
            analysis.append(f"{target} is a utility function (data transformation)")

        # 类型匹配检查
        if dep['output_type'] != dep['input_type']:
            analysis.append(f"⚠️ Type mismatch: {dep['output_type']} → {dep['input_type']}")

    return "; ".join(analysis) if analysis else "Clean data flow, types match"
```

### Phase 4: 测试验证

1. **单元测试**
   - 测试 schema 提取函数
   - 测试不同场景的 prompt 生成
   - 测试缺失 schema 的处理

2. **集成测试**
   - 生成小批量数据（10-20 条）
   - 检查 insert_short 的 query 质量
   - 检查 insert_long 的代词使用
   - 检查 reason 的解释准确性

3. **质量评估**
   - 对比有无 schema 的 query 质量
   - 统计"明确提及 helper"的错误率
   - 统计代词使用的准确性

## 预期收益

### 定量指标

| 指标 | 当前 | 预期（有 Schema） | 改善幅度 |
|------|------|----------------|---------|
| Insert 场景 helper 隐式率 | ~50% | ~85% | +35% |
| Long-dep 代词使用准确率 | ~60% | ~85% | +25% |
| Reason 解释完整性 | ~40% | ~80% | +40% |
| 类型不匹配早期发现率 | 0% | ~60% | +60% |

### 定性收益

1. **Insert 关系理解**
   - ✅ 模型能判断哪些是 utility function
   - ✅ 模型能理解数据流动路径
   - ✅ Query 更自然，不提及中间步骤

2. **Long-Dependency 改善**
   - ✅ 代词引用更准确（"those coordinates" vs "that result"）
   - ✅ 理解跨 turn 的数据传递
   - ✅ 避免重复具体值

3. **调试和维护**
   - ✅ Reason 更详细，便于 debug
   - ✅ 类型不匹配提前发现
   - ✅ 数据质量更容易验证

## 风险和缓解

### 风险 1：Token 消耗增加

**影响**：每个 prompt 增加 200-500 tokens

**缓解**：
- 使用简化版 schema（方案 1）
- 只展示关键字段，不展示完整 schema
- 缓存常见函数的 schema 描述

### 风险 2：Schema 缺失或不准确

**影响**：部分函数没有 output_schema

**缓解**：
- 优雅降级：没有 schema 时使用当前逻辑
- 添加默认 schema 推断逻辑
- 逐步补充缺失的 schema

### 风险 3：模型理解偏差

**影响**：模型可能过度依赖 schema，忽略语义

**缓解**：
- Schema 作为辅助信息，不替代原有指令
- 保留语义判断的指导
- 通过 examples 平衡 schema 和语义

## 优先级和时间安排

### 高优先级（立即实施）

1. ✅ **方案 1：最小化 Schema**
   - 时间：1-2 天
   - 收益：立即改善 Insert 场景

2. ✅ **辅助函数开发**
   - 时间：1 天
   - 必要性：基础设施

### 中优先级（1-2 周内）

3. ⏱️ **方案 2：完整 Schema**
   - 时间：2-3 天
   - 收益：全面改善，特别是复杂场景

4. ⏱️ **质量评估和迭代**
   - 时间：持续
   - 重要性：验证效果，优化策略

### 低优先级（可选）

5. 📋 **方案 3：语义标注**
   - 时间：1 天
   - 收益：辅助改善

## 依赖和前置条件

1. **Tool Schemas 完整性**
   - 需要确认有多少函数有 output_schema
   - 如果覆盖率低（<50%），需要先补充 schema

2. **Schema 格式标准化**
   - 确认 output_schema 的格式是否统一
   - 是否需要 schema 预处理或格式转换

3. **Token 预算**
   - 评估当前 prompt 的 token 使用
   - 确定可以增加多少 token 给 schema

## 成功标准

### 短期目标（1-2 周）

- ✅ Insert_short 场景：helper 明确提及率降低到 <20%
- ✅ Insert_long 场景：代词使用准确率提升到 >80%
- ✅ 类型不匹配错误减少 30%

### 长期目标（1 个月）

- ✅ 所有 Insert 场景的 query 质量提升 40%
- ✅ Reason 解释完整性达到 80%
- ✅ 数据生成成功率提升 20%

## 相关文档

- `MAGNET_Insert_Merge_Query_Generation_Analysis.md` - Insert 和 Merge 的定义
- `TODO_SHORT_DEPENDENCY_ISSUE.md` - Short-dependency 标注问题
- `BACKWARD_TO_QUERY_MAGNET_IMPROVEMENTS.md` - 已完成的改进
- `src/backward_to_query_magnet.py` - 主要代码文件

---

**创建时间**: 2026-01-08
**状态**: 待实施
**优先级**: ⭐⭐⭐⭐⭐ 高优先级
**预计工作量**: 3-5 天（方案 1 + 测试）
