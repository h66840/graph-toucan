import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI
from graph import load_tools_with_output_schema
import yaml
# 配置文件路径
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")


def load_config(config_path: str = CONFIG_PATH) -> Dict[str, Any]:
    """
    加载配置文件

    Args:
        config_path: 配置文件路径

    Returns:
        配置字典
    """
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


# 加载配置
config = load_config()

# 初始化 AsyncOpenAI 客户端
# 支持两种配置方式：
# 1. 通过环境变量：api_key_env: "DASHSCOPE_API_KEY"
# 2. 直接配置：api_key: "EMPTY"
api_key_env = config["api"].get("api_key_env")
if api_key_env:
    # 如果配置了 api_key_env，从环境变量读取
    api_key = os.getenv(api_key_env, "EMPTY")
else:
    # 否则直接从配置读取
    api_key = config["api"].get("api_key", "EMPTY")
base_url = config["api"]["base_url"]

async_client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)

# 模型配置
DEFAULT_MODEL = config["model"]["default"]

ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
TOOL_INFO_DIR = os.path.join(ROOT_DIR, "tool_info")
GRAPH_DIR = os.path.join(ROOT_DIR, "graph")

TOOL_SCHEMA_V1_PATH = os.path.join(TOOL_INFO_DIR, "tool_response_schema_v1.json")
TOOL_SCHEMA_WITH_OUTPUT_PATH = os.path.join(TOOL_INFO_DIR, "tool_schema_with_outputformat.json")
GRAPH_PATH = os.path.join(GRAPH_DIR, "test_graph_v1.5.1_acyclic.json")
OUTPUT_CLASSIFICATION_PATH = os.path.join(TOOL_INFO_DIR, "tool_execution_type_classification_v1.json")


