"""
生成 FSP v2：应用 MAGNET 论文的 Merge、Insert 和 Split 操作

Pipeline:
1. 加载现有的随机游走路径（path_v1.json）
2. 对每条路径应用节点操作（按论文顺序）：
   - Merge: 合并连续的 turn（论文 p=0.3）
   - Insert: 添加嵌套函数（短依赖/长依赖）
   - Split: 创建信息缺失场景（miss_func/miss_params）
3. 保存增强后的 FSP 到 fsp_v2.json
"""

import json
import os
import random
from typing import Dict, List, Any
from random_walker import (
    load_graph_for_walk,
    convert_flat_path_to_fsp,
    apply_merge_operation,
    apply_insert_operation,
    apply_split_operation,
)


def generate_fsp_v2(
    input_path: str,
    output_path: str,
    graph_path: str,
    merge_probability: float = 0.3,
    insert_probability: float = 0.5,
    long_dependency_probability: float = 0.3,
    split_probability: float = 0.15,
    seed: int = 42,
):
    """
    从现有的随机游走路径生成 FSP v2。

    Args:
        input_path: 输入的路径文件（path_v1.json）
        output_path: 输出的 FSP 文件（fsp_v2.json）
        graph_path: 图文件路径
        merge_probability: Merge 操作的概率（论文推荐 0.3）
        insert_probability: Insert 操作的概率（每个 turn）
        long_dependency_probability: Insert 为长依赖的概率
        split_probability: Split 操作的概率（论文推荐 0.15）
        seed: 随机种子
    """
    print("=" * 80)
    print("生成 FSP v2：应用 Merge、Insert 和 Split 操作")
    print("=" * 80)

    # 1. 加载图数据
    print(f"\n1. 加载图数据: {graph_path}")
    nodes, edges, index_to_name, adj = load_graph_for_walk(graph_path)
    print(f"   - 节点数: {len(nodes)}")
    print(f"   - 边数: {len(edges)}")

    # 2. 加载现有路径
    print(f"\n2. 加载现有路径: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        path_data = json.load(f)

    node_results = path_data.get("node_results", {})
    print(f"   - 节点数: {len(node_results)}")

    # 3. 统计信息
    stats = {
        "total_paths": 0,
        "total_turns_before": 0,
        "total_turns_after_merge": 0,
        "total_turns_after_insert": 0,
        "total_turns_final": 0,
        "total_functions_before": 0,
        "total_functions_final": 0,
        "total_merges": 0,
        "total_inserts": 0,
        "short_dependency_inserts": 0,
        "long_dependency_inserts": 0,
        "total_splits": 0,
    }

    # 4. 处理每个节点的路径
    print(f"\n3. 应用节点操作（Merge + Insert + Split）")
    print(f"   - Merge 概率: {merge_probability}")
    print(f"   - Insert 概率: {insert_probability}")
    print(f"   - 长依赖概率: {long_dependency_probability}")
    print(f"   - Split 概率: {split_probability}")

    rng = random.Random(seed)
    enhanced_results = {}

    for node_idx_str, node_data in node_results.items():
        node_idx = int(node_idx_str)
        node_name = node_data.get("name", f"node_{node_idx}")

        # 只处理去重后的路径
        paths_after_dedup = node_data.get("paths_after_dedup", [])

        if not paths_after_dedup:
            continue

        enhanced_paths = []

        for path_idx, path_data in enumerate(paths_after_dedup):
            # 提取节点索引列表
            if isinstance(path_data, dict):
                path = path_data.get("node_indices", [])
            else:
                path = path_data

            if not path:
                continue

            # 转换为 FSP 格式（每个节点一个 turn）
            fsp_initial = convert_flat_path_to_fsp(path)

            # 应用 Merge 操作（论文推荐先做 Merge）
            fsp_merged, merge_logs = apply_merge_operation(
                fsp=fsp_initial,
                merge_probability=merge_probability,
                rng=rng,
                index_to_name=index_to_name,
            )

            # 应用 Insert 操作（论文推荐在 Merge 后做 Insert）
            fsp_after_insert, insert_logs = apply_insert_operation(
                fsp=fsp_merged,
                adj=adj,
                insert_probability=insert_probability,
                long_dependency_probability=long_dependency_probability,
                rng=rng,
                index_to_name=index_to_name,
            )

            # 应用 Split 操作（论文推荐最后做 Split）
            fsp_final, split_logs = apply_split_operation(
                fsp=fsp_after_insert,
                split_probability=split_probability,
                rng=rng,
                index_to_name=index_to_name,
            )

            # 修复：Split 后更新所有受影响的 logs 的 turn_idx
            # Bug fix: 当 split 在某个位置插入空 turn 时，所有后续 turn 的索引 +1
            # 需要更新 insert_logs 和 merge_logs 中的 turn_idx
            if split_logs:
                for split_log in split_logs:
                    insert_position = split_log["insert_position"]

                    # 更新 insert_logs 中受影响的 turn_idx
                    for insert_log in insert_logs:
                        # target_turn_idx: 嵌套函数所在的 turn
                        if insert_log.get("target_turn_idx", -1) > insert_position:
                            insert_log["target_turn_idx"] += 1

                        # source_turn_idx: source 函数所在的 turn（long dependency）
                        if insert_log.get("source_turn_idx", -1) > insert_position:
                            insert_log["source_turn_idx"] += 1

                    # 更新 merge_logs 中受影响的 turn_idx
                    for merge_log in merge_logs:
                        if merge_log.get("turn_idx", -1) > insert_position:
                            merge_log["turn_idx"] += 1

            # 统计
            stats["total_paths"] += 1
            stats["total_turns_before"] += len(fsp_initial)
            stats["total_turns_after_merge"] += len(fsp_merged)
            stats["total_turns_after_insert"] += len(fsp_after_insert)
            stats["total_turns_final"] += len(fsp_final)
            stats["total_functions_before"] += len(path)
            stats["total_functions_final"] += sum(len(turn) for turn in fsp_final)
            stats["total_merges"] += len(merge_logs)
            stats["total_inserts"] += len(insert_logs)
            stats["short_dependency_inserts"] += sum(
                1 for log in insert_logs if log["insert_type"] == "short_dependency"
            )
            stats["long_dependency_inserts"] += sum(
                1 for log in insert_logs if log["insert_type"] == "long_dependency"
            )
            stats["total_splits"] += len(split_logs)

            # 构建增强路径数据
            enhanced_path = {
                "path_idx": path_idx,
                "original_path": path,
                "original_path_names": [
                    index_to_name.get(idx, f"node_{idx}") for idx in path
                ],
                "fsp_initial": fsp_initial,
                "fsp_merged": fsp_merged,
                "fsp_after_insert": fsp_after_insert,
                "fsp_final": fsp_final,
                "fsp_final_names": [
                    [index_to_name.get(idx, f"node_{idx}") for idx in turn]
                    for turn in fsp_final
                ],
                "statistics": {
                    "turns_initial": len(fsp_initial),
                    "turns_merged": len(fsp_merged),
                    "turns_after_insert": len(fsp_after_insert),
                    "turns_final": len(fsp_final),
                    "functions_initial": len(path),
                    "functions_final": sum(len(turn) for turn in fsp_final),
                    "num_merges": len(merge_logs),
                    "num_inserts": len(insert_logs),
                    "short_dependency_inserts": sum(
                        1 for log in insert_logs if log["insert_type"] == "short_dependency"
                    ),
                    "long_dependency_inserts": sum(
                        1 for log in insert_logs if log["insert_type"] == "long_dependency"
                    ),
                    "num_splits": len(split_logs),
                },
                "merge_logs": merge_logs,
                "insert_logs": insert_logs,
                "split_logs": split_logs,
            }

            enhanced_paths.append(enhanced_path)

        enhanced_results[node_idx_str] = {
            "node_idx": node_idx,
            "node_name": node_name,
            "num_paths": len(enhanced_paths),
            "paths": enhanced_paths,
        }

    # 5. 保存结果
    print(f"\n4. 保存结果到: {output_path}")

    output_data = {
        "meta": {
            "input_path": input_path,
            "graph_path": graph_path,
            "merge_probability": merge_probability,
            "insert_probability": insert_probability,
            "long_dependency_probability": long_dependency_probability,
            "seed": seed,
        },
        "statistics": stats,
        "node_results": enhanced_results,
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    # 6. 打印统计信息
    print(f"\n" + "=" * 80)
    print("生成完成！统计信息：")
    print("=" * 80)
    print(f"总路径数: {stats['total_paths']}")
    print(f"\nTurn 统计:")
    print(f"  - 初始 turns: {stats['total_turns_before']}")
    print(f"  - Merge 后 turns: {stats['total_turns_after_merge']}")
    print(f"  - Insert 后 turns: {stats['total_turns_after_insert']}")
    print(f"  - 最终 turns: {stats['total_turns_final']}")
    print(f"  - Turn 变化数: {stats['total_turns_final'] - stats['total_turns_before']} "
          f"(Merge减少 {stats['total_turns_before'] - stats['total_turns_after_merge']}, "
          f"Split增加 {stats['total_turns_final'] - stats['total_turns_after_insert']})")
    print(f"\n函数统计:")
    print(f"  - 初始函数数: {stats['total_functions_before']}")
    print(f"  - 最终函数数: {stats['total_functions_final']}")
    print(f"  - 新增函数数: {stats['total_functions_final'] - stats['total_functions_before']}")
    print(f"\n操作统计:")
    print(f"  - 总 Merge 次数: {stats['total_merges']}")
    print(f"  - 总 Insert 次数: {stats['total_inserts']}")
    print(f"    - 短依赖: {stats['short_dependency_inserts']}")
    print(f"    - 长依赖: {stats['long_dependency_inserts']}")
    print(f"  - 总 Split 次数: {stats['total_splits']}")
    print(f"\n平均统计:")
    if stats['total_paths'] > 0:
        print(f"  - 平均每条路径 turns: {stats['total_turns_final'] / stats['total_paths']:.2f}")
        print(f"  - 平均每条路径函数数: {stats['total_functions_final'] / stats['total_paths']:.2f}")
        print(f"  - 平均每条路径 merge 次数: {stats['total_merges'] / stats['total_paths']:.2f}")
        print(f"  - 平均每条路径 insert 次数: {stats['total_inserts'] / stats['total_paths']:.2f}")
        print(f"  - 平均每条路径 split 次数: {stats['total_splits'] / stats['total_paths']:.2f}")
    print("=" * 80)


def print_sample_paths(fsp_path: str, num_samples: int = 3):
    """打印一些示例路径，展示 Merge、Insert 和 Split 的效果"""
    print("\n" + "=" * 80)
    print(f"示例路径（展示前 {num_samples} 条）")
    print("=" * 80)

    with open(fsp_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    node_results = data.get("node_results", {})
    count = 0

    for node_idx, node_data in node_results.items():
        if count >= num_samples:
            break

        paths = node_data.get("paths", [])
        if not paths:
            continue

        for path in paths[:1]:  # 每个节点只展示第一条路径
            if count >= num_samples:
                break

            print(f"\n路径 {count + 1}: 节点 {node_data['node_name']}")
            print("-" * 80)

            # 原始路径
            print(f"原始路径 ({path['statistics']['functions_initial']} 函数, {path['statistics']['turns_initial']} turns):")
            for i, name in enumerate(path['original_path_names']):
                print(f"  Turn {i}: [{name}]")

            # Merge 后
            if path['statistics']['num_merges'] > 0:
                print(f"\nMerge 后 ({path['statistics']['num_merges']} 次合并, {path['statistics']['turns_merged']} turns):")
                for i, turn in enumerate(path['fsp_merged']):
                    turn_names = [data['meta'].get('index_to_name', {}).get(str(idx), f"node_{idx}") for idx in turn]
                    print(f"  Turn {i}: {turn_names}")

            # Insert 后
            if path['statistics']['num_inserts'] > 0:
                print(f"\nInsert 后 ({path['statistics']['num_inserts']} 次插入, {path['statistics']['turns_after_insert']} turns):")
                for i, turn in enumerate(path['fsp_after_insert']):
                    turn_names = [data.get('node_results', {}).get('0', {}).get('paths', [{}])[0].get('fsp_final_names', [[]])[0] if i == 0 else [] for idx in turn]
                    # 简化：直接显示索引
                    print(f"  Turn {i}: {turn}")

                # 打印 Insert 详情
                print(f"\nInsert 详情:")
                for log in path['insert_logs']:
                    print(f"  - Turn {log['source_turn_idx']}: {log['source_func_name']} "
                          f"→ 插入 {log['nested_func_name']} "
                          f"到 Turn {log['target_turn_idx']} ({log['insert_type']})")

            # Split 后（最终）
            if path['statistics']['num_splits'] > 0:
                print(f"\n最终 FSP ({path['statistics']['num_splits']} 次 split, {path['statistics']['turns_final']} turns):")
                for i, (turn, turn_names) in enumerate(zip(path['fsp_final'], path['fsp_final_names'])):
                    if not turn:  # 空 turn（split 插入的）
                        print(f"  Turn {i}: [] ← 空 turn (miss_func/miss_params)")
                    else:
                        print(f"  Turn {i}: {turn_names}")

                # 打印 Split 详情
                print(f"\nSplit 详情:")
                for log in path['split_logs']:
                    print(f"  - 在 Turn {log['insert_position']} 后插入空 turn")
                    print(f"    类型: {log['miss_type']}")
                    print(f"    前: {log['turn_before_names']}")
                    print(f"    后: {log['turn_after_names']}")
            elif path['statistics']['num_inserts'] > 0:
                # 如果没有 split，显示 insert 后的最终结果
                print(f"\n最终 FSP ({path['statistics']['functions_final']} 函数, {path['statistics']['turns_final']} turns):")
                for i, (turn, turn_names) in enumerate(zip(path['fsp_final'], path['fsp_final_names'])):
                    print(f"  Turn {i}: {turn_names}")

            count += 1


if __name__ == "__main__":
    # 配置路径
    INPUT_PATH = "/data/lhy/datasets/graph-Toucan/walker_path/path_v1.json"
    OUTPUT_PATH = "/data/lhy/datasets/graph-Toucan/walker_path/fsp_v2.json"
    GRAPH_PATH = "/data/lhy/datasets/graph-Toucan/graph/graph_v1.json"

    # 论文推荐的参数
    MERGE_PROBABILITY = 0.3  # 论文使用 30%
    INSERT_PROBABILITY = 0.5  # 每个 turn 50% 概率尝试插入
    LONG_DEPENDENCY_PROBABILITY = 0.3  # 30% 概率为长依赖
    SPLIT_PROBABILITY = 0.15  # 论文使用 15%

    # 生成 FSP v2
    generate_fsp_v2(
        input_path=INPUT_PATH,
        output_path=OUTPUT_PATH,
        graph_path=GRAPH_PATH,
        merge_probability=MERGE_PROBABILITY,
        insert_probability=INSERT_PROBABILITY,
        long_dependency_probability=LONG_DEPENDENCY_PROBABILITY,
        split_probability=SPLIT_PROBABILITY,
        seed=42,
    )

    # 打印示例路径
    print_sample_paths(OUTPUT_PATH, num_samples=5)

    print("\n✅ FSP v2 生成完成！")
    print(f"   输入: {INPUT_PATH}")
    print(f"   输出: {OUTPUT_PATH}")
