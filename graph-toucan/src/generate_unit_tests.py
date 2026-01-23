"""
为 generated_functions 文件夹中的每个 Python 文件生成单元测试
使用 OpenAI API 来生成测试代码
"""
import os
import json
import asyncio
import re
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from openai import AsyncOpenAI

# 导入修复语法错误的模块
from fix_syntax import check_syntax, fix_syntax_error

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化异步 OpenAI 客户端
async_client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
GENERATED_FUNCTIONS_DIR = os.path.join(ROOT_DIR, "tool_info", "generated_functions")
UNIT_TEST_DIR = os.path.join(ROOT_DIR, "tool_info", "unit_test")
STATUS_FILE = os.path.join(ROOT_DIR, "tool_info", "unit_test_status.json")


def extract_function_name_from_code(code: str) -> Optional[str]:
    """从代码中提取主函数名"""
    # 查找第一个 def 开头的函数定义（排除 call_external_api 等辅助函数）
    pattern = r'^def\s+([a-zA-Z_][a-zA-Z0-9_]+)\s*\('
    for line in code.split('\n'):
        match = re.match(pattern, line.strip())
        if match:
            func_name = match.group(1)
            # 跳过辅助函数
            if func_name not in ['call_external_api']:
                return func_name
    return None


def get_test_file_name(source_file: str) -> str:
    """根据源文件名生成测试文件名"""
    base_name = os.path.basename(source_file)
    # 将 .py 替换为 _test.py
    test_name = base_name.replace('.py', '_test.py')
    return test_name


async def generate_unit_test(
    function_code: str,
    function_name: str,
    source_file_name: str,
    model: str = "qwen3-235b-a22b-instruct-2507"
) -> tuple[str, Dict[str, Any]]:
    """
    使用 OpenAI API 生成单元测试代码
    
    Args:
        function_code: 函数源代码
        function_name: 函数名
        source_file_name: 源文件名
        model: 使用的模型名称
        
    Returns:
        tuple: (generated_test_code, token_usage)
    """
    prompt = f"""Please generate complete unit test code for the following Python function.

Requirements:
1. Use pytest framework
2. Must import necessary libraries: pytest, unittest.mock (if mocking is needed)
3. Tests should cover:
   - Normal function calls (2-3 test cases)
   - Boundary value testing (e.g., maximum, minimum, boundary values)
   - Exception cases (ValueError, TypeError, etc., according to the Raises section in the function documentation)
   - Input validation (invalid inputs, None values, etc.)
4. For functions that depend on external APIs (such as call_external_api), use unittest.mock.patch or pytest's monkeypatch to mock external API calls
5. Each test function name should start with test_ and clearly describe the test content
6. Each test case should have clear comments explaining the test purpose
7. Use assert statements for assertions, verifying the structure and content of return values
8. The test file should be able to run independently
9. If the function has multiple parameters, test different parameter combinations

Source file: {source_file_name}
Function name: {function_name}

Function code:
```python
{function_code}
```

Please return only the complete test code, without any explanatory text, markdown code block markers, or other descriptions. The test code should be directly runnable."""

    try:
        response = await async_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional Python test engineer, skilled at writing high-quality unit tests."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        test_code = response.choices[0].message.content.strip()
        
        # 提取 token 使用信息
        token_usage = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            "total_tokens": response.usage.total_tokens if response.usage else 0,
        }
        
        # 清理代码（移除可能的 markdown 代码块标记）
        # 移除开头的代码块标记
        if test_code.startswith("```python"):
            test_code = test_code[9:]
        elif test_code.startswith("```"):
            test_code = test_code[3:]
        
        # 移除结尾的代码块标记
        if test_code.endswith("```"):
            test_code = test_code[:-3]
        
        # 移除可能的说明文字（如果代码块前后有说明）
        lines = test_code.split('\n')
        code_start = 0
        code_end = len(lines)
        
        # 找到第一个实际的代码行（不是空行或说明）
        for i, line in enumerate(lines):
            if line.strip() and not line.strip().startswith('#'):
                # 检查是否是 Python 代码（包含 import, def, class 等）
                if any(keyword in line for keyword in ['import ', 'from ', 'def ', 'class ', 'pytest']):
                    code_start = i
                    break
        
        # 从后往前找到最后一个代码行
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip() and not lines[i].strip().startswith('#'):
                code_end = i + 1
                break
        
        test_code = '\n'.join(lines[code_start:code_end]).strip()
        
        return test_code, token_usage
        
    except Exception as e:
        raise RuntimeError(f"生成测试代码时出错: {str(e)}") from e


