"""
过滤出 failed 的 data（在图连通性检查中不连通的样本）
"""

import json
import datasets
from tqdm import tqdm

# 1. 加载 failed cases
print("Loading failed cases from unreachable_examples_analysis.json...")
with open('/data/lhy/datasets/graph-Toucan/unreachable_examples_analysis_v1.json', 'r', encoding='utf-8') as f:
    failed_data = json.load(f)

# 2. 提取所有 failed 样本的 uuid，并构建 uuid -> unreachable_steps 的映射
failed_uuids = set()
uuid_to_unreachable_steps = {}  # uuid -> unreachable_steps 列表

for example in failed_data.get('examples_unreachable', []):
    uuid = example.get('uuid', '')
    if uuid:
        failed_uuids.add(uuid)
        # 如果同一个 uuid 有多个 turn，合并所有 unreachable_steps
        unreachable_steps = example.get('unreachable_steps', [])
        if uuid not in uuid_to_unreachable_steps:
            uuid_to_unreachable_steps[uuid] = []
        # 添加当前 turn 的 unreachable_steps
        uuid_to_unreachable_steps[uuid].extend(unreachable_steps)

print(f"Found {len(failed_uuids)} failed UUIDs")
print(f"Summary from analysis file:")
summary = failed_data.get('summary', {})
print(f"  Total turns: {summary.get('total_turns', 0)}")
print(f"  Connected turns: {summary.get('connected_turns', 0)}")
print(f"  Turns with unreachable steps: {summary.get('turns_with_unreachable', 0)}")
print(f"  Connectivity rate: {summary.get('connectivity_rate', 0):.2f}%")

# 3. 加载完整数据集
print("\nLoading full dataset...")
total_data = datasets.load_from_disk('/data/lhy/datasets/graph-Toucan/datasets/Toucan-single-turn-subset-common-mcp-v1')
print(f"Total samples in dataset: {len(total_data)}")

# 4. 过滤出 failed 的样本
print("\nFiltering failed samples...")
failed_dataset = total_data.filter(lambda x: x['uuid'] in failed_uuids, desc="Filtering failed cases")
print(f"Filtered failed samples: {len(failed_dataset)}")

# 4.1 为每个样本添加 unreachable_steps 字段
print("\nAdding unreachable_steps field to failed samples...")
def add_unreachable_steps(sample):
    """为样本添加 unreachable_steps 字段"""
    uuid = sample.get('uuid', '')
    # 获取该 uuid 对应的 unreachable_steps，如果没有则设为空列表
    unreachable_steps = uuid_to_unreachable_steps.get(uuid, [])
    # 将 unreachable_steps 转为 JSON 字符串（与数据集其他字段格式保持一致）
    sample['unreachable_steps'] = json.dumps(unreachable_steps, ensure_ascii=False)
    return sample

failed_dataset = failed_dataset.map(add_unreachable_steps, desc="Adding unreachable_steps field")
print("Added unreachable_steps field to all failed samples")

# 5. 保存过滤后的数据集
output_path = '/data/lhy/datasets/graph-Toucan/datasets/Toucan-single-turn-subset-common-mcp-v1.1-failed'
print(f"\nSaving failed dataset to {output_path}...")
failed_dataset.save_to_disk(output_path)
print(f"Failed dataset saved successfully!")

# 6. 打印一些统计信息
print("\n" + "="*80)
print("Failed Cases Summary")
print("="*80)
print(f"Total samples in original dataset: {len(total_data)}")
print(f"Failed samples: {len(failed_dataset)}")
print(f"Success rate: {(len(total_data) - len(failed_dataset)) / len(total_data) * 100:.2f}%")
print(f"Failure rate: {len(failed_dataset) / len(total_data) * 100:.2f}%")
print("="*80)

