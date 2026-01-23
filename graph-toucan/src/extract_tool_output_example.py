"""
基于一个 tool set，找到 datasets 里每个 tool 被调用的三条数据，
保留 tool call 对应的最近的 user query 和 assistant message 和对应的 tool response。

新流程：
1. 读取 tool_with_server.json 获取所有 tool
2. 读取 mcp_status_judgment_results.json 获取所有 MCP 的状态信息
3. 筛选出所有属于 non-stateful MCP 的 tools（is_stateful == false）
4. 使用 find_tool_examples 函数为这些 tools 找示例
5. 保存到 tool_output.json

对于并行调用，按照顺序匹配：tool call A 和 tool call B，得到 tool response 1 和 tool response 2，
那么 tool call A 对应的是 tool response 1。
"""

import json
import os
import datasets
from typing import Dict, List, Any, Optional
from collections import defaultdict
from tqdm import tqdm


def load_tools_from_tool_with_server(
    tool_with_server_path: str,
    mcp_status_path: str,
) -> tuple[List[str], Dict[str, Any]]:
    """
    从 tool_with_server.json 中加载所有 tools，并根据 mcp_status_judgment_results.json
    筛选出属于 non-stateful MCP 的 tools

    Args:
        tool_with_server_path: tool_with_server.json 文件路径
        mcp_status_path: mcp_status_judgment_results.json 文件路径

    Returns:
        tuple: (non_stateful_tools, statistics)
            - non_stateful_tools: List[str], non-stateful 的 tool 名称列表
            - statistics: Dict, 统计信息
    """
    print(f"Loading tools from {tool_with_server_path}...")
    with open(tool_with_server_path, 'r', encoding='utf-8') as f:
        tools_data = json.load(f)

    print(f"Loading MCP status information from {mcp_status_path}...")
    with open(mcp_status_path, 'r', encoding='utf-8') as f:
        mcp_status_data = json.load(f)

    # 获取 MCP 状态信息字典（key: MCP server name）
    mcp_results = mcp_status_data.get('results', {})

    # 统计信息
    total_tools = 0
    stateful_tools = 0
    non_stateful_tools_list = []
    tools_by_mcp = defaultdict(list)
    unknown_mcp_tools = []

    print("\nProcessing tools and filtering by MCP status...")
    for tool_entry in tqdm(tools_data):
        # 提取 tool 名称
        tool_name = tool_entry.get('function_schema', {}).get('function', {}).get('name', '')
        if not tool_name:
            continue

        total_tools += 1

        # 获取 MCP server 信息
        # tool_with_server.json 中的 mcp_server_info.name 对应 mcp_status 中的 key
        mcp_server_name = tool_entry.get('mcp_server_info', {}).get('name', '')

        if not mcp_server_name:
            # 如果没有 MCP server 信息，跳过
            unknown_mcp_tools.append(tool_name)
            continue

        # 查找该 MCP 的状态信息
        mcp_info = mcp_results.get(mcp_server_name)

        if mcp_info is None:
            # 如果在 mcp_status 中找不到该 MCP，记录但先假设为 non-stateful
            unknown_mcp_tools.append(tool_name)
            non_stateful_tools_list.append(tool_name)
            tools_by_mcp[mcp_server_name].append(tool_name)
        else:
            is_stateful = mcp_info.get('is_stateful', False)

            if is_stateful:
                # 有状态的 MCP，跳过这个 tool
                stateful_tools += 1
            else:
                # 无状态的 MCP，保留这个 tool
                non_stateful_tools_list.append(tool_name)
                tools_by_mcp[mcp_server_name].append(tool_name)

    # 统计信息
    statistics = {
        'total_tools': total_tools,
        'stateful_tools': stateful_tools,
        'non_stateful_tools': len(non_stateful_tools_list),
        'unknown_mcp_tools': len(unknown_mcp_tools),
        'non_stateful_mcps': len(tools_by_mcp),
        'tools_by_mcp': {
            mcp: len(tools) for mcp, tools in tools_by_mcp.items()
        }
    }

    # 打印统计信息
    print("\n" + "=" * 80)
    print("Tool Filtering Summary")
    print("=" * 80)
    print(f"Total tools in tool_with_server.json: {total_tools}")
    print(f"Tools from stateful MCPs (filtered out): {stateful_tools}")
    print(f"Tools from non-stateful MCPs (kept): {len(non_stateful_tools_list)}")
    print(f"Tools with unknown MCP status (kept): {len(unknown_mcp_tools)}")
    print(f"Number of non-stateful MCPs: {len(tools_by_mcp)}")
    print("=" * 80)

    return non_stateful_tools_list, statistics


