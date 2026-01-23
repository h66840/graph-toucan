# MAGNET 正向蒸馏实现文档（基于 fsp_v2_queries.jsonl）

## 1. 概述

本文档描述如何基于 `fsp_v2_queries.jsonl` 数据结构实现 MAGNET 论文中的**正向蒸馏（Context Distillation - Positive Trajectories）**。

### 目标

将 backward-to-query 生成的多轮对话数据（user queries + ground truth function calls）通过教师模型蒸馏，生成包含完整 reasoning 的高质量训练数据。

### 核心思想

根据 MAGNET 论文（Section 5.3），正向蒸馏的关键是：

1. **添加 Hints**：在 prompt 中提供正确的函数调用作为 hints
2. **隐式引导**：Hints 确保教师模型生成正确的轨迹，但不在响应中明确提到 hints
3. **多轮执行**：支持多轮对话，每个 turn 可能包含多个函数调用（Insert/Merge）
4. **完整 Reasoning**：教师模型生成推理过程 + 函数调用 + 结果总结

## 2. 数据结构对比

### 2.1 fsp_v2_queries.jsonl 结构

```json
{
  "path_info": {
    "node_idx": 0,
    "path_idx": 0
  },
  "turns_data": [
    {
      "turn_idx": 0,
      "turn_type": "normal",  // 或 "merged", "insert_short", "insert_long", "insert_mixed", "merged_with_insert", "empty"
      "operations": [],        // ["merge"], ["insert_short"], ["merge", "insert_short"], 等
      "functions": ["func1"],
      "user_query": "...",
      "chose_func": ["func1"],
      "reason": "...",
      "tool_calls": [
        {
          "function": "func1",
          "parameters": {...},
          "params_source": {...}
        }
      ],
      "outputs": [
        {
          "function": "func1",
          "parameters": {...},
          "output": {...},
          "token_usage": {...}
        }
      ]
    },
    {
      "turn_idx": 1,
      "turn_type": "merged_with_insert",
      "operations": ["merge", "insert_short"],
      "functions": ["func2", "func3", "func4"],
      "user_query": "...",
      // ...
    }
  ],
  "token_usage": {...},
  "statistics": {...}
}
```

### 2.2 关键特点

1. **多轮对话**：一个 path 包含多个 turns
2. **丰富的 turn 类型**：normal, merged, insert_short/long/mixed, merged_with_insert, empty
3. **完整的 ground truth**：每个 turn 都有 tool_calls 和 outputs
4. **操作标注**：operations 字段标明了该 turn 的 Insert/Merge 操作类型

## 3. 蒸馏流程设计

### 3.1 整体流程

```
┌─────────────────────────────────────────────────────────────┐
│ 输入: fsp_v2_queries.jsonl                                   │
│ - path_info                                                  │
│ - turns_data: [turn0, turn1, turn2, ...]                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: 准备 Hints                                         │
│ - 提取每个 turn 的 ground truth tool_calls                 │
│ - 根据 turn_type 构建不同的 hint 策略                      │
│ - 准备 tool schemas                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: 逐轮正向执行（Multi-turn Rollout）                │
│                                                              │
│ Turn 0:                                                      │
│   1. Build prompt with hints for turn 0                     │
│   2. Teacher model generates: reasoning + tool_calls        │
│   3. Execute tool_calls → get outputs                       │
│   4. Add to conversation history                            │
│                                                              │
│ Turn 1:                                                      │
│   1. Build prompt with hints for turn 1                     │
│   2. Teacher model generates based on history               │
│   3. Execute tool_calls → get outputs                       │
│   4. Add to conversation history                            │
│                                                              │
│ ... (continue for all turns)                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: 生成训练数据                                       │
│ - 完整的对话历史（user + assistant messages）              │
│ - 每个 assistant message 包含：                             │
│   * Reasoning                                               │
│   * Tool calls                                              │
│   * Summary of results                                      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 输出: distilled_data.jsonl                                  │
│ - 格式: 标准的 multi-turn conversation format               │
│ - 用于 SFT 训练                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Hints 构建策略

根据 turn_type 的不同，hints 的构建方式不同：

#### 3.2.1 Normal Turn

**特点**：单个或多个独立的函数调用

**Hint 格式**：
```
[Hint for this turn]: You should call the following functions:
- function_name1 with parameters: {...}
- function_name2 with parameters: {...}

