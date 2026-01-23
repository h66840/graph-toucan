"""
使用 LLM 修复 generated_functions_v1 目录下 Python 文件的代码问题
主要修复函数名中的非法字符（连字符、括号、点号等）和其他语法错误
"""
import os
import json
import asyncio
import logging
import ast
import re
from typing import Dict, List, Any, Optional, Tuple
from openai import AsyncOpenAI

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 尝试导入 tqdm，如果不可用则使用简单的进度显示
try:
    from tqdm.asyncio import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    # 创建一个简单的 tqdm 替代类
    class tqdm:
        def __init__(self, *args, **kwargs):
            self.total = kwargs.get('total', 0)
            self.desc = kwargs.get('desc', '')
            self.unit = kwargs.get('unit', '')
            self.ncols = kwargs.get('ncols', 80)
            self.current = 0
            if self.desc:
                logger.info(f"{self.desc}: 开始处理 {self.total} 个任务")
        
        def __enter__(self):
            return self
        
        def __exit__(self, *args):
            if self.desc:
                logger.info(f"{self.desc}: 完成 {self.current}/{self.total}")
        
        def update(self, n=1):
            self.current += n
            if self.current % 10 == 0 or self.current == self.total:
                logger.info(f"{self.desc}: 进度 {self.current}/{self.total} ({self.current*100//self.total if self.total > 0 else 0}%)")
        
        def set_postfix(self, *args, **kwargs):
            # 在日志中显示额外信息
            if kwargs:
                logger.debug(f"当前状态: {kwargs}")
        
        def close(self):
            if self.desc:
                logger.info(f"{self.desc}: 完成 {self.current}/{self.total}")

# 初始化异步 OpenAI 客户端
async_client = AsyncOpenAI(
    api_key="EMPTY",
    base_url="http://10.1.144.30:8000/v1",
)

ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
GENERATED_FUNCTIONS_DIR = os.path.join(ROOT_DIR, "tool_info", "generated_functions_v1")
FAILED_FUNCTIONS_FILE = os.path.join(ROOT_DIR, "tool_info", "failed_functions.json")
FIX_CODE_STATUS_FILE = os.path.join(ROOT_DIR, "tool_info", "llm_fix_code_status.json")
REGENERATE_SUMMARY_FILE = os.path.join(ROOT_DIR, "tool_info", "regenerate_code_summary.json")

# Python 标识符允许的字符：字母、数字、下划线，以及中文字符
VALID_IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5]*$')


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
        ast.parse(code, filename=filename)
        return True, None
    except SyntaxError as e:
        error_msg = f"语法错误: {e.msg} (行 {e.lineno}, 列 {e.offset})"
        if e.text:
            error_msg += f"\n  代码: {e.text.strip()}"
        return False, error_msg
    except Exception as e:
        return False, f"检查语法时出错: {str(e)}"


def find_invalid_function_names(code: str) -> List[Dict[str, Any]]:
    """
    查找代码中所有包含非法字符的函数名
    
    Args:
        code: Python 代码字符串
        
    Returns:
        List[Dict]: 包含非法字符的函数名信息列表
            每个字典包含: {'name': 函数名, 'line': 行号, 'line_content': 行内容}
    """
    invalid_functions = []
    lines = code.split('\n')
    
    # 匹配函数定义：def 函数名(参数)
    function_pattern = re.compile(r'^\s*def\s+([a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5\-\(\)\.\/]*)\s*\(')
    
    for line_num, line in enumerate(lines, 1):
        match = function_pattern.match(line)
        if match:
            func_name = match.group(1)
            # 检查函数名是否包含非法字符
            if not VALID_IDENTIFIER_PATTERN.match(func_name):
                invalid_functions.append({
                    'name': func_name,
                    'line': line_num,
                    'line_content': line.strip()
                })
    
    return invalid_functions


