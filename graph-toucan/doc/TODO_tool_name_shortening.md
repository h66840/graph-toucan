# TODO: 工具名称长度限制处理

## 问题描述

某些工具的名称超过了模型允许的最大长度限制（64字符），导致无法正常调用这些工具。

## 解决方案

实现工具名称的动态缩短机制：
1. 在发送给模型前，使用缩短后的名称
2. 在执行函数时，映射回原始名称执行
3. **在保存结果时，统一使用缩短后的名称**（conversation 和 tools 保持一致）
4. 同时保存 name_mapping，便于后续还原

## 推荐方案：智能缩短 + 哈希

### 命名策略
```python
# 原名: "very-long-tool-name-with-many-parts-and-more-stuff"
# 缩短: "very-long-tool-name-wi_a3f5b"  (保留前58字符 + "_" + 5位哈希)
```

### 优点
- 保留部分可读性
- 哈希后缀保证唯一性
- conversation 和 tools 完全一致
- 可通过 mapping 还原

## 需要修改的位置

### 1. 添加工具名称缩短函数

在 `src/positive_distill.py` 文件顶部添加：

```python
import hashlib
import copy
from typing import Tuple

def shorten_tool_name(name: str, max_length: int = 64) -> str:
    """
    缩短工具名称到指定长度

    Args:
        name: 原始工具名称
        max_length: 最大长度（默认64）

    Returns:
        缩短后的工具名称
    """
    if len(name) <= max_length:
        return name

    # 生成5位哈希后缀保证唯一性
    hash_suffix = hashlib.md5(name.encode()).hexdigest()[:5]

    # 保留前 max_length-6 个字符 + "_" + 哈希
    max_prefix = max_length - 6
    return f"{name[:max_prefix]}_{hash_suffix}"
```

### 2. 修改 `build_tools_for_api` 函数（约172行）

**当前代码：**
```python
def build_tools_for_api(tool_schemas: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    tools = []
    for tool_name, tool_meta in tool_schemas.items():
        tool_schema = tool_meta.get("function_schema", {})
        if tool_schema:
            tools.append(tool_schema)
    return tools
```

**修改后：**
```python
def build_tools_for_api(
    tool_schemas: Dict[str, Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], Dict[str, str], Dict[str, Dict[str, Any]]]:
    """
    将 tool schemas 转换为 OpenAI API 格式的 tools 列表

    Args:
        tool_schemas: 工具 schema 字典 {original_name: tool_meta}

    Returns:
        - tools: OpenAI API 格式的 tools 列表（名称已缩短）
        - name_mapping: {short_name: original_name} 映射字典
        - short_tool_schemas: 缩短名称后的 tool schemas {short_name: tool_meta_with_short_name}
    """
    tools = []
    name_mapping = {}  # short_name -> original_name
    short_tool_schemas = {}  # short_name -> tool_meta (with short name in schema)

    for original_name, tool_meta in tool_schemas.items():
        tool_schema = tool_meta.get("function_schema", {})
        if tool_schema:
            # 缩短名称
            short_name = shorten_tool_name(original_name)

            # 深拷贝避免修改原始数据
            tool_schema_copy = copy.deepcopy(tool_schema)
            tool_meta_copy = copy.deepcopy(tool_meta)

            # 修改 schema 中的名称
            if "function" in tool_schema_copy:
                tool_schema_copy["function"]["name"] = short_name

            # 修改 tool_meta 中的名称
            tool_meta_copy["function_schema"] = tool_schema_copy

            tools.append(tool_schema_copy)
            name_mapping[short_name] = original_name
            short_tool_schemas[short_name] = tool_meta_copy

    return tools, name_mapping, short_tool_schemas
```

### 3. 修改 `forward_rollout_step` 函数（约220行）

#### 3.1 调用 `build_tools_for_api`
```python
# 旧代码:
tools = build_tools_for_api(tool_schemas)

# 新代码:
tools, name_mapping, short_tool_schemas = build_tools_for_api(tool_schemas)
```

#### 3.2 执行函数时映射回原始名称（约320-340行）
```python
for tc in api_tool_calls:
    short_func_name = tc.function.name
    # 映射回原始名称执行
    original_func_name = name_mapping.get(short_func_name, short_func_name)

    # 使用原始名称执行函数
    output_result = await execute_function_call(original_func_name, parameters)

    # 但在 step_outputs 中记录缩短的名称
    step_outputs.append({
        "function": short_func_name,  # 使用缩短的名称
        "output": output
    })
```

#### 3.3 返回时使用缩短后的 schemas
```python
# 在返回结果中，conversation_history 已经包含缩短的名称（自然生成）
# 不需要额外处理
```

### 4. 修改 `process_single_record_v1` 函数（约648行）

#### 4.1 调用 `build_tools_for_api`
```python
# 约648行
tools, name_mapping, short_tool_schemas = build_tools_for_api(nodes_tool_schema)
```

#### 4.2 执行函数时映射回原始名称（约755-760行）
```python
for tc in api_tool_calls:
    short_func_name = tc.function.name
    tool_call_id = tc.id

    try:
        parameters = json.loads(tc.function.arguments) if tc.function.arguments else {}
    except json.JSONDecodeError:
        parameters = {}

    try:
        # 映射回原始名称执行
        original_func_name = name_mapping.get(short_func_name, short_func_name)
        output_result = await execute_function_call(original_func_name, parameters)

        # ... 处理 output ...

        step_outputs.append({
            "function": short_func_name,  # 使用缩短的名称
            "output": output
        })
```

