"""
检查 generated_functions 目录中的所有函数是否包含危险操作

检测内容：
1. 危险模块导入（os, subprocess, socket, ctypes 等）
2. 危险函数调用（eval, exec, compile, __import__ 等）
3. 文件系统操作（open, pathlib 等）
4. 网络操作
5. 系统调用
"""
import ast
import os
from pathlib import Path
from typing import List, Dict, Set, Any
from collections import defaultdict
import json


# 危险操作分类定义
DANGEROUS_MODULES = {
    'os': 'Operating system interface',
    'subprocess': 'Subprocess execution',
    'socket': 'Network operations',
    'ctypes': 'C library access',
    'multiprocessing': 'Process manipulation',
    'threading': 'Thread manipulation',
    'importlib': 'Dynamic imports',
    'sys': 'System-specific operations',
    'shutil': 'High-level file operations',
    'glob': 'File pattern matching',
    'tempfile': 'Temporary file/directory creation',
    'urllib': 'URL handling',
    'requests': 'HTTP requests',
    'http': 'HTTP modules',
    'ftplib': 'FTP operations',
    'telnetlib': 'Telnet operations',
    'pickle': 'Serialization (can execute code)',
    'marshal': 'Serialization (can execute code)',
    'code': 'Code interpretation',
    'codeop': 'Code compilation',
}

DANGEROUS_BUILTINS = {
    'eval': 'Dynamic code evaluation',
    'exec': 'Dynamic code execution',
    'compile': 'Code compilation',
    '__import__': 'Dynamic imports',
    'open': 'File operations',
    'input': 'User input (potential injection)',
}

DANGEROUS_OS_FUNCTIONS = {
    'system', 'popen', 'execv', 'execve', 'execvp', 'execvpe',
    'spawn', 'fork', 'kill', 'killpg', 'remove', 'unlink',
    'rmdir', 'removedirs', 'rename', 'chmod', 'chown', 'chdir',
    'chroot', 'listdir', 'walk', 'scandir', 'stat', 'lstat',
}

DANGEROUS_SUBPROCESS_FUNCTIONS = {
    'run', 'call', 'check_call', 'check_output', 'Popen',
    'getstatusoutput', 'getoutput',
}

DANGEROUS_PATHLIB_OPERATIONS = {
    'unlink', 'rmdir', 'chmod', 'lchmod', 'rename', 'replace',
    'touch', 'mkdir', 'write_text', 'write_bytes', 'open',
}