def sanitize_function_name(func_name: str) -> str:
    """
    将函数名中的非法字符替换为下划线
    
    Args:
        func_name: 原始函数名
        
    Returns:
        str: 清理后的函数名
    """
    # 替换所有非法字符为下划线
    # 非法字符包括：连字符、括号、点号、斜杠等
    sanitized = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fa5]', '_', func_name)
    
    # 确保不以数字开头
    if sanitized and sanitized[0].isdigit():
        sanitized = '_' + sanitized
    
    # 移除连续的下划线
    sanitized = re.sub(r'_+', '_', sanitized)
    
    # 移除开头和结尾的下划线
    sanitized = sanitized.strip('_')
    
    # 如果为空，使用默认名称
    if not sanitized:
        sanitized = 'function'
    
    return sanitized


def has_only_call_external_api(code: str) -> bool:
    """
    检测代码是否只有 call_external_api 函数（没有主函数）
    
    Args:
        code: Python 代码字符串
        
    Returns:
        bool: True 表示只有 call_external_api 函数，False 表示还有其他函数
    """
    lines = code.split('\n')
    
    # 匹配函数定义：def 函数名(参数)
    function_pattern = re.compile(r'^\s*def\s+([a-zA-Z_\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5\-\(\)\.\/]*)\s*\(')
    
    function_names = []
    for line in lines:
        match = function_pattern.match(line)
        if match:
            func_name = match.group(1)
            function_names.append(func_name)
    
    # 如果只有 call_external_api 函数，或者没有函数，返回 True
    if not function_names:
        return True
    
    # 过滤掉 call_external_api
    other_functions = [f for f in function_names if f != 'call_external_api']
    
    # 如果只有 call_external_api 或没有其他函数，返回 True
    return len(other_functions) == 0


async def fix_code_with_llm(
    code: str,
    filename: str,
    invalid_functions: List[Dict[str, Any]],
    syntax_error: Optional[str] = None,
    model: str = "/data/models/Qwen/Qwen3-235B-A22B-Instruct-2507/",
    max_retries: int = 1
) -> Tuple[str, bool, Dict[str, Any]]:
    """
    使用 LLM 修复代码中的函数名非法字符和其他语法错误
    
    Args:
        code: 原始代码
        filename: 文件名
        invalid_functions: 包含非法字符的函数名列表
        syntax_error: 语法错误信息（如果有）
        model: 使用的模型名称
        max_retries: 最大重试次数
        
    Returns:
        tuple: (fixed_code, is_valid, token_usage)
            - fixed_code: 修复后的代码
            - is_valid: 修复后是否语法正确
            - token_usage: token 使用统计
    """
    # 构建问题描述
    issues = []
    if invalid_functions:
        issues.append("函数名包含非法字符（如连字符、括号、点号等），需要修复为合法的 Python 标识符：")
        for func in invalid_functions:
            issues.append(f"  - 第 {func['line']} 行: {func['name']} -> 应改为合法标识符")
    
    if syntax_error:
        issues.append(f"\n语法错误：\n{syntax_error}")
    
    issues_text = "\n".join(issues)
    
    prompt = f"""请修复以下 Python 代码中的问题。

文件名: {filename}

问题列表:
{issues_text}

原始代码:
```python
{code}
```

修复要求:
1. 将所有包含非法字符的函数名修复为合法的 Python 标识符（只能包含字母、数字、下划线和中文）
2. 函数名中的连字符(-)、括号(())、点号(.)、斜杠(/)等非法字符应替换为下划线(_)
3. 修复所有语法错误
4. 保持原有功能和逻辑不变
5. 如果函数名被修改，需要同时更新函数内部对该函数的调用（如果有）
6. 确保修复后的代码可以通过 Python 语法检查

请只返回修复后的完整代码，不要包含任何解释文字、markdown 代码块标记或其他描述。"""

    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0
    }
    
    fixed_code = code
    
    for attempt in range(max_retries):
        try:
            logger.info(f"尝试修复 {filename} (第 {attempt + 1}/{max_retries} 次)")
            
            response = await async_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional Python code repair expert, skilled at fixing function naming issues and syntax errors while preserving functionality."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
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
            
            # 检查是否还有非法函数名
            remaining_invalid = find_invalid_function_names(fixed_code)
            
            if is_valid and not remaining_invalid:
                logger.info(f"成功修复 {filename}")
                return fixed_code, True, total_token_usage
            else:
                if remaining_invalid:
                    logger.warning(f"修复后仍有非法函数名: {[f['name'] for f in remaining_invalid]}")
                if not is_valid:
                    logger.warning(f"修复后仍有语法错误: {new_error}")
                
                if attempt < max_retries - 1:
                    # 更新 prompt，包含新的错误信息
                    new_issues = []
                    if remaining_invalid:
                        new_issues.append("仍有函数名包含非法字符：")
                        for func in remaining_invalid:
                            new_issues.append(f"  - 第 {func['line']} 行: {func['name']}")
                    if not is_valid:
                        new_issues.append(f"\n仍有语法错误：\n{new_error}")
                    
                    prompt = f"""之前的修复仍有问题，请再次修复。

文件名: {filename}

原始问题:
{issues_text}

修复后的代码:
```python
{fixed_code}
```

新发现的问题:
{chr(10).join(new_issues)}

请再次修复所有问题，确保代码可以通过 Python 语法检查且所有函数名都是合法的标识符。只返回修复后的完整代码。"""
                else:
                    logger.error(f"达到最大重试次数，无法完全修复 {filename}")
                    return fixed_code, False, total_token_usage
                    
        except Exception as e:
            logger.error(f"修复代码时出错: {str(e)}")
            if attempt == max_retries - 1:
                return fixed_code, False, total_token_usage
    
    return fixed_code, False, total_token_usage


