"""
正向蒸馏 V2：基于 fsp_v2_queries.jsonl 的多轮蒸馏

实现 MAGNET 的 Context Distillation：
1. 为每个 turn 构建 hints（根据 turn_type 不同采用不同策略）
2. 使用教师模型逐轮生成 reasoning + function calls
3. 执行函数获取 outputs（或使用 ground truth）
4. 生成完整的对话历史作为 SFT 训练数据
"""

import asyncio
import json
import os
import sys
import yaml
import hashlib
import copy
from typing import Any, Dict, List, Optional, Tuple
from tqdm import tqdm
from openai import AsyncOpenAI

# 导入 backward_to_query 中的函数执行逻辑
sys.path.insert(0, os.path.dirname(__file__))
from backward_to_query import execute_function_call

# 路径配置
ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
FSP_V2_PATH = os.path.join(ROOT_DIR, "fsp_path/fsp_v2_queries.jsonl")
DISTILL_V2_OUTPUT = os.path.join(ROOT_DIR, "distill/distill_v3.jsonl")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
TOOL_SCHEMA_PATH = os.path.join(ROOT_DIR, "tool_info/tool_schema_with_outputformat.json")


def load_config(config_path: str = CONFIG_PATH) -> Dict[str, Any]:
    """加载配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


def load_all_tool_schemas(schema_path: str = TOOL_SCHEMA_PATH) -> Dict[str, Dict[str, Any]]:
    """
    加载所有 tool schemas（不包含 output format）

    Args:
        schema_path: tool schema 文件路径

    Returns:
        {tool_name: {"function_schema": {...}}} 格式的字典
    """
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


def extract_tool_schemas_for_path(path_data: Dict, all_tool_schemas: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    从 path_data 中提取需要的 tool schemas

    Args:
        path_data: path 数据
        all_tool_schemas: 所有的 tool schemas

    Returns:
        该 path 需要的 tool schemas
    """
    # 收集该 path 中所有出现的函数名
    function_names = set()
    for turn_data in path_data.get('turns_data', []):
        functions = turn_data.get('functions', [])
        function_names.update(functions)

    # 提取对应的 schemas
    path_tool_schemas = {}
    for func_name in function_names:
        if func_name in all_tool_schemas:
            path_tool_schemas[func_name] = all_tool_schemas[func_name]
        else:
            print(f"    Warning: Tool schema not found for function: {func_name}")

    return path_tool_schemas


# 加载配置
config = load_config()

# 初始化 AsyncOpenAI 客户端
api_key_env = config["api"].get("api_key_env")
if api_key_env:
    api_key = os.getenv(api_key_env, "EMPTY")
else:
    api_key = config["api"].get("api_key", "EMPTY")
base_url = config["api"]["base_url"]

async_client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)

# 模型配置
TEACHER_MODEL = config["model"].get("teacher", config["model"]["default"])

# 系统提示
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


def shorten_tool_name(name: str, max_length: int = 64) -> str:
    """缩短工具名称到指定长度"""
    if len(name) <= max_length:
        return name
    hash_suffix = hashlib.md5(name.encode()).hexdigest()[:5]
    max_prefix = max_length - 6
    return f"{name[:max_prefix]}_{hash_suffix}"


def build_tools_for_api(
    tool_schemas: Dict[str, Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], Dict[str, str], Dict[str, Dict[str, Any]]]:
    """
    将 tool schemas 转换为 OpenAI API 格式

    Returns:
        - tools: OpenAI API 格式的 tools 列表（名称已缩短）
        - name_mapping: {short_name: original_name} 映射字典
        - short_tool_schemas: 缩短名称后的 tool schemas {short_name: tool_meta_with_short_name}
    """
    tools = []
    name_mapping = {}
    short_tool_schemas = {}  # short_name -> tool_meta (with short name in schema)

    for original_name, tool_meta in tool_schemas.items():
        # 支持两种格式：function_schema 或 tool_schema
        tool_schema = tool_meta.get("function_schema") or tool_meta.get("tool_schema", {})

        if tool_schema:
            short_name = shorten_tool_name(original_name)
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


