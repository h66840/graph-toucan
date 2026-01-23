# v1.0.0
# 从tool_classification_results_v1.json的tool里抽样300个tool作为node,然后使用primary + secendary labels存在重合作为候选candidates方法，得到每个node的
# possible candidates集合，然后随机抽样30个作为candidate list,然后调用openai API，根据target func 的input 是否依赖于 node function 的output，比如 node function output的一部分 可以作为target func 的 部分 or完全 input，如果node function 的output能作为target func执行的前提，也可以作为edge。比如node function是检查文件是否存在，target function是下载文件，那么node function determined we can whether call target function, 来建立有向edge，从而得到graph v1.0.0
# v1.0.1 改进一下选择候选candidates的方法，从primary labels是否相等判断是否为candidates，如果node function的candidates不足30，则接下来找node function的secondary label和其余函数的primary labels是否重合，如果还不到30个candidates，则用node function 的secondary label和其余函数的secondary labels是否重合来增加candidates。
import json
import os
import random
import asyncio
import yaml
from collections import Counter, defaultdict
from typing import Any, Dict, List, Set, Tuple
from tqdm import tqdm
from openai import AsyncOpenAI
import matplotlib.pyplot as plt
import networkx as nx

# 配置文件路径
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


def load_tools_with_output_schema(schema_file: str) -> Tuple[Set[str], List[Dict]]:
    """
    从 tool_response_schema.json 中加载已经设计好 output schema 的 tool 集合。

    预期文件结构：
    {
        "tool_name_1": { "tool_name": "...", "output_schema_parsed": {...}, ... },
        "tool_name_2": { ... },
        ...
    }
    """
    print(f"Loading tools with output schema from {schema_file}...")
    with open(schema_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    sub_data = []
    tool_names: set[str] = set()
    for key, value in data.items():
        # 以 key 为准，兜底再看看内部的 tool_name
        if not value.get('output_schema_parsed'):
            continue
        sub_data.append(value)
        if isinstance(key, str) and key:
            tool_names.add(key)
            continue
        inner_name = ""
        if isinstance(value, dict):
            inner_name = value.get("tool_name", "") or ""
        if inner_name:
            tool_names.add(inner_name)

    print(f"Loaded {len(tool_names)} tools with designed output schema.")
    return tool_names,sub_data


def load_common_use_mcp_servers(txt_file='common_use_MCP.txt'):
    """
    从 common_use_MCP.txt 文件中加载 common_use_MCP server 列表
    
    Args:
        txt_file: str, common_use_MCP.txt 文件路径
        
    Returns:
        set: common_use_MCP server 名称的集合
    """
    print(f"Loading common_use_MCP servers from {txt_file}...")
    common_mcp_set = set()
    
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # 格式: "0059.@smithery-ai_national-weather-service_labeled.json: 859 (state: stateless(859))"
            # 提取冒号前的部分作为 MCP server 名称
            if ':' in line:
                mcp_server = line.split(':', 1)[0].strip()
                common_mcp_set.add(mcp_server)
            else:
                # 如果没有冒号，整行作为 MCP server 名称
                common_mcp_set.add(line)
    
    print(f"Loaded {len(common_mcp_set)} common_use_MCP servers")
    return common_mcp_set


def get_tools_from_common_use_mcp(
    common_use_mcp_file: str = 'common_use_MCP.txt',
    tool_with_server_file: str = 'tool_with_server.json',
    classification_file: str = 'tool_classification_results_v1.json',
):
    """
    从 common_use_MCP.txt 获取对应的 tools 列表
    
    Args:
        common_use_mcp_file: str, common_use_MCP.txt 文件路径
        tool_with_server_file: str, tool_with_server.json 文件路径
        
    Returns:
        list: 包含所有 common_use_MCP 对应的 tools 的列表
           每个 tool 包含完整的 function_schema、classification、mcp_server 等信息，
           其中 classification 来自 tool_classification_results_v1.json（更准确）
    """
    # 1. 加载 common_use_MCP server 列表
    common_mcp_servers = load_common_use_mcp_servers(common_use_mcp_file)
    # 2. 加载 tool_with_server.json
    print(f"Loading tools from {tool_with_server_file}...")
    with open(tool_with_server_file, 'r', encoding='utf-8') as f:
        all_tools = json.load(f)
    print(f"Loaded {len(all_tools)} tools from {tool_with_server_file}")

    # 2.1 加载更准确的分类结果，用于覆盖每个 tool 的 classification
    print(f"Loading accurate classifications from {classification_file}...")
    classification_results = load_tool_classification_results(classification_file)
    print(f"Loaded {len(classification_results)} classification entries")

    # 构建 name -> classification 的映射
    name_to_classification: dict[str, dict] = {}
    for item in classification_results:
        func_schema = item.get("function_schema", {})
        func = func_schema.get("function", {})
        name = func.get("name", "")
        if name:
            name_to_classification[name] = item.get("classification", {}) or {}
    
    # 3. 找到所有属于 common_use_MCP 的 tools
    common_mcp_tools = []
    mcp_to_tools = defaultdict(list)  # 用于统计每个 MCP server 对应的 tools 数量
    
    for tool in tqdm(all_tools, desc="Filtering tools by common_use_MCP"):
        mcp_server = tool.get('mcp_server', '')
        if mcp_server in common_mcp_servers:
            # 用 tool_classification_results_v1.json 中的 classification 覆盖原有标签
            func_schema = tool.get("function_schema", {}).get("function", {})
            tool_name = func_schema.get("name", "")
            if tool_name and tool_name in name_to_classification:
                tool["classification"] = name_to_classification[tool_name]

            common_mcp_tools.append(tool)
            mcp_to_tools[mcp_server].append(tool)
    
    print(f"\nFound {len(common_mcp_tools)} tools from {len(common_mcp_servers)} common_use_MCP servers")
    
    # 打印统计信息
    print("\n" + "="*80)
    print("Tools per MCP Server")
    print("="*80)
    for mcp_server in sorted(common_mcp_servers):
        tool_count = len(mcp_to_tools[mcp_server])
        if tool_count > 0:
            print(f"  {mcp_server}: {tool_count} tools")
        else:
            print(f"  {mcp_server}: 0 tools (WARNING: No tools found!)")
    print("="*80)
    
    return common_mcp_tools


def load_tool_classification_results(json_file):
    """
    加载工具分类结果
    
    Args:
        json_file: str, JSON 文件路径
        
    Returns:
        list: 工具分类结果列表
    """
    print(f"Loading tool classification results from {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        results = json.load(f)
    print(f"Loaded {len(results)} tools")
    return results


def sample_nodes(results, num_nodes=300, seed=42):
    """
    从结果中抽样指定数量的节点
    
    Args:
        results: list, 工具分类结果列表
        num_nodes: int, 要抽样的节点数量
        seed: int, 随机种子
        
    Returns:
        list: 抽样后的节点列表
    """
    random.seed(seed)
    if len(results) <= num_nodes:
        print(f"Total tools ({len(results)}) <= requested nodes ({num_nodes}), using all tools")
        return results
    
    sampled = random.sample(results, num_nodes)
    print(f"Sampled {len(sampled)} nodes from {len(results)} tools")
    return sampled


def get_function_labels(classification):
    """
    获取函数的所有 labels (primary + secondary)
    
    Args:
        classification: dict, 分类结果
        
    Returns:
        set: labels 集合
    """
    labels = set()
    primary_label = classification.get('primary_label', '').strip()
    secondary_labels = classification.get('secondary_labels', [])
    
    if primary_label:
        labels.add(primary_label)
    
    for sec_label in secondary_labels:
        if sec_label and sec_label.strip():
            labels.add(sec_label.strip())
    
    return labels


def find_candidates_for_nodes_raw(nodes, max_candidates: int | None = None):
    """
    为每个节点找到可能的 candidates（raw 版本）
    
    规则：直接遍历两个函数的所有 labels（primary + secondary），
    只要找到 label 重合，就算 node 的 candidate。
    
    Args:
        nodes: list, 节点列表
        max_candidates: int | None, 每个节点最多保留的 candidates 数量，None 表示不限制
        
    Returns:
        dict: {node_index: [candidate_indices]}
    """
    print("Finding candidates for each node using raw label matching...")
    
    # 收集每个节点的所有 labels
    node_labels = []
    for node in nodes:
        classification = node.get("classification", {})
        labels = get_function_labels(classification)
        node_labels.append(labels)
    
    num_nodes = len(nodes)
    node_candidates = {}
    
    for i in tqdm(range(num_nodes), desc="Finding candidates (raw)"):
        labels_i = node_labels[i]
        candidates: list[int] = []
        
        # 遍历所有其他节点，检查 labels 是否有交集
        for j in range(num_nodes):
            if j == i:
                continue
            labels_j = node_labels[j]
            # 如果有 label 重合，就加入 candidates
            if labels_i & labels_j:  # 集合交集不为空
                candidates.append(j)
        
        # 如果设置了 max_candidates，则截断
        if max_candidates is not None and len(candidates) > max_candidates:
            candidates = candidates[:max_candidates]
        
        node_candidates[i] = candidates
    
    # 统计信息
    candidate_counts = [len(cands) for cands in node_candidates.values()]
    if candidate_counts:
        avg_cands = sum(candidate_counts) / len(candidate_counts)
        print(f"Average candidates per node (raw): {avg_cands:.2f}")
        print(f"Max candidates: {max(candidate_counts)}")
        print(f"Min candidates: {min(candidate_counts)}")
        if max_candidates is not None:
            print(f"Max candidates limit: {max_candidates}")
    
    return node_candidates


def find_candidates_for_nodes(nodes, min_candidates: int = 30):
    """
    为每个节点找到可能的 candidates（v1.0.1 规则）
    
    v1.0.1 规则：
    1) 先根据 primary label 是否相等作为 candidates
    2) 如果不足 min_candidates，再用「node 的 secondary label 与其他函数的 primary label 重合」补充
    3) 如果还不足，再用「node 的 secondary label 与其他函数的 secondary label 重合」补充
    
    Args:
        nodes: list, 节点列表
        min_candidates: int, 希望至少得到的候选数量（用于统计；真正使用时仍会在 sample 阶段截断为固定数量）
        
    Returns:
        dict: {node_index: [candidate_indices]}
    """
    print("Finding candidates for each node using v1.0.1 rules...")
    
    # 收集每个节点的 primary / secondary labels
    primary_labels = []
    secondary_label_sets = []
    for node in nodes:
        classification = node.get("classification", {})
        primary = classification.get("primary_label", "").strip()
        secondary_list = classification.get("secondary_labels", []) or []
        secondary_set = {s.strip() for s in secondary_list if s and s.strip()}
        primary_labels.append(primary)
        secondary_label_sets.append(secondary_set)
    
    num_nodes = len(nodes)
    node_candidates = {}
    # 记录不同来源的 candidates，便于统计和打印
    primary_only_candidates = {}
    sec_with_primary_candidates = {}
    sec_with_sec_candidates = {}
    
    for i in tqdm(range(num_nodes), desc="Finding candidates"):
        primary_i = primary_labels[i]
        secondary_i = secondary_label_sets[i]
        candidates: list[int] = []
        used = set()
        primary_list: list[int] = []
        sec_primary_list: list[int] = []
        sec_sec_list: list[int] = []
        
        # 1) primary label 相等
        if primary_i:
            for j in range(num_nodes):
                if j == i:
                    continue
                if primary_labels[j] == primary_i:
                    candidates.append(j)
                    used.add(j)
                    primary_list.append(j)
        
        # 2) node 的 secondary label 与其他函数的 primary label 重合
        if len(candidates) < min_candidates and secondary_i:
            for j in range(num_nodes):
                if j == i or j in used:
                    continue
                primary_j = primary_labels[j]
                if primary_j and primary_j in secondary_i:
                    candidates.append(j)
                    used.add(j)
                    sec_primary_list.append(j)
                    if len(candidates) >= min_candidates:
                        break
        
        # 3) node 的 secondary label 与其他函数的 secondary label 重合
        if len(candidates) < min_candidates and secondary_i:
            for j in range(num_nodes):
                if j == i or j in used:
                    continue
                secondary_j = secondary_label_sets[j]
                if secondary_j and (secondary_i & secondary_j):
                    candidates.append(j)
                    used.add(j)
                    sec_sec_list.append(j)
                    if len(candidates) >= min_candidates:
                        break

        # 4) 如果仍不足 min_candidates，则从剩余函数中随机补充
        if len(candidates) < min_candidates:
            remaining_indices = [
                j for j in range(num_nodes)
                if j != i and j not in used
            ]
            needed = min_candidates - len(candidates)
            if remaining_indices and needed > 0:
                extra = random.sample(remaining_indices, min(needed, len(remaining_indices)))
                candidates.extend(extra)
                # 不归入三种语义来源，只作为随机补充
                used.update(extra)
        
        node_candidates[i] = candidates
        primary_only_candidates[i] = primary_list
        sec_with_primary_candidates[i] = sec_primary_list
        sec_with_sec_candidates[i] = sec_sec_list
    
    # 统计信息
    candidate_counts = [len(cands) for cands in node_candidates.values()]
    if candidate_counts:
        avg_cands = sum(candidate_counts) / len(candidate_counts)
        print(f"Average candidates per node (v1.0.1): {avg_cands:.2f}")
        print(f"Max candidates: {max(candidate_counts)}")
        print(f"Min candidates: {min(candidate_counts)}")
    else:
        print("No candidates found.")

    # 打印不同来源的 candidates 统计
    print("\n" + "-" * 80)
    print("Candidate source statistics (per node)")
    print("-" * 80)
    primary_counts = [len(v) for v in primary_only_candidates.values()]
    sec_primary_counts = [len(v) for v in sec_with_primary_candidates.values()]
    sec_sec_counts = [len(v) for v in sec_with_sec_candidates.values()]
    if primary_counts:
        print(f"  From same primary_label:")
        print(f"    Avg: {sum(primary_counts)/len(primary_counts):.2f}, "
              f"Max: {max(primary_counts)}, Min: {min(primary_counts)}")
    if sec_primary_counts:
        print(f"  From secondary_label with other primary_label:")
        print(f"    Avg: {sum(sec_primary_counts)/len(sec_primary_counts):.2f}, "
              f"Max: {max(sec_primary_counts)}, Min: {min(sec_primary_counts)}")
    if sec_sec_counts:
        print(f"  From secondary_label with other secondary_label:")
        print(f"    Avg: {sum(sec_sec_counts)/len(sec_sec_counts):.2f}, "
              f"Max: {max(sec_sec_counts)}, Min: {min(sec_sec_counts)}")

    # 对候选集做一次 candidate pairs 去重分析
    analyze_candidate_pairs(node_candidates, label="after candidate mining")

    return node_candidates


def analyze_candidate_pairs(node_candidates: dict[int, list[int]], label: str = ""):
    """
    对 candidate pairs 做去重分析并打印统计信息。
    
    注意：这里的 pair 去重是“无序”的，即 (i, j) 和 (j, i) 视为同一个 pair。
    """
    total_pairs = sum(len(cands) for cands in node_candidates.values())
    unique_pairs = set()
    for src_idx, cand_list in node_candidates.items():
        for tgt_idx in cand_list:
            # 无序 pair：把 (src, tgt) 和 (tgt, src) 视为同一个
            if src_idx == tgt_idx:
                # 自环边就按一个点算
                key = frozenset({src_idx})
            else:
                key = frozenset({src_idx, tgt_idx})
            unique_pairs.add(key)

    num_unique = len(unique_pairs)
    num_duplicates = total_pairs - num_unique

    prefix = f"[{label}] " if label else ""
    print("\n" + "-" * 80)
    print(f"{prefix}Candidate pairs dedup analysis (order-insensitive)")
    print("-" * 80)
    print(f"{prefix}Total candidate pairs (with duplicates): {total_pairs}")
    print(f"{prefix}Unique unordered candidate pairs: {num_unique}")
    print(f"{prefix}Duplicate candidate pairs: {num_duplicates}")
    if total_pairs > 0:
        print(f"{prefix}Duplicate ratio: {num_duplicates / total_pairs * 100:.4f}%")
    print("-" * 80 + "\n")


def sample_candidates(node_candidates, num_candidates=30, seed=42):
    """
    为每个节点随机抽样指定数量的 candidates
    
    Args:
        node_candidates: dict, {node_index: [candidate_indices]}
        num_candidates: int, 每个节点要抽样的 candidates 数量
        seed: int, 随机种子
        
    Returns:
        dict: {node_index: [sampled_candidate_indices]}
    """
    random.seed(seed)
    sampled_candidates = {}
    
    for node_idx, candidates in node_candidates.items():
        if len(candidates) <= num_candidates:
            sampled_candidates[node_idx] = candidates
        else:
            sampled_candidates[node_idx] = random.sample(candidates, num_candidates)
    
    print(f"Sampled {num_candidates} candidates per node (or all if less)")

    # 对采样后的 candidate pairs 做一次去重分析
    analyze_candidate_pairs(sampled_candidates, label=f"after sampling top-{num_candidates}")

    return sampled_candidates


async def filter_output_params_async(node_name: str, node_params: Dict, node_output_schema: Dict) -> Dict:
    """
    过滤掉 node function 输出参数中的"pass-through"参数

    过滤规则：
    1. 如果某个输出参数的名称与输入参数的名称相同，则过滤掉（代码逻辑判断）
    2. 如果某个输出参数的描述与输入参数的描述语义相同，则过滤掉（LLM判断）

    Args:
        node_name: str, node function 的名称
        node_params: dict, node function 的输入参数 schema
        node_output_schema: dict, node function 的输出参数 schema

    Returns:
        dict: 过滤后的输出参数 schema
    """
    if not node_output_schema or 'fields' not in node_output_schema:
        return node_output_schema

    # 获取输入参数的名称集合
    input_param_names = set()
    input_params_list = []

    if 'properties' in node_params:
        for param_name, param_info in node_params['properties'].items():
            input_param_names.add(param_name.lower())
            input_params_list.append({
                'name': param_name,
                'description': param_info.get('description', ''),
                'type': param_info.get('type', '')
            })

    # 第一步：过滤名称相同的参数
    after_name_filter = []
    original_fields = node_output_schema['fields']

    for output_field in original_fields:
        output_param_name = output_field.get('name', '')
        output_name_lower = output_param_name.lower()

        # 规则1: 检查名称是否重复
        if output_name_lower not in input_param_names:
            after_name_filter.append(output_field)

    # 如果第一步过滤后没有剩余参数，直接返回
    if not after_name_filter:
        filtered_output = node_output_schema.copy()
        filtered_output['fields'] = []
        return filtered_output

    # 第二步：使用 LLM 判断语义相同的参数
    output_params_list = []
    for field in after_name_filter:
        output_params_list.append({
            'name': field.get('name', ''),
            'description': field.get('description', ''),
            'type': field.get('type', '')
        })

    prompt = f"""You are an expert at analyzing function parameter semantics.

Function Name: {node_name}

Input Parameters:
{json.dumps(input_params_list, indent=2, ensure_ascii=False)}

Output Parameters (after name filtering):
{json.dumps(output_params_list, indent=2, ensure_ascii=False)}

Your task is to identify which output parameters have the similar or related description with any input parameters or express similar attribute or meaning , even if their names are different. 

Output format: A JSON object with two fields:
1. "filtered_params": A JSON array of parameter names that should be filtered out
2. "reasoning": Your reasoning process explaining which parameters should be filtered and why, or why none should be filtered


Your output (JSON object only):"""

    try:
        completion = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert at analyzing parameter semantics. Always respond with a JSON object containing 'filtered_params' array and 'reasoning' string."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.7,
            max_completion_tokens=512
        )

        response_text = completion.choices[0].message.content.strip()

        # 清理可能的 markdown 代码块标记
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        # 解析 LLM 返回的结果
        try:
            result = json.loads(response_text)
            params_to_filter = result.get('filtered_params', [])
            filter_reasoning = result.get('reasoning', 'No reasoning provided')

            if not isinstance(params_to_filter, list):
                params_to_filter = []
        except json.JSONDecodeError:
            print(f"Warning: Failed to parse filter params from LLM: {response_text}")
            params_to_filter = []
            filter_reasoning = f"Parse error: {response_text[:100]}"

        # 第三步：应用语义过滤
        final_filtered = []
        params_to_filter_lower = {p.lower() for p in params_to_filter}

        for field in after_name_filter:
            field_name = field.get('name', '')
            if field_name.lower() not in params_to_filter_lower:
                final_filtered.append(field)

        filtered_output = node_output_schema.copy()
        filtered_output['fields'] = final_filtered
        # 添加过滤推理信息，用于调试和分析
        filtered_output['filter_reasoning'] = filter_reasoning
        filtered_output['filtered_param_names'] = params_to_filter

        return filtered_output

    except Exception as e:
        print(f"Warning: Error in semantic filtering, using name-filtered result: {e}")
        filtered_output = node_output_schema.copy()
        filtered_output['fields'] = after_name_filter
        filtered_output['filter_reasoning'] = f"Error occurred: {str(e)}"
        filtered_output['filtered_param_names'] = []
        return filtered_output


async def judge_edge_async(node_func, candidate_func):
    """
    使用 LLM 判断是否应该建立从 node_func 到 candidate_func 的有向边

    Args:
        node_func: dict, 源函数（node function）
        candidate_func: dict, 目标函数（candidate function）

    Returns:
        dict: 包含判断结果的字典
            - has_edge: bool, 是否应该有边
            - confidence: float, 置信度
            - reasoning: str, 判断理由
            - dependency_type: str, 依赖类型（full/partial/prerequisite/none）
            - param_mapping: dict, 参数映射关系（对于 data dependency）
    """
    node_schema = node_func.get('function_schema', {}).get('function', {})
    candidate_schema = candidate_func.get('function_schema', {}).get('function', {})

    node_name = node_schema.get('name', 'Unknown')
    node_desc = node_schema.get('description', '')
    node_params = node_schema.get('parameters', {})
    node_output_schema = node_func.get('output_schema',{})
    candidate_name = candidate_schema.get('name', 'Unknown')
    candidate_desc = candidate_schema.get('description', '')
    candidate_params = candidate_schema.get('parameters', {})

    # 先过滤输出参数
    filtered_output_schema = await filter_output_params_async(node_name, node_params, node_output_schema)

    # 构建只包含 fields 的 schema 用于传递给 LLM（不包含过滤元数据）
    output_schema_for_llm = {'fields': filtered_output_schema.get('fields', [])}

    # 构建提示词
    prompt = f"""You are an expert in analyzing function dependencies. Determine if there should be a directed edge from the node function to the candidate function.

Node Function (Source):
- Name: {node_name}
- Description: {node_desc}
- Output Schema (already filtered, excluding pass-through params): {json.dumps(output_schema_for_llm, indent=2, ensure_ascii=False)}

Candidate Function (Target):
- Name: {candidate_name}
- Description: {candidate_desc}
- Input Parameters: {json.dumps(candidate_params, indent=2, ensure_ascii=False)}


Analyze whether there should be a directed edge from node function to candidate function. Consider the following scenarios:

1. **Data Dependency**: Can the node function's filtered output be used as part or all of the candidate function's input?
   - Example: node function returns a file path, candidate function needs that path as input
   - **You must explicitly point out which output parameter from node function maps to which input parameter of candidate function**

2. **Prerequisite Dependency**: Can the node function's output determine whether we can/should call the candidate function?
   - Example: node function checks if a file exists, candidate function downloads the file (we should only download if file doesn't exist)
   - Example: node function validates permissions, candidate function performs an action (we should only perform action if permissions are valid)
   - Example: node function checks resource availability, candidate function uses that resource (we should only use resource if available)

A directed edge should exist if:
- The node function's filtered output can be used as input for the candidate function (data dependency), OR
- The node function's output determines whether it's appropriate/safe to call the candidate function (prerequisite dependency)

Your output MUST be in the following format:
HAS_EDGE: [true/false]
DEPENDENCY_TYPE: [full/partial/prerequisite/none]
PARAM_MAPPING: [JSON object mapping node output params to candidate input params, or "NONE" if no data dependency]
REASONING: [detailed explanation]

- HAS_EDGE: true if there should be a directed edge from node to candidate, false otherwise
- DEPENDENCY_TYPE:
  - "full" if node's output can be used as complete input for candidate
  - "partial" if node's output can be used as part of candidate's input
  - "prerequisite" if node's output determines whether we can/should call candidate function
  - "none" if no dependency exists
- PARAM_MAPPING: For data dependency (full/partial), provide a JSON object like {{"node_output_param1": "candidate_input_param1", "node_output_param2": "candidate_input_param2"}}. If the output has nested fields, use dot notation like "result.items". For prerequisite dependency or no dependency, output "NONE".
- REASONING: explain your thinking process, including which output parameters you used and how they map to candidate input parameters.
"""

    try:
        completion = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert analyst specializing in determining function dependencies and data flow."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.3,
            max_completion_tokens=1024
        )

        response_text = completion.choices[0].message.content

        # 解析响应
        has_edge = False
        confidence = 0.0
        dependency_type = "none"
        reasoning = ""
        param_mapping = {}

        lines = response_text.split('\n')
        for line in lines:
            line_upper = line.upper().strip()
            if line_upper.startswith('HAS_EDGE:'):
                value = line.split(':', 1)[1].strip() if ':' in line else ""
                has_edge = value.lower() in ['true', 'yes', '1', 'y']
            elif line_upper.startswith('CONFIDENCE:'):
                value = line.split(':', 1)[1].strip() if ':' in line else "0.0"
                try:
                    confidence = float(value)
                except ValueError:
                    confidence = 0.0
            elif line_upper.startswith('DEPENDENCY_TYPE:'):
                value = line.split(':', 1)[1].strip() if ':' in line else "none"
                dependency_type = value.lower()
            elif line_upper.startswith('PARAM_MAPPING:'):
                value = line.split(':', 1)[1].strip() if ':' in line else "NONE"
                if value.upper() != "NONE":
                    try:
                        param_mapping = json.loads(value)
                    except json.JSONDecodeError:
                        param_mapping = {}
                else:
                    param_mapping = {}
            elif line_upper.startswith('REASONING:'):
                reasoning = line.split(':', 1)[1].strip() if ':' in line else ""

        token_usage = {
            'prompt_tokens': completion.usage.prompt_tokens,
            'completion_tokens': completion.usage.completion_tokens,
            'total_tokens': completion.usage.total_tokens
        }

        return {
            'has_edge': has_edge,
            'confidence': confidence,
            'dependency_type': dependency_type,
            'param_mapping': param_mapping,
            'reasoning': reasoning,
            'token_usage': token_usage,
            'node_func':node_func['function_schema'],
            'candidate_func':candidate_func['function_schema'],
            'filtered_output_schema': filtered_output_schema
        }

    except Exception as e:
        return {
            'has_edge': False,
            'confidence': 0.0,
            'dependency_type': 'none',
            'param_mapping': {},
            'reasoning': f'Error: {str(e)}',
            'token_usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0},
            'filtered_output_schema': {}
        }