def parse_tool_call_content(content: str) -> Optional[Dict[str, Any]]:
    """
    解析 tool_call 消息的 content，提取 tool name

    Args:
        content: tool_call 消息的 content 字段

    Returns:
        dict: 包含 name 和 arguments 的字典，如果解析失败返回 None
    """
    try:
        if isinstance(content, str):
            try:
                tool_data = json.loads(content)
            except json.JSONDecodeError:
                import ast
                tool_data = ast.literal_eval(content)
        else:
            tool_data = content

        if isinstance(tool_data, dict):
            return {
                'name': tool_data.get('name', ''),
                'arguments': tool_data.get('arguments', '')
            }
    except Exception as e:
        pass

    return None


def extract_tool_call_context(messages: List[Dict[str, Any]], target_tool_name: str) -> List[Dict[str, Any]]:
    """
    从 messages 中提取指定 tool 的调用上下文

    Args:
        messages: 消息列表
        target_tool_name: str, 目标 tool 名称

    Returns:
        List[Dict]: 包含该 tool 调用上下文的数据列表
        每个元素包含：
        - user_query: str, 最近的 user query
        - assistant_message: str, assistant 消息（包含 tool call 的说明）
        - tool_call: dict, tool call 信息
        - tool_response: str, 对应的 tool response
    """
    results = []
    i = 0

    while i < len(messages):
        msg = messages[i]
        role = msg.get('role', '')

        # 查找 tool_call
        if role == 'tool_call':
            tool_info = parse_tool_call_content(msg.get('content', ''))
            if tool_info and tool_info['name'] == target_tool_name:
                # 找到了目标 tool 的调用
                # 1. 找到这一批连续的 tool_call 的开始位置，并计算当前 tool_call 的索引
                batch_start = i
                tool_call_index = 0
                for j in range(i - 1, -1, -1):
                    if messages[j].get('role') == 'tool_call':
                        batch_start = j
                        tool_call_index += 1
                    else:
                        break

                # 2. 向前查找最近的 user query 和 assistant message
                user_query = None
                assistant_message = None
                for j in range(batch_start - 1, -1, -1):
                    prev_msg = messages[j]
                    prev_role = prev_msg.get('role', '')
                    if prev_role == 'user':
                        user_query = prev_msg.get('content', '')
                        # 检查 user 和 batch_start 之间是否有 assistant message
                        for k in range(j + 1, batch_start):
                            if messages[k].get('role') == 'assistant':
                                assistant_message = messages[k].get('content', '')
                                break
                        break
                    elif prev_role == 'assistant' and assistant_message is None:
                        # 记录最近的 assistant message（可能是说明性的）
                        assistant_message = prev_msg.get('content', '')

                # 3. 向后查找对应的 tool_response（按照顺序匹配）
                tool_response = None
                response_count = 0
                is_structured_response = None  # 该次调用的返回是否为结构化格式
                for j in range(i + 1, len(messages)):
                    next_msg = messages[j]
                    next_role = next_msg.get('role', '')
                    if next_role == 'tool_response':
                        if response_count == tool_call_index:
                            # 找到与当前 tool_call 对应的 tool_response
                            tool_response = next_msg.get('content', '')

                            # 判断 tool response 是否是结构化的形式
                            # 允许两种情况：
                            # 1) 直接是 dict / list
                            # 2) 字符串形式但能被 json 解析为 dict / list
                            try:
                                value = tool_response
                                if isinstance(value, str):
                                    stripped = value.strip()
                                    # 先快速判断一下是否像 JSON，再尝试解析
                                    if (stripped.startswith("{") and stripped.endswith("}")) or (
                                        stripped.startswith("[") and stripped.endswith("]")
                                    ):
                                        parsed = json.loads(stripped)
                                        is_structured_response = isinstance(parsed, (dict, list))
                                    else:
                                        is_structured_response = False
                                else:
                                    # 非字符串，直接看是否是常见结构化类型
                                    is_structured_response = isinstance(value, (dict, list))
                            except Exception:
                                is_structured_response = False

                            break
                        response_count += 1
                    elif next_role in ['assistant', 'user', 'tool_call']:
                        # 如果遇到新的 assistant/user/tool_call，说明已经过了 responses
                        break

                # 如果找到了完整的上下文，添加到结果
                if user_query and tool_response:
                    results.append({
                        'user_query': user_query,
                        'assistant_message': assistant_message or '',
                        'tool_call': {
                            'name': tool_info['name'],
                            'arguments': tool_info['arguments']
                        },
                        'tool_response': tool_response,
                        # 标记该次调用的返回是否为结构化格式
                        # （后续在聚合阶段，可以对同一个 tool 只保留一个标记）
                        'tool_response_is_structured': is_structured_response,
                    })

        i += 1

    return results


