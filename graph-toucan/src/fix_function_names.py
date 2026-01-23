"""
修正 generated_functions_v1 目录下的函数名，使其与文件名保持一致。

问题：
- 文件名：12306-mcp-server-search.py
- 期望函数名：12306_mcp_server_search
- 实际函数名：search_12306_mcp_server

解决方案：
- 将主函数名重命名为与文件名对应的格式（将 - 替换为 _）
"""

import os
import ast
import re
from typing import List, Dict, Any, Optional, Tuple


GENERATED_FUNCTIONS_DIR = "/data/lhy/datasets/graph-Toucan/tool_info/generated_functions_v1"


class FunctionRenamer(ast.NodeTransformer):
    """AST 转换器，用于重命名函数"""

    def __init__(self, old_name: str, new_name: str):
        self.old_name = old_name
        self.new_name = new_name
        self.renamed_count = 0

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """访问函数定义节点"""
        if node.name == self.old_name:
            node.name = self.new_name
            self.renamed_count += 1
            print(f"      Renamed function: {self.old_name} -> {self.new_name}")

        # 继续访问子节点
        self.generic_visit(node)
        return node


def get_expected_function_name(file_path: str) -> str:
    """
    根据文件路径获取期望的函数名

    Args:
        file_path: 文件路径

    Returns:
        期望的函数名（将文件名转换为合法的 Python 函数名）
    """
    file_name = os.path.basename(file_path)
    # 移除 .py 后缀
    name_without_ext = file_name[:-3] if file_name.endswith('.py') else file_name

    # 将所有非字母数字字符替换为 _
    # 但保留中文字符（Unicode 字母）
    expected_name = re.sub(r'[^\w]', '_', name_without_ext, flags=re.UNICODE)

    # 移除连续的下划线
    expected_name = re.sub(r'_+', '_', expected_name)

    # 移除开头和结尾的下划线
    expected_name = expected_name.strip('_')

    # 如果函数名以数字开头，添加 'tool_' 前缀
    if expected_name and expected_name[0].isdigit():
        expected_name = f'tool_{expected_name}'

    return expected_name


def find_main_function(file_path: str) -> Optional[str]:
    """
    查找文件中的主函数（不是 call_external_api）

    Args:
        file_path: 文件路径

    Returns:
        主函数名，如果没找到返回 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content, filename=file_path)

        # 查找所有函数定义
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 排除私有函数、call_external_api 和类型提示相关的名称
                if (not node.name.startswith('_') and
                    node.name != 'call_external_api' and
                    node.name not in ['Any', 'Dict', 'List', 'Optional', 'Union', 'Tuple']):
                    functions.append(node.name)

        # 如果只有一个非 call_external_api 的函数，就是主函数
        if len(functions) == 1:
            return functions[0]
        elif len(functions) > 1:
            # 如果有多个函数，返回第一个（通常是主函数）
            print(f"      Warning: Multiple functions found: {functions}, using first one")
            return functions[0]
        else:
            return None

    except Exception as e:
        print(f"      Error finding main function: {e}")
        return None


def rename_function_in_file(file_path: str, old_name: str, new_name: str) -> bool:
    """
    在文件中重命名函数

    Args:
        file_path: 文件路径
        old_name: 旧函数名
        new_name: 新函数名

    Returns:
        是否成功重命名
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析 AST
        tree = ast.parse(content, filename=file_path)

        # 重命名函数
        renamer = FunctionRenamer(old_name, new_name)
        new_tree = renamer.visit(tree)

        if renamer.renamed_count == 0:
            print(f"      Warning: Function {old_name} not found")
            return False

        # 将 AST 转换回代码
        # 注意：ast.unparse 会丢失注释和格式，所以我们使用字符串替换
        # 但为了安全，我们只替换函数定义行

        # 使用正则表达式替换函数定义
        # 匹配 "def old_name(" 但不匹配 "_old_name" 或 "xold_name"
        pattern = r'\bdef\s+' + re.escape(old_name) + r'\s*\('
        replacement = f'def {new_name}('

        new_content = re.sub(pattern, replacement, content)

        # 检查是否有实际替换
        if new_content == content:
            print(f"      Warning: No replacement made for {old_name}")
            return False

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"      Error renaming function: {e}")
        return False