def load_tool_definition_from_schema(tool_name: str, tool_schemas: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    从 tool_response_schema_v1.json 中读取指定 tool 的定义。
    
    Args:
        tool_name: str, 工具名称
        tool_schemas: Dict, 从 tool_response_schema_v1.json 加载的完整数据
        
    Returns:
        Dict: tool 的定义信息，包含 tool_schema 和 output_schema_parsed
    """
    return tool_schemas.get(tool_name)


def load_tool_definition(tool_file):
    """
    从文件中加载工具定义和示例
    
    Args:
        tool_file: str, 工具定义文件路径（如 test_tool.txt）
        
    Returns:
        tuple: (tool_definition: str, tool_example: str)
    """
    with open(tool_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割工具定义和示例部分
    parts = content.split('tool call example')
    tool_definition = parts[0].strip()
    tool_example = parts[1].strip() if len(parts) > 1 else ""
    
    return tool_definition, tool_example

# 然后需要依据函数schema来生成对应的可执行的python code，对于computation类型，可以直接写计算逻辑，基于param 写出计算逻辑 然后生成对应的output。
# 对于query 和 action，都是需要依赖于外部API才能执行的，这种情况 把来自于外部API的信息用占位符进行表示，基于占位符和参数写出函数逻辑，得到output。
async def generate_function_implementation(
    tool_name: str,
    tool_meta: Dict[str, Any],
    classification: Optional[Dict[str, Any]] = None,
    language: str = 'python',
) -> tuple[str, Dict[str, Any]]:
    """
    根据工具定义和分类结果，使用 LLM 生成函数实现。
    
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
  * If it's a list/array (e.g., "items[].name"), create indexed fields (e.g., "item_0_name", "item_1_name", etc.)
  * Keep the original field type (str, int, float, bool) for each flattened field
- The `call_external_api` function should:
  * Accept tool_name as parameter (use "{tool_name}" when calling)
  * Return a dictionary containing ONLY simple scalar values (str, int, float, bool)
  * Use flat field names to represent nested paths (e.g., "user_name", "user_age", "weather_temp", "weather_city" instead of nested dicts)
  * For list/array fields, use indexed field names (e.g., "item_0_name", "item_0_price", "item_1_name", "item_1_price")
  * Generate 2 items for list fields (use indices 0, 1)
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
            - item_0_name (str): First item name
            - item_0_price (float): First item price
            - item_1_name (str): Second item name
            - item_1_price (float): Second item price
        \"\"\"
        return {{
            "user_name": "Alice",
            "user_age": 25,
            "weather_temp": 22.5,
            "weather_city": "Shanghai",
            "item_0_name": "iPhone",
            "item_0_price": 7999.0,
            "item_1_name": "AirPods",
            "item_1_price": 1899.0,
        }}
    ```
- **Step 2: In the main function**, write explicit construction logic:
  * Call `call_external_api("{tool_name}")` to get external data (which contains only simple fields)
  * **MUST write explicit code to construct nested structures** matching the output schema exactly
  * Map flat field names from `call_external_api` to nested output schema structure
  * For nested objects: create dict structures manually
  * For lists/arrays: collect indexed fields (item_0_*, item_1_*, etc.) into list of dicts
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
                {{"name": api_data["item_0_name"], "price": api_data["item_0_price"]}},
                {{"name": api_data["item_1_name"], "price": api_data["item_1_price"]}}
            ]
        }}
        return result
    ```
  * Apply any necessary business logic, filtering, or transformations when constructing the nested structure
  * Ensure the final result matches the output schema structure exactly

=== REQUIREMENTS ===
1. **MUST include all necessary import statements at the top of the code**
   * Import from `typing` module: `Dict`, `List`, `Any`, `Optional` as needed
   * Import any other standard library modules if needed (e.g., `datetime`, `json`, `base64`)
   * Format imports properly: `from typing import Dict, List, Any, Optional`
   * Example:
     ```python
     from typing import Dict, List, Any, Optional
     ```
2. Function name MUST be: {tool_name}
3. Include complete type hints for all parameters and return values
   * If return type contains `List`, import `List` from typing
   * If return type contains `Optional`, import `Optional` from typing
   * Use proper type hints: `Dict[str, Any]`, `List[Dict[str, Any]]`, `Optional[str]`, etc.
4. Add comprehensive docstring explaining purpose, parameters, and return value
5. Include proper error handling and input validation

=== OUTPUT FORMAT ===
Return ONLY the Python code starting with import statements, then the functions. No explanations, no markdown blocks, no additional text."""

    try:
        completion = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert Python developer that generates {language} function implementations based on tool definitions and execution types.",
                },
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.3,
            max_completion_tokens=2048,
        )
        
        generated_code = completion.choices[0].message.content.strip()
        
        # 清理代码（移除可能的 markdown 代码块标记）
        if generated_code.startswith('```'):
            lines = generated_code.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            generated_code = '\n'.join(lines)
        
        token_usage = {
            'prompt_tokens': completion.usage.prompt_tokens,
            'completion_tokens': completion.usage.completion_tokens,
            'total_tokens': completion.usage.total_tokens,
        }
        
        return generated_code, token_usage
        
    except Exception as e:
        print(f"Error generating function implementation for '{tool_name}': {str(e)}")
        raise


async def generate_function_from_json(tool_json_file, language='python', output_file=None):
    """
    从 JSON 文件读取工具定义，生成函数实现
    
    Args:
        tool_json_file: str, 包含工具定义的 JSON 文件路径
        language: str, 目标编程语言，默认为 'python'
        output_file: str, 可选，输出文件路径
        
    Returns:
        tuple: (generated_code: str, token_usage: dict)
    """
    # 读取工具定义
    with open(tool_json_file, 'r', encoding='utf-8') as f:
        tool_definition = json.dumps(json.load(f), indent=2, ensure_ascii=False)
    
    # 构建提示词
    prompt = f"""You are a code generation assistant. Based on the tool definition provided below, generate a complete function implementation in {language}.

Tool Definition (JSON):
{tool_definition}

Requirements:
1. Generate a complete, working function implementation in {language}
2. The function should match the tool definition (name, parameters, description)
3. For demonstration purposes, you can use mock data or simple implementations if external APIs are needed
4. Include proper error handling
5. Add docstrings and comments where appropriate
6. Make sure the code is production-ready and follows best practices

Please generate only the function code, without any explanations or markdown formatting. Just the pure code."""

    try:
        completion = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that generates {language} function implementations based on tool definitions."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.3,
            max_completion_tokens=2048
        )
        
        generated_code = completion.choices[0].message.content.strip()
        
        # 清理代码（移除可能的 markdown 代码块标记）
        if generated_code.startswith('```'):
            lines = generated_code.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            generated_code = '\n'.join(lines)
        
        token_usage = {
            'prompt_tokens': completion.usage.prompt_tokens,
            'completion_tokens': completion.usage.completion_tokens,
            'total_tokens': completion.usage.total_tokens
        }
        
        # 如果指定了输出文件，保存代码
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(generated_code)
            print(f"Generated code saved to {output_file}")
        
        return generated_code, token_usage
        
    except Exception as e:
        print(f"Error generating function implementation: {str(e)}")
        raise


def build_tool_info_text(tool_name: str, tool_meta: Optional[Dict[str, Any]]) -> str:
    """
    构建工具信息的文本描述，用于分类。
    """
    if not tool_meta:
        return f"Tool name: {tool_name}\n(no schema info found)"
    
    tool_schema = tool_meta.get("function_schema", {}) or {}
    func = tool_schema.get("function", {}) or {}
    description = func.get("description", "")
    params = (func.get("parameters", {}) or {}).copy()
    
    # 输入参数信息
    param_lines: List[str] = []
    if params:
        properties = (params.get("properties") or {}) if isinstance(params, dict) else {}
        required = set(params.get("required") or [])
        for pname, pinfo in properties.items():
            if not isinstance(pinfo, dict):
                continue
            ptype = pinfo.get("type", "unknown")
            pdesc = pinfo.get("description", "")
            req_flag = "required" if pname in required else "optional"
            param_lines.append(f"  - {pname} ({ptype}, {req_flag}): {pdesc}")
    
    param_block = "\n".join(param_lines) if param_lines else "  (no parameters)"
    
    # 输出字段信息
    output_schema = tool_meta.get("output_schema_parsed", {}) or {}
    fields = output_schema.get("fields", []) or []
    output_lines: List[str] = []
    for field in fields:
        fname = field.get("name", "")
        ftype = field.get("type", "")
        fdesc = field.get("description", "")
        if fname:
            output_lines.append(f"  - {fname} ({ftype}): {fdesc}")
    
    output_block = "\n".join(output_lines) if output_lines else "  (no structured output schema)"
    
    info_text = (
        f"Tool name: {tool_name}\n"
        f"Description: {description}\n"
        f"Input parameters:\n{param_block}\n"
        f"Output fields:\n{output_block}"
    )
    return info_text


async def classify_single_tool(
    tool_name: str,
    tool_meta: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    使用 LLM 对单个 tool 进行分类。
    
    分类类别：
    1. 计算类（computation）：完全不依赖于外部信息源，只依赖于 tool param + 运算逻辑即可执行
    2. 查询类（query）：需要依赖外部API信息
    3. 执行类（action）：执行某些动作，除了依赖参数外仍依赖于外部API
    
    Returns:
        {
            "tool_name": str,
            "category": str,  # "computation" / "query" / "action"
            "reasoning": str,
            "error": str or None
        }
    """
    tool_info = build_tool_info_text(tool_name, tool_meta)
    
    prompt = f"""You are an expert tool classifier. Analyze the following tool and classify it into one of three categories based on its execution dependencies:

Tool Information:
{tool_info}

Classification Categories:
1. **computation**: The tool does NOT depend on any external information sources. It can be executed using only the tool parameters and computational logic (e.g., mathematical calculations, string manipulations, data transformations, format conversions). Examples: calculate sum, convert units, format text, parse JSON.

2. **query**: The tool depends on external API information sources to retrieve/query data. It reads or fetches information from external systems but does not modify external state. Examples: search database, fetch weather data, retrieve file content, query API.

3. **action**: The tool performs actions that modify external state or execute operations, and it depends on external APIs beyond just parameters. It changes something in the external world (create, update, delete, send, execute). Examples: create file, send email, update database record, execute command.

Output format (JSON only, no other text):
{{
    "category": "computation" | "query" | "action",
    "reasoning": "brief explanation of why this category was chosen"
}}"""

    try:
        completion = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert tool classifier. "
                        "Analyze tools and classify them into computation, query, or action categories. "
                        "Output only valid JSON, no other text."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.2,
            max_completion_tokens=256,
        )
        
        content = completion.choices[0].message.content.strip()
        
        # 尝试解析 JSON（可能包含 markdown 代码块）
        if content.startswith("```"):
            lines = content.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines)
        
        result = json.loads(content)
        
        return {
            "tool_name": tool_name,
            "category": result.get("category", "unknown"),
            "reasoning": result.get("reasoning", ""),
            "error": None,
        }
    except Exception as e:
        print(f"[ERROR] classify tool '{tool_name}' failed: {e}")
        return {
            "tool_name": tool_name,
            "category": "unknown",
            "reasoning": "",
            "error": str(e),
        }