async def fix_single_file(
    file_path: str,
    model: str = "/data/models/Qwen/Qwen3-235B-A22B-Instruct-2507/",
    save_fixed: bool = True
) -> Dict[str, Any]:
    """
    修复单个文件的代码问题
    
    Args:
        file_path: 文件路径
        model: 使用的模型名称
        save_fixed: 是否保存修复后的代码
        
    Returns:
        dict: 处理结果信息
    """
    file_name = os.path.basename(file_path)
    logger.info(f"处理文件: {file_name}")
    
    try:
        # 读取源文件
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 检查是否只有 call_external_api 函数
        if has_only_call_external_api(code):
            logger.info(f"{file_name} 只有 call_external_api 函数，跳过 LLM 处理")
            return {
                "file": file_name,
                "status": "only_call_external_api",
                "reason": "文件只有 call_external_api 函数，需要单独处理"
            }
        
        # 检查语法
        is_valid, syntax_error = check_syntax(code, file_name)
        
        # 查找非法函数名
        invalid_functions = find_invalid_function_names(code)
        
        # 如果没有问题，跳过
        if is_valid and not invalid_functions:
            logger.info(f"{file_name} 无需修复")
            return {
                "file": file_name,
                "status": "no_issue",
                "reason": "代码无问题"
            }
        
        # 尝试修复
        logger.info(f"检测到问题，尝试修复: {file_name}")
        if invalid_functions:
            logger.info(f"  发现 {len(invalid_functions)} 个非法函数名")
        if syntax_error:
            logger.info(f"  发现语法错误: {syntax_error[:100]}...")
        
        fixed_code, is_fixed, token_usage = await fix_code_with_llm(
            code,
            file_name,
            invalid_functions,
            syntax_error,
            model
        )
        
        if is_fixed:
            # 保存修复后的代码
            if save_fixed:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_code)
                logger.info(f"已修复并保存 {file_name}")
            
            return {
                "file": file_name,
                "status": "fixed",
                "reason": "代码问题已修复",
                "invalid_functions_count": len(invalid_functions),
                "had_syntax_error": syntax_error is not None,
                "token_usage": token_usage
            }
        else:
            logger.warning(f"无法完全修复 {file_name}")
            return {
                "file": file_name,
                "status": "partially_fixed",
                "reason": "部分修复或无法完全修复",
                "invalid_functions_count": len(invalid_functions),
                "had_syntax_error": syntax_error is not None,
                "token_usage": token_usage
            }
        
    except Exception as e:
        logger.error(f"处理 {file_name} 时出错: {str(e)}", exc_info=True)
        return {
            "file": file_name,
            "status": "error",
            "error": str(e)
        }


