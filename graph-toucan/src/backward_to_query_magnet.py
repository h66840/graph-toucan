"""
MAGNET-style Back-and-Forth Translation
完全复刻 MAGNET 论文中的方法

主要特性:
1. 支持 FSP v2 格式 (List[List[int]])
2. 检测 turn 类型 (merged/insert_short/insert_long/split)
3. Turn 内顺序执行 + 参数传递
4. 维护完整历史输出 (支持长依赖)
5. 处理空 turn (Split 操作)
"""

import asyncio
import json
import os
import sys
import importlib.util
import ast
import re
import time
import yaml
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from tqdm import tqdm
from openai import AsyncOpenAI

# 导入 backward_to_query 中的工具函数和类
from backward_to_query import (
    execute_function_call as _execute_function_call_base,
    load_function_from_file as _load_function_from_file_base,
    build_function_documentation,
    format_tool_output,
)

# ==================== 路径配置 ====================

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOL_INFO_DIR = os.path.join(ROOT_DIR, "tool_info")
FSP_DIR = os.path.join(ROOT_DIR, "fsp_path")
TOOL_FUNCTION_DIR = os.path.join(TOOL_INFO_DIR, "tool_function")

# 输入输出路径
FSP_V2_PATH = os.path.join(ROOT_DIR, "walker_path", "fsp_v2.json")
TOOL_SCHEMA_SUMMARY_PATH = os.path.join(TOOL_INFO_DIR, "tool_schema_with_outputformat.json")
OUTPUT_PATH = os.path.join(FSP_DIR, "fsp_v2_queries.jsonl")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")


# ==================== 配置加载 ====================
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


# ==================== 数据加载 ====================

