"""
修复 generated_functions 文件夹中 Python 文件的语法错误
使用 OpenAI API 来修复语法错误
"""
import os
import json
import asyncio
import logging
import ast
from typing import Dict, List, Any, Optional, Tuple
from openai import AsyncOpenAI

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
GENERATED_FUNCTIONS_DIR = os.path.join(ROOT_DIR, "tool_info", "generated_functions_v1")
FIX_SYNTAX_STATUS_FILE = os.path.join(ROOT_DIR, "tool_info", "fix_syntax_status.json")


def check_syntax(code: str, filename: str = "<string>") -> Tuple[bool, Optional[str]]:
    """
    检查 Python 代码的语法是否正确
    
    Args:
        code: 要检查的代码字符串
        filename: 文件名（用于错误信息）
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid: True 表示语法正确，False 表示语法错误
            - error_message: 如果语法错误，返回错误信息；否则为 None
    """
    try:
        # 使用 ast.parse 检查语法
        ast.parse(code, filename=filename)
        return True, None
    except SyntaxError as e:
        error_msg = f"语法错误: {e.msg} (行 {e.lineno}, 列 {e.offset})"
        if e.text:
            error_msg += f"\n  代码: {e.text.strip()}"
        return False, error_msg
    except Exception as e:
        return False, f"检查语法时出错: {str(e)}"


async def fix_syntax_error(
    code: str,
    syntax_error: str,
    filename: str,
    model: str = "qwen3-235b-a22b-instruct-2507",
    max_retries: int = 2
) -> Tuple[str, bool, Dict[str, Any]]:
    """
    使用大模型修复代码中的语法错误
    
    Args:
        code: 有语法错误的代码
        syntax_error: 语法错误信息
        filename: 文件名
        model: 使用的模型名称
        max_retries: 最大重试次数
        
    Returns:
        tuple: (fixed_code, is_valid, token_usage)
            - fixed_code: 修复后的代码
            - is_valid: 修复后是否语法正确
            - token_usage: token 使用统计
    """
    prompt = f"""The following Python code has syntax errors. Please fix these errors.

Filename: {filename}

Syntax error information:
{syntax_error}

Code with errors:
```python
{code}
```

Requirements:
1. Fix all syntax errors
2. Keep the original functionality and logic unchanged
3. Only fix syntax issues, do not change the business logic
4. Ensure the fixed code can pass Python syntax checking

Please return only the complete fixed code, without any explanatory text, markdown code block markers, or other descriptions."""

    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0
    }
    
    fixed_code = code
    
    for attempt in range(max_retries):
        try:
            logger.info(f"尝试修复 {filename} 的语法错误 (第 {attempt + 1}/{max_retries} 次)")
            
            response = await async_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional Python code repair expert, skilled at fixing syntax errors."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # 使用较低的温度以确保修复的准确性
            )
            
            fixed_code = response.choices[0].message.content.strip()
            
            # 更新 token 使用
            if response.usage:
                total_token_usage["prompt_tokens"] += response.usage.prompt_tokens
                total_token_usage["completion_tokens"] += response.usage.completion_tokens
                total_token_usage["total_tokens"] += response.usage.total_tokens
            
            # 清理代码（移除可能的 markdown 代码块标记）
            if fixed_code.startswith("```python"):
                fixed_code = fixed_code[9:]
            elif fixed_code.startswith("```"):
                fixed_code = fixed_code[3:]
            if fixed_code.endswith("```"):
                fixed_code = fixed_code[:-3]
            fixed_code = fixed_code.strip()
            
            # 检查修复后的代码是否语法正确
            is_valid, new_error = check_syntax(fixed_code, filename)
            
            if is_valid:
                logger.info(f"成功修复 {filename} 的语法错误")
                return fixed_code, True, total_token_usage
            else:
                logger.warning(f"修复后仍有语法错误: {new_error}")
                if attempt < max_retries - 1:
                    # 更新 prompt，包含新的错误信息
                    prompt = f"""The following Python code still has syntax errors after the previous fix. Please fix them again.

Filename: {filename}

Previous syntax error:
{syntax_error}

Fixed code:
```python
{fixed_code}
```

New syntax error:
{new_error}

Please fix all syntax errors again, ensuring the code can pass Python syntax checking. Return only the complete fixed code."""
                else:
                    logger.error(f"达到最大重试次数，无法修复 {filename} 的语法错误")
                    return fixed_code, False, total_token_usage
                    
        except Exception as e:
            logger.error(f"修复语法错误时出错: {str(e)}")
            if attempt == max_retries - 1:
                return fixed_code, False, total_token_usage
    
    return fixed_code, False, total_token_usage


