#!/usr/bin/env python3
"""
Merge two Toucan-SFT datasets with filtering
- dataset1: Existing HuggingFace Dataset (Toucan-SFT format)
- dataset2: JSONL file in Toucan message format (with tool_call/tool_response roles)

Filter out data where any turn has exactly 10 steps
"""
import json
import argparse
from datasets import load_from_disk, concatenate_datasets
from tqdm import tqdm


def filter_dataset_by_steps(dataset, max_steps_to_exclude=10):
    """
    Filter out data where any turn has exactly max_steps_to_exclude steps

    Args:
        dataset: HuggingFace Dataset
        max_steps_to_exclude: Number of steps to filter out (default: 10)

    Returns:
        Filtered dataset
    """
    print(f"Filtering dataset to exclude data with turns having {max_steps_to_exclude} steps...")
    print(f"Original dataset size: {len(dataset)}")

    indices_to_keep = []
    filtered_count = 0

    for idx in tqdm(range(len(dataset)), desc="Filtering"):
        sample = dataset[idx]

        # Parse modification_info to get distilled_turns
        try:
            modification_info = json.loads(sample['modification_info'])

            # Check if this is from the distill dataset (has path_info)
            if 'path_info' in modification_info:
                # This sample is from the distill dataset, no need to check steps
                # Actually, we need to check the original jsonl data
                # But since we already converted, we don't have distilled_turns in the dataset
                # We need to go back to the original jsonl or store more info
                indices_to_keep.append(idx)
            else:
                # This is from the original dataset, keep it
                indices_to_keep.append(idx)

        except Exception as e:
            # If there's any error, keep the sample
            indices_to_keep.append(idx)

    filtered_dataset = dataset.select(indices_to_keep)
    print(f"Filtered out {filtered_count} samples")
    print(f"Remaining samples: {len(filtered_dataset)}")

    return filtered_dataset


def filter_jsonl_data_by_steps(data_list, max_steps_to_exclude=10):
    """
    Filter JSONL data to exclude samples where any turn has exactly max_steps_to_exclude steps

    Args:
        data_list: List of data samples from JSONL
        max_steps_to_exclude: Number of steps to filter out (default: 10)

    Returns:
        Filtered data list
    """
    print(f"Filtering data to exclude samples with turns having {max_steps_to_exclude} steps...")
    print(f"Original data size: {len(data_list)}")

    filtered_data = []
    filtered_count = 0

    for item in tqdm(data_list, desc="Filtering"):
        distilled_turns = item.get('distilled_turns', [])

        # Check if any turn has exactly max_steps_to_exclude steps
        should_filter = False
        for turn in distilled_turns:
            total_steps = turn.get('total_steps', 0)
            if total_steps == max_steps_to_exclude:
                should_filter = True
                break

        if not should_filter:
            filtered_data.append(item)
        else:
            filtered_count += 1

    print(f"Filtered out {filtered_count} samples")
    print(f"Remaining samples: {len(filtered_data)}")

    return filtered_data


