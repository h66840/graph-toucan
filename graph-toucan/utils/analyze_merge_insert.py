#!/usr/bin/env python3
"""分析包含 merge/insert 操作的数据"""

import json
import random
from typing import List, Dict, Any

def load_jsonl(file_path: str) -> List[Dict]:
    """加载 JSONL 文件"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def extract_merge_insert_turns(data: List[Dict]) -> List[Dict]:
    """提取包含 merge/insert 操作的 turns"""
    merge_insert_turns = []

    for path in data:
        path_idx = path.get('path_info', {}).get('path_idx', 'unknown')
        node_idx = path.get('path_info', {}).get('node_idx', 'unknown')

        for turn in path.get('turns_data', []):
            turn_type = turn.get('turn_type', '')

            # 筛选包含 merge 或 insert 的 turn
            if turn_type in ['merged', 'insert_short', 'insert_long', 'insert_mixed', 'merged_with_insert']:
                merge_insert_turns.append({
                    'path_idx': path_idx,
                    'node_idx': node_idx,
                    'turn_idx': turn.get('turn_idx', 'unknown'),
                    'turn_type': turn_type,
                    'operations': turn.get('operations', []),
                    'functions': turn.get('functions', []),
                    'user_query': turn.get('user_query', ''),
                    'chose_func': turn.get('chose_func', []),
                    'reason': turn.get('reason', ''),
                })

    return merge_insert_turns

def check_short_dep_implicit(turn: Dict) -> Dict[str, Any]:
    """检查 short-dependency helper 是否在 query 中被提及"""
    query = turn['user_query'].lower()
    turn_type = turn['turn_type']

    issues = []

    # 对于 merged_with_insert, insert_short, insert_mixed，检查是否有 short-dep helper 被提及
    if turn_type in ['merged_with_insert', 'insert_short', 'insert_mixed']:
        # 简单的关键词检查
        suspicious_patterns = [
            ('temperature', 'temp'),
            ('coordinate', 'coord'),
            ('convert', 'conversion'),
            ('geocode', 'location'),
            ('get_live_temp', 'live temperature'),
            ('format', 'formatting'),
        ]

        for func, keyword in suspicious_patterns:
            if keyword in query:
                issues.append(f"Query mentions '{keyword}' which might indicate explicit mention of helper function")

    return {
        'has_issues': len(issues) > 0,
        'issues': issues
    }

def main():
    # 加载数据
    data = load_jsonl('/data/lhy/datasets/graph-Toucan/fsp_path/fsp_v2_queries.jsonl')
    print(f"Total paths loaded: {len(data)}")

    # 提取 merge/insert turns
    merge_insert_turns = extract_merge_insert_turns(data)
    print(f"Total merge/insert turns: {len(merge_insert_turns)}")

    # 统计各类型数量
    type_counts = {}
    for turn in merge_insert_turns:
        turn_type = turn['turn_type']
        type_counts[turn_type] = type_counts.get(turn_type, 0) + 1

    print("\nTurn type distribution:")
    for turn_type, count in sorted(type_counts.items()):
        print(f"  {turn_type}: {count}")

    # 随机抽样10条（如果不足10条则全部使用）
    sample_size = min(10, len(merge_insert_turns))
    sampled_turns = random.sample(merge_insert_turns, sample_size)

    print(f"\n{'='*80}")
    print(f"Analyzing {sample_size} sampled turns")
    print(f"{'='*80}\n")

    for i, turn in enumerate(sampled_turns, 1):
        print(f"[Sample {i}] Path {turn['node_idx']}-{turn['path_idx']}, Turn {turn['turn_idx']}, Type: {turn['turn_type']}")
        print(f"Operations: {turn['operations']}")
        print(f"Functions: {turn['functions']}")
        print(f"User Query: {turn['user_query']}")
        print(f"Chose Func: {turn['chose_func']}")
        print(f"Reason (first 200 chars): {turn['reason'][:200]}...")

        # 检查问题
        check_result = check_short_dep_implicit(turn)
        if check_result['has_issues']:
            print(f"⚠️  POTENTIAL ISSUES:")
            for issue in check_result['issues']:
                print(f"    - {issue}")
        else:
            print(f"✅ No obvious issues detected")

        print(f"{'-'*80}\n")

if __name__ == '__main__':
    main()
