# 修复方案：基于函数名匹配的 detect_turn_operations

## 修改位置

`src/backward_to_query_magnet.py` 的 `detect_turn_operations` 函数 (lines 231-303)

## 修改前（有bug）

```python
def detect_turn_operations(
    turn_idx: int,
    turn_functions: List[str],
    path_data: Dict[str, Any],
) -> Dict[str, Any]:
    # ...

    # 检查 insert (可能有多个 insert 在同一个 turn)
    insert_logs = path_data.get("insert_logs", [])
    for log in insert_logs:
        if log.get("target_turn_idx") == turn_idx:  # ← 问题：基于可能过期的 turn_idx
            result["insert_info"].append(log)

            # 区分 short 和 long dependency
            if log.get("insert_type") == "long_dependency":
                result["operations"].append("insert_long")
            else:
                result["operations"].append("insert_short")

    # ...
```

## 修改后（方案A）

```python
def detect_turn_operations(
    turn_idx: int,
    turn_functions: List[str],
    path_data: Dict[str, Any],
) -> Dict[str, Any]:
    # ...

    # 检查 insert (基于函数名匹配，不依赖 turn_idx)
    insert_logs = path_data.get("insert_logs", [])
    for log in insert_logs:
        source_func = log.get("source_func_name")
        nested_func = log.get("nested_func_name")
        insert_type = log.get("insert_type")

        # 根据 insert_type 判断如何匹配
        if insert_type == "short_dependency":
            # Short dependency: 两个函数都必须在当前 turn
            if source_func in turn_functions and nested_func in turn_functions:
                result["insert_info"].append(log)
                result["operations"].append("insert_short")

        elif insert_type == "long_dependency":
            # Long dependency: 只有 nested_func 在当前 turn
            # source_func 在之前的某个 turn（通过 source_turn_idx 记录）
            if nested_func in turn_functions:
                result["insert_info"].append(log)
                result["operations"].append("insert_long")

    # ...
```

## 详细说明

### Short Dependency 匹配逻辑

```python
if insert_type == "short_dependency":
    if source_func in turn_functions and nested_func in turn_functions:
        # ✅ 确保两个函数都在当前 turn
        result["insert_info"].append(log)
```

**为什么这样判断？**
- Short dependency 的定义：同一个 turn 内的依赖
- 必须保证 source 和 nested 都在当前 turn 的函数列表中
- 这样可以避免匹配到错误的 turn

### Long Dependency 匹配逻辑

```python
elif insert_type == "long_dependency":
    if nested_func in turn_functions:
        # ✅ 只检查 nested_func 是否在当前 turn
        result["insert_info"].append(log)
```

**为什么只检查 nested_func？**
- Long dependency 的定义：跨 turn 的依赖
- source_func 在之前的某个 turn，不在当前 turn
- 只有 nested_func 在当前 turn
- `source_turn_idx` 字段记录了 source 所在的 turn（用于 prompt 生成）

## 测试用例

### 案例1：正常情况（无 split）

```python
# Turn 2 函数
turn_functions = ['get_weather', 'convert_temp']

# insert_log
log = {
    'insert_type': 'short_dependency',
    'source_func_name': 'get_weather',
    'nested_func_name': 'convert_temp',
    'target_turn_idx': 2
}

# 修改前：基于 turn_idx=2 匹配 ✅
# 修改后：基于函数名匹配 ✅
# 结果：都能正确匹配
```

### 案例2：有 split 的情况

```python
# Turn 4 函数（split 后）
turn_functions = ['mcp-directory-server-get_definitions']

# Turn 5 函数（split 后，实际包含 insert 的函数）
turn_functions_5 = ['pubmed-get_count', 'is_prime']

# insert_log（记录的还是 split 前的索引）
log = {
    'insert_type': 'short_dependency',
    'source_func_name': 'pubmed-get_count',
    'nested_func_name': 'is_prime',
    'target_turn_idx': 4  # ← split 前的索引
}

# 修改前：
# Turn 4: turn_idx=4 匹配成功 ❌
#   但函数不在 Turn 4，错误匹配！
# Turn 5: turn_idx=5 不等于 4，不匹配 ❌
#   但函数在 Turn 5，漏掉了！

# 修改后：
# Turn 4: 'pubmed-get_count' not in turn_functions ✅
#   不匹配，正确！
# Turn 5: 'pubmed-get_count' in turn_functions ✅
#   匹配成功，正确！
```

### 案例3：Long Dependency

```python
# Turn 0 函数
turn_0_functions = ['get_weather']

# Turn 2 函数
turn_2_functions = ['get_live_temp']

# insert_log
log = {
    'insert_type': 'long_dependency',
    'source_func_name': 'get_weather',
    'nested_func_name': 'get_live_temp',
    'source_turn_idx': 0,
    'target_turn_idx': 2
}

# 修改前：
# Turn 0: target_turn_idx=2 != 0，不匹配 ✅
# Turn 2: target_turn_idx=2 == 2，匹配 ✅

# 修改后：
# Turn 0: 'get_live_temp' not in turn_0_functions，不匹配 ✅
# Turn 2: 'get_live_temp' in turn_2_functions，匹配 ✅

# 结果：都能正确匹配
```

## 预期效果

### 修复前（4.52% 路径有问题）

```
总路径：4,163
受影响路径：188 (4.52%)
- 错误匹配：部分路径的 insert_info 被加到错误的 turn
- 漏掉匹配：部分路径的 insert_info 没有被检测到
```

### 修复后

```
总路径：4,163
受影响路径：0 (0%)
- 所有 insert_info 都匹配到正确的 turn ✅
```

## 代码完整性

修改不影响其他功能：
- ✅ Merge 检测逻辑不变
- ✅ Empty turn 检测逻辑不变
- ✅ Primary style 判断逻辑不变
- ✅ 只改变 insert 的匹配方式

## 向后兼容性

✅ 完全兼容现有数据：
- 对于没有 split 的路径（95.48%）：新旧方法结果一致
- 对于有 split 的路径（4.52%）：新方法修复了问题

## 实施步骤

1. 修改 `detect_turn_operations` 函数 (lines 272-281)
2. 运行测试，确保 188 个受影响路径能正确匹配
3. 生成小批量数据验证