def analyze_functions_directory(directory: str) -> Dict[str, Any]:
    """
    分析目录中的所有函数文件

    Args:
        directory: 目录路径

    Returns:
        分析结果字典
    """
    results = {
        "total_files": 0,
        "matched_files": 0,
        "mismatched_files": 0,
        "error_files": 0,
        "mismatches": [],  # [(file_path, expected_name, actual_name)]
    }

    # 遍历目录中的所有 Python 文件
    for file_name in sorted(os.listdir(directory)):
        if not file_name.endswith('.py'):
            continue

        file_path = os.path.join(directory, file_name)
        results["total_files"] += 1

        # 获取期望的函数名
        expected_name = get_expected_function_name(file_path)

        # 查找实际的主函数名
        actual_name = find_main_function(file_path)

        if actual_name is None:
            print(f"  ❓ {file_name}: No main function found")
            results["error_files"] += 1
            continue

        # 比较期望名和实际名
        if actual_name == expected_name:
            # print(f"  ✅ {file_name}: {actual_name}")
            results["matched_files"] += 1
        else:
            print(f"  ❌ {file_name}: expected '{expected_name}', got '{actual_name}'")
            results["mismatched_files"] += 1
            results["mismatches"].append((file_path, expected_name, actual_name))

    return results


def fix_all_functions(directory: str, dry_run: bool = True) -> None:
    """
    修正目录中所有函数的名称

    Args:
        directory: 目录路径
        dry_run: 是否为演练模式（不实际修改文件）
    """
    print(f"\n{'=' * 80}")
    print(f"分析 {directory} 中的函数名...")
    print(f"{'=' * 80}\n")

    # 分析目录
    results = analyze_functions_directory(directory)

    # 打印汇总
    print(f"\n{'=' * 80}")
    print("分析汇总")
    print(f"{'=' * 80}")
    print(f"总文件数: {results['total_files']}")
    print(f"✅ 匹配: {results['matched_files']}")
    print(f"❌ 不匹配: {results['mismatched_files']}")
    print(f"❓ 错误: {results['error_files']}")
    print(f"{'=' * 80}\n")

    if results['mismatched_files'] == 0:
        print("✅ 所有函数名都已正确！无需修改。")
        return

    # 修正不匹配的函数
    if dry_run:
        print(f"{'=' * 80}")
        print("⚠️  DRY RUN 模式 - 不会实际修改文件")
        print(f"{'=' * 80}\n")
        print(f"将要修正 {results['mismatched_files']} 个文件：\n")

        for file_path, expected_name, actual_name in results['mismatches']:
            file_name = os.path.basename(file_path)
            print(f"  📝 {file_name}")
            print(f"      {actual_name} -> {expected_name}")

        print(f"\n运行命令修正这些文件:")
        print(f"  python src/fix_function_names.py --fix")
    else:
        print(f"{'=' * 80}")
        print(f"开始修正 {results['mismatched_files']} 个文件...")
        print(f"{'=' * 80}\n")

        success_count = 0
        fail_count = 0

        for file_path, expected_name, actual_name in results['mismatches']:
            file_name = os.path.basename(file_path)
            print(f"  📝 {file_name}")

            success = rename_function_in_file(file_path, actual_name, expected_name)

            if success:
                success_count += 1
                print(f"      ✅ 成功")
            else:
                fail_count += 1
                print(f"      ❌ 失败")

        print(f"\n{'=' * 80}")
        print("修正完成")
        print(f"{'=' * 80}")
        print(f"✅ 成功: {success_count}")
        print(f"❌ 失败: {fail_count}")
        print(f"{'=' * 80}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="修正 generated_functions_v1 目录下的函数名")
    parser.add_argument('--fix', action='store_true',
                        help='实际修改文件（默认为 dry-run 模式）')
    parser.add_argument('--dir', type=str, default=GENERATED_FUNCTIONS_DIR,
                        help='要处理的目录路径')

    args = parser.parse_args()

    dry_run = not args.fix

    fix_all_functions(args.dir, dry_run=dry_run)


if __name__ == "__main__":
    main()
