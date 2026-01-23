"""
读取 generated_functions 下的每个源文件，提取 call_external_api 函数，
根据函数的 docstring（特别是 Returns 部分）设计数据库 schema，写成 ORM 格式
"""
import os
import json
import asyncio
import ast
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
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
GENERATED_FUNCTIONS_DIR = os.path.join(ROOT_DIR, "tool_info", "generated_functions")
ORM_MODELS_FILE = os.path.join(ROOT_DIR, "tool_info", "orm_models.py")


def extract_call_external_api_function(file_path: str) -> Optional[Tuple[str, str, str]]:
    """
    从 Python 文件中提取 call_external_api 函数的代码和 docstring
    
    Args:
        file_path: Python 文件路径
        
    Returns:
        tuple: (function_code, docstring, tool_name) 或 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 AST
        tree = ast.parse(content, filename=file_path)
        
        # 查找 call_external_api 函数
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'call_external_api':
                # 提取函数代码
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
                lines = content.split('\n')
                function_code = '\n'.join(lines[start_line:end_line])
                
                # 提取 docstring
                docstring = ast.get_docstring(node)
                
                # 从文件名提取 tool_name
                tool_name = os.path.splitext(os.path.basename(file_path))[0]
                
                return function_code, docstring or "", tool_name
        
        return None
    except Exception as e:
        logger.error(f"提取 {file_path} 中的 call_external_api 函数时出错: {str(e)}")
        return None


def parse_returns_section(docstring: str) -> Dict[str, Any]:
    """
    解析 docstring 中的 Returns 部分，提取字段信息
    
    Args:
        docstring: 函数的 docstring
        
    Returns:
        dict: 包含字段信息的字典
    """
    if not docstring:
        return {"fields": []}
    
    fields = []
    lines = docstring.split('\n')
    in_returns = False
    returns_lines = []
    
    # 提取 Returns 部分
    for line in lines:
        line_stripped = line.strip()
        if 'Returns:' in line or 'returns:' in line.lower():
            in_returns = True
            continue
        if in_returns:
            # 如果遇到新的 section（如 Raises:），停止
            if line_stripped and not line.startswith(' ') and not line.startswith('\t') and ':' in line_stripped:
                if not any(keyword in line_stripped.lower() for keyword in ['returns', 'return']):
                    break
            if line_stripped:
                returns_lines.append(line)
    
    # 解析字段
    current_field = None
    for line in returns_lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # 匹配格式: field_name (type): description
        match = re.match(r'[-*]?\s*(\w+)\s*\(([^)]+)\):\s*(.+)', line_stripped)
        if match:
            field_name = match.group(1)
            field_type = match.group(2).strip()
            field_desc = match.group(3).strip()
            
            fields.append({
                "name": field_name,
                "type": field_type,
                "description": field_desc,
                "nested": []
            })
            current_field = fields[-1]
        # 匹配嵌套字段: - nested_field (type): description
        elif line_stripped.startswith('-') or line_stripped.startswith('*'):
            nested_match = re.match(r'[-*]\s*(\w+)\s*\(([^)]+)\):\s*(.+)', line_stripped)
            if nested_match and current_field:
                nested_name = nested_match.group(1)
                nested_type = nested_match.group(2).strip()
                nested_desc = nested_match.group(3).strip()
                current_field["nested"].append({
                    "name": nested_name,
                    "type": nested_type,
                    "description": nested_desc
                })
        # 匹配简单格式: field_name: description
        else:
            simple_match = re.match(r'[-*]?\s*(\w+):\s*(.+)', line_stripped)
            if simple_match:
                field_name = simple_match.group(1)
                field_desc = simple_match.group(2).strip()
                fields.append({
                    "name": field_name,
                    "type": "Any",
                    "description": field_desc,
                    "nested": []
                })
                current_field = fields[-1]
    
    return {"fields": fields}


async def generate_orm_model(
    tool_name: str,
    function_code: str,
    docstring: str,
    fields_info: Dict[str, Any],
    model: str = "qwen3-235b-a22b-instruct-2507"
) -> Tuple[str, Dict[str, Any]]:
    """
    使用大模型根据函数信息生成 ORM 模型代码
    
    Args:
        tool_name: 工具名称
        function_code: call_external_api 函数代码
        docstring: 函数 docstring
        fields_info: 解析出的字段信息
        model: 使用的模型名称
        
    Returns:
        tuple: (orm_model_code, token_usage)
    """
    # 构建字段描述
    fields_desc = []
    for field in fields_info.get("fields", []):
        field_line = f"- {field['name']} ({field['type']}): {field['description']}"
        if field.get("nested"):
            field_line += "\n  Nested fields:"
            for nested in field["nested"]:
                field_line += f"\n    - {nested['name']} ({nested['type']}): {nested['description']}"
        fields_desc.append(field_line)
    
    fields_text = "\n".join(fields_desc)
    
    prompt = f"""Based on the following call_external_api function, generate a SQLAlchemy ORM model class.

