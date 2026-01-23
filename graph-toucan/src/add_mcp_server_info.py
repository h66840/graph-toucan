import json
import os
import re
from collections import defaultdict
from tqdm import tqdm

def load_all_mcp_servers(mcp_servers_dir):
    """
    加载所有 MCP server 文件，构建 tool name 到 server 的映射
    
    Args:
        mcp_servers_dir: str, MCP server 文件目录路径
        
    Returns:
        dict: {tool_full_name: mcp_server_info}
        dict: {server_file_name: mcp_server_data}
        dict: {server_file_name: server_prefix}  # 用于反向查找
    """
    tool_to_server = {}
    server_files_data = {}
    server_prefix_map = {}  # server_file -> server_prefix
    
    print(f"Loading MCP server files from {mcp_servers_dir}...")
    
    # 获取所有 JSON 文件
    json_files = [f for f in os.listdir(mcp_servers_dir) if f.endswith('.json')]
    
    for json_file in tqdm(json_files, desc="Loading MCP servers"):
        file_path = os.path.join(mcp_servers_dir, json_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                server_data = json.load(f)
            
            server_files_data[json_file] = server_data
            
            # 获取 server_info_crawled
            server_info = server_data['metadata'].get('server_info_crawled', {})
            if not server_info:
                continue
            
            # 获取 tools 列表
            tools = server_info.get('tools', [])
            if not tools:
                # 尝试从 remote_server_response 获取
                remote_response = server_data.get('remote_server_response', {})
                tools = remote_response.get('tools', [])
            
            if not tools:
                continue
            
            # 构建 server prefix
            # 从文件名或 server_info 中提取 server identifier
            server_name = server_info.get('name', '')
            author = server_info.get('author', '')
            
            # 尝试多种方式构建 server prefix
            server_prefixes = []
            
            # 方式1: 从 author 提取（如 @pwh-pwh/coin-mcp-server -> coin-mcp-server）
            if author:
                # 移除 @ 和 / 后的部分
                if '/' in author:
                    prefix = author.split('/')[-1]
                    server_prefixes.append(prefix)
                elif author.startswith('@'):
                    # 处理 @username_repo-name 格式
                    if '_' in author:
                        prefix = author.split('_')[-1]
                    else:
                        prefix = author[1:].replace('/', '-')
                    server_prefixes.append(prefix)
            
            # 方式2: 从文件名提取（如 0358.@pwh-pwh_coin-mcp-server_labeled.json -> coin-mcp-server）
            file_base = json_file.replace('_labeled.json', '').replace('.json', '')
            # 移除开头的数字和点
            if '.' in file_base:
                parts = file_base.split('.', 1)
                if len(parts) > 1:
                    file_prefix = parts[1]
                    # 移除 @ 和可能的用户名部分
                    if '@' in file_prefix:
                        # 处理 @username_repo-name 格式，取最后一部分
                        if '_' in file_prefix:
                            file_prefix = file_prefix.split('_')[-1]
                        else:
                            # 处理 @username/repo-name 格式
                            if '/' in file_prefix:
                                file_prefix = file_prefix.split('/')[-1]
                    server_prefixes.append(file_prefix)
            
            # 方式3: 从 server name 提取（转换为小写，替换空格为连字符）
            if server_name:
                name_prefix = server_name.lower().replace(' ', '-').replace('_', '-')
                server_prefixes.append(name_prefix)
            
            # 去重并选择最可能的 prefix（优先使用 author 中的）
            unique_prefixes = []
            seen = set()
            for prefix in server_prefixes:
                if prefix and prefix not in seen:
                    unique_prefixes.append(prefix)
                    seen.add(prefix)
            
            # 使用第一个 prefix 作为主要 prefix
            main_prefix = unique_prefixes[0] if unique_prefixes else None
            if main_prefix:
                server_prefix_map[json_file] = main_prefix
            
            # 为每个 tool 构建完整名称并建立映射
            for tool in tools:
                tool_name = tool.get('name', '')
                if not tool_name:
                    continue
                
                # 尝试不同的 server prefix 组合
                for prefix in unique_prefixes:
                    # 构建可能的完整 tool 名称
                    possible_names = [
                        f"{prefix}-{tool_name}",  # 最常见格式：coin-mcp-server-getTokenPrice
                        f"{prefix}_{tool_name}",  # 下划线格式
                    ]
                    
                    for full_name in possible_names:
                        if full_name not in tool_to_server:
                            tool_to_server[full_name] = {
                                'server_file': json_file,
                                'server_data': server_data,
                                'server_info': server_info,
                                'tool': tool,
                                'server_prefix': prefix
                            }
            
        except Exception as e:
            print(f"Error loading {json_file}: {str(e)}")
            continue
    
    print(f"Loaded {len(server_files_data)} MCP server files")
    print(f"Built mapping for {len(tool_to_server)} tools")
    
    return tool_to_server, server_files_data, server_prefix_map


def extract_mcp_server_info(server_info, server_data=None):
    """
    从 server_info_crawled 中提取需要的字段
    
    Args:
        server_info: dict, server_info_crawled 字典
        server_data: dict, 可选的完整 server_data，用于获取 tools（如果 server_info 中没有）
        
    Returns:
        dict: 包含 name, overview, tools 的字典
    """
    tools = server_info.get('tools', [])
    
    # 如果 server_info 中没有 tools，尝试从 remote_server_response 获取
    if not tools and server_data:
        remote_response = server_data.get('remote_server_response', {})
        tools = remote_response.get('tools', [])
    
    return {
        'name': server_info.get('name', ''),
        'overview': server_info.get('overview', ''),
        'tools': tools
    }


def add_mcp_server_info_to_results(results_file, tool_to_server, server_prefix_map, server_files_data, output_file=None):
    """
    为 tool_classification_results.json 中的每个函数添加 MCP server 信息
    
    Args:
        results_file: str, tool_classification_results.json 文件路径
        tool_to_server: dict, tool name 到 server 的映射
        server_prefix_map: dict, server_file -> server_prefix
        server_files_data: dict, server_file -> server_data
        output_file: str, 可选，输出文件路径，如果为 None 则覆盖原文件
        
    Returns:
        dict: 统计信息
    """
    print(f"Loading classification results from {results_file}...")
    with open(results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    print(f"Found {len(results)} functions to process")
    
    stats = {
        'total': len(results),
        'matched': 0,
        'unmatched': 0,
        'unmatched_tools': set(),
        'matched_servers': set()  # 记录匹配到的不同 MCP server
    }
    
    # 构建反向映射：从 server_prefix 到 server_file，用于模糊匹配
    prefix_to_servers = defaultdict(list)
    for server_file, prefix in server_prefix_map.items():
        prefix_to_servers[prefix].append(server_file)
    
    # 处理每个结果
    for result in tqdm(results, desc="Adding MCP server info"):
        function_schema = result.get('function_schema', {})
        function_info = function_schema.get('function', {})
        tool_name = function_info.get('name', '')
        
        if not tool_name:
            stats['unmatched'] += 1
            continue
        
        # 方法1: 直接匹配完整 tool 名称
        server_mapping = tool_to_server.get(tool_name)
        
        if server_mapping:
            server_info = server_mapping['server_info']
            
            # 添加 mcp_server 字段（server 文件名）
            result['mcp_server'] = server_mapping['server_file']
            
            # 添加 mcp_server_info 字段
            result['mcp_server_info'] = extract_mcp_server_info(server_info, server_mapping['server_data'])
            
            stats['matched'] += 1
            stats['matched_servers'].add(server_mapping['server_file'])
        else:
            # 方法2: 尝试通过 server prefix 匹配
            # 从 tool_name 中提取可能的 server prefix 和 tool name
            # 格式通常是: server-prefix-tool-name
            matched = False
            
            # 尝试不同的分割方式
            parts = tool_name.split('-')
            if len(parts) >= 2:
                # 尝试从后往前匹配：假设最后一部分是 tool name，前面是 server prefix
                for i in range(1, len(parts)):
                    possible_prefix = '-'.join(parts[:-i])
                    possible_tool_name = '-'.join(parts[-i:])
                    
                    # 查找匹配的 server
                    if possible_prefix in prefix_to_servers:
                        # 找到匹配的 server，检查 tool name 是否匹配
                        for server_file in prefix_to_servers[possible_prefix]:
                            server_data = server_files_data.get(server_file, {})
                            # 尝试从 metadata 中获取，如果没有则从根级别获取
                            server_info = server_data.get('metadata', {}).get('server_info_crawled', {})
                            if not server_info:
                                server_info = server_data.get('server_info_crawled', {})
                            if not server_info:
                                continue
                            
                            tools = server_info.get('tools', [])
                            if not tools:
                                remote_response = server_data.get('remote_server_response', {})
                                tools = remote_response.get('tools', [])
                            
                            # 检查 tool name 是否匹配（支持多种格式）
                            for tool in tools:
                                tool_base_name = tool.get('name', '')
                                
                                # 标准化工具名称用于比较（转换为小写，统一分隔符）
                                def normalize_name(name):
                                    # 将驼峰命名转换为连字符命名
                                    # 在大写字母前插入连字符（除了第一个字符）
                                    name = re.sub(r'(?<!^)(?=[A-Z])', '-', name)
                                    return name.lower().replace('_', '-')
                                
                                normalized_tool = normalize_name(tool_base_name)
                                normalized_possible = normalize_name(possible_tool_name)
                                
                                # 支持完全匹配或忽略大小写/格式差异
                                if tool_base_name == possible_tool_name or \
                                   tool_base_name.lower() == possible_tool_name.lower() or \
                                   tool_base_name.replace('_', '-') == possible_tool_name.replace('_', '-') or \
                                   normalized_tool == normalized_possible:
                                    result['mcp_server'] = server_file
                                    result['mcp_server_info'] = extract_mcp_server_info(server_info, server_data)
                                    stats['matched'] += 1
                                    stats['matched_servers'].add(server_file)
                                    matched = True
                                    break
                            
                            if matched:
                                break
                    
                    if matched:
                        break
            
            if not matched:
                stats['unmatched'] += 1
                stats['unmatched_tools'].add(tool_name)
    
    # 保存结果
    if output_file is None:
        output_file = results_file
    
    print(f"\nSaving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nStatistics:")
    print(f"  Total functions: {stats['total']}")
    print(f"  Matched: {stats['matched']} ({stats['matched']/stats['total']*100:.2f}%)")
    print(f"  Unmatched: {stats['unmatched']} ({stats['unmatched']/stats['total']*100:.2f}%)")
    print(f"  Matched MCP servers: {len(stats['matched_servers'])} unique servers")
    
    if stats['unmatched_tools']:
        print(f"\nSample unmatched tools (showing first 20):")
        for tool in list(stats['unmatched_tools'])[:20]:
            print(f"  - {tool}")
    
    return stats


def main():
    mcp_servers_dir = '/data/lhy/Toucan/mcp_servers'
    results_file = '/data/lhy/datasets/graph-Toucan/tool_classification_results.json'
    output_file = '/data/lhy/datasets/graph-Toucan/tool_with_server.json'  # 覆盖原文件
    
    # 加载所有 MCP server 文件
    tool_to_server, server_files_data, server_prefix_map = load_all_mcp_servers(mcp_servers_dir)
    
    # 为结果添加 MCP server 信息
    stats = add_mcp_server_info_to_results(
        results_file, 
        tool_to_server, 
        server_prefix_map,
        server_files_data,
        output_file
    )
    
    print("\nDone!")


if __name__ == "__main__":
    main()

