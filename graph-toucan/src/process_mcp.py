import datasets
import json
import os
import asyncio
import logging
import time
from collections import Counter, defaultdict
from tqdm import tqdm
from openai import AsyncOpenAI
import sys
sys.path.append('/data/lhy/datasets')
from louvain_community_detection import LouvainCommunityDetection

# 初始化异步 OpenAI 客户端
async_client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 配置日志
logger = logging.getLogger("tool_classification")
logger.setLevel(logging.INFO)
if not logger.handlers:
    log_dir = os.path.dirname(__file__)
    log_path = os.path.join(log_dir, "tool_classification.log")
    handler = logging.FileHandler(log_path, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def count_unique_tool_lists(dataset):
    """
    统计数据集中有多少种不同的 tool list
    
    Args:
        dataset: HuggingFace datasets.Dataset 对象，包含 'tools' 字段
        
    Returns:
        int: 不同 tool list 的数量
        dict: 每个 tool list 及其出现次数的统计
    """
    unique_tool_lists = set()
    tool_list_counter = Counter()
    
    for example in dataset:
        if 'tools' in example and example['tools']:
            try:
                # 解析 JSON 字符串得到 list of dict
                tool_list = json.loads(example['tools'])
                
                # 将 tool list 转换为可哈希的形式（JSON 字符串）用于去重
                # 使用 sort_keys=True 确保相同内容的 dict 顺序一致
                tool_list_str = json.dumps(tool_list, sort_keys=True)
                
                unique_tool_lists.add(tool_list_str)
                tool_list_counter[tool_list_str] += 1
            except (json.JSONDecodeError, TypeError) as e:
                # 如果解析失败，跳过这条数据
                print(f"Warning: Failed to parse tools field: {e}")
                continue
    
    return len(unique_tool_lists), dict(tool_list_counter)

def get_total_tool_set(dataset):
    """
    遍历每个sample的tool list，收集所有的tool到一个集合中
    
    Args:
        dataset: HuggingFace datasets.Dataset 对象，包含 'tools' 字段
        
    Returns:
        set: 包含所有不同tool的集合（每个tool以JSON字符串形式存储）
        int: tool set的大小
    """
    total_tool_set = set()
    
    for example in dataset:
        if 'tools' in example and example['tools']:
            try:
                # 解析 JSON 字符串得到 list of dict
                tool_list = json.loads(example['tools'])
                
                # 遍历每个tool，将其添加到集合中
                for tool in tool_list:
                    # 将每个tool dict转换为可哈希的JSON字符串
                    tool_str = json.dumps(tool, sort_keys=True)
                    total_tool_set.add(tool_str)
            except (json.JSONDecodeError, TypeError) as e:
                # 如果解析失败，跳过这条数据
                print(f"Warning: Failed to parse tools field: {e}")
                continue
    
    return total_tool_set, len(total_tool_set)

def build_tool_cooccurrence_graph(dataset):
    """
    构建 tool 共现图：如果两个 tool 在同一个 sample 的 tool list 中出现，它们之间就有边
    
    Args:
        dataset: HuggingFace datasets.Dataset 对象，包含 'tools' 字段
        
    Returns:
        tuple: (tool_to_id: dict, id_to_tool: dict, adjacency_dict: dict)
            - tool_to_id: 将 tool JSON 字符串映射到整数 ID
            - id_to_tool: 将整数 ID 映射回 tool JSON 字符串
            - adjacency_dict: 图的邻接字典，格式为 {node_id: {neighbor_id: weight}}
    """
    # 首先收集所有的 tool
    total_tool_set, _ = get_total_tool_set(dataset)
    
    # 创建 tool 到 ID 的映射
    tool_to_id = {tool_str: idx for idx, tool_str in enumerate(sorted(total_tool_set))}
    id_to_tool = {idx: tool_str for tool_str, idx in tool_to_id.items()}
    
    # 初始化邻接字典
    adjacency_dict = defaultdict(lambda: defaultdict(float))
    
    # 遍历每个 sample，构建共现关系
    for example in dataset:
        if 'tools' in example and example['tools']:
            try:
                # 解析 JSON 字符串得到 list of dict
                tool_list = json.loads(example['tools'])
                
                # 将 tool list 中的每个 tool 转换为 ID
                tool_ids = []
                for tool in tool_list:
                    tool_str = json.dumps(tool, sort_keys=True)
                    if tool_str in tool_to_id:
                        tool_ids.append(tool_to_id[tool_str])
                
                # 在同一个 tool list 中的所有 tool 对之间添加边
                # 权重为共现次数（这里简单设为1，也可以累加）
                for i, tool_id_i in enumerate(tool_ids):
                    for tool_id_j in tool_ids[i+1:]:
                        # 无向图，所以两个方向都要添加
                        adjacency_dict[tool_id_i][tool_id_j] += 1.0
                        adjacency_dict[tool_id_j][tool_id_i] += 1.0
            except (json.JSONDecodeError, TypeError) as e:
                # 如果解析失败，跳过这条数据
                continue
    
    # 确保所有节点都在图中（包括孤立节点）
    for tool_id in tool_to_id.values():
        if tool_id not in adjacency_dict:
            adjacency_dict[tool_id] = {}
    
    # 转换为普通字典格式
    adjacency_dict = {node: dict(neighbors) for node, neighbors in adjacency_dict.items()}
    
    return tool_to_id, id_to_tool, adjacency_dict

def detect_tool_communities(dataset, verbose=True):
    """
    对 total_tool_set 进行社区检测，得到分类结果
    
    Args:
        dataset: HuggingFace datasets.Dataset 对象，包含 'tools' 字段
        verbose: 是否显示详细过程
        
    Returns:
        dict: 将 tool JSON 字符串映射到社区 ID 的字典
        dict: 将社区 ID 映射到该社区中所有 tool 的列表
    """
    # 构建共现图
    print("构建 tool 共现图...")
    tool_to_id, id_to_tool, adjacency_dict = build_tool_cooccurrence_graph(dataset)
    print(f"图包含 {len(adjacency_dict)} 个节点")
    
    # 运行 Louvain 社区检测算法
    print("\n运行 Louvain 社区检测算法...")
    louvain = LouvainCommunityDetection(adjacency_dict, verbose=verbose)
    communities = louvain.detect_communities()
    
    # 将结果映射回 tool
    tool_to_community = {}
    for node_id, community_id in communities.items():
        tool_str = id_to_tool[node_id]
        tool_to_community[tool_str] = community_id
    
    # 按社区分组
    community_to_tools = defaultdict(list)
    for tool_str, community_id in tool_to_community.items():
        community_to_tools[community_id].append(tool_str)
    
    return tool_to_community, dict(community_to_tools)

def filter_by_ratio(dataset, field_name, target_value, remove_ratio=0.5):
    """
    按比例剔除匹配的数据
    remove_ratio: 0.0-1.0，表示剔除匹配数据的比例
    """
    import random
    
    def ratio_filter(example, idx):
        if example[field_name] == target_value:
            # 根据索引和比例决定是否保留
            random.seed(idx)  # 确保结果可重现
            return random.random() > remove_ratio
        return True
    
    return dataset.filter(ratio_filter, with_indices=True)

# dataset = datasets.load_from_disk('/data/lhy/datasets/Toucan-SFT')
# filtered_dataset = filter_by_ratio(dataset,'subset_name','irrelevant',1)
# print(len(filtered_dataset))

# # 统计不同的 tool list 数量
# unique_count, tool_list_stats = count_unique_tool_lists(filtered_dataset)
# print(f"不同的 tool list 数量: {unique_count}")
# print(f"前10个最常见的 tool list 及其出现次数:")
# for tool_list_str, count in list(tool_list_stats.items())[:10]:
#     tool_list = json.loads(tool_list_str)
#     print(f"  Tool list with {len(tool_list)} tools: {count} 次")

def save_tool_set_to_json(total_tool_set, output_file):
    """
    将 total_tool_set 中的所有函数保存为一个 JSON 文件
    
    Args:
        total_tool_set: 包含所有不同 tool 的集合（每个 tool 以 JSON 字符串形式存储）
        output_file: 输出 JSON 文件的路径
        
    Returns:
        int: 保存的函数数量
    """
    # 将每个 JSON 字符串解析回字典（function_schema）
    function_schemas = []
    for tool_str in total_tool_set:
        try:
            function_schema = json.loads(tool_str)
            function_schemas.append(function_schema)
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse tool JSON string: {e}")
            continue
    
    # 保存为 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(function_schemas, f, indent=2, ensure_ascii=False)
    
    print(f"已保存 {len(function_schemas)} 个函数到 {output_file}")
    return len(function_schemas)

def load_classification_prompt(prompt_file):
    """
    从文件中加载分类提示词
    
    Args:
        prompt_file: 提示词文件路径
        
    Returns:
        str: 分类提示词内容
    """
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()

async def classify_function_async(function_schema):
    """
    使用 LLM 对单个 function 进行分类
    
    Args:
        function_schema: dict, function schema 字典
        
    Returns:
        tuple: (classification_result: dict, token_usage: dict)
            - classification_result: 包含 primary_label 和 custom_label 的字典
            - token_usage: token 使用统计
    """
    # 加载分类提示词
    prompt_file = os.path.join(os.path.dirname(__file__), 'Toucan-MCP-label.txt')
    classification_prompt_template = load_classification_prompt(prompt_file)
    
    # 构建完整的提示词
    prompt = f"""
    Below is some domains,I will give you a function, and you are asked to category the func based on its info into one of
    the domains. And if you think there is no proper domain to match with the func, you should based on the func description
    to give a CUSTOM_LABEL. And you can only choose one domain or give only one CUSTOM_LABEL. when you finish, you are expected
    to give a reason about your chosen label.
    {classification_prompt_template}

Function schema to classify:
{json.dumps(function_schema, indent=2, ensure_ascii=False)}

Please classify this function according to the instructions above. Your output format MUST be:
PRIMARY_LABEL: [label from predefined list or empty if using custom]
SECONDARY_LABELS: [0-2 additional relevant categories from predefined list, separated by commas, or empty if none]
CUSTOM_LABEL: [custom label if needed, or empty if using predefined]
EXPLAIN: [why you choose this label]
If using a predefined category, provide PRIMARY_LABEL and leave CUSTOM_LABEL empty.
If creating a custom label, leave PRIMARY_LABEL empty and provide CUSTOM_LABEL.
SECONDARY_LABELS should be 0-2 labels from the predefined list that are also relevant but less primary than PRIMARY_LABEL.
"""

    try:
        completion = await async_client.chat.completions.create(
            model="qwen3-235b-a22b-instruct-2507",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that classifies functions into categories."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0,
            max_completion_tokens=512
        )
        
        response_text = completion.choices[0].message.content
        
        # 解析响应
        primary_label = ""
        secondary_labels = []
        custom_label = ""
        explain = ""
        lines = response_text.split('\n')
        for line in lines:
            line_upper = line.upper().strip()
            if line_upper.startswith('PRIMARY_LABEL:'):
                primary_label = line.split(':', 1)[1].strip() if ':' in line else ""
            elif line_upper.startswith('SECONDARY_LABELS:'):
                secondary_str = line.split(':', 1)[1].strip() if ':' in line else ""
                if secondary_str:
                    # 解析 secondary labels，支持逗号分隔
                    secondary_labels = [label.strip() for label in secondary_str.split(',') if label.strip()]
            elif line_upper.startswith('CUSTOM_LABEL:'):
                custom_label = line.split(':', 1)[1].strip() if ':' in line else ""
            elif line_upper.startswith('EXPLAIN'):
                explain = line.split(':', 1)[1].strip() if ':' in line else ""
        classification_result = {
            'primary_label': primary_label,
            'secondary_labels': secondary_labels,
            'custom_label': custom_label,
            'explain': explain
        }
        
        token_usage = {
            'prompt_tokens': completion.usage.prompt_tokens,
            'completion_tokens': completion.usage.completion_tokens,
            'total_tokens': completion.usage.total_tokens
        }
        
        return classification_result, token_usage
        
    except Exception as e:
        logger.error(f"Error classifying function: {str(e)}")
        logger.error(f"Function schema: {json.dumps(function_schema, ensure_ascii=False)[:200]}")
        raise

async def classify_functions_batch(function_schemas, batch_size=10):
    """
    批量对 function schemas 进行分类
    
    Args:
        function_schemas: list of dict, function schema 列表
        batch_size: int, 每批处理的函数数量
        
    Returns:
        tuple: (results: list, token_stats: dict, failed_samples: list)
            - results: list of dict, 每个元素包含 function_schema 和 classification_result
            - token_stats: dict, token 使用统计
            - failed_samples: list, 失败的样本信息
    """
    results = []
    failed_samples = []
    all_batch_results = []
    total_batches = (len(function_schemas) + batch_size - 1) // batch_size
    start_total_time = time.time()
    
    batch_iterator = tqdm(
        range(0, len(function_schemas), batch_size),
        total=total_batches if total_batches else None,
        desc="Classifying functions",
        unit="batch"
    )
    
    for i in batch_iterator:
        batch = function_schemas[i:i+batch_size]
        batch_num = i // batch_size + 1
        
        batch_start_time = time.time()
        batch_iterator.set_postfix_str(f"size={len(batch)}")
        
        # 创建异步任务
        tasks = [classify_function_async(func_schema) for func_schema in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        batch_end_time = time.time()
        batch_duration = batch_end_time - batch_start_time
        
        # 处理结果
        for idx, result in enumerate(batch_results):
            sample_index = i + idx
            if isinstance(result, Exception):
                error_msg = str(result)
                log_msg = f"Error classifying function {sample_index} (batch {batch_num}): {error_msg}"
                tqdm.write(f"  {log_msg}")
                logger.error(log_msg)
                failed_samples.append({
                    'batch_index': batch_num,
                    'sample_index': sample_index,
                    'error': error_msg,
                    'function_schema': batch[idx] if idx < len(batch) else None
                })
                all_batch_results.append(result)
                continue
            
            classification_result, token_usage = result
            results.append({
                'function_schema': batch[idx],
                'classification': classification_result
            })
            all_batch_results.append((classification_result, token_usage))

        batch_iterator.set_postfix_str(f"size={len(batch)}, time={batch_duration:.2f}s")
    
    batch_iterator.close()
    
    # 计算总时间
    total_duration = time.time() - start_total_time
    avg_batch_time = total_duration / total_batches if total_batches > 0 else 0
    print(f"\nTotal classification time: {total_duration:.2f}s")
    print(f"Average batch time: {avg_batch_time:.2f}s")
    
    # 计算 token 统计
    successful_results = [r for r in all_batch_results if not isinstance(r, Exception)]
    if successful_results:
        total_prompt_tokens = sum(t[1]['prompt_tokens'] for t in successful_results)
        total_completion_tokens = sum(t[1]['completion_tokens'] for t in successful_results)
        total_tokens = sum(t[1]['total_tokens'] for t in successful_results)
        num_successful = len(successful_results)
        
        token_stats = {
            'successful_samples': num_successful,
            'failed_samples': len(failed_samples),
            'avg_prompt_tokens': total_prompt_tokens / num_successful,
            'avg_completion_tokens': total_completion_tokens / num_successful,
            'avg_total_tokens': total_tokens / num_successful,
            'total_prompt_tokens': total_prompt_tokens,
            'total_completion_tokens': total_completion_tokens,
            'total_tokens': total_tokens
        }
    else:
        token_stats = {
            'successful_samples': 0,
            'failed_samples': len(failed_samples),
            'avg_prompt_tokens': 0,
            'avg_completion_tokens': 0,
            'avg_total_tokens': 0,
            'total_prompt_tokens': 0,
            'total_completion_tokens': 0,
            'total_tokens': 0
        }
    
    return results, token_stats, failed_samples

async def classify_tool_set_from_json(json_file, output_file=None, batch_size=10):
    """
    从 JSON 文件读取 function schemas，进行分类，并保存结果
    
    Args:
        json_file: str, 包含 function schemas 的 JSON 文件路径
        output_file: str, 可选，输出分类结果的 JSON 文件路径
        batch_size: int, 批处理大小
        
    Returns:
        tuple: (results: list, token_stats: dict, failed_samples: list)
    """
    # 读取 function schemas
    print(f"Loading function schemas from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        function_schemas = json.load(f)
    
    print(f"Found {len(function_schemas)} functions to classify")
    
    # 批量分类
    results, token_stats, failed_samples = await classify_functions_batch(
        function_schemas, batch_size=batch_size
    )
    
    # 打印统计信息
    print(f"\n成功分类: {len(results)}/{len(function_schemas)}")
    print(f"失败: {len(failed_samples)}")
    print(f"\nToken 使用统计:")
    print(f"  成功样本数: {token_stats['successful_samples']}")
    print(f"  平均 prompt tokens: {token_stats['avg_prompt_tokens']:.2f}")
    print(f"  平均 completion tokens: {token_stats['avg_completion_tokens']:.2f}")
    print(f"  平均 total tokens: {token_stats['avg_total_tokens']:.2f}")
    print(f"  总 prompt tokens: {token_stats['total_prompt_tokens']}")
    print(f"  总 completion tokens: {token_stats['total_completion_tokens']}")
    print(f"  总 tokens: {token_stats['total_tokens']}")
    
    # 保存结果
    if output_file:
        print(f"\n保存分类结果到 {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"已保存 {len(results)} 个分类结果")
    
    return results, token_stats, failed_samples

def count_classification_categories(classification_results_file):
    """
    统计分类结果中每个类别的函数数量
    
    Args:
        classification_results_file: str, 分类结果 JSON 文件路径
        
    Returns:
        dict: 包含统计信息的字典
            - primary_labels: dict, 每个 primary_label 及其数量
            - custom_labels: dict, 每个 custom_label 及其数量
            - total_functions: int, 总函数数
            - empty_labels: int, 空标签的数量
    """
    # 读取分类结果
    with open(classification_results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    # 统计各类别
    primary_label_counter = Counter()
    custom_label_counter = Counter()
    empty_labels_count = 0
    
    for result in results:
        classification = result.get('classification', {})
        primary_label = classification.get('primary_label', '').strip()
        custom_label = classification.get('custom_label', '').strip()
        
        if primary_label:
            primary_label_counter[primary_label] += 1
        elif custom_label:
            custom_label_counter[custom_label] += 1
        else:
            empty_labels_count += 1
    
    stats = {
        'primary_labels': dict(primary_label_counter),
        'custom_labels': dict(custom_label_counter),
        'total_functions': len(results),
        'empty_labels': empty_labels_count,
        'total_primary_labels': len(primary_label_counter),
        'total_custom_labels': len(custom_label_counter)
    }
    
    return stats
# 把属于一个label的func先统计出来，作为一个fun的candidate，这是baseline版本，只统计primary label,然后对于每个函数，设定其candidates为和其有一个label重合的func，统计每一个func的candidates的数量分布。
def print_classification_statistics(classification_results_file):
    """
    打印分类结果的统计信息，并统计每个函数的 candidates 数量分布
    
    Args:
        classification_results_file: str, 分类结果 JSON 文件路径
    """
    # 读取分类结果
    with open(classification_results_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    
    total_functions = len(results)
    
    # 收集函数信息
    function_to_primary_label = {}  # Baseline: 只存储 primary label
    function_to_all_labels = {}  # 当前版本: 存储所有 labels (primary + secondary)
    
    for idx, result in enumerate(results):
        function_schema = result.get('function_schema', {})
        function_info = function_schema.get('function', {})
        function_name = function_info.get('name', f'function_{idx}')
        
        classification = result.get('classification', {})
        primary_label = classification.get('primary_label', '').strip()
        secondary_labels = classification.get('secondary_labels', [])
        
        # Baseline: 只存储 primary label
        if primary_label:
            function_to_primary_label[function_name] = primary_label
        
        # 当前版本: 收集所有 labels (primary + secondary)
        all_labels = set()
        if primary_label:
            all_labels.add(primary_label)
        for sec_label in secondary_labels:
            if sec_label and sec_label.strip():
                all_labels.add(sec_label.strip())
        
        function_to_all_labels[function_name] = all_labels
    
    # Baseline版本: 只考虑 primary label，计算每个函数的 candidates
    baseline_candidates_count = {}
    function_names = list(function_to_primary_label.keys())
    
    for func_name in function_names:
        func_primary_label = function_to_primary_label[func_name]
        candidates = set()
        
        # 遍历所有其他函数，检查是否有相同的 primary label
        for other_func_name, other_primary_label in function_to_primary_label.items():
            if other_func_name == func_name:
                continue
            
            # 如果有相同的 primary label，则加入 candidates
            if func_primary_label == other_primary_label:
                candidates.add(other_func_name)
        
        baseline_candidates_count[func_name] = len(candidates)
    
    # 当前版本: 考虑 primary + secondary labels，计算每个函数的 candidates
    current_candidates_count = {}
    
    for func_name in function_names:
        func_labels = function_to_all_labels[func_name]
        candidates = set()
        
        # 遍历所有其他函数，检查是否有 label 重合
        for other_func_name, other_labels in function_to_all_labels.items():
            if other_func_name == func_name:
                continue
            
            # 如果有至少一个 label 重合，则加入 candidates
            if func_labels & other_labels:  # 集合交集
                candidates.add(other_func_name)
        
        current_candidates_count[func_name] = len(candidates)
    
    # 统计 candidates 数量分布
    baseline_distribution = Counter(baseline_candidates_count.values())
    current_distribution = Counter(current_candidates_count.values())
    
    # 打印统计信息
    print("\n" + "="*80)
    print("分类结果统计")
    print("="*80)
    print(f"总函数数: {total_functions}")
    
    # Baseline 版本统计摘要
    baseline_values = list(baseline_candidates_count.values())
    baseline_avg = sum(baseline_values) / total_functions if total_functions > 0 else 0
    baseline_max = max(baseline_values) if baseline_values else 0
    baseline_min = min(baseline_values) if baseline_values else 0
    sorted_baseline = sorted(baseline_values)
    if total_functions > 0:
        if total_functions % 2 == 0:
            baseline_median = (sorted_baseline[total_functions//2 - 1] + sorted_baseline[total_functions//2]) / 2
        else:
            baseline_median = sorted_baseline[total_functions//2]
    else:
        baseline_median = 0
    
    # 当前版本统计摘要
    current_values = list(current_candidates_count.values())
    current_avg = sum(current_values) / total_functions if total_functions > 0 else 0
    current_max = max(current_values) if current_values else 0
    current_min = min(current_values) if current_values else 0
    sorted_current = sorted(current_values)
    if total_functions > 0:
        if total_functions % 2 == 0:
            current_median = (sorted_current[total_functions//2 - 1] + sorted_current[total_functions//2]) / 2
        else:
            current_median = sorted_current[total_functions//2]
    else:
        current_median = 0
    
    print("\n" + "-"*80)
    print("Baseline: Candidates 数量分布统计 (仅考虑 Primary Label)")
    print("-"*80)
    print("说明: 每个函数的 candidates = 与其有相同 primary label 的其他函数")
    print(f"\n{'Candidates数量':<20} {'函数数量':<15} {'占比':<15}")
    print("-" * 50)
    
    sorted_baseline_dist = sorted(baseline_distribution.items())
    for candidates_count, func_count in sorted_baseline_dist:
        percentage = (func_count / total_functions) * 100
        print(f"  {candidates_count:<20} {func_count:<15} {percentage:>6.2f}%")
    
    print("\n" + "-"*80)
    print("Baseline: Candidates 统计摘要")
    print("-"*80)
    print(f"  平均 candidates 数量: {baseline_avg:.2f}")
    print(f"  最大 candidates 数量: {baseline_max}")
    print(f"  最小 candidates 数量: {baseline_min}")
    print(f"  中位数 candidates 数量: {baseline_median:.2f}")
    
    print("\n" + "-"*80)
    print("当前版本: Candidates 数量分布统计 (考虑 Primary + Secondary Labels)")
    print("-"*80)
    print("说明: 每个函数的 candidates = 与其有至少一个相同 label (primary 或 secondary) 的其他函数")
    print(f"\n{'Candidates数量':<20} {'函数数量':<15} {'占比':<15}")
    print("-" * 50)
    
    sorted_current_dist = sorted(current_distribution.items())
    for candidates_count, func_count in sorted_current_dist:
        percentage = (func_count / total_functions) * 100
        print(f"  {candidates_count:<20} {func_count:<15} {percentage:>6.2f}%")
    
    print("\n" + "-"*80)
    print("当前版本: Candidates 统计摘要")
    print("-"*80)
    print(f"  平均 candidates 数量: {current_avg:.2f}")
    print(f"  最大 candidates 数量: {current_max}")
    print(f"  最小 candidates 数量: {current_min}")
    print(f"  中位数 candidates 数量: {current_median:.2f}")
    
    print("\n" + "-"*80)
    print("对比分析")
    print("-"*80)
    avg_increase = current_avg - baseline_avg
    avg_increase_pct = (avg_increase / baseline_avg * 100) if baseline_avg > 0 else 0
    median_increase = current_median - baseline_median
    median_increase_pct = (median_increase / baseline_median * 100) if baseline_median > 0 else 0
    print(f"  平均 candidates 数量提升: {avg_increase:.2f} ({avg_increase_pct:.2f}%)")
    print(f"  中位数 candidates 数量提升: {median_increase:.2f} ({median_increase_pct:.2f}%)")
    
    print("="*80 + "\n")
    
    return {
        'baseline_candidates_count': baseline_candidates_count,
        'baseline_distribution': dict(baseline_distribution),
        'baseline_avg': baseline_avg,
        'baseline_max': baseline_max,
        'baseline_min': baseline_min,
        'baseline_median': baseline_median,
        'current_candidates_count': current_candidates_count,
        'current_distribution': dict(current_distribution),
        'current_avg': current_avg,
        'current_max': current_max,
        'current_min': current_min,
        'current_median': current_median
    }




# 如果需要运行分类，取消下面的注释
if __name__ == "__main__":
    #asyncio.run(classify_tool_set_from_json('tool_schema.json', 'tool_classification_results_v1.json', batch_size=10))
    print_classification_statistics('tool_classification_results_v1.json')