async def process_single_file(
    source_file_path: str,
    output_dir: str,
    model: str = "qwen3-235b-a22b-instruct-2507",
    fix_syntax: bool = True
) -> Dict[str, Any]:
    """
    处理单个源文件，生成对应的单元测试
    
    Args:
        source_file_path: 源文件路径
        output_dir: 输出目录
        model: 使用的模型名称
        fix_syntax: 是否尝试修复语法错误（如果发现语法错误）
        
    Returns:
        dict: 处理结果信息
    """
    source_file_name = os.path.basename(source_file_path)
    logger.info(f"处理文件: {source_file_name}")
    
    try:
        # 读取源文件
        with open(source_file_path, 'r', encoding='utf-8') as f:
            function_code = f.read()
        
        # 首先检查语法
        is_valid, syntax_error = check_syntax(function_code, source_file_name)
        fix_token_usage = None
        was_fixed = False
        
        if not is_valid:
            # 如果允许修复语法错误，尝试修复
            if fix_syntax:
                logger.info(f"检测到语法错误，尝试修复: {source_file_name}")
                fixed_code, is_fixed, fix_token_usage = await fix_syntax_error(
                    function_code,
                    syntax_error,
                    source_file_name,
                    model
                )
                
                if is_fixed:
                    # 保存修复后的代码
                    with open(source_file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_code)
                    logger.info(f"已修复并保存 {source_file_name}")
                    function_code = fixed_code
                    was_fixed = True
                else:
                    logger.warning(f"无法修复 {source_file_name} 的语法错误")
                    return {
                        "file": source_file_name,
                        "status": "syntax_error_unfixed",
                        "reason": "语法错误且无法修复",
                        "error_message": syntax_error,
                        "fix_token_usage": fix_token_usage
                    }
            else:
                logger.warning(f"跳过 {source_file_name}: 语法错误 - {syntax_error}")
                return {
                    "file": source_file_name,
                    "status": "syntax_error",
                    "reason": "语法错误",
                    "error_message": syntax_error
                }
        
        # 提取函数名
        function_name = extract_function_name_from_code(function_code)
        if not function_name:
            logger.warning(f"跳过 {source_file_name}: 未找到主函数")
            return {
                "file": source_file_name,
                "status": "skipped",
                "reason": "未找到主函数"
            }
        
        logger.info(f"为 {source_file_name} 的函数 {function_name} 生成测试...")
        
        # 生成测试代码
        test_code, token_usage = await generate_unit_test(
            function_code,
            function_name,
            source_file_name,
            model
        )
        
        logger.info(f"成功生成 {source_file_name} 的测试代码 (tokens: {token_usage['total_tokens']})")
        
        # 生成测试文件名
        test_file_name = get_test_file_name(source_file_name)
        test_file_path = os.path.join(output_dir, test_file_name)
        
        # 添加必要的导入语句
        # 计算相对路径
        source_dir_relative = os.path.relpath(
            os.path.dirname(source_file_path),
            output_dir
        ).replace('\\', '/')  # 统一使用 / 作为路径分隔符
        
        module_name = source_file_name.replace('.py', '')
        
        # 构建导入语句
        import_statements = [
            "import sys",
            "import os",
            "from pathlib import Path",
            "",
            "# 添加源文件目录到路径",
            f"source_dir = Path(__file__).parent.parent / 'tool_info' / 'generated_functions'",
            f"sys.path.insert(0, str(source_dir))",
            "",
            f"from {module_name} import {function_name}",
            "",
        ]
        
        # 检查测试代码中是否已经导入了函数
        needs_import = True
        if function_name in test_code:
            # 检查是否有正确的导入语句
            if f"from {module_name} import" in test_code or f"import {function_name}" in test_code:
                needs_import = False
        
        # 如果测试代码中没有正确的导入，添加它
        if needs_import:
            # 查找第一个 import 语句的位置
            lines = test_code.split('\n')
            import_end_idx = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    import_end_idx = i + 1
                elif line.strip() and not line.strip().startswith('#') and import_end_idx > 0:
                    break
            
            # 在导入语句后插入我们的导入
            import_block = '\n'.join(import_statements)
            if import_end_idx > 0:
                test_code = '\n'.join(lines[:import_end_idx]) + '\n' + import_block + '\n'.join(lines[import_end_idx:])
            else:
                test_code = import_block + test_code
        
        # 写入测试文件
        os.makedirs(output_dir, exist_ok=True)
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        logger.info(f"测试文件已保存: {test_file_path}")
        
        result = {
            "file": source_file_name,
            "test_file": test_file_name,
            "function_name": function_name,
            "status": "success",
            "token_usage": token_usage
        }
        
        # 如果修复过语法错误，记录修复的 token 使用
        if was_fixed and fix_token_usage:
            result["fix_token_usage"] = fix_token_usage
            result["was_syntax_fixed"] = True
        
        return result
        
    except Exception as e:
        logger.error(f"处理 {source_file_name} 时出错: {str(e)}", exc_info=True)
        return {
            "file": source_file_name,
            "status": "error",
            "error": str(e)
        }