def load_fsp_v2(path: str = FSP_V2_PATH) -> List[Dict[str, Any]]:
    """
    加载 FSP v2 数据

    Returns:
        List of path dicts, each containing:
        - node_idx: int  # 节点索引
        - path_idx: int  # 路径索引
        - fsp_final: List[List[int]]  # FSP 格式
        - fsp_final_names: List[List[str]]  # 函数名
        - merge_logs: List[Dict]
        - insert_logs: List[Dict]
        - split_logs: List[Dict]
        - statistics: Dict
    """
    print(f"Loading FSP v2 from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # FSP v2 结构: {"node_results": {"0": {"paths": [...]}, "1": {...}, ...}}
    node_results = data.get("node_results", {})

    all_paths = []
    for node_idx_str, node_data in node_results.items():
        node_idx = int(node_idx_str)
        paths = node_data.get("paths", [])

        # 为每个 path 添加 node_idx
        for path in paths:
            path["node_idx"] = node_idx
            all_paths.append(path)

    print(f"Loaded {len(all_paths)} FSP v2 paths from {len(node_results)} nodes")
    return all_paths


def load_tool_schemas(path: str = TOOL_SCHEMA_SUMMARY_PATH) -> Dict[str, Dict[str, Any]]:
    """加载 tool schemas"""
    print(f"Loading tool schemas from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} tools from schema summary.")
    return data


def get_function_output_info(func_name: str, tool_schemas: Dict) -> str:
    """
    获取函数的输出 schema 信息，展示所有字段

    Args:
        func_name: 函数名称
        tool_schemas: 工具 schema 字典

    Returns:
        格式化的输出 schema 字符串，每个字段一行
        例如:
          distance (float) - Distance value
          unit (string) - Always in miles
    """
    tool_meta = tool_schemas.get(func_name, {})
    output_schema = tool_meta.get('output_schema_parsed', {})

    if not output_schema or not output_schema.get('fields'):
        return "  output (unknown type)"

    fields = output_schema['fields']
    lines = []

    # 展示所有字段
    for field in fields:
        name = field.get('name', 'result')
        ftype = field.get('type', 'unknown')
        desc = field.get('description', '')

        if desc:
            lines.append(f"  {name} ({ftype}) - {desc}")
        else:
            lines.append(f"  {name} ({ftype})")

    return "\n".join(lines)


# ==================== 函数加载和执行 (复用现有代码) ====================

def load_function_from_file(func_name: str) -> Tuple[Any, Optional[Dict[str, Any]], Optional[str], Any]:
    """
    从文件加载函数 (委托给 backward_to_query 的实现)

    Returns:
        tuple: (函数对象, call_external_api信息, source_without_api, module)

    Raises:
        RuntimeError: 如果函数文件不存在或加载失败
    """
    return _load_function_from_file_base(func_name)


async def execute_function_call(
    func_name: str,
    parameters: Dict[str, Any],
    tool_schemas: Dict[str, Dict],
) -> Dict[str, Any]:
    """
    执行单个函数调用 (委托给 backward_to_query 的实现)

    Args:
        func_name: 函数名称
        parameters: 函数参数字典
        tool_schemas: 工具 schema (为了兼容性保留，但不使用)

    Returns:
        dict: 包含以下字段的字典
            - function: str, 函数名称
            - parameters: Dict, 函数参数
            - output: Any, 函数输出
            - token_usage: Dict, token 使用情况
    """
    # 调用 backward_to_query 的实现（不需要 tool_schemas 参数）
    result = await _execute_function_call_base(func_name, parameters)

    # backward_to_query 的版本返回格式略有不同，需要适配
    # 它返回的是直接的输出字典，而不是包含 function/parameters 的结构
    if result is None:
        raise RuntimeError(f"Function execution returned None: {func_name}")

    # 如果结果已经包�� function 和 parameters，直接返回
    if "function" in result and "parameters" in result:
        return result

    # 否则，包装成期望的格式
    # backward_to_query 的 execute_function_call 返回的结果已经包含 token_usage
    return {
        "function": func_name,
        "parameters": parameters,
        "output": result if not isinstance(result, dict) or "token_usage" not in result else {k: v for k, v in result.items() if k != "token_usage"},
        "token_usage": result.get("token_usage", {}) if isinstance(result, dict) else {},
    }


# ==================== Turn 类型检测 ====================

def detect_turn_operations(
    turn_idx: int,
    turn_functions: List[str],
    path_data: Dict[str, Any],
) -> Dict[str, Any]:
    """
    检测 turn 应用了哪些操作 (一个 turn 可能同时经历多个操作)

    Returns:
        {
            "is_empty": bool,
            "operations": List[str],  # 所有应用的操作列表
            "primary_style": str,  # 主要类型（用于选择 prompt 模板）
            "merge_info": Dict or None,
            "insert_info": List[Dict],  # 可能有多个 insert
        }
    """
    result = {
        "is_empty": False,
        "operations": [],
        "primary_style": "normal",
        "merge_info": None,
        "insert_info": [],
    }

    # 检查是否是空 turn
    if not turn_functions:
        result["is_empty"] = True
        result["primary_style"] = "empty"
        result["operations"].append("split")
        return result

    # 检查 merge (基于函数名匹配，不依赖可能过期的 turn_idx)
    # 修复：split 操作后 turn_idx 可能失效，改为基于函数名匹配
    merge_logs = path_data.get("merge_logs", [])
    for log in merge_logs:
        merged_names = log.get("merged_names", [])
        # 检查 merged_names 中的所有函数是否都在当前 turn
        if merged_names and all(name in turn_functions for name in merged_names):
            result["operations"].append("merge")
            result["merge_info"] = log
            break

    # 检查 insert (基于函数名匹配，不依赖可能过期的 turn_idx)
    # 修复：split 操作后 turn_idx 可能失效，改为基于函数名匹配
    insert_logs = path_data.get("insert_logs", [])
    for log in insert_logs:
        source_func = log.get("source_func_name")
        nested_func = log.get("nested_func_name")
        insert_type = log.get("insert_type")

        # 根据 insert_type 判断如何匹配
        if insert_type == "short_dependency":
            # Short dependency: 两个函数都必须在当前 turn
            if source_func in turn_functions and nested_func in turn_functions:
                result["insert_info"].append(log)
                result["operations"].append("insert_short")

        elif insert_type == "long_dependency":
            # Long dependency: 只有 nested_func 在当前 turn
            # source_func 在之前的某个 turn（通过 source_turn_idx 记录）
            if nested_func in turn_functions:
                result["insert_info"].append(log)
                result["operations"].append("insert_long")

    # 确定主要类型
    has_merge = "merge" in result["operations"]
    has_insert_short = "insert_short" in result["operations"]
    has_insert_long = "insert_long" in result["operations"]

    # 优先级: merge+insert > merge > insert_mixed > insert_long > insert_short > normal
    if has_merge and (has_insert_short or has_insert_long):
        result["primary_style"] = "merged_with_insert"
    elif has_merge:
        result["primary_style"] = "merged"
    elif has_insert_short and has_insert_long:
        # 新增：同时有 short 和 long dependency
        result["primary_style"] = "insert_mixed"
    elif has_insert_long:
        result["primary_style"] = "insert_long"
    elif has_insert_short:
        result["primary_style"] = "insert_short"
    else:
        result["primary_style"] = "normal"

    return result


# ==================== 风格指导 ====================

STYLE_INSTRUCTIONS = {
    "insert_short": """
**IMPORTANT - Query Style for Nested Functions (Short Dependency)**:

Characteristics:
- User has a SINGLE, CLEAR GOAL
- Intermediate/helper functions are IMPLICIT and automatic
- Query only mentions the FINAL outcome the user wants
- All functions execute in the SAME turn

Examples:
✓ "Get kilometers from San Francisco to San Mateo"
   (NOT "Get miles and convert to kilometers")

✓ "Book a business class flight from LA to NYC"
   (NOT "Check flight cost and book")

✓ "Get customer records in table format"
   (NOT "Query database and format to table")

Rules:
- Focus on the end result
- Don't mention intermediate steps
- Keep it natural and concise
- Assume helper functions are automatic
""",

    "insert_long": """
**IMPORTANT - Query Style for Long Dependency (Cross-Turn Reference)**:

Characteristics:
- User references PREVIOUS results from earlier turns
- Uses PRONOUNS and INDIRECT REFERENCES
- Does NOT repeat specific values or IDs
- The referenced output is from a DIFFERENT turn (not current)

Referencing Patterns:
- "that <noun>" → "that distance", "that booking"
- "the previous <noun>" → "the previous search"
- "my <noun>" → "my trip", "my reservation"
- "those <noun>" → "those results", "those records"

Examples:
✓ "Using that distance, find cities within that range"
   (NOT "Using 25.4km, find cities within 25.4km")

✓ "Cancel my New York trip"
   (NOT "Cancel booking 3426812")

✓ "Export those customer records to PDF"
   (NOT "Export the 150 records to PDF")

Rules:
- Reference history naturally
- Use context-aware language
- Assume the model remembers previous outputs
- Don't repeat specific values
- Make it sound like a natural conversation continuation
""",

    "merged": """
**IMPORTANT - Query Style for Merged Functions (Short Dependency with Explicit Intents)**:

Characteristics:
- Multiple functions in the SAME TURN
- SHORT DEPENDENCY: Output of one function → Input of the next (within same turn)
- User EXPLICITLY mentions BOTH actions/intents
- Unlike insert_short: User states both steps, not just final goal

Data Flow Pattern:
Function A (explicit) → output → Function B (explicit, uses A's output)

Examples:
✓ "Find the distance from SF to SM and set up navigation"
   → distance output feeds into navigation
   → User mentions BOTH: find distance AND navigate

✓ "Search for flights to NYC and send results to my friend"
   → search results feed into email content
   → User mentions BOTH: search AND send

Contrast with Insert Short:
❌ Insert Short: "Navigate to San Mateo" (only mentions navigation, distance is implicit)
✓ Merged: "Find the distance and set up navigation" (mentions both steps)

Rules:
- Explicitly mention ALL steps in the dependency chain
- Use connecting words: "and", "then", "after that"
- Show the data flow clearly in the query
- Both functions should be reflected in the query
""",

    "merged_with_insert": """
**IMPORTANT - Query Style for Merged with Insert (Mixed Function Types)**:

Characteristics:
- **THREE types of functions** (not just two):
  1. MERGED functions: Explicit intents that should be clearly stated
  2. LONG-DEPENDENCY inserts: Explicit, but reference history with pronouns
  3. SHORT-DEPENDENCY inserts: Implicit helpers that should NOT be mentioned

Function Roles:
- **Merged (explicit)**: Direct user intents, state them clearly
- **Long-dep insert (explicit with pronouns)**: Reference previous outputs using "that", "those", "my"
- **Short-dep insert (implicit)**: Helper/utility functions working in background

Examples:
✓ "Get weather forecast for Shanghai and check that distance"
   → "weather forecast" is merged (explicit)
   → "that distance" is long-dep insert (explicit, pronoun reference)
   → coordinate conversion might be short-dep insert (implicit, not mentioned)

✓ "Book flights to Beijing and cancel my previous reservation"
   → "book flights" is merged (explicit)
   → "my previous reservation" is long-dep insert (explicit, pronoun reference)
   → price calculation might be short-dep insert (implicit, not mentioned)

Contrast:
❌ "Get weather and also get live temperature and convert units"
   → Mentions short-dep helpers (should be implicit)

❌ "Check the distance of 25.4km from Turn 1"
   → Repeats specific value (should use pronoun)

Rules:
- Mention merged functions explicitly
- Reference long-dep inserts with pronouns (no specific values)
- Keep short-dep helpers completely implicit
- Use connecting words for merged functions: "and", "then"
- Natural combination of explicit intents and historical references
""",

    "insert_mixed": """
**IMPORTANT - Query Style for Mixed Dependencies (Short + Long)**:

Characteristics:
- Some functions are SHORT dependency (same-turn nested, implicit)
- Some functions are LONG dependency (cross-turn reference, pronouns)
- User has ONE main goal BUT references history

Combined Rules:
- Short dependency functions → Keep IMPLICIT (don't mention)
- Long dependency functions → Use PRONOUNS to reference history
- Focus on the main goal while naturally referencing previous results

Example:
✓ "Using that distance, calculate the area in square meters"
   → "that distance" references history (long dependency)
   → "calculate area" is the main goal
   → unit conversion to square meters is implicit (short dependency)

Rules:
- Combine implicit style with historical references
- Use pronouns for history: "that", "my", "those"
- Don't mention utility/helper functions
- Make it sound like a natural continuation with a new goal
""",

    "normal": """
**Query Style**:
- Generate a natural query for the given function(s)
- Provide all necessary parameter information
- Keep the query concise and user-friendly
""",
}


def get_style_instruction(primary_style: str) -> str:
    """获取风格指导语句"""
    return STYLE_INSTRUCTIONS.get(primary_style, STYLE_INSTRUCTIONS["normal"])


# ==================== Examples 库 ====================

EXAMPLES = {
    # Short Dependency: 同turn内的嵌套函数（隐式风格）
    "short_dependency": [
        {
            "name": "Unit Conversion",
            "functions": ["get_distance(from, to)", "convert_unit(value, from_unit, to_unit)"],
            "query": "How many kilometers from San Francisco to San Mateo?",
            "explanation": "User only mentions the final goal (kilometers). The miles→km conversion is implicit and automatic.",
            "anti_example": "Get the distance in miles and convert it to kilometers",
        },
        {
            "name": "Price Check before Booking",
            "functions": ["get_flight_cost(from, to, class)", "book_flight(from, to, class)"],
            "query": "Book a business class flight from LA to NYC on April 15th",
            "explanation": "User wants to book. Price check is an automatic prerequisite, not explicitly mentioned.",
            "anti_example": "Check flight prices and then book the flight",
        },
        {
            "name": "Data Formatting",
            "functions": ["query_database(table)", "format_json_to_table(data)"],
            "query": "Get customer records in a readable table format",
            "explanation": "User wants formatted output. JSON→table conversion is implicit.",
            "anti_example": "Query the database and format the results as a table",
        },
        {
            "name": "Temperature Unit Conversion",
            "functions": ["get_current_temperature(city)", "fahrenheit_to_celsius(temp)"],
            "query": "What's the temperature in New York in Celsius?",
            "explanation": "User only states the desired unit. Conversion is automatic.",
            "anti_example": "Get temperature and convert from Fahrenheit to Celsius",
        },
        {
            "name": "Currency Exchange",
            "functions": ["get_product_price(product_id)", "convert_currency(amount, from, to)"],
            "query": "How much does product #12345 cost in Euros?",
            "explanation": "User focuses on the final price in Euros. Currency conversion is implicit.",
            "anti_example": "Get the price and convert it to Euros",
        },
    ],

    # Long Dependency: 跨turn引用历史（使用代词和引用）
    "long_dependency": [
        {
            "name": "Distance → Range Search",
            "history": "Turn 0: Get distance from SF to San Mateo (25.4 km)",
            "functions": ["find_cities_in_range(center, radius)"],
            "query": "Using that distance, find all cities within that range from San Francisco",
            "explanation": "References Turn 0's distance (25.4km) using 'that distance' instead of repeating the value.",
            "anti_example": "Find cities within 25.4 kilometers from San Francisco",
            "key_reference": "that distance",
        },
        {
            "name": "Booking → Cancellation",
            "history": "Turn 0: Book NYC flight (booking #3426812)\nTurn 1: Message friend\nTurn 2: Book hotel",
            "functions": ["cancel_booking(booking_id)"],
            "query": "Cancel my New York trip due to unforeseen circumstances",
            "explanation": "References Turn 0's booking using 'my New York trip', not the booking ID.",
            "anti_example": "Cancel booking 3426812",
            "key_reference": "my New York trip",
        },
        {
            "name": "Query → Export",
            "history": "Turn 0: Get customer records (150 results)\nTurn 1: Analyze patterns",
            "functions": ["export_to_pdf(data)"],
            "query": "Export those customer records to a PDF report",
            "explanation": "Uses 'those records' to reference Turn 0's data without repeating details.",
            "anti_example": "Export the 150 customer records to PDF",
            "key_reference": "those customer records",
        },
        {
            "name": "Calculation → Visualization",
            "history": "Turn 0: Calculate quarterly revenue (Q1: $2.5M, Q2: $3.1M, Q3: $2.8M, Q4: $3.4M)",
            "functions": ["create_bar_chart(data)"],
            "query": "Create a bar chart showing those quarterly figures",
            "explanation": "References previous calculation using 'those figures' instead of repeating all numbers.",
            "anti_example": "Create a bar chart with Q1: $2.5M, Q2: $3.1M, Q3: $2.8M, Q4: $3.4M",
            "key_reference": "those quarterly figures",
        },
        {
            "name": "Search → Filter",
            "history": "Turn 0: Search all available hotels in Paris (50 results)\nTurn 1: Check weather forecast",
            "functions": ["filter_by_rating(items, min_rating)"],
            "query": "Filter those hotels to only show 4-star and above",
            "explanation": "References the previous search results using 'those hotels' without repeating the search.",
            "anti_example": "Filter the 50 Paris hotel results by rating",
            "key_reference": "those hotels",
        },
    ],

    # Sequential (Merged): 多意图并列 + 短依赖（显式风格）
    "sequential": [
        {
            "name": "Distance and Navigation",
            "functions": ["get_distance(from, to)", "set_navigation(destination)"],
            "query": "Find the distance from SF to San Mateo and set up navigation",
            "explanation": "SHORT DEPENDENCY: distance output → navigation input. User EXPLICITLY mentions both steps (find distance AND navigate), unlike insert_short where only final goal is mentioned.",
            "data_flow": "get_distance output → set_navigation parameter",
        },
        {
            "name": "Search and Share",
            "functions": ["search_flights(from, to, date)", "send_email(content, to)"],
            "query": "Search flights to NYC for April 15th and send the results to my friend",
            "explanation": "SHORT DEPENDENCY: search results → email content. User explicitly wants both: search AND send (not just 'notify my friend' which would be implicit).",
            "data_flow": "search_flights results → send_email content",
        },
        {
            "name": "Book and Insure",
            "functions": ["book_hotel(location, date)", "purchase_insurance(booking_id)"],
            "query": "Book a hotel in Paris for next week and get travel insurance",
            "explanation": "SHORT DEPENDENCY: booking_id → insurance parameter. Both actions explicitly stated (book AND insure).",
            "data_flow": "book_hotel booking_id → purchase_insurance parameter",
        },
        {
            "name": "Query and Summarize",
            "functions": ["get_database_records(table)", "summarize_data(data)"],
            "query": "Get all sales records from last quarter and provide a summary",
            "explanation": "SHORT DEPENDENCY: database records → summary input. User wants both data retrieval AND summary, not just summary (which would make retrieval implicit).",
            "data_flow": "get_database_records data → summarize_data parameter",
        },
        {
            "name": "Translate and Send",
            "functions": ["translate_text(text, to_lang)", "send_message(message, recipient)"],
            "query": "Translate this message to Spanish and send it to Maria",
            "explanation": "SHORT DEPENDENCY: translated text → message content. Two explicit steps: translate AND send (not just 'send to Maria in Spanish' which would make translation implicit).",
            "data_flow": "translate_text output → send_message message",
        },
    ],

    # Merged with Insert: 合并 + 插入混合（三种函数类型）
    "merged_with_insert": [
        {
            "name": "Weather Forecast and Distance Check",
            "history": "Turn 0: Get distance from SF to SM (25.4 km)",
            "functions": ["get_weather_forecast(city)", "cities_by_range(center, radius)", "get_live_temp(lat, lon)"],
            "merged_funcs": ["get_weather_forecast"],
            "long_dep_funcs": ["cities_by_range"],  # references Turn 0's distance
            "short_dep_funcs": ["get_live_temp"],   # implicit temperature helper
            "query": "Get weather forecast for Shanghai and find cities within that distance",
            "explanation": "MERGED: 'get weather forecast' is explicit. LONG-DEP: 'that distance' references Turn 0's output (25.4km) with pronoun. SHORT-DEP: get_live_temp works implicitly to provide temperature data.",
            "anti_example": "Get weather forecast and also get live temperature and find cities within 25.4km",
        },
        {
            "name": "Flight Booking and Previous Cancellation",
            "history": "Turn 0: Book NYC flight (booking #3426812)\nTurn 1: Message friend",
            "functions": ["book_flight(from, to, date)", "cancel_booking(booking_id)", "calculate_refund(booking_id)"],
            "merged_funcs": ["book_flight"],
            "long_dep_funcs": ["cancel_booking"],    # references Turn 0's booking
            "short_dep_funcs": ["calculate_refund"], # implicit refund calculation
            "query": "Book a flight to Boston for next week and cancel my previous New York trip",
            "explanation": "MERGED: 'book a flight' is explicit. LONG-DEP: 'my previous New York trip' references Turn 0's booking with pronoun. SHORT-DEP: calculate_refund works implicitly.",
            "anti_example": "Book flight and cancel booking 3426812 and calculate the refund amount",
        },
        {
            "name": "Search Hotels and Export Previous Data",
            "history": "Turn 0: Get customer records (150 results)\nTurn 1: Analyze patterns",
            "functions": ["search_hotels(location, date)", "export_to_pdf(data)", "format_report(content)"],
            "merged_funcs": ["search_hotels"],
            "long_dep_funcs": ["export_to_pdf"],  # references Turn 0's records
            "short_dep_funcs": ["format_report"], # implicit formatting
            "query": "Search hotels in Paris for May and export those customer records to PDF",
            "explanation": "MERGED: 'search hotels' is explicit. LONG-DEP: 'those customer records' references Turn 0's data. SHORT-DEP: format_report for PDF formatting is implicit.",
            "anti_example": "Search hotels and export the 150 records and format the report",
        },
    ],

    # Insert Mixed: 混合插入（long + short dependency）
    "insert_mixed": [
        {
            "name": "Area Calculation with Historical Distance",
            "history": "Turn 0: Get distance from SF to SM (25.4 km)",
            "functions": ["calculate_area(length, width)", "convert_to_square_meters(value)"],
            "primary_funcs": ["calculate_area"],
            "long_dep_context": "uses 'that distance' from Turn 0 as length parameter",
            "short_dep_funcs": ["convert_to_square_meters"],
            "query": "Using that distance, calculate the area in square meters",
            "explanation": "PRIMARY: calculate_area is the main goal. LONG-DEP: 'that distance' references Turn 0's 25.4km. SHORT-DEP: conversion to square meters is implicit.",
            "anti_example": "Using 25.4km, calculate area and convert to square meters",
        },
        {
            "name": "Restaurant Search with Previous Budget",
            "history": "Turn 0: Calculate travel budget ($500)\nTurn 1: Book transportation",
            "functions": ["search_restaurants(location, price_range)", "convert_currency(amount, to)"],
            "primary_funcs": ["search_restaurants"],
            "long_dep_context": "uses 'that budget' from Turn 0 as price_range",
            "short_dep_funcs": ["convert_currency"],
            "query": "Find restaurants near downtown within that budget in Euros",
            "explanation": "PRIMARY: search_restaurants is the main intent. LONG-DEP: 'that budget' references Turn 0's $500. SHORT-DEP: currency conversion to Euros is implicit.",
            "anti_example": "Find restaurants within $500 and convert to Euros",
        },
        {
            "name": "Route Planning with Historical Coordinates",
            "history": "Turn 0: Find hotel location (lat: 37.7749, lon: -122.4194)\nTurn 1: Check weather",
            "functions": ["plan_route(start, end)", "get_distance_in_km(coords1, coords2)"],
            "primary_funcs": ["plan_route"],
            "long_dep_context": "uses 'those coordinates' from Turn 0 as destination",
            "short_dep_funcs": ["get_distance_in_km"],
            "query": "Plan a route to those coordinates",
            "explanation": "PRIMARY: plan_route is the goal. LONG-DEP: 'those coordinates' references Turn 0's location. SHORT-DEP: distance calculation in km is implicit.",
            "anti_example": "Plan route to lat 37.7749, lon -122.4194 and calculate distance in km",
        },
        {
            "name": "Visualization with Previous Query Results",
            "history": "Turn 0: Calculate quarterly revenue (Q1: $2.5M, Q2: $3.1M, Q3: $2.8M, Q4: $3.4M)",
            "functions": ["create_bar_chart(data)", "format_to_percentage(values)"],
            "primary_funcs": ["create_bar_chart"],
            "long_dep_context": "uses 'those quarterly figures' from Turn 0",
            "short_dep_funcs": ["format_to_percentage"],
            "query": "Create a bar chart showing those quarterly figures as percentages",
            "explanation": "PRIMARY: create_bar_chart is the main action. LONG-DEP: 'those quarterly figures' references Turn 0's revenue data. SHORT-DEP: percentage formatting is implicit.",
            "anti_example": "Create chart with Q1 $2.5M, Q2 $3.1M, Q3 $2.8M, Q4 $3.4M and format as percentage",
        },
    ],
}


def select_examples(primary_style: str, num_examples: int = 2) -> List[Dict]:
    """
    根据 primary_style 选择合适的 examples

    Args:
        primary_style: Turn 的主要风格
        num_examples: 每种类型选择的例子数量

    Returns:
        选中的 examples 列表
    """
    import random

    if primary_style == "insert_short":
        # 选择 short dependency examples
        examples = random.sample(EXAMPLES["short_dependency"],
                                min(num_examples, len(EXAMPLES["short_dependency"])))

    elif primary_style == "insert_long":
        # 选择 long dependency examples
        examples = random.sample(EXAMPLES["long_dependency"],
                                min(num_examples, len(EXAMPLES["long_dependency"])))

    elif primary_style == "merged":
        # 选择 sequential examples
        examples = random.sample(EXAMPLES["sequential"],
                                min(num_examples, len(EXAMPLES["sequential"])))

    elif primary_style == "merged_with_insert":
        # 使用专门的 merged_with_insert examples
        examples = random.sample(EXAMPLES["merged_with_insert"],
                                min(num_examples, len(EXAMPLES["merged_with_insert"])))

    elif primary_style == "insert_mixed":
        # 使用专门的 insert_mixed examples
        examples = random.sample(EXAMPLES["insert_mixed"],
                                min(num_examples, len(EXAMPLES["insert_mixed"])))

    else:  # normal, empty
        examples = []

    return examples


def format_examples_for_prompt(examples: List[Dict]) -> str:
    """
    格式化 examples 为 prompt 文本

    Args:
        examples: 例子列表

    Returns:
        格式化后的 prompt 文本
    """
    if not examples:
        return ""

    formatted_parts = []

    for i, ex in enumerate(examples, 1):
        # 检查是否是 merged_with_insert example
        if "merged_funcs" in ex and "long_dep_funcs" in ex and "short_dep_funcs" in ex:
            formatted = f"""
Example {i}: {ex['name']} (Merged + Insert Mix)

Previous Context:
{ex['history']}

Functions:
- MERGED (explicit): {', '.join(ex['merged_funcs'])}
- LONG-DEP (explicit, pronoun): {', '.join(ex['long_dep_funcs'])}
- SHORT-DEP (implicit): {', '.join(ex['short_dep_funcs'])}

User Query: "{ex['query']}"

Why this works: {ex['explanation']}

❌ Bad Example: "{ex['anti_example']}"
"""
        # 检查是否是 insert_mixed example
        elif "primary_funcs" in ex and "long_dep_context" in ex and "short_dep_funcs" in ex:
            formatted = f"""
Example {i}: {ex['name']} (Mixed Dependencies)

Previous Context:
{ex['history']}

Functions:
- PRIMARY (explicit): {', '.join(ex['primary_funcs'])}
- LONG-DEP context: {ex['long_dep_context']}
- SHORT-DEP helpers (implicit): {', '.join(ex['short_dep_funcs'])}

User Query: "{ex['query']}"

Why this works: {ex['explanation']}

❌ Bad Example: "{ex['anti_example']}"
"""
        # 检查是否是普通的 long dependency example（有历史上下文）
        elif "history" in ex and "key_reference" in ex:
            formatted = f"""
Example {i}: {ex['name']} (References Previous Turn)

Previous Context:
{ex['history']}

Current Turn Functions: {', '.join(ex['functions'])}
User Query: "{ex['query']}"

Why this works: {ex['explanation']}
Key Reference: "{ex['key_reference']}"

❌ Bad Example: "{ex['anti_example']}"
"""
        else:
            # 普通 example（short dependency 或 sequential）
            anti_part = f"\n❌ Bad Example: \"{ex['anti_example']}\"" if "anti_example" in ex else ""
            data_flow_part = f"\nData Flow: {ex['data_flow']}" if "data_flow" in ex else ""

            formatted = f"""
Example {i}: {ex['name']}

Functions: {', '.join(ex['functions'])}
User Query: "{ex['query']}"

Why this works: {ex['explanation']}{data_flow_part}{anti_part}
"""

        formatted_parts.append(formatted)

    return "\n".join(formatted_parts)


# ==================== Prompt 构建 ====================

def build_prompt_for_turn(
    turn_idx: int,
    turn_type: str,
    turn_functions: List[str],
    all_turn_outputs: List[List[Dict]],  # 完整历史
    tool_schemas: Dict[str, Dict],
    turn_operations: Optional[Dict[str, Any]] = None,
    error_feedback: Optional[str] = None,
) -> str:
    """
    根据 turn 类型构建不同的 prompt

    Args:
        turn_idx: 当前 turn 索引
        turn_type: turn 类型 (normal/merged/insert_short/insert_long/empty)
        turn_functions: 当前 turn 的函数列表
        all_turn_outputs: [[turn0_outputs], [turn1_outputs], ...]
        tool_schemas: 工具 schema
        turn_operations: turn 操作信息 (包含 merge_info, insert_info 等)
        error_feedback: 错误反馈 (用于重试)
    """
    is_first_turn = turn_idx == 0

    # 构建历史信息
    history_block = ""
    if not is_first_turn and turn_idx > 0:
        history_parts = []
        for h_idx in range(turn_idx):
            h_outputs = all_turn_outputs[h_idx]
            if h_outputs:
                output_strs = []
                for out in h_outputs:
                    func = out.get("function", "unknown")
                    output = out.get("output", {})
                    output_strs.append(f"  {func}: {format_tool_output(output)}")
                history_parts.append(f"Turn {h_idx}:\n" + "\n".join(output_strs))

        if history_parts:
            history_block = f"""
[Previous Turns History]
{chr(10).join(history_parts)}
"""

    # 构建上一轮输出
    last_round_block = ""
    if not is_first_turn and turn_idx > 0:
        last_outputs = all_turn_outputs[turn_idx - 1]
        if last_outputs:
            output_strs = []
            for out in last_outputs:
                func = out.get("function", "unknown")
                output = out.get("output", {})
                output_strs.append(f"{func}: {format_tool_output(output)}")
            last_round_block = f"""
[Last Turn Outputs]
{chr(10).join(output_strs)}
"""

    # 构建候选函数文档
    candidate_docs = []
    for func_name in turn_functions:
        meta = tool_schemas.get(func_name, {})
        candidate_docs.append(build_function_documentation(func_name, meta))
    candidate_block = "\n\n".join(candidate_docs)

    # 错误反馈块
    error_feedback_block = ""
    if error_feedback:
        error_feedback_block = f"""
[PREVIOUS ATTEMPT FAILED]
Your previous query attempt resulted in an error:
{error_feedback}

Please revise your query to fix this issue.
"""

    # 获取风格指导
    style_instruction = get_style_instruction(turn_type)

    # 选择并格式化 examples
    examples = select_examples(turn_type, num_examples=2)
    examples_block = format_examples_for_prompt(examples)
    if examples_block:
        examples_block = f"\n{examples_block}\n"

    # 根据 turn 类型构建特定的 prompt
    if turn_type == "empty":
        # Split 操作：空 turn
        prompt = f"""You are role-playing as a user in a multi-turn conversation with a function-calling agent.

This is Turn {turn_idx}. The user will make a request, but there is NO suitable function available to fulfill it, OR the request is missing critical parameters.

**CRITICAL: You MUST generate the user query in English, regardless of function names or descriptions.**
{error_feedback_block}
{history_block}
{last_round_block}

Your task:
Generate a natural user query that would require a function that doesn't exist, or that is missing critical information.

Examples:
- "Retrieve my recent invoice" (but no retrieve_invoice function exists)
- "Book a hotel" (missing: location, check-in date, etc.)

Output format (strictly follow this format):
user query: <your natural language query here>
reason: <explanation of what function/info is missing>
"""

    elif turn_type == "merged":
        # Merge 操作：多意图场景
        prompt = f"""You are role-playing as a user in a multi-turn conversation with a function-calling agent.

This is Turn {turn_idx}. This is a **MERGED** scenario where you express multiple intents in a single query.

**MERGED Definition**:
- Multiple functions in the SAME turn with potential SHORT DEPENDENCY
- Output of one function may feed as input to the next (within same turn)
- User EXPLICITLY mentions ALL actions/intents (unlike insert where some are implicit)
- Use connecting words to link multiple intents: "and", "then", "after that"
- Show the data flow relationship clearly

**All functions to call**: {', '.join(turn_functions)}

**CRITICAL: You MUST generate the user query in English, regardless of function names or descriptions.**
{error_feedback_block}
{history_block}
{last_round_block}

**Critical Instructions**:
1. EXPLICITLY mention ALL {len(turn_functions)} intents/actions in your query
2. Use connecting words: "and", "then", "after that" to link them
3. Make the data flow clear if functions have dependencies
4. Each function should be reflected in the query
5. Natural combination of multiple explicit intents

**Contrast with Insert Short**:
- Insert Short: "Navigate to San Mateo" (only final goal, distance is implicit)
- Merged: "Find the distance to San Mateo and set up navigation" (both steps explicit)

{style_instruction}
{examples_block}
Candidate Functions:
{candidate_block}

Output format (strictly follow this format):
user query: <natural English query EXPLICITLY mentioning ALL intents with connecting words>
chose func: {', '.join(turn_functions)}
reason: <explain why these functions are needed and how they relate (e.g., which output feeds into which input)>
"""

    elif turn_type == "merged_with_insert":
        # Merge + Insert 混合：部分显式 + 部分隐式
        # 需要区分三类函数：
        # 1. merged 函数：显式的合并意图
        # 2. long_dependency insert：显式的，但使用代词引用历史
        # 3. short_dependency insert：隐式的 helper

        merged_funcs = []
        long_dep_funcs = []
        short_dep_funcs = []
        short_dependencies = []  # 存储 short dependency 的依赖关系
        long_dependencies = []  # 存储 long dependency 的跨 turn 依赖关系

        if turn_operations:
            # 从 merge_info 提取 merged 函数
            merge_info = turn_operations.get("merge_info")
            if merge_info:
                # 优先使用 merged_names（函数名列表）
                merged_names = merge_info.get("merged_names", [])
                if merged_names:
                    merged_funcs = merged_names
                else:
                    # 如果没有 merged_names，尝试使用 merged_functions（索引）
                    # 但注意：这些索引是全局索引，不能直接用于 turn_functions
                    # 所以如果没有 merged_names，我们无法准确获取函数名
                    merged_funcs = []

            # 从 insert_info 提取 inserted 函数，并区分 long/short dependency
            insert_info_list = turn_operations.get("insert_info", [])
            for insert_info in insert_info_list:
                # 直接使用 nested_func_name（函数名）
                nested_func_name = insert_info.get("nested_func_name")
                source_func_name = insert_info.get("source_func_name")
                source_turn_idx = insert_info.get("source_turn_idx")
                target_turn_idx = insert_info.get("target_turn_idx", turn_idx)
                insert_type = insert_info.get("insert_type")

                if nested_func_name:
                    if insert_type == "long_dependency":
                        # Long dependency: 显式，但需要代词引用
                        long_dep_funcs.append(nested_func_name)
                        # 记录跨 turn 依赖关系
                        if source_func_name and source_turn_idx is not None:
                            long_dependencies.append({
                                'source_turn': source_turn_idx,
                                'source_func': source_func_name,
                                'target_turn': target_turn_idx,
                                'target_func': nested_func_name
                            })
                    else:
                        # Short dependency: 隐式 helper
                        short_dep_funcs.append(nested_func_name)
                        # 记录依赖关系
                        if source_func_name:
                            short_dependencies.append({
                                'source': source_func_name,
                                'target': nested_func_name
                            })

        # 如果没有 turn_operations，回退到所有函数都显式
        if not merged_funcs and not long_dep_funcs and not short_dep_funcs:
            merged_funcs = turn_functions

        # 显式函数 = merged + long_dependency
        explicit_funcs = merged_funcs + long_dep_funcs
        explicit_funcs_str = ', '.join(explicit_funcs) if explicit_funcs else "None"
        merged_funcs_str = ', '.join(merged_funcs) if merged_funcs else "None"
        long_dep_funcs_str = ', '.join(long_dep_funcs) if long_dep_funcs else "None"
        short_dep_funcs_str = ', '.join(short_dep_funcs) if short_dep_funcs else "None"

        # 构建依赖关系说明，包含 output schema
        dependency_info = ""
        if short_dependencies:
            dependency_info = "\n**Short Dependency Data Flow (same turn, implicit helpers)**:\n"
            for dep in short_dependencies:
                source_func = dep['source']
                target_func = dep['target']
                # 获取 source 函数的输出 schema
                output_info = get_function_output_info(source_func, tool_schemas)
                dependency_info += f"  - {source_func} → {target_func}\n"
                dependency_info += f"    {source_func} output:\n{output_info}\n"
                dependency_info += f"    → {target_func} input: see parameters in Candidate Functions below\n"
        if long_dependencies:
            dependency_info += "**Long Dependency Relationships (cross-turn data flow)**:\n"
            for dep in long_dependencies:
                source_func = dep['source_func']
                target_func = dep['target_func']
                # 获取 source 函数的输出 schema
                output_info = get_function_output_info(source_func, tool_schemas)
                dependency_info += f"  - Turn {dep['source_turn']}: {source_func} → Turn {dep['target_turn']}: {target_func}\n"
                dependency_info += f"    {source_func} output:\n{output_info}\n"
                dependency_info += f"    → {target_func} input: see parameters in Candidate Functions below\n"
            dependency_info += "\n"

        prompt = f"""You are role-playing as a user in a multi-turn conversation with a function-calling agent.

This is Turn {turn_idx}. This is a **MERGE + INSERT** scenario with multiple types of functions:

**Function Classification**:
- **MERGED functions** (explicit intents): {merged_funcs_str}
- **LONG-DEPENDENCY functions** (explicit, reference history): {long_dep_funcs_str}
- **SHORT-DEPENDENCY helpers** (implicit, do NOT mention): {short_dep_funcs_str}
- **All functions to call**: {', '.join(turn_functions)}
{dependency_info}
**CRITICAL: You MUST generate the user query in English, regardless of function names or descriptions.**
{error_feedback_block}
{history_block}
{last_round_block}

**Critical Instructions**:
1. **MERGED functions** ({merged_funcs_str}): Express these explicit intents clearly
2. **LONG-DEPENDENCY functions** ({long_dep_funcs_str}):
   - Express these intents BUT use pronouns to reference previous outputs
   - "that <noun>", "those <noun>", "my <noun>"
   - DO NOT repeat specific values from history
   - Understand the cross-turn data flow shown above
3. **SHORT-DEPENDENCY helpers** ({short_dep_funcs_str}):
   - DO NOT mention these - they work automatically in the background
   - Understand the same-turn data flow: these help process outputs from other functions
4. Use connecting words like "and", "then" for multiple explicit intents
5. Understand both cross-turn (long-dep) and same-turn (short-dep) data flows
6. Query should lead to calling ALL {len(turn_functions)} functions

**Good Examples**:
✓ "Get weather forecast for Shanghai and check that distance" (merged + long-dep with pronoun)
✓ "Book flights to Beijing and cancel my previous reservation" (merged + long-dep)

**Bad Examples**:
✗ "Get weather and also get live temperature" ← Mentions short-dep helper
✗ "Check the 25.4km distance" ← Repeats specific value instead of using pronoun

{style_instruction}
{examples_block}
Candidate Functions:
{candidate_block}

Output format (strictly follow this format):
user query: <natural English query expressing merged intents + long-dep with pronouns, NO short-dep helpers>
chose func: {', '.join(turn_functions)}
reason: <explain which are merged, which are long-dep (from which turn numbers), which are short-dep helpers, both cross-turn and same-turn data flows, and why ALL are needed>
"""

    elif turn_type == "insert_short":
        # Insert 短依赖：隐式嵌套
        # 区分主函数和插入函数
        primary_funcs = []
        inserted_funcs = []
        dependencies = []  # 存储依赖关系

        if turn_operations:
            # 从 insert_info 提取插入的函数和依赖关系
            insert_info_list = turn_operations.get("insert_info", [])
            for insert_info in insert_info_list:
                # 直接使用 nested_func_name（函数名）
                nested_func_name = insert_info.get("nested_func_name")
                source_func_name = insert_info.get("source_func_name")

                if nested_func_name:
                    inserted_funcs.append(nested_func_name)
                    # 记录依赖关系，包含 output schema
                    if source_func_name:
                        dependencies.append({
                            'source': source_func_name,
                            'target': nested_func_name
                        })

            # 主函数 = 所有函数 - 插入的函数
            primary_funcs = [f for f in turn_functions if f not in inserted_funcs]

        # 如果没有 turn_operations，回退到原有逻辑（第一个是主函数）
        if not primary_funcs and not inserted_funcs:
            primary_funcs = [turn_functions[0]] if turn_functions else []
            inserted_funcs = turn_functions[1:] if len(turn_functions) > 1 else []

        primary_funcs_str = ', '.join(primary_funcs) if primary_funcs else "None"
        inserted_funcs_str = ', '.join(inserted_funcs) if inserted_funcs else "None"

        # 构建依赖关系说明，包含 output schema
        dependency_info = ""
        if dependencies:
            dependency_info = f"\n**Data Flow (output feeds as input)**:\n"
            for dep in dependencies:
                source_func = dep['source']
                target_func = dep['target']
                # 获取 source 函数的输出 schema
                output_info = get_function_output_info(source_func, tool_schemas)
                dependency_info += f"  - {source_func} → {target_func}\n"
                dependency_info += f"    {source_func} output:\n{output_info}\n"
                dependency_info += f"    → {target_func} input: see parameters in Candidate Functions below\n"

        prompt = f"""You are role-playing as a user in a multi-turn conversation with a function-calling agent.

This is Turn {turn_idx}. The user will make a query that **implicitly** requires calling multiple functions, even though the user only explicitly mentions the primary goal.

**PRIMARY function(s) to mention in query**: {primary_funcs_str}
**IMPLICIT nested/helper function(s) (do NOT mention)**: {inserted_funcs_str}
**All functions that will be called**: {', '.join(turn_functions)}
{dependency_info}
**CRITICAL: You MUST generate the user query in English, regardless of function names or descriptions.**
{error_feedback_block}
{history_block}
{last_round_block}

**Critical Instructions**:
1. Your query should ONLY express the PRIMARY goal: {primary_funcs_str}
2. DO NOT mention the nested/helper functions: {inserted_funcs_str}
3. The nested functions work automatically in the background to support the primary goal
4. Understand the data flow: the output of one function feeds as input to the next
5. Keep your query natural and focused on what the user actually wants

{style_instruction}
{examples_block}
Candidate Functions:
{candidate_block}

Output format (strictly follow this format):
user query: <natural English query focusing ONLY on primary goal: {primary_funcs_str}>
chose func: {', '.join(turn_functions)}
reason: <explain the data flow and why nested function is needed even though user didn't mention it>
"""

    elif turn_type == "insert_long":
        # Insert 长依赖：从历史获取参数
        # 提取跨 turn 的依赖关系
        long_dependencies = []

        if turn_operations:
            insert_info_list = turn_operations.get("insert_info", [])
            for insert_info in insert_info_list:
                source_turn_idx = insert_info.get("source_turn_idx")
                source_func_name = insert_info.get("source_func_name")
                nested_func_name = insert_info.get("nested_func_name")
                target_turn_idx = insert_info.get("target_turn_idx", turn_idx)

                if source_func_name and nested_func_name and source_turn_idx is not None:
                    long_dependencies.append({
                        'source_turn': source_turn_idx,
                        'source_func': source_func_name,
                        'target_turn': target_turn_idx,
                        'target_func': nested_func_name
                    })

        # 构建依赖关系说明，包含 output schema
        dependency_info = ""
        if long_dependencies:
            dependency_info = "\n**Long Dependency Relationships (cross-turn data flow)**:\n"
            for dep in long_dependencies:
                source_func = dep['source_func']
                target_func = dep['target_func']
                # 获取 source 函数的输出 schema
                output_info = get_function_output_info(source_func, tool_schemas)
                dependency_info += f"  - Turn {dep['source_turn']}: {source_func} → Turn {dep['target_turn']}: {target_func}\n"
                dependency_info += f"    {source_func} output:\n{output_info}\n"
                dependency_info += f"    → {target_func} input: see parameters in Candidate Functions below\n"
            dependency_info += "\n"

        prompt = f"""You are role-playing as a user in a multi-turn conversation with a function-calling agent.

This is Turn {turn_idx}. This is a **LONG DEPENDENCY** scenario where you reference results from previous turns.

**LONG DEPENDENCY Definition**:
- Your query references outputs from **earlier turns** (NOT the same turn)
- You use PRONOUNS and INDIRECT REFERENCES to refer to previous results
- You do NOT repeat specific values, IDs, or numbers from history
- Natural conversation style: users don't remember exact values, they use references

**Functions to call**: {', '.join(turn_functions)}
{dependency_info}
**CRITICAL: You MUST generate the user query in English, regardless of function names or descriptions.**
{error_feedback_block}
{history_block}
{last_round_block}

**Critical Instructions for Long Dependency**:
1. Reference previous results using pronouns:
   - "that <noun>" → "that distance", "that booking", "that result"
   - "those <noun>" → "those records", "those cities"
   - "the previous <noun>" → "the previous search"
   - "my <noun>" → "my trip", "my reservation"
2. DO NOT repeat specific values from history (e.g., don't say "25.4km" or "booking ID 3426812")
3. Make it sound like natural conversation continuation
4. Assume the agent remembers the context
5. Understand the cross-turn data flow shown above

**Good Examples**:
✓ "Using that distance, find nearby cities"
✓ "Cancel my New York trip"
✓ "Export those customer records to PDF"

**Bad Examples** (avoid these):
✗ "Using 25.4 kilometers, find cities" ← Don't repeat the exact value
✗ "Cancel booking 3426812" ← Don't use specific IDs
✗ "Export the 150 records" ← Don't repeat exact counts

{style_instruction}
{examples_block}
Candidate Functions:
{candidate_block}

Output format (strictly follow this format):
user query: <natural English query using pronouns to reference previous outputs, NO specific values>
chose func: {', '.join(turn_functions)}
reason: <explain which parameters come from which previous turns (specify turn numbers), the cross-turn data flow, and why pronouns are used>
"""

    elif turn_type == "insert_mixed":
        # Insert 混合：同时有 short 和 long dependency
        # 区分主函数和short dependency的插入函数
        primary_funcs = []
        inserted_short_funcs = []
        short_dependencies = []  # 存储 short dependency 的依赖关系
        long_dep_funcs = []  # 存储 long dependency 函数
        long_dependencies = []  # 存储 long dependency 的跨 turn 依赖关系

        if turn_operations:
            # 从 insert_info 提取 short 和 long dependency 的插入函数
            insert_info_list = turn_operations.get("insert_info", [])
            for insert_info in insert_info_list:
                nested_func_name = insert_info.get("nested_func_name")
                source_func_name = insert_info.get("source_func_name")
                source_turn_idx = insert_info.get("source_turn_idx")
                target_turn_idx = insert_info.get("target_turn_idx", turn_idx)
                insert_type = insert_info.get("insert_type")

                if nested_func_name:
                    if insert_type == "short_dependency":
                        # Short dependency 函数是隐式的
                        inserted_short_funcs.append(nested_func_name)
                        if source_func_name:
                            short_dependencies.append({
                                'source': source_func_name,
                                'target': nested_func_name
                            })
                    elif insert_type == "long_dependency":
                        # Long dependency 函数需要用代词引用
                        long_dep_funcs.append(nested_func_name)
                        # 记录跨 turn 依赖关系
                        if source_func_name and source_turn_idx is not None:
                            long_dependencies.append({
                                'source_turn': source_turn_idx,
                                'source_func': source_func_name,
                                'target_turn': target_turn_idx,
                                'target_func': nested_func_name
                            })

            # 主函数 = 所有函数 - short dependency 的插入函数
            primary_funcs = [f for f in turn_functions if f not in inserted_short_funcs]

        # 如果没有 turn_operations，所有函数都视为主函数
        if not primary_funcs:
            primary_funcs = turn_functions

        primary_funcs_str = ', '.join(primary_funcs) if primary_funcs else "None"
        inserted_short_funcs_str = ', '.join(inserted_short_funcs) if inserted_short_funcs else "None"
        long_dep_funcs_str = ', '.join(long_dep_funcs) if long_dep_funcs else "None"

        # 构建依赖关系说明，包含 output schema
        dependency_info = ""
        if short_dependencies:
            dependency_info = "\n**Short Dependency Data Flow (same turn, implicit)**:\n"
            for dep in short_dependencies:
                source_func = dep['source']
                target_func = dep['target']
                # 获取 source 函数的输出 schema
                output_info = get_function_output_info(source_func, tool_schemas)
                dependency_info += f"  - {source_func} → {target_func}\n"
                dependency_info += f"    {source_func} output:\n{output_info}\n"
                dependency_info += f"    → {target_func} input: see parameters in Candidate Functions below\n"
        if long_dependencies:
            dependency_info += "**Long Dependency Relationships (cross-turn data flow)**:\n"
            for dep in long_dependencies:
                source_func = dep['source_func']
                target_func = dep['target_func']
                # 获取 source 函数的输出 schema
                output_info = get_function_output_info(source_func, tool_schemas)
                dependency_info += f"  - Turn {dep['source_turn']}: {source_func} → Turn {dep['target_turn']}: {target_func}\n"
                dependency_info += f"    {source_func} output:\n{output_info}\n"
                dependency_info += f"    → {target_func} input: see parameters in Candidate Functions below\n"
            dependency_info += "\n"

        prompt = f"""You are role-playing as a user in a multi-turn conversation with a function-calling agent.

This is Turn {turn_idx}. This is a **MIXED DEPENDENCY** scenario combining BOTH:
- **LONG dependency**: References outputs from earlier turns using pronouns
- **SHORT dependency**: Helper functions work implicitly in the background

**PRIMARY function(s) to mention in query**: {primary_funcs_str}
**IMPLICIT short-dependency helper(s) (do NOT mention)**: {inserted_short_funcs_str}
**All functions that will be called**: {', '.join(turn_functions)}
{dependency_info}
**CRITICAL: You MUST generate the user query in English, regardless of function names or descriptions.**
{error_feedback_block}
{history_block}
{last_round_block}

**Critical Instructions**:
1. **LONG dependency** - Reference previous results using pronouns:
   - "that <noun>" → "that distance", "that result"
   - "those <noun>" → "those records", "those cities"
   - "my <noun>" → "my trip", "my booking"
   - DO NOT repeat specific values/IDs from history
2. **SHORT dependency** - DO NOT mention helpers: {inserted_short_funcs_str}
   - These functions work automatically in the background
   - Understand the same-turn data flow: output feeds as input
3. Express ONLY the PRIMARY intent: {primary_funcs_str}
4. Natural conversation style - assume the agent remembers context
5. Understand both cross-turn (long-dep) and same-turn (short-dep) data flows shown above
6. Query should lead to calling ALL {len(turn_functions)} functions

**Good Examples**:
✓ "Using that distance, find nearby restaurants" (long ref + short helper implicit)
✓ "Book a hotel at those locations" (long ref)

**Bad Examples**:
✗ "Using 25.4km, find restaurants and convert coordinates" ← Repeats value + mentions helper
✗ "Book hotel at location IDs 123, 456" ← Uses specific IDs

{style_instruction}
{examples_block}
Candidate Functions:
{candidate_block}

Output format (strictly follow this format):
user query: <natural English query with pronouns for history, expressing ONLY primary intent: {primary_funcs_str}>
chose func: {', '.join(turn_functions)}
reason: <explain the mix: which are long dependency (from which turn numbers), which are short dependency helpers, both cross-turn and same-turn data flows, and why all are needed>
"""

    else:
        # Normal turn
        if is_first_turn:
            prompt = f"""You are role-playing as a user in a multi-turn conversation with a function-calling agent.

This is the **first turn** (Turn 0) of the conversation, so there is no previous history.

**CRITICAL: You MUST generate the user query in English, regardless of function names or descriptions.**
{error_feedback_block}

{style_instruction}

Candidate Functions:
{candidate_block}

Output format (strictly follow this format):
user query: <your natural language query here>
chose func: {', '.join(turn_functions)}
reason: <explanation of why you chose these functions>
"""
        else:
            prompt = f"""You are role-playing as a user in a multi-turn conversation with a function-calling agent.

This is Turn {turn_idx}. You will continue the conversation based on previous turn outputs.

**CRITICAL: You MUST generate the user query in English, regardless of function names or descriptions.**
{error_feedback_block}
{history_block}
{last_round_block}

{style_instruction}
{examples_block}
Candidate Functions:
{candidate_block}

Output format (strictly follow this format):
user query: <your natural language query here>
chose func: {', '.join(turn_functions)}
reason: <explanation of why you chose these functions and how they relate to previous outputs>
"""

    return prompt


# ==================== LLM 调用 ====================

async def call_llm(
    prompt: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 1.0,
    max_tokens: int = 512,
) -> Dict[str, Any]:
    """
    调用 LLM

    Returns:
        {
            "content": str,
            "token_usage": {
                "prompt_tokens": int,
                "completion_tokens": int,
                "total_tokens": int,
            }
        }
    """
    try:
        response = await async_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        content = response.choices[0].message.content or ""
        usage = response.usage

        return {
            "content": content,
            "token_usage": {
                "prompt_tokens": usage.prompt_tokens if usage else 0,
                "completion_tokens": usage.completion_tokens if usage else 0,
                "total_tokens": usage.total_tokens if usage else 0,
            }
        }
    except Exception as e:
        raise RuntimeError(f"LLM call failed: {e}")


def parse_query_response(response: str) -> Dict[str, Any]:
    """
    解析 query 生成的响应

    Expected format:
        user query: ...
        chose func: ...
        reason: ...
    """
    lines = response.strip().split("\n")

    user_query = ""
    chose_func = []
    reason = ""

    for line in lines:
        line = line.strip()
        if line.startswith("user query:"):
            user_query = line[len("user query:"):].strip()
        elif line.startswith("chose func:"):
            func_str = line[len("chose func:"):].strip()
            chose_func = [f.strip() for f in func_str.split(",")]
        elif line.startswith("reason:"):
            reason = line[len("reason:"):].strip()

    return {
        "user_query": user_query,
        "chose_func": chose_func,
        "reason": reason,
        "raw_output": response,
    }


# ==================== Backward: 生成 Query ====================

async def generate_query_for_turn_magnet(
    turn_idx: int,
    turn_type: str,
    turn_functions: List[str],
    all_turn_outputs: List[List[Dict]],
    tool_schemas: Dict[str, Dict],
    turn_operations: Optional[Dict[str, Any]] = None,
    error_feedback: Optional[str] = None,
) -> Dict[str, Any]:
    """
    为指定 turn 生成 query (MAGNET 方法)

    Returns:
        {
            "user_query": str,
            "chose_func": List[str],
            "reason": str,
            "raw_output": str,
            "token_usage": Dict,
        }
    """
    prompt = build_prompt_for_turn(
        turn_idx=turn_idx,
        turn_type=turn_type,
        turn_functions=turn_functions,
        all_turn_outputs=all_turn_outputs,
        tool_schemas=tool_schemas,
        turn_operations=turn_operations,
        error_feedback=error_feedback,
    )

    llm_result = await call_llm(
        prompt=prompt,
        model=DEFAULT_MODEL,
        temperature=1.0,
        max_tokens=512,
    )

    parsed = parse_query_response(llm_result["content"])
    parsed["token_usage"] = llm_result["token_usage"]

    return parsed


# ==================== 执行顺序推断 ====================

def infer_execution_order(
    turn_functions: List[str],
    tool_schemas: Dict[str, Dict],
) -> List[str]:
    """
    推断 turn 内函数的执行顺序

    简单策略：
    - 如果只有 1-2 个函数，按原顺序
    - 如果有更多函数，尝试基于输入输出类型排序

    TODO: 可以改进为基于依赖图的拓扑排序
    """
    if len(turn_functions) <= 2:
        return turn_functions

    # 简单策略：保持原顺序（假设 FSP 生成时已经排好序）
    return turn_functions


# ==================== Forward: 顺序执行 + 参数传递 ====================

async def forward_with_sequential_execution(
    turn_idx: int,
    turn_query: str,
    turn_functions: List[str],
    all_turn_outputs: List[List[Dict]],
    tool_schemas: Dict[str, Dict],
) -> Dict[str, Any]:
    """
    Forward 阶段：顺序执行 turn 内函数，支持参数传递

    核心逻辑：
    1. 推断执行顺序
    2. 逐个生成函数参数
    3. 立即执行，将输出添加到可用上下文
    4. 下一个函数可以使用前面函数的输出

    Returns:
        {
            "think": str,
            "tool_calls": List[Dict],
            "turn_outputs": List[Dict],
            "token_usage": Dict,
        }
    """
    execution_order = infer_execution_order(turn_functions, tool_schemas)

    tool_calls = []
    turn_outputs = []
    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }

    for func_idx, func_name in enumerate(execution_order):
        try:
            # 构建可用上下文：历史 + 当前 turn 已执行的输出
            available_context = []
            for h_outputs in all_turn_outputs:
                available_context.extend(h_outputs)
            available_context.extend(turn_outputs)

            # 为当前函数生成参数
            param_result = await generate_single_func_params(
                turn_query=turn_query,
                func_name=func_name,
                available_context=available_context,
                tool_schemas=tool_schemas,
            )

            # 累加 token 使用
            tq = param_result.get("token_usage", {})
            total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
            total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
            total_token_usage["total_tokens"] += tq.get("total_tokens", 0)

            parameters = param_result.get("parameters", {})
            params_source = param_result.get("params_source", {})

            tool_call = {
                "function": func_name,
                "parameters": parameters,
                "params_source": params_source,
            }
            tool_calls.append(tool_call)

        except Exception as e:
            raise RuntimeError(
                f"[generate_single_func_params] Failed for function '{func_name}' "
                f"at turn {turn_idx}, func_idx={func_idx}: {e}"
            )

        # 立即执行函数
        try:
            exec_result = await execute_function_call(
                func_name=func_name,
                parameters=parameters,
                tool_schemas=tool_schemas,
            )

            # 累加执行的 token 使用 (如果有)
            exec_tq = exec_result.get("token_usage", {})
            total_token_usage["prompt_tokens"] += exec_tq.get("prompt_tokens", 0)
            total_token_usage["completion_tokens"] += exec_tq.get("completion_tokens", 0)
            total_token_usage["total_tokens"] += exec_tq.get("total_tokens", 0)

            turn_outputs.append(exec_result)

        except Exception as e:
            raise RuntimeError(
                f"[execute_function_call] Failed for function '{func_name}' "
                f"at turn {turn_idx}, func_idx={func_idx}, "
                f"parameters={parameters}: {e}"
            )

    return {
        "think": f"Executed {len(tool_calls)} functions in turn {turn_idx}",
        "tool_calls": tool_calls,
        "turn_outputs": turn_outputs,
        "token_usage": total_token_usage,
    }


