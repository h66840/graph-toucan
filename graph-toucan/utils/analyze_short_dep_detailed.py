#!/usr/bin/env python3
"""深入分析 short-dependency helper 是否在 query 中被明确提及"""

import json
import re
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

def extract_function_keywords(func_name: str) -> List[str]:
    """从函数名提取关键词"""
    # 移除 server/mcp 等通用词
    func_name = func_name.lower()
    # 按常见分隔符分割
    parts = re.split(r'[-_\.]', func_name)

    keywords = []
    for part in parts:
        # 过滤掉常见的无意义词
        if part not in ['mcp', 'server', 'tool', 'get', 'set', 'api', 'protocol', 'model', 'context']:
            if len(part) > 2:  # 过滤太短的词
                keywords.append(part)

    return keywords

def analyze_turn_with_operations(path_data: Dict, turn_data: Dict) -> Dict[str, Any]:
    """深入分析包含 turn_operations 的 turn"""
    turn_idx = turn_data.get('turn_idx', 'unknown')
    turn_type = turn_data.get('turn_type', '')
    query = turn_data.get('user_query', '').lower()
    functions = turn_data.get('functions', [])
    reason = turn_data.get('reason', '')

    # 查找原始的 turn_operations (如果存在的话)
    # 注意：生成的 jsonl 可能不包含原始的 turn_operations
    # 但我们可以从 reason 中推断

    analysis = {
        'turn_idx': turn_idx,
        'turn_type': turn_type,
        'query': turn_data.get('user_query', ''),
        'functions': functions,
        'short_dep_helpers': [],
        'long_dep_functions': [],
        'merged_functions': [],
        'issues': []
    }

    # 对于 merged_with_insert，分析 reason 来判断哪些是 short-dep
    if turn_type == 'merged_with_insert':
        reason_lower = reason.lower()

        # 检查 reason 中是否提到 short-dependency
        if 'short-dependency' in reason_lower or 'short dependency' in reason_lower:
            # 尝试从 reason 中提取 short-dep 函数
            for func in functions:
                func_lower = func.lower()
                func_keywords = extract_function_keywords(func)

                # 检查 reason 中是否说这个函数是 short-dep helper
                for keyword in func_keywords:
                    if keyword in reason_lower:
                        # 查找这个关键词周围的上下文
                        pattern = rf'.{{0,100}}{re.escape(keyword)}.{{0,100}}short.{{0,20}}dep'
                        match = re.search(pattern, reason_lower, re.IGNORECASE)
                        if match:
                            analysis['short_dep_helpers'].append(func)

                            # 检查这个函数的关键词是否在 query 中
                            for kw in func_keywords:
                                if kw in query:
                                    analysis['issues'].append({
                                        'type': 'short_dep_mentioned',
                                        'function': func,
                                        'keyword': kw,
                                        'detail': f"Short-dep helper '{func}' has keyword '{kw}' mentioned in query"
                                    })
                            break

        # 检查是否提到 long-dependency
        if 'long-dependency' in reason_lower or 'long dependency' in reason_lower:
            for func in functions:
                func_lower = func.lower()
                func_keywords = extract_function_keywords(func)

                for keyword in func_keywords:
                    if keyword in reason_lower:
                        pattern = rf'.{{0,100}}{re.escape(keyword)}.{{0,100}}long.{{0,20}}dep'
                        match = re.search(pattern, reason_lower, re.IGNORECASE)
                        if match:
                            analysis['long_dep_functions'].append(func)
                            break

    elif turn_type == 'insert_short':
        # 对于 insert_short，需要区分主函数和插入的 helper
        # 从 reason 中判断
        reason_lower = reason.lower()

        # 查找提到 "implicit", "helper", "background" 的函数
        for func in functions:
            func_keywords = extract_function_keywords(func)

            for keyword in func_keywords:
                if keyword in reason_lower:
                    # 检查这个关键词周围是否有 implicit/helper/background
                    pattern = rf'.{{0,150}}{re.escape(keyword)}.{{0,150}}(implicit|helper|background|automatically|not.{{0,20}}mention)'
                    match = re.search(pattern, reason_lower, re.IGNORECASE)
                    if match:
                        analysis['short_dep_helpers'].append(func)

                        # 检查是否在 query 中被提及
                        for kw in func_keywords:
                            if kw in query:
                                analysis['issues'].append({
                                    'type': 'short_dep_mentioned',
                                    'function': func,
                                    'keyword': kw,
                                    'detail': f"Short-dep helper '{func}' has keyword '{kw}' mentioned in query"
                                })
                        break

    return analysis

