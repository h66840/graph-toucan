"""
全面分析 generated_functions_v1 目录下所有函数
评估 SafeExecutionContext 的保护能力
"""
import os
import ast
from pathlib import Path
from collections import defaultdict
import json


GENERATED_FUNCTIONS_DIR = "/data/lhy/datasets/graph-Toucan/tool_info/generated_functions_v1"


class FunctionAnalyzer:
    """分析函数使用的操作"""

    def __init__(self):
        self.stats = {
            'total_files': 0,
            'analyzed_files': 0,
            'error_files': 0,

            # 文件操作
            'uses_open': [],
            'uses_pathlib': [],
            'uses_file_operations': [],

            # 模块导入
            'imports_os': [],
            'imports_sys': [],
            'imports_subprocess': [],
            'imports_pathlib': [],
            'imports_shutil': [],

            # 危险函数调用
            'calls_eval': [],
            'calls_exec': [],
            'calls_compile': [],
            'calls_subprocess': [],
            'calls_os_system': [],
            'calls_os_chdir': [],
            'calls_os_listdir': [],
            'calls_os_walk': [],

            # pathlib 操作
            'pathlib_read': [],
            'pathlib_write': [],
            'pathlib_unlink': [],
        }

    def analyze_file(self, file_path: str) -> dict:
        """分析单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=file_path)
            file_name = os.path.basename(file_path)

            # 检查导入
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_name = alias.name
                        if module_name == 'os' or module_name.startswith('os.'):
                            self.stats['imports_os'].append(file_name)
                        elif module_name == 'sys':
                            self.stats['imports_sys'].append(file_name)
                        elif module_name == 'subprocess':
                            self.stats['imports_subprocess'].append(file_name)
                        elif module_name == 'pathlib':
                            self.stats['imports_pathlib'].append(file_name)
                        elif module_name == 'shutil':
                            self.stats['imports_shutil'].append(file_name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        if node.module == 'os' or node.module.startswith('os.'):
                            self.stats['imports_os'].append(file_name)
                        elif node.module == 'pathlib':
                            self.stats['imports_pathlib'].append(file_name)
                            # 检查导入的具体内容
                            for alias in node.names:
                                if alias.name == 'Path':
                                    self.stats['uses_pathlib'].append(file_name)
                        elif node.module == 'subprocess':
                            self.stats['imports_subprocess'].append(file_name)
                        elif node.module == 'shutil':
                            self.stats['imports_shutil'].append(file_name)

                # 检查函数调用
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        func_name = node.func.id

                        if func_name == 'open':
                            self.stats['uses_open'].append(file_name)
                        elif func_name == 'eval':
                            self.stats['calls_eval'].append(file_name)
                        elif func_name == 'exec':
                            self.stats['calls_exec'].append(file_name)
                        elif func_name == 'compile':
                            self.stats['calls_compile'].append(file_name)

                    elif isinstance(node.func, ast.Attribute):
                        # 检查 os.xxx() 调用
                        if isinstance(node.func.value, ast.Name):
                            if node.func.value.id == 'os':
                                attr = node.func.attr
                                if attr == 'system':
                                    self.stats['calls_os_system'].append(file_name)
                                elif attr == 'chdir':
                                    self.stats['calls_os_chdir'].append(file_name)
                                elif attr in ['listdir', 'scandir']:
                                    self.stats['calls_os_listdir'].append(file_name)
                                elif attr == 'walk':
                                    self.stats['calls_os_walk'].append(file_name)

                        # 检查 subprocess.xxx() 调用
                        if isinstance(node.func.value, ast.Name):
                            if node.func.value.id == 'subprocess':
                                self.stats['calls_subprocess'].append(file_name)

                        # 检查 pathlib 操作
                        if node.func.attr in ['read_text', 'read_bytes']:
                            self.stats['pathlib_read'].append(file_name)
                        elif node.func.attr in ['write_text', 'write_bytes']:
                            self.stats['pathlib_write'].append(file_name)
                        elif node.func.attr == 'unlink':
                            self.stats['pathlib_unlink'].append(file_name)

            return {'status': 'success', 'file': file_name}

        except Exception as e:
            return {'status': 'error', 'file': os.path.basename(file_path), 'error': str(e)}

    def analyze_directory(self, directory: str):
        """分析整个目录"""
        py_files = sorted(Path(directory).glob("*.py"))
        self.stats['total_files'] = len(py_files)

        print(f"开始分析 {len(py_files)} 个文件...")

        for i, py_file in enumerate(py_files):
            if (i + 1) % 100 == 0:
                print(f"  进度: {i + 1}/{len(py_files)}")

            result = self.analyze_file(str(py_file))
            if result['status'] == 'success':
                self.stats['analyzed_files'] += 1
            else:
                self.stats['error_files'] += 1

        print(f"✅ 分析完成！")

    def get_report(self) -> dict:
        """生成报告"""
        # 去重
        for key in self.stats:
            if isinstance(self.stats[key], list):
                self.stats[key] = list(set(self.stats[key]))

        return self.stats


def evaluate_safe_execution_context(stats: dict):
    """评估 SafeExecutionContext 的保护能力"""

    print("\n" + "="*70)
    print("SafeExecutionContext 保护能力评估")
    print("="*70)

    total_files = stats['total_files']

    # 1. 统计可被保护的文件
    protected_operations = {
        'open()': stats['uses_open'],
        'os module imports': stats['imports_os'],
        'sys module imports': stats['imports_sys'],
        'eval': stats['calls_eval'],
        'exec': stats['calls_exec'],
        'subprocess': stats['calls_subprocess'],
    }

    # 2. 统计可能绕过的文件
    bypass_operations = {
        'pathlib usage': stats['uses_pathlib'] + stats['imports_pathlib'],
        'os.chdir': stats['calls_os_chdir'],
        'os.listdir/walk': stats['calls_os_listdir'] + stats['calls_os_walk'],
        'os.system': stats['calls_os_system'],
        'pathlib read': stats['pathlib_read'],
        'pathlib write': stats['pathlib_write'],
    }

    print("\n✅ SafeExecutionContext 能够保护的操作：\n")
    protected_files = set()
    for op_name, files in protected_operations.items():
        files = list(set(files))
        if files:
            print(f"  {op_name}: {len(files)} 个文件")
            protected_files.update(files)

    print(f"\n  总计被保护的文件: {len(protected_files)} 个")

    print("\n❌ SafeExecutionContext 无法保护的操作（可能被绕过）：\n")
    vulnerable_files = set()
    for op_name, files in bypass_operations.items():
        files = list(set(files))
        if files:
            print(f"  {op_name}: {len(files)} 个文件")
            vulnerable_files.update(files)

    print(f"\n  总计有漏洞的文件: {len(vulnerable_files)} 个")

    # 3. 统计完全安全的文件
    all_risky_files = protected_files | vulnerable_files
    safe_files = total_files - len(all_risky_files)

    print("\n" + "="*70)
    print("总体统计")
    print("="*70)

    print(f"\n总文件数: {total_files}")
    print(f"  🟢 完全不含任何危险操作: {safe_files} ({safe_files/total_files*100:.1f}%)")
    print(f"  ✅ 使用危险操作但被保护: {len(protected_files - vulnerable_files)} ({len(protected_files - vulnerable_files)/total_files*100:.1f}%)")
    print(f"  ⚠️  使用危险操作且部分可绕过: {len(protected_files & vulnerable_files)} ({len(protected_files & vulnerable_files)/total_files*100:.1f}%)")
    print(f"  ❌ 使用危险操作且完全可绕过: {len(vulnerable_files - protected_files)} ({len(vulnerable_files - protected_files)/total_files*100:.1f}%)")

    # 4. 风险评估
    print("\n" + "="*70)
    print("风险等级分类")
    print("="*70)

    # 高风险：使用 pathlib 或 os.chdir
    high_risk = set(stats['uses_pathlib']) | set(stats['imports_pathlib']) | set(stats['calls_os_chdir'])

    # 中风险：使用 os.listdir/walk 或 os.system
    medium_risk = (set(stats['calls_os_listdir']) | set(stats['calls_os_walk']) |
                   set(stats['calls_os_system'])) - high_risk

    # 低风险：仅使用 open() 和导入 os/sys
    low_risk = (set(stats['uses_open']) | set(stats['imports_os']) |
                set(stats['imports_sys'])) - high_risk - medium_risk

    print(f"\n🔴 高风险（pathlib/os.chdir）: {len(high_risk)} 个文件")
    if high_risk:
        print("   这些文件可以完全绕过 SafeExecutionContext")
        for f in sorted(list(high_risk))[:10]:
            print(f"     - {f}")
        if len(high_risk) > 10:
            print(f"     ... 还有 {len(high_risk) - 10} 个")

    print(f"\n🟠 中风险（os.listdir/walk/system）: {len(medium_risk)} 个文件")
    if medium_risk:
        print("   这些文件可以泄露信息或执行命令")
        for f in sorted(list(medium_risk))[:5]:
            print(f"     - {f}")
        if len(medium_risk) > 5:
            print(f"     ... 还有 {len(medium_risk) - 5} 个")

    print(f"\n🟡 低风险（open/import os/sys）: {len(low_risk)} 个文件")
    print("   这些文件被 SafeExecutionContext 有效保护")

    print(f"\n🟢 无风险: {safe_files} 个文件")
    print("   这些文件不含任何危险操作")

    # 5. 最终评估
    print("\n" + "="*70)
    print("最终评估")
    print("="*70)

    total_protected = safe_files + len(low_risk)
    total_vulnerable = len(high_risk) + len(medium_risk)

    print(f"\n✅ 安全/被保护: {total_protected}/{total_files} ({total_protected/total_files*100:.1f}%)")
    print(f"❌ 有漏洞: {total_vulnerable}/{total_files} ({total_vulnerable/total_files*100:.1f}%)")

    if total_vulnerable / total_files > 0.1:
        print(f"\n⚠️  警告: {total_vulnerable/total_files*100:.1f}% 的文件存在安全漏洞")
        print("   SafeExecutionContext 不足以保护这些文件")
        print("   建议：")
        print("     1. 增强 SafeExecutionContext（限制 pathlib, os.chdir 等）")
        print("     2. 使用 Docker 沙箱")
        print("     3. 重新生成高风险函数，移除危险操作")
    elif total_vulnerable / total_files > 0.05:
        print(f"\n⚠️  注意: {total_vulnerable/total_files*100:.1f}% 的文件存在安全漏洞")
        print("   SafeExecutionContext 基本够用，但建议增强")
    else:
        print(f"\n✅ 良好: 只有 {total_vulnerable/total_files*100:.1f}% 的文件存在漏洞")
        print("   SafeExecutionContext 基本满足需求")

    # 保存详细结果
    with open('/data/lhy/datasets/graph-Toucan/tool_info/safe_execution_analysis.json', 'w') as f:
        json.dump({
            'total_files': total_files,
            'safe_files': safe_files,
            'high_risk_files': sorted(list(high_risk)),
            'medium_risk_files': sorted(list(medium_risk)),
            'low_risk_files': sorted(list(low_risk)),
            'statistics': {
                'protected': total_protected,
                'vulnerable': total_vulnerable,
                'protection_rate': total_protected / total_files,
            }
        }, f, indent=2)

    print(f"\n📄 详细结果已保存到: tool_info/safe_execution_analysis.json")


def main():
    print("="*70)
    print("分析所有函数对 SafeExecutionContext 的依赖")
    print("="*70)
    print()

    analyzer = FunctionAnalyzer()
    analyzer.analyze_directory(GENERATED_FUNCTIONS_DIR)

    stats = analyzer.get_report()
    evaluate_safe_execution_context(stats)


if __name__ == "__main__":
    main()
