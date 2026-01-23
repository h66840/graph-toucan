# TODO: Positive Distillation V2 实现问题清单

## 状态：待处理
**创建时间**：2026-01-09

---

## 问题列表

### 1. ✅ Hint 构建策略优化（已完成）

**问题描述**：
当前 hint 构建策略可能不够准确，特别是 `insert_short` 场景中如何区分 primary function 和 helper functions。

**解决方案**：
- ✅ 从 `turn_operations` 的 `insert_info` 中提取 nested_func_name（这些是 helpers）
- ✅ 根据 `insert_type` 区分 short-dependency 和 long-dependency
- ✅ 只给出函数名和依赖关系，不给参数值
- ✅ 让模型自己推理执行流程

**实现细节**：
```python
# 从 turn_operations 提取依赖信息
insert_info_list = turn_operations.get('insert_info', [])
for insert_info in insert_info_list:
    nested_func_name = insert_info.get('nested_func_name')
    source_func_name = insert_info.get('source_func_name')
    insert_type = insert_info.get('insert_type')
    # 构建数据流关系
    if insert_type == 'short_dependency':
        dependencies.append(f"{source_func_name} → {nested_func_name}")
```

**完成时间**：2026-01-09

---

### 2. ✅ 添加总结步骤（已完成）

**问题描述**：
每一轮的最后一步，如果模型认为该轮的任务已经完成了，需要增加一个总结，然后开始进行下一轮。

**解决方案**：
- ✅ 实现 Multi-step per turn 流程（参考 `process_single_record_v1`）
- ✅ 每个 turn 内部有循环，模型可以分多步执行
- ✅ 当模型不返回 tool_calls 时，认为 turn 完成，最后的消息就是总结
- ✅ 对话历史自然形成：user → assistant (reasoning + tool_calls) → tool → ... → assistant (summary)

**实现流程**：
```python
for turn_idx, turn_data in enumerate(turns_data):
    # 添加 user message (query + hint)
    conversation_history.append({"role": "user", "content": query + hint})

    # Multi-step 循环
    for step_num in range(1, max_steps_per_turn + 1):
        completion = await async_client.chat.completions.create(...)
        message = completion.choices[0].message

        if not message.tool_calls:
            # 没有 tool calls → turn 完成，这就是总结
            conversation_history.append({
                "role": "assistant",
                "content": message.content
            })
            break

        # 有 tool calls → 执行并继续
        conversation_history.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": [...]
        })

        # 执行函数
        for tool_call in message.tool_calls:
            output = await execute_function_call_async(...)
            conversation_history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(output)
            })
```

**关键特点**：
1. ✅ Hints 只作为引导，不强制执行
2. ✅ 模型决定执行流程和步骤数
3. ✅ 必须实际执行函数（不再使用 ground truth outputs）
4. ✅ 总结是自然生成的，不需要额外 API 调用

**完成时间**：2026-01-09

---

### 3. ✅ Tool Schemas 格式支持（已完成）

**问题描述**：
需要确保支持 `fsp_v2_queries.jsonl` 中 tool schemas 的实际格式。

**发现的问题**：
- `fsp_v2_queries.jsonl` 中 **没有** `nodes_tool_schema` 字段（设计疏漏）
- 需要从外部文件 `tool_schema_with_outputformat.json` 加载

**解决方案**：
- ✅ 从 `tool_schema_with_outputformat.json` 加载所有 tool schemas
- ✅ 只保留 `function_schema`，移除 `output_schema` 字段
- ✅ 根据每个 path 的 `functions` 字段提取所需的 schemas
- ✅ 在 batch processing 时为每个 path 动态提取 schemas

**实现细节**：
```python
def load_all_tool_schemas(schema_path: str) -> Dict[str, Dict[str, Any]]:
    """加载所有 tool schemas（不包含 output format）"""
    with open(schema_path, "r", encoding="utf-8") as f:
        all_schemas = json.load(f)

    # 只保留 function_schema，移除 output_schema
    tool_schemas = {}
    for tool_name, tool_data in all_schemas.items():
        if "function_schema" in tool_data:
            tool_schemas[tool_name] = {
                "function_schema": tool_data["function_schema"]
            }
    return tool_schemas

def extract_tool_schemas_for_path(path_data: Dict, all_tool_schemas: Dict) -> Dict:
    """从 path_data 中提取需要的 tool schemas"""
    function_names = set()
    for turn_data in path_data.get('turns_data', []):
        functions = turn_data.get('functions', [])
        function_names.update(functions)

    path_tool_schemas = {}
    for func_name in function_names:
        if func_name in all_tool_schemas:
            path_tool_schemas[func_name] = all_tool_schemas[func_name]
    return path_tool_schemas
```

**完成时间**：2026-01-09

---

### 4. ✅ Empty Turn 的 Miss Type 提取（已完成）

**问题描述**：
Empty turn 的 hint 需要说明为什么无法完成任务（缺少函数还是缺少参数），但当前没有提取这个信息。

**数据结构发现**：
Empty turn 在 `fsp_v2_queries.jsonl` 中包含以下字段：
```json
{
  "turn_type": "empty",
  "user_query": "...",
  "response": "预期的拒绝回复",
  "miss_type": "miss_func" or "miss_params",
  "reason": "详细说明缺失原因"
}
```

**实现方案**：
- ✅ 提取 `miss_type` 字段区分缺失类型
- ✅ 根据 miss_type 生成针对性的 hint
- ✅ 在输出中记录 miss_type、ground_truth_response 和 reason

