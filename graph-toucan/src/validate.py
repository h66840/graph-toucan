"""
检查 tool call chain 在构建好的函数依赖图上的连通性。

- 使用 `tool_call_chains.json` 中由 `toucan-subset-tool-call-parser.py` 生成的链信息
  （每个样本对应若干 turn，每个 turn 中包含若干 step，每个 step 内可能有多个并行的 tool 调用）。
- 使用 `test_graph_v1.1.0.json` 中由 `contrust_graph.py` 生成的有向图：
  节点是 tool（function），边是有向依赖（source -> target）。

连通性判定策略（针对单个 turn）：
1. 将这一 turn 的 steps 视作有序序列 S0, S1, ..., Sk-1，
   其中每个 Si 是一个 tool 名的集合（并行调用）。
2. 令 reachable_prefix = S0 对应的图节点集合。
3. 对于每个后续 step Si (i >= 1)：
   - 取该 step 中在图上的节点集合 Ti。
   - 通过从 reachable_prefix 出发的多源 BFS，检查 Ti 中的每个节点是否都可达：
       * 允许多跳路径。
   - 若存在某个节点在图上从 reachable_prefix 不可达，则认为该 turn 的链不完全连通。
   - 若全部可达，则将 Ti 并入 reachable_prefix，继续处理下一 step。

并行调用的处理：
- 同一 step 内的多个 tool 视为“无内部顺序的并行前驱”，只要求它们为后续 step 提供潜在前驱。
- 我们不要求 step 内 tool 之间存在边。

主要函数：
- detect_cycles_in_graph(graph_path: str, max_cycles: int = 20) -> Dict[str, Any]
  检测有向图中是否存在环，并返回部分环路示例。
  
- detect_bidirectional_edges(graph_path: str) -> Dict[str, Any]
  检测有向图中是否存在双向边（即 A -> B 和 B -> A 同时存在）。
  
- remove_bidirectional_edges_randomly(graph_path: str, output_path: str, seed: int = 42) -> Dict[str, Any]
  检测图中的双向边，对每个双向边对随机选择保留其中一条，删除另一条，生成新图。
  
- remove_cycles_minimally(graph_path: str, output_path: str) -> Dict[str, Any]
  通过删除最少的边来消除图中的所有环。使用强连通分量（SCC）算法和贪心策略。
  
- check_all_chains(chains_path: str, graph_path: str, output_json_path: str = None) -> None
  读取 tool_call_chains.json 和 graph，检查所有样本的连通性，并打印统计信息。
"""

import json
import os
import random
from collections import deque
from typing import Dict, List, Set, Tuple, Any


def load_graph(graph_path: str) -> Tuple[Dict[str, int], Dict[int, List[int]]]:
    """
    从 test_graph_v1.1.0.json 加载图，构建：
    - name_to_index: tool 名 -> 节点索引
    - adj: 邻接表，index -> List[index]（有向边 source -> target）
    """
    print(f"Loading graph from {graph_path}...")
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    name_to_index: Dict[str, int] = {}
    for node in nodes:
        idx = node.get("index")
        func_schema = node.get("function_schema", {}).get("function", {})
        name = func_schema.get("name")
        if name is not None and idx is not None:
            name_to_index[name] = idx

    adj: Dict[int, List[int]] = {}
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src is None or tgt is None:
            continue
        adj.setdefault(src, []).append(tgt)

    print(f"Loaded graph: {len(nodes)} nodes, {len(edges)} edges, {len(name_to_index)} named tools")
    return name_to_index, adj


