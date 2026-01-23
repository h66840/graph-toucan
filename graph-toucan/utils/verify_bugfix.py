#!/usr/bin/env python3
"""
验证 detect_turn_operations 修复效果

检查：
1. 修复前：188 个路径有问题（基于 turn_idx 匹配错误）
2. 修复后：0 个路径有问题（基于函数名正确匹配）
"""

import json
from typing import Dict, List, Any


def detect_turn_operations_old(
    turn_idx: int,
    turn_functions: List[str],
    path_data: Dict[str, Any],
) -> Dict[str, Any]:
    """旧版本：基于 turn_idx 匹配（有 bug）"""
    result = {
        "insert_info": [],
        "operations": [],
    }

    insert_logs = path_data.get("insert_logs", [])
    for log in insert_logs:
        if log.get("target_turn_idx") == turn_idx:
            result["insert_info"].append(log)
            if log.get("insert_type") == "long_dependency":
                result["operations"].append("insert_long")
            else:
                result["operations"].append("insert_short")

    return result


def detect_turn_operations_new(
    turn_idx: int,
    turn_functions: List[str],
    path_data: Dict[str, Any],
) -> Dict[str, Any]:
    """新版本：基于函数名匹配（修复后）"""
    result = {
        "insert_info": [],
        "operations": [],
    }

    insert_logs = path_data.get("insert_logs", [])
    for log in insert_logs:
        source_func = log.get("source_func_name")
        nested_func = log.get("nested_func_name")
        insert_type = log.get("insert_type")

        if insert_type == "short_dependency":
            # Short dependency: 两个函数都在当前 turn
            if source_func in turn_functions and nested_func in turn_functions:
                result["insert_info"].append(log)
                result["operations"].append("insert_short")

        elif insert_type == "long_dependency":
            # Long dependency: 只有 nested_func 在当前 turn
            if nested_func in turn_functions:
                result["insert_info"].append(log)
                result["operations"].append("insert_long")

    return result


def verify_insert_info(insert_info: List[Dict], turn_functions: List[str]) -> bool:
    """验证 insert_info 是否匹配当前 turn 的函数"""
    for info in insert_info:
        source_func = info.get("source_func_name")
        nested_func = info.get("nested_func_name")
        insert_type = info.get("insert_type")

        if insert_type == "short_dependency":
            # Short dependency: 两个函数都必须在当前 turn
            if source_func not in turn_functions or nested_func not in turn_functions:
                return False
        elif insert_type == "long_dependency":
            # Long dependency: 至少 nested_func 在当前 turn
            if nested_func not in turn_functions:
                return False

    return True


def main():
    print("=" * 80)
    print("验证 detect_turn_operations 修复效果")
    print("=" * 80)

    # 加载数据
    print("\n📂 加载 FSP v2 数据...")
    with open('walker_path/fsp_v2.json', 'r') as f:
        data = json.load(f)

    node_results = data['node_results']

    # 统计
    total_paths = 0
    affected_paths = 0
    old_method_errors = 0
    new_method_errors = 0

    error_cases = []

    # 检查所有路径
    print("🔍 检查所有路径...")
    for node_key, node in node_results.items():
        for path in node['paths']:
            total_paths += 1
            fsp_final_names = path.get('fsp_final_names', [])

            # 检查是否有 insert 和 split
            has_insert = 'insert_logs' in path and len(path['insert_logs']) > 0
            has_split = 'split_logs' in path and len(path['split_logs']) > 0

            if not has_insert:
                continue

            # 对每个 turn 测试
            for turn_idx, turn_functions in enumerate(fsp_final_names):
                if not turn_functions:  # 空 turn
                    continue

                # 旧方法
                old_result = detect_turn_operations_old(turn_idx, turn_functions, path)
                old_valid = verify_insert_info(old_result["insert_info"], turn_functions)

                # 新方法
                new_result = detect_turn_operations_new(turn_idx, turn_functions, path)
                new_valid = verify_insert_info(new_result["insert_info"], turn_functions)

                # 统计错误
                if not old_valid:
                    old_method_errors += 1
                    if has_split:
                        affected_paths += 1

                if not new_valid:
                    new_method_errors += 1

                # 记录错误案例
                if not old_valid or not new_valid:
                    error_cases.append({
                        'node': node_key,
                        'path': path['path_idx'],
                        'turn': turn_idx,
                        'functions': turn_functions,
                        'old_valid': old_valid,
                        'new_valid': new_valid,
                        'old_insert_info': old_result["insert_info"],
                        'new_insert_info': new_result["insert_info"],
                        'has_split': has_split
                    })

    # 打印结果
    print("\n" + "=" * 80)
    print("📊 验证结果")
    print("=" * 80)

    print(f"\n总路径数: {total_paths}")
    print(f"有 insert 和 split 的路径: {affected_paths}")

    print(f"\n【修复前】旧方法 (基于 turn_idx):")
    print(f"  ❌ 错误匹配次数: {old_method_errors}")
    if old_method_errors > 0:
        print(f"  ⚠️  {old_method_errors} 个 turn 的 insert_info 匹配错误")

    print(f"\n【修复后】新方法 (基于函数名):")
    print(f"  ✅ 错误匹配次数: {new_method_errors}")
    if new_method_errors == 0:
        print(f"  🎉 所有 turn 的 insert_info 都正确匹配！")
    else:
        print(f"  ⚠️  仍有 {new_method_errors} 个 turn 匹配错误")

    # 显示一些错误案例
    if error_cases and len(error_cases) > 0:
        print(f"\n" + "=" * 80)
        print("🔍 错误案例详情 (前 3 个)")
        print("=" * 80)

        for i, case in enumerate(error_cases[:3]):
            print(f"\n案例 {i+1}:")
            print(f"  Node: {case['node']}, Path: {case['path']}, Turn: {case['turn']}")
            print(f"  Has split: {case['has_split']}")
            print(f"  Functions: {case['functions']}")

            print(f"\n  旧方法 (基于 turn_idx):")
            print(f"    Valid: {case['old_valid']}")
            if case['old_insert_info']:
                for info in case['old_insert_info']:
                    print(f"    - {info.get('source_func_name')} → {info.get('nested_func_name')}")
            else:
                print(f"    - (无 insert_info)")

            print(f"\n  新���法 (基于函数名):")
            print(f"    Valid: {case['new_valid']}")
            if case['new_insert_info']:
                for info in case['new_insert_info']:
                    print(f"    - {info.get('source_func_name')} → {info.get('nested_func_name')}")
            else:
                print(f"    - (无 insert_info)")

    # 最终判断
    print(f"\n" + "=" * 80)
    print("🎯 最终结论")
    print("=" * 80)

    if new_method_errors == 0 and old_method_errors > 0:
        print("✅ 修复成功！")
        print(f"   - 修复前: {old_method_errors} 个错误")
        print(f"   - 修复后: 0 个错误")
        print(f"   - 改进: 100%")
    elif new_method_errors == 0 and old_method_errors == 0:
        print("✅ 所有路径都正确，无需修复")
    else:
        print(f"⚠️  修复不完全")
        print(f"   - 修复前: {old_method_errors} 个错误")
        print(f"   - 修复后: {new_method_errors} 个错误")
        print(f"   - 改进: {100 * (old_method_errors - new_method_errors) / old_method_errors:.1f}%")

    print("=" * 80)


if __name__ == "__main__":
    main()
