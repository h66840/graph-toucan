#!/usr/bin/env python3
"""
测试 generated_functions_v1 目录下的所有 Python 文件是否能正常运行。
检查语法错误、导入错误等。
"""
import os
import sys
import importlib.util
import traceback
from pathlib import Path
from typing import Dict, List, Tuple
import json

ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
TOOL_INFO_DIR = os.path.join(ROOT_DIR, "tool_info")
GENERATED_FUNCTIONS_DIR = os.path.join(TOOL_INFO_DIR, "generated_functions_v1")


def test_python_file(file_path: str) -> Tuple[bool, str, str]:
    """
    测试单个 Python 文件是否能正常运行。
    
    Args:
        file_path: Python 文件路径
        
    Returns:
        (success: bool, error_type: str, error_message: str)
    """
    file_name = os.path.basename(file_path)
    
    try:
        # 读取文件内容，检查语法
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        
        # 编译检查语法错误
        compile(source_code, file_path, "exec")
        
        # 尝试导入模块
        spec = importlib.util.spec_from_file_location(
            f"test_module_{file_name}", file_path
        )
        if spec is None or spec.loader is None:
            return False, "ImportError", "Failed to create module spec"
        
        module = importlib.util.module_from_spec(spec)
        
        # 执行模块（这会运行模块级别的代码）
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            # 捕获运行时错误
            error_type = type(e).__name__
            error_message = str(e)
            return False, error_type, error_message
        
        return True, "", ""
        
    except SyntaxError as e:
        return False, "SyntaxError", f"{e.msg} at line {e.lineno}: {e.text}"
    except Exception as e:
        error_type = type(e).__name__
        error_message = str(e)
        return False, error_type, error_message


def test_all_functions(directory: str = GENERATED_FUNCTIONS_DIR) -> Dict[str, any]:
    """
    测试目录下所有 Python 文件。
    
    Args:
        directory: 要测试的目录路径
        
    Returns:
        包含测试结果的字典
    """
    if not os.path.exists(directory):
        print(f"Error: Directory {directory} does not exist!")
        return {}
    
    print(f"Testing Python files in: {directory}")
    print("=" * 80)
    
    # 获取所有 .py 文件（排除 __init__.py 和 summary 文件）
    py_files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith('.py') and f != '__init__.py' and f != 'generation_summary.json'
    ]
    
    if not py_files:
        print("No Python files found!")
        return {}
    
    print(f"Found {len(py_files)} Python files to test.\n")
    
    results = {
        "total": len(py_files),
        "passed": 0,
        "failed": 0,
        "details": {}
    }
    
    # 测试每个文件
    for idx, file_path in enumerate(py_files, 1):
        file_name = os.path.basename(file_path)
        print(f"[{idx}/{len(py_files)}] Testing: {file_name}...", end=" ", flush=True)
        
        success, error_type, error_message = test_python_file(file_path)
        
        if success:
            print("✓ PASSED")
            results["passed"] += 1
            results["details"][file_name] = {
                "status": "passed",
                "error_type": None,
                "error_message": None
            }
        else:
            print(f"✗ FAILED ({error_type})")
            results["failed"] += 1
            results["details"][file_name] = {
                "status": "failed",
                "error_type": error_type,
                "error_message": error_message
            }
    
    # 打印汇总
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    print(f"Total files tested: {results['total']}")
    print(f"Passed: {results['passed']} ({results['passed'] / results['total'] * 100:.1f}%)")
    print(f"Failed: {results['failed']} ({results['failed'] / results['total'] * 100:.1f}%)")
    
    # 打印失败的文件详情
    # if results["failed"] > 0:
    #     print("\n" + "=" * 80)
    #     print("Failed Files Details")
    #     print("=" * 80)
    #     for file_name, detail in results["details"].items():
    #         if detail["status"] == "failed":
    #             print(f"\n{file_name}:")
    #             print(f"  Error Type: {detail['error_type']}")
    #             print(f"  Error Message: {detail['error_message']}")
    
    # 保存失败的文件名到 JSON 文件
    failed_files = [
        file_name for file_name, detail in results["details"].items()
        if detail["status"] == "failed"
    ]
    
    if failed_files:
        output_file = os.path.join(directory, "failed_functions.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump({"failed_files": failed_files}, f, indent=2, ensure_ascii=False)
        print(f"\nFailed function files saved to: {output_file}")
        print(f"Total failed files: {len(failed_files)}")
    
    
    return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test generated Python function files")
    parser.add_argument(
        "--dir",
        type=str,
        default=GENERATED_FUNCTIONS_DIR,
        help="Directory containing Python files to test (default: generated_functions_v1)"
    )
    
    args = parser.parse_args()
    
    results = test_all_functions(args.dir)
    
    # 返回适当的退出码
    sys.exit(0 if results.get("failed", 0) == 0 else 1)


if __name__ == "__main__":
    main()

