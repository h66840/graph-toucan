"""
找出构建的图中相比于原始数据"多了哪些边"。

方法1：基于真实 chain 中的相邻 step 关系
- 从所有 tool call chain 中提取相邻 step 的 tool pairs（A 在 step i，B 在 step i+1）
- 对于图中的每条边 (A → B)，检查是否存在真实 chain 中，A 和 B 在相邻 step 中出现的情况
- 如果从未出现，标记为"可能多余的边"
"""

import json
import os
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Any
from tqdm import tqdm


def load_graph(graph_path: str) -> Tuple[Dict[str, int], Dict[int, str], List[Dict[str, Any]]]:
    """
    加载图数据
    
    Returns:
        name_to_index: tool 名 -> 节点索引
        index_to_name: 节点索引 -> tool 名
        edges: 边的列表，每个边包含 source, target 等信息
    """
    print(f"Loading graph from {graph_path}...")
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    name_to_index: Dict[str, int] = {}
    index_to_name: Dict[int, str] = {}
    
    for node in nodes:
        idx = node.get("index")
        func_schema = node.get("function_schema", {}).get("function", {})
        name = func_schema.get("name")
        if name is not None and idx is not None:
            name_to_index[name] = idx
            index_to_name[idx] = name

    print(f"Loaded graph: {len(nodes)} nodes, {len(edges)} edges, {len(name_to_index)} named tools")
    return name_to_index, index_to_name, edges


def extract_adjacent_step_pairs(chains_path: str) -> Set[Tuple[str, str]]:
    """
    从 tool call chains 中提取所有相邻 step 的 tool pairs
    
    对于每个 turn 的 steps: S0, S1, ..., Sk-1
    提取所有 (tool_in_Si, tool_in_Si+1) 对，其中 i 从 0 到 k-2
    
    Returns:
        Set[Tuple[str, str]]: 所有相邻 step 的 tool pairs 集合
    """
    print(f"Loading tool call chains from {chains_path}...")
    with open(chains_path, "r", encoding="utf-8") as f:
        chains = json.load(f)
    print(f"Loaded {len(chains)} chains")

    adjacent_pairs: Set[Tuple[str, str]] = set()
    total_pairs = 0
    
    for sample in tqdm(chains, desc="Extracting adjacent step pairs"):
        chain_info = sample.get("chain_info", {})
        turns: List[Dict[str, Any]] = chain_info.get("turns", [])
        
        for turn in turns:
            steps: List[Dict[str, Any]] = turn.get("steps", [])
            
            # 对于每个相邻的 step 对 (step_i, step_i+1)
            for i in range(len(steps) - 1):
                step_i = steps[i]
                step_i_plus_1 = steps[i + 1]
                
                tools_i = step_i.get("tool_calls", []) or []
                tools_i_plus_1 = step_i_plus_1.get("tool_calls", []) or []
                
                # 提取所有 (tool_in_step_i, tool_in_step_i+1) 对
                # 注意：step_i 中可能有多个并行调用的 tool，step_i+1 中也可能有多个
                # 所以需要提取所有组合
                for tool_a in tools_i:
                    for tool_b in tools_i_plus_1:
                        if tool_a and tool_b:  # 确保都不是空字符串
                            adjacent_pairs.add((tool_a, tool_b))
                            total_pairs += 1

    print(f"\nExtracted {len(adjacent_pairs)} unique adjacent step pairs from {total_pairs} total pairs")
    return adjacent_pairs