def main():
    # 加载数据
    data = load_jsonl('/data/lhy/datasets/graph-Toucan/fsp_path/fsp_v2_queries.jsonl')
    print(f"Total paths loaded: {len(data)}")

    # 分析所有 merged_with_insert 和 insert_short
    target_types = ['merged_with_insert', 'insert_short', 'insert_mixed']

    all_issues = []
    no_issue_count = 0

    for path in data:
        path_idx = path.get('path_info', {}).get('path_idx', 'unknown')
        node_idx = path.get('path_info', {}).get('node_idx', 'unknown')

        for turn in path.get('turns_data', []):
            turn_type = turn.get('turn_type', '')

            if turn_type in target_types:
                analysis = analyze_turn_with_operations(path, turn)

                if analysis['issues']:
                    all_issues.append({
                        'path_idx': path_idx,
                        'node_idx': node_idx,
                        'turn_idx': analysis['turn_idx'],
                        'turn_type': turn_type,
                        'query': analysis['query'],
                        'functions': analysis['functions'],
                        'short_dep_helpers': analysis['short_dep_helpers'],
                        'issues': analysis['issues'],
                        'reason': turn.get('reason', '')[:300]
                    })
                else:
                    no_issue_count += 1

    print(f"\n{'='*80}")
    print(f"Analysis Summary")
    print(f"{'='*80}")
    print(f"Total turns analyzed: {no_issue_count + len(all_issues)}")
    print(f"Turns with NO issues: {no_issue_count}")
    print(f"Turns with ISSUES: {len(all_issues)}")

    if all_issues:
        print(f"\n{'='*80}")
        print(f"Detailed Issue Report")
        print(f"{'='*80}\n")

        for i, issue_turn in enumerate(all_issues, 1):
            print(f"[Issue {i}] Path {issue_turn['node_idx']}-{issue_turn['path_idx']}, "
                  f"Turn {issue_turn['turn_idx']}, Type: {issue_turn['turn_type']}")
            print(f"Functions: {issue_turn['functions']}")
            print(f"Short-dep helpers: {issue_turn['short_dep_helpers']}")
            print(f"Query: {issue_turn['query']}")
            print(f"\nIssues found:")
            for issue in issue_turn['issues']:
                print(f"  ❌ {issue['detail']}")
            print(f"\nReason (first 300 chars):\n{issue_turn['reason']}")
            print(f"{'-'*80}\n")

    # 统计问题类型
    if all_issues:
        print(f"\n{'='*80}")
        print(f"Statistics")
        print(f"{'='*80}")

        by_type = {}
        for issue_turn in all_issues:
            turn_type = issue_turn['turn_type']
            by_type[turn_type] = by_type.get(turn_type, 0) + 1

        print(f"Issues by turn type:")
        for turn_type, count in sorted(by_type.items()):
            print(f"  {turn_type}: {count}")

        # 找出最常见的问题函数
        problem_funcs = {}
        for issue_turn in all_issues:
            for helper in issue_turn['short_dep_helpers']:
                problem_funcs[helper] = problem_funcs.get(helper, 0) + 1

        print(f"\nMost problematic functions:")
        for func, count in sorted(problem_funcs.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {func}: {count} times")

if __name__ == '__main__':
    main()
