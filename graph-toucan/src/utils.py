import json
import datasets
import random
from collections import defaultdict
from tqdm import tqdm

# 加载数据集
data = datasets.load_from_disk('/data/lhy/datasets/graph-Toucan/Toucan-single-turn-subset')

# 加载 tool -> MCP 映射关系
def load_tool_server_mapping(json_file='tool_with_server.json'):
    """
    加载 tool 到 MCP server 的映射关系
    
    Args:
        json_file: str, tool_with_server.json 文件路径
        
    Returns:
        dict: {tool_name: {mcp_server: str, mcp_server_info: dict}}
    """
    print(f"Loading tool-server mapping from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        tool_list = json.load(f)
    
    # 构建 tool_name -> MCP server 的映射
    tool_to_mcp = {}
    for tool_item in tool_list:
        function_schema = tool_item.get('function_schema', {})
        function = function_schema.get('function', {})
        tool_name = function.get('name', '')
        
        if tool_name:
            tool_to_mcp[tool_name] = {
                'mcp_server': tool_item.get('mcp_server', ''),
                'mcp_server_info': tool_item.get('mcp_server_info', {})
            }
    
    print(f"Loaded {len(tool_to_mcp)} tool-to-MCP mappings")
    return tool_to_mcp


def load_mcp_status_info(json_file='mcp_status_judgment_results.json'):
    """
    加载 MCP server 的状态信息（stateful/stateless）
    
    Args:
        json_file: str, mcp_status_judgment_results.json 文件路径
        
    Returns:
        dict: {server_name: {is_stateful: bool, confidence: float, ...}}
    """
    print(f"Loading MCP status information from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        status_data = json.load(f)
    
    # results 字典的 key 是 server name，value 包含 is_stateful 等信息
    status_info = status_data.get('results', {})
    print(f"Loaded status information for {len(status_info)} MCP servers")
    return status_info


def extract_mcp_info_for_sample(sample, tool_to_mcp, mcp_status_info=None):
    """
    对一条数据样本，提取其使用的所有 MCP server 信息
    
    Args:
        sample: dict, 数据集中的一条样本
        tool_to_mcp: dict, tool_name -> MCP server 的映射
        mcp_status_info: dict, {server_name: {is_stateful: bool, ...}}，MCP server 状态信息
        
    Returns:
        dict: 包含 MCP 信息的字典
            - mcp_servers: list, 使用的 MCP server 列表（去重）
            - mcp_info: dict, {mcp_server_name: {name, overview, is_stateful, ...}}
    """
    # 解析 tools 字段（JSON 字符串）
    tools_str = sample.get('tools', '[]')
    try:
        tools = json.loads(tools_str) if isinstance(tools_str, str) else tools_str
    except json.JSONDecodeError as e:
        # 静默处理错误，返回空结果
        tools = []
    
    # 收集所有使用的 MCP server
    mcp_servers_set = set()
    mcp_info_dict = {}
    
    for tool in tools:
        if isinstance(tool, dict):
            function = tool.get('function', {})
            tool_name = function.get('name', '')
            
            if tool_name and tool_name in tool_to_mcp:
                mcp_mapping = tool_to_mcp[tool_name]
                mcp_server = mcp_mapping.get('mcp_server', '')
                mcp_server_info = mcp_mapping.get('mcp_server_info', {})
                server_name = mcp_server_info.get('name', '')
                
                if mcp_server:
                    mcp_servers_set.add(mcp_server)
                    
                    # 如果这个 MCP server 还没有记录，则添加其信息
                    if mcp_server not in mcp_info_dict:
                        # 从 mcp_status_judgment_results.json 中获取状态信息
                        is_stateful = None
                        confidence = None
                        if mcp_status_info and server_name in mcp_status_info:
                            status_data = mcp_status_info[server_name]
                            is_stateful = status_data.get('is_stateful', None)
                            confidence = status_data.get('confidence', None)
                        
                        mcp_info_dict[mcp_server] = {
                            'mcp_server': mcp_server,
                            'name': server_name,
                            'overview': mcp_server_info.get('overview', ''),
                            'is_stateful': is_stateful,
                            'confidence': confidence
                        }
    
    return {
        'mcp_servers': sorted(list(mcp_servers_set)),
        'mcp_info': mcp_info_dict
    }


def add_contained_mcp_field(dataset, tool_to_mcp, mcp_status_info=None, output_path=None):
    """
    为数据集添加 contained_MCP 字段
    
    Args:
        dataset: datasets.Dataset, HuggingFace 数据集对象
        tool_to_mcp: dict, tool_name -> MCP server 的映射
        mcp_status_info: dict, {server_name: {is_stateful: bool, ...}}，MCP server 状态信息
        output_path: str or None, 如果提供则保存处理后的数据集
        
    Returns:
        datasets.Dataset: 添加了 contained_MCP 字段的数据集
    """
    print(f"Processing {len(dataset)} samples...")
    
    def process_sample(sample):
        mcp_info = extract_mcp_info_for_sample(sample, tool_to_mcp, mcp_status_info)
        sample['contained_MCP'] = json.dumps(mcp_info, ensure_ascii=False)
        return sample
    
    # 使用 map 函数批量处理
    dataset = dataset.map(process_sample, desc="Adding contained_MCP field")
    
    if output_path:
        print(f"Saving processed dataset to {output_path}...")
        dataset.save_to_disk(output_path)
        print(f"Dataset saved successfully!")
    
    return dataset


def load_common_use_mcp(txt_file='common_use_MCP.txt'):
    """
    从文本文件中加载 common_use_MCP 列表
    
    Args:
        txt_file: str, common_use_MCP.txt 文件路径
        
    Returns:
        set: common_use_MCP 的集合
    """
    print(f"Loading common_use_MCP from {txt_file}...")
    common_mcp_set = set()
    
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 格式: "0059.@smithery-ai_national-weather-service_labeled.json: 322"
            # 提取冒号前的部分作为 MCP server 名称
            if ':' in line:
                mcp_server = line.split(':', 1)[0].strip()
                common_mcp_set.add(mcp_server)
            else:
                # 如果没有冒号，整行作为 MCP server 名称
                common_mcp_set.add(line)
    
    print(f"Loaded {len(common_mcp_set)} common_use_MCP servers")
    return common_mcp_set


def count_samples_with_common_mcp(dataset, common_mcp_set, return_indices=False):
    """
    统计数据集中涉及 common_use_MCP 的数据条数
    
    Args:
        dataset: datasets.Dataset, HuggingFace 数据集对象
        common_mcp_set: set, common_use_MCP 的集合
        return_indices: bool, 是否返回涉及 common_use_MCP 的样本索引
        
    Returns:
        dict: 统计结果
            - total_samples: int, 总样本数
            - samples_with_common_mcp: int, 涉及 common_use_MCP 的样本数
            - samples_by_mcp: dict, {mcp_server: count} 每个 common MCP 涉及的样本数
            - samples_with_multiple_common_mcp: int, 涉及多个 common MCP 的样本数
            - sample_indices: list, 涉及 common_use_MCP 的样本索引（如果 return_indices=True）
    """
    print(f"\nAnalyzing dataset for common_use_MCP...")
    print(f"Common MCP servers to check: {len(common_mcp_set)}")
    
    samples_with_common_mcp = 0
    samples_to_test = 0
    samples_by_mcp = defaultdict(int)
    samples_with_multiple_common_mcp = 0
    sample_indices = []
    
    for idx, sample in enumerate(tqdm(dataset, desc="Counting samples")):
        contained_mcp_str = sample.get('contained_MCP', '{}')
        try:
            contained_mcp = json.loads(contained_mcp_str) if isinstance(contained_mcp_str, str) else contained_mcp_str
            mcp_servers = contained_mcp.get('mcp_servers', [])
            
            # 检查是否使用了非 common_use_MCP 的 MCP
            uncommon_mcps = [mcp for mcp in mcp_servers if mcp not in common_mcp_set]
            if uncommon_mcps:
                # 如果使用了非 common_use_MCP 的 MCP，跳过这个样本
                samples_to_test += 1
                continue
            
            # 检查是否有 common_use_MCP
            matched_common_mcps = []
            for mcp_server in mcp_servers:
                if mcp_server in common_mcp_set:
                    matched_common_mcps.append(mcp_server)
                    samples_by_mcp[mcp_server] += 1
                    
            if matched_common_mcps:
                samples_with_common_mcp += 1
                if return_indices:
                    sample_indices.append(idx)
                if len(matched_common_mcps) > 1:
                    samples_with_multiple_common_mcp += 1
        except Exception as e:
            # 静默处理错误
            pass
    
    result = {
        'total_samples': len(dataset),
        'samples_with_common_mcp': samples_with_common_mcp,
        'sample_with_uncommon_mcp': samples_to_test,
        'samples_by_mcp': dict(samples_by_mcp),
        'samples_with_multiple_common_mcp': samples_with_multiple_common_mcp,
        'coverage_rate': samples_with_common_mcp / len(dataset) * 100 if len(dataset) > 0 else 0
    }
    
    if return_indices:
        result['sample_indices'] = sample_indices
    
    return result


def analyze_common_use_mcp(output_path=None):
    """
    分析数据集中涉及 common_use_MCP 的情况，并保存涉及 common_use_MCP 的样本
    
    Args:
        output_path: str or None, 如果提供则保存涉及 common_use_MCP 的数据集
        
    Returns:
        dict: 统计结果和过滤后的数据集
    """
    # 加载数据集
    print("Loading dataset...")
    data_with_mcp = datasets.load_from_disk('/data/lhy/datasets/graph-Toucan/TOucan-single-turn-with-mcp-field-filtered-out')
    
    # 加载 common_use_MCP
    common_mcp_set = load_common_use_mcp('common_use_MCP_subset.txt')
    
    # 统计并获取样本索引
    stats = count_samples_with_common_mcp(data_with_mcp, common_mcp_set, return_indices=True)
    
    # 打印结果
    print("\n" + "="*80)
    print("Common Use MCP Analysis")
    print("="*80)
    print(f"Total samples in dataset: {stats['total_samples']}")
    print(f"Samples involving common_use_MCP: {stats['samples_with_common_mcp']}")
    print(f"Samples involving uncommon_MCP: {stats['sample_with_uncommon_mcp']}")
    print(f"Coverage rate: {stats['coverage_rate']:.2f}%")
    print(f"Samples with multiple common_use_MCP: {stats['samples_with_multiple_common_mcp']}")
    print(f"\nSamples count by common_use_MCP:")
    
    
    # 按样本数排序
    sorted_mcps = sorted(stats['samples_by_mcp'].items(), key=lambda x: x[1], reverse=True)
    for mcp_server, count in sorted_mcps:
        print(f"  {mcp_server}: {count} samples")
    
    print("="*80)
    
    # 过滤数据集，只保留涉及 common_use_MCP 的样本
    if stats['sample_indices']:
        print(f"\nFiltering dataset to keep only samples with common_use_MCP...")
        filtered_dataset = data_with_mcp.select(stats['sample_indices'])
        print(f"Filtered dataset size: {len(filtered_dataset)} samples")
        
        # 保存数据集
        if output_path:
            print(f"Saving filtered dataset to {output_path}...")
            filtered_dataset.save_to_disk(output_path)
            print(f"Dataset saved successfully!")
        else:
            # 如果没有指定输出路径，使用默认路径
            default_output_path = '/data/lhy/datasets/graph-Toucan/Toucan-single-turn-subset-common-mcp'
            print(f"Saving filtered dataset to {default_output_path}...")
            filtered_dataset.save_to_disk(default_output_path)
            print(f"Dataset saved successfully!")
        
        stats['filtered_dataset'] = filtered_dataset
    else:
        print("\nWarning: No samples found with common_use_MCP!")
        stats['filtered_dataset'] = None
    
    return stats


# 主函数
if __name__ == "__main__":
    # 对全量single turn 数据进行MCP处理
    # data = datasets.load_from_disk('/data/lhy/datasets/Toucan-SFT')
    # data = data.filter(lambda x: x['subset_name'] == 'single-turn-original')
    # add mcp field
    # tool_to_mcp = load_tool_server_mapping()
    # mcp_status_info = load_mcp_status_info()
    # output_path = '/data/lhy/datasets/graph-Toucan/Toucan-single-turn-with-mcp-field'
    # my_data = add_contained_mcp_field(data,tool_to_mcp,mcp_status_info,output_path)
    # 分析 common_use_MCP 并保存涉及 common_use_MCP 的数据集
    # output_path = '/data/lhy/datasets/graph-Toucan/Toucan-single-turn-subset-common-mcp-v1'
    # stats = analyze_common_use_mcp(output_path)
    
    # 如果需要运行原来的统计功能，取消下面的注释
    data_with_mcp = datasets.load_from_disk('/data/lhy/datasets/graph-Toucan/Toucan-single-turn-subset-common-mcp-v1')
    
    # 加载 MCP 状态信息（用于统计 stateful/stateless）
    mcp_status_info = load_mcp_status_info('mcp_status_judgment_results.json')
    
    # 打印统计信息
    print("\n" + "="*80)
    print("Statistics")
    print("="*80)
    
    # 统计有多少样本使用了 MCP
    samples_with_mcp = 0
    mcp_server_counts = defaultdict(int)
    stateful_mcp_counts = defaultdict(int)  # stateful MCP 使用次数
    stateless_mcp_counts = defaultdict(int)  # stateless MCP 使用次数
    unknown_state_mcp_counts = defaultdict(int)  # 状态未知的 MCP 使用次数
    
    # 统计样本级别的状态分布
    samples_with_stateful = 0  # 至少使用一个 stateful MCP 的样本数
    samples_with_stateless = 0  # 至少使用一个 stateless MCP 的样本数
    samples_with_both = 0  # 同时使用 stateful 和 stateless MCP 的样本数
    
    for sample in tqdm(data_with_mcp, desc="Analyzing"):
        contained_mcp_str = sample.get('contained_MCP', '{}')
        try:
            contained_mcp = json.loads(contained_mcp_str) if isinstance(contained_mcp_str, str) else contained_mcp_str
            mcp_servers = contained_mcp.get('mcp_servers', [])
            mcp_info = contained_mcp.get('mcp_info', {})
            
            if mcp_servers:
                samples_with_mcp += 1
                
                # 用于统计当前样本的状态
                has_stateful = False
                has_stateless = False
                
                for mcp_server in mcp_servers:
                    mcp_server_counts[mcp_server] += 1
                    
                    # 获取 MCP 的状态信息
                    server_info = mcp_info.get(mcp_server, {})
                    is_stateful = server_info.get('is_stateful', None)
                    
                    if is_stateful is True:
                        stateful_mcp_counts[mcp_server] += 1
                        has_stateful = True
                    elif is_stateful is False:
                        stateless_mcp_counts[mcp_server] += 1
                        has_stateless = True
                    else:
                        unknown_state_mcp_counts[mcp_server] += 1
                
                # 统计样本级别的状态
                if has_stateful and has_stateless:
                    samples_with_both += 1
                elif has_stateful:
                    samples_with_stateful += 1
                elif has_stateless:
                    samples_with_stateless += 1
        except:
            pass
    
    print(f"Total samples: {len(data_with_mcp)}")
    print(f"Samples with MCP servers: {samples_with_mcp}")
    print(f"Unique MCP servers used: {len(mcp_server_counts)}")
    
    # 状态统计
    print(f"\nMCP State Statistics:")
    print(f"  Samples with stateful MCP: {samples_with_stateful}")
    print(f"  Samples with stateless MCP: {samples_with_stateless}")
    print(f"  Samples with both stateful and stateless MCP: {samples_with_both}")
    print(f"  Stateful MCP servers: {len(stateful_mcp_counts)}")
    print(f"  Stateless MCP servers: {len(stateless_mcp_counts)}")
    print(f"  Unknown state MCP servers: {len(unknown_state_mcp_counts)}")
    
    print(f"\nMost used MCP servers (count >= 70):")
    for mcp_server, count in sorted(mcp_server_counts.items(), key=lambda x: x[1], reverse=True):
        if count >= 70:
            state_info = []
            if mcp_server in stateful_mcp_counts:
                state_info.append(f"stateful({stateful_mcp_counts[mcp_server]})")
            if mcp_server in stateless_mcp_counts:
                state_info.append(f"stateless({stateless_mcp_counts[mcp_server]})")
            if mcp_server in unknown_state_mcp_counts:
                state_info.append(f"unknown({unknown_state_mcp_counts[mcp_server]})")
            
            state_str = ", ".join(state_info) if state_info else "unknown"
            print(f"  {mcp_server}: {count} (state: {state_str})")
    print("="*80)


def sample_common_use_mcp(
    input_file='common_use_MCP.txt',
    output_file='common_use_MCP_subset.txt',
    num_samples=20,
    seed=42
):
    """
    从 common_use_MCP.txt 中随机抽样指定数量的 MCP，保存到新文件
    
    Args:
        input_file: str, 输入的 common_use_MCP.txt 文件路径
        output_file: str, 输出的子集文件路径
        num_samples: int, 要抽样的 MCP 数量
        seed: int, 随机种子
        
    Returns:
        list: 抽样后的 MCP 行列表
    """
    print(f"Loading MCPs from {input_file}...")
    all_lines = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  # 跳过空行
                all_lines.append(line)
    
    print(f"Loaded {len(all_lines)} MCPs")
    
    # 随机抽样
    random.seed(seed)
    if len(all_lines) <= num_samples:
        print(f"Total MCPs ({len(all_lines)}) <= requested samples ({num_samples}), using all MCPs")
        sampled_lines = all_lines
    else:
        sampled_lines = random.sample(all_lines, num_samples)
        print(f"Sampled {num_samples} MCPs from {len(all_lines)} total MCPs")
    
    # 保存到新文件
    print(f"Saving sampled MCPs to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in sampled_lines:
            f.write(line + '\n')
    
    print(f"Saved {len(sampled_lines)} MCPs to {output_file}")
    
    return sampled_lines
