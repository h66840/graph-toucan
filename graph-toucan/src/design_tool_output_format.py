"""
任务需求：

- 让大模型根据函数的 example（包括最近一轮的 user_query、assistant message、
  tool_call info、tool_response），来设计 tool response schema。
- 每个 example 里有一个字段 tool_response_is_structured，代表 tool_response
  是否是结构化形式：
  - 对于非结构化的 tool_response，让大模型解析出 key info，并抽象为字段；
  - 对于结构化的 tool_response（字段很多、嵌套很深），让大模型保留关键字段，扔掉细节。
- 最终的 tool response schema 设计为 Python Pydantic 模型格式。

本文件需要实现：
- 读取函数 schema（来自 tool_schema.json）
- 读取调用 example（来自 tool_output_examples.json）
- 为每个 tool 构造 prompt，并调用 OpenAI API（参考 contrust_graph.py 的用法），
  让大模型输出 Pydantic 模型代码；
- 将每个 tool 的 Pydantic schema 结果保存下来，方便后续使用。
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI
import re
from datetime import datetime


# 路径配置
ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
TOOL_INFO_DIR = os.path.join(ROOT_DIR, "tool_info")

# 从 tool_with_server.json 获取 function_schema
TOOL_WITH_SERVER_PATH = os.path.join(TOOL_INFO_DIR, "tool_with_server.json")
# 从 tool_output.json 获取 tool 列表和 examples
TOOL_OUTPUT_PATH = os.path.join(TOOL_INFO_DIR, "tool_output.json")
OUTPUT_JSON_PATH = os.path.join(TOOL_INFO_DIR, "tool_schema_with_outputformat.json")
LOG_PATH = os.path.join(TOOL_INFO_DIR, "12311436.log")


# 异步 OpenAI 客户端（参考 contrust_graph.py）
async_client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def append_log(message: str) -> None:
    """
    追加写入简单日志到 LOG_PATH。
    """
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {message}\n"
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        # 日志写入失败时不影响主流程
        pass


def load_tool_schemas_from_tool_with_server(tool_with_server_path: str) -> Dict[str, Dict[str, Any]]:
    """
    从 tool_with_server.json 加载 function_schema，构建 name -> function_schema 映射。
    """
    print(f"Loading tool schemas from {tool_with_server_path}...")
    with open(tool_with_server_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    name_to_schema: Dict[str, Dict[str, Any]] = {}
    for item in data:
        func_schema = item.get("function_schema", {})
        func = func_schema.get("function", {})
        if not isinstance(func, dict):
            continue
        name = func.get("name")
        if not isinstance(name, str) or not name:
            continue
        # 只保存 function_schema 部分
        name_to_schema[name] = func_schema

    print(f"Loaded {len(name_to_schema)} tool schemas.")
    return name_to_schema


def load_tool_output_data(path: str) -> Dict[str, Any]:
    """
    加载 tool_output.json，包含 tool 列表和 examples。
    """
    print(f"Loading tool output data from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Loaded tool_output.json")
    return data



def build_prompt_for_tool(
    tool_name: str,
    function_schema: Optional[Dict[str, Any]],
    examples: List[Dict[str, Any]],
) -> str:
    """
    构造 user prompt，让大模型根据 schema + examples 设计 Pydantic 响应模型。
    如果没有 example，让 LLM 基于 function_schema 合成合理的 output format。
    """
    schema_str = json.dumps(function_schema, indent=2, ensure_ascii=False) if function_schema else "N/A"

    # 如果没有 examples，使用基于 schema 的 prompt
    if not examples:
        prompt = f"""You are an AI assistant that helps design **output schemas** for tools.

Below is the definition of a tool. Since there are **no real usage examples available**, you need to **synthesize a reasonable output schema** based on the function's purpose and description.

Tool name: {tool_name}

