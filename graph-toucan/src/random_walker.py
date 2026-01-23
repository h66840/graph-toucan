"""
Random walker on the constructed tool graph.

功能需求：
- 基于已经构建好的函数依赖图（如 test_graph_v1.4.0_acyclic.json），
  从每个节点出发沿着有向边做随机游走（random walk）。
- 游走步数由参数控制 `max_steps`。
- 如果在图中无法走满指定步数（例如当前节点没有后继边），则提前停止，并记录日志。
- 需要将随机游走得到的「函数签名路径」以及元信息保存为一个 JSON 文件。

主要函数签名：
- run_random_walks(
    graph_path: str,
    max_steps: int = 10,
    walks_per_node: int = 1,
    log_path: str | None = None,
    save_json_path: str | None = None,
) -> dict
"""

import json
import os
import random
from typing import Dict, List, Tuple, Any, Optional


GRAPH_DIR = "/data/lhy/datasets/graph-Toucan/graph"
DEFAULT_GRAPH_PATH = os.path.join(GRAPH_DIR, "graph_v1.json")
DEFAULT_LOG_PATH = os.path.join(GRAPH_DIR, "random_walk.log")
DEFAULT_WALKS_JSON_PATH = os.path.join(GRAPH_DIR, "random_walk_paths1_5.json")
TOOL_CLASSIFICATION_PATH = "/data/lhy/datasets/graph-Toucan/tool_info/tool_classification_results_v1.json"
NODE_CANDIDATES_MAPPING_PATH = os.path.join(GRAPH_DIR, "node_candidates_mapping.json")


def load_graph_for_walk(
    graph_path: str,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[int, str], Dict[int, List[int]]]:
    """
    从图 JSON 文件中加载节点和边，并构建：
    - index_to_name: 节点索引 -> 函数名
    - adj: 邻接表 index -> List[index]（有向边 source -> target）
    """
    print(f"Loading graph for random walk from {graph_path}...")
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    
    need_edges = []
    for edge in edges:
        if edge['dependency_type'] == "prerequisite":
            continue
        need_edges.append(edge)
    
    edges = need_edges
    index_to_name: Dict[int, str] = {}
    for node in nodes:
        idx = node.get("index")
        func_schema = node.get("function_schema", {}).get("function", {})
        name = func_schema.get("name", f"node_{idx}")
        if idx is not None:
            index_to_name[idx] = name

    adj: Dict[int, List[int]] = {}
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src is None or tgt is None:
            continue
        adj.setdefault(src, []).append(tgt)

    print(
        f"Loaded graph: {len(nodes)} nodes, {len(edges)} edges, "
        f"{len(index_to_name)} named tools"
    )
    return nodes, edges, index_to_name, adj


def random_walk_from_node(
    start_idx: int,
    adj: Dict[int, List[int]],
    max_steps: int,
    rng: random.Random,
) -> List[int]:
    """
    从指定起点节点 `start_idx` 出发，按照邻接表 `adj` 做随机游走。

    **重要：保证路径无环（DAG）**
    - 维护已访问节点集合，避免重复访问
    - 在选择下一个节点时，只考虑未访问过的邻居
    - 如果所有邻居都已访问或无邻居，则提前停止

    返回经过的节点索引序列（包含起点），长度 <= max_steps + 1。
    如果在某一步没有后继节点，则提前停止。
    """
    path: List[int] = [start_idx]
    current = start_idx
    visited = {start_idx}  # 记录已访问的节点，确保无环

    for _ in range(max_steps):
        neighbors = adj.get(current, [])
        if not neighbors:
            break

        # 只考虑未访问过的邻居节点
        unvisited_neighbors = [n for n in neighbors if n not in visited]

        if not unvisited_neighbors:
            # 所有邻居都已访问，无法继续，提前停止
            break

        # 从未访问的邻居中随机选择一个
        current = rng.choice(unvisited_neighbors)
        path.append(current)
        visited.add(current)

    return path


def append_log(message: str, log_path: str) -> None:
    """
    将日志写入到指定 log 文件中（追加模式）。
    """
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(message.rstrip() + "\n")
    except Exception as e:
        # 不要因为日志失败影响主流程
        print(f"[random_walker] Failed to write log: {e}")