async def generate_single_func_params(
    turn_query: str,
    func_name: str,
    available_context: List[Dict],
    tool_schemas: Dict[str, Dict],
) -> Dict[str, Any]:
    """
    为单个函数生成参数

    Args:
        turn_query: 当前 turn 的用户查询
        func_name: 要生成参数的函数
        available_context: 可用的输出上下文 (历史 + turn 内已执行)
        tool_schemas: 工具 schema

    Returns:
        {
            "parameters": Dict,
            "params_source": Dict,
            "token_usage": Dict,
        }
    """
    try:
        # 构建上下文信息
        context_block = ""
        if available_context:
            context_parts = []
            for i, ctx in enumerate(available_context):
                func = ctx.get("function", "unknown")
                output = ctx.get("output", {})
                context_parts.append(f"[{i}] {func}: {format_tool_output(output)}")
            context_block = f"""
[Available Context from Previous Function Calls]
{chr(10).join(context_parts)}
"""

        # 获取函数 schema
        func_schema = tool_schemas.get(func_name, {})
        func_doc = build_function_documentation(func_name, func_schema)

        prompt = f"""You are a function-calling agent. Extract parameters for the target function from the user query and available context.

**CRITICAL: All your responses and reasoning must be in English, regardless of function names or query content.**

User Query: {turn_query}
{context_block}

Target Function:
{func_doc}

**Instructions**:
1. Extract parameter values from the user query first
2. If a parameter is not in the query, check if it can be obtained from the available context
3. For each parameter, indicate its source

Output format (JSON):
{{
    "parameters": {{
        "param1": "value1",
        "param2": "value2"
    }},
    "params_source": {{
        "param1": "user_query",
        "param2": "context[0]"
    }}
}}
"""

        llm_result = await call_llm(
            prompt=prompt,
            model=DEFAULT_MODEL,
            temperature=0.3,
            max_tokens=1024,
        )

    except Exception as e:
        raise RuntimeError(
            f"[call_llm] Failed when calling LLM for function '{func_name}': {e}"
        )

    # 解析 JSON 响应
    try:
        content = llm_result["content"].strip()
        # 移除可能的代码块标记
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        parsed = json.loads(content)
        parameters = parsed.get("parameters", {})
        params_source = parsed.get("params_source", {})

    except json.JSONDecodeError as e:
        print(f"[WARN] Failed to parse JSON response for {func_name}: {e}")
        print(f"Response: {llm_result['content']}")
        # 返回空参数而不是抛出异常
        parameters = {}
        params_source = {}

    except Exception as e:
        raise RuntimeError(
            f"[parse_json] Failed to parse LLM response for function '{func_name}': {e}"
        )

    return {
        "parameters": parameters,
        "params_source": params_source,
        "token_usage": llm_result["token_usage"],
    }