**实现细节**：
```python
def build_empty_hint(turn_data: Dict) -> str:
    miss_type = turn_data.get('miss_type', 'unknown')

    if miss_type == 'miss_func':
        hint_lines = [
            "[Hint]: This query cannot be fulfilled.",
            "Reason: Required function is not available.",
            "",
            "Generate a polite response explaining:",
            "- That you lack the capability to perform this action",
            "- What specific function or feature is missing",
            "- Possible alternatives or how the user might proceed differently"
        ]
    elif miss_type == 'miss_params':
        hint_lines = [
            "[Hint]: This query cannot be fulfilled.",
            "Reason: Required parameters are missing or unclear.",
            "",
            "Generate a polite response explaining:",
            "- What specific information is needed to proceed",
            "- How the user can provide the missing details",
            "- Why these parameters are necessary for the request"
        ]
    else:
        # 通用 hint（fallback）
        ...

    return "\n".join(hint_lines)

# 在 distilled_turns 中记录额外信息
if turn_type == 'empty':
    turn_result["miss_type"] = turn_data.get('miss_type', 'unknown')
    turn_result["ground_truth_response"] = turn_data.get('response', '')
    turn_result["reason"] = turn_data.get('reason', '')
```

**完成时间**：2026-01-09

---

### 5. ✅ 错误处理、统计和鲁棒性（已完成）

**问题描述**：
如果教师模型生成的函数与 ground truth 不匹配，或者生成失败，应该如何处理？

**实现方案**：
根据用户需求，实现了以下功能（**不包含重试机制**）：

1. ✅ **函数匹配率统计**：
   - 计算生成的函数与 ground truth 的匹配率
   - 统计每个 turn 的匹配情况
   - 在最终 summary 中显示整体匹配率

2. ✅ **断点续传机制**：
   - 通过 `--resume` 参数启用
   - 读取已处理的 paths，跳过已成功处理的记录
   - 使用追加模式写入文件，避免覆盖已有结果
   - 只记录成功的 paths（没有 error 字段的）

3. ✅ **早停机制**：
   - 通过 `--early-stop N` 参数配置（默认 3）
   - 如果连续 N 个 batch 全部失败，自动停止
   - 防止在严重错误时浪费 API 调用
   - 设置为 0 可禁用早停

**实现细节**：

```python
async def run_distillation_v2(
    max_paths: Optional[int] = None,
    batch_size: int = 5,
    resume: bool = False,  # 断点续传
    early_stop_batches: int = 3  # 早停阈值
) -> None:
    # 断点续传：读取已成功处理的 paths
    successfully_processed_paths = set()
    if resume and os.path.exists(DISTILL_V2_OUTPUT):
        # 读取已处理的 (node_idx, path_idx)
        for line in f:
            result = json.loads(line)
            if 'error' not in result:
                successfully_processed_paths.add((node_idx, path_idx))

    # 统计函数匹配率
    total_function_matches = 0
    total_functions = 0
    for turn in distilled_turns:
        gt_funcs = set(call['function'] for call in turn['ground_truth_tool_calls'])
        gen_funcs = set(turn['generated_tool_calls'])
        total_function_matches += len(gt_funcs & gen_funcs)
        total_functions += len(gt_funcs)

    # 早停检查
    if batch_errors == len(batch):
        consecutive_failed_batches += 1
        if consecutive_failed_batches >= early_stop_batches:
            print("🛑 EARLY STOPPING TRIGGERED")
            break
```

**命令行参数**：
```bash
# 断点续传
python src/positive_distill_v2.py --resume

# 配置早停阈值
python src/positive_distill_v2.py --early-stop 5

# 禁用早停
python src/positive_distill_v2.py --early-stop 0

# 组合使用
python src/positive_distill_v2.py --resume --early-stop 3 --batch-size 5
```

**输出统计信息**：
```
DISTILLATION V2 SUMMARY
======================================
Total paths: 100
Processed: 95
Failed: 5
Success rate: 95.0%
Total tokens used: 150000
Function match rate: 87.50% (350/400)
======================================
```

**未实现的功能**（按用户需求）：
- ❌ 重试机制（用户明确要求不实现）
- ❌ 自动调整 temperature（不需要）
- ❌ 详细的错误分类（当前只记录异常信息）

**完成时间**：2026-01-09

---

## 优先级总结

| 问题 | 优先级 | 工作量 | 状态 |
|------|--------|--------|------|
| 1. Hint 构建策略优化 | 中 | 1-2h | ✅ 已完成 (2026-01-09) |
| 2. 添加总结步骤 | 高 | 2-3h | ✅ 已完成 (2026-01-09) |
| 3. Tool Schemas 格式支持 | 中 | 1h | ✅ 已完成 (2026-01-09) |
| 4. Empty Turn 处理 | 低 | 1-2h | ✅ 已完成 (2026-01-09) |
| 5. 错误处理和鲁棒性 | 中 | 2-3h | ✅ 已完成 (2026-01-09) |

---

## 下一步

1. ✅ 完成问题 1（Hint 构建策略优化）- 已完成
2. ✅ 完成问题 2（添加总结步骤）- 已完成
3. ✅ 完成问题 3（Tool Schemas 格式）- 已完成
4. ✅ 完成问题 4（Empty Turn 处理）- 已完成
5. ✅ 完成问题 5（错误处理和鲁棒性）- 已完成
6. ⏳ **当前任务**：测试完整流程
   - 运行 `python src/positive_distill_v2.py --test` 验证实现
   - 测试断点续传功能（`--resume`）
   - 测试早停机制（`--early-stop`）
   - 检查函数匹配率统计
   - 验证所有 turn types 的 hints 是否正确构建
   - 确认 multi-step 流程是否正常工作
   - 检查 empty turn 的拒绝回复质量

---

**更新时间**：2026-01-09