#### 4.3 返回时使用缩短的 tool schemas（约833-851行）
```python
# 构建 tools 列表：使用缩短名称的 schemas
tools_list = [
    {"function_schema": tool_meta.get("function_schema", {})}
    for tool_meta in short_tool_schemas.values()
    if "function_schema" in tool_meta
]

return {
    "path_info": record.get("path_info", {}),
    "atomic_queries": atomic_queries,
    "total_turns": len(atomic_queries),
    "ground_truth_steps": len(ground_truth_fc),
    "generated_steps": len(all_steps),
    "metrics": metrics,
    "token_usage": total_token_usage,
    "ground_truth_fc": ground_truth_fc,
    "generated_fc": all_steps,
    "conversation": conversation_history,  # 已包含缩短的名称
    "tools": tools_list,  # 缩短名称的 schemas
    "tool_name_mapping": name_mapping  # 添加映射关系
}
```

### 5. 修改 `process_single_record` 函数（约857-926行）

类似 `process_single_record_v1` 的修改：

```python
async def process_single_record(record: Dict[str, Any]) -> Dict[str, Any]:
    # ... 前面的代码 ...

    nodes_tool_schema = record.get("nodes_tool_schema", {})

    # 正向 rollout（多步执行）- 需要传入 tool_schemas 而非构建好的 tools
    # 在 forward_rollout_step 内部调用 build_tools_for_api
    rollout_result = await forward_rollout_step(
        user_query=final_query,
        tool_schemas=nodes_tool_schema,
        conversation_history=[],
        max_steps=10
    )

    # rollout_result 中已经包含缩短名称的 conversation_history
    # 需要从 rollout_result 获取 short_tool_schemas 和 name_mapping
    # （需要修改 forward_rollout_step 的返回值）
```

**注意**: `forward_rollout_step` 需要在返回值中添加：
```python
return {
    "steps": all_steps,
    "token_usage": total_token_usage,
    "conversation_history": conversation_history,
    "short_tool_schemas": short_tool_schemas,  # 新增
    "tool_name_mapping": name_mapping  # 新增
}
```

然后在 `process_single_record` 中：
```python
# 构建 tools 列表：使用缩短名称的 schemas
short_tool_schemas = rollout_result.get("short_tool_schemas", {})
tools_list = [
    {"function_schema": tool_meta.get("function_schema", {})}
    for tool_meta in short_tool_schemas.values()
    if "function_schema" in tool_meta
]

return {
    "path_info": record.get("path_info", {}),
    "final_query": final_query,
    "ground_truth_steps": len(ground_truth_fc),
    "generated_steps": len(generated_steps),
    "metrics": metrics,
    "token_usage": rollout_result.get("token_usage", {}),
    "ground_truth_fc": ground_truth_fc,
    "generated_fc": generated_steps,
    "conversation": conversation_history,  # 已包含缩短的名称
    "tools": tools_list,  # 缩短名称的 schemas
    "tool_name_mapping": rollout_result.get("tool_name_mapping", {})  # 添加映射
}
```

## 数据一致性保证

### 保存的数据结构

```json
{
    "conversation": [
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "function": {
                        "name": "shortened_name_a3f5b"
                    }
                }
            ]
        }
    ],
    "tools": [
        {
            "function_schema": {
                "function": {
                    "name": "shortened_name_a3f5b"
                }
            }
        }
    ],
    "tool_name_mapping": {
        "shortened_name_a3f5b": "original-very-long-tool-name"
    }
}
```

### 一致性验证
- ✅ conversation 中的工具名：`shortened_name_a3f5b`
- ✅ tools 中的工具名：`shortened_name_a3f5b`
- ✅ 完全一致
- ✅ 可通过 tool_name_mapping 还原

## 实现细节

### 注意事项

1. **导入依赖**
   ```python
   import hashlib
   import copy
   from typing import Tuple
   ```

2. **深拷贝**
   - 必须使用 `copy.deepcopy()` 避免修改原始数据
   - 原始 `nodes_tool_schema` 保持不变

3. **映射方向**
   - `name_mapping`: `short_name -> original_name`
   - 执行时：查 mapping 获取原始名称
   - 保存时：直接使用缩短名称

4. **错误处理**
   - 如果映射失败，使用缩短名称作为 fallback
   - 记录警告日志

5. **测试**
   - 测试超长名称的工具
   - 测试名称冲突的情况（哈希应该避免）
   - 验证 conversation 和 tools 的一致性
   - 验证通过 mapping 可以还原

### 潜在问题

1. **哈希冲突**
   - MD5 5位哈希冲突概率极低
   - 如果担心，可以增加到6-8位

2. **调试体验**
   - 日志中会出现缩短的名称
   - 建议在关键位置同时记录原始名称
   - 例如：`print(f"Executing {short_name} (original: {original_name})")`

3. **向后兼容**
   - 确保对于长度未超限的工具，行为保持不变
   - 添加单元测试验证

## 优先级

**中等** - 只有在遇到超长工具名时才会影响功能

## 预计工作量

- 实现时间：2-3小时
- 测试时间：1小时
- 总计：3-4小时

## 相关文件

- `/data/lhy/datasets/graph-Toucan/src/positive_distill.py` (主要修改)

## 参考

- OpenAI API 工具名称限制：最大64字符
- Python hashlib 文档：https://docs.python.org/3/library/hashlib.html

## 额外优化（可选）

### 1. 添加日志
```python
if len(name) > max_length:
    short_name = shorten_tool_name(name)
    print(f"Tool name shortened: {name} -> {short_name}")
```

### 2. 统计缩短的工具数量
```python
shortened_count = sum(1 for name in tool_schemas if len(name) > 64)
if shortened_count > 0:
    print(f"Shortened {shortened_count} tool names")
```

### 3. 验证映射完整性
```python
# 在返回前验证
for short_name in conversation_tool_names:
    assert short_name in name_mapping or len(short_name) <= 64
```
