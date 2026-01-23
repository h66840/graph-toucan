"""
使用大模型重新生成检测出的危险函数

功能：
1. 读取 danger_scan_report.json，获取所有危险函数文件
2. 对每个危险函数，使用 LLM 重新生成安全版本
3. 保持输入输出字段和格式完全一致
4. 移除所有危险操作（eval, exec, subprocess, 等）
5. 保存到新目录或覆盖原文件
"""
import asyncio
import json
import os
import ast
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

import yaml
from openai import AsyncOpenAI
from tqdm.asyncio import tqdm as async_tqdm


# 路径配置
ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
TOOL_INFO_DIR = os.path.join(ROOT_DIR, "tool_info")
GENERATED_FUNCTIONS_DIR = os.path.join(TOOL_INFO_DIR, "generated_functions_v1")
DANGER_REPORT_PATH = os.path.join(TOOL_INFO_DIR, "danger_scan_report.json")
REGENERATED_FUNCTIONS_DIR = os.path.join(TOOL_INFO_DIR, "generated_functions_v1_safe")
CONFIG_PATH = os.path.join(ROOT_DIR, "src", "config.yaml")
LOG_DIR = os.path.join(ROOT_DIR, "logs")
REGEN_LOG_PATH = os.path.join(LOG_DIR, "function_regeneration_log.jsonl")

# 确保目录存在
os.makedirs(REGENERATED_FUNCTIONS_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


def load_config(config_path: str = CONFIG_PATH) -> Dict[str, Any]:
    """加载配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


# 加载配置
config = load_config()

# 初始化 AsyncOpenAI 客户端
api_key_env = config["api"].get("api_key_env")
if api_key_env:
    api_key = os.getenv(api_key_env, "EMPTY")
else:
    api_key = config["api"].get("api_key", "EMPTY")
base_url = config["api"]["base_url"]

async_client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)

DEFAULT_MODEL = config["model"]["default"]


class FunctionAnalyzer:
    """分析函数的输入输出定义"""

    @staticmethod
    def extract_function_info(file_path: str) -> Optional[Dict[str, Any]]:
        """
        提取函数的完整信息

        Returns:
            dict: {
                'function_name': str,
                'docstring': str,
                'args': List[Dict],  # 参数信息
                'returns': str,       # 返回值描述
                'original_code': str, # 原始代码
            }
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=file_path)

            # 找到主函数（不是 call_external_api）
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name != 'call_external_api':
                    # 提取 docstring
                    docstring = ast.get_docstring(node) or ""

                    # 提取参数信息
                    args_info = []
                    for arg in node.args.args:
                        arg_name = arg.arg
                        # 尝试从 docstring 中提取参数描述
                        arg_type = None
                        if arg.annotation:
                            arg_type = ast.unparse(arg.annotation)
                        args_info.append({
                            'name': arg_name,
                            'type': arg_type,
                        })

                    return {
                        'function_name': node.name,
                        'docstring': docstring,
                        'args': args_info,
                        'returns': FunctionAnalyzer._extract_return_type(node),
                        'original_code': content,
                    }

            return None
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None

    @staticmethod
    def _extract_return_type(node: ast.FunctionDef) -> str:
        """提取返回类型"""
        if node.returns:
            return ast.unparse(node.returns)
        return "Any"