def merge_datasets(dataset1_path, dataset2_jsonl_path, output_path, max_steps_to_exclude=10):
    """
    Merge two datasets with filtering

    Args:
        dataset1_path: Path to the first dataset (existing Toucan-SFT)
        dataset2_jsonl_path: Path to the second dataset's JSONL file
        output_path: Output path for merged dataset
        max_steps_to_exclude: Number of steps to filter out (default: 10)
    """
    print("=" * 60)
    print("Step 1: Loading existing dataset")
    print("=" * 60)
    dataset1 = load_from_disk(dataset1_path)
    print(f"Loaded dataset1 from {dataset1_path}")
    print(f"Dataset1 size: {len(dataset1)}")

    print("\n" + "=" * 60)
    print("Step 2: Loading and filtering new JSONL data")
    print("=" * 60)

    # Load JSONL data
    print(f"Loading data from {dataset2_jsonl_path}...")
    data = []
    with open(dataset2_jsonl_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(tqdm(f, desc="Reading lines"), 1):
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Warning: Failed to parse line {line_num}: {e}")
                    continue
    print(f"Loaded {len(data)} samples from JSONL")

    # Filter the JSONL data
    filtered_data = filter_jsonl_data_by_steps(data, max_steps_to_exclude)

    print("\n" + "=" * 60)
    print("Step 3: Converting filtered data to dataset format")
    print("=" * 60)

    # Convert filtered data to dataset format (same as convert_jsonl_to_parquet.py)
    import uuid as uuid_lib
    from datasets import Dataset

    dataset_dict = {
        'uuid': [],
        'subset_name': [],
        'question': [],
        'target_tools': [],
        'tools': [],
        'messages': [],
        'is_modified': [],
        'modification_info': []
    }

    for item in tqdm(filtered_data, desc="Processing"):
        dataset_dict['uuid'].append(str(uuid_lib.uuid4()))

        # Set subset_name to "toucan-graph" for all data from jsonl
        dataset_dict['subset_name'].append("toucan-graph")

        # Still need path_info for modification_info
        path_info = item.get('path_info', {})
        conversation_history = item.get('conversation_history', [])

        question = ""
        for msg in conversation_history:
            if msg.get('role') == 'user':
                question = msg.get('content', '')
                break
        dataset_dict['question'].append(question)

        tools = item.get('tools', [])
        dataset_dict['tools'].append(json.dumps(tools))

        distilled_turns = item.get('distilled_turns', [])
        target_tools = []
        for turn in distilled_turns:
            ground_truth_calls = turn.get('ground_truth_tool_calls', [])
            for call in ground_truth_calls:
                func_name = call.get('function', '')
                if func_name and func_name not in target_tools:
                    target_tools.append(func_name)
        dataset_dict['target_tools'].append(", ".join(target_tools))

        messages = [msg for msg in conversation_history if msg.get('role') in ['user', 'assistant', 'tool_call', 'tool_response']]
        dataset_dict['messages'].append(json.dumps(messages))

        dataset_dict['is_modified'].append(False)

        modification_info = {
            'path_info': path_info,
            'token_usage': item.get('token_usage', {}),
            'statistics': item.get('statistics', {}),
            'tool_name_mapping': item.get('tool_name_mapping', {})
        }
        dataset_dict['modification_info'].append(json.dumps(modification_info))

    dataset2 = Dataset.from_dict(dataset_dict)
    print(f"Created dataset2 with {len(dataset2)} samples")

    print("\n" + "=" * 60)
    print("Step 4: Merging datasets")
    print("=" * 60)

    # Concatenate datasets
    merged_dataset = concatenate_datasets([dataset1, dataset2])
    print(f"Merged dataset size: {len(merged_dataset)}")
    print(f"  - Dataset1: {len(dataset1)} samples")
    print(f"  - Dataset2 (filtered): {len(dataset2)} samples")

    print("\n" + "=" * 60)
    print("Step 5: Saving merged dataset")
    print("=" * 60)

    merged_dataset.save_to_disk(output_path)
    print(f"Merged dataset saved to {output_path}")

    # Print stats
    import os
    if os.path.isdir(output_path):
        total_size = sum(os.path.getsize(os.path.join(output_path, f))
                        for f in os.listdir(output_path)
                        if os.path.isfile(os.path.join(output_path, f)))
        print(f"Directory size: {total_size / (1024 ** 2):.2f} MB")

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Original dataset1 size: {len(dataset1)}")
    print(f"Original dataset2 size (before filtering): {len(data)}")
    print(f"Dataset2 filtered size: {len(dataset2)}")
    print(f"Samples filtered out: {len(data) - len(dataset2)}")
    print(f"Final merged size: {len(merged_dataset)}")
    print(f"\n✅ Dataset merge completed successfully!")


def main():
    parser = argparse.ArgumentParser(description="Merge two Toucan-SFT datasets with filtering")
    parser.add_argument(
        "--dataset1",
        type=str,
        required=True,
        help="Path to the first dataset (existing Toucan-SFT)"
    )
    parser.add_argument(
        "--dataset2_jsonl",
        type=str,
        default="distill_v3_toucan.jsonl",
        help="Path to the second dataset's JSONL file (default: distill_v3_toucan.jsonl)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="merged_toucan_sft",
        help="Output path for merged dataset (default: merged_toucan_sft)"
    )
    parser.add_argument(
        "--max_steps_to_exclude",
        type=int,
        default=10,
        help="Exclude data where any turn has exactly this many steps (default: 10)"
    )

    args = parser.parse_args()

    merge_datasets(
        args.dataset1,
        args.dataset2_jsonl,
        args.output,
        args.max_steps_to_exclude
    )


if __name__ == "__main__":
    main()