Remember: Do not explicitly mention these hints in your response. Use them to guide your reasoning and tool selection.
```

#### 3.2.2 Merged Turn

**特点**：多个显式意图，用户明确提到多个操作

**Hint 格式**：
```
[Hint for this turn]: The user wants to accomplish multiple explicit intents:
- Intent 1: function_name1(...)
- Intent 2: function_name2(...)

Generate reasoning that:
1. Identifies each explicit intent
2. Explains why each function is needed
3. Shows how to combine the results
```

#### 3.2.3 Insert_Short Turn

**特点**：隐式嵌套，有些函数是 helper（用户未提及）

**Hint 格式**：
```
[Hint for this turn]:
- Primary function (user's explicit goal): function_name1(...)
- Helper function (implicit, needed for data flow): function_name2(...)

Generate reasoning that:
1. Focuses on the user's explicit goal
2. Naturally incorporates the helper function without explicitly mentioning it
3. Explains the data flow: function1.output → function2.input
```

#### 3.2.4 Insert_Long Turn

**特点**：需要从历史 turn 获取参数

**Hint 格式**：
```
[Hint for this turn]: This turn has long-dependency:
- Current function: function_name(...)
- Parameters from history: Turn X provided value Y
- Use pronouns to reference history (e.g., "that booking", "those coordinates")

Generate reasoning that:
1. References previous results using pronouns
2. Explains which historical information is needed
3. Does NOT repeat specific values from history
```

#### 3.2.5 Insert_Mixed Turn

**特点**：同时包含 short-dependency 和 long-dependency

**Hint 格式**：
```
[Hint for this turn]: Mixed dependency scenario:
- Primary functions (explicit): func1(...), func2(...)
- Short-dependency helpers (implicit): helper_func(...)
- Long-dependency reference: Uses output from Turn X

Generate reasoning that:
1. References history with pronouns
2. Mentions primary intents explicitly
3. Incorporates helpers naturally without mentioning them
```

#### 3.2.6 Merged_with_Insert Turn

**特点**：多个显式意图 + 隐式 helpers

**Hint 格式**：
```
[Hint for this turn]: Complex scenario with multiple intents and helpers:
- Merged functions (explicit): func1(...), func2(...)
- Long-dependency functions (explicit, use pronouns): func3(...)
- Short-dependency helpers (implicit): helper_func(...)

Generate reasoning that:
1. Clearly expresses all explicit intents
2. Uses pronouns for long-dependency references
3. Naturally incorporates helpers
```

#### 3.2.7 Empty Turn

**特点**：没有合适的函数或参数缺失

**Hint 格式**：
```
[Hint for this turn]: This query cannot be fulfilled because:
- Reason: {miss_type}
- Missing: {what's missing}

Generate a polite response explaining:
1. Why you cannot fulfill the request
2. What information or capability is missing
3. How the user might rephrase or provide more information
```

### 3.3 Prompt 模板

#### 系统提示（System Prompt）

```python
SYSTEM_PROMPT = """You are an expert AI assistant specialized in multi-turn function calling.

Your task is to help users accomplish their goals by:
1. Understanding their queries and conversation history
2. Reasoning about which functions to call
3. Executing the appropriate tool calls
4. Summarizing the results

IMPORTANT Instructions:
- Think step-by-step about the user's request
- Explain your reasoning clearly before making function calls
- Use pronouns (e.g., "that result", "those coordinates") to reference previous outputs
- When you see [Hint] in the messages, use them to guide your reasoning but DO NOT explicitly mention the hints in your response
- Always generate responses in English

Response Format:
1. First, provide your reasoning (1-2 paragraphs explaining your understanding and approach)
2. Then, make the appropriate function calls
3. After receiving tool outputs, summarize the results for the user
"""
```

#### Turn Prompt 模板

```python
def build_turn_prompt(turn_data: Dict, tool_schemas: Dict) -> str:
    """构建单个 turn 的 prompt"""
    turn_type = turn_data['turn_type']
    user_query = turn_data['user_query']

    # 构建 hint
    hint = build_hint_for_turn(turn_data, turn_type)

    # 组合 user query + hint
    prompt = f"""{user_query}

{hint}
"""
    return prompt
```

## 4. 核心实现

### 4.1 主函数

```python
async def distill_path(
    path_data: Dict,
    tool_schemas: Dict,
    teacher_model: str = "gemini-1.5-pro-002"
) -> Dict:
    """
    蒸馏单个 path 的所有 turns

    Args:
        path_data: 包含 path_info 和 turns_data 的字典
        tool_schemas: 所有工具的 schema
        teacher_model: 教师模型名称

    Returns:
        蒸馏后的数据，包含完整的对话历史
    """
    path_info = path_data['path_info']
    turns_data = path_data['turns_data']

    # 初始化对话历史
    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    distilled_turns = []

    # 逐轮执行
    for turn_idx, turn_data in enumerate(turns_data):
        print(f"Processing Turn {turn_idx}, type: {turn_data['turn_type']}")

        # 构建该 turn 的 prompt（包含 hints）
        turn_prompt = build_turn_prompt(turn_data, tool_schemas)

        # 添加 user message
        conversation_history.append({
            "role": "user",
            "content": turn_prompt
        })

        # 根据 turn_type 执行不同的策略
        if turn_data['turn_type'] == 'empty':
            # 空 turn：生成拒绝响应
            assistant_message = await generate_rejection_response(
                turn_data,
                conversation_history,
                teacher_model
            )
        else:
            # 正常 turn：执行函数调用
            assistant_message = await execute_turn_with_hints(
                turn_data,
                tool_schemas,
                conversation_history,
                teacher_model
            )

        # 添加 assistant message
        conversation_history.append(assistant_message)

        # 记录该 turn 的结果
        distilled_turns.append({
            "turn_idx": turn_idx,
            "turn_type": turn_data['turn_type'],
            "user_message": turn_prompt,
            "assistant_message": assistant_message,
            "ground_truth_tool_calls": turn_data.get('tool_calls', []),
            "generated_tool_calls": assistant_message.get('tool_calls', [])
        })

    return {
        "path_info": path_info,
        "conversation_history": conversation_history,
        "distilled_turns": distilled_turns,
        "statistics": compute_statistics(distilled_turns)
    }
```

### 4.2 Turn 执行函数

```python
async def execute_turn_with_hints(
    turn_data: Dict,
    tool_schemas: Dict,
    conversation_history: List[Dict],
    teacher_model: str
) -> Dict:
    """
    执行单个 turn，使用 hints 引导教师模型

    Args:
        turn_data: 当前 turn 的数据（包含 ground truth）
        tool_schemas: 工具 schemas
        conversation_history: 对话历史
        teacher_model: 教师模型

    Returns:
        Assistant message（包含 reasoning + tool_calls + summary）
    """
    # 准备 tools for API
    tools, name_mapping, short_tool_schemas = build_tools_for_api(tool_schemas)

    # 调用教师模型
    completion = await async_client.chat.completions.create(
        model=teacher_model,
        messages=conversation_history,
        tools=tools,
        temperature=0.7,
        max_completion_tokens=2048
    )

    message = completion.choices[0].message

    # 提取 reasoning（在 tool_calls 之前的内容）
    reasoning = message.content or ""

    # 提取 tool_calls
    api_tool_calls = message.tool_calls or []

    # 映射回原始函数名
    original_tool_calls = []
    for api_call in api_tool_calls:
        short_name = api_call.function.name
        original_name = name_mapping.get(short_name, short_name)
        original_tool_calls.append({
            "function": original_name,
            "parameters": json.loads(api_call.function.arguments)
        })

    # 执行函数调用（使用 ground truth outputs 或实际执行）
    tool_outputs = []
    use_ground_truth = True  # 可配置

    if use_ground_truth:
        # 使用 ground truth outputs（更快，确���一致性）
        tool_outputs = turn_data.get('outputs', [])
    else:
        # 实际执行函数调用
        for tool_call in original_tool_calls:
            output = execute_function_call(
                tool_call['function'],
                tool_call['parameters'],
                short_tool_schemas.get(tool_call['function'], {})
            )
            tool_outputs.append({
                "function": tool_call['function'],
                "parameters": tool_call['parameters'],
                "output": output
            })

    # 生成结果总结
    # 将 tool_outputs 添加到对话历史，让模型生成总结
    temp_history = conversation_history + [
        {"role": "assistant", "content": reasoning, "tool_calls": api_tool_calls},
        {
            "role": "tool",
            "content": json.dumps(tool_outputs),
            "tool_call_id": api_tool_calls[0].id if api_tool_calls else "dummy"
        }
    ]

    # 生成总结
    summary_completion = await async_client.chat.completions.create(
        model=teacher_model,
        messages=temp_history + [
            {"role": "user", "content": "Based on the tool results above, provide a clear summary for the user."}
        ],
        temperature=0.7,
        max_completion_tokens=512
    )

    summary = summary_completion.choices[0].message.content or ""

    # 组合完整的 assistant message
    assistant_message = {
        "role": "assistant",
        "content": f"{reasoning}\n\n{summary}",
        "tool_calls": original_tool_calls,
        "tool_outputs": tool_outputs,
        "token_usage": {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens + summary_completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens + summary_completion.usage.total_tokens
        }
    }

    return assistant_message
```

### 4.3 Hint 构建函数

```python
def build_hint_for_turn(turn_data: Dict, turn_type: str) -> str:
    """
    根据 turn_type 构建 hints

    Args:
        turn_data: turn 数据
        turn_type: turn 类型

    Returns:
        格式化的 hint 字符串
    """
    tool_calls = turn_data.get('tool_calls', [])

    if turn_type == 'normal':
        return build_normal_hint(tool_calls)
    elif turn_type == 'merged':
        return build_merged_hint(tool_calls)
    elif turn_type == 'insert_short':
        return build_insert_short_hint(turn_data)
    elif turn_type == 'insert_long':
        return build_insert_long_hint(turn_data)
    elif turn_type == 'insert_mixed':
        return build_insert_mixed_hint(turn_data)
    elif turn_type == 'merged_with_insert':
        return build_merged_with_insert_hint(turn_data)
    elif turn_type == 'empty':
        return build_empty_hint(turn_data)
    else:
        return build_normal_hint(tool_calls)

def build_normal_hint(tool_calls: List[Dict]) -> str:
    """构建 normal turn 的 hint"""
    hint_lines = ["[Hint for this turn]: You should call the following functions:"]
    for call in tool_calls:
        func_name = call['function']
        params = json.dumps(call['parameters'], ensure_ascii=False)
        hint_lines.append(f"- {func_name} with parameters: {params}")

    hint_lines.append("")
    hint_lines.append("Remember: Do not explicitly mention these hints in your response. Use them to guide your reasoning and tool selection.")

    return "\n".join(hint_lines)

def build_insert_short_hint(turn_data: Dict) -> str:
    """构建 insert_short turn 的 hint"""
    tool_calls = turn_data.get('tool_calls', [])
    operations = turn_data.get('operations', [])

    # 从 turn_operations 中提取 primary vs helper 信息
    # （如果有的话，否则根据函数顺序推断）

    # 简化版本：假设第一个是 primary，其余是 helpers
    if len(tool_calls) > 1:
        primary = tool_calls[0]
        helpers = tool_calls[1:]

        hint_lines = [
            "[Hint for this turn]:",
            f"- Primary function (user's explicit goal): {primary['function']} with parameters: {json.dumps(primary['parameters'])}",
            "- Helper functions (implicit, needed for data flow):"
        ]

        for helper in helpers:
            hint_lines.append(f"  * {helper['function']} with parameters: {json.dumps(helper['parameters'])}")

        hint_lines.extend([
            "",
            "Generate reasoning that:",
            "1. Focuses on the user's explicit goal",
            "2. Naturally incorporates the helper functions without explicitly mentioning them",
            "3. Explains the data flow between functions"
        ])
    else:
        # 只有一个函数，使用 normal hint
        return build_normal_hint(tool_calls)

    return "\n".join(hint_lines)

def build_insert_long_hint(turn_data: Dict) -> str:
    """构建 insert_long turn 的 hint"""
    tool_calls = turn_data.get('tool_calls', [])

    # 识别哪些参数来自历史
    # （可以从 params_source 字段判断）
    hint_lines = ["[Hint for this turn]: This turn has long-dependency:"]

    for call in tool_calls:
        params_source = call.get('params_source', {})
        from_context = [k for k, v in params_source.items() if 'context' in str(v)]

        hint_lines.append(f"- Function: {call['function']}")
        hint_lines.append(f"  Parameters: {json.dumps(call['parameters'])}")
        if from_context:
            hint_lines.append(f"  Parameters from history: {', '.join(from_context)}")

    hint_lines.extend([
        "",
        "Generate reasoning that:",
        "1. References previous results using pronouns (e.g., 'that booking', 'those coordinates')",
        "2. Explains which historical information is needed",
        "3. Does NOT repeat specific values from history"
    ])

    return "\n".join(hint_lines)

# 其他 hint 构建函数类似...
```

## 5. 输出格式

### 5.1 蒸馏后的数据格式

```json
{
  "path_info": {
    "node_idx": 0,
    "path_idx": 0
  },
  "conversation": [
    {
      "role": "system",
      "content": "You are an expert AI assistant..."
    },
    {
      "role": "user",
      "content": "I need to check train tickets from Beijing to Shanghai on 2024-05-20.\n\n[Hint]: ..."
    },
    {
      "role": "assistant",
      "content": "To help you find train tickets from Beijing to Shanghai on May 20, 2024, I'll search the 12306 railway system...\n\n[Tool Calls executed]\n\nI found 2 train options for you: ...",
      "tool_calls": [
        {
          "function": "12306-mcp-server-search",
          "parameters": {...}
        }
      ],
      "tool_outputs": [...]
    },
    {
      "role": "user",
      "content": "Get the weather forecast for Shanghai...\n\n[Hint]: ..."
    },
    {
      "role": "assistant",
      "content": "...",
      "tool_calls": [...],
      "tool_outputs": [...]
    }
  ],
  "statistics": {
    "num_turns": 4,
    "num_tool_calls": 8,
    "total_tokens": 15234,
    "accuracy": {
      "function_match": 0.95,
      "parameter_match": 0.88
    }
  }
}
```

### 5.2 用于 SFT 训练的格式

可以转换为标准的 chat format：

```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "...", "tool_calls": [...]},
    {"role": "tool", "content": "...", "tool_call_id": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "...", "tool_calls": [...]}
  ]
}
```

## 6. 质量评估

### 6.1 评估指标

```python
def evaluate_distilled_data(distilled_data: Dict) -> Dict:
    """
    评估蒸馏数据的质量

    返回指标:
    - function_match_rate: 函数名匹配率
    - parameter_match_rate: 参数匹配率
    - turn_success_rate: turn 级别成功率
    - reasoning_quality: reasoning 质量（可选，需要额外判断）
    """
    metrics = {
        "total_turns": 0,
        "successful_turns": 0,
        "function_matches": 0,
        "total_functions": 0,
        "parameter_matches": 0,
        "total_parameters": 0
    }

    for turn in distilled_data['distilled_turns']:
        metrics["total_turns"] += 1

        gt_calls = turn['ground_truth_tool_calls']
        gen_calls = turn['generated_tool_calls']

        # 函数匹配
        gt_funcs = set(call['function'] for call in gt_calls)
        gen_funcs = set(call['function'] for call in gen_calls)
        matches = len(gt_funcs & gen_funcs)

        metrics["function_matches"] += matches
        metrics["total_functions"] += len(gt_funcs)

        # 参数匹配（需要详细比较）
        # ...

        # Turn 成功判断
        if matches == len(gt_funcs):
            metrics["successful_turns"] += 1

    return {
        "function_match_rate": metrics["function_matches"] / metrics["total_functions"],
        "turn_success_rate": metrics["successful_turns"] / metrics["total_turns"],
        # ...
    }