async def build_graph_v1(nodes, sampled_candidates, batch_size=10, progress_file=None):
    """
    构建 graph v1.0.0，支持增量保存和断点续传

    Args:
        nodes: list, 节点列表
        sampled_candidates: dict, {node_index: [candidate_indices]}
        batch_size: int, 批处理大小
        progress_file: str, 进度文件路径（用于断点续传和增量保存）

    Returns:
        dict: 图的结构，包含 nodes 和 edges
    """
    print(f"\nBuilding graph v1.0.0 with {len(nodes)} nodes...")

    edges = []
    edge_details = []
    total_pairs = sum(len(candidates) for candidates in sampled_candidates.values())

    # 累积整体 token 使用情况（包括有边和无边的所有 LLM 调用）
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_tokens = 0
    successful_calls = 0

    print(f"Total candidate pairs to evaluate: {total_pairs}")

    # 收集所有需要判断的边
    edge_tasks = []
    for node_idx, candidate_indices in sampled_candidates.items():
        node_func = nodes[node_idx]
        for candidate_idx in candidate_indices:
            candidate_func = nodes[candidate_idx]
            edge_tasks.append((node_idx, candidate_idx, node_func, candidate_func))

    # 检查是否有进度文件（断点续传）
    processed_pairs = set()
    previous_processed_batches = 0  # 记录之前已经处理的批次数量（用于累加）
    if progress_file and os.path.exists(progress_file):
        print(f"\n==> Found progress file: {progress_file}")
        print("==> Loading previously processed pairs...")
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
                # 恢复之前的结果
                edges = progress_data.get('edges', [])
                edge_details = progress_data.get('edge_details', [])
                stats = progress_data.get('token_usage_summary', {})
                total_prompt_tokens = stats.get('total_prompt_tokens', 0)
                total_completion_tokens = stats.get('total_completion_tokens', 0)
                total_tokens = stats.get('total_tokens', 0)
                successful_calls = stats.get('successful_calls', 0)
                
                # 恢复之前已经处理的批次数量（用于累加）
                progress_info = progress_data.get('progress', {})
                previous_processed_batches = progress_info.get('processed_batches', 0)

                # 恢复已处理的pairs（所有的，不只是有边的）
                processed_pairs_list = progress_data.get('processed_pairs', [])
                processed_pairs_raw = set(tuple(pair) for pair in processed_pairs_list)
                
                # 构建 function name -> index 的映射（用于验证和转换）
                name_to_index = {}
                for idx, node in enumerate(nodes):
                    func_name = node.get('function_schema', {}).get('function', {}).get('name', '')
                    if func_name:
                        name_to_index[func_name] = idx
                
                # 如果有保存的 function name pairs，优先使用（向后兼容）
                processed_pairs_by_name = progress_data.get('processed_pairs_by_name', [])
                if processed_pairs_by_name:
                    # 通过 function name 转换索引
                    processed_pairs = set()
                    for pair_names in processed_pairs_by_name:
                        if len(pair_names) == 2:
                            node_name, candidate_name = pair_names
                            node_idx = name_to_index.get(node_name)
                            candidate_idx = name_to_index.get(candidate_name)
                            if node_idx is not None and candidate_idx is not None:
                                processed_pairs.add((node_idx, candidate_idx))
                    print(f"==> Converted {len(processed_pairs)} pairs from function names")
                else:
                    # 使用索引，但验证有效性
                    num_nodes = len(nodes)
                    valid_pairs = set()
                    for pair in processed_pairs_raw:
                        if len(pair) == 2:
                            node_idx, candidate_idx = pair
                            # 验证索引是否在有效范围内
                            if 0 <= node_idx < num_nodes and 0 <= candidate_idx < num_nodes:
                                valid_pairs.add(pair)
                    processed_pairs = valid_pairs
                    if len(processed_pairs) < len(processed_pairs_raw):
                        print(f"==> Warning: {len(processed_pairs_raw) - len(processed_pairs)} pairs have invalid indices (likely due to node order change)")

            print(f"==> Resumed: {len(processed_pairs)} pairs already processed, {len(edges)} edges found")
        except Exception as e:
            print(f"Warning: Failed to load progress file: {e}")
            print("==> Starting from scratch...")
            processed_pairs = set()

    # 过滤掉已处理的任务
    if processed_pairs:
        original_count = len(edge_tasks)
        # 构建当前edge_tasks中所有pairs的集合，用于验证processed_pairs的有效性
        current_task_pairs = {(task[0], task[1]) for task in edge_tasks}
        
        # 只保留在当前任务中实际存在的processed_pairs（过滤掉无效的）
        valid_processed_pairs = processed_pairs & current_task_pairs
        invalid_processed_pairs_count = len(processed_pairs) - len(valid_processed_pairs)
        
        # 过滤掉已处理的任务（只使用有效的pairs）
        edge_tasks = [
            task for task in edge_tasks
            if (task[0], task[1]) not in valid_processed_pairs
        ]
        
        skipped_count = original_count - len(edge_tasks)
        print(f"==> Remaining pairs to process: {len(edge_tasks)} (skipped {skipped_count})")
        if invalid_processed_pairs_count > 0:
            print(f"==> Warning: {invalid_processed_pairs_count} processed pairs are not in current task list (ignored)")
            print(f"==> Valid processed pairs: {len(valid_processed_pairs)}, Invalid: {invalid_processed_pairs_count}")
        
        # 更新processed_pairs为只包含有效的pairs（用于后续保存，避免累积无效数据）
        processed_pairs = valid_processed_pairs

    if not edge_tasks:
        print("==> All pairs already processed!")
        # 直接返回已有结果
        token_summary = {
            'successful_calls': successful_calls,
            'total_prompt_tokens': total_prompt_tokens,
            'total_completion_tokens': total_completion_tokens,
            'total_tokens': total_tokens,
            'avg_prompt_tokens_per_call': total_prompt_tokens / successful_calls if successful_calls > 0 else 0.0,
            'avg_completion_tokens_per_call': total_completion_tokens / successful_calls if successful_calls > 0 else 0.0,
            'avg_total_tokens_per_call': total_tokens / successful_calls if successful_calls > 0 else 0.0,
        }
        return {
            'version': '1.0.0',
            'num_nodes': len(nodes),
            'num_edges': len(edges),
            'nodes': [
                {
                    'index': i,
                    'function_schema': node['function_schema'],
                    'classification': node.get('classification', {})
                }
                for i, node in enumerate(nodes)
            ],
            'edges': edges,
            'edge_details': edge_details,
            'token_usage_summary': token_summary,
        }

    # 批量处理
    total_batches = (len(edge_tasks) + batch_size - 1) // batch_size
    batch_iterator = tqdm(
        range(0, len(edge_tasks), batch_size),
        total=total_batches,
        desc="Judging edges",
        unit="batch"
    )

    for i in batch_iterator:
        batch = edge_tasks[i:i+batch_size]
        batch_num = i // batch_size + 1

        # 创建异步任务
        tasks = [judge_edge_async(node_func, candidate_func) for _, _, node_func, candidate_func in batch]
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        # 统计这个batch中成功处理的数量（用于早停检测）
        batch_success_count = 0

        # 处理结果
        for idx, result in enumerate(batch_results):
            node_idx, candidate_idx, _, _ = batch[idx]

            # 检查是否是异常类型
            if isinstance(result, Exception):
                tqdm.write(f"  Error judging edge {node_idx} -> {candidate_idx}: {str(result)}")
                # 出错的pair不记录到processed_pairs，下次重启时会重试
                continue

            # 检查是否是函数内部捕获的错误（reasoning 以 "Error:" 开头）
            reasoning = result.get('reasoning', '')
            if reasoning.startswith('Error:'):
                tqdm.write(f"  Error in judge_edge_async for {node_idx} -> {candidate_idx}: {reasoning}")
                # 出错的pair不记录到processed_pairs，下次重启时会重试
                continue

            # 检查 filter 过程是否出错
            filtered_schema = result.get('filtered_output_schema', {})
            filter_reasoning = filtered_schema.get('filter_reasoning', '')
            if filter_reasoning.startswith('Error occurred:'):
                tqdm.write(f"  Error in filter_output_params for {node_idx} -> {candidate_idx}: {filter_reasoning}")
                # 出错的pair不记录到processed_pairs，下次重启时会重试
                continue

            # 成功处理（无论是否有边）
            batch_success_count += 1

            # 记录已成功处理的pair（无论是否有边）
            processed_pairs.add((node_idx, candidate_idx))

            # 累计 token 使用（无论是否判定为有边）
            tu = result.get('token_usage', {}) or {}
            total_prompt_tokens += tu.get('prompt_tokens', 0)
            total_completion_tokens += tu.get('completion_tokens', 0)
            total_tokens += tu.get('total_tokens', 0)
            successful_calls += 1

            if result.get('has_edge', False):
                edges.append({
                    'source': node_idx,
                    'target': candidate_idx,
                    'confidence': result.get('confidence', 0.0),
                    'dependency_type': result.get('dependency_type', 'none'),
                    'param_mapping': result.get('param_mapping', {})
                })
                edge_details.append({
                    'source': node_idx,
                    'target': candidate_idx,
                    'source_name': nodes[node_idx]['function_schema']['function'].get('name', ''),
                    'target_name': nodes[candidate_idx]['function_schema']['function'].get('name', ''),
                    'confidence': result.get('confidence', 0.0),
                    'dependency_type': result.get('dependency_type', 'none'),
                    'param_mapping': result.get('param_mapping', {}),
                    'filtered_output_schema': result.get('filtered_output_schema', {}),
                    'reasoning': result.get('reasoning', ''),
                    'token_usage': tu
                })

        # 早停机制：如果这个batch的所有任务都失败了，停止程序
        if batch_success_count == 0:
            error_msg = f"\n{'='*80}\nEARLY STOP: All tasks in batch {batch_num} failed!\n{'='*80}"
            tqdm.write(error_msg)
            print(error_msg)
            print(f"Batch size: {len(batch)}")
            print(f"Successful tasks: {batch_success_count}")
            print(f"Failed tasks: {len(batch)}")
            print("\nThis indicates a critical issue (API down, rate limit, network error, etc.)")
            print("Please check the error messages above and fix the issue before retrying.")

            # 打印失败batch中的所有函数对
            print("\n" + "="*80)
            print("Failed batch details:")
            print("="*80)
            for idx, (node_idx, candidate_idx, node_func, candidate_func) in enumerate(batch):
                node_name = node_func.get('function_schema', {}).get('function', {}).get('name', 'Unknown')
                candidate_name = candidate_func.get('function_schema', {}).get('function', {}).get('name', 'Unknown')
                print(f"\nTask {idx + 1}:")
                print(f"  Node (source): [{node_idx}] {node_name}")
                print(f"  Candidate (target): [{candidate_idx}] {candidate_name}")
            print("="*80 + "\n")

            assert False, "All tasks in current batch failed - stopping execution"

        # 每个batch完成后，写入进度文件（增量保存）
        if progress_file:
            # 构建 function name pairs（用于向后兼容，即使 nodes 顺序变化也能恢复）
            processed_pairs_by_name = []
            for node_idx, candidate_idx in processed_pairs:
                node_name = nodes[node_idx].get('function_schema', {}).get('function', {}).get('name', '')
                candidate_name = nodes[candidate_idx].get('function_schema', {}).get('function', {}).get('name', '')
                if node_name and candidate_name:
                    processed_pairs_by_name.append([node_name, candidate_name])
            
            progress_data = {
                'version': '1.0.0',
                'progress': {
                    'processed_batches': previous_processed_batches + batch_num,  # 累加批次数量
                    'total_batches': (total_pairs + batch_size - 1) // batch_size,
                    'processed_pairs': len(processed_pairs),
                    'total_pairs': total_pairs,
                },
                'processed_pairs': list(processed_pairs),  # 保存索引对（向后兼容）
                'processed_pairs_by_name': processed_pairs_by_name,  # 保存 function name 对（用于索引转换）
                'edges': edges,
                'edge_details': edge_details,
                'token_usage_summary': {
                    'successful_calls': successful_calls,
                    'total_prompt_tokens': total_prompt_tokens,
                    'total_completion_tokens': total_completion_tokens,
                    'total_tokens': total_tokens,
                }
            }
            try:
                os.makedirs(os.path.dirname(progress_file), exist_ok=True)
                with open(progress_file, 'w', encoding='utf-8') as f:
                    json.dump(progress_data, f, indent=2, ensure_ascii=False)
            except Exception as e:
                tqdm.write(f"Warning: Failed to save progress: {e}")

        batch_iterator.set_postfix_str(f"batch={batch_num}/{total_batches}, edges={len(edges)}")

    batch_iterator.close()
    
    # 构建图结构
    # 统计整体 token 使用
    token_summary = {
        'successful_calls': successful_calls,
        'total_prompt_tokens': total_prompt_tokens,
        'total_completion_tokens': total_completion_tokens,
        'total_tokens': total_tokens,
        'avg_prompt_tokens_per_call': total_prompt_tokens / successful_calls if successful_calls > 0 else 0.0,
        'avg_completion_tokens_per_call': total_completion_tokens / successful_calls if successful_calls > 0 else 0.0,
        'avg_total_tokens_per_call': total_tokens / successful_calls if successful_calls > 0 else 0.0,
    }
    
    graph = {
        'version': '1.0.0',
        'num_nodes': len(nodes),
        'num_edges': len(edges),
        'nodes': [
            {
                'index': i,
                'function_schema': node['function_schema'],
                'classification': node.get('classification', {})
            }
            for i, node in enumerate(nodes)
        ],
        'edges': edges,
        'edge_details': edge_details,
        'token_usage_summary': token_summary,
    }
    
    print(f"\nGraph v1.0.0 built successfully!")
    print(f"  Nodes: {len(nodes)}")
    print(f"  Edges: {len(edges)}")
    print(f"  Edge density: {len(edges) / (len(nodes) * (len(nodes) - 1)) * 100:.4f}%")
    print("\nToken usage summary (edge judgments):")
    print(f"  Successful calls: {successful_calls}")
    print(f"  Total prompt tokens: {total_prompt_tokens}")
    print(f"  Total completion tokens: {total_completion_tokens}")
    print(f"  Total tokens: {total_tokens}")
    if successful_calls > 0:
        print(f"  Avg tokens per call: {total_tokens / successful_calls:.2f}")
    
    return graph


