#!/usr/bin/env python3
"""
检查Python文件中缺失的import语句

这个脚本会分析指定目录下的所有Python文件，检查：
1. 使用了typing模块的类型注解但没有导入
2. 使用了标准库模块但没有导入
3. import语句的位置是否正确（应该在文件开头）
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple


class ImportChecker:
    """检查Python文件中的import问题"""

    # typing模块中常用的类型
    TYPING_TYPES = {
        'Dict', 'List', 'Set', 'Tuple', 'Optional', 'Union', 'Any',
        'Callable', 'Iterator', 'Iterable', 'Sequence', 'Mapping',
        'TypeVar', 'Generic', 'Protocol', 'Literal', 'Final',
        'ClassVar', 'Type', 'cast', 'overload', 'TypedDict'
    }

    # 常用的标准库模块
    COMMON_STDLIB = {
        'json', 'os', 'sys', 'datetime', 're', 'math', 'random',
        'collections', 'itertools', 'functools', 'pathlib', 'time',
        'logging', 'argparse', 'subprocess', 'threading', 'multiprocessing',
        'asyncio', 'dataclasses', 'enum', 'abc', 'copy', 'pickle'
    }

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.content = ""
        self.lines = []
        self.issues = []

    def read_file(self) -> bool:
        """读取文件内容"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
            return True
        except Exception as e:
            print(f"Error reading {self.file_path}: {e}")
            return False

    def find_imports(self) -> Tuple[Set[str], Set[str], int]:
        """
        查找文件中的import语句

        Returns:
            imported_modules: 已导入的模块集合
            imported_from_typing: 从typing导入的类型集合
            last_import_line: 最后一个import语句的行号
        """
        imported_modules = set()
        imported_from_typing = set()
        last_import_line = 0

        for i, line in enumerate(self.lines):
            stripped = line.strip()

            # 匹配 import xxx
            if stripped.startswith('import '):
                match = re.match(r'import\s+([\w.]+)', stripped)
                if match:
                    module = match.group(1).split('.')[0]
                    imported_modules.add(module)
                    last_import_line = i

            # 匹配 from xxx import yyy
            elif stripped.startswith('from '):
                match = re.match(r'from\s+([\w.]+)\s+import\s+(.+)', stripped)
                if match:
                    module = match.group(1).split('.')[0]
                    imports = match.group(2)

                    imported_modules.add(module)

                    if module == 'typing':
                        # 解析从typing导入的类型
                        import_items = [item.strip().split(' as ')[0]
                                       for item in imports.split(',')]
                        imported_from_typing.update(import_items)

                    last_import_line = i

        return imported_modules, imported_from_typing, last_import_line

    def find_used_types_and_modules(self) -> Tuple[Set[str], Set[str]]:
        """
        查找代码中使用的typing类型和模块

        Returns:
            used_typing_types: 使用的typing类型集合
            used_modules: 使用的标准库模块集合
        """
        used_typing_types = set()
        used_modules = set()

        # 查找类型注解中使用的typing类型
        # 匹配函数参数和返回值类型注解
        type_annotation_pattern = r':\s*([A-Z][\w\[\],\s]+?)(?:\s*[=\)]|$)'
        for match in re.finditer(type_annotation_pattern, self.content):
            annotation = match.group(1)
            for typing_type in self.TYPING_TYPES:
                if re.search(r'\b' + typing_type + r'\b', annotation):
                    used_typing_types.add(typing_type)

        # 匹配变量类型注解
        var_annotation_pattern = r'^\s*\w+\s*:\s*([A-Z][\w\[\],\s]+?)\s*='
        for line in self.lines:
            match = re.match(var_annotation_pattern, line)
            if match:
                annotation = match.group(1)
                for typing_type in self.TYPING_TYPES:
                    if re.search(r'\b' + typing_type + r'\b', annotation):
                        used_typing_types.add(typing_type)

        # 查找使用的标准库模块
        for module in self.COMMON_STDLIB:
            # 匹配 module.function() 的模式
            if re.search(r'\b' + module + r'\.\w+', self.content):
                used_modules.add(module)

        return used_typing_types, used_modules

    def check_import_position(self, last_import_line: int) -> List[int]:
        """
        检查import语句的位置

        Returns:
            错误位置的import语句行号列表
        """
        misplaced_imports = []

        # 跳过文件开头的注释和空行
        first_code_line = 0
        in_docstring = False
        for i, line in enumerate(self.lines):
            stripped = line.strip()

            # 跳过空行和注释
            if not stripped or stripped.startswith('#'):
                continue

            # 处理文档字符串
            if stripped.startswith('"""') or stripped.startswith("'''"):
                if not in_docstring:
                    in_docstring = True
                    if stripped.count('"""') >= 2 or stripped.count("'''") >= 2:
                        in_docstring = False
                else:
                    in_docstring = False
                continue

            if in_docstring:
                continue

            # 找到第一个非import的代码行
            if not (stripped.startswith('import ') or stripped.startswith('from ')):
                first_code_line = i
                break

        # 检查在代码中间的import
        for i, line in enumerate(self.lines):
            if i > first_code_line:
                stripped = line.strip()
                if stripped.startswith('import ') or stripped.startswith('from '):
                    misplaced_imports.append(i + 1)  # 行号从1开始

        return misplaced_imports

    def analyze(self) -> bool:
        """分析文件并生成报告"""
        if not self.read_file():
            return False

        imported_modules, imported_from_typing, last_import_line = self.find_imports()
        used_typing_types, used_modules = self.find_used_types_and_modules()
        misplaced_imports = self.check_import_position(last_import_line)

        # 检查缺失的typing导入
        missing_typing = used_typing_types - imported_from_typing
        if missing_typing:
            self.issues.append({
                'type': 'missing_typing',
                'missing': sorted(missing_typing),
                'suggestion': f"from typing import {', '.join(sorted(missing_typing))}"
            })

        # 检查缺失的标准库导入
        missing_modules = used_modules - imported_modules
        if missing_modules:
            for module in sorted(missing_modules):
                self.issues.append({
                    'type': 'missing_module',
                    'missing': module,
                    'suggestion': f"import {module}"
                })

        # 检查import位置错误
        if misplaced_imports:
            self.issues.append({
                'type': 'misplaced_import',
                'lines': misplaced_imports,
                'suggestion': 'Import statements should be at the beginning of the file'
            })

        return len(self.issues) > 0

    def get_report(self) -> str:
        """生成分析报告"""
        if not self.issues:
            return None

        report = [f"\n{'='*80}"]
        report.append(f"文件: {self.file_path}")
        report.append('='*80)

        for issue in self.issues:
            if issue['type'] == 'missing_typing':
                report.append("\n❌ 缺少typing类型导入:")
                report.append(f"   使用了但未导入: {', '.join(issue['missing'])}")
                report.append(f"   建议添加: {issue['suggestion']}")

            elif issue['type'] == 'missing_module':
                report.append(f"\n❌ 缺少模块导入: {issue['missing']}")
                report.append(f"   建议添加: {issue['suggestion']}")

            elif issue['type'] == 'misplaced_import':
                report.append(f"\n⚠️  Import语句位置不正确:")
                report.append(f"   在代码中间发现import语句，行号: {', '.join(map(str, issue['lines']))}")
                report.append(f"   建议: {issue['suggestion']}")

        return '\n'.join(report)


