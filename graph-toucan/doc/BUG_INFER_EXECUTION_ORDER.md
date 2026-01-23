# BUG: Insert Logs Turn Index 在 Split 后失效

**发现日期**: 2026-01-09
**严重程度**: 🟡 中等（影响 4.52% 的路径）
**状态**: 待修复

---

## 问题描述

在 FSP v2 数据生成过程中，`insert_logs` 中记录的 `target_turn_idx` 在 `split` 操作后会失效，导致 `detect_turn_operations` 函数无法正确匹配 insert 信息。

## 根本原因

FSP 生成的操作顺序：
1. **Insert 操作**：在某个 turn 添加嵌套函数，记录 `target_turn_idx`
2. **Split 操作**：将某个 turn 拆分成两个 turn，导致后续所有 turn 的索引 +1
3. **结果**：`insert_logs` 中的 `target_turn_idx` 没有更新，指向错误的 turn

### 示例

```python
# 初始状态
Turn 0: [func_A]
Turn 1: [func_B]
Turn 2: [func_C]
Turn 3: [func_D]
Turn 4: [func_E]  ← Insert 操作：添加 func_F（依赖 func_E）

# Insert 后
insert_logs: [
    {
        "target_turn_idx": 4,  # ← 记录的是 Turn 4
        "source_func_name": "func_E",
        "nested_func_name": "func_F"
    }
]

# Split Turn 3 后（Turn 3 被拆分成 Turn 3 和 Turn 4）
Turn 0: [func_A]
Turn 1: [func_B]
Turn 2: [func_C]
Turn 3: [func_D_part1]
Turn 4: []           # ← Split 产生的空 turn
Turn 5: [func_E, func_F]  # ← 实际函数在 Turn 5

# 但 insert_logs 还是：
insert_logs: [
    {
        "target_turn_idx": 4,  # ← 仍然是 4，但函数已经在 Turn 5 了！ ❌
        "source_func_name": "func_E",
        "nested_func_name": "func_F"
    }
]
```

## 数据统计

通过扫描 `walker_path/fsp_v2.json` 中的前 100 个节点：

- **总路径数**: 4,163
- **受影响路径数**: 188
- **影响比例**: 4.52%
- **正确顺序率**（可检查的案例）: 100% ✅

受影响的路径特征：
- 同时包含 `insert_logs` 和 `split_logs`
- insert 的 turn 在 split 的 turn 之后

## 当前代码的行为

### `detect_turn_operations` 函数的问题

```python
# src/backward_to_query_magnet.py, lines 272-275
insert_logs = path_data.get("insert_logs", [])
for log in insert_logs:
    if log.get("target_turn_idx") == turn_idx:  # ← 基于 turn_idx 匹配
        result["insert_info"].append(log)
```

**问题**：
1. 当 `turn_idx = 4` 时，会匹配到 `target_turn_idx = 4` 的 insert_log
2. 但实际上函数在 Turn 5，不在 Turn 4
3. Turn 4 可能是空 turn，或者包含完全不同的函数
4. **结果**：`detect_turn_operations` 返回错误的 insert 信息

### 错误匹配的后果

```python
# Turn 4 的实际函数
turn_functions = ['mcp-directory-server-get_definitions']

# 错误匹配到的 insert_info
insert_info = {
    'source_func_name': 'pubmed-enhanced-search-server-get_pubmed_count',
    'nested_func_name': 'advanced-calculator-server-is_prime'
}

# 结果：prompt 中会包含不存在的依赖关系！
**Data Flow (output feeds as input)**:
  - pubmed-enhanced-search-server-get_pubmed_count → advanced-calculator-server-is_prime
    (但这两个函数都不在当前 turn！)
```

## 实际案例

### 案例：Node 4, Path 1

```python
# insert_logs 记录
{
    'insert_type': 'short_dependency',
    'source_func_name': 'pubmed-enhanced-search-server-get_pubmed_count',
    'nested_func_name': 'advanced-calculator-server-is_prime',
    'source_turn_idx': 4,
    'target_turn_idx': 4  # ← 记录是 Turn 4
}

# 实际 fsp_final
Turn 4: ['mcp-directory-server-get_definitions']  # ← 完全不同的函数！
Turn 5: ['pubmed-enhanced-search-server-get_pubmed_count',
         'advanced-calculator-server-is_prime']  # ← 实际在 Turn 5

# split_logs
{
    'insert_position': 2,  # 在 Turn 2 位置插入空 turn
    'miss_type': 'miss_params',
    ...
}
```

## 影响范围

### ✅ 不受影响的部分（96%）