Tool Name: {tool_name}

Function Code:
```python
{function_code}
```

Function Docstring:
{docstring}

Extracted Fields Information:
{fields_text}

Requirements:
1. Use SQLAlchemy ORM (from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey)
2. Use SQLAlchemy declarative_base() for base class
3. Create a model class named based on the tool_name (convert to PascalCase, e.g., "airbnb-search" -> "AirbnbSearch")
4. For each field in the Returns section, create a corresponding Column
5. Map Python types to appropriate SQLAlchemy types:
   - str -> String or Text (use Text for long strings)
   - int -> Integer
   - float -> Float
   - bool -> Boolean
   - dict -> JSON
   - list -> JSON (store as JSON array)
   - Optional types should use nullable=True
6. For nested structures (Dict with nested fields), consider use JSON column
7. Add appropriate primary key (use id as Integer primary key)
8. Add __tablename__ attribute based on tool_name (convert to snake_case)
9. Include docstring for the class explaining what it represents
10. If there are list items with nested structures, create a separate model for the item type

Please return only the complete ORM model code, without any explanatory text, markdown code block markers, or other descriptions. The code should be directly usable."""

    try:
        response = await async_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional database architect, skilled at designing SQLAlchemy ORM models based on API response schemas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        orm_code = response.choices[0].message.content.strip()
        
        # 提取 token 使用信息
        token_usage = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            "total_tokens": response.usage.total_tokens if response.usage else 0,
        }
        
        # 清理代码（移除可能的 markdown 代码块标记）
        if orm_code.startswith("```python"):
            orm_code = orm_code[9:]
        elif orm_code.startswith("```"):
            orm_code = orm_code[3:]
        if orm_code.endswith("```"):
            orm_code = orm_code[:-3]
        orm_code = orm_code.strip()
        
        return orm_code, token_usage
        
    except Exception as e:
        raise RuntimeError(f"生成 ORM 模型时出错: {str(e)}") from e


async def process_single_file(
    file_path: str,
    model: str = "qwen3-235b-a22b-instruct-2507"
) -> Optional[Dict[str, Any]]:
    """
    处理单个文件，提取 call_external_api 并生成 ORM 模型
    
    Args:
        file_path: 文件路径
        model: 使用的模型名称
        
    Returns:
        dict: 处理结果，包含 orm_code, tool_name, token_usage 等
    """
    logger.info(f"处理文件: {os.path.basename(file_path)}")
    
    # 提取 call_external_api 函数
    result = extract_call_external_api_function(file_path)
    if not result:
        logger.warning(f"未找到 call_external_api 函数: {os.path.basename(file_path)}")
        return None
    
    function_code, docstring, tool_name = result
    
    if not docstring:
        logger.warning(f"call_external_api 函数没有 docstring: {tool_name}")
        return None
    
    # 解析 Returns 部分
    fields_info = parse_returns_section(docstring)
    
    if not fields_info.get("fields"):
        logger.warning(f"未解析到字段信息: {tool_name}")
        return None
    
    # 生成 ORM 模型
    try:
        orm_code, token_usage = await generate_orm_model(
            tool_name,
            function_code,
            docstring,
            fields_info,
            model
        )
        
        logger.info(f"成功生成 {tool_name} 的 ORM 模型 (tokens: {token_usage['total_tokens']})")
        
        return {
            "tool_name": tool_name,
            "orm_code": orm_code,
            "fields_info": fields_info,
            "token_usage": token_usage
        }
    except Exception as e:
        logger.error(f"生成 {tool_name} 的 ORM 模型时出错: {str(e)}")
        return None


async def generate_all_orm_models(
    source_dir: str = GENERATED_FUNCTIONS_DIR,
    output_file: str = ORM_MODELS_FILE,
    model: str = "qwen3-235b-a22b-instruct-2507"
):
    """
    为所有源文件生成 ORM 模型并统一写到一个文件中
    
    Args:
        source_dir: 源文件目录
        output_file: 输出文件路径
        model: 使用的模型名称
    """
    # 获取所有 Python 文件（排除 __pycache__ 和 helper_func.py）
    source_files = []
    for file in os.listdir(source_dir):
        if file.endswith('.py') and file != 'helper_func.py' and file != '__init__.py':
            source_files.append(os.path.join(source_dir, file))
    
    logger.info(f"找到 {len(source_files)} 个文件需要处理")
    logger.info(f"源目录: {source_dir}")
    logger.info(f"输出文件: {output_file}")
    logger.info(f"使用模型: {model}")
    
    # 批量处理，使用 asyncio.gather 并发执行所有任务
    tasks = [process_single_file(file_path, model) for file_path in source_files]
    
    # 使用 tqdm 显示进度（如果可用）
    try:
        from tqdm.asyncio import tqdm
        results = []
        for coro in tqdm.as_completed(tasks, total=len(tasks), desc="生成 ORM 模型"):
            result = await coro
            if result:
                results.append(result)
    except ImportError:
        # 如果没有 tqdm，使用普通方式
        results = [r for r in await asyncio.gather(*tasks) if r is not None]
    
    # 统计结果
    success_count = len(results)
    total_tokens = sum(r.get("token_usage", {}).get("total_tokens", 0) for r in results)
    
    # 生成统一的 ORM 模型文件
    orm_file_content = """\"\"\"
