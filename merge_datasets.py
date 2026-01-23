#!/usr/bin/env python3
"""
Merge split dataset folders into a single dataset.
Supports Hugging Face datasets format (.arrow files).
"""

from pathlib import Path
from datasets import load_from_disk, concatenate_datasets
import json


def merge_datasets(source_dir: str, output_dir: str, pattern: str = "split_*"):
    """
    Merge all split dataset folders into a single dataset.
    
    Args:
        source_dir: Directory containing split folders
        output_dir: Output directory for merged dataset
        pattern: Pattern to match split folders (default: "split_*")
    """
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    if not source_path.exists():
        print(f"❌ Error: Source directory not found: {source_dir}")
        return
    
    # Find all split folders
    split_folders = sorted(source_path.glob(pattern))
    split_folders = [f for f in split_folders if f.is_dir()]
    
    if not split_folders:
        print(f"⚠️  No split folders found matching pattern: {pattern}")
        return
    
    print("=" * 70)
    print("Dataset Merge Script")
    print("=" * 70)
    print(f"Source directory: {source_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Found {len(split_folders)} split folder(s)")
    print("=" * 70)
    print()
    
    # Load all datasets
    datasets = []
    total_samples = 0
    
    for i, folder in enumerate(split_folders, 1):
        try:
            print(f"[{i}/{len(split_folders)}] Loading {folder.name}...", end=" ")
            
            # Load dataset from disk
            dataset = load_from_disk(str(folder))
            num_samples = len(dataset)
            total_samples += num_samples
            
            datasets.append(dataset)
            print(f"✓ ({num_samples:,} samples)")
            
        except Exception as e:
            print(f"❌ Error loading {folder.name}: {e}")
    
    if not datasets:
        print("\n❌ No datasets loaded successfully")
        return
    
    print()
    print("-" * 70)
    print(f"Total samples to merge: {total_samples:,}")
    print("-" * 70)
    print()
    
    # Merge datasets
    print("Merging datasets...", end=" ")
    try:
        merged_dataset = concatenate_datasets(datasets)
        print(f"✓ Merged {len(merged_dataset):,} samples")
    except Exception as e:
        print(f"❌ Error merging datasets: {e}")
        return
    
    # Save merged dataset
    print(f"Saving to {output_dir}...", end=" ")
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        merged_dataset.save_to_disk(str(output_path))
        print("✓ Saved")
    except Exception as e:
        print(f"❌ Error saving dataset: {e}")
        return
    
    print()
    print("=" * 70)
    print("✓ Merge completed successfully!")
    print("=" * 70)
    print(f"Merged dataset location: {output_path}")
    print(f"Total samples: {len(merged_dataset):,}")
    
    # Print dataset info
    print()
    print("Dataset Info:")
    print(f"  - Features: {list(merged_dataset.features.keys())}")
    print(f"  - Num rows: {merged_dataset.num_rows:,}")
    print(f"  - Num columns: {merged_dataset.num_columns}")
    
    # Save metadata
    metadata = {
        "source_folders": [f.name for f in split_folders],
        "total_samples": len(merged_dataset),
        "features": list(merged_dataset.features.keys()),
        "num_rows": merged_dataset.num_rows,
        "num_columns": merged_dataset.num_columns,
    }
    
    metadata_path = output_path / "merge_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\nMetadata saved to: {metadata_path}")


if __name__ == "__main__":
    import sys
    
    # Default paths
    default_source = "/Users/plastic/Documents/code/biyesheji/datasets/merged_toucan"
    default_output = "/Users/plastic/Documents/code/biyesheji/datasets/merged_dataset"
    
    if len(sys.argv) > 1:
        source_directory = sys.argv[1]
    else:
        source_directory = default_source
    
    if len(sys.argv) > 2:
        output_directory = sys.argv[2]
    else:
        output_directory = default_output
    
    if len(sys.argv) > 3:
        folder_pattern = sys.argv[3]
    else:
        folder_pattern = "split_*"
    
    merge_datasets(source_directory, output_directory, folder_pattern)