def run_walks_from_single_node_with_dedup(
    start_node_index: int,
    graph_path: str = DEFAULT_GRAPH_PATH,
    max_steps: int = 10,
    num_walks: int = 3,
    seed: int = 42,
    log_path: Optional[str] = None,
    save_json_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    从单个节点出发，生成多条路径并去重。
    
    Args:
        start_node_index: 起始节点索引
        graph_path: 图 JSON 文件路径
        max_steps: 每条游走路径允许的最大步数
        num_walks: 要生成的路径数量（默认3条）
        seed: 随机种子
        log_path: 日志文件路径（可选）
    
    Returns:
        {
            "start_node_index": int,
            "start_node_name": str,
            "num_walks": int,
            "paths_before_dedup": List[List[int]],  # 去重前的路径
            "paths_after_dedup": List[List[int]],    # 去重后的路径
            "num_paths_before_dedup": int,
            "num_paths_after_dedup": int,
            "dedup_ratio": float,  # 去重率 = (去重前 - 去重后) / 去重前
        }
    """
    rng = random.Random(seed)
    nodes, edges, index_to_name, adj = load_graph_for_walk(graph_path)
    
    start_node_name = index_to_name.get(start_node_index, f"node_{start_node_index}")
    
    # 生成多条路径
    paths_before_dedup: List[List[int]] = []
    for walk_id in range(num_walks):
        path = random_walk_from_node(start_node_index, adj, max_steps=max_steps, rng=rng)
        paths_before_dedup.append(path)
        
        if log_path is not None:
            msg = (
                f"[WALK {walk_id+1}/{num_walks}] start={start_node_index}({start_node_name}), "
                f"path_len={len(path)}, path={path}"
            )
            append_log(msg, log_path)
    
    # 去重：将路径转换为元组以便比较
    seen_paths = set()
    paths_after_dedup: List[List[int]] = []
    
    for path in paths_before_dedup:
        # 将路径转换为元组以便作为集合元素
        path_tuple = tuple(path)
        if path_tuple not in seen_paths:
            seen_paths.add(path_tuple)
            paths_after_dedup.append(path)
    
    num_before = len(paths_before_dedup)
    num_after = len(paths_after_dedup)
    dedup_ratio = (num_before - num_after) / num_before if num_before > 0 else 0.0
    
    result = {
        "start_node_index": start_node_index,
        "start_node_name": start_node_name,
        "num_walks": num_walks,
        "paths_before_dedup": paths_before_dedup,
        "paths_after_dedup": paths_after_dedup,
        "num_paths_before_dedup": num_before,
        "num_paths_after_dedup": num_after,
        "dedup_ratio": dedup_ratio,
    }
    
    # 打印结果
    print(f"\n从节点 {start_node_index} ({start_node_name}) 出发:")
    print(f"  生成路径数: {num_before}")
    print(f"  去重后路径数: {num_after}")
    print(f"  去重率: {dedup_ratio:.2%}")
    print(f"  去重前路径:")
    for i, path in enumerate(paths_before_dedup, 1):
        path_names = [index_to_name.get(p, f"node_{p}") for p in path]
        print(f"    {i}. {path} -> {path_names}")
    print(f"  去重后路径:")
    for i, path in enumerate(paths_after_dedup, 1):
        path_names = [index_to_name.get(p, f"node_{p}") for p in path]
        print(f"    {i}. {path} -> {path_names}")
    
    # 如果需要，保存结果到 JSON 文件
    if save_json_path is not None:
        print(f"\n保存结果到 {save_json_path}...")
        os.makedirs(os.path.dirname(save_json_path), exist_ok=True)
        
        # 准备保存的数据
        to_save = {
            "meta": {
                "start_node_index": start_node_index,
                "start_node_name": start_node_name,
                "graph_path": graph_path,
                "max_steps": max_steps,
                "num_walks": num_walks,
                "seed": seed,
            },
            "statistics": {
                "num_paths_before_dedup": num_before,
                "num_paths_after_dedup": num_after,
                "dedup_ratio": dedup_ratio,
            },
            "paths_before_dedup": [
                {
                    "walk_id": i,
                    "node_indices": path,
                    "node_names": [index_to_name.get(p, f"node_{p}") for p in path],
                    "path_length": len(path),
                }
                for i, path in enumerate(paths_before_dedup, 1)
            ],
            "paths_after_dedup": [
                {
                    "walk_id": i,
                    "node_indices": path,
                    "node_names": [index_to_name.get(p, f"node_{p}") for p in path],
                    "path_length": len(path),
                }
                for i, path in enumerate(paths_after_dedup, 1)
            ],
        }
        
        with open(save_json_path, "w", encoding="utf-8") as f:
            json.dump(to_save, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到 {save_json_path}")
    
    return result


def run_walks_from_all_nodes_with_dedup(
    graph_path: str = DEFAULT_GRAPH_PATH,
    max_steps: int = 10,
    num_walks_per_node: int = 3,
    seed: int = 42,
    log_path: Optional[str] = DEFAULT_LOG_PATH,
    save_json_path: Optional[str] = None,
    merge_probability: float = 0.15,
    candidates_mapping_path: str = NODE_CANDIDATES_MAPPING_PATH,
) -> Dict[str, Any]:
    """
    从每个节点出发，生成多条路径并去重，遍历整个图。
    然后对去重后的路径进行 merge 操作。
    
    Args:
        graph_path: 图 JSON 文件路径
        max_steps: 每条游走路径允许的最大步数
        num_walks_per_node: 每个节点要生成的路径数量（默认3条）
        seed: 随机种子
        log_path: 日志文件路径（可选）
        save_json_path: 保存结果的 JSON 文件路径（可选）
        merge_probability: 每个节点进行 merge 的概率（默认0.3）
        candidates_mapping_path: 节点候选映射文件路径
    
    Returns:
        {
            "graph_path": str,
            "max_steps": int,
            "num_walks_per_node": int,
            "num_nodes": int,
            "total_walks_before_dedup": int,
            "total_walks_after_dedup": int,
            "overall_dedup_ratio": float,
            "node_results": {
                "<node_index>": {
                    "name": str,
                    "num_paths_before_dedup": int,
                    "num_paths_after_dedup": int,
                    "dedup_ratio": float,
                    "paths_before_dedup": List[List[int]],
                    "paths_after_dedup": List[List[int]],
                },
                ...
            },
        }
    """
    rng = random.Random(seed)
    nodes, edges, index_to_name, adj = load_graph_for_walk(graph_path)
    
    # 构建 name_to_index 映射（用于 merge 时查找候选节点的索引）
    name_to_index: Dict[str, int] = {name: idx for idx, name in index_to_name.items()}
    
    # 加载节点候选映射
    node_to_candidates = load_node_candidates_mapping(candidates_mapping_path)
    
    node_indices = sorted(index_to_name.keys())
    
    if log_path is not None:
        # 清空旧日志
        try:
            if os.path.exists(log_path):
                os.remove(log_path)
        except Exception:
            pass
    
    node_results: Dict[str, Dict[str, Any]] = {}
    total_walks_before = 0
    total_walks_after = 0
    
    print(f"\n开始遍历所有节点，共 {len(node_indices)} 个节点...")
    
    for idx in node_indices:
        name = index_to_name.get(idx, f"node_{idx}")
        
        # 生成多条路径
        paths_before_dedup: List[List[int]] = []
        for walk_id in range(num_walks_per_node):
            path = random_walk_from_node(idx, adj, max_steps=max_steps, rng=rng)
            paths_before_dedup.append(path)
            
            if log_path is not None:
                msg = (
                    f"[WALK] node={idx}({name}), walk_id={walk_id+1}/{num_walks_per_node}, "
                    f"path_len={len(path)}, path={path}"
                )
                append_log(msg, log_path)
        
        # 去重
        seen_paths = set()
        paths_after_dedup: List[List[int]] = []
        
        for path in paths_before_dedup:
            path_tuple = tuple(path)
            if path_tuple not in seen_paths:
                seen_paths.add(path_tuple)
                paths_after_dedup.append(path)
        
        num_before = len(paths_before_dedup)
        num_after = len(paths_after_dedup)
        dedup_ratio = (num_before - num_after) / num_before if num_before > 0 else 0.0
        
        total_walks_before += num_before
        total_walks_after += num_after
        
        # 对去重后的路径进行 merge 操作
        merged_paths = merge_paths_with_candidates(
            paths_after_dedup=paths_after_dedup,
            index_to_name=index_to_name,
            node_to_candidates=node_to_candidates,
            name_to_index=name_to_index,
            merge_probability=merge_probability,
            rng=rng,
        )
        
        node_results[str(idx)] = {
            "name": name,
            "num_paths_before_dedup": num_before,
            "num_paths_after_dedup": num_after,
            "dedup_ratio": dedup_ratio,
            "paths_before_dedup": paths_before_dedup,
            "paths_after_dedup": paths_after_dedup,
            "merged_paths": merged_paths,
            "total_merges": sum(mp["num_merges"] for mp in merged_paths),
        }
        
        # 打印每个节点的结果
        if num_after < num_before:
            total_merges = sum(mp["num_merges"] for mp in merged_paths)
            print(f"节点 {idx} ({name}): {num_before} -> {num_after} 条路径 (去重率: {dedup_ratio:.2%}), merge: {total_merges} 次")
    
    overall_dedup_ratio = (total_walks_before - total_walks_after) / total_walks_before if total_walks_before > 0 else 0.0
    
    # 统计总的 merge 次数
    total_merges = sum(
        node_data.get("total_merges", 0)
        for node_data in node_results.values()
    )
    
    result = {
        "graph_path": graph_path,
        "max_steps": max_steps,
        "num_walks_per_node": num_walks_per_node,
        "num_nodes": len(node_indices),
        "total_walks_before_dedup": total_walks_before,
        "total_walks_after_dedup": total_walks_after,
        "overall_dedup_ratio": overall_dedup_ratio,
        "merge_probability": merge_probability,
        "total_merges": total_merges,
        "node_results": node_results,
    }
    
    # 打印总体统计
    print(f"\n" + "=" * 80)
    print(f"遍历完成！")
    print(f"总节点数: {len(node_indices)}")
    print(f"总路径数（去重前）: {total_walks_before}")
    print(f"总路径数（去重后）: {total_walks_after}")
    print(f"总体去重率: {overall_dedup_ratio:.2%}")
    print(f"Merge 概率: {merge_probability:.2%}")
    print(f"总 merge 次数: {total_merges}")
    print(f"=" * 80)
    
    # 如果需要，保存结果到 JSON 文件
    if save_json_path is not None:
        print(f"\n保存结果到 {save_json_path}...")
        os.makedirs(os.path.dirname(save_json_path), exist_ok=True)
        
        # 准备保存的数据，包含节点名称信息
        to_save = {
            "meta": {
                "graph_path": graph_path,
                "max_steps": max_steps,
                "num_walks_per_node": num_walks_per_node,
                "num_nodes": len(node_indices),
                "seed": seed,
            },
            "statistics": {
                "total_walks_before_dedup": total_walks_before,
                "total_walks_after_dedup": total_walks_after,
                "overall_dedup_ratio": overall_dedup_ratio,
            },
            "node_results": {
                node_idx: {
                    "name": node_data["name"],
                    "num_paths_before_dedup": node_data["num_paths_before_dedup"],
                    "num_paths_after_dedup": node_data["num_paths_after_dedup"],
                    "dedup_ratio": node_data["dedup_ratio"],
                    "paths_before_dedup": [
                        {
                            "walk_id": i,
                            "node_indices": path,
                            "node_names": [index_to_name.get(p, f"node_{p}") for p in path],
                            "path_length": len(path),
                        }
                        for i, path in enumerate(node_data["paths_before_dedup"], 1)
                    ],
                    "paths_after_dedup": [
                        {
                            "walk_id": i,
                            "node_indices": path,
                            "node_names": [index_to_name.get(p, f"node_{p}") for p in path],
                            "path_length": len(path),
                        }
                        for i, path in enumerate(node_data["paths_after_dedup"], 1)
                    ],
                    "merged_paths": node_data.get("merged_paths", []),
                    "total_merges": node_data.get("total_merges", 0),
                }
                for node_idx, node_data in node_results.items()
            },
        }
        
        with open(save_json_path, "w", encoding="utf-8") as f:
            json.dump(to_save, f, ensure_ascii=False, indent=2)
        print(f"结果已保存到 {save_json_path}")
    
    return result


def load_node_candidates_mapping(
    mapping_file: str = NODE_CANDIDATES_MAPPING_PATH,
) -> Dict[str, List[str]]:
    """
    加载节点候选映射文件。
    
    Args:
        mapping_file: node_candidates_mapping.json 文件路径
    
    Returns:
        dict: 节点名称 -> 候选节点名称列表的映射
    """
    print(f"Loading node candidates mapping from {mapping_file}...")
    with open(mapping_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    node_to_candidates = data.get("node_to_candidates", {})
    print(f"Loaded candidates for {len(node_to_candidates)} nodes")
    return node_to_candidates


def merge_paths_with_candidates(
    paths_after_dedup: List[List[int]],
    index_to_name: Dict[int, str],
    node_to_candidates: Dict[str, List[str]],
    name_to_index: Dict[str, int],
    merge_probability: float = 0.15,
    rng: random.Random = None,
) -> List[Dict[str, Any]]:
    """
    对去重后的路径进行 merge 操作。
    
    对每条路径的每个节点，以概率 p 选择是否 merge：
    - 如果选择 merge，从 node_candidates_mapping.json 中找到该节点的 candidates
    - 过滤掉已经在路径中的 candidates
    - 随机选择一个 candidate，添加到路径中（添加到同一层，不改变路径结构）
    
    Args:
        paths_after_dedup: 去重后的路径列表（每条路径是节点索引列表）
        index_to_name: 节点索引 -> 节点名称的映射
        node_to_candidates: 节点名称 -> 候选节点名称列表的映射
        name_to_index: 节点名称 -> 节点索引的映射
        merge_probability: 每个节点进行 merge 的概率
        rng: 随机数生成器
    
    Returns:
        List[Dict]: merge 后的路径列表，每个路径包含：
            - "path": 原始路径（节点索引列表）
            - "merged_path": merge 后的路径（节点索引列表，可能包含额外的候选节点）
            - "merge_info": 每个节点的 merge 信息
    """
    if rng is None:
        rng = random.Random()
    
    merged_paths = []
    total_merges = 0
    
    for path_idx, path in enumerate(paths_after_dedup):
        path_names = [index_to_name.get(node_idx, f"node_{node_idx}") for node_idx in path]
        merge_info = []
        
        # 第一步：收集所有需要 merge 的信息（不修改路径）
        merges_to_apply = []  # [(step_idx, candidate_name, candidate_idx), ...]
        
        for step_idx, (node_idx, node_name) in enumerate(zip(path, path_names)):
            step_merge_info = {
                "step_idx": step_idx,
                "node_idx": node_idx,
                "node_name": node_name,
                "merged": False,
                "merged_candidate": None,
                "merged_candidate_idx": None,
            }
            
            # 以概率 p 决定是否 merge
            if rng.random() < merge_probability:
                # 获取该节点的 candidates
                candidates = node_to_candidates.get(node_name, [])
                
                if candidates:
                    # 过滤掉已经在路径中的 candidates
                    available_candidates = [
                        cand for cand in candidates
                        if cand not in path_names and cand in name_to_index
                    ]
                    
                    if available_candidates:
                        # 随机选择一个 candidate
                        selected_candidate = rng.choice(available_candidates)
                        candidate_idx = name_to_index[selected_candidate]
                        
                        step_merge_info["merged"] = True
                        step_merge_info["merged_candidate"] = selected_candidate
                        step_merge_info["merged_candidate_idx"] = candidate_idx
                        total_merges += 1
                        
                        # 记录需要应用的 merge（从后往前插入，避免索引变化）
                        merges_to_apply.append((step_idx + 1, selected_candidate, candidate_idx))
            
            merge_info.append(step_merge_info)
        
        # 第二步：从后往前插入 candidates（避免索引变化）
        merged_path = path.copy()
        merged_path_names = path_names.copy()
        for insert_position, candidate_name, candidate_idx in reversed(merges_to_apply):
            merged_path.insert(insert_position, candidate_idx)
            merged_path_names.insert(insert_position, candidate_name)
        
        merged_paths.append({
            "path": path,
            "path_names": [index_to_name.get(node_idx, f"node_{node_idx}") for node_idx in path],
            "merged_path": merged_path,
            "merged_path_names": [index_to_name.get(node_idx, f"node_{node_idx}") for node_idx in merged_path],
            "merge_info": merge_info,
            "num_merges": sum(1 for info in merge_info if info["merged"]),
        })
    
    print(f"Merge 完成: {len(paths_after_dedup)} 条路径，共 {total_merges} 次 merge 操作")
    return merged_paths


def apply_merge_operation(
    fsp: List[List[int]],
    merge_probability: float = 0.3,
    rng: random.Random = None,
    index_to_name: Dict[int, str] = None,
) -> Tuple[List[List[int]], List[Dict[str, Any]]]:
    """
    应用 MAGNET 论文中的 Merge 操作：合并连续的 turn。

    论文描述 (Section 3.3.2):
    - 对每两个连续的 turn，以概率 p (默认30%) 进行合并
    - 合并后：turn 数量减少，每个 turn 内的函数数量可能增加
    - 目的：创建单轮中包含多个相关函数调用的场景（多意图）

    示例:
        输入 FSP:
            Turn 0: [get_distance]
            Turn 1: [set_navigation]
            Turn 2: [book_hotel]

        应用 Merge (假设 Turn0 和 Turn1 被合并):
            Turn 0: [get_distance, set_navigation]  ← 合并了！
            Turn 1: [book_hotel]

        生成的查询: "查询SF到SM的距离，并用这个距离设置导航" (多意图)

    Args:
        fsp: 函数签名路径，每个元素是一个 turn（函数索引列表）
        merge_probability: 合并概率 (论文中使用 0.3)
        rng: 随机数生成器
        index_to_name: 节点索引到名称的映射（用于日志）

    Returns:
        Tuple[新的FSP, merge日志列表]
        - 新的FSP: List[List[int]]
        - merge日志: List[Dict] 包含每次merge的详细信息
    """
    if rng is None:
        rng = random.Random()

    if index_to_name is None:
        index_to_name = {}

    merged_fsp = []
    merge_logs = []
    i = 0

    while i < len(fsp):
        current_turn = fsp[i]

        # 如果不是最后一个 turn，考虑是否与下一个 turn 合并
        if i < len(fsp) - 1 and rng.random() < merge_probability:
            next_turn = fsp[i + 1]

            # 合并两个 turn
            merged_turn = current_turn + next_turn
            merged_fsp.append(merged_turn)

            # 记录 merge 信息
            merge_log = {
                "turn_idx": i,
                "merged_turn_indices": [i, i + 1],
                "turn_0_functions": current_turn,
                "turn_1_functions": next_turn,
                "merged_functions": merged_turn,
                "turn_0_names": [index_to_name.get(idx, f"node_{idx}") for idx in current_turn],
                "turn_1_names": [index_to_name.get(idx, f"node_{idx}") for idx in next_turn],
                "merged_names": [index_to_name.get(idx, f"node_{idx}") for idx in merged_turn],
            }
            merge_logs.append(merge_log)

            i += 2  # 跳过下一个 turn（已被合并）
        else:
            # 不合并，直接添加当前 turn
            merged_fsp.append(current_turn)
            i += 1

    return merged_fsp, merge_logs


def apply_insert_operation(
    fsp: List[List[int]],
    adj: Dict[int, List[int]],
    insert_probability: float = 0.5,
    long_dependency_probability: float = 0.3,
    rng: random.Random = None,
    index_to_name: Dict[int, str] = None,
) -> Tuple[List[List[int]], List[Dict[str, Any]]]:
    """
    应用 MAGNET 论文中的 Insert 操作：添加嵌套函数调用。

    论文描述 (Section 3.3.1):
    - 对每个 turn 的最后一个函数，检查其邻居中是否有可嵌套的函数
    - 嵌套判断标准：第二个函数的参数值可从第一个函数输出获得，且在查询中未被明确提到
    - 两种插入方式：
      * 方式A (短依赖): 添加到当前 turn 内 → Turn: [f1] → Turn: [f1, f2]
      * 方式B (长依赖): 插入到后续随机 turn → Turn h: [f1], Turn h+k: [..., f2]
    - 目的：解决嵌套函数调用问题

    示例 (短依赖):
        输入 FSP:
            Turn 0: [get_distance]

        应用 Insert (get_distance 的邻居 convert_unit 被识别为嵌套):
            Turn 0: [get_distance, convert_unit]  ← 添加了嵌套函数！

        生成的查询: "查询从SF到SM多少公里"
        实际调用: get_distance(返回miles) → convert_unit(miles→km)
        用户只提到"公里"，但模型需要推断出要先获取miles再转换

    示例 (长依赖):
        输入 FSP:
            Turn 0: [get_distance]
            Turn 1: [book_hotel]
            Turn 2: [send_email]

        应用 Insert (convert_unit 被插入到 Turn 2):
            Turn 0: [get_distance]
            Turn 1: [book_hotel]
            Turn 2: [send_email, convert_unit]  ← 在后续 turn 使用 Turn 0 的输出！

    Args:
        fsp: 函数签名路径，每个元素是一个 turn（函数索引列表）
        adj: 邻接表，用于查找每个函数的后继函数（嵌套候选）
        insert_probability: 对每个 turn 尝试插入的概率
        long_dependency_probability: 插入为长依赖（后续turn）的概率，否则插入到当前turn
        rng: 随机数生成器
        index_to_name: 节点索引到名称的映射（用于日志）

    Returns:
        Tuple[新的FSP, insert日志列表]
        - 新的FSP: List[List[int]]
        - insert日志: List[Dict] 包含每次insert的详细信息
    """
    if rng is None:
        rng = random.Random()

    if index_to_name is None:
        index_to_name = {}

    # 复制 FSP，避免修改原始数据
    new_fsp = [turn.copy() for turn in fsp]
    insert_logs = []

    # 收集所有已在 FSP 中的函数（避免重复插入）
    functions_in_fsp = set()
    for turn in new_fsp:
        functions_in_fsp.update(turn)

    # 遍历每个 turn
    for turn_idx, turn in enumerate(new_fsp):
        # 对每个 turn，以概率 p 考虑插入
        if rng.random() >= insert_probability:
            continue

        # 检查 turn 的最后一个函数
        if not turn:
            continue

        last_func = turn[-1]
        neighbors = adj.get(last_func, [])

        if not neighbors:
            continue

        # 过滤掉已经在 FSP 中的邻居（避免重复）
        available_neighbors = [n for n in neighbors if n not in functions_in_fsp]

        if not available_neighbors:
            continue

        # 随机选择一个邻居作为嵌套函数
        nested_func = rng.choice(available_neighbors)
        functions_in_fsp.add(nested_func)  # 标记为已使用

        # 决定插入方式：短依赖（当前turn）还是长依赖（后续turn）
        is_long_dependency = rng.random() < long_dependency_probability

        if is_long_dependency and turn_idx < len(new_fsp) - 1:
            # 长依赖：插入到后续随机 turn
            # 选择一个后续 turn（turn_idx+1 到最后）
            target_turn_idx = rng.randint(turn_idx + 1, len(new_fsp) - 1)
            new_fsp[target_turn_idx].append(nested_func)

            insert_log = {
                "source_turn_idx": turn_idx,
                "source_func": last_func,
                "source_func_name": index_to_name.get(last_func, f"node_{last_func}"),
                "nested_func": nested_func,
                "nested_func_name": index_to_name.get(nested_func, f"node_{nested_func}"),
                "insert_type": "long_dependency",
                "target_turn_idx": target_turn_idx,
            }
        else:
            # 短依赖：插入到当前 turn
            new_fsp[turn_idx].append(nested_func)

            insert_log = {
                "source_turn_idx": turn_idx,
                "source_func": last_func,
                "source_func_name": index_to_name.get(last_func, f"node_{last_func}"),
                "nested_func": nested_func,
                "nested_func_name": index_to_name.get(nested_func, f"node_{nested_func}"),
                "insert_type": "short_dependency",
                "target_turn_idx": turn_idx,
            }

        insert_logs.append(insert_log)

    return new_fsp, insert_logs


def apply_split_operation(
    fsp: List[List[int]],
    split_probability: float = 0.15,
    rng: random.Random = None,
    index_to_name: Dict[int, str] = None,
) -> Tuple[List[List[int]], List[Dict[str, Any]]]:
    """
    应用 MAGNET 论文中的 Split 操作：创建信息缺失场景。

    论文描述 (Section 3.3.3):
    - 随机选择一个位置，在该位置插入一个空的 turn
    - 空 turn 标记为 'miss_func' 或 'miss_params'
    - 目的：训练模型识别和处理缺少功能或参数的情况

    示例:
        输入 FSP:
            Turn 0: [book_flight]
            Turn 1: [send_email]
            Turn 2: [get_weather]

        应用 Split (在 Turn 1 后插入空 turn):
            Turn 0: [book_flight]
            Turn 1: []  ← 空 turn，标记为 'miss_func'
            Turn 2: [send_email]
            Turn 3: [get_weather]

        生成的查询: 用户请求某个功能，但系统没有对应的函数
        模型应该输出: "我没有 XXX 功能，请确认..."

    Args:
        fsp: 函数签名路径，每个元素是一个 turn（函数索引列表）
        split_probability: 对整个 FSP 进行 split 的概率（不是每个 turn）
        rng: 随机数生成器
        index_to_name: 节点索引到名称的映射（用于日志）

    Returns:
        Tuple[新的FSP, split日志列表]
        - 新的FSP: List[List[int]]，可能包含空的 turn（用特殊值 -1 表示）
        - split日志: List[Dict] 包含每次split的详细信息
    """
    if rng is None:
        rng = random.Random()

    if index_to_name is None:
        index_to_name = {}

    # 对整个 FSP，以概率 p 决定是否进行 split
    if rng.random() >= split_probability:
        return fsp, []

    # 如果 FSP 为空或只有一个 turn，不进行 split
    if len(fsp) <= 1:
        return fsp, []

    # 随机选择一个插入位置（在 0 到 len(fsp) 之间）
    # 选择在某个 turn 之后插入
    insert_position = rng.randint(0, len(fsp) - 1)

    # 随机选择缺失类型：'miss_func' 或 'miss_params'
    miss_type = rng.choice(['miss_func', 'miss_params'])

    # 创建新的 FSP，在指定位置插入空 turn
    new_fsp = fsp[:insert_position + 1] + [[]] + fsp[insert_position + 1:]

    split_log = {
        "insert_position": insert_position,
        "miss_type": miss_type,
        "turn_before": fsp[insert_position] if insert_position < len(fsp) else [],
        "turn_before_names": [
            index_to_name.get(idx, f"node_{idx}")
            for idx in (fsp[insert_position] if insert_position < len(fsp) else [])
        ],
        "turn_after": fsp[insert_position + 1] if insert_position + 1 < len(fsp) else [],
        "turn_after_names": [
            index_to_name.get(idx, f"node_{idx}")
            for idx in (fsp[insert_position + 1] if insert_position + 1 < len(fsp) else [])
        ],
    }

    return new_fsp, [split_log]


def convert_flat_path_to_fsp(
    flat_path: List[int],
) -> List[List[int]]:
    """
    将扁平路径（每个节点一个turn）转换为 FSP 格式。

    Args:
        flat_path: 扁平路径，如 [idx1, idx2, idx3]

    Returns:
        FSP 格式: [[idx1], [idx2], [idx3]]
    """
    return [[node] for node in flat_path]


def convert_fsp_to_flat_path(
    fsp: List[List[int]],
) -> List[int]:
    """
    将 FSP 格式转换为扁平路径（用于向后兼容）。

    注意：这会丢失 turn 的边界信息！如果一个 turn 有多个函数，
    它们会被展平到一个列表中。

    Args:
        fsp: FSP 格式，如 [[idx1], [idx2, idx3], [idx4]]

    Returns:
        扁平路径: [idx1, idx2, idx3, idx4]
    """
    flat_path = []
    for turn in fsp:
        flat_path.extend(turn)
    return flat_path


if __name__ == "__main__":

    # 从每个节点出发，每个节点生成5条路径并去重
    result = run_walks_from_all_nodes_with_dedup(
        graph_path="/data/lhy/datasets/graph-Toucan/graph/graph_v1.json",
        max_steps=5,
        num_walks_per_node=5,
        seed=42,
        save_json_path='/data/lhy/datasets/graph-Toucan/walker_path/path_v1.json'
    )

    print(f"总节点数: {result['num_nodes']}")
    print(f"总路径数（去重前）: {result['total_walks_before_dedup']}")
    print(f"总路径数（去重后）: {result['total_walks_after_dedup']}")
    print(f"总体去重率: {result['overall_dedup_ratio']:.2%}")
