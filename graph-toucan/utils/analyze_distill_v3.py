#!/usr/bin/env python3
"""
分析 distill_v3.jsonl 的统计信息
"""

import json
from collections import Counter
from typing import List, Dict, Any


def analyze_distill_data(jsonl_path: str) -> Dict[str, Any]:
    """
    分析蒸馏数据

    Args:
        jsonl_path: JSONL 文件路径

    Returns:
        统计信息字典
    """
    total_records = 0
    total_turns = 0
    total_steps = 0

    # 用于统计分布
    turns_distribution = []  # 每条数据的 turns 数
    steps_per_turn_distribution = []  # 每个 turn 的 steps 数
    steps_per_record_distribution = []  # 每条数据的总 steps 数

    # 用于统计函数匹配率
    function_match_rates = []

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue

            data = json.loads(line)
            total_records += 1

            # 从 statistics 字段获取汇总信息
            stats = data.get('statistics', {})
            num_turns = stats.get('num_turns', 0)
            num_steps = stats.get('total_steps', 0)
            func_match_rate = stats.get('function_match_rate', 0.0)

            total_turns += num_turns
            total_steps += num_steps

            turns_distribution.append(num_turns)
            steps_per_record_distribution.append(num_steps)
            function_match_rates.append(func_match_rate)

            # 统计每个 turn 的 steps 数
            distilled_turns = data.get('distilled_turns', [])
            for turn in distilled_turns:
                turn_steps = len(turn.get('steps', []))
                steps_per_turn_distribution.append(turn_steps)

    # 计算平均值
    avg_turns = total_turns / total_records if total_records > 0 else 0
    avg_steps_per_turn = total_steps / total_turns if total_turns > 0 else 0
    avg_steps_per_record = total_steps / total_records if total_records > 0 else 0
    avg_func_match_rate = sum(function_match_rates) / len(function_match_rates) if function_match_rates else 0

    # 统计分布
    turns_counter = Counter(turns_distribution)
    steps_per_turn_counter = Counter(steps_per_turn_distribution)

    return {
        'total_records': total_records,
        'total_turns': total_turns,
        'total_steps': total_steps,
        'avg_turns_per_record': avg_turns,
        'avg_steps_per_turn': avg_steps_per_turn,
        'avg_steps_per_record': avg_steps_per_record,
        'avg_function_match_rate': avg_func_match_rate,
        'turns_distribution': dict(sorted(turns_counter.items())),
        'steps_per_turn_distribution': dict(sorted(steps_per_turn_counter.items())),
        'raw_data': {
            'turns_list': turns_distribution,
            'steps_per_turn_list': steps_per_turn_distribution,
            'steps_per_record_list': steps_per_record_distribution,
        }
    }


def print_analysis(stats: Dict[str, Any]) -> None:
    """
    打印分析结果

    Args:
        stats: 统计信息字典
    """
    print("=" * 80)
    print("DISTILL_V3.JSONL ANALYSIS REPORT")
    print("=" * 80)

    print(f"\n📊 Overall Statistics:")
    print(f"  Total records: {stats['total_records']}")
    print(f"  Total turns: {stats['total_turns']}")
    print(f"  Total steps: {stats['total_steps']}")

    print(f"\n📈 Average Metrics:")
    print(f"  Average turns per record: {stats['avg_turns_per_record']:.2f}")
    print(f"  Average steps per turn: {stats['avg_steps_per_turn']:.2f}")
    print(f"  Average steps per record: {stats['avg_steps_per_record']:.2f}")
    print(f"  Average function match rate: {stats['avg_function_match_rate']:.2%}")

    print(f"\n📋 Turns Distribution (turns per record):")
    turns_dist = stats['turns_distribution']
    for num_turns in sorted(turns_dist.keys()):
        count = turns_dist[num_turns]
        percentage = count / stats['total_records'] * 100
        bar = '█' * int(percentage / 2)
        print(f"  {num_turns} turns: {count:4d} records ({percentage:5.1f}%) {bar}")

    print(f"\n📋 Steps per Turn Distribution:")
    steps_dist = stats['steps_per_turn_distribution']
    for num_steps in sorted(steps_dist.keys()):
        count = steps_dist[num_steps]
        percentage = count / stats['total_turns'] * 100
        bar = '█' * int(percentage / 2)
        print(f"  {num_steps} steps: {count:4d} turns ({percentage:5.1f}%) {bar}")

    print(f"\n📋 Steps per Record Distribution:")
    raw_data = stats['raw_data']
    steps_per_record_counter = Counter(raw_data['steps_per_record_list'])
    for num_steps in sorted(steps_per_record_counter.keys()):
        count = steps_per_record_counter[num_steps]
        percentage = count / stats['total_records'] * 100
        bar = '█' * int(percentage / 2)
        print(f"  {num_steps} steps: {count:4d} records ({percentage:5.1f}%) {bar}")

    print("\n" + "=" * 80)


def main():
    jsonl_path = "/data/lhy/datasets/graph-Toucan/distill/distill_v3.jsonl"

    print(f"Loading data from {jsonl_path}...\n")

    stats = analyze_distill_data(jsonl_path)
    print_analysis(stats)

    # 可选：保存详细统计到 JSON 文件
    # output_path = "/data/lhy/datasets/graph-Toucan/distill/distill_v3_analysis.json"
    # with open(output_path, 'w', encoding='utf-8') as f:
    #     json.dump(stats, f, indent=2, ensure_ascii=False)
    # print(f"\nDetailed statistics saved to: {output_path}")


if __name__ == "__main__":
    main()