def build_hint_for_turn(turn_data: Dict, turn_type: str) -> str:
    """
    根据 turn_type 构建 hints

    Args:
        turn_data: turn 数据
        turn_type: turn 类型

    Returns:
        格式化的 hint 字符串
    """
    if turn_type == 'normal':
        return build_normal_hint(turn_data)
    elif turn_type == 'merged':
        return build_merged_hint(turn_data)
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
        return build_normal_hint(turn_data)


def build_normal_hint(turn_data: Dict) -> str:
    """构建 normal turn 的 hint"""
    tool_calls = turn_data.get('tool_calls', [])

    if len(tool_calls) == 1:
        hint_lines = [f"[Hint]: You should call the function: {tool_calls[0]['function']}"]
    else:
        hint_lines = ["[Hint]: You should call the following functions:"]
        for call in tool_calls:
            hint_lines.append(f"- {call['function']}")

    hint_lines.append("")
    hint_lines.append("Remember: Do not explicitly mention these hints in your response. Use them to guide your reasoning and tool selection.")

    return "\n".join(hint_lines)


def build_merged_hint(turn_data: Dict) -> str:
    """构建 merged turn 的 hint"""
    tool_calls = turn_data.get('tool_calls', [])

    hint_lines = ["[Hint]: This turn has multiple independent intents:"]
    for call in tool_calls:
        hint_lines.append(f"- {call['function']}")

    hint_lines.extend([
        "",
        "These are separate user goals that should both be addressed.",
        "Generate reasoning that identifies each explicit intent and explains how to accomplish them."
    ])

    return "\n".join(hint_lines)


def build_insert_short_hint(turn_data: Dict) -> str:
    """构建 insert_short turn 的 hint"""
    tool_calls = turn_data.get('tool_calls', [])
    turn_operations = turn_data.get('turn_operations', {})

    # 提取 insert 信息
    insert_info_list = turn_operations.get('insert_info', [])
    nested_funcs = set()
    dependencies = []

    for insert_info in insert_info_list:
        nested_func_name = insert_info.get('nested_func_name')
        source_func_name = insert_info.get('source_func_name')
        insert_type = insert_info.get('insert_type')

        if nested_func_name and insert_type == 'short_dependency':
            nested_funcs.add(nested_func_name)
            if source_func_name:
                dependencies.append(f"{source_func_name} → {nested_func_name}")

    # 区分 primary 和 helper functions
    primary_funcs = [call['function'] for call in tool_calls if call['function'] not in nested_funcs]
    helper_funcs = [call['function'] for call in tool_calls if call['function'] in nested_funcs]

    hint_lines = ["[Hint]: Data flow for this turn:"]

    if primary_funcs:
        if len(primary_funcs) == 1:
            hint_lines.append(f"- Primary function: {primary_funcs[0]}")
        else:
            hint_lines.append(f"- Primary functions: {', '.join(primary_funcs)}")

    if helper_funcs:
        if len(helper_funcs) == 1:
            hint_lines.append(f"- Helper function: {helper_funcs[0]} (implicit, provides data for primary function)")
        else:
            hint_lines.append(f"- Helper functions: {', '.join(helper_funcs)} (implicit)")

    if dependencies:
        hint_lines.append("- Data flow: " + ", ".join(dependencies))

    hint_lines.extend([
        "",
        "Note: The helper function is implicit in the user's goal and should be incorporated naturally.",
        "Focus on the primary function's purpose, but use the helper to complete the task."
    ])

    return "\n".join(hint_lines)


def build_insert_long_hint(turn_data: Dict) -> str:
    """构建 insert_long turn 的 hint"""
    tool_calls = turn_data.get('tool_calls', [])
    turn_operations = turn_data.get('turn_operations', {})
    turn_idx = turn_data.get('turn_idx', 0)

    # 提取 long-dependency 信息
    insert_info_list = turn_operations.get('insert_info', [])
    long_dependencies = []

    for insert_info in insert_info_list:
        nested_func_name = insert_info.get('nested_func_name')
        source_func_name = insert_info.get('source_func_name')
        source_turn_idx = insert_info.get('source_turn_idx')
        insert_type = insert_info.get('insert_type')

        if nested_func_name and insert_type == 'long_dependency':
            if source_func_name and source_turn_idx is not None:
                long_dependencies.append({
                    'func': nested_func_name,
                    'source_turn': source_turn_idx,
                    'source_func': source_func_name
                })

    hint_lines = ["[Hint]: This turn requires data from previous conversation:"]

    for dep in long_dependencies:
        hint_lines.append(f"- Function: {dep['func']}")
        hint_lines.append(f"  Depends on: output from Turn {dep['source_turn']} ({dep['source_func']})")

    if long_dependencies:
        hint_lines.extend([
            "",
            "Important:",
            "- Use pronouns to reference previous results (e.g., 'that booking', 'those coordinates')",
            "- Do NOT repeat specific values from history",
            "- Let the data flow naturally from the conversation context"
        ])

    return "\n".join(hint_lines)


