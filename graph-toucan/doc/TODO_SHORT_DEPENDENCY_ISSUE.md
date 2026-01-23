# TODO: Short-Dependency Helper 隐式性问题

## 问题描述

在生成的 merged_with_insert 数据中，发现 short-dependency helper 函数在 user query 中被明确提及，违反了"隐式helper不应该在query中提及"的原则。

## 具体案例

### Case 1: Path 0, Turn 1 (merged_with_insert)

**Functions**:
- weather-information-server-get_weather_forecast_tool
- region-weather-get_weather
- model-context-protocol-server-get_live_temp (标注为 short-dependency)

**Generated User Query**:
```
Get the weather forecast for Shanghai and check the weather in that region,
then also get the live temperature there
```

**问题**: Query 明确说了 "get the live temperature"，但 `model-context-protocol-server-get_live_temp` 被标注为 short-dependency helper（应该隐式工作）。

**Model's Reason**:
> "model-context-protocol-server-get_live_temp is a SHORT-DEPENDENCY helper that operates implicitly based on location context"

### Case 2: Path 2, Turn 2 (merged_with_insert)

**Functions**:
- current-forest-fire-status-in-korea-get_comprehensive_fire_info
- region-weather-get_weather
- model-context-protocol-server-get_live_temp (标注为 short-dependency)

**Generated User Query**:
```
Check the current forest fire status in Korea and get weather for that region,
then provide live temperature from those coordinates
```

**问题**: Query 明确说了 "provide live temperature"，违反了 short-dependency helper 应该隐式的原则。

## 根本原因分析

有两种可能性：

### 可能性1: 模型理解偏差
- Prompt 中已经明确指出 "SHORT dependency - DO NOT mention helpers"
- 但模型在生成 query 时没有严格遵守这个指令
- 可能是 prompt 的表达不够强烈，或者例子不够明确

### 可能性2: 数据标注问题
- 这些 turn 中的 `get_live_temp` 可能不应该被标记为 short_dependency
- 如果 user query 中明确提到了某个功能，它就不应该是"隐式"的
- 需要重新审视 FSP 数据中 insert_type 的标注逻辑

## Short Dependency 的定义回顾

根据 MAGNET_Short_vs_Long_Dependency.md：

**Short Dependency 特征**:
- Same turn nested function calls
- Output of one feeds into the next
- **Helper functions should be IMPLICIT** (not mentioned in query)
- User only expresses the primary intent

**好的 Short-Dep 例子**:
```
Query: "Find restaurants near Times Square"
Functions:
  - geocode("Times Square") ← implicit helper
  - find_restaurants(lat, lng) ← explicit intent
```

**坏的 Short-Dep 例子**:
```
Query: "Convert Times Square to coordinates, then find restaurants"
← This explicitly mentions the helper, so it's not short-dep anymore
```

## 可能的解决方案

### 方案1: 加强 Prompt 指令
- 在 merged_with_insert prompt 中更明确地说明哪些函数不应该被提及
- 添加更多的正反例子，展示隐式 helper 的正确用法
- 使用更强的语言如 "NEVER mention" 替代 "do NOT mention"

### 方案2: 修正数据标注
- 检查 FSP 数据生成逻辑，如果某个函数在语义上必须被明确提及，它就不应该被标注为 short_dependency
- 可能需要根据函数的语义特性（如 get_live_temp 是一个独立的信息获取操作）来判断是否应该标注为 short-dep
- 重新审视 insert_type 的自动标注规则

### 方案3: 混合方案
- 对于某些函数（如 get_live_temp），它可能在某些场景下是 short-dep，在另一些场景下不是
- 需要根据具体的 query 意图来动态判断
- 可能需要在 FSP 生成阶段增加更细粒度的分类

## 下一步行动

1. **数据诊断**: 统计生成数据中有多少 short-dependency helper 被明确提及
2. **标注审查**: 检查 FSP v2 数据中 insert_type 的标注规则和准确性
3. **Prompt 优化**: 如果是模型理解问题，优化 prompt 的表达
4. **标注修正**: 如果是数据标注问题，修正 FSP 生成逻辑

## 测试建议

生成一批数据后，可以运行以下检查：

```python
# 检查 short-dep helper 是否被提及
for path in paths:
    for turn in path['turns_data']:
        if turn['turn_type'] in ['merged_with_insert', 'insert_short', 'insert_mixed']:
            query = turn['user_query'].lower()
            turn_ops = turn.get('operations', [])

            # 提取 short-dep functions
            short_dep_funcs = []
            if 'insert_info' in turn_ops:
                for insert in turn_ops['insert_info']:
                    if insert.get('insert_type') == 'short_dependency':
                        func_name = insert['inserted_function']
                        short_dep_funcs.append(func_name)

            # 检查这些函数是否在 query 中被提及
            for func in short_dep_funcs:
                func_keywords = extract_keywords(func)
                if any(kw in query for kw in func_keywords):
                    print(f"WARNING: Short-dep helper mentioned in query")
                    print(f"  Function: {func}")
                    print(f"  Query: {query}")
```

## 优先级

- **优先级**: 中等
- **影响范围**: merged_with_insert, insert_short, insert_mixed 类型的数据质量
- **建议时机**: 在大规模数据生成前解决，避免生成大量有问题的数据

## 相关文件

- `/data/lhy/datasets/graph-Toucan/src/backward_to_query_magnet.py` - 主要生成逻辑
- `/data/lhy/datasets/graph-Toucan/MAGNET_Short_vs_Long_Dependency.md` - Dependency 定义文档
- `/data/lhy/datasets/graph-Toucan/fsp_path/fsp_v2_queries.jsonl` - 测试数据

---

**创建时间**: 2026-01-08
**状态**: 待处理