async def regenerate_function_safely(
    file_path: str,
    danger_info: Dict[str, Any],
    model: str = None
) -> Dict[str, Any]:
    """
    使用 LLM 重新生成安全版本的函数

    Args:
        file_path: 原始函数文件路径
        danger_info: 危险操作信息（从扫描报告获取）
        model: 使用的模型

    Returns:
        dict: {
            'success': bool,
            'new_code': str,
            'error': str,
            'token_usage': dict,
        }
    """
    if model is None:
        model = DEFAULT_MODEL

    # 分析原函数
    func_info = FunctionAnalyzer.extract_function_info(file_path)
    if not func_info:
        return {
            'success': False,
            'error': 'Failed to analyze function',
        }

    # 提取危险操作列表
    dangers = danger_info.get('dangers', [])
    danger_summary = []
    for danger in dangers:
        severity = danger.get('severity', 'UNKNOWN')
        danger_type = danger.get('type', 'unknown')
        reason = danger.get('reason', '')
        line = danger.get('line', '?')

        if danger_type == 'dangerous_builtin':
            func = danger.get('function', '?')
            danger_summary.append(f"Line {line}: Uses {func}() - {reason}")
        elif danger_type == 'dangerous_import':
            module = danger.get('module', '?')
            danger_summary.append(f"Line {line}: Imports {module} - {reason}")
        elif danger_type == 'dangerous_from_import':
            module = danger.get('module', '?')
            items = danger.get('items', [])
            danger_summary.append(f"Line {line}: From {module} imports {', '.join(items)} - {reason}")
        elif danger_type in ['dangerous_os_call', 'dangerous_subprocess']:
            func = danger.get('function', '?')
            danger_summary.append(f"Line {line}: Calls {func}() - {reason}")
        else:
            danger_summary.append(f"Line {line}: {danger_type} - {reason}")

    danger_text = "\n".join(danger_summary)

    # 构建 prompt
    prompt = f"""You are an expert Python developer tasked with rewriting a function to remove dangerous operations while maintaining the exact same interface and behavior.

## Original Function Information

**Function Name**: {func_info['function_name']}

**Original Code**:
```python
{func_info['original_code']}
```

**Docstring** (Input/Output specification):
```
{func_info['docstring']}
```

## Detected Dangerous Operations

{danger_text}

## Your Task

Rewrite this function to:

1. **CRITICAL REQUIREMENTS**:
   - Keep the EXACT SAME function signature (name, parameters, types)
   - Keep the EXACT SAME return type and structure
   - Keep the EXACT SAME docstring (copy it verbatim)
   - Maintain the same behavior from the user's perspective

2. **Security Requirements**:
   - Remove ALL dangerous operations:
     * NO eval(), exec(), compile(), __import__()
     * NO subprocess calls
     * NO os.system(), os.popen(), or similar
     * NO file operations (open(), pathlib file writes) UNLESS the function explicitly requires file I/O based on its docstring
     * If file operations are required, implement safe path validation
   - Use only safe Python built-ins and standard library functions

3. **Implementation Strategy**:
   - If the original function uses `eval()` for math: Use `ast.literal_eval()` or implement a safe expression parser
   - If it uses `subprocess`: Return simulated/mock results with proper structure
   - If it uses external APIs: Keep the `call_external_api()` helper function and use its results
   - If it uses file I/O: Add path validation to ensure operations stay within allowed directories

4. **Output Format**:
   - Return ONLY the complete Python code
   - Include all necessary imports
   - Include the `call_external_api()` function if it exists in the original
   - NO explanations, NO markdown code blocks, just the raw Python code

## Example Transformation

**Before (dangerous)**:
```python
def calc(expr: str) -> dict:
    result = eval(expr)  # Dangerous!
    return {{"result": result}}
```

**After (safe)**:
```python
import ast

def calc(expr: str) -> dict:
    try:
        # Safe evaluation using ast.literal_eval
        result = ast.literal_eval(expr)
        return {{"result": result}}
    except (ValueError, SyntaxError) as e:
        raise ValueError(f"Invalid expression: {{e}}")
```

Now generate the safe version of the function:"""

    try:
        completion = await async_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert Python security engineer. "
                        "You specialize in rewriting functions to remove security vulnerabilities "
                        "while maintaining exact functionality and interface compatibility. "
                        "You always follow instructions precisely and output only valid Python code."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.2,  # 低温度确保输出稳定
            max_completion_tokens=4096,
        )

        content = completion.choices[0].message.content.strip()

        # 清理可能的 markdown 代码块
        if content.startswith("```python"):
            content = content[9:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        # 验证生成的代码是否有效
        try:
            ast.parse(content)
        except SyntaxError as e:
            return {
                'success': False,
                'error': f'Generated code has syntax error: {e}',
                'new_code': content,
            }

        # 提取 token 使用信息
        usage = completion.usage
        token_usage = {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        }

        return {
            'success': True,
            'new_code': content,
            'token_usage': token_usage,
            'original_function': func_info['function_name'],
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
        }


async def verify_regenerated_function(new_code: str, original_func_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证重新生成的函数是否安全且接口一致

    Returns:
        dict: {
            'valid': bool,
            'issues': List[str],
        }
    """
    issues = []

    try:
        # 解析新代码
        tree = ast.parse(new_code)

        # 查找主函数
        main_func = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == original_func_info['function_name']:
                main_func = node
                break

        if not main_func:
            issues.append(f"Function {original_func_info['function_name']} not found in generated code")
            return {'valid': False, 'issues': issues}

        # 检查参数一致性
        new_args = [arg.arg for arg in main_func.args.args]
        original_args = [arg['name'] for arg in original_func_info['args']]
        if new_args != original_args:
            issues.append(f"Function signature mismatch: expected {original_args}, got {new_args}")

        # 检查是否还包含危险操作
        for node in ast.walk(tree):
            # 检查危险的函数调用
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', 'compile', '__import__']:
                        issues.append(f"Still contains dangerous function: {node.func.id}")
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr
                    if func_name in ['run', 'call', 'Popen', 'system', 'popen']:
                        issues.append(f"Still contains dangerous function: {func_name}")

            # 检查危险的模块导入
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in ['subprocess', 'os']:
                            # 允许导入，但需要检查使用方式
                            pass
                elif isinstance(node, ast.ImportFrom):
                    if node.module in ['subprocess']:
                        issues.append(f"Still imports from dangerous module: {node.module}")

        return {
            'valid': len(issues) == 0,
            'issues': issues,
        }

    except SyntaxError as e:
        return {
            'valid': False,
            'issues': [f'Syntax error: {e}'],
        }
    except Exception as e:
        return {
            'valid': False,
            'issues': [f'Verification error: {e}'],
        }


async def process_dangerous_file(
    file_name: str,
    danger_info: Dict[str, Any],
    overwrite: bool = False,
) -> Dict[str, Any]:
    """
    处理单个危险文件

    Args:
        file_name: 文件名
        danger_info: 危险信息
        overwrite: 是否覆盖原文件（False 时保存到新目录）

    Returns:
        处理结果字典
    """
    file_path = os.path.join(GENERATED_FUNCTIONS_DIR, file_name)

    if not os.path.exists(file_path):
        return {
            'file': file_name,
            'status': 'error',
            'error': 'File not found',
        }

    # 获取原函数信息
    func_info = FunctionAnalyzer.extract_function_info(file_path)
    if not func_info:
        return {
            'file': file_name,
            'status': 'error',
            'error': 'Failed to analyze function',
        }

    # 重新生成函数
    regen_result = await regenerate_function_safely(file_path, danger_info)

    if not regen_result['success']:
        return {
            'file': file_name,
            'status': 'regeneration_failed',
            'error': regen_result.get('error', 'Unknown error'),
        }

    new_code = regen_result['new_code']

    # 验证新函数
    verification = await verify_regenerated_function(new_code, func_info)

    if not verification['valid']:
        return {
            'file': file_name,
            'status': 'verification_failed',
            'issues': verification['issues'],
            'new_code': new_code,
        }

    # 保存新文件
    if overwrite:
        output_path = file_path
    else:
        output_path = os.path.join(REGENERATED_FUNCTIONS_DIR, file_name)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_code)

        return {
            'file': file_name,
            'status': 'success',
            'output_path': output_path,
            'token_usage': regen_result.get('token_usage', {}),
            'original_dangers': len(danger_info.get('dangers', [])),
        }

    except Exception as e:
        return {
            'file': file_name,
            'status': 'save_failed',
            'error': str(e),
        }


async def regenerate_all_dangerous_functions(
    max_files: Optional[int] = None,
    overwrite: bool = False,
    batch_size: int = 5,
    severity_filter: Optional[List[str]] = None,
    resume: bool = False,
) -> None:
    """
    批量重新生成所有危险函数

    Args:
        max_files: 最多处理多少个文件（用于测试）
        overwrite: 是否覆盖原文件
        batch_size: 并发批次大小
        severity_filter: 只处理特定严重级别的函数，如 ['CRITICAL', 'HIGH']
        resume: 是否启用断点续传（跳过已生成的文件）
    """
    # 加载扫描报告
    if not os.path.exists(DANGER_REPORT_PATH):
        print(f"❌ Danger report not found: {DANGER_REPORT_PATH}")
        print("Please run check_dangerous_operations.py first.")
        return

    with open(DANGER_REPORT_PATH, 'r', encoding='utf-8') as f:
        report = json.load(f)

    dangerous_files = report.get('dangerous_files', [])

    if not dangerous_files:
        print("✅ No dangerous files found!")
        return

    # 过滤严重级别
    if severity_filter:
        filtered_files = []
        for file_info in dangerous_files:
            dangers = file_info.get('dangers', [])
            # 检查是否有匹配的严重级别
            for danger in dangers:
                if danger.get('severity') in severity_filter:
                    filtered_files.append(file_info)
                    break
        dangerous_files = filtered_files
        print(f"🔍 Filtered to {len(dangerous_files)} files with severity: {severity_filter}")

    # 断点续传：跳过已生成的文件
    if resume:
        # 方法1: 检查输出目录中已存在的文件
        existing_files = set()
        if os.path.exists(REGENERATED_FUNCTIONS_DIR):
            existing_files = set(os.listdir(REGENERATED_FUNCTIONS_DIR))

        # 方法2: 从日志文件中读取已成功处理的文件
        successfully_processed = set()
        if os.path.exists(REGEN_LOG_PATH):
            with open(REGEN_LOG_PATH, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line.strip())
                        if log_entry.get('status') == 'success':
                            successfully_processed.add(log_entry.get('file'))
                    except:
                        continue

        # 合并两种方法的结果
        skip_files = existing_files | successfully_processed

        if skip_files:
            original_count = len(dangerous_files)
            dangerous_files = [f for f in dangerous_files if f['file'] not in skip_files]
            skipped_count = original_count - len(dangerous_files)

            print(f"\n🔄 Resume mode enabled:")
            print(f"   - Found {len(existing_files)} files in output directory")
            print(f"   - Found {len(successfully_processed)} successfully processed files in logs")
            print(f"   - Skipping {skipped_count} already processed files")
            print(f"   - Remaining {len(dangerous_files)} files to process")

            if len(dangerous_files) == 0:
                print("\n✅ All files already processed! Nothing to do.")
                return

    if max_files:
        dangerous_files = dangerous_files[:max_files]

    print(f"\n🔧 Regenerating {len(dangerous_files)} dangerous functions...")
    if overwrite:
        print("⚠️  WARNING: Will OVERWRITE original files!")
    else:
        print(f"📁 Saving to: {REGENERATED_FUNCTIONS_DIR}")
    print()

    # 批量处理
    total = len(dangerous_files)
    results = []
    total_tokens = 0
    success_count = 0
    failed_count = 0

    # 使用 async_tqdm 显示进度
    for i in range(0, total, batch_size):
        batch = dangerous_files[i:i + batch_size]

        tasks = [
            process_dangerous_file(
                file_info['file'],
                file_info,
                overwrite=overwrite
            )
            for file_info in batch
        ]

        batch_results = await asyncio.gather(*tasks, return_exceptions=True)

        for file_info, result in zip(batch, batch_results):
            if isinstance(result, Exception):
                result = {
                    'file': file_info['file'],
                    'status': 'exception',
                    'error': str(result),
                }

            results.append(result)

            # 统计
            if result['status'] == 'success':
                success_count += 1
                token_usage = result.get('token_usage', {})
                total_tokens += token_usage.get('total_tokens', 0)
            else:
                failed_count += 1

            # 记录日志
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                **result,
            }
            with open(REGEN_LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

        # 显示进度
        print(f"[Batch {i // batch_size + 1}/{(total + batch_size - 1) // batch_size}] "
              f"Success: {success_count}, Failed: {failed_count}, Tokens: {total_tokens}")

    # 打印总结
    print("\n" + "=" * 80)
    print("REGENERATION SUMMARY")
    print("=" * 80)
    print(f"Total files: {total}")
    print(f"✅ Success: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"🪙 Total tokens used: {total_tokens}")
    print()

    # 显示失败的文件
    if failed_count > 0:
        print("Failed files:")
        for result in results:
            if result['status'] != 'success':
                file = result['file']
                status = result['status']
                error = result.get('error', 'Unknown error')
                issues = result.get('issues', [])
                print(f"  ❌ {file}: {status}")
                if error:
                    print(f"     Error: {error}")
                if issues:
                    print(f"     Issues: {', '.join(issues[:3])}")

    print(f"\n📄 Detailed log saved to: {REGEN_LOG_PATH}")
    if not overwrite:
        print(f"📁 New functions saved to: {REGENERATED_FUNCTIONS_DIR}")

    # 保存摘要报告
    summary_path = os.path.join(LOG_DIR, "regeneration_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_files': total,
            'success_count': success_count,
            'failed_count': failed_count,
            'total_tokens': total_tokens,
            'results': results,
        }, f, indent=2, ensure_ascii=False)
    print(f"📊 Summary report saved to: {summary_path}")


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='Regenerate dangerous functions safely')
    parser.add_argument('--max-files', type=int, default=None,
                        help='Maximum number of files to process (for testing)')
    parser.add_argument('--overwrite', action='store_true',
                        help='Overwrite original files (default: save to new directory)')
    parser.add_argument('--batch-size', type=int, default=5,
                        help='Batch size for parallel processing')
    parser.add_argument('--severity', nargs='+', choices=['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
                        help='Only process files with specific severity levels')
    parser.add_argument('--test', action='store_true',
                        help='Test mode: process only 3 files')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from previous run (skip already processed files)')

    args = parser.parse_args()

    if args.test:
        print("🧪 Running in TEST mode (3 files only)...")
        args.max_files = 3

    asyncio.run(regenerate_all_dangerous_functions(
        max_files=args.max_files,
        overwrite=args.overwrite,
        batch_size=args.batch_size,
        severity_filter=args.severity,
        resume=args.resume,
    ))


if __name__ == "__main__":
    main()
