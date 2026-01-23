"""
验证 merge 逻辑修复
"""
import json

# 加载数据
with open('walker_path/path_v1_converted.json', 'r') as f:
    data = json.load(f)

paths = data['paths']

print("=" * 80)
print("验证 merge 逻辑修复")
print("=" * 80)

# 测试不同类型的 paths
test_cases = [
    ("num_merges=0", lambda p: p.get('num_merges', 0) == 0),
    ("num_merges=1", lambda p: p.get('num_merges', 0) == 1),
    ("num_merges=2", lambda p: p.get('num_merges', 0) == 2),
]

for name, filter_func in test_cases:
    matching_paths = [p for p in paths if filter_func(p)]
    if not matching_paths:
        continue

    path = matching_paths[0]

    # 旧的判断逻辑
    old_has_merge_info = "merge_info" in path and path.get("merge_info") is not None

    # 新的判断逻辑
    new_has_merge_info = path.get("num_merges", 0) > 0

    # 实际是否有 merged 节点
    actual_has_merge = any(item.get('merged', False) for item in path.get('merge_info', []))

    print(f"\n{name}:")
    print(f"  start_name: {path['start_name']}")
    print(f"  num_merges: {path.get('num_merges', 0)}")
    print(f"  旧逻辑 (merge_info存在): {old_has_merge_info}")
    print(f"  新逻辑 (num_merges>0): {new_has_merge_info}")
    print(f"  实际有merge节点: {actual_has_merge}")

    # 检查是否一致
    if new_has_merge_info == actual_has_merge:
        print(f"  ✅ 新逻辑正确")
    else:
        print(f"  ❌ 新逻辑错误")

print("\n" + "=" * 80)
print("统计结果")
print("=" * 80)

correct_count = 0
incorrect_count = 0

for path in paths:
    new_has_merge_info = path.get("num_merges", 0) > 0
    actual_has_merge = any(item.get('merged', False) for item in path.get('merge_info', []))

    if new_has_merge_info == actual_has_merge:
        correct_count += 1
    else:
        incorrect_count += 1

print(f"正确判断: {correct_count}/{len(paths)} ({correct_count/len(paths)*100:.1f}%)")
print(f"错误判断: {incorrect_count}/{len(paths)} ({incorrect_count/len(paths)*100:.1f}%)")

if incorrect_count == 0:
    print("\n✅ 所有 paths 的 merge 逻辑判断都正确！")
else:
    print(f"\n⚠️  有 {incorrect_count} 个 paths 的判断不一致，需要进一步检查")