对于没有 split 操作、或者 insert 在 split 之前的路径：
- ✅ 函数执行顺序 100% 正确（source 在 nested 之前）
- ✅ FSP 生成器已经正确排序
- ✅ `infer_execution_order` 保持原顺序是安全的

### ❌ 受影响的部分（4.52%）

对于同时有 insert 和 split 且 insert 在 split 后的路径：
- ❌ `detect_turn_operations` 可能匹配到错误的 insert_info
- ❌ Prompt 中的依赖关系信息错误
- ❌ 可能导致 query 生成质量下降

## 潜在问题

即使当前没有导致执行失败，但仍存在隐患：

1. **Prompt 污染**：错误的依赖关系信息被加入 prompt
2. **Query 质量下降**：模型基于错误信息生成 query
3. **难以调试**：错误不明显，但影响数据质量
4. **执行顺序风险**：如果未来基于 insert_info 进行排序，会出错

## 修复方案

### 方案 A：基于函数名匹配（推荐）✅

**优点**：
- 不依赖 turn_idx，更鲁棒
- 无需修改 FSP 生成器
- 适用于所有场景

**实现**：
```python
def detect_turn_operations(
    turn_idx: int,
    turn_functions: List[str],
    path_data: Dict[str, Any],
) -> Dict[str, Any]:
    # ... 现有代码 ...

    # 检查 insert (基于函数名匹配，不依赖 turn_idx)
    insert_logs = path_data.get("insert_logs", [])
    for log in insert_logs:
        source_func = log.get("source_func_name")
        nested_func = log.get("nested_func_name")

        # 方式 1: 检查两个函数是否都在当前 turn (short_dependency)
        if source_func in turn_functions and nested_func in turn_functions:
            result["insert_info"].append(log)
            if log.get("insert_type") == "long_dependency":
                result["operations"].append("insert_long")
            else:
                result["operations"].append("insert_short")

        # 方式 2: 检查 nested_func 是否在当前 turn (long_dependency)
        elif nested_func in turn_functions:
            # 这是 long_dependency，source_func 在其他 turn
            result["insert_info"].append(log)
            result["operations"].append("insert_long")

    # ... 现有代码 ...
```

### 方案 B：修复 FSP 生成器

**优点**：
- 从源头解决问题
- 数据更准确

**缺点**：
- 需要修改 FSP 生成器
- 需要重新生成所有数据

**实现**：
在 FSP 生成器的 split 操作后，更新所有受影响的 logs：
```python
def apply_split(fsp, split_position):
    # ... split 逻辑 ...

    # 更新所有后续 turn 的索引
    for log in insert_logs:
        if log['target_turn_idx'] > split_position:
            log['target_turn_idx'] += 1
        if log.get('source_turn_idx', -1) > split_position:
            log['source_turn_idx'] += 1

    for log in merge_logs:
        if log['turn_idx'] > split_position:
            log['turn_idx'] += 1
```

## 推荐行动

1. **立即修复**：采用方案 A，修改 `detect_turn_operations` 函数
2. **验证**：运行测试，确保 4.52% 的受影响路径能正确匹配
3. **长期**：考虑方案 B，从源头修复数据生成逻辑

## 相关代码位置

- `src/backward_to_query_magnet.py`:
  - `detect_turn_operations` (lines 231-303)
  - `infer_execution_order` (lines 1580-1597)
- `walker_path/fsp_v2.json`: FSP v2 数据文件

## 测试验证

### 验证脚本

```python
import json

with open('walker_path/fsp_v2.json', 'r') as f:
    data = json.load(f)

node_results = data['node_results']

# 找出受影响的案例
for node_key, node in node_results.items():
    for path in node['paths']:
        insert_logs = path.get('insert_logs', [])
        for log in insert_logs:
            turn_idx = log['target_turn_idx']
            turn_funcs = path['fsp_final_names'][turn_idx]
            source = log['source_func_name']
            nested = log['nested_func_name']

            # 检查函数是否在记录的 turn
            if source not in turn_funcs or nested not in turn_funcs:
                print(f"❌ Mismatch in Node {node_key}, Path {path['path_idx']}")
                print(f"   Expected turn {turn_idx}: {source}, {nested}")
                print(f"   Actual turn {turn_idx}: {turn_funcs}")

                # 找出实际所在的 turn
                for i, funcs in enumerate(path['fsp_final_names']):
                    if source in funcs and nested in funcs:
                        print(f"   Actually in turn {i}: {funcs}")
                        break
```

---

**创建时间**: 2026-01-09
**发现者**: Claude (在检查 `infer_execution_order` 函数时发现)
**优先级**: 🟡 中等（建议尽快修复，但不阻塞当前功能）
