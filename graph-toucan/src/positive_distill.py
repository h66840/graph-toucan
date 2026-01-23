"""
正向蒸馏脚本：验证 backward_to_query 生成的 user query 质量

流程：
1. 读取 backward_to_query 生成的结果（final_query + tool_schema + fc_reference）
2. 将 final_query 和 tool_schema 给大模型，让其正向 rollout（多步执行）
3. 对比生成的 fc_reference 和原始的 fc_reference，计算准确率

评估指标：
- 函数调用准确率（函数名匹配）
- 参数准确率（参数键和值匹配）
- Step 顺序准确率
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

# 导入 backward_to_query 中的函数
sys.path.insert(0, os.path.dirname(__file__))
from backward_to_query import execute_function_call


# 路径配置
ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
GRAPH_DIR = os.path.join(ROOT_DIR, "graph")
FSP_DIR = "/data/lhy/datasets/graph-Toucan/fsp_path"
DISTILL_DIR = "/data/lhy/datasets/graph-Toucan/distill"
BACKWARD_QUERIES_PATH = os.path.join(FSP_DIR, "fsp_v1.json")
OUTPUT_DISTILL_RESULTS_PATH = os.path.join(DISTILL_DIR, "distill_v1.jsonl")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")


def load_config(config_path: str = CONFIG_PATH) -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


# 加载配置
config = load_config()

# 初始化 AsyncOpenAI 客户端
# 支持两种配置方式：
# 1. 通过环境变量：api_key_env: "DASHSCOPE_API_KEY"
# 2. 直接配置：api_key: "EMPTY"
api_key_env = config["api"].get("api_key_env")
if api_key_env:
    # 如果配置了 api_key_env，从环境变量读取
    api_key = os.getenv(api_key_env, "EMPTY")
else:
    # 否则直接从配置读取
    api_key = config["api"].get("api_key", "EMPTY")
base_url = config["api"]["base_url"]

async_client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)

# 模型配置
DEFAULT_MODEL = config["model"]["default"]


def build_tool_schema_prompt(nodes_tool_schema: Dict[str, Dict[str, Any]]) -> str:
    """
    构建工具 schema 的 prompt 描述

    Args:
        nodes_tool_schema: 工具 schema 字典

    Returns:
        格式化的工具文档字符串
    """
    tool_docs = []
    for tool_name, tool_meta in nodes_tool_schema.items():
        tool_schema = tool_meta.get("tool_schema", {}).get("function", {})
        description = tool_schema.get("description", "")
        params = tool_schema.get("parameters", {})

        # 构建参数文档
        param_lines = []
        if params and isinstance(params, dict):
            properties = params.get("properties", {})
            required = set(params.get("required", []))

            for param_name, param_info in properties.items():
                if not isinstance(param_info, dict):
                    continue
                param_type = param_info.get("type", "unknown")
                param_desc = param_info.get("description", "")
                req_flag = "required" if param_name in required else "optional"
                param_lines.append(f"    - {param_name} ({param_type}, {req_flag}): {param_desc}")

        param_block = "\n".join(param_lines) if param_lines else "    (no parameters)"

        tool_doc = f"""- {tool_name}:
  Description: {description}
  Parameters:
{param_block}
"""
        tool_docs.append(tool_doc)

    return "\n".join(tool_docs)


def parse_tool_calls_from_content(content: str) -> List[Dict[str, Any]]:
    """
    从 LLM 输出中解析 tool calls

    格式:
    tool_call1: function_name with parameters: {...}
    tool_call2: function_name with parameters: {...}

    Args:
        content: LLM 的输出内容

    Returns:
        tool_calls 列表
    """
    tool_calls = []
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 解析 tool_call 部分
        if line.startswith("tool_call"):
            try:
                # 提取函数名和参数
                if "with parameters:" in line:
                    parts = line.split("with parameters:")
                    func_part = parts[0].strip()
                    params_part = parts[1].strip()

                    # 提取函数名 (tool_call1: function_name)
                    func_name = func_part.split(":")[-1].strip()

                    # 解析 JSON 参数
                    try:
                        params = json.loads(params_part)
                    except json.JSONDecodeError:
                        # 如果 JSON 解析失败，使用空参数
                        params = {}

                    tool_calls.append({
                        "function": func_name,
                        "parameters": params
                    })
            except Exception as e:
                print(f"Warning: Failed to parse tool_call line: {line}, error: {e}")

    return tool_calls


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


async def forward_rollout_step(
    user_query: str,
    tool_schemas: Dict[str, Dict[str, Any]],
    conversation_history: List[Dict[str, str]],
    max_steps: int = 10,
    model: str = None
) -> Dict[str, Any]:
    """
    正向 rollout：单步执行，根据 user query 和对话历史生成下一步函数调用

    这是一个 single turn multi-step 的过程：
    1. LLM 根据 user query 和历史生成当前 step 的 tool calls
    2. 执行这些 tool calls，获取 outputs
    3. 将 tool outputs 加入 message history
    4. 继续下一个 step，直到 LLM 认为任务完成或达到最大步数

    Args:
        user_query: 用户查询
        tool_schemas: 可用工具的 schema
        conversation_history: 对话历史（初始为空）
        max_steps: 最大步数
        model: 使用的模型名称（默认使用配置文件中的 default 模型）

    Returns:
        包含所有 steps 和 token 使用信息的字典
    """
    if model is None:
        model = DEFAULT_MODEL

    # 构建 OpenAI API 格式的 tools（包含名称映射）
    tools, name_mapping, short_tool_schemas = build_tools_for_api(tool_schemas)

    all_steps = []
    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }

    # 初始化对话历史（如果为空）
    if not conversation_history:
        conversation_history = [
            {
                "role": "system",
                "content": (
                    "You are a multi-step function-calling agent. "
                    "When you try to solve user's query, you should provide your thinking process and proper function call,you need give your thinking process to user,And give the proper function call "
                    "Your thinking process should explain:\n"
                    "What you understand about the current task\n"
                    "Why you are choosing to call specific tools\n"
                    "What information you expect to get from the tool calls\n"
                    "How you plan to use the results\n\n"
                    "Then provide the appropriate function calls. "
                    
                    "Your thinking process should be written as a coherent narrative paragraph (not bullet points), explaining what you understand about the current task, "
                    "Think step by step and generate function calls to accomplish the user's task. "
                    "After each step, you will receive the tool outputs. "
                    "Continue until the task is complete."
                    "always use english language"
                )
            },
            {
                "role": "user",
                "content": user_query
            }
        ]

    # 多步执行循环
    for step_num in range(1, max_steps + 1):
        try:
            # 调用 LLM 生成当前步骤的函数调用（使用标准 function calling API）
            completion = await async_client.chat.completions.create(
                model=model,
                messages=conversation_history,
                tools=tools,  # 传递标准的 tools
                stream=False,
                temperature=1,
                max_completion_tokens=1024,
            )

            message = completion.choices[0].message

            # 累计 token 使用
            usage = completion.usage
            if usage:
                total_token_usage["prompt_tokens"] += usage.prompt_tokens
                total_token_usage["completion_tokens"] += usage.completion_tokens
                total_token_usage["total_tokens"] += usage.total_tokens

            # 检查是否有 tool_calls
            if not message.tool_calls:
                # 没有 tool calls，任务完成，记录最后的总结
                final_step = {
                    "step_num": step_num,
                    "summary": message.content or "",
                    "tool_calls": [],
                    "tool_outputs": []
                }
                all_steps.append(final_step)

                # 将最后的 assistant 消息添加到对话历史
                conversation_history.append({
                    "role": "assistant",
                    "content": message.content or ""
                })

                print(f"  Task completed at step {step_num} (no more tool calls)")
                break

            # 提取 tool_calls
            api_tool_calls = message.tool_calls

            # 记录当前步骤
            tool_calls_for_record = []
            for tc in api_tool_calls:
                try:
                    params = json.loads(tc.function.arguments) if tc.function.arguments else {}
                except json.JSONDecodeError:
                    params = {}

                tool_calls_for_record.append({
                    "function": tc.function.name,
                    "parameters": params
                })

            current_step = {
                "step_num": step_num,
                "tool_calls": tool_calls_for_record,
                "tool_outputs": []
            }

            # 执行函数调用
            step_outputs = []
            tool_messages = []  # 用于构建 tool role 消息

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

                    # 提取实际的 result
                    if isinstance(output_result, dict):
                        # 如果有 "result" 字段，提取它；否则使用整个 dict
                        if "result" in output_result:
                            output = output_result["result"]
                        else:
                            # 没有 "result" 字段，使用整个 dict 但移除 token_usage
                            output = {k: v for k, v in output_result.items() if k != "token_usage"}

                        # 累加 execute_function_call 的 token 使用
                        tq = output_result.get("token_usage", {})
                        total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
                        total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
                        total_token_usage["total_tokens"] += tq.get("total_tokens", 0)
                    else:
                        output = output_result

                    step_outputs.append({
                        "function": short_func_name,  # 使用缩短的名称
                        "output": output
                    })

                    # 构建 tool message
                    tool_output_str = json.dumps(output, ensure_ascii=False) if isinstance(output, (dict, list)) else str(output)
                    tool_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": tool_output_str
                    })

                except Exception as e:
                    print(f"  Error executing {short_func_name}: {e}")
                    step_outputs.append({
                        "function": short_func_name,  # 使用缩短的名称
                        "error": str(e)
                    })

                    # 即使出错也要添加 tool message
                    tool_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": json.dumps({"error": str(e)}, ensure_ascii=False)
                    })

            current_step["tool_outputs"] = step_outputs
            all_steps.append(current_step)

            # 将 assistant message（带 tool_calls）添加到对话历史
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
                    for tc in api_tool_calls
                ]
            })

            # 添加所有 tool messages
            conversation_history.extend(tool_messages)

        except Exception as e:
            print(f"  Error at step {step_num}: {e}")
            return {
                "error": f"Error at step {step_num}: {e}",
                "steps": all_steps,
                "token_usage": total_token_usage
            }

    return {
        "steps": all_steps,
        "token_usage": total_token_usage,
        "total_steps": len(all_steps),
        "conversation_history": conversation_history,
        "short_tool_schemas": short_tool_schemas,
        "tool_name_mapping": name_mapping
    }


def compare_function_calls_v1(
    ground_truth: List[Dict[str, Any]],
    generated: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    对比 ground truth 和 generated 的函数调用（多轮对话版本，按 turn 比较）

    这个版本专门用于多轮对话：
    - ground_truth 的每个元素代表一个 turn 的 tool calls
    - generated 中的 steps 需要按 turn_idx 分组后再比较
    - 只比较同一个 turn 内的 function names

    Args:
        ground_truth: 原始的 fc_results（每个元素代表一个 turn，包含 tool_calls）
        generated: 正向生成的 steps（每个 step 包含 turn_idx 和 tool_calls）

    Returns:
        评估指标字典，包含：
        - total_gt_turns: ground truth 总轮数
        - total_gen_turns: generated 总轮数（从 steps 中提取的唯一 turn_idx 数量）
        - turn_matches: 匹配的 turn 数量
        - turn_details: 每个 turn 的详细对比信息
        - overall_accuracy: turn 匹配准确率
        - exact_match: 是否所有 turn 都匹配
    """
    metrics = {
        "total_gt_turns": len(ground_truth),
        "total_gen_turns": 0,
        "turn_matches": 0,
        "turn_details": [],
    }

    # 将 generated steps 按 turn_idx 分组
    gen_by_turn = {}
    for step in generated:
        turn_idx = step.get("turn_idx")
        if turn_idx is not None:
            if turn_idx not in gen_by_turn:
                gen_by_turn[turn_idx] = []
            gen_by_turn[turn_idx].append(step)

    metrics["total_gen_turns"] = len(gen_by_turn)

    # 逐 turn 对比
    max_turns = max(len(ground_truth), len(gen_by_turn) if gen_by_turn else 0)

    for turn_idx in range(1, max_turns + 1):
        turn_detail = {
            "turn_idx": turn_idx,
            "gt_functions": [],
            "gen_functions": [],
            "match": False,
            "missing_functions": [],  # 在 GT 中有但 generated 中缺失
            "extra_functions": [],     # generated 中有但 GT 中没有
        }

        # 提取 ground truth 该 turn 的所有函数名
        if turn_idx - 1 < len(ground_truth):
            gt_turn = ground_truth[turn_idx - 1]
            tool_calls = gt_turn.get("tool_calls", [])
            for tc in tool_calls:
                if isinstance(tc, dict):
                    func_name = tc.get("function", "")
                    if func_name:
                        turn_detail["gt_functions"].append(func_name)

        # 提取 generated 该 turn 的所有函数名（合并该 turn 所有 steps 的函数调用）
        if turn_idx in gen_by_turn:
            for step in gen_by_turn[turn_idx]:
                tool_calls = step.get("tool_calls", [])
                for tc in tool_calls:
                    if isinstance(tc, dict):
                        func_name = tc.get("function", "")
                        if func_name:
                            turn_detail["gen_functions"].append(func_name)

        # 转换为集合进行比较（去重）
        gt_funcs_set = set(turn_detail["gt_functions"])
        gen_funcs_set = set(turn_detail["gen_functions"])

        # 检查是否完全匹配
        if gt_funcs_set == gen_funcs_set:
            turn_detail["match"] = True
            metrics["turn_matches"] += 1
        else:
            # 找出缺失和多余的函数
            turn_detail["missing_functions"] = list(gt_funcs_set - gen_funcs_set)
            turn_detail["extra_functions"] = list(gen_funcs_set - gt_funcs_set)

        metrics["turn_details"].append(turn_detail)

    # 计算总体准确率
    if metrics["total_gt_turns"] > 0:
        metrics["overall_accuracy"] = metrics["turn_matches"] / metrics["total_gt_turns"]
    else:
        metrics["overall_accuracy"] = 0.0

    # 检查是否完全匹配（所有 turns 都匹配）
    metrics["exact_match"] = (
        metrics["total_gt_turns"] == metrics["total_gen_turns"] and
        metrics["turn_matches"] == metrics["total_gt_turns"]
    )

    return metrics