class DangerousOperationDetector(ast.NodeVisitor):
    """AST 访问器，检测危险操作"""

    def __init__(self, filename: str):
        self.filename = filename
        self.dangers: List[Dict[str, Any]] = []
        self.imported_modules: Set[str] = set()
        self.imported_names: Dict[str, str] = {}  # alias -> real_name

    def visit_Import(self, node: ast.Import):
        """检测 import 语句"""
        for alias in node.names:
            module_name = alias.name.split('.')[0]
            self.imported_modules.add(module_name)

            # 记录别名
            if alias.asname:
                self.imported_names[alias.asname] = alias.name

            # 检查是否导入危险模块
            if module_name in DANGEROUS_MODULES:
                self.dangers.append({
                    'type': 'dangerous_import',
                    'severity': 'HIGH',
                    'module': alias.name,
                    'reason': DANGEROUS_MODULES[module_name],
                    'line': node.lineno,
                    'col': node.col_offset,
                })

        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """检测 from ... import 语句"""
        if node.module:
            module_name = node.module.split('.')[0]
            self.imported_modules.add(module_name)

            # 检查是否从危险模块导入
            if module_name in DANGEROUS_MODULES:
                imported_items = [alias.name for alias in node.names]
                self.dangers.append({
                    'type': 'dangerous_from_import',
                    'severity': 'HIGH',
                    'module': node.module,
                    'items': imported_items,
                    'reason': DANGEROUS_MODULES[module_name],
                    'line': node.lineno,
                    'col': node.col_offset,
                })

            # 记录导入的名称和别名
            for alias in node.names:
                real_name = f"{node.module}.{alias.name}"
                alias_name = alias.asname if alias.asname else alias.name
                self.imported_names[alias_name] = real_name

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        """检测函数调用"""
        func_name = self._get_function_name(node.func)

        if func_name:
            # 检查危险的内置函数
            if func_name in DANGEROUS_BUILTINS:
                self.dangers.append({
                    'type': 'dangerous_builtin',
                    'severity': 'CRITICAL',
                    'function': func_name,
                    'reason': DANGEROUS_BUILTINS[func_name],
                    'line': node.lineno,
                    'col': node.col_offset,
                })

            # 检查 os 模块的危险函数
            if func_name.startswith('os.'):
                func_base = func_name.split('.')[-1]
                if func_base in DANGEROUS_OS_FUNCTIONS:
                    self.dangers.append({
                        'type': 'dangerous_os_call',
                        'severity': 'HIGH',
                        'function': func_name,
                        'reason': f'OS operation: {func_base}',
                        'line': node.lineno,
                        'col': node.col_offset,
                    })

            # 检查 subprocess 模块的函数
            if func_name.startswith('subprocess.'):
                func_base = func_name.split('.')[-1]
                if func_base in DANGEROUS_SUBPROCESS_FUNCTIONS:
                    self.dangers.append({
                        'type': 'dangerous_subprocess',
                        'severity': 'CRITICAL',
                        'function': func_name,
                        'reason': f'Subprocess execution: {func_base}',
                        'line': node.lineno,
                        'col': node.col_offset,
                    })

            # 检查 pathlib 的危险操作
            if any(pathlib_op in func_name for pathlib_op in DANGEROUS_PATHLIB_OPERATIONS):
                self.dangers.append({
                    'type': 'dangerous_pathlib',
                    'severity': 'MEDIUM',
                    'function': func_name,
                    'reason': 'Pathlib file operation',
                    'line': node.lineno,
                    'col': node.col_offset,
                })

            # 检查网络操作
            if 'socket' in func_name.lower() or 'urlopen' in func_name or 'request' in func_name.lower():
                self.dangers.append({
                    'type': 'network_operation',
                    'severity': 'HIGH',
                    'function': func_name,
                    'reason': 'Network operation detected',
                    'line': node.lineno,
                    'col': node.col_offset,
                })

        self.generic_visit(node)

    def _get_function_name(self, node) -> str:
        """获取函数调用的完整名称"""
        if isinstance(node, ast.Name):
            name = node.id
            # 解析别名
            return self.imported_names.get(name, name)
        elif isinstance(node, ast.Attribute):
            value = self._get_function_name(node.value)
            return f"{value}.{node.attr}" if value else node.attr
        return ""