def check_directory(directory: str, pattern: str = "*.py") -> Dict[str, List[str]]:
    """
    检查目录下所有Python文件

    Args:
        directory: 要检查的目录路径
        pattern: 文件匹配模式，默认为*.py

    Returns:
        问题文件的字典，key为文件路径，value为问题列表
    """
    path = Path(directory)
    problem_files = {}
    total_files = 0
    problem_count = 0

    print(f"\n🔍 开始检查目录: {directory}")
    print(f"📁 匹配模式: {pattern}\n")

    for py_file in path.glob(pattern):
        if py_file.is_file():
            total_files += 1
            checker = ImportChecker(str(py_file))

            if checker.analyze():
                problem_count += 1
                report = checker.get_report()
                if report:
                    print(report)
                    problem_files[str(py_file)] = checker.issues

    # 打印总结
    print(f"\n{'='*80}")
    print(f"📊 检查完成!")
    print(f"   总文件数: {total_files}")
    print(f"   有问题的文件数: {problem_count}")
    print(f"   正常文件数: {total_files - problem_count}")
    print(f"{'='*80}\n")

    return problem_files


def main():
    """主函数"""
    import sys

    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        # 默认检查generated_functions目录
        directory = "generated_functions_v1"

    if not os.path.exists(directory):
        print(f"❌ 错误: 目录不存在: {directory}")
        sys.exit(1)

    problem_files = check_directory(directory)

    # 生成修复建议
    if problem_files:
        print("\n💡 修复建议:")
        print("-" * 80)
        for file_path, issues in problem_files.items():
            print(f"\n文件: {file_path}")
            for issue in issues:
                if 'suggestion' in issue:
                    print(f"  • {issue['suggestion']}")
    else:
        print("\n✅ 太棒了！所有文件的import都是正确的！")


if __name__ == "__main__":
    main()
