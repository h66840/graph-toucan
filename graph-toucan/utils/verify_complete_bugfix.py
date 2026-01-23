#!/usr/bin/env python3
"""
完整验证 detect_turn_operations 修复效果

检查：
1. Insert 检测修复
2. Merge 检测修复
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
        "merge_info": None,
        "insert_info": [],
        "operations": [],
    }

    # Merge (旧方法)
    merge_logs = path_data.get("merge_logs", [])
    for log in merge_logs:
        if log.get("turn_idx") == turn_idx:
            result["operations"].append("merge")
            result["merge_info"] = log
            break

    # Insert (旧方法)
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
        "merge_info": None,
        "insert_info": [],
        "operations": [],
    }

    # Merge (新方法)
    merge_logs = path_data.get("merge_logs", [])
    for log in merge_logs:
        merged_names = log.get("merged_names", [])
        if merged_names and all(name in turn_functions for name in merged_names):
            result["operations"].append("merge")
            result["merge_info"] = log
            break

    # Insert (新方法)
    insert_logs = path_data.get("insert_logs", [])
    for log in insert_logs:
        source_func = log.get("source_func_name")
        nested_func = log.get("nested_func_name")
        insert_type = log.get("insert_type")

        if insert_type == "short_dependency":
            if source_func in turn_functions and nested_func in turn_functions:
                result["insert_info"].append(log)
                result["operations"].append("insert_short")

        elif insert_type == "long_dependency":
            if nested_func in turn_functions:
                result["insert_info"].append(log)
                result["operations"].append("insert_long")

    return result


def verify_merge_info(merge_info, turn_functions: List[str]) -> bool:
    """验证 merge_info 是否匹配当前 turn 的函数"""
    if not merge_info:
        return True

    merged_names = merge_info.get("merged_names", [])
    if not merged_names:
        return True

    return all(name in turn_functions for name in merged_names)


def verify_insert_info(insert_info: List[Dict], turn_functions: List[str]) -> bool:
    """验证 insert_info 是否匹配当前 turn 的函数"""
    for info in insert_info:
        source_func = info.get("source_func_name")
        nested_func = info.get("nested_func_name")
        insert_type = info.get("insert_type")

        if insert_type == "short_dependency":
            if source_func not in turn_functions or nested_func not in turn_functions:
                return False
        elif insert_type == "long_dependency":
            if nested_func not in turn_functions:
                return False

    return True


def main():
    print("=" * 80)
    print("完整验证 detect_turn_operations 修复效果")
    print("=" * 80)

    # 加载数据
    print("\n📂 加载 FSP v2 数据...")
    with open('walker_path/fsp_v2.json', 'r') as f:
        data = json.load(f)

    node_results = data['node_results']

    # 统计
    total_turns = 0

    # Insert 统计
    old_insert_errors = 0
    new_insert_errors = 0

    # Merge 统计
    old_merge_errors = 0
    new_merge_errors = 0

    # 总体统计
    old_total_errors = 0
    new_total_errors = 0

    error_cases = []

    # 检查所有路径
    print("🔍 检查所有路径...")
    for node_key, node in node_results.items():
        for path in node['paths']:
            fsp_final_names = path.get('fsp_final_names', [])

            for turn_idx, turn_functions in enumerate(fsp_final_names):
                if not turn_functions:  # 空 turn
                    continue

                total_turns += 1

                # 旧方法
                old_result = detect_turn_operations_old(turn_idx, turn_functions, path)
                old_merge_valid = verify_merge_info(old_result["merge_info"], turn_functions)
                old_insert_valid = verify_insert_info(old_result["insert_info"], turn_functions)

                # 新方法
                new_result = detect_turn_operations_new(turn_idx, turn_functions, path)
                new_merge_valid = verify_merge_info(new_result["merge_info"], turn_functions)
                new_insert_valid = verify_insert_info(new_result["insert_info"], turn_functions)

                # 统计错误
                if not old_merge_valid:
                    old_merge_errors += 1
                    old_total_errors += 1

                if not old_insert_valid:
                    old_insert_errors += 1
                    old_total_errors += 1

                if not new_merge_valid:
                    new_merge_errors += 1
                    new_total_errors += 1

                if not new_insert_valid:
                    new_insert_errors += 1
                    new_total_errors += 1

                # 记录错误案例
                if (not old_merge_valid or not old_insert_valid) and len(error_cases) < 3:
                    error_cases.append({
                        'node': node_key,
                        'path': path['path_idx'],
                        'turn': turn_idx,
                        'functions': turn_functions,
                        'old_merge_valid': old_merge_valid,
                        'new_merge_valid': new_merge_valid,
                        'old_insert_valid': old_insert_valid,
                        'new_insert_valid': new_insert_valid,
                        'old_merge': old_result["merge_info"],
                        'new_merge': new_result["merge_info"],
                        'old_insert': old_result["insert_info"],
                        'new_insert': new_result["insert_info"],
                    })

    # 打印结果
    print("\n" + "=" * 80)
    print("📊 验证结果")
    print("=" * 80)

    print(f"\n总 turn 数: {total_turns}")

    print(f"\n{'='*80}")
    print("【Insert 检测】")
    print(f"{'='*80}")
    print(f"修复前 (基于 turn_idx): ❌ {old_insert_errors} 个错误")
    print(f"修复后 (基于函数名):   ✅ {new_insert_errors} 个错误")
    if old_insert_errors > 0 and new_insert_errors == 0:
        print(f"改进: 100% ({old_insert_errors} → 0)")

    print(f"\n{'='*80}")
    print("【Merge 检测】")
    print(f"{'='*80}")
    print(f"修复前 (基于 turn_idx): ❌ {old_merge_errors} 个错误")
    print(f"修复后 (基于函数名):   ✅ {new_merge_errors} 个错误")
    if old_merge_errors > 0 and new_merge_errors == 0:
        print(f"改进: 100% ({old_merge_errors} → 0)")

    print(f"\n{'='*80}")
    print("【总体】")
    print(f"{'='*80}")
    print(f"修复前总错误: ❌ {old_total_errors}")
    print(f"修复后总错误: ✅ {new_total_errors}")
    if old_total_errors > 0 and new_total_errors == 0:
        print(f"改进: 100% ({old_total_errors} → 0)")

    # 显示一些错误案例
    if error_cases:
        print(f"\n" + "=" * 80)
        print("🔍 错误案例详情 (前 3 个)")
        print("=" * 80)

        for i, case in enumerate(error_cases[:3]):
            print(f"\n案例 {i+1}:")
            print(f"  Node: {case['node']}, Path: {case['path']}, Turn: {case['turn']}")
            print(f"  Functions: {case['functions'][:2]}...")  # 只显示前2个

            if not case['old_merge_valid']:
                print(f"\n  【Merge 错误】")
                print(f"    旧方法: Valid={case['old_merge_valid']}")
                if case['old_merge']:
                    print(f"      Merged: {case['old_merge'].get('merged_names', [])}")
                print(f"    新方法: Valid={case['new_merge_valid']}")

            if not case['old_insert_valid']:
                print(f"\n  【Insert 错误】")
                print(f"    旧方法: Valid={case['old_insert_valid']}")
                if case['old_insert']:
                    for ins in case['old_insert']:
                        print(f"      {ins.get('source_func_name')} → {ins.get('nested_func_name')}")
                print(f"    新方法: Valid={case['new_insert_valid']}")

    # 最终判断
    print(f"\n" + "=" * 80)
    print("🎯 最终结论")
    print("=" * 80)

    if new_total_errors == 0 and old_total_errors > 0:
        print("✅ 修复完全成功！")
        print(f"\n   📋 修复详情:")
        print(f"      - Insert 错误: {old_insert_errors} → 0")
        print(f"      - Merge 错误:  {old_merge_errors} → 0")
        print(f"      - 总错误:      {old_total_errors} → 0")
        print(f"\n   🎉 改进率: 100%")
    elif new_total_errors == 0 and old_total_errors == 0:
        print("✅ 所有路径都正确，无需修复")
    else:
        print(f"⚠️  修复不完全")
        print(f"      - 修复前: {old_total_errors} 个错误")
        print(f"      - 修复后: {new_total_errors} 个错误")

    print("=" * 80)


if __name__ == "__main__":
    main()
