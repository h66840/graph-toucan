#!/usr/bin/env python3
"""
Batch decompression script for compressed files.
Supports .gz, .tar.gz, .tgz, .zip formats.
"""

import gzip
import tarfile
import zipfile
from pathlib import Path
import shutil


def decompress_gz(file_path: Path, output_dir: Path):
    """Decompress .gz file (not tar.gz)"""
    output_file = output_dir / file_path.stem
    print(f"Decompressing {file_path.name} -> {output_file.name}")
    
    with gzip.open(file_path, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    print(f"✓ Decompressed: {output_file.name}")


def decompress_tar_gz(file_path: Path, output_dir: Path):
    """Decompress .tar.gz or .tgz file"""
    print(f"Extracting {file_path.name} to {output_dir}")
    
    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(path=output_dir)
    
    print(f"✓ Extracted: {file_path.name}")


def decompress_zip(file_path: Path, output_dir: Path):
    """Decompress .zip file"""
    print(f"Extracting {file_path.name} to {output_dir}")
    
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    
    print(f"✓ Extracted: {file_path.name}")


def batch_decompress(source_dir: str, output_dir: str = None):
    """
    Batch decompress all compressed files in a directory.
    
    Args:
        source_dir: Directory containing compressed files
        output_dir: Output directory (default: same as source_dir)
    """
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"❌ Error: Directory not found: {source_dir}")
        return
    
    # Use source directory as output if not specified
    output_path = Path(output_dir) if output_dir else source_path
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all compressed files
    compressed_files = []
    compressed_files.extend(source_path.glob("*.tar.gz"))
    compressed_files.extend(source_path.glob("*.tgz"))
    compressed_files.extend(source_path.glob("*.gz"))
    compressed_files.extend(source_path.glob("*.zip"))
    
    if not compressed_files:
        print(f"⚠️  No compressed files found in {source_dir}")
        return
    
    print(f"Found {len(compressed_files)} compressed file(s)")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    
    for file_path in compressed_files:
        try:
            # Determine file type and decompress
            if file_path.suffix == '.gz':
                if file_path.suffixes[-2:] == ['.tar', '.gz']:
                    # .tar.gz file
                    decompress_tar_gz(file_path, output_path)
                else:
                    # .gz file (not tar)
                    decompress_gz(file_path, output_path)
            elif file_path.suffix == '.tgz':
                decompress_tar_gz(file_path, output_path)
            elif file_path.suffix == '.zip':
                decompress_zip(file_path, output_path)
            
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error decompressing {file_path.name}: {e}")
            error_count += 1
    
    print("-" * 60)
    print(f"✓ Successfully decompressed: {success_count}")
    if error_count > 0:
        print(f"❌ Failed: {error_count}")
    print(f"Output directory: {output_path}")


if __name__ == "__main__":
    import sys
    
    # Default directory
    default_dir = "/Users/plastic/Documents/code/biyesheji/datasets/merged_toucan"
    
    if len(sys.argv) > 1:
        source_directory = sys.argv[1]
    else:
        source_directory = default_dir
    
    if len(sys.argv) > 2:
        output_directory = sys.argv[2]
    else:
        output_directory = None
    
    print("=" * 60)
    print("Batch Decompression Script")
    print("=" * 60)
    print(f"Source: {source_directory}")
    print(f"Output: {output_directory or source_directory}")
    print("=" * 60)
    print()
    
    batch_decompress(source_directory, output_directory)