async def fix_files_from_regenerate_summary(
    summary_file: str = REGENERATE_SUMMARY_FILE,
    model: str = "/data/models/Qwen/Qwen3-235B-A22B-Instruct-2507/",
    save_fixed: bool = True,
    batch_size: int = 5
):
    """
    从 regenerate_code_summary.json 读取重新生成的文件列表并修复
    
    Args:
        summary_file: regenerate 结果摘要文件路径
        model: 使用的模型名称
        save_fixed: 是否保存修复后的代码
        batch_size: 批处理大小
    """
    # 读取 regenerate 结果摘要
    if not os.path.exists(summary_file):
        logger.error(f"文件不存在: {summary_file}")
        return
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 从 results 中提取成功重新生成的文件名
    regenerated_files = []
    for result in data.get("results", []):
        if result.get("status") == "regenerated":
            file_name = result.get("file", "")
            if file_name:
                regenerated_files.append(file_name)
    
    if not regenerated_files:
        logger.info("没有需要修复的重新生成文件")
        return
    
    logger.info(f"从 {summary_file} 读取到 {len(regenerated_files)} 个重新生成的文件")
    
    # 构建完整文件路径
    file_paths = []
    for file_name in regenerated_files:
        file_path = os.path.join(GENERATED_FUNCTIONS_DIR, file_name)
        if os.path.exists(file_path):
            file_paths.append(file_path)
        else:
            logger.warning(f"文件不存在: {file_path}")
    
    logger.info(f"找到 {len(file_paths)} 个有效文件")
    
    # 批量处理，使用进度条
    results = []
    if HAS_TQDM:
        # 使用 tqdm 显示进度条
        tasks = [fix_single_file(file_path, model, save_fixed) for file_path in file_paths]
        pbar = tqdm(total=len(tasks), desc="修复文件", unit="文件", ncols=100)
        try:
            for coro in asyncio.as_completed(tasks):
                result = await coro
                results.append(result)
                pbar.update(1)
                # 更新进度条描述
                status = result.get("status", "unknown")
                file_name = os.path.basename(result.get("file", ""))[:25]
                pbar.set_postfix({
                    "当前": file_name,
                    "状态": status
                })
        finally:
            pbar.close()
    else:
        # 没有 tqdm，使用简单的日志输出
        for i in range(0, len(file_paths), batch_size):
            batch = file_paths[i:i + batch_size]
            logger.info(f"处理批次 {i // batch_size + 1} (文件 {i + 1}-{min(i + len(batch), len(file_paths))}/{len(file_paths)})")
            
            tasks = [fix_single_file(file_path, model, save_fixed) for file_path in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
    
    # 统计结果
    only_call_external_api_count = sum(1 for r in results if r.get("status") == "only_call_external_api")
    no_issue_count = sum(1 for r in results if r.get("status") == "no_issue")
    fixed_count = sum(1 for r in results if r.get("status") == "fixed")
    partially_fixed_count = sum(1 for r in results if r.get("status") == "partially_fixed")
    error_count = sum(1 for r in results if r.get("status") == "error")
    
    # 计算总 token 使用
    total_tokens = sum(
        r.get("token_usage", {}).get("total_tokens", 0)
        for r in results
        if r.get("status") in ["fixed", "partially_fixed"]
    )
    
    # 构建状态记录
    status_record = {
        "files_only_call_external_api": [],
        "files_no_issue": [],
        "files_fixed": [],
        "files_partially_fixed": [],
        "files_error": []
    }
    
    for r in results:
        file_name = r.get("file", "")
        status = r.get("status", "")
        
        if status == "only_call_external_api":
            status_record["files_only_call_external_api"].append(file_name)
        elif status == "no_issue":
            status_record["files_no_issue"].append(file_name)
        elif status == "fixed":
            status_record["files_fixed"].append(file_name)
        elif status == "partially_fixed":
            status_record["files_partially_fixed"].append({
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
        "total_files": len(file_paths),
        "only_call_external_api": only_call_external_api_count,
        "no_issue": no_issue_count,
        "fixed": fixed_count,
        "partially_fixed": partially_fixed_count,
        "error": error_count,
        "total_tokens": total_tokens,
        "status_record": status_record,
        "results": results
    }
    
    summary_path = os.path.join(os.path.dirname(summary_file), "llm_fix_regenerated_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # 保存状态记录
    with open(FIX_CODE_STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status_record, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n修复完成！")
    logger.info(f"总计: {len(file_paths)} 个文件")
    logger.info(f"只有 call_external_api: {only_call_external_api_count} (跳过 LLM 处理)")
    logger.info(f"无需修复: {no_issue_count}")
    logger.info(f"已修复: {fixed_count}")
    logger.info(f"部分修复: {partially_fixed_count}")
    logger.info(f"处理出错: {error_count}")
    logger.info(f"总 token 使用: {total_tokens}")
    logger.info(f"结果摘要已保存到: {summary_path}")
    logger.info(f"状态记录已保存到: {FIX_CODE_STATUS_FILE}")


async def fix_files_from_json(
    json_file: str = FAILED_FUNCTIONS_FILE,
    model: str = "/data/models/Qwen/Qwen3-235B-A22B-Instruct-2507/",
    save_fixed: bool = True,
    batch_size: int = 5
):
    """
    从 JSON 文件读取需要修复的文件列表并批量修复
    
    Args:
        json_file: 包含失败文件列表的 JSON 文件路径
        model: 使用的模型名称
        save_fixed: 是否保存修复后的代码
        batch_size: 批处理大小
    """
    # 读取失败文件列表
    if not os.path.exists(json_file):
        logger.error(f"文件不存在: {json_file}")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    failed_files = data.get("failed_files", [])
    
    if not failed_files:
        logger.info("没有需要修复的文件")
        return
    
    logger.info(f"从 {json_file} 读取到 {len(failed_files)} 个需要修复的文件")
    
    # 构建完整文件路径
    file_paths = []
    for file_name in failed_files:
        file_path = os.path.join(GENERATED_FUNCTIONS_DIR, file_name)
        if os.path.exists(file_path):
            file_paths.append(file_path)
        else:
            logger.warning(f"文件不存在: {file_path}")
    
    logger.info(f"找到 {len(file_paths)} 个有效文件")
    
    # 批量处理，使用进度条
    results = []
    if HAS_TQDM:
        # 使用 tqdm 显示进度条
        tasks = [fix_single_file(file_path, model, save_fixed) for file_path in file_paths]
        pbar = tqdm(total=len(tasks), desc="修复文件", unit="文件", ncols=100)
        try:
            for coro in asyncio.as_completed(tasks):
                result = await coro
                results.append(result)
                pbar.update(1)
                # 更新进度条描述
                status = result.get("status", "unknown")
                file_name = os.path.basename(result.get("file", ""))[:25]
                pbar.set_postfix({
                    "当前": file_name,
                    "状态": status
                })
        finally:
            pbar.close()
    else:
        # 没有 tqdm，使用简单的日志输出
        for i in range(0, len(file_paths), batch_size):
            batch = file_paths[i:i + batch_size]
            logger.info(f"处理批次 {i // batch_size + 1} (文件 {i + 1}-{min(i + len(batch), len(file_paths))}/{len(file_paths)})")
            
            tasks = [fix_single_file(file_path, model, save_fixed) for file_path in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
    
    # 统计结果
    only_call_external_api_count = sum(1 for r in results if r.get("status") == "only_call_external_api")
    no_issue_count = sum(1 for r in results if r.get("status") == "no_issue")
    fixed_count = sum(1 for r in results if r.get("status") == "fixed")
    partially_fixed_count = sum(1 for r in results if r.get("status") == "partially_fixed")
    error_count = sum(1 for r in results if r.get("status") == "error")
    
    # 计算总 token 使用
    total_tokens = sum(
        r.get("token_usage", {}).get("total_tokens", 0)
        for r in results
        if r.get("status") in ["fixed", "partially_fixed"]
    )
    
    # 构建状态记录
    status_record = {
        "files_only_call_external_api": [],
        "files_no_issue": [],
        "files_fixed": [],
        "files_partially_fixed": [],
        "files_error": []
    }
    
    for r in results:
        file_name = r.get("file", "")
        status = r.get("status", "")
        
        if status == "only_call_external_api":
            status_record["files_only_call_external_api"].append(file_name)
        elif status == "no_issue":
            status_record["files_no_issue"].append(file_name)
        elif status == "fixed":
            status_record["files_fixed"].append(file_name)
        elif status == "partially_fixed":
            status_record["files_partially_fixed"].append({
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
        "total_files": len(file_paths),
        "only_call_external_api": only_call_external_api_count,
        "no_issue": no_issue_count,
        "fixed": fixed_count,
        "partially_fixed": partially_fixed_count,
        "error": error_count,
        "total_tokens": total_tokens,
        "status_record": status_record,
        "results": results
    }
    
    summary_path = os.path.join(os.path.dirname(json_file), "llm_fix_code_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # 保存状态记录
    with open(FIX_CODE_STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status_record, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n修复完成！")
    logger.info(f"总计: {len(file_paths)} 个文件")
    logger.info(f"只有 call_external_api: {only_call_external_api_count} (跳过 LLM 处理)")
    logger.info(f"无需修复: {no_issue_count}")
    logger.info(f"已修复: {fixed_count}")
    logger.info(f"部分修复: {partially_fixed_count}")
    logger.info(f"处理出错: {error_count}")
    logger.info(f"总 token 使用: {total_tokens}")
    logger.info(f"结果摘要已保存到: {summary_path}")
    logger.info(f"状态记录已保存到: {FIX_CODE_STATUS_FILE}")


async def fix_all_files(
    source_dir: str = GENERATED_FUNCTIONS_DIR,
    model: str = "/data/models/Qwen/Qwen3-235B-A22B-Instruct-2507/",
    save_fixed: bool = True,
    batch_size: int = 5
):
    """
    修复目录下所有 Python 文件的代码问题
    
    Args:
        source_dir: 源文件目录
        model: 使用的模型名称
        save_fixed: 是否保存修复后的代码
        batch_size: 批处理大小
    """
    # 获取所有 Python 文件
    file_paths = []
    for file in os.listdir(source_dir):
        if file.endswith('.py') and file != '__init__.py':
            file_paths.append(os.path.join(source_dir, file))
    
    logger.info(f"找到 {len(file_paths)} 个文件需要检查")
    logger.info(f"源目录: {source_dir}")
    logger.info(f"使用模型: {model}")
    
    # 批量处理，使用进度条
    results = []
    if HAS_TQDM:
        # 使用 tqdm 显示进度条
        tasks = [fix_single_file(file_path, model, save_fixed) for file_path in file_paths]
        pbar = tqdm(total=len(tasks), desc="修复文件", unit="文件", ncols=100)
        try:
            for coro in asyncio.as_completed(tasks):
                result = await coro
                results.append(result)
                pbar.update(1)
                # 更新进度条描述
                status = result.get("status", "unknown")
                file_name = os.path.basename(result.get("file", ""))[:25]
                pbar.set_postfix({
                    "当前": file_name,
                    "状态": status
                })
        finally:
            pbar.close()
    else:
        # 没有 tqdm，使用简单的日志输出
        for i in range(0, len(file_paths), batch_size):
            batch = file_paths[i:i + batch_size]
            logger.info(f"处理批次 {i // batch_size + 1} (文件 {i + 1}-{min(i + len(batch), len(file_paths))}/{len(file_paths)})")
            
            tasks = [fix_single_file(file_path, model, save_fixed) for file_path in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
    
    # 统计结果（与 fix_files_from_json 相同的逻辑）
    only_call_external_api_count = sum(1 for r in results if r.get("status") == "only_call_external_api")
    no_issue_count = sum(1 for r in results if r.get("status") == "no_issue")
    fixed_count = sum(1 for r in results if r.get("status") == "fixed")
    partially_fixed_count = sum(1 for r in results if r.get("status") == "partially_fixed")
    error_count = sum(1 for r in results if r.get("status") == "error")
    
    total_tokens = sum(
        r.get("token_usage", {}).get("total_tokens", 0)
        for r in results
        if r.get("status") in ["fixed", "partially_fixed"]
    )
    
    status_record = {
        "files_only_call_external_api": [],
        "files_no_issue": [],
        "files_fixed": [],
        "files_partially_fixed": [],
        "files_error": []
    }
    
    for r in results:
        file_name = r.get("file", "")
        status = r.get("status", "")
        
        if status == "only_call_external_api":
            status_record["files_only_call_external_api"].append(file_name)
        elif status == "no_issue":
            status_record["files_no_issue"].append(file_name)
        elif status == "fixed":
            status_record["files_fixed"].append(file_name)
        elif status == "partially_fixed":
            status_record["files_partially_fixed"].append({
                "file": file_name,
                "reason": r.get("reason", "")
            })
        elif status == "error":
            status_record["files_error"].append({
                "file": file_name,
                "error": r.get("error", "")
            })
    
    summary = {
        "total_files": len(file_paths),
        "only_call_external_api": only_call_external_api_count,
        "no_issue": no_issue_count,
        "fixed": fixed_count,
        "partially_fixed": partially_fixed_count,
        "error": error_count,
        "total_tokens": total_tokens,
        "status_record": status_record,
        "results": results
    }
    
    summary_path = os.path.join(os.path.dirname(source_dir), "llm_fix_code_summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    with open(FIX_CODE_STATUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(status_record, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n修复完成！")
    logger.info(f"总计: {len(file_paths)} 个文件")
    logger.info(f"只有 call_external_api: {only_call_external_api_count} (跳过 LLM 处理)")
    logger.info(f"无需修复: {no_issue_count}")
    logger.info(f"已修复: {fixed_count}")
    logger.info(f"部分修复: {partially_fixed_count}")
    logger.info(f"处理出错: {error_count}")
    logger.info(f"总 token 使用: {total_tokens}")
    logger.info(f"结果摘要已保存到: {summary_path}")
    logger.info(f"状态记录已保存到: {FIX_CODE_STATUS_FILE}")


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="使用 LLM 修复 generated_functions_v1 中的代码问题")
    parser.add_argument(
        "--model",
        type=str,
        default="/data/models/Qwen/Qwen3-235B-A22B-Instruct-2507/",
        help="使用的模型名称（默认: qwen3-235b-a22b-instruct-2507）"
    )
    parser.add_argument(
        "--json-file",
        type=str,
        default=None,
        help=f"包含失败文件列表的 JSON 文件（默认: {FAILED_FUNCTIONS_FILE}）"
    )
    parser.add_argument(
        "--regenerate-summary",
        type=str,
        default=None,
        help=f"从 regenerate 结果摘要文件读取文件列表（默认: {REGENERATE_SUMMARY_FILE}）"
    )
    parser.add_argument(
        "--source-dir",
        type=str,
        default=None,
        help="源文件目录（如果指定，则修复目录下所有文件，而不是从 JSON 读取）"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="不保存修复后的代码（仅检查）"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=3,
        help="批处理大小（默认: 5）"
    )
    
    args = parser.parse_args()
    
    if args.source_dir:
        await fix_all_files(
            source_dir=args.source_dir,
            model=args.model,
            save_fixed=not args.no_save,
            batch_size=args.batch_size
        )
    elif args.regenerate_summary is not None:
        # 从 regenerate 结果读取
        summary_file = args.regenerate_summary if args.regenerate_summary else REGENERATE_SUMMARY_FILE
        await fix_files_from_regenerate_summary(
            summary_file=summary_file,
            model=args.model,
            save_fixed=not args.no_save,
            batch_size=args.batch_size
        )
    else:
        # 从 failed_functions.json 读取
        json_file = args.json_file if args.json_file else FAILED_FUNCTIONS_FILE
        await fix_files_from_json(
            json_file=json_file,
            model=args.model,
            save_fixed=not args.no_save,
            batch_size=args.batch_size
        )


if __name__ == "__main__":
    asyncio.run(main())

