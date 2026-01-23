"""
测试 MAGNET 论文中的 Merge 和 Insert 操作。

演示如何使用 apply_merge_operation 和 apply_insert_operation。
"""

import random
from random_walker import (
    apply_merge_operation,
    apply_insert_operation,
    convert_flat_path_to_fsp,
    load_graph_for_walk,
)


def test_merge_operation():
    """测试 Merge 操作"""
    print("=" * 80)
    print("测试 Merge 操作")
    print("=" * 80)

    # 创建一个简单的 FSP 示例
    # 假设这是随机游走生成的初始 FSP（每个 turn 只有 1 个函数）
    fsp_before = [
        [100],  # Turn 0: 函数 100
        [101],  # Turn 1: 函数 101
        [102],  # Turn 2: 函数 102
        [103],  # Turn 3: 函数 103
        [104],  # Turn 4: 函数 104
    ]

    # 创建函数名映射（用于日志）
    index_to_name = {
        100: "get_distance",
        101: "set_navigation",
        102: "book_hotel",
        103: "send_email",
        104: "get_weather",
    }

    print("\n初始 FSP (5个turn):")
    for i, turn in enumerate(fsp_before):
        names = [index_to_name.get(idx, f"node_{idx}") for idx in turn]
        print(f"  Turn {i}: {turn} → {names}")

    # 应用 Merge 操作
    rng = random.Random(42)
    fsp_after, merge_logs = apply_merge_operation(
        fsp=fsp_before,
        merge_probability=0.5,  # 50% 概率合并（方便演示）
        rng=rng,
        index_to_name=index_to_name,
    )

    print(f"\n应用 Merge 后 (共 {len(merge_logs)} 次合并):")
    for i, turn in enumerate(fsp_after):
        names = [index_to_name.get(idx, f"node_{idx}") for idx in turn]
        print(f"  Turn {i}: {turn} → {names}")

    print(f"\nMerge 详细日志:")
    for log in merge_logs:
        print(f"  合并 Turn {log['merged_turn_indices']}: "
              f"{log['turn_0_names']} + {log['turn_1_names']} "
              f"→ {log['merged_names']}")

    print(f"\n统计:")
    print(f"  原始 turn 数: {len(fsp_before)}")
    print(f"  合并后 turn 数: {len(fsp_after)}")
    print(f"  减少 turn 数: {len(fsp_before) - len(fsp_after)}")


def test_insert_operation():
    """测试 Insert 操作"""
    print("\n" + "=" * 80)
    print("测试 Insert 操作")
    print("=" * 80)

    # 创建一个简单的 FSP 示例
    fsp_before = [
        [200],  # Turn 0
        [201],  # Turn 1
        [202],  # Turn 2
        [203],  # Turn 3
    ]

    # 创建函数名映射
    index_to_name = {
        200: "get_flight_cost",
        201: "book_flight",
        202: "send_confirmation",
        203: "get_weather",
        # 潜在的嵌套函数
        210: "validate_card",
        211: "send_sms",
        212: "log_booking",
    }

    # 创建邻接表（定义哪些函数可以作为嵌套函数）
    adj = {
        200: [210, 211],  # get_flight_cost 的邻居：validate_card, send_sms
        201: [212],       # book_flight 的邻居：log_booking
        202: [211],       # send_confirmation 的邻居：send_sms
        203: [],          # get_weather 没有邻居
    }

    print("\n初始 FSP (4个turn):")
    for i, turn in enumerate(fsp_before):
        names = [index_to_name.get(idx, f"node_{idx}") for idx in turn]
        print(f"  Turn {i}: {turn} → {names}")

    print("\n邻接关系（嵌套候选）:")
    for func, neighbors in adj.items():
        func_name = index_to_name.get(func, f"node_{func}")
        neighbor_names = [index_to_name.get(n, f"node_{n}") for n in neighbors]
        print(f"  {func_name} → {neighbor_names}")

    # 应用 Insert 操作
    rng = random.Random(42)
    fsp_after, insert_logs = apply_insert_operation(
        fsp=fsp_before,
        adj=adj,
        insert_probability=0.8,  # 80% 概率尝试插入（方便演示）
        long_dependency_probability=0.3,  # 30% 概率插入为长依赖
        rng=rng,
        index_to_name=index_to_name,
    )

    print(f"\n应用 Insert 后 (共 {len(insert_logs)} 次插入):")
    for i, turn in enumerate(fsp_after):
        names = [index_to_name.get(idx, f"node_{idx}") for idx in turn]
        print(f"  Turn {i}: {turn} → {names}")

    print(f"\nInsert 详细日志:")
    for log in insert_logs:
        print(f"  Turn {log['source_turn_idx']}: {log['source_func_name']} "
              f"→ 插入 {log['nested_func_name']} "
              f"到 Turn {log['target_turn_idx']} ({log['insert_type']})")

    print(f"\n统计:")
    short_deps = sum(1 for log in insert_logs if log['insert_type'] == 'short_dependency')
    long_deps = sum(1 for log in insert_logs if log['insert_type'] == 'long_dependency')
    print(f"  短依赖插入: {short_deps}")
    print(f"  长依赖插入: {long_deps}")
    print(f"  总插入次数: {len(insert_logs)}")