def detect_cycles_in_graph(graph_path: str, max_cycles: int = 20) -> Dict[str, Any]:
    """
    检测有向图中是否存在环，并返回部分环路示例。
    
    Args:
        graph_path: str, 图 JSON 文件路径
        max_cycles: int, 最多返回的环数量
        
    Returns:
        {
          "has_cycle": bool,
          "num_cycles_found": int,          # 实际发现记录下来的环数量（<= max_cycles）
          "cycles": [                      # 每个元素是一个 dict，包含 index 和 name 序列
              {
                  "node_indices": [int, ...],
                  "node_names": [str, ...],
              },
              ...
          ],
        }
    """
    print(f"\nChecking for cycles in graph from {graph_path}...")
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)
    
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    # index -> name 映射，便于打印
    index_to_name: Dict[int, str] = {}
    for node in nodes:
        idx = node.get("index")
        func_schema = node.get("function_schema", {}).get("function", {})
        name = func_schema.get("name", f"node_{idx}")
        if idx is not None:
            index_to_name[idx] = name

    # 构建邻接表
    adj: Dict[int, List[int]] = {}
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src is None or tgt is None:
            continue
        adj.setdefault(src, []).append(tgt)

    visited: Set[int] = set()
    in_stack: Set[int] = set()
    stack: List[int] = []
    cycles: List[Dict[str, List]] = []

    def dfs(u: int) -> None:
        if len(cycles) >= max_cycles:
            return
        visited.add(u)
        in_stack.add(u)
        stack.append(u)

        for v in adj.get(u, []):
            if v not in visited:
                dfs(v)
                if len(cycles) >= max_cycles:
                    break
            elif v in in_stack:
                # 发现一个环：从 v 到当前栈顶
                try:
                    start_idx = stack.index(v)
                    cycle_indices = stack[start_idx:] + [v]
                except ValueError:
                    continue

                # 归一化环（以最小 index 作为起点），降低重复记录概率
                if len(cycle_indices) > 1:
                    core = cycle_indices[:-1]
                    min_idx = min(core)
                    min_pos = core.index(min_idx)
                    norm_core = core[min_pos:] + core[:min_pos]
                    norm_cycle = norm_core + [norm_core[0]]

                    cycle_names = [index_to_name.get(idx, f"node_{idx}") for idx in norm_cycle]
                    cycle_dict = {
                        "node_indices": norm_cycle,
                        "node_names": cycle_names,
                    }
                    # 避免简单重复
                    if cycle_dict not in cycles:
                        cycles.append(cycle_dict)
                        if len(cycles) >= max_cycles:
                            break

        stack.pop()
        in_stack.remove(u)

    for node in nodes:
        idx = node.get("index")
        if idx is None or idx in visited:
            continue
        dfs(idx)
        if len(cycles) >= max_cycles:
            break

    return {
        "has_cycle": bool(cycles),
        "num_cycles_found": len(cycles),
        "cycles": cycles,
    }


def detect_bidirectional_edges(graph_path: str) -> Dict[str, Any]:
    """
    检测有向图中是否存在双向边（即 A -> B 和 B -> A 同时存在）。
    
    Args:
        graph_path: str, 图 JSON 文件路径
        
    Returns:
        {
          "has_bidirectional": bool,
          "num_bidirectional_pairs": int,    # 双向边对的数量
          "bidirectional_pairs": [         # 每个元素是一个双向边对
              {
                  "node_a_index": int,
                  "node_b_index": int,
                  "node_a_name": str,
                  "node_b_name": str,
                  "edge_a_to_b": dict,     # A -> B 这条边的详细信息
                  "edge_b_to_a": dict,      # B -> A 这条边的详细信息
              },
              ...
          ],
        }
    """
    print(f"\nChecking for bidirectional edges in graph from {graph_path}...")
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)
    
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    # index -> name 映射
    index_to_name: Dict[int, str] = {}
    for node in nodes:
        idx = node.get("index")
        func_schema = node.get("function_schema", {}).get("function", {})
        name = func_schema.get("name", f"node_{idx}")
        if idx is not None:
            index_to_name[idx] = name

    # 构建边集合：使用 (src, tgt) 元组表示
    edge_set: Set[Tuple[int, int]] = set()
    edge_info_map: Dict[Tuple[int, int], Dict[str, Any]] = {}
    
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src is None or tgt is None:
            continue
        edge_set.add((src, tgt))
        edge_info_map[(src, tgt)] = edge

    # 查找双向边对
    bidirectional_pairs: List[Dict[str, Any]] = []
    processed_pairs: Set[Tuple[int, int]] = set()  # 避免重复记录 (a, b) 和 (b, a)
    
    for (src, tgt) in edge_set:
        # 检查是否存在反向边 (tgt, src)
        if (tgt, src) in edge_set:
            # 确保只记录一次（按索引大小排序）
            pair_key = tuple(sorted([src, tgt]))
            if pair_key in processed_pairs:
                continue
            processed_pairs.add(pair_key)
            
            edge_a_to_b = edge_info_map.get((src, tgt), {})
            edge_b_to_a = edge_info_map.get((tgt, src), {})
            
            bidirectional_pairs.append({
                "node_a_index": src,
                "node_b_index": tgt,
                "node_a_name": index_to_name.get(src, f"node_{src}"),
                "node_b_name": index_to_name.get(tgt, f"node_{tgt}"),
                "edge_a_to_b": {
                    "dependency_type": edge_a_to_b.get("dependency_type", "unknown"),
                    "confidence": edge_a_to_b.get("confidence", None),
                },
                "edge_b_to_a": {
                    "dependency_type": edge_b_to_a.get("dependency_type", "unknown"),
                    "confidence": edge_b_to_a.get("confidence", None),
                },
            })

    return {
        "has_bidirectional": bool(bidirectional_pairs),
        "num_bidirectional_pairs": len(bidirectional_pairs),
        "bidirectional_pairs": bidirectional_pairs,
    }