def find_tool_examples(
    dataset_path: str,
    tool_set: List[str],
    examples_per_tool: int = 3,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    为每个 tool 找到指定数量的调用示例

    Args:
        dataset_path: str, 数据集路径
        tool_set: List[str], tool 名称列表
        examples_per_tool: int, 每个 tool 需要的示例数量

    Returns:
        Dict[str, List[Dict]]: {tool_name: [example1, example2, ...]}
    """
    print(f"\nLoading dataset from {dataset_path}...")
    dataset = datasets.load_from_disk(dataset_path)
    print(f"Loaded {len(dataset)} samples")

    # 为每个 tool 收集示例
    tool_examples: Dict[str, List[Dict[str, Any]]] = {tool: [] for tool in tool_set}

    print(f"\nFinding examples for {len(tool_set)} tools (target: {examples_per_tool} per tool)...")

    for sample in tqdm(dataset, desc="Processing samples"):
        uuid = sample.get('uuid', '')
        messages_str = sample.get('messages', '[]')

        try:
            messages = json.loads(messages_str) if isinstance(messages_str, str) else messages_str
        except json.JSONDecodeError:
            continue

        # 检查每个 tool 是否在这个样本中被调用
        for tool_name in tool_set:
            if len(tool_examples[tool_name]) >= examples_per_tool:
                continue  # 已经收集够了

            contexts = extract_tool_call_context(messages, tool_name)
            for context in contexts:
                if len(tool_examples[tool_name]) >= examples_per_tool:
                    break

                # 添加 uuid 以便追踪
                context['uuid'] = uuid
                tool_examples[tool_name].append(context)

    # 打印统计信息
    print("\n" + "=" * 80)
    print("Tool Examples Collection Summary")
    print("=" * 80)
    tools_with_examples = sum(1 for examples in tool_examples.values() if len(examples) > 0)
    tools_without_examples = sum(1 for examples in tool_examples.values() if len(examples) == 0)
    print(f"Tools with at least 1 example: {tools_with_examples}")
    print(f"Tools with no examples: {tools_without_examples}")
    print(f"Total tools: {len(tool_set)}")
    print("=" * 80)

    return tool_examples


def save_tool_examples(
    tool_examples: Dict[str, List[Dict[str, Any]]],
    output_path: str,
    statistics: Dict[str, Any] = None,
) -> None:
    """
    保存 tool examples 到 JSON 文件

    Args:
        tool_examples: Dict[str, List[Dict]], tool 示例字典
        output_path: str, 输出文件路径
        statistics: Dict, 可选的统计信息
    """
    print(f"\nSaving tool examples to {output_path}...")

    # 转换为更易读的格式
    output_data = {
        'summary': {
            'total_tools': len(tool_examples),
            'tools_with_examples': sum(1 for examples in tool_examples.values() if len(examples) > 0),
            'tools_without_examples': sum(1 for examples in tool_examples.values() if len(examples) == 0),
            'examples_per_tool': {
                tool: len(examples) for tool, examples in tool_examples.items()
            }
        },
        'tool_examples': tool_examples
    }

    # 如果提供了统计信息，添加到输出
    if statistics:
        output_data['filtering_statistics'] = statistics

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(tool_examples)} tools' examples to {output_path}")


def main():
    """
    主流程：
    1. 读取 tool_with_server.json 获取所有 tool
    2. 读取 mcp_status_judgment_results.json 获取所有 MCP 的状态信息
    3. 筛选出所有属于 non-stateful MCP 的 tools
    4. 使用 find_tool_examples 函数为这些 tools 找示例
    5. 保存到 tool_output.json
    """
    # 配置路径
    ROOT_DIR = '/data/lhy/datasets/graph-Toucan'
    tool_with_server_path = os.path.join(ROOT_DIR, 'tool_info', 'tool_with_server.json')
    mcp_status_path = os.path.join(ROOT_DIR, 'test_MCP', 'mcp_status_judgment_results.json')
    dataset_path = os.path.join(ROOT_DIR, 'datasets', 'Toucan-single-turn-with-mcp-field')
    output_path = os.path.join(ROOT_DIR, 'tool_output.json')

    # 步骤 1-3: 加载并筛选 non-stateful tools
    non_stateful_tools, statistics = load_tools_from_tool_with_server(
        tool_with_server_path=tool_with_server_path,
        mcp_status_path=mcp_status_path,
    )

    if not non_stateful_tools:
        print("\nNo non-stateful tools found! Exiting...")
        return

    # 步骤 4: 查找示例
    tool_examples = find_tool_examples(
        dataset_path=dataset_path,
        tool_set=non_stateful_tools,
        examples_per_tool=3,
    )

    # 步骤 5: 保存结果
    save_tool_examples(tool_examples, output_path, statistics)

    


if __name__ == "__main__":
    main()
