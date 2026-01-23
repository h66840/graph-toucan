import json
import os
import re
import asyncio
from collections import defaultdict
from tqdm import tqdm
from openai import AsyncOpenAI

# 初始化异步 OpenAI 客户端
async_client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def load_unique_mcp_servers(json_file):
    """
    从 tool_with_server.json 中读取所有唯一的 MCP server info
    
    Args:
        json_file: str, JSON 文件路径
        
    Returns:
        dict: {server_key: mcp_server_info}，server_key 用于去重
        dict: {server_key: [function_names]}，每个 server 对应的函数名列表
    """
    print(f"Loading data from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 使用 server name 作为唯一标识
    unique_servers = {}
    server_to_functions = defaultdict(list)
    
    for item in tqdm(data, desc="Extracting unique MCP servers"):
        mcp_server_info = item.get('mcp_server_info')
        if not mcp_server_info:
            continue
        
        function_schema = item.get('function_schema', {})
        function_info = function_schema.get('function', {})
        function_name = function_info.get('name', '')
        
        # 使用 server name 作为唯一标识
        server_name = mcp_server_info.get('name', 'Unknown')
        
        # 如果 server 还没有被记录，添加它
        if server_name not in unique_servers:
            unique_servers[server_name] = mcp_server_info
        
        # 记录这个函数属于哪个 server
        if function_name:
            server_to_functions[server_name].append(function_name)
    
    print(f"Found {len(unique_servers)} unique MCP servers")
    return unique_servers, dict(server_to_functions)


async def judge_mcp_status(mcp_server_info):
    """
    根据 MCP server 的 info，判断这个 MCP 是否是有状态的。
    
    状态的定义：MCP 中一个函数的调用是否会影响任一其他的函数的调用。
    例如：函数 A 调用后会改变 system 的某个状态 A，而函数 B 调用依赖于 system 的状态 A。
    
    Args:
        mcp_server_info: dict, MCP server 信息，包含以下字段：
            - name: str, MCP server 名称
            - overview: str, MCP server 概述
            - tools: list, 工具列表，每个工具包含 name, description, input_schema 等
    
    Returns:
        dict: 包含以下字段：
            - is_stateful: bool, 是否有状态
            - confidence: float, 置信度 (0.0-1.0)
            - reasoning: str, 判断理由
            - state_dependencies: list, 状态依赖关系列表，每个元素包含：
                - function_a: str, 改变状态的函数名
                - function_b: str, 依赖状态的函数名
                - state_description: str, 状态描述
            - token_usage: dict, token 使用统计
    """
    server_name = mcp_server_info.get('name', 'Unknown')
    overview = mcp_server_info.get('overview', '')
    tools = mcp_server_info.get('tools', [])
    
    if not tools:
        return {
            'is_stateful': False,
            'confidence': 1.0,
            'reasoning': 'No tools found in MCP server',
            'state_dependencies': [],
            'token_usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        }
    
    # 如果只有一个函数，直接返回无状态（单个函数无法形成状态依赖）
    if len(tools) == 1:
        return {
            'is_stateful': False,
            'confidence': 1.0,
            'reasoning': 'MCP server has only one function, so there cannot be state dependencies between functions',
            'state_dependencies': [],
            'token_usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        }
    
    # 构建 tools 信息字符串
    tools_info = []
    for i, tool in enumerate(tools, 1):
        tool_name = tool.get('name', f'tool_{i}')
        tool_desc = tool.get('description', '')
        tool_params = tool.get('input_schema', {})
        
        tool_str = f"Tool {i}: {tool_name}\n"
        tool_str += f"  Description: {tool_desc}\n"
        if tool_params:
            tool_str += f"  Parameters: {json.dumps(tool_params, indent=2, ensure_ascii=False)}\n"
        tools_info.append(tool_str)
    
    tools_text = "\n".join(tools_info)
    
    # 构建提示词
    prompt = f"""You are an expert in analyzing MCP (Model Context Protocol) servers to determine if they are stateful.

A stateful MCP server means that calling one function can affect the behavior or results of other function calls. This happens when:
1. Function A modifies some system state (e.g., sets a configuration, creates a session, stores data)
2. Function B depends on that state (e.g., reads the configuration, uses the session, retrieves the stored data)

MCP Server Information:
- Name: {server_name}
- Overview: {overview}

Available Tools:
{tools_text}

Please analyze whether this MCP server is stateful. Consider:
1. Do any functions modify persistent state (e.g., create/update/delete operations)?
2. Do any functions depend on previously set state (e.g., read operations that depend on prior writes)?
3. Are there function pairs where one function sets up state that another function uses?
4. Do functions share context, sessions, or configurations that persist across calls?

Your output MUST be in the following format:
IS_STATEFUL: [true/false]
CONFIDENCE: [0.0-1.0]
REASONING: [detailed explanation of your judgment]
STATE_DEPENDENCIES: [JSON array of state dependency objects, or empty array if not stateful]
Each state dependency object should have:
  - "function_a": name of function that modifies state
  - "function_b": name of function that depends on the state
  - "state_description": description of what state is shared

Example output:
IS_STATEFUL: true
CONFIDENCE: 0.85
REASONING: The MCP server has a create_session function that creates a session ID, and a query_session function that requires the session ID to retrieve session data. This indicates stateful behavior.
STATE_DEPENDENCIES: [{{"function_a": "create_session", "function_b": "query_session", "state_description": "Session ID created by create_session is required by query_session"}}]
"""

    try:
        completion = await async_client.chat.completions.create(
            model="qwen3-235b-a22b-instruct-2507",
            messages=[
                {"role": "system", "content": "You are an expert analyst specializing in determining whether MCP servers exhibit stateful behavior."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.3,
            max_completion_tokens=1024
        )
        
        response_text = completion.choices[0].message.content
        
        # 解析响应
        is_stateful = False
        confidence = 0.0
        reasoning = ""
        state_dependencies = []
        
        lines = response_text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_upper = line.upper().strip()
            
            if line_upper.startswith('IS_STATEFUL:'):
                value = line.split(':', 1)[1].strip() if ':' in line else ""
                is_stateful = value.lower() in ['true', 'yes', '1', 'y']
                current_section = None
            elif line_upper.startswith('CONFIDENCE:'):
                value = line.split(':', 1)[1].strip() if ':' in line else "0.0"
                try:
                    confidence = float(value)
                except ValueError:
                    confidence = 0.0
                current_section = None
            elif line_upper.startswith('REASONING:'):
                current_section = 'reasoning'
                current_content = []
                if ':' in line:
                    current_content.append(line.split(':', 1)[1].strip())
            elif line_upper.startswith('STATE_DEPENDENCIES:'):
                current_section = 'dependencies'
                current_content = []
                if ':' in line:
                    dep_str = line.split(':', 1)[1].strip()
                    if dep_str:
                        current_content.append(dep_str)
            elif current_section == 'reasoning':
                current_content.append(line.strip())
            elif current_section == 'dependencies':
                current_content.append(line.strip())
        
        # 处理 reasoning
        if current_section == 'reasoning' and current_content:
            reasoning = ' '.join(current_content).strip()
        
        # 处理 state_dependencies
        if current_section == 'dependencies' and current_content:
            dep_text = ' '.join(current_content).strip()
            # 尝试解析 JSON
            try:
                # 查找 JSON 数组部分
                start_idx = dep_text.find('[')
                end_idx = dep_text.rfind(']')
                if start_idx != -1 and end_idx != -1:
                    json_str = dep_text[start_idx:end_idx+1]
                    state_dependencies = json.loads(json_str)
            except json.JSONDecodeError:
                # 如果解析失败，尝试其他方式
                pass
        
        # 如果没有找到明确的标记，尝试从整个响应中提取
        if not reasoning and response_text:
            # 尝试找到 REASONING 部分
            reasoning_match = re.search(r'REASONING[:\s]+(.+?)(?=STATE_DEPENDENCIES|$)', response_text, re.IGNORECASE | re.DOTALL)
            if reasoning_match:
                reasoning = reasoning_match.group(1).strip()
        
        token_usage = {
            'prompt_tokens': completion.usage.prompt_tokens,
            'completion_tokens': completion.usage.completion_tokens,
            'total_tokens': completion.usage.total_tokens
        }
        
        return {
            'is_stateful': is_stateful,
            'confidence': confidence,
            'reasoning': reasoning,
            'state_dependencies': state_dependencies,
            'token_usage': token_usage
        }
        
    except Exception as e:
        return {
            'is_stateful': False,
            'confidence': 0.0,
            'reasoning': f'Error analyzing MCP server: {str(e)}',
            'state_dependencies': [],
            'token_usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        }


async def batch_judge_mcp_status(unique_servers, batch_size=10):
    """
    批量判断 MCP servers 的状态
    
    Args:
        unique_servers: dict, {server_name: mcp_server_info}
        batch_size: int, 批处理大小
        
    Returns:
        dict: {server_name: judgment_result}
    """
    results = {}
    failed_servers = []
    
    server_names = list(unique_servers.keys())
    total_batches = (len(server_names) + batch_size - 1) // batch_size
    
    batch_iterator = tqdm(
        range(0, len(server_names), batch_size),
        total=total_batches,
        desc="Judging MCP servers",
        unit="batch"
    )
    
    for i in batch_iterator:
        batch_names = server_names[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        # 创建异步任务
        tasks = []
        for server_name in batch_names:
            mcp_server_info = unique_servers[server_name]
            tasks.append(judge_mcp_status(mcp_server_info))
        
        # 并发执行
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        for idx, result in enumerate(batch_results):
            server_name = batch_names[idx]
            if isinstance(result, Exception):
                error_msg = str(result)
                tqdm.write(f"  Error judging server '{server_name}': {error_msg}")
                failed_servers.append({
                    'server_name': server_name,
                    'error': error_msg
                })
                results[server_name] = {
                    'is_stateful': False,
                    'confidence': 0.0,
                    'reasoning': f'Error: {error_msg}',
                    'state_dependencies': [],
                    'token_usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
                }
            else:
                results[server_name] = result
        
        batch_iterator.set_postfix_str(f"batch={batch_num}/{total_batches}")
    
    batch_iterator.close()
    
    return results, failed_servers


def print_statistics(results, server_to_functions):
    """
    打印统计结果
    
    Args:
        results: dict, {server_name: judgment_result}
        server_to_functions: dict, {server_name: [function_names]}
    """
    total_servers = len(results)
    stateful_servers = sum(1 for r in results.values() if r.get('is_stateful', False))
    stateless_servers = total_servers - stateful_servers
    
    # 统计函数数量
    total_functions = sum(len(funcs) for funcs in server_to_functions.values())
    stateful_functions = sum(
        len(server_to_functions.get(server_name, []))
        for server_name, result in results.items()
        if result.get('is_stateful', False)
    )
    stateless_functions = total_functions - stateful_functions
    
    # 统计 token 使用
    total_prompt_tokens = sum(r.get('token_usage', {}).get('prompt_tokens', 0) for r in results.values())
    total_completion_tokens = sum(r.get('token_usage', {}).get('completion_tokens', 0) for r in results.values())
    total_tokens = sum(r.get('token_usage', {}).get('total_tokens', 0) for r in results.values())
    
    # 统计置信度
    stateful_confidences = [r.get('confidence', 0.0) for r in results.values() if r.get('is_stateful', False)]
    avg_confidence = sum(stateful_confidences) / len(stateful_confidences) if stateful_confidences else 0.0
    
    print("\n" + "="*80)
    print("MCP Server Statefulness Analysis Statistics")
    print("="*80)
    
    print(f"\nServer Statistics:")
    print(f"  Total MCP servers analyzed: {total_servers}")
    print(f"  Stateful servers: {stateful_servers} ({stateful_servers/total_servers*100:.2f}%)")
    print(f"  Stateless servers: {stateless_servers} ({stateless_servers/total_servers*100:.2f}%)")
    
    print(f"\nFunction Statistics:")
    print(f"  Total functions: {total_functions}")
    print(f"  Functions in stateful servers: {stateful_functions} ({stateful_functions/total_functions*100:.2f}%)")
    print(f"  Functions in stateless servers: {stateless_functions} ({stateless_functions/total_functions*100:.2f}%)")
    
    print(f"\nConfidence Statistics:")
    if stateful_confidences:
        print(f"  Average confidence (stateful servers): {avg_confidence:.3f}")
        print(f"  Min confidence: {min(stateful_confidences):.3f}")
        print(f"  Max confidence: {max(stateful_confidences):.3f}")
    
    print(f"\nToken Usage:")
    print(f"  Total prompt tokens: {total_prompt_tokens:,}")
    print(f"  Total completion tokens: {total_completion_tokens:,}")
    print(f"  Total tokens: {total_tokens:,}")
    print(f"  Average tokens per server: {total_tokens/total_servers:.0f}")
    
    # 显示一些示例
    print(f"\nSample Stateful Servers (top 5 by confidence):")
    stateful_items = [(name, r) for name, r in results.items() if r.get('is_stateful', False)]
    stateful_items.sort(key=lambda x: x[1].get('confidence', 0.0), reverse=True)
    for server_name, result in stateful_items[:5]:
        confidence = result.get('confidence', 0.0)
        func_count = len(server_to_functions.get(server_name, []))
        print(f"  - {server_name}: confidence={confidence:.3f}, functions={func_count}")
    
    print("="*80 + "\n")


async def main():
    """
    主函数：从 tool_with_server.json 读取数据，批量分析 MCP servers，并输出统计结果
    """
    json_file = '/data/lhy/datasets/graph-Toucan/tool_with_server.json'
    output_file = '/data/lhy/datasets/graph-Toucan/mcp_status_judgment_results.json'
    
    # 1. 加载唯一的 MCP servers
    unique_servers, server_to_functions = load_unique_mcp_servers(json_file)
    
    # 2. 批量判断
    print(f"\nStarting batch judgment for {len(unique_servers)} MCP servers...")
    results, failed_servers = await batch_judge_mcp_status(unique_servers, batch_size=10)
    
    # 3. 保存结果
    output_data = {
        'summary': {
            'total_servers': len(unique_servers),
            'analyzed_servers': len(results),
            'failed_servers': len(failed_servers)
        },
        'results': {
            server_name: {
                **result,
                'function_count': len(server_to_functions.get(server_name, [])),
                'functions': server_to_functions.get(server_name, [])
            }
            for server_name, result in results.items()
        },
        'failed_servers': failed_servers
    }
    
    print(f"\nSaving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"Results saved successfully!")
    
    # 4. 打印统计信息
    print_statistics(results, server_to_functions)
    
    return results, server_to_functions


if __name__ == "__main__":
    asyncio.run(main())