def save_node_candidates_mapping(
    nodes: List[Dict],
    node_candidates: Dict[int, List[int]],
    output_file: str
) -> None:
    """
    保存 node -> candidates 的映射关系到文件（以 function name 为标识）

    Args:
        nodes: list, 节点列表
        node_candidates: dict, {node_index: [candidate_indices]}
        output_file: str, 输出文件路径
    """
    print(f"\nSaving node-candidates mapping to {output_file}...")

    # 构建 index -> function_name 的映射
    index_to_name = {}
    for idx, node in enumerate(nodes):
        func_name = node.get('function_schema', {}).get('function', {}).get('name', '')
        if func_name:
            index_to_name[idx] = func_name

    # 转换为 name-based 映射
    name_based_mapping = {}
    missing_names = []

    for node_idx, candidate_indices in node_candidates.items():
        node_name = index_to_name.get(node_idx)
        if not node_name:
            missing_names.append(node_idx)
            continue

        candidate_names = []
        for cand_idx in candidate_indices:
            cand_name = index_to_name.get(cand_idx)
            if cand_name:
                candidate_names.append(cand_name)
            else:
                missing_names.append(cand_idx)

        name_based_mapping[node_name] = candidate_names

    if missing_names:
        print(f"Warning: {len(set(missing_names))} node indices have no function name")

    # 构建输出数据
    output_data = {
        'metadata': {
            'total_nodes': len(nodes),
            'total_mappings': len(name_based_mapping),
            'avg_candidates_per_node': sum(len(v) for v in name_based_mapping.values()) / len(name_based_mapping) if name_based_mapping else 0,
        },
        'node_to_candidates': name_based_mapping
    }

    # 保存到文件
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(name_based_mapping)} node-candidates mappings")
    print(f"  Average candidates per node: {output_data['metadata']['avg_candidates_per_node']:.2f}")