async def generate_all_unit_tests(
    source_dir: str = GENERATED_FUNCTIONS_DIR,
    output_dir: str = UNIT_TEST_DIR,
    model: str = "qwen3-235b-a22b-instruct-2507",
    fix_syntax: bool = True
):
    """
    为所有源文件生成单元测试
    
    Args:
        source_dir: 源文件目录
        output_dir: 输出目录
        model: 使用的模型名称
        fix_syntax: 是否在发现语法错误时尝试修复
    """
    # 获取所有 Python 文件（排除 __pycache__ 和 helper_func.py）
    source_files = []
    for file in os.listdir(source_dir):
        if file.endswith('.py') and file != 'helper_func.py' and file != '__init__.py':
            source_files.append(os.path.join(source_dir, file))
    
    logger.info(f"找到 {len(source_files)} 个文件需要生成测试")
    logger.info(f"源目录: {source_dir}")
    logger.info(f"输出目录: {output_dir}")
    logger.info(f"使用模型: {model}")
    logger.info(f"自动修复语法错误: {fix_syntax}")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 批量处理，使用 asyncio.gather 并发执行所有任务
    tasks = [process_single_file(file_path, output_dir, model, fix_syntax) for file_path in source_files]
    
    # 使用 tqdm 显示进度（如果可用）
    try:
        from tqdm.asyncio import tqdm
        results = []
        for coro in tqdm.as_completed(tasks, total=len(tasks), desc="生成测试"):
            result = await coro
            results.append(result)
    except ImportError:
        # 如果没有 tqdm，使用普通方式
        results = await asyncio.gather(*tasks)
    
    # 统计结果
    success_count = sum(1 for r in results if r.get("status") == "success")
    error_count = sum(1 for r in results if r.get("status") == "error")
    skipped_count = sum(1 for r in results if r.get("status") == "skipped")
    syntax_error_count = sum(1 for r in results if r.get("status") == "syntax_error")
    syntax_error_unfixed_count = sum(1 for r in results if r.get("status") == "syntax_error_unfixed")
    
    # 计算总 token 使用（包括修复语法错误和生成测试的 tokens）
    total_tokens = 0
    fix_tokens = 0
    for r in results:
        if r.get("status") == "success":
            total_tokens += r.get("token_usage", {}).get("total_tokens", 0)
            # 如果修复过语法错误，也统计修复的 tokens
            if "fix_token_usage" in r:
                fix_tokens += r.get("fix_token_usage", {}).get("total_tokens", 0)
        elif r.get("status") == "syntax_error_unfixed":
            fix_tokens += r.get("fix_token_usage", {}).get("total_tokens", 0)
    
    # 构建状态记录
    status_record = {
        "files_with_ut": [],  # 已生成单元测试的文件
        "files_with_syntax_error_fixed": [],  # 修复了语法错误并生成UT的文件
        "files_with_syntax_error_unfixed": [],  # 有语法错误且无法修复的文件
        "files_skipped": [],  # 跳过的文件（未找到主函数等）
        "files_error": []  # 生成UT时出错的文件
    }
    
    for r in results:
        file_name = r.get("file", "")
        status = r.get("status", "")
        
        if status == "success":
            status_record["files_with_ut"].append(file_name)
            if "fix_token_usage" in r:
                status_record["files_with_syntax_error_fixed"].append(file_name)
        elif status == "syntax_error_unfixed":
            status_record["files_with_syntax_error_unfixed"].append({
                "file": file_name,
                "error": r.get("error_message", "")
            })
        elif status == "skipped":
            status_record["files_skipped"].append({
                "file": file_name,
                "reason": r.get("reason", "")
            })
        elif status == "error":
            status_record["files_error"].append({
                "file": file_name,
                "error": r.get("error", "")
            })
    
    # 保存结果摘要
    summary = {
        "total_files": len(source_files),
        "success": success_count,
        "error": error_count,
        "skipped": skipped_count,
        "syntax_error_unfixed": syntax_error_unfixed_count,
        "total_tokens": total_tokens,
        "fix_tokens": fix_tokens,
        "total_tokens_all": total_tokens + fix_tokens,
        "status_record": status_record,
        "results": results
    }
    
    summary_path = os.path.join(output_dir, "generation_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # 保存状态记录到单独的文件
    with open(STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status_record, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n生成完成！")
    logger.info(f"总计: {len(source_files)} 个文件")
    logger.info(f"成功生成UT: {success_count}")
    logger.info(f"  - 其中修复语法错误后生成: {len(status_record['files_with_syntax_error_fixed'])}")
    logger.info(f"生成UT时出错: {error_count}")
    logger.info(f"跳过: {skipped_count}")
    logger.info(f"语法错误且无法修复: {syntax_error_unfixed_count}")
    logger.info(f"生成UT的 token 使用: {total_tokens}")
    logger.info(f"修复语法的 token 使用: {fix_tokens}")
    logger.info(f"总 token 使用: {total_tokens + fix_tokens}")
    logger.info(f"结果摘要已保存到: {summary_path}")
    logger.info(f"状态记录已保存到: {STATUS_FILE}")
    
    # 如果有错误，打印错误文件列表
    if error_count > 0:
        error_files = [r["file"] for r in results if r.get("status") == "error"]
        logger.warning(f"出错的文件: {', '.join(error_files)}")
    
    # 如果有语法错误且无法修复，打印文件列表
    if syntax_error_unfixed_count > 0:
        syntax_error_files = [r["file"] for r in results if r.get("status") == "syntax_error_unfixed"]
        logger.warning(f"语法错误且无法修复的文件: {', '.join(syntax_error_files)}")


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="为 generated_functions 生成单元测试")
    parser.add_argument(
        "--model",
        type=str,
        default="qwen3-235b-a22b-instruct-2507",
        help="使用的模型名称（默认: qwen3-235b-a22b-instruct-2507）"
    )
    parser.add_argument(
        "--source-dir",
        type=str,
        default=GENERATED_FUNCTIONS_DIR,
        help="源文件目录"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=UNIT_TEST_DIR,
        help="输出目录"
    )
    parser.add_argument(
        "--no-fix-syntax",
        action="store_true",
        help="不自动修复语法错误（如果发现语法错误则跳过）"
    )
    
    args = parser.parse_args()
    
    await generate_all_unit_tests(
        source_dir=args.source_dir,
        output_dir=args.output_dir,
        model=args.model,
        fix_syntax=not args.no_fix_syntax
    )


if __name__ == "__main__":
    asyncio.run(main())
