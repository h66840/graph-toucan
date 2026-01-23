#!/usr/bin/env python3
"""
清理 tool_execution_type_classification.json 文件，删除所有 error 字段值不是 null 的条目。
"""
import json
import os
from pathlib import Path

# 文件路径
ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
TOOL_INFO_DIR = os.path.join(ROOT_DIR, "tool_info")
INPUT_FILE = os.path.join(TOOL_INFO_DIR, "tool_execution_type_classification_v1.json")
OUTPUT_FILE = os.path.join(TOOL_INFO_DIR, "tool_execution_type_classification_v1.json")  # 原地修改，也可以改成新文件

def clean_classification_file(input_path: str, output_path: str = None):
    """
    清理分类文件，删除所有 error 字段值不是 null 的条目。
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径，如果为 None 则原地修改
    """
    if output_path is None:
        output_path = input_path
    
    print(f"Loading classification file from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    original_count = len(data)
    print(f"Original entries: {original_count}")
    
    # 过滤掉 error 不是 null 的条目
    cleaned_data = {}
    removed_count = 0
    removed_tools = []
    
    for tool_name, entry in data.items():
        error_value = entry.get("error")
        if error_value is None or error_value == "null":
            cleaned_data[tool_name] = entry
        else:
            removed_count += 1
            removed_tools.append(tool_name)
            print(f"  Removing: {tool_name} (error: {error_value})")
    
    print(f"\nRemoved {removed_count} entries with errors")
    print(f"Remaining entries: {len(cleaned_data)}")
    
    # 保存清理后的数据
    print(f"\nSaving cleaned data to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Cleaned file saved successfully!")
    
    # 打印被删除的工具列表
    if removed_tools:
        print(f"\nRemoved tools ({len(removed_tools)}):")
        for tool in removed_tools[:10]:  # 只显示前10个
            print(f"  - {tool}")
        if len(removed_tools) > 10:
            print(f"  ... and {len(removed_tools) - 10} more")
    
    return cleaned_data


if __name__ == "__main__":
    # 可以指定输出文件，如果不指定则原地修改
    # OUTPUT_FILE = os.path.join(TOOL_INFO_DIR, "tool_execution_type_classification_cleaned.json")
    
    clean_classification_file(INPUT_FILE, OUTPUT_FILE)