async def fix_single_file(
    source_file_path: str,
    model: str = "qwen3-235b-a22b-instruct-2507",
    save_fixed: bool = True
) -> Dict[str, Any]:
    """
    修复单个文件的语法错误
    
    Args:
        source_file_path: 源文件路径
        model: 使用的模型名称
        save_fixed: 是否保存修复后的代码
        
    Returns:
        dict: 处理结果信息
    """
    source_file_name = os.path.basename(source_file_path)
    logger.info(f"处理文件: {source_file_name}")
    
    try:
        # 读取源文件
        with open(source_file_path, 'r', encoding='utf-8') as f:
            function_code = f.read()
        
        # 检查语法
        is_valid, syntax_error = check_syntax(function_code, source_file_name)
        
        if is_valid:
            logger.info(f"{source_file_name} 语法正确，无需修复")
            return {
                "file": source_file_name,
                "status": "no_error",
                "reason": "语法正确"
            }
        
        # 尝试修复语法错误
        logger.info(f"检测到语法错误，尝试修复: {source_file_name}")
        fixed_code, is_fixed, fix_token_usage = await fix_syntax_error(
            function_code,
            syntax_error,
            source_file_name,
            model
        )
        
        if is_fixed:
            # 保存修复后的代码
            if save_fixed:
                with open(source_file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_code)
                logger.info(f"已修复并保存 {source_file_name}")
            
            return {
                "file": source_file_name,
                "status": "fixed",
                "reason": "语法错误已修复",
                "fix_token_usage": fix_token_usage
            }
        else:
            logger.warning(f"无法修复 {source_file_name} 的语法错误")
            return {
                "file": source_file_name,
                "status": "unfixed",
                "reason": "语法错误且无法修复",
                "error_message": syntax_error,
                "fix_token_usage": fix_token_usage
            }
        
    except Exception as e:
        logger.error(f"处理 {source_file_name} 时出错: {str(e)}", exc_info=True)
        return {
            "file": source_file_name,
            "status": "error",
            "error": str(e)
        }


async def fix_all_syntax_errors(
    source_dir: str = GENERATED_FUNCTIONS_DIR,
    model: str = "qwen3-235b-a22b-instruct-2507",
    save_fixed: bool = True
):
    """
    修复所有源文件的语法错误
    
    Args:
        source_dir: 源文件目录
        model: 使用的模型名称
        save_fixed: 是否保存修复后的代码
    """
    # 获取所有 Python 文件（排除 __pycache__ 和 helper_func.py）
    source_files = []
    for file in os.listdir(source_dir):
        if file.endswith('.py') and file != 'helper_func.py' and file != '__init__.py':
            source_files.append(os.path.join(source_dir, file))
    
    logger.info(f"找到 {len(source_files)} 个文件需要检查语法")
    logger.info(f"源目录: {source_dir}")
    logger.info(f"使用模型: {model}")
    
    # 批量处理，使用 asyncio.gather 并发执行所有任务
    tasks = [fix_single_file(file_path, model, save_fixed) for file_path in source_files]
    
    # 使用 tqdm 显示进度（如果可用）
    try:
        from tqdm.asyncio import tqdm
        results = []
        for coro in tqdm.as_completed(tasks, total=len(tasks), desc="修复语法错误"):
            result = await coro
            results.append(result)
    except ImportError:
        # 如果没有 tqdm，使用普通方式
        results = await asyncio.gather(*tasks)
    
    # 统计结果
    no_error_count = sum(1 for r in results if r.get("status") == "no_error")
    fixed_count = sum(1 for r in results if r.get("status") == "fixed")
    unfixed_count = sum(1 for r in results if r.get("status") == "unfixed")
    error_count = sum(1 for r in results if r.get("status") == "error")
    
    # 计算总 token 使用
    total_tokens = sum(
        r.get("fix_token_usage", {}).get("total_tokens", 0)
        for r in results
        if r.get("status") in ["fixed", "unfixed"]
    )
    
    # 构建状态记录
    status_record = {
        "files_no_error": [],  # 语法正确的文件
        "files_fixed": [],  # 修复了语法错误的文件
        "files_unfixed": [],  # 有语法错误且无法修复的文件
        "files_error": []  # 处理时出错的文件
    }
    
    for r in results:
        file_name = r.get("file", "")
        status = r.get("status", "")
        
        if status == "no_error":
            status_record["files_no_error"].append(file_name)
        elif status == "fixed":
            status_record["files_fixed"].append(file_name)
        elif status == "unfixed":
            status_record["files_unfixed"].append({
                "file": file_name,
                "error": r.get("error_message", "")
            })
        elif status == "error":
            status_record["files_error"].append({
                "file": file_name,
                "error": r.get("error", "")
            })
    
    # 保存结果摘要
    summary = {
        "total_files": len(source_files),
        "no_error": no_error_count,
        "fixed": fixed_count,
        "unfixed": unfixed_count,
        "error": error_count,
        "total_tokens": total_tokens,
        "status_record": status_record,
        "results": results
    }
    
    summary_path = os.path.join(os.path.dirname(source_dir), "fix_syntax_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # 保存状态记录到单独的文件
    with open(FIX_SYNTAX_STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status_record, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n修复完成！")
    logger.info(f"总计: {len(source_files)} 个文件")
    logger.info(f"语法正确: {no_error_count}")
    logger.info(f"已修复: {fixed_count}")
    logger.info(f"无法修复: {unfixed_count}")
    logger.info(f"处理出错: {error_count}")
    logger.info(f"总 token 使用: {total_tokens}")
    logger.info(f"结果摘要已保存到: {summary_path}")
    logger.info(f"状态记录已保存到: {FIX_SYNTAX_STATUS_FILE}")
    
    # 如果有无法修复的文件，打印文件列表
    if unfixed_count > 0:
        unfixed_files = [r["file"] for r in results if r.get("status") == "unfixed"]
        logger.warning(f"无法修复的文件: {', '.join(unfixed_files)}")
    
    # 如果有错误，打印错误文件列表
    if error_count > 0:
        error_files = [r["file"] for r in results if r.get("status") == "error"]
        logger.warning(f"出错的文件: {', '.join(error_files)}")


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="修复 generated_functions 中的语法错误")
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
        "--no-save",
        action="store_true",
        help="不保存修复后的代码（仅检查）"
    )
    
    args = parser.parse_args()
    
    await fix_all_syntax_errors(
        source_dir=args.source_dir,
        model=args.model,
        save_fixed=not args.no_save
    )


if __name__ == "__main__":
    asyncio.run(main())
