"""
Node merging functionality for random walk paths.

功能：对随机游走路径进行节点合并增强
- 按概率选择路径中的节点进行 merge
- 从 tool_classification_results_v1.json 中查找相同 primary_label 的函数
- 将找到的函数添加到同一层（不改变原路径结构）
"""

import json
import random
from typing import Dict, List, Tuple, Any, Optional


TOOL_CLASSIFICATION_PATH = "/data/lhy/datasets/graph-Toucan/tool_info/tool_classification_results_v1.json"


def load_tool_classification(
    classification_file: str = TOOL_CLASSIFICATION_PATH,
) -> Dict[str, Any]:
    """
    从 tool_classification_results_v1.json 加载工具分类信息。

    Returns:
        dict: 工具分类字典，key 是工具名称
    """
    print(f"Loading tool classification from {classification_file}...")
    with open(classification_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} tools with classification info")
    return data


def select_nodes_for_merge(
    paths: List[Dict[str, Any]],
    nodes: List[Dict[str, Any]],
    merge_probability: float,
    rng: random.Random,
) -> Dict[str, List[Tuple[int, int]]]:
    """
    对每条路径的每个节点按概率进行随机选择，标记为 'need_merge'。

    Args:
        paths: 路径列表（来自 run_random_walks 的结果）
        nodes: 图中的节点列表
        merge_probability: 选择节点的概率
        rng: 随机数生成器

    Returns:
        dict: {path_id: [(step_idx, node_idx), ...]} 需要 merge 的节点位置
    """
    selected_for_merge: Dict[str, List[Tuple[int, int]]] = {}

    for path_record in paths:
        path_id = f"{path_record['start_index']}_{path_record['walk_id']}"
        node_indices = path_record['node_indices']
        selected_positions = []

        for step_idx, node_idx in enumerate(node_indices):
            # 按概率随机选择
            if rng.random() < merge_probability:
                selected_positions.append((step_idx, node_idx))

        if selected_positions:
            selected_for_merge[path_id] = selected_positions

    print(f"Selected {sum(len(v) for v in selected_for_merge.values())} nodes for merge across {len(selected_for_merge)} paths")
    return selected_for_merge


def merge_nodes(
    paths: List[Dict[str, Any]],
    nodes: List[Dict[str, Any]],
    merge_probability: float = 0.3,
    classification_file: str = TOOL_CLASSIFICATION_PATH,
    seed: Optional[int] = None,
    rng: Optional[random.Random] = None,
) -> List[Dict[str, Any]]:
    """
    对路径中的节点进行 merge 操作。

    核心逻辑：
    1. 对每条路径的每个节点，按概率 p 随机选择
    2. 如果选中，从 tool_classification_results_v1.json 中查找：
       - primary_label 与当前节点相同的函数
       - 且该函数未在此路径中出现过
    3. 将找到的函数添加到同一层（与当前节点并列），标记为 merge
    4. 这个额外的节点不改变原路径结构

    Args:
        paths: 路径列表（来自 run_random_walks 的 flat_paths）
        nodes: 图中的节点列表（包含 function_schema 等信息）
        merge_probability: 选择节点进行 merge 的概率
        classification_file: 工具分类文件路径
        seed: 随机种子，用于确保可复现性。如果提供了 rng，则忽略此参数
        rng: 随机数生成器。如果为 None，则使用 seed 创建新的 Random 对象

    Returns:
        List[Dict]: 增强后的路径列表，每个节点可能包含 merged_nodes 字段
    """
    # 创建或使用随机数生成器
    if rng is None:
        if seed is not None:
            rng = random.Random(seed)
            print(f"Using seed {seed} for reproducible node merging")
        else:
            rng = random.Random()
            print("Warning: No seed provided, results may not be reproducible")

    # 加载工具分类信息
    tool_classification = load_tool_classification(classification_file)

    # 构建节点索引到节点信息的映射
    index_to_node = {node['index']: node for node in nodes}

    # 选择需要 merge 的节点
    selected_for_merge = select_nodes_for_merge(paths, nodes, merge_probability, rng)

    # 对每条路径进行处理
    enriched_paths = []

    for path_record in paths:
        path_id = f"{path_record['start_index']}_{path_record['walk_id']}"
        node_indices = path_record['node_indices']
        node_names = path_record['node_names']

        # 为路径中的每个节点创建扩展信息
        enriched_steps = []

        for step_idx, (node_idx, node_name) in enumerate(zip(node_indices, node_names)):
            step_info = {
                'step_idx': step_idx,
                'node_idx': node_idx,
                'node_name': node_name,
                'need_merge': False,
                'merged_nodes': []  # 同一层的额外节点
            }

            # 检查这个节点是否被选中进行 merge
            if path_id in selected_for_merge:
                for selected_step, selected_node in selected_for_merge[path_id]:
                    if selected_step == step_idx and selected_node == node_idx:
                        step_info['need_merge'] = True
                        break

            # 如果需要 merge，查找兼容的函数
            if step_info['need_merge']:
                node_info = index_to_node.get(node_idx)
                if node_info:
                    func_schema = node_info.get('function_schema', {}).get('function', {})
                    current_func_name = func_schema.get('name', '')

                    # 从工具分类中获取当前节点的 primary_label
                    current_tool_info = tool_classification.get(current_func_name)
                    if current_tool_info:
                        primary_label = current_tool_info.get('primary_label')

                        if primary_label:
                            # 查找相同 primary_label 且未在路径中出现的函数
                            candidates = []
                            for tool_name, tool_info in tool_classification.items():
                                if tool_info.get('primary_label') == primary_label:
                                    # 检查是否已在路径中出现
                                    if tool_name not in node_names:
                                        candidates.append((tool_name, tool_info))

                            # 随机选择一个候选函数
                            if candidates:
                                selected_tool_name, selected_tool_info = rng.choice(candidates)
                                merged_node = {
                                    'function_name': selected_tool_name,
                                    'primary_label': primary_label,
                                    'secondary_labels': selected_tool_info.get('secondary_labels', []),
                                    'function_schema': selected_tool_info.get('function_schema', {}),
                                    'merge_reason': f'Same primary_label "{primary_label}" as node {node_name}',
                                }
                                step_info['merged_nodes'].append(merged_node)

            enriched_steps.append(step_info)

        # 创建增强后的路径记录
        enriched_path = path_record.copy()
        enriched_path['enriched_steps'] = enriched_steps
        enriched_path['num_merged_nodes'] = sum(len(s['merged_nodes']) for s in enriched_steps)
        enriched_paths.append(enriched_path)

    total_merged = sum(p['num_merged_nodes'] for p in enriched_paths)
    print(f"Merged {total_merged} additional nodes across {len(enriched_paths)} paths")

    return enriched_paths


def save_enriched_paths(
    enriched_paths: List[Dict[str, Any]],
    output_file: str,
) -> None:
    """
    保存增强后的路径到 JSON 文件。

    Args:
        enriched_paths: 增强后的路径列表
        output_file: 输出文件路径
    """
    print(f"Saving enriched paths to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enriched_paths, f, ensure_ascii=False, indent=2)
    print(f"Enriched paths saved to {output_file}")