Function schema (shows the function's PURPOSE and INPUT parameters - NOT the output):
{schema_str}

**CRITICAL RULES:**
1. **DO NOT copy or transform input parameters** - the output schema should describe what the function RETURNS, not what it takes as input
2. **Design NEW fields** that represent the function's result/response data
3. **Think about what information the function produces**, not what it receives
4. **Bad example**: If input has "query: str", output should NOT have "query" or "processed_query"
5. **Good example**: If input has "query: str", output might have "results: List[Dict]", "count: int", "metadata: Dict"

Your task:
1. Carefully analyze the function's **name** and **description** to understand what this tool does and what it RETURNS
2. **Ignore the input parameters** - they are NOT part of the output
3. Based on the function's purpose, **infer what information it would return as a result**
4. Design a **fully structured and comprehensive output schema** that captures the function's response:
   - **One semantic concept per field**: Each distinct type of information should map to a separate field
   - **Support nested structures**: Use nested objects (Dict[str, ...]) or arrays (List[...]) when there's natural hierarchy
   - **Be comprehensive**: Include all fields that would be useful for this type of operation
   - **Consider common patterns for different operation types**:
     * **Search/Query functions** → results list, total count, pagination info, metadata
     * **Get/Retrieve functions** → detailed information fields about the retrieved entity
     * **Create/Update functions** → created/updated object details, success status, timestamp
     * **Delete functions** → success status, confirmation message, deleted item ID
     * **List functions** → array of items, count, pagination, filters applied
     * **Analysis functions** → metrics, statistics, insights, summary data
     * **Check/Validation functions** → boolean result, validation details, error messages

Examples of correct inference:
- A "search_users" function → output: results: List[Dict], total_count: int, page: int, has_more: bool
  (NOT: query: str, filters: Dict ← these are INPUTS)
- A "get_weather" function → output: temperature: float, humidity: float, conditions: str, forecast: List[Dict]
  (NOT: city: str, date: str ← these are INPUTS)
- A "create_task" function → output: task_id: str, created_at: str, status: str, task_details: Dict
  (NOT: title: str, description: str ← these are INPUTS)


OUTPUT FORMAT
**output_schema**
field1_name: [type, brief description]
field2_name: [type, brief description]
...
(design as many fields as needed to fully capture the expected response)

For nested structures, use one of these patterns:
- For a list of items: field_name: [List[str], description] or [List[Dict], description if items have multiple attributes]
- For a nested object: field_name: [Dict, description] and explain what keys/structure it contains
- For a list of structured items: field_name: [List[Dict], description] and explain the dict structure

**brief_explain**
Explain your reasoning: what does this function do, and why does the output schema make sense for its RETURN VALUE (not its input)?
"""
        return prompt

    # 如果有 examples，使用现有的基于 examples 的 prompt
    # 只取前几条 example，防止 prompt 过长
    max_examples = 3
    used_examples = examples[:max_examples]

    examples_text_parts: List[str] = []
    for idx, ex in enumerate(used_examples):
        user_query = ex.get("user_query", "")
        assistant_message = ex.get("assistant_message", "")
        tool_call = ex.get("tool_call", {})
        tool_response = ex.get("tool_response", "")
        is_structured = ex.get("tool_response_is_structured")

        examples_text_parts.append(
            f"=== Example {idx + 1} ===\n"
            f"user_query:\n{user_query}\n\n"
            f"assistant_message:\n{assistant_message}\n\n"
            f"tool_call:\n{json.dumps(tool_call, indent=2, ensure_ascii=False)}\n\n"
            f"tool_response_is_structured: {is_structured}\n"
            f"tool_response:\n{tool_response}\n"
        )

    examples_block = "\n".join(examples_text_parts)

    prompt = f"""You are an AI assistant that helps design **output schemas** for tools.

Below is the definition of a tool, along with several real usage examples. Based on this information, design an **output schema** that describes the structure of this tool's response.

Tool name: {tool_name}

Function schema (shows the function's PURPOSE and INPUT parameters - for context only, NOT part of output):
{schema_str}

**CRITICAL RULES:**
1. **DO NOT copy or transform input parameters** - the output schema should describe what the function RETURNS (shown in `tool_response`), not what it takes as input (shown in `tool_call`)
2. **Design fields based on `tool_response` content** - only extract fields from what the tool actually returns
3. **Ignore input parameters** - they appear in `tool_call` but should NOT appear in output schema
4. **Bad example**: If `tool_call` has "query: str" parameter, output schema should NOT have "query" or "processed_query"
5. **Good example**: If `tool_response` contains search results, output schema should have fields like "results: List[Dict]", "total_count: int", etc.

Here are several real call examples. Each example contains:
- `user_query`: the user's latest natural language request
- `assistant_message`: the assistant's message before making the tool call
- `tool_call`: the actual tool name and arguments used (these are INPUTS - DO NOT copy them to output schema)
- `tool_response_is_structured`: whether this particular `tool_response` is structurally formatted (e.g., JSON / dict / list)
- `tool_response`: the actual content returned by the tool (this is what you should design the schema for)

Carefully read the `tool_response` content in these examples and abstract from them a concise and no lack for information response schema.

Examples:
{examples_block}

Your task:
1. For **unstructured** `tool_response` values (typically plain text), extract ALL key information and design reasonable fields. Each distinct piece of information should have its own field.
2. For already **structured** `tool_response` values (typically JSON strings or dict/list), preserve all meaningful information in the schema design.
3. Design a schema that is **fully structured and lossless** (足够结构化，并且信息无损):
   - **One semantic concept per field**: Each distinct type of information should map to a separate field
   - **Support nested structures**: Use nested objects (Dict[str, ...]) or arrays (List[...]) when there's natural hierarchy
   - **No artificial field limits**: Design as many fields as needed to capture all information without loss
   - **Balance granularity**: Keep fields at appropriate semantic level - not too fine-grained (atomic values everywhere) nor too coarse (everything lumped together)
   - **Examples**:
     * If response contains "status" and "message" - create two separate fields
     * If response contains a list of items with multiple attributes - use List[Dict] or a nested model
     * If response has hierarchical data (e.g., user info with address) - use nested structures
4. The schema should cover all realistic response variants of this tool while maintaining clarity.


OUTPUT FORMAT
**output_schema**
field1_name: [type, brief description]
field2_name: [type, brief description]
...
(design as many fields as needed, no limit)

For nested structures, use one of these patterns:
- For a list of items: field_name: [List[str], description] or [List[Dict], description if items have multiple attributes]
- For a nested object: field_name: [Dict, description] and explain what keys/structure it contains
- For a list of structured items: field_name: [List[Dict], description] and explain the dict structure

Examples:
- Simple list: tags: [List[str], list of tag strings]
- List of objects: items: [List[Dict], list of items, each with 'id', 'name', 'price' fields]
- Nested object: metadata: [Dict, contains 'created_at', 'author', 'version' fields]

**brief_explain**
give one brief explain.
...

"""
    return prompt


def parse_output_schema_text(text: str) -> Dict[str, Any]:
    """
    解析大模型按照 OUTPUT FORMAT 返回的文本。

    格式约定：
    **output_schema**
    field1_name: [type, brief description]
    field2_name: [type, brief description]

    **brief_explain**
    give one brief explain.
    ...
    """
    lines = [line.rstrip() for line in text.splitlines()]
    fields: List[Dict[str, str]] = []
    brief_explain: str = ""

    section = None  # None / "output_schema" / "brief_explain"
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped == "**output_schema**":
            section = "output_schema"
            continue
        if stripped == "**brief_explain**":
            section = "brief_explain"
            continue

        if section == "output_schema":
            # 期望形如：field_name: [type, brief description]
            # 先拆 field_name 与后面的部分
            if ":" not in stripped:
                continue
            field_name, rest = stripped.split(":", 1)
            field_name = field_name.strip()
            rest = rest.strip()

            # 去掉可能的方括号
            if rest.startswith("[") and rest.endswith("]"):
                inner = rest[1:-1].strip()
            else:
                inner = rest

            if not inner:
                field_type = ""
                desc = ""
            else:
                # 按第一个逗号切分 type 与 description
                type_part, _, desc_part = inner.partition(",")
                field_type = type_part.strip()
                desc = desc_part.strip()

            if field_name:
                fields.append(
                    {
                        "name": field_name,
                        "type": field_type,
                        "description": desc,
                    }
                )
        elif section == "brief_explain":
            # 取第一行非空、非省略号作为简要说明
            if stripped == "...":
                continue
            if not brief_explain:
                brief_explain = stripped

    return {
        "fields": fields,
        "brief_explain": brief_explain,
    }


async def _design_schema_for_single_tool_async(
    tool_name: str,
    function_schema: Optional[Dict[str, Any]],
    examples: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    调用大模型，为单个 tool 设计响应 schema（单个 tool）。
    因为给了function_schema，所以直接返回function_schema和output_schema，这样就有了输入和输出的格式了
    """

    
    user_prompt = build_prompt_for_tool(tool_name, function_schema, examples)

    try:
        completion = await async_client.chat.completions.create(
            model="qwen3-235b-a22b-instruct-2507",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert API designer. "
                        "You only output concise output schemas for tool responses, "
                        "strictly following the requested OUTPUT FORMAT."
                    ),
                },
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            temperature=0.2,
            max_completion_tokens=1024,
        )

        content = completion.choices[0].message.content
        parsed = parse_output_schema_text(content or "")
        result = {
            "tool_name": tool_name,
            "function_schema": function_schema,  # 输入格式（函数定义）
            "output_schema_raw": content,
            "output_schema_parsed": parsed,  # 输出格式
        }
        return result
    except Exception as e:
        err_msg = f"[ERROR] design schema for tool '{tool_name}' failed: {e}"
        print(err_msg)
        append_log(err_msg)
        return {
            "tool_name": tool_name,
            "error": str(e),
        }