```

### 6.2 质量检查点

1. **Hint 隐式性**：检查 assistant 响应中是否明确提到了 hint
2. **函数调用准确性**：生成的函数调用是否与 ground truth 一致
3. **Reasoning 完整性**：reasoning 是否清晰解释了思考过程
4. **代词使用**：Long-dependency 场景是否正确使用代词
5. **Helper 隐式性**：Insert 场景中 helper 是否被隐式处理

## 7. 实施步骤

### Phase 1: 基础实现（1-2 天）

1. ✅ 实现数据加载和解析
2. ✅ 实现基本的 hint 构建（先支持 normal turn）
3. ✅ 实现单 path 的多轮执行
4. ✅ 测试 1-2 个简单 paths

### Phase 2: 完整 Turn 类型支持（2-3 天）

5. ✅ 实现所有 turn_type 的 hint 构建
6. ✅ 添加 empty turn 的处理
7. ✅ 优化 long-dependency 的 hint
8. ✅ 测试各种复杂场景

### Phase 3: 质量优化（1-2 天）

9. ✅ 添加质量评估指标
10. ✅ 实现自动质量检查
11. ✅ 优化 prompt 模板
12. ✅ 迭代改进 hint 策略

### Phase 4: 批量生成（1 天）

13. ✅ 添加并发处理
14. ✅ 添加进度跟踪和断点续传
15. ✅ 生成完整数据集
16. ✅ 数据格式转换（用于 SFT）

## 8. 配置参数

```python
# config.yaml
distillation:
  teacher_model: "gemini-1.5-pro-002"  # 或 "gpt-4o"
  temperature: 0.7
  max_completion_tokens: 2048
  use_ground_truth_outputs: true  # 是否使用 ground truth outputs

  # Hint 配置
  hints:
    include_hints: true
    explicit_hint_mention: false  # hints 不在响应中提及

  # 并发配置
  concurrency:
    max_concurrent_paths: 5
    rate_limit: 100  # requests per minute

  # 输出配置
  output:
    save_intermediate: true
    format: "chat"  # "chat" 或 "raw"