def build_insert_mixed_hint(turn_data: Dict) -> str:
    """构建 insert_mixed turn 的 hint"""
    tool_calls = turn_data.get('tool_calls', [])
    turn_operations = turn_data.get('turn_operations', {})
    turn_idx = turn_data.get('turn_idx', 0)

    # 提取 insert 信息
    insert_info_list = turn_operations.get('insert_info', [])
    short_deps = []
    long_deps = []

    for insert_info in insert_info_list:
        nested_func_name = insert_info.get('nested_func_name')
        source_func_name = insert_info.get('source_func_name')
        source_turn_idx = insert_info.get('source_turn_idx')
        insert_type = insert_info.get('insert_type')

        if nested_func_name:
            if insert_type == 'short_dependency' and source_func_name:
                short_deps.append(f"{source_func_name} → {nested_func_name}")
            elif insert_type == 'long_dependency' and source_turn_idx is not None:
                long_deps.append({
                    'func': nested_func_name,
                    'source_turn': source_turn_idx,
                    'source_func': source_func_name
                })

    hint_lines = ["[Hint]: Mixed dependency scenario:"]
    hint_lines.append("- Functions involved: " + ", ".join([call['function'] for call in tool_calls]))

    if short_deps:
        hint_lines.append(f"- Short-dependency data flow: {', '.join(short_deps)}")

    if long_deps:
        hint_lines.append("- Long-dependency references:")
        for dep in long_deps:
            hint_lines.append(f"  * {dep['func']} depends on Turn {dep['source_turn']} ({dep['source_func']})")

    hint_lines.extend([
        "",
        "Guidance:",
        "- Use pronouns for long-dependency references",
        "- Incorporate short-dependency helpers naturally",
        "- Execute in logical order based on data dependencies"
    ])

    return "\n".join(hint_lines)


def build_merged_with_insert_hint(turn_data: Dict) -> str:
    """构建 merged_with_insert turn 的 hint"""
    tool_calls = turn_data.get('tool_calls', [])
    turn_operations = turn_data.get('turn_operations', {})
    turn_idx = turn_data.get('turn_idx', 0)

    # 提取 merged 和 insert 信息
    merge_info = turn_operations.get('merge_info', {})
    merged_names = merge_info.get('merged_names', [])

    insert_info_list = turn_operations.get('insert_info', [])
    nested_funcs = set()
    short_deps = []
    long_deps = []

    for insert_info in insert_info_list:
        nested_func_name = insert_info.get('nested_func_name')
        source_func_name = insert_info.get('source_func_name')
        source_turn_idx = insert_info.get('source_turn_idx')
        insert_type = insert_info.get('insert_type')

        if nested_func_name:
            nested_funcs.add(nested_func_name)
            if insert_type == 'short_dependency' and source_func_name:
                short_deps.append(f"{source_func_name} → {nested_func_name}")
            elif insert_type == 'long_dependency' and source_turn_idx is not None:
                long_deps.append({
                    'func': nested_func_name,
                    'source_turn': source_turn_idx,
                    'source_func': source_func_name
                })

    hint_lines = ["[Hint]: Complex multi-intent scenario:"]

    # 显式意图
    if merged_names:
        hint_lines.append("- Explicit intents: " + ", ".join(merged_names))

    # Helper functions
    helpers = [func for func in nested_funcs if func not in merged_names]
    if helpers:
        hint_lines.append("- Helper functions: " + ", ".join(helpers) + " (implicit)")

    # 依赖关系
    if short_deps:
        hint_lines.append(f"- Short-dependency flow: {', '.join(short_deps)}")

    if long_deps:
        hint_lines.append("- Long-dependency references:")
        for dep in long_deps:
            hint_lines.append(f"  * {dep['func']} from Turn {dep['source_turn']}")

    hint_lines.extend([
        "",
        "Guidance:",
        "- Address all explicit intents clearly",
        "- Use pronouns for long-dependency references",
        "- Naturally incorporate helpers without explicitly mentioning them"
    ])

    return "\n".join(hint_lines)