async def design_schema_for_tool_async(
    batch_inputs: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    支持 batch 调用的封装：
    - 输入：每个元素包含 `tool_name`、`function_schema`、`examples`
    - 输出：与输入一一对应的结果列表
    """
    tasks = []
    for item in batch_inputs:
        tasks.append(
            _design_schema_for_single_tool_async(
                tool_name=item["tool_name"],
                function_schema=item.get("function_schema"),
                examples=item.get("examples") or [],
            )
        )

    results: List[Dict[str, Any]] = await asyncio.gather(*tasks)
    return results


async def run_all_tools() -> None:
    """
    主流程：对所有 tool 调用大模型生成 schema，并写入 JSON。
    - 只处理 tool_output.json 中的 tools
    - 对于有 examples 的 tools，基于 examples 生成 schema
    - 对于没有 examples 的 tools，基于 function_schema 合成 schema
    """
    # 从 tool_with_server.json 加载 function_schema（作为查找表）
    name_to_schema = load_tool_schemas_from_tool_with_server(TOOL_WITH_SERVER_PATH)

    # 从 tool_output.json 加载 tool 列表和 examples
    tool_output_data = load_tool_output_data(TOOL_OUTPUT_PATH)
    examples_by_tool: Dict[str, List[Dict[str, Any]]] = tool_output_data.get(
        "tool_examples", {}
    )

    # 只处理 tool_output.json 中的 tools
    all_tools_to_process: Dict[str, List[Dict[str, Any]]] = {}

    for tool_name, examples in examples_by_tool.items():
        # 只处理在 tool_with_server.json 中有 schema 的 tool
        if tool_name in name_to_schema:
            all_tools_to_process[tool_name] = examples  # examples 可能为空列表

    os.makedirs(os.path.dirname(OUTPUT_JSON_PATH), exist_ok=True)

    tools_with_examples = sum(1 for exs in all_tools_to_process.values() if exs)
    tools_without_examples_count = sum(1 for exs in all_tools_to_process.values() if not exs)

    print(f"\n" + "=" * 80)
    print(f"Tool Schema Design Summary")
    print("=" * 80)
    print(f"Data source: {TOOL_OUTPUT_PATH}")
    print(f"Total tools to process: {len(all_tools_to_process)}")
    print(f"  - Tools with examples: {tools_with_examples}")
    print(f"  - Tools without examples (schema-based): {tools_without_examples_count}")
    print(f"Output path: {OUTPUT_JSON_PATH}")
    print("=" * 80)

    # 按 batch 方式并发调用，控制并发规模；最终保存为一个 JSON 文件
    batch_size = 10
    items = list(all_tools_to_process.items())
    total = len(items)
    all_results: Dict[str, Any] = {}

    for start_idx in range(0, total, batch_size):
        batch_items = items[start_idx : start_idx + batch_size]
        has_examples_info = [
            f"{tool_name}({'with examples' if examples else 'schema-based'})"
            for tool_name, examples in batch_items
        ]
        print(
            f"\nProcessing batch {start_idx // batch_size + 1} "
            f"(tools {start_idx + 1}-{start_idx + len(batch_items)} of {total}):"
        )
        print(f"  {', '.join(has_examples_info)}")

        batch_inputs: List[Dict[str, Any]] = []
        for tool_name, examples in batch_items:
            func_schema = name_to_schema.get(tool_name)
            batch_inputs.append(
                {
                    "tool_name": tool_name,
                    "function_schema": func_schema,
                    "examples": examples,  # 可能是空 list
                }
            )

        batch_results = await design_schema_for_tool_async(batch_inputs)

        for result in batch_results:
            tname = result.get("tool_name")
            if isinstance(tname, str) and tname:
                # function_schema 已经在 _design_schema_for_single_tool_async 中返回
                # 只需要标记是否是基于 examples 还是 schema 生成的
                has_examples = tname in all_tools_to_process and bool(all_tools_to_process[tname])
                result["generation_type"] = "example-based" if has_examples else "schema-based"
                all_results[tname] = result
            else:
                # 兜底：如果没有合法的 tool_name，就用索引 key
                assert 0
                key = f"tool_{start_idx}"
                all_results[key] = result

    with open(OUTPUT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 80)
    print("All tools processed successfully!")
    print(f"Results saved to: {OUTPUT_JSON_PATH}")
    print("=" * 80)


def main():
    asyncio.run(run_all_tools())


if __name__ == "__main__":
    main()