# ==================== 空 Turn 处理 ====================

async def handle_empty_turn(
    turn_idx: int,
    all_turn_outputs: List[List[Dict]],
    tool_schemas: Dict[str, Dict],
    miss_type: str = "miss_func",
) -> Dict[str, Any]:
    """
    处理空 turn (Split 操作)

    Returns:
        {
            "user_query": str,
            "response": str,
            "miss_type": str,
            "token_usage": Dict,
        }
    """
    # 生成 query
    query_result = await generate_query_for_turn_magnet(
        turn_idx=turn_idx,
        turn_type="empty",
        turn_functions=[],
        all_turn_outputs=all_turn_outputs,
        tool_schemas=tool_schemas,
        turn_operations=None,  # empty turn 没有 operations
    )

    user_query = query_result.get("user_query", "")

    # 生成响应 (模拟 agent 无法满足请求)
    if miss_type == "miss_func":
        response = "I don't have a function to handle this request. Could you please clarify or provide more details?"
    else:
        response = "To proceed with this request, I need more information. Could you please provide the missing details?"

    return {
        "user_query": user_query,
        "response": response,
        "miss_type": miss_type,
        "reason": query_result.get("reason", ""),
        "token_usage": query_result.get("token_usage", {}),
    }


# ==================== 主处理流程 ====================