def remove_bidirectional_edges_randomly(graph_path: str, output_path: str, seed: int = 42) -> Dict[str, Any]:
    """
    检测图中的双向边，对每个双向边对随机选择保留其中一条，删除另一条，生成新图。
    
    Args:
        graph_path: str, 输入图 JSON 文件路径
        output_path: str, 输出图 JSON 文件路径
        seed: int, 随机种子，用于可复现性
        
    Returns:
        {
          "original_edges": int,
          "removed_edges": int,
          "remaining_edges": int,
          "bidirectional_pairs_processed": int,
          "removed_edge_pairs": List[Tuple[str, str]],  # 被删除的边的 (source_name, target_name) 列表
        }
    """
    print(f"\nProcessing bidirectional edges: loading graph from {graph_path}...")
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)
    
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    original_edge_count = len(edges)
    
    # index -> name 映射
    index_to_name: Dict[int, str] = {}
    for node in nodes:
        idx = node.get("index")
        func_schema = node.get("function_schema", {}).get("function", {})
        name = func_schema.get("name", f"node_{idx}")
        if idx is not None:
            index_to_name[idx] = name
    
    # 构建边集合和映射
    edge_set: Set[Tuple[int, int]] = set()
    edge_list: List[Dict[str, Any]] = []  # 保留边的完整信息
    edge_info_map: Dict[Tuple[int, int], Dict[str, Any]] = {}
    
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src is None or tgt is None:
            continue
        edge_set.add((src, tgt))
        edge_list.append(edge)
        edge_info_map[(src, tgt)] = edge
    
    # 查找双向边对
    bidirectional_pairs: List[Tuple[int, int, int, int]] = []  # (src, tgt, src, tgt) 表示一对双向边
    processed_pairs: Set[Tuple[int, int]] = set()
    
    for (src, tgt) in edge_set:
        if (tgt, src) in edge_set:
            pair_key = tuple(sorted([src, tgt]))
            if pair_key in processed_pairs:
                continue
            processed_pairs.add(pair_key)
            bidirectional_pairs.append((src, tgt, tgt, src))
    
    # 随机选择保留哪条边
    random.seed(seed)
    edges_to_remove: Set[Tuple[int, int]] = set()
    removed_edge_pairs: List[Tuple[str, str]] = []
    
    for src, tgt, rev_src, rev_tgt in bidirectional_pairs:
        # 随机选择保留 src->tgt 或 tgt->src
        if random.random() < 0.5:
            # 保留 src->tgt，删除 tgt->src
            edges_to_remove.add((rev_src, rev_tgt))
            removed_edge_pairs.append((
                index_to_name.get(rev_src, f"node_{rev_src}"),
                index_to_name.get(rev_tgt, f"node_{rev_tgt}")
            ))
        else:
            # 保留 tgt->src，删除 src->tgt
            edges_to_remove.add((src, tgt))
            removed_edge_pairs.append((
                index_to_name.get(src, f"node_{src}"),
                index_to_name.get(tgt, f"node_{tgt}")
            ))
    
    # 过滤掉要删除的边
    filtered_edges = [
        edge for edge in edge_list
        if (edge.get("source"), edge.get("target")) not in edges_to_remove
    ]
    
    # 更新图结构
    graph["edges"] = filtered_edges
    graph["num_edges"] = len(filtered_edges)
    
    # 更新版本号（如果存在）
    if "version" in graph:
        # 尝试解析版本号并递增
        version = graph["version"]
        if isinstance(version, str) and version.startswith("v"):
            try:
                parts = version.split(".")
                if len(parts) >= 3:
                    major, minor, patch = parts[0], parts[1], parts[2]
                    patch_num = int(patch) if patch.isdigit() else 0
                    graph["version"] = f"{major}.{minor}.{patch_num + 1}"
            except:
                pass
    
    # 保存新图
    print(f"Saving processed graph to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"Graph saved successfully!")
    
    return {
        "original_edges": original_edge_count,
        "removed_edges": len(edges_to_remove),
        "remaining_edges": len(filtered_edges),
        "bidirectional_pairs_processed": len(bidirectional_pairs),
        "removed_edge_pairs": removed_edge_pairs,
    }


def find_strongly_connected_components(adj: Dict[int, List[int]], nodes: List[int]) -> List[List[int]]:
    """
    使用 Kosaraju 算法找到所有强连通分量（SCC）。
    
    Args:
        adj: 邻接表，index -> List[index]
        nodes: 所有节点索引列表
        
    Returns:
        List[List[int]]: 每个元素是一个SCC（节点索引列表）
    """
    # 第一步：构建反向图
    rev_adj: Dict[int, List[int]] = {}
    for u in adj:
        for v in adj[u]:
            rev_adj.setdefault(v, []).append(u)
    
    # 第二步：第一次DFS，记录完成时间
    visited: Set[int] = set()
    finish_order: List[int] = []
    
    def dfs1(u: int):
        visited.add(u)
        for v in adj.get(u, []):
            if v not in visited:
                dfs1(v)
        finish_order.append(u)
    
    for node in nodes:
        if node not in visited:
            dfs1(node)
    
    # 第三步：在反向图上按完成时间逆序DFS
    visited.clear()
    sccs: List[List[int]] = []
    
    def dfs2(u: int, component: List[int]):
        visited.add(u)
        component.append(u)
        for v in rev_adj.get(u, []):
            if v not in visited:
                dfs2(v, component)
    
    for node in reversed(finish_order):
        if node not in visited:
            component = []
            dfs2(node, component)
            if component:
                sccs.append(component)
    
    return sccs


def remove_cycles_minimally(graph_path: str, output_path: str) -> Dict[str, Any]:
    """
    通过删除最少的边来消除图中的所有环。
    
    使用强连通分量（SCC）算法和贪心策略：
    1. 找到所有强连通分量
    2. 对于每个包含多个节点的SCC（意味着有环），删除一条边来破坏环
    3. 使用贪心策略：选择删除后能破坏最多环的边
    
    Args:
        graph_path: str, 输入图 JSON 文件路径
        output_path: str, 输出图 JSON 文件路径
        
    Returns:
        {
          "original_edges": int,
          "removed_edges": int,
          "remaining_edges": int,
          "sccs_with_cycles": int,  # 包含环的SCC数量
          "removed_edges_info": List[Dict],  # 被删除的边的详细信息
        }
    """
    print(f"\nRemoving cycles minimally: loading graph from {graph_path}...")
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)
    
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    original_edge_count = len(edges)
    
    # index -> name 映射
    index_to_name: Dict[int, str] = {}
    node_indices: List[int] = []
    for node in nodes:
        idx = node.get("index")
        if idx is None:
            continue
        func_schema = node.get("function_schema", {}).get("function", {})
        name = func_schema.get("name", f"node_{idx}")
        index_to_name[idx] = name
        node_indices.append(idx)
    
    # 构建邻接表和边映射
    adj: Dict[int, List[int]] = {}
    edge_info_map: Dict[Tuple[int, int], Dict[str, Any]] = {}
    
    for edge in edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src is None or tgt is None:
            continue
        adj.setdefault(src, []).append(tgt)
        edge_info_map[(src, tgt)] = edge
    
    # 迭代删除边，直到没有环
    edges_to_remove: Set[Tuple[int, int]] = set()
    removed_edges_info: List[Dict[str, Any]] = []
    iteration = 0
    max_iterations = 100  # 防止无限循环
    
    while iteration < max_iterations:
        iteration += 1
        print(f"Iteration {iteration}: Finding strongly connected components...")
        
        # 重新构建当前图的邻接表（排除已删除的边）
        current_adj: Dict[int, List[int]] = {}
        for edge in edges:
            src = edge.get("source")
            tgt = edge.get("target")
            if src is None or tgt is None:
                continue
            if (src, tgt) in edges_to_remove:
                continue
            current_adj.setdefault(src, []).append(tgt)
        
        # 找到所有强连通分量
        sccs = find_strongly_connected_components(current_adj, node_indices)
        
        # 找出包含多个节点的SCC（这些SCC包含环）
        cyclic_sccs = [scc for scc in sccs if len(scc) > 1]
        
        if not cyclic_sccs:
            print(f"No cycles found after {iteration} iteration(s).")
            break
        
        print(f"Found {len(sccs)} SCCs, {len(cyclic_sccs)} contain cycles")
        
        # 对于每个包含环的SCC，删除一条边来破坏环
        iteration_removed = 0
        for scc in cyclic_sccs:
            # 构建这个SCC内部的子图
            scc_set = set(scc)
            scc_edges: List[Tuple[int, int]] = []
            
            for u in scc:
                for v in current_adj.get(u, []):
                    if v in scc_set:
                        scc_edges.append((u, v))
            
            if not scc_edges:
                continue
            
            # 贪心策略：删除置信度最低的边
            best_edge = None
            min_confidence = float('inf')
            
            for (u, v) in scc_edges:
                if (u, v) in edges_to_remove:
                    continue  # 已经标记删除
                edge_info = edge_info_map.get((u, v), {})
                confidence = edge_info.get("confidence", 1.0)
                if confidence < min_confidence:
                    min_confidence = confidence
                    best_edge = (u, v)
            
            if best_edge:
                edges_to_remove.add(best_edge)
                edge_info = edge_info_map.get(best_edge, {})
                removed_edges_info.append({
                    "source_index": best_edge[0],
                    "target_index": best_edge[1],
                    "source_name": index_to_name.get(best_edge[0], f"node_{best_edge[0]}"),
                    "target_name": index_to_name.get(best_edge[1], f"node_{best_edge[1]}"),
                    "confidence": edge_info.get("confidence", None),
                    "dependency_type": edge_info.get("dependency_type", "unknown"),
                    "scc_size": len(scc),
                    "iteration": iteration,
                })
                iteration_removed += 1
        
        print(f"Removed {iteration_removed} edges in this iteration")
        
        if iteration_removed == 0:
            # 如果这一轮没有删除任何边，说明无法继续破坏环
            print("Warning: Could not remove more edges to break cycles.")
            break
    
    if iteration >= max_iterations:
        print(f"Warning: Reached maximum iterations ({max_iterations}). Some cycles may remain.")
    
    # 过滤掉要删除的边
    filtered_edges = [
        edge for edge in edges
        if (edge.get("source"), edge.get("target")) not in edges_to_remove
    ]
    
    # 验证删除后是否还有环
    final_adj: Dict[int, List[int]] = {}
    for edge in filtered_edges:
        src = edge.get("source")
        tgt = edge.get("target")
        if src is None or tgt is None:
            continue
        final_adj.setdefault(src, []).append(tgt)
    
    final_sccs = find_strongly_connected_components(final_adj, node_indices)
    final_cyclic_sccs = [scc for scc in final_sccs if len(scc) > 1]
    
    if final_cyclic_sccs:
        print(f"WARNING: Still found {len(final_cyclic_sccs)} SCCs with cycles after removal.")
        print("This may indicate the algorithm needs improvement or there are complex cycles.")
    else:
        print("✓ Verification: No cycles remaining in the graph.")
    
    # 更新图结构
    graph["edges"] = filtered_edges
    graph["num_edges"] = len(filtered_edges)
    
    # 更新版本号
    if "version" in graph:
        version = graph["version"]
        if isinstance(version, str) and version.startswith("v"):
            try:
                parts = version.split(".")
                if len(parts) >= 3:
                    major, minor, patch = parts[0], parts[1], parts[2]
                    patch_num = int(patch) if patch.isdigit() else 0
                    graph["version"] = f"{major}.{minor}.{patch_num + 1}"
            except:
                pass
    
    # 保存新图
    print(f"Saving acyclic graph to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"Graph saved successfully!")
    
    return {
        "original_edges": original_edge_count,
        "removed_edges": len(edges_to_remove),
        "remaining_edges": len(filtered_edges),
        "iterations": iteration,
        "removed_edges_info": removed_edges_info,
    }


def single_hop_reach_all_targets(
    adj: Dict[int, List[int]],
    sources: Set[int],
    targets: Set[int],
) -> Tuple[bool, Set[int]]:
    """
    单跳版本：从多个源节点（sources）出发，只检查直接边，判断是否能到达 targets 中的所有节点。
    
    只检查是否存在直接边 source -> target，不允许多跳路径。

    返回:
        (all_reached, reached_targets)
        all_reached: bool，是否所有 targets 都可达（通过直接边）
        reached_targets: 实际可达的 target 节点集合
    """
    if not targets:
        return True, set()

    reached_targets: Set[int] = set()
    
    # 如果源节点本身就在 targets 中，先记录
    for s in sources:
        if s in targets:
            reached_targets.add(s)
    
    # 检查每个 source 的直接邻居是否在 targets 中
    for source in sources:
        neighbors = adj.get(source, [])
        for neighbor in neighbors:
            if neighbor in targets:
                reached_targets.add(neighbor)
                if reached_targets == targets:
                    return True, reached_targets

    return reached_targets == targets, reached_targets


def multi_source_reach_all_targets(
    adj: Dict[int, List[int]],
    sources: Set[int],
    targets: Set[int],
) -> Tuple[bool, Set[int]]:
    """
    多跳版本：从多个源节点（sources）出发做 BFS，判断是否能到达 targets 中的所有节点。
    
    允许多跳路径（transitive closure）。

    返回:
        (all_reached, reached_targets)
        all_reached: bool，是否所有 targets 都可达
        reached_targets: 实际可达的 target 节点集合
    """
    if not targets:
        return True, set()

    visited: Set[int] = set(sources)
    q: deque[int] = deque(sources)

    reached_targets: Set[int] = set()
    # 如果源节点本身就在 targets 中，先记录
    for s in sources:
        if s in targets:
            reached_targets.add(s)
    if reached_targets == targets:
        return True, reached_targets

    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if v not in visited:
                visited.add(v)
                q.append(v)
                if v in targets:
                    reached_targets.add(v)
                    if reached_targets == targets:
                        return True, reached_targets

    return reached_targets == targets, reached_targets


def check_chain_connectivity_for_turn(
    turn: Dict[str, Any],
    name_to_index: Dict[str, int],
    adj: Dict[int, List[int]],
) -> Dict[str, Any]:
    """
    针对单个 turn，检查其 tool call chain 在图上的连通性。

    返回:
        {
          "turn_index": int,
          "is_connected": bool,
          "missing_tools": List[str],      # 在图中找不到的 tool 名
          "unreachable_steps": [           # 哪些 step 中的哪些 tool 不可达
              {
                "step_index": int,
                "unreachable_tools": List[str]
              }, ...
          ]
        }
    """
    turn_index = turn.get("turn_index", 0)
    steps: List[Dict[str, Any]] = turn.get("steps", [])

    # 抽取每个 step 内的 tool 名，并映射到图节点
    step_tool_names: List[List[str]] = []
    step_node_sets: List[Set[int]] = []
    missing_tools: Set[str] = set()

    for step in steps:
        tools: List[str] = step.get("tool_calls", []) or []
        step_tool_names.append(tools)
        node_set: Set[int] = set()
        for name in tools:
            if name in name_to_index:
                node_set.add(name_to_index[name])
            else:
                missing_tools.add(name)
        step_node_sets.append(node_set)

    # 如果没有 step，视为 trivially connected
    if not steps:
        return {
            "turn_index": turn_index,
            "is_connected": True,
            "missing_tools": sorted(missing_tools),
            "unreachable_steps": [],
        }

    # reachable_prefix: 之前所有 step 中出现过的节点集合
    reachable_prefix: Set[int] = set(step_node_sets[0])

    unreachable_steps: List[Dict[str, Any]] = []

    # 从第 1 个 step 开始检查可达性
    for idx in range(1, len(steps)):
        step = steps[idx]
        step_index = step.get("step_index", idx)
        targets: Set[int] = step_node_sets[idx]

        # 当前 step 没有任何在图上的 tool，则跳过此 step 的检查
        if not targets:
            continue

        # 单跳版本：只检查直接边
        all_reached, reached_targets = single_hop_reach_all_targets(adj, reachable_prefix, targets)
        
        # 如果想改回多跳版本，取消下面这行的注释，并注释掉上面那行
        # all_reached, reached_targets = multi_source_reach_all_targets(adj, reachable_prefix, targets)
        if not all_reached:
            unreachable_indices = targets - reached_targets
            # 反查工具名
            unreachable_tool_names: List[str] = []
            # 我们只有 name_to_index: name -> index，需要反向映射
            for names, node_set in zip(step_tool_names, step_node_sets):
                pass  # 为了类型提示，不实际使用
            # 简单地反向查找
            for name, idx_node in name_to_index.items():
                if idx_node in unreachable_indices:
                    unreachable_tool_names.append(name)

            unreachable_steps.append(
                {
                    "step_index": step_index,
                    "unreachable_tools": sorted(set(unreachable_tool_names)),
                }
            )

        # 无论是否全部可达，都将本 step 中在图上的节点加入前缀，
        # 以便后续 step 可以从这里继续
        reachable_prefix |= targets

    is_connected = not unreachable_steps and not missing_tools

    return {
        "turn_index": turn_index,
        "is_connected": is_connected,
        "missing_tools": sorted(missing_tools),
        "unreachable_steps": unreachable_steps,
    }


def check_all_chains(
    chains_path: str,
    graph_path: str,
    output_json_path: str = None,
) -> None:
    """
    读取 tool_call_chains.json 和 graph，检查所有样本的连通性，并打印统计信息。
    
    Args:
        chains_path: str, tool_call_chains.json 文件路径
        graph_path: str, graph JSON 文件路径
        output_json_path: str or None, 如果提供则保存 examples_unreachable 和统计信息到 JSON 文件
    """
    name_to_index, adj = load_graph(graph_path)

    print(f"Loading tool call chains from {chains_path}...")
    with open(chains_path, "r", encoding="utf-8") as f:
        chains = json.load(f)
    print(f"Loaded {len(chains)} chains")

    total_turns = 0
    connected_turns = 0
    turns_with_missing_tools = 0
    turns_with_unreachable = 0

    # 可以保存一些典型不连通的示例，便于后续分析
    examples_unreachable: List[Dict[str, Any]] = []

    for sample in chains:
        if sample['chain_info']['summary']['total_steps'] == 1:
            continue
        uuid = sample.get("uuid", "")
        chain_info = sample.get("chain_info", {})
        turns: List[Dict[str, Any]] = chain_info.get("turns", [])

        for turn in turns:
            total_turns += 1
            result = check_chain_connectivity_for_turn(turn, name_to_index, adj)

            if result["is_connected"]:
                connected_turns += 1
            else:
                if result["missing_tools"]:
                    turns_with_missing_tools += 1
                if result["unreachable_steps"]:
                    turns_with_unreachable += 1
                    # all add
                    #if len(examples_unreachable) < 5:
                    examples_unreachable.append(
                        {
                            "uuid": uuid,
                            "turn_index": result["turn_index"],
                            "missing_tools": result["missing_tools"],
                            "unreachable_steps": result["unreachable_steps"],
                        }
                    )

    print("\n" + "=" * 80)
    print("Tool Call Chain Connectivity Check")
    print("=" * 80)
    print(f"Total turns: {total_turns}")
    print(f"Connected turns: {connected_turns}")
    print(f"Turns with missing tools: {turns_with_missing_tools}")
    print(f"Turns with unreachable steps: {turns_with_unreachable}")
    if total_turns > 0:
        print(f"Connectivity rate: {connected_turns / total_turns * 100:.2f}%")
    print("=" * 80)

    if examples_unreachable:
        print(f"\nTotal unreachable examples collected: {len(examples_unreachable)}")
        print("\nExamples of unreachable chains (first 5):")
        for ex in examples_unreachable[:5]:
            print("-" * 40)
            print(f"UUID: {ex['uuid']}, turn_index: {ex['turn_index']}")
            if ex["missing_tools"]:
                print(f"  Missing tools: {ex['missing_tools']}")
            for step_info in ex["unreachable_steps"]:
                print(
                    f"  Step {step_info['step_index']} unreachable tools: "
                    f"{step_info['unreachable_tools']}"
                )
        print("=" * 80)
    
    # 保存结果到 JSON 文件
    if output_json_path:
        output_data = {
            "summary": {
                "total_turns": total_turns,
                "connected_turns": connected_turns,
                "turns_with_missing_tools": turns_with_missing_tools,
                "turns_with_unreachable": turns_with_unreachable,
                "connectivity_rate": connected_turns / total_turns * 100 if total_turns > 0 else 0.0,
                "total_unreachable_examples": len(examples_unreachable),
            },
            "examples_unreachable": examples_unreachable,
        }
        
        print(f"\nSaving results to {output_json_path}...")
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"Results saved successfully! ({len(examples_unreachable)} unreachable examples)")


