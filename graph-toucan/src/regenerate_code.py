"""
重新生成只有 call_external_api 函数的文件
这些文件因为超了大模型的最大回复 token 而生成不完整
修改提示词：对于 list fields，只生成 1 个 item（原来是 2 个）
"""
import os
import json
import asyncio
import logging
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI
from graph import load_tools_with_output_schema
import yaml

# 导入原有的生成函数，但需要修改提示词
from tool_translate_code_v1 import (
    build_tool_info_text,
    load_config,
    async_client,
    DEFAULT_MODEL,
    TOOL_SCHEMA_WITH_OUTPUT_PATH,
    OUTPUT_CLASSIFICATION_PATH,
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
GENERATED_FUNCTIONS_DIR = os.path.join(ROOT_DIR, "tool_info", "generated_functions_v1")
FIX_CODE_STATUS_FILE = os.path.join(ROOT_DIR, "tool_info", "llm_fix_code_status.json")
REGENERATE_SUMMARY_FILE = os.path.join(ROOT_DIR, "tool_info", "regenerate_code_summary.json")


def get_tool_name_from_filename(filename: str) -> str:
    """
    从文件名推断工具名称
    例如: "akshare-one-mcp-server-get_income_statement.py" -> "akshare-one-mcp-server-get_income_statement"
    """
    # 移除 .py 扩展名
    tool_name = filename.replace('.py', '')
    return tool_name


async def generate_function_implementation_single_item(
    tool_name: str,
    tool_meta: Dict[str, Any],
    classification: Optional[Dict[str, Any]] = None,
    language: str = 'python',
) -> tuple[str, Dict[str, Any]]:
    """
    根据工具定义和分类结果，使用 LLM 生成函数实现。
    这是修改版本，对于 list fields 只生成 1 个 item（而不是 2 个）。
    
    Args:
        tool_name: str, 工具名称
        tool_meta: Dict, 从 tool_response_schema_v1.json 加载的工具元数据
        classification: Dict, 可选的分类结果（如果为 None，会尝试从文件加载）
        language: str, 目标编程语言，默认为 'python'
        
    Returns:
        tuple: (generated_code: str, token_usage: dict)
            - generated_code: 生成的函数代码
            - token_usage: token 使用统计
    """
    # 如果没有提供分类结果，尝试从文件加载
    if classification is None:
        classification_path = OUTPUT_CLASSIFICATION_PATH
        if os.path.exists(classification_path):
            with open(classification_path, "r", encoding="utf-8") as f:
                all_classifications = json.load(f)
            classification = all_classifications.get(tool_name)
    
    category = classification.get("category", "unknown") if classification else "unknown"
    
    # 构建工具信息
    tool_info = build_tool_info_text(tool_name, tool_meta)
    
    # 统一的 prompt，根据分类类型给出不同指导
    # 关键修改：将 "Generate 2 items" 改为 "Generate 1 item"
    prompt = f"""Generate a complete Python function implementation based on the tool definition and execution type.

=== TOOL INFORMATION ===
{tool_info}

=== EXECUTION TYPE: {category.upper()} ===

=== IMPLEMENTATION INSTRUCTIONS ===

**COMPUTATION Type:**
- Implement pure computation logic using ONLY input parameters
- No external API calls or network requests
- Use mathematical calculations, string operations, data transformations, etc.
- Generate realistic outputs based purely on input parameters
- Include necessary imports (e.g., `from typing import Dict, List, Any, Optional` as needed)

**QUERY/ACTION Types:**
- Create a helper function `call_external_api(tool_name: str) -> Dict[str, Any]` that returns data from external sources
- **CRITICAL: The `call_external_api` function MUST return ONLY simple fields (str, int, float, bool). NO nested structures (no dict, no list, no complex objects).**
- **Step 1: Analyze the output schema** - Look at the "Output fields" section above. For each field in the output schema:
  * If it's a nested object (e.g., "user.name"), flatten it to a simple field name (e.g., "user_name")
  * If it's a list/array (e.g., "items[].name"), create indexed fields (e.g., "item_0_name", etc.)
  * Keep the original field type (str, int, float, bool) for each flattened field
- The `call_external_api` function should:
  * Accept tool_name as parameter (use "{tool_name}" when calling)
  * Return a dictionary containing ONLY simple scalar values (str, int, float, bool)
  * Use flat field names to represent nested paths (e.g., "user_name", "user_age", "weather_temp", "weather_city" instead of nested dicts)
  * For list/array fields, use indexed field names (e.g., "item_0_name", "item_0_price")
  * **Generate only 1 item for list fields (use index 0 only)**
  * Document all fields in the function docstring with their types and descriptions
  * Example structure:
    ```python
    def call_external_api(tool_name: str) -> Dict[str, Any]:
        \"\"\"
        Simulates fetching data from external API.
        
        Returns:
            Dict with simple fields only (str, int, float, bool):
            - user_name (str): User's name
            - user_age (int): User's age
            - weather_temp (float): Temperature in Celsius
            - weather_city (str): City name
            - item_0_name (str): Item name
            - item_0_price (float): Item price
        \"\"\"
        return {{
            "user_name": "Alice",
            "user_age": 25,
            "weather_temp": 22.5,
            "weather_city": "Shanghai",
            "item_0_name": "iPhone",
            "item_0_price": 7999.0,
        }}
    ```
- **Step 2: In the main function**, write explicit construction logic:
  * Call `call_external_api("{tool_name}")` to get external data (which contains only simple fields)
  * **MUST write explicit code to construct nested structures** matching the output schema exactly
  * Map flat field names from `call_external_api` to nested output schema structure
  * For nested objects: create dict structures manually
  * For lists/arrays: collect indexed fields (item_0_*, etc.) into list of dicts
  * Example transformation logic (if output schema contains List, import List from typing):
    ```python
    from typing import Dict, List, Any
    
    # ... call_external_api function ...
    
    def main_function(...) -> Dict[str, Any]:  # or List[Dict[str, Any]] if needed
        api_data = call_external_api("{tool_name}")
        
        # Construct nested structure matching output schema
        result = {{
            "user": {{
                "name": api_data["user_name"],
                "age": api_data["user_age"]
            }},
            "weather": {{
                "temp": api_data["weather_temp"],
                "city": api_data["weather_city"]
            }},
            "items": [
                {{"name": api_data["item_0_name"], "price": api_data["item_0_price"]}}
            ]
        }}
        return result
    ```

=== REQUIREMENTS ===
1. Function name MUST be: {tool_name}
2. Include complete type hints for all parameters and return values
3. Add comprehensive docstring explaining purpose, parameters, and return value
4. Include proper error handling and input validation

=== OUTPUT FORMAT ===
Return ONLY the Python code. No explanations, no markdown blocks, no additional text."""

    try:
        response = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are an expert Python developer. Generate complete, production-ready Python function code based on tool definitions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
        )
        
        generated_code = response.choices[0].message.content.strip()
        
        # 清理代码（移除可能的 markdown 代码块标记）
        if generated_code.startswith("```python"):
            generated_code = generated_code[9:]
        elif generated_code.startswith("```"):
            generated_code = generated_code[3:]
        if generated_code.endswith("```"):
            generated_code = generated_code[:-3]
        generated_code = generated_code.strip()
        
        token_usage = {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
            "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            "total_tokens": response.usage.total_tokens if response.usage else 0,
        }
        
        return generated_code, token_usage
        
    except Exception as e:
        logger.error(f"生成代码时出错: {str(e)}")
        raise