async def process_single_fsp_path(
    path_data: Dict[str, Any],
    tool_schemas: Dict[str, Dict],
) -> Dict[str, Any]:
    """
    处理单个 FSP v2 路径 (MAGNET 方法)

    流程：
    1. 加载 FSP (List[List[int]])
    2. 对每个 turn:
       - 检测 turn 类型
       - 生成 query (Backward)
       - 顺序执行函数 (Forward with intra-turn dependencies)
       - 累积历史输出
    3. 返回完整轨迹

    Args:
        path_data: FSP v2 数据
        tool_schemas: 工具 schema

    Returns:
        {
            "path_info": Dict,  # 路径标识信息
            "turns_data": List[Dict],  # 每个 turn 的完整信息
            "token_usage": Dict,
        }
    """
    try:
        fsp_final = path_data.get("fsp_final", [])
        fsp_final_names = path_data.get("fsp_final_names", [])
        node_idx = path_data.get("node_idx", -1)
        path_idx = path_data.get("path_idx", -1)

        if not fsp_final:
            raise ValueError("Empty FSP: fsp_final is empty")

        # 初始化
        all_turn_outputs: List[List[Dict]] = []
        turns_data: List[Dict] = []
        total_token_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

        # 处理每个 turn
        for turn_idx, turn_functions in enumerate(fsp_final_names):
            print(f"  Processing Turn {turn_idx}/{len(fsp_final_names)-1}: {turn_functions}")

            try:
                # 检测 turn 操作
                turn_operations = detect_turn_operations(turn_idx, turn_functions, path_data)
                primary_style = turn_operations["primary_style"]
                is_empty = turn_operations["is_empty"]

            except Exception as e:
                raise RuntimeError(
                    f"[detect_turn_operations] Failed at turn {turn_idx}, "
                    f"node_idx={node_idx}, path_idx={path_idx}, "
                    f"turn_functions={turn_functions}: {e}"
                )

            # 处理空 turn
            if is_empty:
                try:
                    empty_result = await handle_empty_turn(
                        turn_idx=turn_idx,
                        all_turn_outputs=all_turn_outputs,
                        tool_schemas=tool_schemas,
                        miss_type="miss_func",
                    )

                    tq = empty_result.get("token_usage", {})
                    total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
                    total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
                    total_token_usage["total_tokens"] += tq.get("total_tokens", 0)

                    turns_data.append({
                        "turn_idx": turn_idx,
                        "turn_type": primary_style,
                        "operations": turn_operations["operations"],
                        "user_query": empty_result.get("user_query", ""),
                        "response": empty_result.get("response", ""),
                        "miss_type": empty_result.get("miss_type", ""),
                        "reason": empty_result.get("reason", ""),
                    })

                    # 空 turn 不添加输出
                    all_turn_outputs.append([])
                    continue

                except Exception as e:
                    raise RuntimeError(
                        f"[handle_empty_turn] Failed at turn {turn_idx}, "
                        f"node_idx={node_idx}, path_idx={path_idx}: {e}"
                    )

            # 生成 query (Backward) + 顺序执行 (Forward) with retry
            max_retries = 1
            error_feedback = None

            for retry_attempt in range(max_retries + 1):
                # 生成 query (Backward)
                try:
                    query_result = await generate_query_for_turn_magnet(
                        turn_idx=turn_idx,
                        turn_type=primary_style,
                        turn_functions=turn_functions,
                        all_turn_outputs=all_turn_outputs,
                        tool_schemas=tool_schemas,
                        turn_operations=turn_operations,
                        error_feedback=error_feedback,
                    )

                    user_query = query_result.get("user_query", "")
                    if not user_query:
                        raise ValueError(f"Empty user_query generated for turn {turn_idx}")

                    tq = query_result.get("token_usage", {})
                    total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
                    total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
                    total_token_usage["total_tokens"] += tq.get("total_tokens", 0)

                except Exception as e:
                    raise RuntimeError(
                        f"[generate_query_for_turn_magnet] Failed at turn {turn_idx}, "
                        f"node_idx={node_idx}, path_idx={path_idx}, "
                        f"turn_type={primary_style}, functions={turn_functions}: {e}"
                    )

                # 顺序执行 + 参数传递 (Forward)
                try:
                    forward_result = await forward_with_sequential_execution(
                        turn_idx=turn_idx,
                        turn_query=user_query,
                        turn_functions=turn_functions,
                        all_turn_outputs=all_turn_outputs,
                        tool_schemas=tool_schemas,
                    )

                    tq = forward_result.get("token_usage", {})
                    total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
                    total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
                    total_token_usage["total_tokens"] += tq.get("total_tokens", 0)

                    turn_outputs = forward_result.get("turn_outputs", [])
                    all_turn_outputs.append(turn_outputs)

                    # 执行成功，跳出重试循环
                    break

                except Exception as e:
                    # 函数执行失败
                    if retry_attempt < max_retries:
                        # 构建错误反馈，重新生成 query
                        print(f"  ⚠️  Function execution failed at turn {turn_idx}, attempt {retry_attempt + 1}/{max_retries + 1}")
                        print(f"      Error: {str(e)}")
                        error_feedback = f"""Function execution failed with error:
{str(e)}

Please revise your query to avoid this execution error. Consider:
1. Check if the function parameters are correct
2. Ensure all required parameters are provided
3. Verify that parameter values are in the correct format
"""
                        continue  # 进入下一次重试
                    else:
                        # 重试次数用尽，抛出错误
                        raise RuntimeError(
                            f"[forward_with_sequential_execution] Failed at turn {turn_idx} after {max_retries + 1} attempts, "
                            f"node_idx={node_idx}, path_idx={path_idx}, "
                            f"user_query='{user_query}', functions={turn_functions}: {e}"
                        )

            # 记录 turn 信息
            turns_data.append({
                "turn_idx": turn_idx,
                "turn_type": primary_style,
                "operations": turn_operations["operations"],
                "functions": turn_functions,
                "user_query": user_query,
                "chose_func": query_result.get("chose_func", []),
                "reason": query_result.get("reason", ""),
                "tool_calls": forward_result.get("tool_calls", []),
                "outputs": turn_outputs,
            })

        return {
            "path_info": {
                "node_idx": node_idx,
                "path_idx": path_idx,
            },
            "turns_data": turns_data,
            "token_usage": total_token_usage,
            "statistics": path_data.get("statistics", {}),
        }

    except Exception as e:
        # 顶层错误：添加路径信息后重新抛出
        node_idx = path_data.get("node_idx", -1)
        path_idx = path_data.get("path_idx", -1)
        raise RuntimeError(
            f"[process_single_fsp_path] Failed to process path "
            f"node_idx={node_idx}, path_idx={path_idx}: {e}"
        )