def test_full_pipeline_with_real_graph():
    """使用真实图测试完整 Pipeline"""
    print("\n" + "=" * 80)
    print("测试完整 Pipeline（随机游走 → Merge → Insert）")
    print("=" * 80)

    # 加载真实图
    graph_path = "/data/lhy/datasets/graph-Toucan/graph/graph_v1.json"
    nodes, edges, index_to_name, adj = load_graph_for_walk(graph_path)

    # 1. 模拟随机游走生成的路径（扁平格式）
    # 这里为了演示，我们手动创建一个路径
    # 实际使用时，这应该来自 random_walk_from_node 的结果
    flat_path = list(index_to_name.keys())[:6]  # 取前6个节点

    print(f"\n1. 随机游走生成的路径:")
    path_names = [index_to_name.get(idx, f"node_{idx}") for idx in flat_path]
    print(f"   {flat_path}")
    print(f"   {path_names}")

    # 2. 转换为 FSP 格式（每个节点一个turn）
    fsp = convert_flat_path_to_fsp(flat_path)
    print(f"\n2. 转换为 FSP 格式 ({len(fsp)} turns):")
    for i, turn in enumerate(fsp):
        names = [index_to_name.get(idx, f"node_{idx}") for idx in turn]
        print(f"   Turn {i}: {turn} → {names}")

    # 3. 应用 Merge 操作
    rng = random.Random(42)
    fsp_merged, merge_logs = apply_merge_operation(
        fsp=fsp,
        merge_probability=0.3,
        rng=rng,
        index_to_name=index_to_name,
    )
    print(f"\n3. 应用 Merge ({len(merge_logs)} 次合并, {len(fsp)} → {len(fsp_merged)} turns):")
    for i, turn in enumerate(fsp_merged):
        names = [index_to_name.get(idx, f"node_{idx}") for idx in turn]
        print(f"   Turn {i}: {turn} → {names}")

    # 4. 应用 Insert 操作
    fsp_final, insert_logs = apply_insert_operation(
        fsp=fsp_merged,
        adj=adj,
        insert_probability=0.5,
        long_dependency_probability=0.3,
        rng=rng,
        index_to_name=index_to_name,
    )
    print(f"\n4. 应用 Insert ({len(insert_logs)} 次插入):")
    for i, turn in enumerate(fsp_final):
        names = [index_to_name.get(idx, f"node_{idx}") for idx in turn]
        print(f"   Turn {i}: {turn} → {names}")

    print(f"\n最终统计:")
    print(f"  初始 turns: {len(fsp)}")
    print(f"  Merge 后 turns: {len(fsp_merged)}")
    print(f"  最终 turns: {len(fsp_final)}")

    initial_funcs = sum(len(turn) for turn in fsp)
    final_funcs = sum(len(turn) for turn in fsp_final)
    print(f"  初始函数总数: {initial_funcs}")
    print(f"  最终函数总数: {final_funcs}")
    print(f"  新增函数数: {final_funcs - initial_funcs}")


if __name__ == "__main__":
    # 测试 Merge
    test_merge_operation()

    # 测试 Insert
    test_insert_operation()

    # 测试完整 Pipeline
    test_full_pipeline_with_real_graph()

    print("\n" + "=" * 80)
    print("所有测试完成！")
    print("=" * 80)
