"""
结构一致性验证 (Structural Consistency Verification)

创新点 2: 验证工具调用轨迹在图中的连通性

核心思路: 检查实际的工具调用序列中，每两个连续调用之间是否存在有向边
"""

import json
from collections import defaultdict
from typing import Any, Dict, List, Set, Tuple


class GraphConnectivityVerifier:
    """图连通性验证器"""

    def __init__(self, graph_data: Dict[str, Any]):
        """
        初始化验证器

        Args:
            graph_data: 图数据，包含 nodes 和 edges
        """
        self.graph = graph_data
        self.nodes = graph_data.get('nodes', [])
        self.edges = graph_data.get('edges', [])

        # 构建 function_name -> node_index 的映射
        self.name_to_index = {}
        for node in self.nodes:
            func_name = node.get('function_schema', {}).get('function', {}).get('name', '')
            if func_name:
                self.name_to_index[func_name] = node.get('index')

        # 构建邻接矩阵/集合: (source, target) -> edge_info
        self.edge_set = set()
        self.edge_info_map = {}
        for edge in self.edges:
            source = edge.get('source')
            target = edge.get('target')
            if source is not None and target is not None:
                self.edge_set.add((source, target))
                self.edge_info_map[(source, target)] = edge

    def verify_call_sequence(self, tool_calls: List[Dict[str, Any]]) -> Tuple[bool, List[Dict]]:
        """
        验证工具调用序列在图中的连通性

        Args:
            tool_calls: 工具调用列表，每个元素包含 {'name': str, ...}

        Returns:
            (is_connected, transition_details):
                - is_connected: 整个序列是否连通
                - transition_details: 每个转换的详情列表
        """
        if len(tool_calls) <= 1:
            # 单个或零个工具调用，视为连通
            return True, []

        transition_details = []
        all_connected = True

        for i in range(len(tool_calls) - 1):
            current_tool = tool_calls[i].get('name', '')
            next_tool = tool_calls[i + 1].get('name', '')

            current_idx = self.name_to_index.get(current_tool)
            next_idx = self.name_to_index.get(next_tool)

            transition = {
                'step': i + 1,
                'from_tool': current_tool,
                'to_tool': next_tool,
                'from_index': current_idx,
                'to_index': next_idx,
                'has_edge': False,
                'edge_info': None,
            }

            # 检查是否存在从 current 到 next 的边
            if current_idx is not None and next_idx is not None:
                if (current_idx, next_idx) in self.edge_set:
                    transition['has_edge'] = True
                    transition['edge_info'] = self.edge_info_map[(current_idx, next_idx)]
                else:
                    all_connected = False
                    transition['reason'] = f"No edge from '{current_tool}' to '{next_tool}' in graph"
            else:
                # 工具不在图中，跳过检查（或视为不连通，取决于需求）
                if current_idx is None:
                    transition['reason'] = f"Tool '{current_tool}' not found in graph"
                if next_idx is None:
                    transition['reason'] = f"Tool '{next_tool}' not found in graph"
                # 这里选择不把"不在图中"视为错误，只是标记出来
                transition['has_edge'] = None  # None 表示无法判断

            transition_details.append(transition)

        return all_connected, transition_details


def load_graph(graph_path: str) -> Dict[str, Any]:
    """加载图数据"""
    with open(graph_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_distill_data(jsonl_path: str, max_samples: int = None) -> List[Dict[str, Any]]:
    """加载蒸馏数据"""
    samples = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f):
            if max_samples and line_num >= max_samples:
                break
            if line.strip():
                samples.append(json.loads(line))
    return samples