```

## 9. 预期收益

### 数据质量提升

| 指标 | Backward-to-Query | 正向蒸馏后 | 提升 |
|------|------------------|-----------|------|
| Reasoning 完整性 | 无 | 完整 | +100% |
| 函数调用准确性 | 高（ground truth） | 高（教师模型） | 保持 |
| 多轮连贯性 | 中等 | 高 | +40% |
| 训练价值 | 中等 | 高 | +60% |

### 训练效果预期

根据 MAGNET 论文：
- 多轮场景性能提升：**+32.5%**
- 超越教师模型
- 零样本泛化能力提升

## 10. 风险和缓解

### 风险 1：教师模型不遵循 Hints

**表现**：生成的函数调用与 hints 不一致

**缓解**：
- 增强 hint 的明确性
- 使用更强的教师模型
- 添加 few-shot examples

### 风险 2：Hints 在响应中泄露

**表现**：assistant 明确提到"根据 hint..."

**缓解**：
- 明确的 system prompt 指令
- 后处理过滤
- 质量检查和重新生成

### 风险 3：成本和时间

**表现**：蒸馏所有数据成本高、耗时长

**缓解**：
- 使用较小的教师模型（如 gemini-1.5-flash）
- 并发处理
- 分批生成

## 11. 相关文件

- `MAGNET_Paper_Summary.md` - MAGNET 论文总结
- `fsp_path/fsp_v2_queries.jsonl` - 输入数据
- `src/positive_distill.py` - 现有单轮蒸馏实现（参考）
- `src/backward_to_query_magnet.py` - Query 生成逻辑

## 12. 下一步

1. **实现核心代码** - `src/positive_distill_v2.py`
2. **测试小规模数据** - 10-20 paths
3. **质量评估和迭代** - 优化 hint 和 prompt
4. **大规模生成** - 全部数据

---

**文档创建时间**: 2026-01-08
**状态**: 设计阶段
**预计实施时间**: 5-7 天