# ==================== 批量处理 ====================

async def process_all_fsp_paths(
    max_paths: Optional[int] = None,
    batch_size: int = 5,
    resume: bool = False,
    early_stop_batches: int = 3,
) -> None:
    """
    处理所有 FSP v2 路径

    Args:
        max_paths: 最多处理多少条路径 (用于测试)
        batch_size: 并发批次大小
        resume: 是否启用断点续传（跳过已生成的 paths）
        early_stop_batches: 连续多少个 batch 全部失败后停止（0 表示不启用早停）
    """
    # 加载数据
    paths = load_fsp_v2(FSP_V2_PATH)
    tool_schemas = load_tool_schemas(TOOL_SCHEMA_SUMMARY_PATH)

    if max_paths is not None and max_paths < len(paths):
        paths = paths[:max_paths]
        print(f"[TEST MODE] Processing only {max_paths} paths")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # 断点续传：读取已处理的 paths
    successfully_processed_path_ids = set()

    if resume and os.path.exists(OUTPUT_PATH):
        print(f"\n🔄 Resume mode enabled, reading existing results from {OUTPUT_PATH}...")
        try:
            with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        path_info = record.get("path_info", {})
                        # 使用 node_idx 和 path_idx 作为唯一标识
                        node_idx = path_info.get("node_idx")
                        path_idx = path_info.get("path_idx")
                        if node_idx is not None and path_idx is not None:
                            path_id = (node_idx, path_idx)
                            # 文件中只有成功的记录（失败的不会被写入）
                            successfully_processed_path_ids.add(path_id)
                    except json.JSONDecodeError:
                        continue

            print(f"   Found {len(successfully_processed_path_ids)} successfully processed paths")

            # 过滤掉成功处理的 paths
            original_count = len(paths)
            paths = [
                p for p in paths
                if (p.get("node_idx"), p.get("path_idx")) not in successfully_processed_path_ids
            ]
            skipped_count = original_count - len(paths)

            print(f"   Skipping {skipped_count} successfully processed paths")
            print(f"   Remaining {len(paths)} paths to process")

            if len(paths) == 0:
                print("\n✅ All paths already processed! Nothing to do.")
                return

        except Exception as e:
            print(f"⚠️  Warning: Failed to read existing results: {e}")
            print("   Continuing without resume...")
            successfully_processed_path_ids.clear()

    print(f"\nTotal paths to process: {len(paths)}")
    print(f"Output -> {OUTPUT_PATH}\n")

    # 文件写入模式：
    # - 如果是 resume 模式，使用追加模式（a）
    # - 否则，使用覆盖模式（w）
    file_mode = "a" if resume else "w"
    if file_mode == "a":
        print(f"📝 Appending to existing file: {OUTPUT_PATH}\n")

    with open(OUTPUT_PATH, file_mode, encoding="utf-8") as f:
        total = len(paths)
        total_errors = 0
        overall_tokens = 0
        consecutive_failed_batches = 0  # 连续失败的 batch 计数
        num_batches = (total + batch_size - 1) // batch_size

        for batch_idx, start in enumerate(tqdm(range(0, total, batch_size),
                                               total=num_batches,
                                               desc="Processing FSP paths",
                                               unit="batch"), start=1):
            batch = paths[start: start + batch_size]
            print(
                f"\n[Batch {batch_idx}/{num_batches}] "
                f"Processing paths {start + 1}-{start + len(batch)} "
                f"out of {total}..."
            )

            batch_start_time = time.time()
            batch_tokens = 0
            batch_errors = 0

            tasks = [
                process_single_fsp_path(path, tool_schemas)
                for path in batch
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for path, result in zip(batch, results):
                if isinstance(result, Exception):
                    total_errors += 1
                    batch_errors += 1
                    print(f"[ERROR] Failed to process path: {result}")
                    # 失败的记录不写入文件，这样下次 resume 时会重新处理
                    continue
                else:
                    record = result
                    tq = record.get("token_usage", {})
                    batch_tokens += tq.get("total_tokens", 0)

                    # 只写入成功的记录
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    f.flush()

            batch_elapsed = time.time() - batch_start_time
            overall_tokens += batch_tokens

            # 早停检查：如果当前 batch 全部失败
            if batch_errors == len(batch):
                consecutive_failed_batches += 1
                print(
                    f"[Batch {batch_idx}] ❌ ALL {len(batch)} paths FAILED! "
                    f"(consecutive failed batches: {consecutive_failed_batches}/{early_stop_batches})"
                )

                # 如果连续失败的 batch 数量达到阈值，停止处理
                if early_stop_batches > 0 and consecutive_failed_batches >= early_stop_batches:
                    print("\n" + "=" * 80)
                    print("🛑 EARLY STOPPING TRIGGERED")
                    print("=" * 80)
                    print(f"Consecutive failed batches: {consecutive_failed_batches}")
                    print(f"Stopping to prevent further failures...")
                    print("=" * 80)
                    break
            else:
                # 如果当前 batch 有成功的，重置连续失败计数
                consecutive_failed_batches = 0
                print(
                    f"[Batch {batch_idx}] time={batch_elapsed:.2f}s, "
                    f"batch_tokens={batch_tokens}, overall_tokens={overall_tokens}, "
                    f"batch_errors={batch_errors}/{len(batch)}"
                )

    print("\n" + "=" * 80)
    print("PROCESSING SUMMARY")
    print("=" * 80)
    print(f"Total paths processed: {total}")
    print(f"Successful paths: {total - total_errors}")
    print(f"Failed paths: {total_errors}")
    print(f"Total tokens used: {overall_tokens}")
    print("=" * 80)
    print(f"\nAll paths processed, results saved to: {OUTPUT_PATH}")


# ==================== CLI 入口 ====================

def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="MAGNET-style Back-and-Forth Translation for FSP v2"
    )
    parser.add_argument(
        '--max-paths',
        type=int,
        default=None,
        help='Maximum number of paths to process (for testing)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=5,
        help='Batch size for parallel processing'
    )
    parser.add_argument(
        '--resume',
        action='store_true',
        help='Resume from previous run (skip already processed paths)'
    )
    parser.add_argument(
        '--early-stop',
        type=int,
        default=1,
        help='Stop after N consecutive batches with all failures (0 to disable)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test mode: process only 5 paths'
    )

    args = parser.parse_args()

    if args.test:
        print("🧪 Running in TEST mode (3 paths only)...")
        args.max_paths = 3

    asyncio.run(process_all_fsp_paths(
        max_paths=args.max_paths,
        batch_size=args.batch_size,
        resume=args.resume,
        early_stop_batches=args.early_stop,
    ))


if __name__ == "__main__":
    main()