def verify_sample(
    sample: Dict[str, Any],
    verifier: GraphConnectivityVerifier
) -> Dict[str, Any]:
    """
    验证单个样本的所有 turn

    Args:
        sample: 蒸馏样本数据
        verifier: 验证器实例

    Returns:
        验证结果字典
    """
    result = {
        'path_info': sample.get('path_info', {}),
        'all_turns_connected': True,
        'turns': [],
        'total_turns': 0,
        'connected_turns': 0,
        'disconnected_turns': 0,
    }

    distilled_turns = sample.get('distilled_turns', [])
    result['total_turns'] = len(distilled_turns)

    for turn in distilled_turns:
        turn_idx = turn.get('turn_idx', 0)
        turn_type = turn.get('turn_type', 'unknown')
        generated_calls = turn.get('generated_tool_calls', [])

        # 验证这个 turn 的工具调用序列
        is_connected, transitions = verifier.verify_call_sequence(generated_calls)

        turn_result = {
            'turn_idx': turn_idx,
            'turn_type': turn_type,
            'is_connected': is_connected,
            'num_calls': len(generated_calls),
            'transitions': transitions,
        }

        result['turns'].append(turn_result)

        if is_connected:
            result['connected_turns'] += 1
        else:
            result['disconnected_turns'] += 1
            result['all_turns_connected'] = False

    return result


def main():
    """主函数：批量验证数据集"""

    # 配置路径
    graph_path = '/Users/plastic/Documents/code/biyesheji/graph-toucan/graph/graph_v1.json'
    distill_path = '/Users/plastic/Documents/code/biyesheji/graph-toucan/distill/distill_v3_toucan.jsonl'
    output_path = '/Users/plastic/Documents/code/biyesheji/graph-toucan/distill/verification_results.jsonl'

    # 加载图数据
    print(f"Loading graph from {graph_path}...")
    graph_data = load_graph(graph_path)
    print(f"  Loaded {len(graph_data.get('nodes', []))} nodes")
    print(f"  Loaded {len(graph_data.get('edges', []))} edges")

    # 初始化验证器
    verifier = GraphConnectivityVerifier(graph_data)

    # 加载蒸馏数据
    print(f"\nLoading distillation data from {distill_path}...")
    samples = load_distill_data(distill_path)
    print(f"  Loaded {len(samples)} samples")

    # 批量验证
    print("\nVerifying connectivity...")
    print("=" * 80)

    results = []
    total_turns = 0
    total_connected = 0
    total_disconnected = 0
    valid_samples = 0

    for idx, sample in enumerate(samples):
        result = verify_sample(sample, verifier)
        results.append(result)

        total_turns += result['total_turns']
        total_connected += result['connected_turns']
        total_disconnected += result['disconnected_turns']

        if result['all_turns_connected']:
            valid_samples += 1

        # 每100个样本打印一次进度
        if (idx + 1) % 100 == 0:
            print(f"Processed {idx + 1}/{len(samples)} samples...")

    # 保存结果
    print(f"\nSaving results to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

    # 打印统计信息
    print("\n" + "=" * 80)
    print("Verification Summary")
    print("=" * 80)
    print(f"Total samples: {len(samples)}")
    print(f"Valid samples (all turns connected): {valid_samples} ({valid_samples/len(samples)*100:.2f}%)")
    print(f"Invalid samples (some turns disconnected): {len(samples) - valid_samples} ({(len(samples)-valid_samples)/len(samples)*100:.2f}%)")
    print(f"\nTotal turns: {total_turns}")
    print(f"Connected turns: {total_connected} ({total_connected/total_turns*100:.2f}%)")
    print(f"Disconnected turns: {total_disconnected} ({total_disconnected/total_turns*100:.2f}%)")

    # 分析断连情况
    print("\n" + "=" * 80)
    print("Disconnection Analysis")
    print("=" * 80)

    disconnected_transitions = defaultdict(int)
    for result in results:
        for turn in result['turns']:
            if not turn['is_connected']:
                for trans in turn['transitions']:
                    if not trans.get('has_edge', True):
                        key = f"{trans['from_tool']} -> {trans['to_tool']}"
                        disconnected_transitions[key] += 1

    if disconnected_transitions:
        print("\nTop disconnected transitions:")
        for trans, count in sorted(disconnected_transitions.items(), key=lambda x: -x[1])[:20]:
            print(f"  [{count} times] {trans}")
    else:
        print("\nNo disconnected transitions found! All tool calls follow graph edges.")

    print("\n" + "=" * 80)
    print("Verification completed!")
    print("=" * 80)


if __name__ == '__main__':
    main()