Auto-generated ORM models based on call_external_api functions from generated_functions.
This file contains SQLAlchemy ORM models for all external API response schemas.
\"\"\"

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

"""
    
    # 添加所有 ORM 模型
    for result in results:
        tool_name = result["tool_name"]
        orm_code = result["orm_code"]
        
        # 添加分隔注释
        orm_file_content += f"\n\n# ===== ORM Model for {tool_name} =====\n"
        orm_file_content += orm_code
        orm_file_content += "\n"
    
    # 写入文件
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(orm_file_content)
    
    logger.info(f"\n生成完成！")
    logger.info(f"总计: {len(source_files)} 个文件")
    logger.info(f"成功生成: {success_count} 个 ORM 模型")
    logger.info(f"总 token 使用: {total_tokens}")
    logger.info(f"ORM 模型文件已保存到: {output_file}")
    
    # 保存统计信息
    summary = {
        "total_files": len(source_files),
        "success_count": success_count,
        "total_tokens": total_tokens,
        "models": [
            {
                "tool_name": r["tool_name"],
                "fields_count": len(r.get("fields_info", {}).get("fields", [])),
                "token_usage": r.get("token_usage", {})
            }
            for r in results
        ]
    }
    
    summary_file = output_file.replace('.py', '_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"统计信息已保存到: {summary_file}")


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="从 generated_functions 提取 call_external_api 并生成 ORM 模型")
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
        "--output-file",
        type=str,
        default=ORM_MODELS_FILE,
        help="输出文件路径"
    )
    
    args = parser.parse_args()
    
    await generate_all_orm_models(
        source_dir=args.source_dir,
        output_file=args.output_file,
        model=args.model
    )


if __name__ == "__main__":
    asyncio.run(main())
