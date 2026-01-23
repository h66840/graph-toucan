"""
清理 fsp_v1.json 中的无效数据
删除 tool_outputs 和 fc_results 都为空的记录
"""
import json
import os
from typing import List, Dict, Any


def is_valid_record(record: Dict[str, Any]) -> bool:
    """
    判断记录是否有效

    有效条件：tool_outputs 或 fc_results 至少有一个非空
    """
    tool_outputs = record.get("tool_outputs", [])
    fc_results = record.get("fc_results", [])

    # 至少有一个非空才算有效
    return len(tool_outputs) > 0 or len(fc_results) > 0


def clean_fsp_file(input_path: str, output_path: str = None) -> None:
    """
    清理 fsp 文件，删除无效记录

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（如果为 None，则覆盖原文件）
    """
    if output_path is None:
        output_path = input_path

    # 读取所有记录
    records = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError as e:
                    print(f"[WARNING] Failed to parse line: {e}")
                    continue

    print(f"Total records: {len(records)}")

    # 过滤有效记录
    valid_records = [r for r in records if is_valid_record(r)]
    invalid_count = len(records) - len(valid_records)

    print(f"Valid records: {len(valid_records)}")
    print(f"Invalid records (removed): {invalid_count}")

    # 写入有效记录
    if len(valid_records) > 0:
        with open(output_path, 'w', encoding='utf-8') as f:
            for record in valid_records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        print(f"✅ Cleaned data written to: {output_path}")
    else:
        print("⚠️ No valid records found!")


def main():
    input_file = "fsp_path/fsp_v1.json"

    # 先备份原文件
    backup_file = input_file + ".backup"
    if os.path.exists(input_file):
        import shutil
        shutil.copy(input_file, backup_file)
        print(f"📦 Backup created: {backup_file}\n")

    # 清理数据
    clean_fsp_file(input_file)

    print(f"\n✅ Done! Original file backed up to: {backup_file}")


if __name__ == "__main__":
    main()