def main():
    
    graph_path = os.path.join('/data/lhy/datasets/graph-Toucan/graph', "test_graph_v1.4.0_acyclic.json")
    chains_path = os.path.join('/data/lhy/datasets/graph-Toucan/tool_call_chain', "tool_call_chains_v2.json")
    #output_json_path = os.path.join('/data/lhy/datasets/graph-Toucan', "unreachable_examples_analysis_v1.json")

    # 1. 检测图中是否存在环
    cycle_info = detect_cycles_in_graph(graph_path, max_cycles=200)
    print("\n" + "=" * 80)
    print("Cycle Detection Results")
    print("=" * 80)
    if cycle_info["has_cycle"]:
        print(f"WARNING: Detected {cycle_info['num_cycles_found']} cycles (showing up to 20).")
        print("\nCycle examples:")
        for idx, cyc in enumerate(cycle_info["cycles"], start=1):
            names = " -> ".join(cyc["node_names"])
            print(f"  Cycle {idx}: {names}")
    else:
        print("✓ No cycles detected in the graph.")
    print("=" * 80)
    
    
    # 1.1 如果检测到环，通过删除最少的边来消除所有环
    if cycle_info["has_cycle"]:
        output_acyclic_path = os.path.join('/data/lhy/datasets/graph-Toucan/graph', "test_graph_v1.4.0_acyclic.json")
        print("\n" + "=" * 80)
        print("Removing Cycles Minimally")
        print("=" * 80)
        removal_result = remove_cycles_minimally(
            graph_path=graph_path,
            output_path=output_acyclic_path
        )
        print(f"Original edges: {removal_result['original_edges']}")
        print(f"Removed edges: {removal_result['removed_edges']}")
        print(f"Remaining edges: {removal_result['remaining_edges']}")
        print(f"Iterations: {removal_result['iterations']}")
        print(f"\nRemoved edges (first 10):")
        for idx, edge_info in enumerate(removal_result['removed_edges_info'][:10], start=1):
            print(f"  {idx}. {edge_info['source_name']} -> {edge_info['target_name']} "
                  f"(SCC size: {edge_info.get('scc_size', 'N/A')}, "
                  f"iteration: {edge_info.get('iteration', 'N/A')}, "
                  f"confidence: {edge_info.get('confidence', 'N/A')}, "
                  f"type: {edge_info.get('dependency_type', 'unknown')})")
        if len(removal_result['removed_edges_info']) > 10:
            print(f"  ... and {len(removal_result['removed_edges_info']) - 10} more")
        print("=" * 80)
        print(f"\n✓ Acyclic graph saved to: {output_acyclic_path}")
    
    # 2. 检测双向边
    # bidirectional_info = detect_bidirectional_edges(graph_path)
    # print("\n" + "=" * 80)
    # print("Bidirectional Edges Detection Results")
    # print("=" * 80)
    # if bidirectional_info["has_bidirectional"]:
    #     print(f"Found {bidirectional_info['num_bidirectional_pairs']} bidirectional edge pairs.")
    #     print("\nBidirectional edge pairs (first 20):")
    #     for idx, pair in enumerate(bidirectional_info["bidirectional_pairs"][:20], start=1):
    #         print(f"  {idx}. {pair['node_a_name']} <-> {pair['node_b_name']}")
    #         print(f"     {pair['node_a_name']} -> {pair['node_b_name']}: "
    #               f"type={pair['edge_a_to_b']['dependency_type']}, "
    #               f"confidence={pair['edge_a_to_b'].get('confidence', 'N/A')}")
    #         print(f"     {pair['node_b_name']} -> {pair['node_a_name']}: "
    #               f"type={pair['edge_b_to_a']['dependency_type']}, "
    #               f"confidence={pair['edge_b_to_a'].get('confidence', 'N/A')}")
    #     if bidirectional_info['num_bidirectional_pairs'] > 20:
    #         print(f"  ... and {bidirectional_info['num_bidirectional_pairs'] - 20} more pairs")
    # else:
    #     print("✓ No bidirectional edges detected in the graph.")
    # print("=" * 80)
    
    # 2.1 处理双向边：随机选择保留一条，生成新图
    # if bidirectional_info["has_bidirectional"]:
    #     output_graph_path = os.path.join('/data/lhy/datasets/graph-Toucan/graph', "test_graph_v1.5.0_with_no_bidirectional_edge.json")
    #     print("\n" + "=" * 80)
    #     print("Processing Bidirectional Edges")
    #     print("=" * 80)
    #     removal_result = remove_bidirectional_edges_randomly(
    #         graph_path=graph_path,
    #         output_path=output_graph_path,
    #         seed=42
    #     )
    #     print(f"Original edges: {removal_result['original_edges']}")
    #     print(f"Removed edges: {removal_result['removed_edges']}")
    #     print(f"Remaining edges: {removal_result['remaining_edges']}")
    #     print(f"Bidirectional pairs processed: {removal_result['bidirectional_pairs_processed']}")
    #     print(f"\nRemoved edge pairs (first 10):")
    #     for idx, (src, tgt) in enumerate(removal_result['removed_edge_pairs'][:10], start=1):
    #         print(f"  {idx}. {src} -> {tgt}")
    #     if len(removal_result['removed_edge_pairs']) > 10:
    #         print(f"  ... and {len(removal_result['removed_edge_pairs']) - 10} more")
    #     print("=" * 80)
    #     print(f"\n✓ New graph saved to: {output_graph_path}")
    
    # 3. 检查连通性（使用原始图）
    check_all_chains(chains_path, graph_path)


if __name__ == "__main__":
    main()