def find_extra_edges(
    graph_path: str,
    chains_path: str,
    output_json_path: str = None,
) -> None:
    """
    找出图中相比于真实数据"多了哪些边"
    
    Args:
        graph_path: str, 图 JSON 文件路径
        chains_path: str, tool call chains JSON 文件路径
        output_json_path: str or None, 如果提供则保存结果到 JSON 文件
    """
    # 1. 加载图
    name_to_index, index_to_name, edges = load_graph(graph_path)
    
    # 2. 提取真实数据中的相邻 step pairs
    adjacent_pairs = extract_adjacent_step_pairs(chains_path)
    
    # 3. 分析图中的每条边
    total_edges = len(edges)
    edges_with_real_support = 0
    edges_without_real_support = []
    
    print("\nAnalyzing graph edges...")
    for edge in tqdm(edges, desc="Checking edges"):
        src_idx = edge.get("source")
        tgt_idx = edge.get("target")
        
        if src_idx is None or tgt_idx is None:
            continue
        
        src_name = index_to_name.get(src_idx)
        tgt_name = index_to_name.get(tgt_idx)
        
        if not src_name or not tgt_name:
            continue
        
        # 检查这条边是否在真实数据中出现过（作为相邻 step pair）
        if (src_name, tgt_name) in adjacent_pairs:
            edges_with_real_support += 1
        else:
            # 这条边在真实数据中从未作为相邻 step 出现
            edges_without_real_support.append({
                "source": src_name,
                "target": tgt_name,
                "source_index": src_idx,
                "target_index": tgt_idx,
                "confidence": edge.get("confidence", None),
                "dependency_type": edge.get("dependency_type", None),
            })
    
    # 4. 打印统计信息
    print("\n" + "=" * 80)
    print("Extra Edges Analysis (Method 1: Adjacent Step Pairs)")
    print("=" * 80)
    print(f"Total edges in graph: {total_edges}")
    print(f"Edges with real data support (adjacent step pairs): {edges_with_real_support}")
    print(f"Edges without real data support (possible extra edges): {len(edges_without_real_support)}")
    if total_edges > 0:
        support_rate = edges_with_real_support / total_edges * 100
        extra_rate = len(edges_without_real_support) / total_edges * 100
        print(f"Real data support rate: {support_rate:.2f}%")
        print(f"Possible extra edges rate: {extra_rate:.2f}%")
    print("=" * 80)
    
    # 5. 按依赖类型统计
    if edges_without_real_support:
        print("\nExtra edges by dependency type:")
        dep_type_counts = defaultdict(int)
        for edge in edges_without_real_support:
            dep_type = edge.get("dependency_type", "unknown")
            dep_type_counts[dep_type] += 1
        
        for dep_type, count in sorted(dep_type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {dep_type}: {count}")
    
    # 6. 打印一些示例
    if edges_without_real_support:
        print(f"\nExamples of extra edges (first 10):")
        for i, edge in enumerate(edges_without_real_support[:10]):
            print(f"  {i+1}. {edge['source']} -> {edge['target']} "
                  f"(type: {edge.get('dependency_type', 'unknown')}, "
                  f"confidence: {edge.get('confidence', 'N/A')})")
    
    # 7. 保存结果到 JSON
    if output_json_path:
        output_data = {
            "summary": {
                "total_edges": total_edges,
                "edges_with_real_support": edges_with_real_support,
                "edges_without_real_support": len(edges_without_real_support),
                "support_rate": edges_with_real_support / total_edges * 100 if total_edges > 0 else 0.0,
                "extra_rate": len(edges_without_real_support) / total_edges * 100 if total_edges > 0 else 0.0,
            },
            "extra_edges": edges_without_real_support,
        }
        
        print(f"\nSaving results to {output_json_path}...")
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"Results saved successfully!")
    
    return edges_without_real_support


def main():
    graph_path = os.path.join('/data/lhy/datasets/graph-Toucan/graph', "test_graph_v1.4.0_acyclic.json")
    chains_path = os.path.join('/data/lhy/datasets/graph-Toucan/tool_call_chain', "tool_call_chains_v2.json")
    #output_json_path = os.path.join('/data/lhy/datasets/graph-Toucan', "extra_edges_analysis.json")
    
    find_extra_edges(graph_path, chains_path)


if __name__ == "__main__":
    main()