async def classify_tools_from_graph(
    graph_path: str = GRAPH_PATH,
    tool_schema_path: str = TOOL_SCHEMA_V1_PATH,
    output_path: str = OUTPUT_CLASSIFICATION_PATH,
    batch_size: int = 10,
) -> Dict[str, Any]:
    """
    批量对所有有 output schema 的 tools 进行分类。
    
    Args:
        graph_path: graph JSON 文件路径（已弃用，不再使用）
        tool_schema_path: tool_response_schema_v1.json 路径（已弃用，不再使用）
        output_path: 输出分类结果的 JSON 文件路径
        batch_size: 批处理大小
        
    Returns:
        包含所有分类结果的字典
    """
    # 使用 load_tools_with_output_schema 加载有 output schema 的 tools
    schema_file = TOOL_SCHEMA_WITH_OUTPUT_PATH
    tools_with_output_schema, schema_data = load_tools_with_output_schema(schema_file)
    
    # 构建 tool_name -> schema_data 的映射，方便后续查找
    # 直接从原始文件读取以获取 key -> value 的映射
    tool_schema_map = {}
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_file_data = json.load(f)
        for tool_name, schema_item in schema_file_data.items():
            if schema_item.get('output_schema_parsed'):  # 只包含有 output schema 的
                tool_schema_map[tool_name] = schema_item
    
    # 直接处理所有有 output schema 的 tools
    tool_tasks: List[tuple] = []
    for tool_name in tools_with_output_schema:
        tool_meta = tool_schema_map.get(tool_name)
        if tool_meta:
            tool_tasks.append((tool_name, tool_meta))
    
    print(f"\nFound {len(tool_tasks)} tools to classify.")
    
    # 断点续传：检查是否已有部分结果
    all_results: Dict[str, Dict[str, Any]] = {}
    processed_tools = set()
    
    if os.path.exists(output_path):
        print(f"Found existing classification file: {output_path}")
        print("Loading previously processed results...")
        try:
            with open(output_path, "r", encoding="utf-8") as f:
                all_results = json.load(f)
            # 检查哪些工具已经成功处理（没有错误）
            for tool_name, result in all_results.items():
                error = result.get("error")
                # 如果结果中没有错误，则认为已处理
                if not error or error is None:
                    processed_tools.add(tool_name)
            print(f"Found {len(processed_tools)} already processed tools")
        except Exception as e:
            print(f"Warning: Failed to load existing results: {e}")
            print("Starting from scratch...")
            all_results = {}
            processed_tools = set()
    
    # 过滤掉已处理的工具
    remaining_tasks = [
        (tool_name, tool_meta)
        for tool_name, tool_meta in tool_tasks
        if tool_name not in processed_tools
    ]
    
    print(f"Remaining tools to process: {len(remaining_tasks)}")
    print(f"Processing in batches of {batch_size}...\n")
    
    total = len(tool_tasks)
    remaining_total = len(remaining_tasks)
    
    for batch_idx, start_idx in enumerate(range(0, remaining_total, batch_size)):
        batch = remaining_tasks[start_idx : start_idx + batch_size]
        batch_num = batch_idx + 1
        total_batches = (remaining_total + batch_size - 1) // batch_size
        print(f"Processing batch {batch_num}/{total_batches} (tools {start_idx + 1}-{start_idx + len(batch)}/{remaining_total}, total progress: {len(processed_tools) + start_idx + len(batch)}/{total})...")
        
        tasks = [classify_single_tool(tool_name, tool_meta) for tool_name, tool_meta in batch]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            tool_name = result["tool_name"]
            all_results[tool_name] = result
        
        # 实时保存（避免丢失进度）
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"  Progress saved (batch {batch_num}/{total_batches} completed)")
    
    # 统计信息
    category_counts = {}
    for result in all_results.values():
        cat = result.get("category", "unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print("\n" + "=" * 80)
    print("Classification Summary")
    print("=" * 80)
    if processed_tools:
        print(f"Previously processed: {len(processed_tools)}")
        print(f"Newly processed in this run: {remaining_total}")
    print(f"Total tools classified: {len(all_results)}")
    print("\nCategory distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    print("=" * 80)
    print(f"\nResults saved to: {output_path}")
    
    return all_results


async def generate_all_function_implementations(
    graph_path: str = GRAPH_PATH,
    tool_schema_path: str = TOOL_SCHEMA_V1_PATH,
    classification_path: str = OUTPUT_CLASSIFICATION_PATH,
    output_dir: str = None,
    batch_size: int = 5,
) -> Dict[str, Any]:
    """
    批量为所有有 output schema 的 tools 生成函数实现。
    
    Args:
        graph_path: graph JSON 文件路径（已弃用，不再使用）
        tool_schema_path: tool_response_schema_v1.json 路径（已弃用，不再使用）
        classification_path: tool_execution_type_classification.json 路径
        output_dir: 输出目录，如果为 None 则使用 tool_info 目录下的 generated_functions 子目录
        batch_size: 批处理大小
        
    Returns:
        包含所有生成结果的字典
    """
    if output_dir is None:
        output_dir = os.path.join(TOOL_INFO_DIR, "generated_functions_v1")
    os.makedirs(output_dir, exist_ok=True)
    
    # 改成从schema_file中得到有output schema的tools，复用load_tools_with_output_schema
    # 使用 load_tools_with_output_schema 加载有 output schema 的 tools
    schema_file = TOOL_SCHEMA_WITH_OUTPUT_PATH
    tools_with_output_schema, schema_data = load_tools_with_output_schema(schema_file)
    
    # 构建 tool_name -> schema_data 的映射，方便后续查找
    # 直接从原始文件读取以获取 key -> value 的映射
    tool_schema_map = {}
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_file_data = json.load(f)
        for tool_name, schema_item in schema_file_data.items():
            if schema_item.get('output_schema_parsed'):  # 只包含有 output schema 的
                tool_schema_map[tool_name] = schema_item
    
    print(f"Loading classifications from {classification_path}...")
    with open(classification_path, "r", encoding="utf-8") as f:
        classifications = json.load(f)
    
    # 直接处理所有有 output schema 的 tools
    tool_tasks: List[tuple] = []
    for tool_name in tools_with_output_schema:
        tool_meta = tool_schema_map.get(tool_name)
        classification = classifications.get(tool_name)
        if tool_meta:
            tool_tasks.append((tool_name, tool_meta, classification))
    
    print(f"\nFound {len(tool_tasks)} tools to generate implementations for.")
    
    # 断点续传：检查 output_dir 下已存在的文件
    processed_tools = set()
    if os.path.exists(output_dir):
        print(f"Checking existing files in {output_dir}...")
        existing_files = os.listdir(output_dir)
        # 构建文件名到 tool_name 的映射（反向）
        # 文件名格式：{safe_name}.py，其中 safe_name = tool_name.replace("/", "_").replace("\\", "_")
        for filename in existing_files:
            if filename.endswith('.py') and filename != '__init__.py':
                # 尝试从文件名反推出 tool_name
                # 注意：由于可能有多个 tool_name 映射到同一个 safe_name，我们需要检查所有可能的 tool_name
                safe_name = filename[:-3]  # 去掉 .py 后缀
                # 检查所有 tool_name，看哪个对应的 safe_name 匹配
                for tool_name, tool_meta, _ in tool_tasks:
                    expected_safe_name = tool_name.replace("/", "_").replace("\\", "_")
                    if expected_safe_name == safe_name:
                        processed_tools.add(tool_name)
                        break
        
        print(f"Found {len(processed_tools)} already processed tools (files exist)")
    
    # 过滤掉已处理的工具
    remaining_tasks = [
        (tool_name, tool_meta, classification)
        for tool_name, tool_meta, classification in tool_tasks
        if tool_name not in processed_tools
    ]
    
    print(f"Remaining tools to process: {len(remaining_tasks)}")
    print(f"Processing in batches of {batch_size}...\n")
    
    # 加载已有的 summary 文件（如果存在）
    summary_file = os.path.join(output_dir, "generation_summary.json")
    all_results: Dict[str, Dict[str, Any]] = {}
    if os.path.exists(summary_file):
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                all_results = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load existing summary: {e}")
    
    total = len(tool_tasks)
    remaining_total = len(remaining_tasks)
    
    for batch_idx, start_idx in enumerate(range(0, remaining_total, batch_size)):
        batch = remaining_tasks[start_idx : start_idx + batch_size]
        batch_num = batch_idx + 1
        total_batches = (remaining_total + batch_size - 1) // batch_size
        print(f"Processing batch {batch_num}/{total_batches} (tools {start_idx + 1}-{start_idx + len(batch)}/{remaining_total}, total progress: {len(processed_tools) + start_idx + len(batch)}/{total})...")
        
        tasks = [
            generate_function_implementation(tool_name, tool_meta, classification)
            for tool_name, tool_meta, classification in batch
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for (tool_name, tool_meta, classification), result in zip(batch, results):
            if isinstance(result, Exception):
                print(f"[ERROR] Failed to generate code for '{tool_name}': {result}")
                all_results[tool_name] = {
                    "tool_name": tool_name,
                    "error": str(result),
                    "code": None,
                }
            else:
                code, token_usage = result
                # 保存到单独的文件
                safe_name = tool_name.replace("/", "_").replace("\\", "_")
                code_file = os.path.join(output_dir, f"{safe_name}.py")
                with open(code_file, "w", encoding="utf-8") as f:
                    f.write(code)
                
                all_results[tool_name] = {
                    "tool_name": tool_name,
                    "category": classification.get("category", "unknown") if classification else "unknown",
                    "code_file": code_file,
                    "token_usage": token_usage,
                    "error": None,
                }
        
        # 每个批次完成后保存进度（增量保存）
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"  Progress saved (batch {batch_num}/{total_batches} completed)")
    
    # 统计信息
    category_counts = {}
    for result in all_results.values():
        cat = result.get("category", "unknown")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print("\n" + "=" * 80)
    print("Code Generation Summary")
    print("=" * 80)
    if processed_tools:
        print(f"Previously processed (files exist): {len(processed_tools)}")
        print(f"Newly processed in this run: {remaining_total}")
    print(f"Total tools processed: {len(all_results)}")
    successfully_generated = sum(
        1 for r in all_results.values() 
        if r.get('code_file') and (not r.get('error'))
    )
    print(f"Successfully generated: {successfully_generated}")
    print(f"Failed: {sum(1 for r in all_results.values() if r.get('error'))}")
    print("\nGenerated by category:")
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")
    print("=" * 80)
    print(f"\nCode files saved to: {output_dir}")
    print(f"Summary saved to: {summary_file}")
    
    return all_results


# 示例使用
if __name__ == "__main__":
    async def main():
        # 实现一个逻辑，断点续传，我的程序断了，处理到了一半左右，现在需要继续处理剩下的
        # 选项1: 对 graph 中的所有 tools 进行分类
        # results = await classify_tools_from_graph(
        #     graph_path=GRAPH_PATH,
        #     tool_schema_path=TOOL_SCHEMA_V1_PATH,
        #     output_path=OUTPUT_CLASSIFICATION_PATH,
        #     batch_size=10,
        # )
        # print(f"\nClassification completed. Results saved to {OUTPUT_CLASSIFICATION_PATH}")
        
        # 选项2: 为所有 tools 生成函数实现
        results = await generate_all_function_implementations(
            graph_path=GRAPH_PATH,
            tool_schema_path=TOOL_SCHEMA_V1_PATH,
            classification_path=OUTPUT_CLASSIFICATION_PATH,
            batch_size=10,
        )
        print(f"\nCode generation completed.")
    
    asyncio.run(main())