def analyze_file(file_path: Path) -> Dict[str, Any]:
    """
    分析单个 Python 文件

    Args:
        file_path: 文件路径

    Returns:
        分析结果字典
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析 AST
        tree = ast.parse(content, filename=str(file_path))

        # 检测危险操作
        detector = DangerousOperationDetector(str(file_path))
        detector.visit(tree)

        return {
            'file': str(file_path.name),
            'status': 'analyzed',
            'dangers': detector.dangers,
            'danger_count': len(detector.dangers),
            'imported_modules': sorted(detector.imported_modules),
        }

    except SyntaxError as e:
        return {
            'file': str(file_path.name),
            'status': 'syntax_error',
            'error': str(e),
            'line': e.lineno,
        }
    except Exception as e:
        return {
            'file': str(file_path.name),
            'status': 'error',
            'error': str(e),
        }


def scan_directory(directory: str) -> Dict[str, Any]:
    """
    扫描目录中的所有 Python 文件

    Args:
        directory: 目录路径

    Returns:
        扫描结果统计
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        print(f"❌ Directory not found: {directory}")
        return {}

    # 获取所有 Python 文件
    py_files = sorted(dir_path.glob("*.py"))

    if not py_files:
        print(f"⚠️  No Python files found in {directory}")
        return {}

    print(f"🔍 Scanning {len(py_files)} Python files in {directory}...\n")

    # 分析所有文件
    results = []
    danger_stats = defaultdict(int)
    severity_stats = defaultdict(int)
    dangerous_files = []

    for py_file in py_files:
        result = analyze_file(py_file)
        results.append(result)

        if result.get('status') == 'analyzed':
            danger_count = result.get('danger_count', 0)

            if danger_count > 0:
                dangerous_files.append({
                    'file': result['file'],
                    'danger_count': danger_count,
                    'dangers': result['dangers'],
                })

                # 统计危险类型
                for danger in result['dangers']:
                    danger_type = danger.get('type', 'unknown')
                    severity = danger.get('severity', 'UNKNOWN')
                    danger_stats[danger_type] += 1
                    severity_stats[severity] += 1

    # 打印结果
    print("=" * 80)
    print("SCAN RESULTS")
    print("=" * 80)
    print(f"Total files scanned: {len(py_files)}")
    print(f"Files with dangers: {len(dangerous_files)}")
    print(f"Clean files: {len(py_files) - len(dangerous_files)}")
    print()

    if severity_stats:
        print("Severity Distribution:")
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if severity in severity_stats:
                print(f"  {severity}: {severity_stats[severity]}")
        print()

    if danger_stats:
        print("Danger Types:")
        for danger_type, count in sorted(danger_stats.items(), key=lambda x: -x[1]):
            print(f"  {danger_type}: {count}")
        print()

    if dangerous_files:
        print("=" * 80)
        print("DANGEROUS FILES (Top 20)")
        print("=" * 80)

        # 按危险数量排序
        dangerous_files.sort(key=lambda x: -x['danger_count'])

        for i, file_info in enumerate(dangerous_files[:20], 1):
            print(f"\n{i}. {file_info['file']} ({file_info['danger_count']} dangers)")
            print("-" * 80)

            # 按严重程度分组显示
            dangers_by_severity = defaultdict(list)
            for danger in file_info['dangers']:
                severity = danger.get('severity', 'UNKNOWN')
                dangers_by_severity[severity].append(danger)

            for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'UNKNOWN']:
                if severity in dangers_by_severity:
                    print(f"  [{severity}]")
                    for danger in dangers_by_severity[severity]:
                        line = danger.get('line', '?')
                        danger_type = danger.get('type', 'unknown')
                        reason = danger.get('reason', 'No reason')

                        if danger_type == 'dangerous_import':
                            module = danger.get('module', '?')
                            print(f"    Line {line}: Import {module} - {reason}")
                        elif danger_type == 'dangerous_from_import':
                            module = danger.get('module', '?')
                            items = danger.get('items', [])
                            print(f"    Line {line}: From {module} import {', '.join(items)} - {reason}")
                        elif danger_type in ['dangerous_builtin', 'dangerous_os_call', 'dangerous_subprocess']:
                            func = danger.get('function', '?')
                            print(f"    Line {line}: Call {func}() - {reason}")
                        else:
                            func = danger.get('function', '?')
                            print(f"    Line {line}: {danger_type} - {func} - {reason}")

    # 保存详细报告
    report_path = Path(directory).parent / "danger_scan_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'summary': {
                'total_files': len(py_files),
                'dangerous_files': len(dangerous_files),
                'clean_files': len(py_files) - len(dangerous_files),
                'severity_stats': dict(severity_stats),
                'danger_type_stats': dict(danger_stats),
            },
            'dangerous_files': dangerous_files,
            'all_results': results,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n📄 Detailed report saved to: {report_path}")

    return {
        'total_files': len(py_files),
        'dangerous_files': len(dangerous_files),
        'results': results,
    }


if __name__ == "__main__":
    import sys

    # 默认目录
    default_dir = "/data/lhy/datasets/graph-Toucan/tool_info/generated_functions_v1"

    # 从命令行参数获取目录
    directory = sys.argv[1] if len(sys.argv) > 1 else default_dir

    # 执行扫描
    scan_directory(directory)