def compare_function_calls(
    ground_truth: List[Dict[str, Any]],
    generated: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    对比 ground truth 和 generated 的函数调用（只比较函数名）

    Args:
        ground_truth: 原始的 fc_results（每个元素包含 tool_calls）
        generated: 正向生成的 steps（每个元素包含 tool_calls）

    Returns:
        评估指标字典，包含：
        - total_gt_steps: ground truth 总步数
        - total_gen_steps: generated 总步数
        - step_matches: 每个 step 的函数集合完全匹配的数量
        - step_details: 每个 step 的详细对比信息
        - overall_accuracy: 总体步骤匹配准确率
    """
    metrics = {
        "total_gt_steps": len(ground_truth),
        "total_gen_steps": len(generated),
        "step_matches": 0,
        "step_details": [],
    }

    # 逐步对比
    max_steps = max(len(ground_truth), len(generated))

    for step_idx in range(max_steps):
        step_detail = {
            "step_num": step_idx + 1,
            "gt_functions": [],
            "gen_functions": [],
            "match": False,
            "missing_functions": [],  # 在 GT 中有但 generated 中缺失
            "extra_functions": [],     # generated 中有但 GT 中没有
        }

        # 提取 ground truth 的函数名
        if step_idx < len(ground_truth):
            gt_step = ground_truth[step_idx]
            tool_calls = gt_step.get("tool_calls", [])
            for tc in tool_calls:
                if isinstance(tc, dict):
                    func_name = tc.get("function", "")
                    if func_name:
                        step_detail["gt_functions"].append(func_name)

        # 提取 generated 的函数名
        if step_idx < len(generated):
            gen_step = generated[step_idx]
            tool_calls = gen_step.get("tool_calls", [])
            for tc in tool_calls:
                if isinstance(tc, dict):
                    func_name = tc.get("function", "")
                    if func_name:
                        step_detail["gen_functions"].append(func_name)

        # 转换为集合进行比较
        gt_funcs_set = set(step_detail["gt_functions"])
        gen_funcs_set = set(step_detail["gen_functions"])

        # 检查是否完全匹配
        if gt_funcs_set == gen_funcs_set:
            step_detail["match"] = True
            metrics["step_matches"] += 1
        else:
            # 找出缺失和多余的函数
            step_detail["missing_functions"] = list(gt_funcs_set - gen_funcs_set)
            step_detail["extra_functions"] = list(gen_funcs_set - gt_funcs_set)

        metrics["step_details"].append(step_detail)

    # 计算总体准确率
    if metrics["total_gt_steps"] > 0:
        metrics["overall_accuracy"] = metrics["step_matches"] / metrics["total_gt_steps"]
    else:
        metrics["overall_accuracy"] = 0.0

    # 检查是否完全匹配（所有步骤都匹配）
    metrics["exact_match"] = (
        metrics["total_gt_steps"] == metrics["total_gen_steps"] and
        metrics["step_matches"] == metrics["total_gt_steps"]
    )

    return metrics


async def process_single_record_v1(
    record: Dict[str, Any]
) -> Dict[str, Any]:
    """
    处理单条记录：使用 atomic queries 进行多轮对话的正向 rollout 并对比

    这是一个 multi-turn multi-step 的流程：
    - 每个 atomic_query 是一轮对话（turn）
    - 每轮对话内部是 multi-step 的（single turn multi-step）
    - conversation_history 在所有轮次之间持续累加

    Args:
        record: backward_to_query 生成的记录

    Returns:
        包含对比结果的字典
    """
    # 如果记录本身就有错误，直接返回
    if "error" in record:
        return {
            "path_info": record.get("path_info", {}),
            "skipped": True,
            "reason": "original_error",
            "original_error": record["error"]
        }

    atomic_queries = record.get("atomic_queries", [])
    nodes_tool_schema = record.get("nodes_tool_schema", {})
    ground_truth_fc = record.get("fc_results", [])

    if not atomic_queries or not nodes_tool_schema:
        return {
            "path_info": record.get("path_info", {}),
            "skipped": True,
            "reason": "missing_data"
        }

    # 构建 OpenAI API 格式的 tools（包含名称映射）
    tools, name_mapping, short_tool_schemas = build_tools_for_api(nodes_tool_schema)

    all_steps = []
    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }

    # 初始化对话历史（在所有 turns 之间共享）
    conversation_history = [
        {
            "role": "system",
            "content": (
                "You are a multi-turn multi-step function-calling agent. "
                "Before each function call, briefly explain your reasoning: "
                "what you plan to do, which tool to use and why, and how you determine the parameter values. "
                "Express your thinking in a natural, flowing way (1-3 sentences total, not bullet points). "
                "After each step, you will receive the tool outputs and continue until the task is complete. "
                "Always use English."
            )
        }
    ]

    # 对每个 atomic query 进行一轮对话
    for turn_idx, atomic_query in enumerate(atomic_queries, start=1):
        print(f"  Processing turn {turn_idx}/{len(atomic_queries)}: {atomic_query[:50]}...")

        # 添加当前轮次的 user message
        conversation_history.append({
            "role": "user",
            "content": atomic_query
        })

        # 多步执行循环（当前 turn）
        turn_completed = False
        max_steps_per_turn = 10

        for step_num in range(1, max_steps_per_turn + 1):
            try:
                # 调用 LLM 生成当前步骤的函数调用
                completion = await async_client.chat.completions.create(
                    model=DEFAULT_MODEL,
                    messages=conversation_history,
                    tools=tools,
                    stream=False,
                    temperature=1,
                    max_completion_tokens=1024,
                )

                message = completion.choices[0].message

                # 累计 token 使用
                usage = completion.usage
                if usage:
                    total_token_usage["prompt_tokens"] += usage.prompt_tokens
                    total_token_usage["completion_tokens"] += usage.completion_tokens
                    total_token_usage["total_tokens"] += usage.total_tokens

                # 检查是否有 tool_calls
                if not message.tool_calls:
                    # 没有 tool calls，当前 turn 完成
                    final_step = {
                        "turn_idx": turn_idx,
                        "step_num": len(all_steps) + 1,
                        "summary": message.content or "",
                        "tool_calls": [],
                        "tool_outputs": []
                    }
                    all_steps.append(final_step)

                    # 将最后的 assistant 消息添加到对话历史
                    conversation_history.append({
                        "role": "assistant",
                        "content": message.content or ""
                    })

                    print(f"    Turn {turn_idx} completed at step {step_num}")
                    turn_completed = True
                    break

                # 提取 tool_calls
                api_tool_calls = message.tool_calls

                # 记录当前步骤
                tool_calls_for_record = []
                for tc in api_tool_calls:
                    try:
                        params = json.loads(tc.function.arguments) if tc.function.arguments else {}
                    except json.JSONDecodeError:
                        params = {}

                    tool_calls_for_record.append({
                        "function": tc.function.name,
                        "parameters": params
                    })

                current_step = {
                    "turn_idx": turn_idx,
                    "step_num": len(all_steps) + 1,
                    "tool_calls": tool_calls_for_record,
                    "tool_outputs": []
                }

                # 执行函数调用
                step_outputs = []
                tool_messages = []

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

                        # 提取实际的 result
                        if isinstance(output_result, dict):
                            # 如果有 "result" 字段，提取它；否则使用整个 dict
                            if "result" in output_result:
                                output = output_result["result"]
                            else:
                                # 没有 "result" 字段，使用整个 dict 但移除 token_usage
                                output = {k: v for k, v in output_result.items() if k != "token_usage"}

                            # 累加 execute_function_call 的 token 使用
                            tq = output_result.get("token_usage", {})
                            total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
                            total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
                            total_token_usage["total_tokens"] += tq.get("total_tokens", 0)
                        else:
                            output = output_result

                        step_outputs.append({
                            "function": short_func_name,  # 使用缩短的名称
                            "output": output
                        })

                        # 构建 tool message
                        tool_output_str = json.dumps(output, ensure_ascii=False) if isinstance(output, (dict, list)) else str(output)
                        tool_messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "content": tool_output_str
                        })

                    except Exception as e:
                        # 重新抛出异常，添加上下文信息
                        raise RuntimeError(
                            f"Error executing function {short_func_name} with parameters {parameters} at turn {turn_idx}, step {step_num}: {e}"
                        ) from e

                current_step["tool_outputs"] = step_outputs
                all_steps.append(current_step)

                # 将 assistant message（带 tool_calls）添加到对话历史
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
                        for tc in api_tool_calls
                    ]
                })

                # 添加所有 tool messages
                conversation_history.extend(tool_messages)

            except Exception as e:
                # 重新抛出异常，添加上下文信息
                raise RuntimeError(
                    f"Error at turn {turn_idx}, step {step_num}: {e}"
                ) from e

        if not turn_completed:
            print(f"    Turn {turn_idx} reached max steps ({max_steps_per_turn})")

    # 对比结果（使用 v1 版本的比较函数，按 turn 比较）
    metrics = compare_function_calls_v1(ground_truth_fc, all_steps)

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
        "conversation": conversation_history,
        "tools": tools_list,
        "tool_name_mapping": name_mapping
    }


async def process_single_record(
    record: Dict[str, Any]
) -> Dict[str, Any]:
    """
    处理单条记录：正向 rollout 并对比

    Args:
        record: backward_to_query 生成的记录

    Returns:
        包含对比结果的字典
    """
    # 如果记录本身就有错误，直接返回
    if "error" in record:
        return {
            "path_info": record.get("path_info", {}),
            "skipped": True,
            "reason": "original_error",
            "original_error": record["error"]
        }

    final_query = record.get("final_query", "")
    nodes_tool_schema = record.get("nodes_tool_schema", {})
    ground_truth_fc = record.get("fc_results", [])

    if not final_query or not nodes_tool_schema:
        return {
            "path_info": record.get("path_info", {}),
            "skipped": True,
            "reason": "missing_data"
        }

    # 正向 rollout（多步执行）
    rollout_result = await forward_rollout_step(
        user_query=final_query,
        tool_schemas=nodes_tool_schema,
        conversation_history=[],
        max_steps=10
    )

    if "error" in rollout_result:
        return {
            "path_info": record.get("path_info", {}),
            "final_query": final_query,
            "rollout_error": rollout_result.get("error"),
            "token_usage": rollout_result.get("token_usage", {}),
        }

    # 对比结果
    generated_steps = rollout_result.get("steps", [])
    metrics = compare_function_calls(ground_truth_fc, generated_steps)
    conversation_history = rollout_result["conversation_history"]

    # 获取缩短名称后的 tool schemas
    short_tool_schemas = rollout_result.get("short_tool_schemas", {})
    name_mapping = rollout_result.get("tool_name_mapping", {})

    # 构建 tools 列表：使用缩短名称的 schemas
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
        "conversation": conversation_history,
        "tools": tools_list,
        "tool_name_mapping": name_mapping
    }


async def run_distillation(
    max_records: Optional[int] = None,
    batch_size: int = 5,
    use_atomic_queries: bool = False,
    resume: bool = False,
    early_stop_batches: int = 3,
) -> None:
    """
    运行正向蒸馏验证

    Args:
        max_records: 最多处理的记录数（None 表示全部）
        batch_size: 批处理大小
        use_atomic_queries: 是否使用 atomic queries 进行多轮对话
                           False: 使用 final_query 的单轮多步对话（process_single_record）
                           True: 使用 atomic_queries 的多轮多步对话（process_single_record_v1）
        resume: 是否启用断点续传（跳过已成功处理的记录）
        early_stop_batches: 连续多少个 batch 全部失败后停止（0 表示不启用早停）
    """
    print(f"Loading backward queries from {BACKWARD_QUERIES_PATH}...")

    records = []
    with open(BACKWARD_QUERIES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))
            if max_records and len(records) >= max_records:
                break

    print(f"Loaded {len(records)} records.")

    # 根据版本选择输出路径
    if use_atomic_queries:
        output_path = OUTPUT_DISTILL_RESULTS_PATH.replace(".jsonl", "_multi_turn.jsonl")
        print(f"Mode: Multi-turn (using atomic queries)")
    else:
        output_path = OUTPUT_DISTILL_RESULTS_PATH
        print(f"Mode: Single-turn (using final query)")

    print(f"Output -> {output_path}\n")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 断点续传：读取已成功处理的记录
    successfully_processed_ids = set()

    if resume and os.path.exists(output_path):
        print(f"\n🔄 Resume mode enabled, reading existing results from {output_path}...")
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        # 只统计成功处理且有 metrics 的记录
                        if not record.get("skipped") and not record.get("error") and "metrics" in record:
                            path_info = record.get("path_info", {})
                            # 使用 start_index 和 walk_id 作为唯一标识
                            start_idx = path_info.get("start_index")
                            walk_id = path_info.get("walk_id")
                            if start_idx is not None and walk_id is not None:
                                record_id = (start_idx, walk_id)
                                successfully_processed_ids.add(record_id)
                    except json.JSONDecodeError:
                        continue

            print(f"   Found {len(successfully_processed_ids)} successfully processed records")

            # 过滤掉成功处理的记录
            original_count = len(records)
            records = [
                r for r in records
                if not (
                    r.get("path_info", {}).get("start_index") is not None and
                    r.get("path_info", {}).get("walk_id") is not None and
                    (r.get("path_info", {}).get("start_index"), r.get("path_info", {}).get("walk_id")) in successfully_processed_ids
                )
            ]
            skipped_count = original_count - len(records)

            print(f"   Skipping {skipped_count} successfully processed records")
            print(f"   Remaining {len(records)} records to process")

            if len(records) == 0:
                print("\n✅ All records already processed! Nothing to do.")
                return

        except Exception as e:
            print(f"⚠️  Warning: Failed to read existing results: {e}")
            print("   Continuing without resume...")
            successfully_processed_ids.clear()

    # 文件写入模式：resume 使用追加模式，否则使用覆盖模式
    file_mode = "a" if resume else "w"
    if file_mode == "a":
        print(f"📝 Appending to existing file: {output_path}\n")

    total_tokens = 0
    total_exact_matches = 0
    total_processed = 0
    total_errors = 0
    consecutive_failed_batches = 0  # 连续失败的 batch 计数
    total_steps = 0  # 累积总步数
    total_turns = 0  # 累积总轮次数

    # 选择使用哪个处理函数
    process_func = process_single_record_v1 if use_atomic_queries else process_single_record

    with open(output_path, file_mode, encoding="utf-8") as f:
        num_batches = (len(records) + batch_size - 1) // batch_size

        for batch_idx, start in enumerate(tqdm(range(0, len(records), batch_size),
                                               total=num_batches,
                                               desc="Processing records",
                                               unit="batch"), start=1):
            batch = records[start: start + batch_size]
            print(f"\n[Batch {batch_idx}/{num_batches}] Processing records {start + 1}-{start + len(batch)}...")

            batch_errors = 0  # 当前 batch 的错误数
            batch_tokens = 0
            batch_steps_per_turn = []  # 当前 batch 的每个turn平均步数列表

            tasks = [process_func(record) for record in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    print(f"[ERROR] Exception: {result}")
                    batch_errors += 1
                    total_errors += 1
                    # 失败的记录不写入文件，下次 resume 会重新处理
                    continue

                # 检查是否是处理失败（有 error 或 rollout_error）
                if result.get("error") or result.get("rollout_error"):
                    batch_errors += 1
                    total_errors += 1
                    # 失败的记录不写入文件
                    continue

                # 只写入成功的记录
                f.write(json.dumps(result, ensure_ascii=False) + "\n")
                f.flush()

                # 统计
                if not result.get("skipped") and "metrics" in result:
                    total_processed += 1
                    if result["metrics"].get("exact_match"):
                        total_exact_matches += 1

                    # 累积总步数和总轮次数
                    generated_steps = result.get("generated_steps", 0)
                    record_turns = result.get("total_turns", 1)  # 单轮模式默认为1
                    total_steps += generated_steps
                    total_turns += record_turns

                    # 计算当前记录的平均每个turn的步数
                    steps_per_turn = generated_steps / record_turns if record_turns > 0 else 0
                    batch_steps_per_turn.append(steps_per_turn)

                token_usage = result.get("token_usage", {})
                batch_tokens += token_usage.get("total_tokens", 0)

            total_tokens += batch_tokens

            # 计算当前 batch 的平均每个turn的步数
            avg_steps_per_turn = sum(batch_steps_per_turn) / len(batch_steps_per_turn) if batch_steps_per_turn else 0

            # 早停检查：如果当前 batch 全部失败
            if batch_errors == len(batch):
                consecutive_failed_batches += 1
                print(
                    f"[Batch {batch_idx}] ❌ ALL {len(batch)} records FAILED! "
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
                # 如果当前 batch 有成功的，重置连续失败计数
                consecutive_failed_batches = 0
                print(
                    f"[Batch {batch_idx}] batch_tokens={batch_tokens}, "
                    f"overall_tokens={total_tokens}, "
                    f"batch_errors={batch_errors}/{len(batch)}, "
                    f"avg_steps_per_turn={avg_steps_per_turn:.2f}"
                )

    print("\n" + "=" * 80)
    print(f"DISTILLATION SUMMARY ({'Multi-turn' if use_atomic_queries else 'Single-turn'})")
    print("=" * 80)
    print(f"Total records: {len(records)}")
    print(f"Processed: {total_processed}")
    print(f"Failed: {total_errors}")
    print(f"Exact matches: {total_exact_matches}")
    if total_processed > 0:
        print(f"Exact match rate: {total_exact_matches / total_processed * 100:.2f}%")
    print(f"Total tokens used: {total_tokens}")
    if total_turns > 0:
        print(f"Average steps per turn: {total_steps / total_turns:.2f}")
    print("=" * 80)
    print(f"\nResults saved to: {output_path}")


def main() -> None:
    """
    命令行入口
    """
    import argparse

    parser = argparse.ArgumentParser(description="Run positive distillation validation")
    parser.add_argument('--max-records', type=int, default=None,
                        help='Maximum number of records to process (for testing)')
    parser.add_argument('--batch-size', type=int, default=5,
                        help='Batch size for parallel processing')
    parser.add_argument('--multi-turn', '-m', action='store_true',
                        help='Use multi-turn mode (atomic queries)')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from previous run (skip already processed records)')
    parser.add_argument('--early-stop', type=int, default=1,
                        help='Stop after N consecutive batches with all failures (0 to disable)')
    parser.add_argument('--test', action='store_true',
                        help='Test mode: process only 5 records')

    args = parser.parse_args()

    if args.test:
        print("🧪 Running in TEST mode (5 records only)...")
        args.max_records = 5

    use_atomic_queries = args.multi_turn

    if use_atomic_queries:
        print("Running multi-turn version (using atomic queries)...")
    else:
        print("Running single-turn version (using final query)...")

    asyncio.run(run_distillation(
        max_records=args.max_records,
        batch_size=args.batch_size,
        use_atomic_queries=use_atomic_queries,
        resume=args.resume,
        early_stop_batches=args.early_stop,
    ))


if __name__ == "__main__":
    main()
