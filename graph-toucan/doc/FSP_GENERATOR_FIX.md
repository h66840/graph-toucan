# FSP 生成器修复：Split 后更新 Turn Index

**文件**: `src/generate_fsp_v2.py`
**修改位置**: Lines 144-164
**修复日期**: 2026-01-09

---

## 问题描述

在 FSP v2 生成过程中，操作顺序是：
1. **Merge** → 合并 turns
2. **Insert** → 添加嵌套函数（记录 turn_idx）
3. **Split** → 插入空 turn（导致后续 turn 索引变化）

问题：**Split 操作会改变 turn 索引，但 insert_logs 和 merge_logs 中的 turn_idx 没有更新**。

---

## 修复方案

在 `apply_split_operation` 调用后，立即更新所有受影响的 logs 中的 turn_idx。

### 修复代码

```python
# 应用 Split 操作（论文推荐最后做 Split）
fsp_final, split_logs = apply_split_operation(
    fsp=fsp_after_insert,
    split_probability=split_probability,
    rng=rng,
    index_to_name=index_to_name,
)

# 修复：Split 后更新所有受影响的 logs 的 turn_idx
# Bug fix: 当 split 在某个位置插入空 turn 时，所有后续 turn 的索引 +1
# 需要更新 insert_logs 和 merge_logs 中的 turn_idx
if split_logs:
    for split_log in split_logs:
        insert_position = split_log["insert_position"]

        # 更新 insert_logs 中受影响的 turn_idx
        for insert_log in insert_logs:
            # target_turn_idx: 嵌套函数所在的 turn
            if insert_log.get("target_turn_idx", -1) > insert_position:
                insert_log["target_turn_idx"] += 1

            # source_turn_idx: source 函数所在的 turn（long dependency）
            if insert_log.get("source_turn_idx", -1) > insert_position:
                insert_log["source_turn_idx"] += 1

        # 更新 merge_logs 中受影响的 turn_idx
        for merge_log in merge_logs:
            if merge_log.get("turn_idx", -1) > insert_position:
                merge_log["turn_idx"] += 1
```

---

## 修复逻辑详解

### Split 操作的影响

当 `insert_position = 2` 时：

```
Before Split:
Turn 0: [func_A]
Turn 1: [func_B]
Turn 2: [func_C]      ← insert_position
Turn 3: [func_D]
Turn 4: [func_E]

After Split (在 Turn 2 后插入空 turn):
Turn 0: [func_A]      ← 不变
Turn 1: [func_B]      ← 不变
Turn 2: [func_C]      ← 不变
Turn 3: []            ← 新插入的空 turn
Turn 4: [func_D]      ← 原来的 Turn 3，索引 +1
Turn 5: [func_E]      ← 原来的 Turn 4，索引 +1
```

### 更新规则

1. **insert_logs 中的 target_turn_idx**:
   - 如果 `target_turn_idx > insert_position`，则 `target_turn_idx += 1`
   - 例如：原来 `target_turn_idx = 4`，现在变成 `5`

2. **insert_logs 中的 source_turn_idx**:
   - 如果 `source_turn_idx > insert_position`，则 `source_turn_idx += 1`
   - 适用于 long_dependency，source 在之前的 turn

3. **merge_logs 中的 turn_idx**:
   - 如果 `turn_idx > insert_position`，则 `turn_idx += 1`

---

## 示例：Node 16, Path 2

### 修复前

```python
# Insert 操作记录
insert_log = {
    "insert_type": "short_dependency",
    "target_turn_idx": 2,           # ← 记录时的索引
    "source_func": "multiply",
    "nested_func": "is_prime"
}

# Split at position 0
# 在 Turn 0 后插入空 turn

# 最终 FSP（Split 后）
Turn 0: [mul]
Turn 1: []                           # ← 新插入
Turn 2: [frankfurtermcp, quickchart]
Turn 3: [multiply, is_prime]         # ← 实际在 Turn 3

# 问题：insert_log 的 target_turn_idx 还是 2，但函数在 Turn 3！❌
```

### 修复后

```python
# Insert 操作记录
insert_log = {
    "insert_type": "short_dependency",
    "target_turn_idx": 2,           # ← 初始记录
    "source_func": "multiply",
    "nested_func": "is_prime"
}

# Split at position 0
# 检测到 target_turn_idx (2) > insert_position (0)
# 执行更新：target_turn_idx = 2 + 1 = 3 ✅

# 更新后的 insert_log
insert_log = {
    "insert_type": "short_dependency",
    "target_turn_idx": 3,           # ← 已更新！
    "source_func": "multiply",
    "nested_func": "is_prime"
}

# 最终 FSP（Split 后）
Turn 0: [mul]
Turn 1: []
Turn 2: [frankfurtermcp, quickchart]
Turn 3: [multiply, is_prime]        # ← 索引匹配！✅
```

---

## 修复效果

### 与 backward_to_query_magnet.py 修复的关系

这两个修复是互补的：

1. **FSP 生成器修复**（当前）：
   - 从源头修复数据生成
   - 确保生成的数据 turn_idx 正确
   - 适用于新生成的数据

2. **detect_turn_operations 修复**（已完成）：
   - 修复代码逻辑
   - 基于函数名匹配，不依赖 turn_idx
   - 适用于已有的错误数据

### 推荐策略

**短期**：保留 `detect_turn_operations` 的修复
- 兼容旧数据和新数据
- 不依赖 turn_idx，更鲁棒

**长期**：重新生成 FSP v2 数据
- 使用修复后的生成器
- 数据质量更高
- turn_idx 正确，便于调试

---

## 验证方法

### 生成新数据并验证

```bash
# 重新生成 FSP v2 数据
python src/generate_fsp_v2.py

# 运行验证脚本
python verify_bugfix.py
```

### 预期结果

```
【修复前】旧方法 (基于 turn_idx):
  ❌ 错误匹配次数: 128

【使用新数据】新方法 (基于 turn_idx):
  ✅ 错误匹配次数: 0
```

使用新生成的数据后，即使使用基于 turn_idx 的旧方法，也应该 0 错误。

---

## 代码注释说明

修复代码中添加了详细注释：

```python
# 修复：Split 后更新所有受影响的 logs 的 turn_idx
# Bug fix: 当 split 在某个位置插入空 turn 时，所有后续 turn 的索引 +1
# 需要更新 insert_logs 和 merge_logs 中的 turn_idx
```

这些注释确保未来维护者理解修复的目的和逻辑。

---

## 相关文件

- **FSP 生成器**: `src/generate_fsp_v2.py` (已修复)
- **检测函数**: `src/backward_to_query_magnet.py` (已修复)
- **Bug 报告**: `BUG_INFER_EXECUTION_ORDER.md`
- **修复文档**: `BUGFIX_DETECT_TURN_OPERATIONS.md`
- **案例分析**: `CASE_STUDY_NODE16_PATH2.md`

---

## 总结

✅ **双重修复策略**：
1. 源头修复：FSP 生成器确保数据正确
2. 代码修复：detect_turn_operations 鲁棒处理

✅ **向后兼容**：
- 新代码兼容新旧数据
- 旧数据也能正确处理

✅ **未来建议**：
- 重新生成 FSP v2 数据
- 使用正确的 turn_idx
- 便于调试和维护