def build_empty_hint(turn_data: Dict) -> str:
    """
    构建 empty turn 的 hint

    根据 miss_type 提供不同的引导：
    - miss_func: 缺少所需的函数/能力
    - miss_params: 缺少必需的参数信息
    """
    miss_type = turn_data.get('miss_type', 'unknown')
    reason = turn_data.get('reason', '')

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
        # 通用 hint（如果 miss_type 未知或不存在）
        hint_lines = [
            "[Hint]: This query cannot be fulfilled.",
            "",
            "Generate a polite response explaining:",
            "- Why you cannot fulfill the request",
            "- What information or capability is missing",
            "- How the user might rephrase or provide more information"
        ]

    return "\n".join(hint_lines)



async def distill_path(
    path_data: Dict,
    tool_schemas: Dict[str, Dict[str, Any]]
) -> Dict:
    """
    蒸馏单个 path 的所有 turns

    实现 multi-turn multi-step 流程：
    - 每个 turn 可能包含多个 steps
    - 模型决定何时完成当前 turn（不返回 tool_calls）
    - hints 只作为引导，不强制执行

    Args:
        path_data: 包含 path_info 和 turns_data 的字典
        tool_schemas: 所有工具的 schema

    Returns:
        蒸馏后的数据，包含完整的对话历史
    """
    path_info = path_data['path_info']
    turns_data = path_data['turns_data']

    # 构建 tools for API
    tools, name_mapping, short_tool_schemas = build_tools_for_api(tool_schemas)

    # 初始化对话历史
    conversation_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    distilled_turns = []
    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0
    }

    # 逐轮执行
    for turn_idx, turn_data in enumerate(turns_data):
        turn_type = turn_data['turn_type']
        print(f"    Turn {turn_idx}, type: {turn_type}")

        # 构建该 turn 的 prompt
        user_query = turn_data.get('user_query', '')
        hint = build_hint_for_turn(turn_data, turn_type)
        turn_prompt_with_hint = f"{user_query}\n\n{hint}"

        # 🔥 重要：conversation_history 只保存不带 hint 的 user_query
        conversation_history.append({
            "role": "user",
            "content": user_query
        })

        # 🔥 Multi-step 循环（参考 process_single_record_v1）
        turn_completed = False
        max_steps_per_turn = 10
        turn_steps = []
        turn_generated_calls = []

        for step_num in range(1, max_steps_per_turn + 1):
            try:
                # 🔥 构建包含 hint 的临时 messages 用于 API 调用
                # 第一步：使用带 hint 的 prompt
                # 后续步骤：使用 conversation_history（不含 hint）
                if step_num == 1:
                    # 第一步：用 hint 引导
                    api_messages = conversation_history[:-1] + [{
                        "role": "user",
                        "content": turn_prompt_with_hint
                    }]
                else:
                    # 后续步骤：用对话历史（不含 hint）
                    api_messages = conversation_history

                # 调用教师模型
                completion = await async_client.chat.completions.create(
                    model=TEACHER_MODEL,
                    messages=api_messages,
                    tools=tools,
                    temperature=0.7,
                    max_completion_tokens=2048
                )

                message = completion.choices[0].message

                # 累计 token 使用
                total_token_usage['prompt_tokens'] += completion.usage.prompt_tokens
                total_token_usage['completion_tokens'] += completion.usage.completion_tokens
                total_token_usage['total_tokens'] += completion.usage.total_tokens

                # 检查是否有 tool_calls
                if not message.tool_calls:
                    # 没有 tool calls → turn 完成，这就是总结
                    print(f"      Step {step_num}: Turn completed (summary)")
                    conversation_history.append({
                        "role": "assistant",
                        "content": message.content or ""
                    })

                    turn_steps.append({
                        "step_num": step_num,
                        "type": "summary",
                        "content": message.content or ""
                    })

                    turn_completed = True
                    break

                # 有 tool calls → 执行函数
                print(f"      Step {step_num}: {len(message.tool_calls)} tool calls")

                # 映射回原始函数名
                original_tool_calls = []
                for api_call in message.tool_calls:
                    short_name = api_call.function.name
                    original_name = name_mapping.get(short_name, short_name)
                    try:
                        params = json.loads(api_call.function.arguments)
                    except json.JSONDecodeError:
                        params = {}
                    original_tool_calls.append({
                        "function": original_name,
                        "parameters": params
                    })
                    turn_generated_calls.append(original_name)

                # 添加 assistant message（带 tool_calls）
                conversation_history.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": tc.type,
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })

                # 执行函数并添加 tool messages
                step_outputs = []
                for i, tc in enumerate(message.tool_calls):
                    short_func_name = tc.function.name
                    original_func_name = name_mapping.get(short_func_name, short_func_name)

                    try:
                        params = json.loads(tc.function.arguments)
                    except json.JSONDecodeError:
                        params = {}

                    try:
                        # 实际执行函数
                        output_result = await execute_function_call(
                            original_func_name,
                            params
                        )

                        # 提取实际的 output（移除 token_usage）
                        if output_result:
                            if "token_usage" in output_result:
                                output = {k: v for k, v in output_result.items() if k != "token_usage"}
                            else:
                                output = output_result
                        else:
                            output = {"error": "Function execution returned None"}

                        step_outputs.append({
                            "function": original_func_name,
                            "output": output
                        })

                        # 添加 tool message
                        conversation_history.append({
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": json.dumps(output, ensure_ascii=False)
                        })

                    except Exception as e:
                        # 重新抛出异常，添加上下文信息
                        raise RuntimeError(
                            f"Error executing function {original_func_name} with parameters {params} at turn {turn_idx}, step {step_num}: {e}"
                        ) from e

                turn_steps.append({
                    "step_num": step_num,
                    "type": "tool_calls",
                    "reasoning": message.content or "",
                    "tool_calls": original_tool_calls,
                    "outputs": step_outputs
                })

            except Exception as e:
                # 重新抛出异常，添加上下文信息
                raise RuntimeError(
                    f"Error at turn {turn_idx}, step {step_num}: {e}"
                ) from e

        if not turn_completed:
            print(f"      Warning: Turn {turn_idx} reached max steps ({max_steps_per_turn})")

        # 记录该 turn 的结果
        turn_result = {
            "turn_idx": turn_idx,
            "turn_type": turn_type,
            "user_query": user_query,
            "hint": hint,
            "steps": turn_steps,
            "total_steps": len(turn_steps),
            "ground_truth_tool_calls": turn_data.get('tool_calls', []),
            "generated_tool_calls": turn_generated_calls
        }

        # Empty turn 的额外信息
        if turn_type == 'empty':
            turn_result["miss_type"] = turn_data.get('miss_type', 'unknown')
            turn_result["ground_truth_response"] = turn_data.get('response', '')
            turn_result["reason"] = turn_data.get('reason', '')

        distilled_turns.append(turn_result)

    # 构建 tools 列表：使用缩短名称的 schemas
    tools_list = [
        {"function_schema": tool_meta.get("function_schema", {})}
        for tool_meta in short_tool_schemas.values()
        if "function_schema" in tool_meta
    ]

    return {
        "path_info": path_info,
        "conversation_history": conversation_history,
        "distilled_turns": distilled_turns,
        "token_usage": total_token_usage,
        "statistics": compute_statistics(distilled_turns),
        "tools": tools_list,
        "tool_name_mapping": name_mapping
    }