async def regenerate_single_file(
    file_name: str,
    tool_name: str,
    tool_meta: Dict[str, Any],
    classification: Optional[Dict[str, Any]] = None,
    save_code: bool = True
) -> Dict[str, Any]:
    """
    重新生成单个文件的代码
    
    Args:
        file_name: 文件名
        tool_name: 工具名称
        tool_meta: 工具元数据
        classification: 分类结果
        save_code: 是否保存生成的代码
        
    Returns:
        dict: 处理结果信息
    """
    logger.info(f"重新生成: {file_name} (工具: {tool_name})")
    
    try:
        # 生成代码
        code, token_usage = await generate_function_implementation_single_item(
            tool_name,
            tool_meta,
            classification
        )
        
        # 保存代码
        if save_code:
            file_path = os.path.join(GENERATED_FUNCTIONS_DIR, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            logger.info(f"已保存: {file_name}")
        
        return {
            "file": file_name,
            "tool_name": tool_name,
            "status": "regenerated",
            "token_usage": token_usage,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"重新生成 {file_name} 时出错: {str(e)}", exc_info=True)
        return {
            "file": file_name,
            "tool_name": tool_name,
            "status": "error",
            "error": str(e),
            "token_usage": {}
        }


async def regenerate_all_files(
    status_file: str = FIX_CODE_STATUS_FILE,
    batch_size: int = 3,
    save_code: bool = True
):
    """
    重新生成所有只有 call_external_api 的文件
    
    Args:
        status_file: 状态文件路径
        batch_size: 批处理大小
        save_code: 是否保存生成的代码
    """
    # 读取状态文件
    if not os.path.exists(status_file):
        logger.error(f"状态文件不存在: {status_file}")
        return
    
    with open(status_file, 'r', encoding='utf-8') as f:
        status_data = json.load(f)
    
    # 获取只有 call_external_api 的文件列表
    files_only_call_external_api = status_data.get("files_only_call_external_api", [])
    
    if not files_only_call_external_api:
        logger.info("没有需要重新生成的文件")
        return
    
    logger.info(f"找到 {len(files_only_call_external_api)} 个需要重新生成的文件")
    
    # 加载工具定义和分类信息
    logger.info("加载工具定义和分类信息...")
    tools_with_output_schema, schema_data = load_tools_with_output_schema(TOOL_SCHEMA_WITH_OUTPUT_PATH)
    
    # 构建 tool_name -> schema_data 的映射，方便后续查找
    # 直接从原始文件读取以获取 key -> value 的映射
    tool_schema_map = {}
    with open(TOOL_SCHEMA_WITH_OUTPUT_PATH, "r", encoding="utf-8") as f:
        schema_file_data = json.load(f)
        for tool_name, schema_item in schema_file_data.items():
            if schema_item.get('output_schema_parsed'):  # 只包含有 output schema 的
                tool_schema_map[tool_name] = schema_item
    
    classifications = {}
    if os.path.exists(OUTPUT_CLASSIFICATION_PATH):
        with open(OUTPUT_CLASSIFICATION_PATH, "r", encoding="utf-8") as f:
            classifications = json.load(f)
    
    # 准备任务列表
    tasks = []
    for file_name in files_only_call_external_api:
        tool_name = get_tool_name_from_filename(file_name)
        tool_meta = tool_schema_map.get(tool_name)
        
        if not tool_meta:
            # 尝试查找：可能工具名在 schema_item 内部的 tool_name 字段
            found = False
            for schema_tool_name, schema_item in tool_schema_map.items():
                if schema_item.get('tool_name') == tool_name:
                    tool_meta = schema_item
                    tool_name = schema_tool_name  # 使用 schema 中的 key 作为工具名
                    found = True
                    logger.info(f"通过内部 tool_name 字段找到工具: {tool_name} (文件: {file_name})")
                    break
            
            if not found:
                logger.warning(f"未找到工具定义: {tool_name} (文件: {file_name})")
                logger.debug(f"可用的工具名示例: {list(tool_schema_map.keys())[:5]}")
                continue
        
        classification = classifications.get(tool_name)
        tasks.append((file_name, tool_name, tool_meta, classification))
    
    logger.info(f"准备重新生成 {len(tasks)} 个文件")
    
    # 批量处理
    results = []
    total = len(tasks)
    
    # 尝试导入 tqdm
    try:
        from tqdm.asyncio import tqdm
        HAS_TQDM = True
    except ImportError:
        HAS_TQDM = False
    
    if HAS_TQDM:
        # 使用 tqdm 显示进度条
        async def process_task(task):
            file_name, tool_name, tool_meta, classification = task
            return await regenerate_single_file(file_name, tool_name, tool_meta, classification, save_code)
        
        pbar = tqdm(total=total, desc="重新生成代码", unit="文件", ncols=100)
        try:
            task_coros = [process_task(task) for task in tasks]
            for coro in asyncio.as_completed(task_coros):
                result = await coro
                results.append(result)
                pbar.update(1)
                status = result.get("status", "unknown")
                file_name = result.get("file", "")[:25]
                pbar.set_postfix({
                    "当前": file_name,
                    "状态": status
                })
        finally:
            pbar.close()
    else:
        # 没有 tqdm，使用简单的批处理
        for i in range(0, total, batch_size):
            batch = tasks[i:i + batch_size]
            logger.info(f"处理批次 {i // batch_size + 1} (文件 {i + 1}-{min(i + len(batch), total)}/{total})")
            
            batch_tasks = [
                regenerate_single_file(file_name, tool_name, tool_meta, classification, save_code)
                for file_name, tool_name, tool_meta, classification in batch
            ]
            batch_results = await asyncio.gather(*batch_tasks)
            results.extend(batch_results)
    
    # 统计结果
    regenerated_count = sum(1 for r in results if r.get("status") == "regenerated")
    error_count = sum(1 for r in results if r.get("status") == "error")
    
    # 计算总 token 使用
    total_tokens = sum(
        r.get("token_usage", {}).get("total_tokens", 0)
        for r in results
        if r.get("status") == "regenerated"
    )
    
    # 保存结果摘要
    summary = {
        "total_files": total,
        "regenerated": regenerated_count,
        "error": error_count,
        "total_tokens": total_tokens,
        "results": results
    }
    
    with open(REGENERATE_SUMMARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    logger.info(f"\n重新生成完成！")
    logger.info(f"总计: {total} 个文件")
    logger.info(f"成功重新生成: {regenerated_count}")
    logger.info(f"失败: {error_count}")
    logger.info(f"总 token 使用: {total_tokens}")
    logger.info(f"结果摘要已保存到: {REGENERATE_SUMMARY_FILE}")


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="重新生成只有 call_external_api 的文件")
    parser.add_argument(
        "--status-file",
        type=str,
        default=FIX_CODE_STATUS_FILE,
        help=f"状态文件路径（默认: {FIX_CODE_STATUS_FILE}）"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1,
        help="批处理大小（默认: 3）"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="不保存生成的代码（仅测试）"
    )
    
    args = parser.parse_args()
    
    await regenerate_all_files(
        status_file=args.status_file,
        batch_size=args.batch_size,
        save_code=not args.no_save
    )


if __name__ == "__main__":
    asyncio.run(main())