def load_node_candidates_mapping(
    nodes: List[Dict],
    mapping_file: str
) -> Dict[int, List[int]]:
    """
    从文件加载 node -> candidates 的映射关系，并转换回 index-based 格式

    Args:
        nodes: list, 当前的节点列表
        mapping_file: str, 映射文件路径

    Returns:
        dict: {node_index: [candidate_indices]}
    """
    print(f"\nLoading node-candidates mapping from {mapping_file}...")

    with open(mapping_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    name_based_mapping = data.get('node_to_candidates', {})

    # 构建 function_name -> index 的映射（基于当前的 nodes）
    name_to_index = {}
    for idx, node in enumerate(nodes):
        func_name = node.get('function_schema', {}).get('function', {}).get('name', '')
        if func_name:
            name_to_index[func_name] = idx

    # 转换为 index-based 映射
    index_based_mapping = {}
    not_found_nodes = []
    not_found_candidates = []

    for node_name, candidate_names in name_based_mapping.items():
        node_idx = name_to_index.get(node_name)
        if node_idx is None:
            not_found_nodes.append(node_name)
            continue

        candidate_indices = []
        for cand_name in candidate_names:
            cand_idx = name_to_index.get(cand_name)
            if cand_idx is not None:
                candidate_indices.append(cand_idx)
            else:
                not_found_candidates.append(cand_name)

        index_based_mapping[node_idx] = candidate_indices

    if not_found_nodes:
        print(f"Warning: {len(not_found_nodes)} nodes from mapping file not found in current nodes")
    if not_found_candidates:
        print(f"Warning: {len(set(not_found_candidates))} candidate names not found in current nodes")

    print(f"Loaded {len(index_based_mapping)} node-candidates mappings")

    return index_based_mapping


def main():
    """
    主函数：构建 graph v1.0.0
    """
    input_file = '/data/lhy/datasets/graph-Toucan/tool_info/tool_classification_results_v1.json'
    output_file = '/data/lhy/datasets/graph-Toucan/graph/graph_v1.json'
    candidates_mapping_file = '/data/lhy/datasets/graph-Toucan/graph/node_candidates_mapping.json'

    # 1. 加载工具分类结果
    results = load_tool_classification_results(input_file)

    # 2. 从 tool_schema_with_outputformat.json 获取有 output schema 的 tools
    schema_file = '/data/lhy/datasets/graph-Toucan/tool_info/tool_schema_with_outputformat.json'
    tools_with_output_schema, schema_data = load_tools_with_output_schema(schema_file)

    # 2.1 筛选出同时存在于 classification results 和 output schema 中的 tools
    # 构建 classification results 的 name -> tool 映射
    classification_by_name = {}
    for tool in results:
        func_name = tool.get('function_schema', {}).get('function', {}).get('name', '')
        if func_name:
            classification_by_name[func_name] = tool

    # 只保留在两者中都存在的 tools，并合并信息
    # 注意：tools_with_output_schema 是 Set，需要排序以确保 nodes 顺序固定
    nodes = []
    for tool_name in sorted(tools_with_output_schema):  # 排序确保顺序固定
        if tool_name in classification_by_name:
            # 合并 classification 和 schema 信息
            tool_info = classification_by_name[tool_name].copy()
            # 可以在这里添加 output schema 信息（如果需要的话）
            # 从 schema_data 中找到对应的 schema
            for schema_item in schema_data:
                if schema_item.get('tool_name') == tool_name:
                    tool_info['output_schema'] = schema_item.get('output_schema_parsed')
                    break
            nodes.append(tool_info)

    print(f"\n筛选出 {len(nodes)} 个同时有 classification 和 output schema 的 tools")
    print(f"  - Total tools in classification: {len(results)}")
    print(f"  - Total tools with output schema: {len(tools_with_output_schema)}")
    print(f"  - Intersection: {len(nodes)}")

    # 3. 找到每个节点的 candidates（基于 label 重合）
    # 检查是否已有映射文件，如果有则直接加载，否则重新计算
    if os.path.exists(candidates_mapping_file):
        print(f"\n==> Found existing candidates mapping file: {candidates_mapping_file}")
        print("==> Loading candidates from file (use this to skip recomputation)...")
        node_candidates = load_node_candidates_mapping(nodes, candidates_mapping_file)
    else:
        print(f"\n==> Candidates mapping file not found: {candidates_mapping_file}")
        print("==> Computing candidates from scratch...")
        node_candidates = find_candidates_for_nodes_raw(nodes, max_candidates=40)

        # 3.1 保存 node -> candidates 映射（以 function name 为标识）
        save_node_candidates_mapping(nodes, node_candidates, candidates_mapping_file)

    # 5. 使用 LLM 判断边，构建图（支持增量保存和断点续传）
    progress_file = '/data/lhy/datasets/graph-Toucan/graph/graph_v1_progress.json'
    graph = asyncio.run(build_graph_v1(nodes, node_candidates, batch_size=20, progress_file=progress_file))
    
    # 6. 保存图
    print(f"\nSaving graph to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"Graph saved successfully!")


    # 7. 打印统计信息
    print("\n" + "="*80)
    print("Graph v1.0.0 Statistics")
    print("="*80)
    print(f"Total nodes: {graph['num_nodes']}")
    print(f"Total edges: {graph['num_edges']}")
    
    # 统计依赖类型
    dependency_types = Counter(edge['dependency_type'] for edge in graph['edges'])
    print(f"\nDependency types:")
    for dep_type, count in dependency_types.items():
        print(f"  {dep_type}: {count}")
    
    # 统计置信度
    confidences = [edge['confidence'] for edge in graph['edges']]
    if confidences:
        print(f"\nConfidence statistics:")
        print(f"  Average: {sum(confidences) / len(confidences):.3f}")
        print(f"  Max: {max(confidences):.3f}")
        print(f"  Min: {min(confidences):.3f}")
    
    print("="*80 + "\n")


def visualize_graph(
    graph_file: str,
    max_nodes: int = 100,
    layout: str = "spring",
    output_file: str | None = None,
    min_confidence: float = 0.0,
):
    """
    可视化已经构建好的 graph（如 test_graph_v1.0.0.json）

    Args:
        graph_file: str, 图的 JSON 文件路径
        max_nodes: int, 最多显示的节点数（防止太密集）
        layout: str, 布局类型："spring" / "kamada_kawai" / "circular"
        output_file: str 或 None, 如果提供则保存为图片文件，否则直接展示
        min_confidence: float, 只显示置信度大于等于该阈值的边
    """
    print(f"Loading graph from {graph_file}...")
    with open(graph_file, "r", encoding="utf-8") as f:
        graph = json.load(f)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    if not nodes:
        print("No nodes found in graph, aborting visualization.")
        return

    # 如果节点太多，截断
    if len(nodes) > max_nodes:
        print(f"Graph has {len(nodes)} nodes, visualizing first {max_nodes} nodes only.")
        node_indices = set(range(max_nodes))
    else:
        node_indices = set(range(len(nodes)))

    # 构建 NetworkX 有向图
    G = nx.DiGraph()

    # 添加节点（使用函数名作为标签）
    for node in nodes:
        idx = node.get("index")
        if idx not in node_indices:
            continue
        func_schema = node.get("function_schema", {}).get("function", {})
        name = func_schema.get("name", f"node_{idx}")
        G.add_node(idx, label=name)

    # 添加边（只保留在可视节点集合中的边，并按置信度过滤）
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        conf = edge.get("confidence", 0.0)
        dep_type = edge.get("dependency_type", "none")

        if src in node_indices and tgt in node_indices and conf >= min_confidence:
            G.add_edge(src, tgt, confidence=conf, dependency_type=dep_type)

    if G.number_of_nodes() == 0:
        print("No nodes to visualize after filtering, aborting.")
        return

    print(f"Visualizing graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges...")

    # 选择布局
    if layout == "spring":
        pos = nx.spring_layout(G, seed=42)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(G)
    elif layout == "circular":
        pos = nx.circular_layout(G)
    else:
        print(f"Unknown layout '{layout}', fallback to spring layout.")
        pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(12, 8))

    # 节点标签（过长则截断）
    labels = {}
    for n in G.nodes():
        label = str(G.nodes[n].get("label", n))
        if len(label) > 28:
            label = label[:25] + "..."
        labels[n] = label

    # 根据 dependency_type 给边着色
    edge_colors = []
    for _, _, data in G.edges(data=True):
        dep_type = data.get("dependency_type", "none")
        if dep_type == "full":
            edge_colors.append("green")
        elif dep_type == "partial":
            edge_colors.append("orange")
        elif dep_type == "prerequisite":
            edge_colors.append("blue")
        else:
            edge_colors.append("gray")

    nx.draw_networkx_nodes(G, pos, node_size=400, node_color="#87ceeb", alpha=0.9)
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15, edge_color=edge_colors, width=1.5, alpha=0.8)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    plt.axis("off")
    plt.title(f"Graph Visualization ({os.path.basename(graph_file)})", fontsize=12)

    if output_file:
        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        print(f"Graph visualization saved to {output_file}")
        plt.close()
    else:
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()  # 构图时再开
    #visualize_graph("test_graph_v1.0.0.json", max_nodes=100, layout="spring",output_file='test_graph_v1.0.0.png')