def compute_statistics(distilled_turns: List[Dict]) -> Dict:
    """计算蒸馏结果的统计信息"""
    total_turns = len(distilled_turns)
    total_steps = sum(turn['total_steps'] for turn in distilled_turns)
    total_tool_calls = sum(len(turn['generated_tool_calls']) for turn in distilled_turns)

    # 计算函数匹配率
    function_matches = 0
    total_functions = 0

    for turn in distilled_turns:
        gt_funcs = set(call['function'] for call in turn['ground_truth_tool_calls'])
        gen_funcs = set(turn['generated_tool_calls'])

        function_matches += len(gt_funcs & gen_funcs)
        total_functions += len(gt_funcs)

    function_match_rate = function_matches / total_functions if total_functions > 0 else 0.0

    return {
        "num_turns": total_turns,
        "total_steps": total_steps,
        "avg_steps_per_turn": total_steps / total_turns if total_turns > 0 else 0,
        "num_tool_calls": total_tool_calls,
        "function_match_rate": function_match_rate
    }


async def run_distillation_v2(
    max_paths: Optional[int] = None,
    batch_size: int = 5,
    resume: bool = False,
    early_stop_batches: int = 3
) -> None:
    """
    运行正向蒸馏 V2

    Args:
        max_paths: 最多处理的 path 数（None 表示全部）
        batch_size: 批处理大小
        resume: 是否启用断点续传（跳过已成功处理的 path）
        early_stop_batches: 连续多少个 batch 全部失败后停止（0 表示不启用早停）
    """
    print(f"Loading FSP V2 data from {FSP_V2_PATH}...")

    paths = []
    with open(FSP_V2_PATH, "r", encoding="utf-8") as f:
        for line in f:
            paths.append(json.loads(line))
            if max_paths and len(paths) >= max_paths:
                break

    print(f"Loaded {len(paths)} paths.")

    # 🔥 加载所有 tool schemas
    print(f"Loading tool schemas from {TOOL_SCHEMA_PATH}...")
    all_tool_schemas = load_all_tool_schemas()
    print(f"Loaded {len(all_tool_schemas)} tool schemas.")

    print(f"Output -> {DISTILL_V2_OUTPUT}\n")

    os.makedirs(os.path.dirname(DISTILL_V2_OUTPUT), exist_ok=True)

    # 断点续传：读取已成功处理的 path
    successfully_processed_paths = set()

    if resume and os.path.exists(DISTILL_V2_OUTPUT):
        print(f"\n🔄 Resume mode enabled, reading existing results from {DISTILL_V2_OUTPUT}...")
        try:
            with open(DISTILL_V2_OUTPUT, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        result = json.loads(line)
                        path_info = result.get('path_info', {})
                        node_idx = path_info.get('node_idx')
                        path_idx = path_info.get('path_idx')

                        # 只记录成功处理的（没有 error 字段）
                        if node_idx is not None and path_idx is not None and 'error' not in result:
                            successfully_processed_paths.add((node_idx, path_idx))
                    except json.JSONDecodeError:
                        continue

            print(f"✅ Found {len(successfully_processed_paths)} successfully processed paths.")

            # 过滤掉已处理的 paths
            original_count = len(paths)
            paths = [
                p for p in paths
                if (p.get('path_info', {}).get('node_idx'),
                    p.get('path_info', {}).get('path_idx')) not in successfully_processed_paths
            ]

            skipped_count = original_count - len(paths)
            print(f"📋 Skipping {skipped_count} already processed paths.")
            print(f"📋 Remaining paths to process: {len(paths)}\n")

            if len(paths) == 0:
                print("\n✅ All paths already processed! Nothing to do.")
                return

        except Exception as e:
            print(f"⚠️  Warning: Failed to read existing results: {e}")
            print("   Continuing without resume...")
            successfully_processed_paths.clear()

    # 文件写入模式：resume 使��追加模式，否则使用覆盖模式
    file_mode = "a" if resume else "w"
    if file_mode == "a":
        print(f"📝 Appending to existing file: {DISTILL_V2_OUTPUT}\n")

    total_tokens = 0
    total_processed = 0
    total_errors = 0
    total_function_matches = 0
    total_functions = 0
    consecutive_failed_batches = 0

    with open(DISTILL_V2_OUTPUT, file_mode, encoding="utf-8") as f:
        num_batches = (len(paths) + batch_size - 1) // batch_size

        for batch_idx, start in enumerate(tqdm(range(0, len(paths), batch_size),
                                               total=num_batches,
                                               desc="Processing paths",
                                               unit="batch"), start=1):
            batch = paths[start: start + batch_size]
            print(f"\n[Batch {batch_idx}/{num_batches}] Processing paths {start + 1}-{start + len(batch)}...")

            batch_errors = 0
            batch_tokens = 0

            # 准备 batch tasks（并发执行）
            tasks = []
            task_path_info = []  # 记录每个 task 对应的 path_info，用于错误报告

            for path_data in batch:
                path_info = path_data.get('path_info', {})

                # 提取 tool_schemas
                tool_schemas = extract_tool_schemas_for_path(path_data, all_tool_schemas)

                if not tool_schemas:
                    print(f"  Path {path_info.get('node_idx', '?')}-{path_info.get('path_idx', '?')}: Warning: No tool schemas found")
                    batch_errors += 1
                    total_errors += 1
                    continue

                # 创建 task
                tasks.append(distill_path(path_data, tool_schemas))
                task_path_info.append(path_info)

            # 并发执行所有 tasks
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)

                # 处理结果
                for result, path_info in zip(results, task_path_info):
                    if isinstance(result, Exception):
                        print(f"  Path {path_info.get('node_idx', '?')}-{path_info.get('path_idx', '?')}: [ERROR] {result}")
                        import traceback
                        traceback.print_exc()
                        batch_errors += 1
                        total_errors += 1
                        continue

                    # 写入成功结果
                    f.write(json.dumps(result, ensure_ascii=False) + "\n")
                    f.flush()

                    # 统计
                    total_processed += 1
                    token_usage = result.get('token_usage', {})
                    batch_tokens += token_usage.get('total_tokens', 0)

                    # 统计函数匹配率
                    distilled_turns = result.get('distilled_turns', [])
                    for turn in distilled_turns:
                        gt_funcs = set(call['function'] for call in turn.get('ground_truth_tool_calls', []))
                        gen_funcs = set(turn.get('generated_tool_calls', []))
                        total_function_matches += len(gt_funcs & gen_funcs)
                        total_functions += len(gt_funcs)

            total_tokens += batch_tokens

            # 计算当前 batch 的统计
            batch_success = len(batch) - batch_errors
            print(f"[Batch {batch_idx}] Success: {batch_success}/{len(batch)}, "
                  f"batch_tokens={batch_tokens}, overall_tokens={total_tokens}")

            # 早停检查：如果当前 batch 全部失败
            if batch_errors == len(batch):
                consecutive_failed_batches += 1
                print(
                    f"[Batch {batch_idx}] ❌ ALL {len(batch)} paths FAILED! "
                    f"(consecutive failed batches: {consecutive_failed_batches}/{early_stop_batches})"
                )

                # 如果连续失败的 batch 数量达到阈值，停止处理
                if early_stop_batches > 0 and consecutive_failed_batches >= early_stop_batches:
                    print("\n" + "=" * 80)
                    print("🛑 EARLY STOPPING TRIGGERED")
                    print("=" * 80)
                    print(f"Consecutive failed batches: {consecutive_failed_batches}")
                    print(f"Stopping to prevent further failures...")
                    print("=" * 80)
                    break
            else:
                # 只要有一个成功，就重置连续失败计数
                consecutive_failed_batches = 0

    # 计算整体函数匹配率
    overall_match_rate = total_function_matches / total_functions if total_functions > 0 else 0.0

    print("\n" + "=" * 80)
    print("DISTILLATION V2 SUMMARY")
    print("=" * 80)
    print(f"Total paths: {len(paths)}")
    print(f"Processed: {total_processed}")
    print(f"Failed: {total_errors}")
    print(f"Success rate: {total_processed / len(paths) * 100:.1f}%" if len(paths) > 0 else "N/A")
    print(f"Total tokens used: {total_tokens}")
    print(f"Function match rate: {overall_match_rate:.2%} ({total_function_matches}/{total_functions})")
    print("=" * 80)
    print(f"\nResults saved to: {DISTILL_V2_OUTPUT}")


def main() -> None:
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Run positive distillation V2")
    parser.add_argument('--max-paths', type=int, default=None,
                        help='Maximum number of paths to process (for testing)')
    parser.add_argument('--batch-size', type=int, default=1,
                        help='Batch size for processing')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from previous run (skip already processed paths)')
    parser.add_argument('--early-stop', type=int, default=3,
                        help='Stop after N consecutive batches with all failures (0 to disable, default: 3)')
    parser.add_argument('--test', action='store_true',
                        help='Test mode: process only 2 paths')

    args = parser.parse_args()

    if args.test:
        print("🧪 Running in TEST mode (2 paths only)...")
        args.max_paths = 2

    asyncio.run(run_distillation_v2(
        max_paths=args.max_paths,
        batch_size=args.batch_size,
        resume=args.resume,
        early_stop_batches=args.early_stop
    ))


if __name__ == "__main__":
    main()
