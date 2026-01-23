"""
Backward query generation: Generate user queries for each turn based on previous turn's function calls.

流程概述：
- 从 `graph/random_walk_paths_v1.json` 中读取包含 turns 的路径信息
首先通过random walk加上merge操作，会得到一条enhanced fsp path.
并且这条path上通过turn idx对fsp进行了阶段性的划分，我们先认为turn idx对应的是step idx
假设这条fsp path对应的是single turn multiple steps 的tool call调用。
那么现在的目标是给single turn生成一个user query, 采取的方法是 给每一个step生成一个atomic query，
最后把这条fsp path上的所有atomic query 进行一个merge -> final user query.
具体做法是: for fsp path step1: funcA and funcB, step2: func C steps3: func D and func E
we let atomic query 1 (corresponding to step1) ,it must satisfy to call the func A and B
then we based on the atomic query 1 to get the tool result A and tool result B.
then we based on the last round tool output, in this case is tool result A and B,
make a atomic query2 (step2), it need to be motivated by the last round tool output. and can call the func C. preferably the func C 's input come from last round tool output. 
Then we get the atomic query2, we based on the query2 and history execute the func C,
get the tool output(func C). then we based on the last round(tool output C) and the steps3 func D and E to generate the atomic query3.
final,we merge the atomic query list to generate the user query.
additional, the prompt rule in the build_prompt_for_turn is helpful.

TODO:
1. ✅ 为每个 step 生成 atomic query
2. ✅ 执行函数调用获取 tool output
3. ✅ 基于 tool output 生成下一个 atomic query（修改 prompt 包含 tool output）
4. ✅ 合并所有 atomic query 生成最终 user query
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
from functools import wraps
from typing import Any, Dict, List, Optional, Set, Tuple

from tqdm import tqdm
from openai import AsyncOpenAI


ROOT_DIR = "/data/lhy/datasets/graph-Toucan"
GRAPH_DIR = os.path.join(ROOT_DIR, "graph")
FSP_DIR = os.path.join(ROOT_DIR,"fsp_path")
TOOL_INFO_DIR = os.path.join(ROOT_DIR, "tool_info")
GENERATED_FUNCTIONS_DIR = os.path.join(TOOL_INFO_DIR, "generated_functions_v1")

# 安全执行配置：限制文件操作的工作目录
SAFE_WORK_DIR = os.path.join(ROOT_DIR, "safe_work_dir")
# 确保安全目录存在
os.makedirs(SAFE_WORK_DIR, exist_ok=True)


class SafeExecutionContext:
    """
    安全执行上下文，限制文件操作和危险操作
    """
    def __init__(self, safe_dir: str = SAFE_WORK_DIR):
        self.safe_dir = os.path.abspath(safe_dir)
        self.original_builtins = {}
        self.original_modules = {}
        self.original_os = None
        self.original_shutil = None
        self.original_subprocess = None
        
    def _check_path_safe(self, path: str) -> str:
        """
        检查路径是否在安全目录内，如果是则返回绝对路径，否则抛出异常
        
        如果路径是相对路径，会先解析为相对于安全目录的路径
        """
        safe_dir_abs = os.path.abspath(self.safe_dir)
        
        # 如果是相对路径，先解析为相对于安全目录的路径
        if not os.path.isabs(path):
            abs_path = os.path.abspath(os.path.join(safe_dir_abs, path))
        else:
            abs_path = os.path.abspath(path)
        
        # 检查路径是否在安全目录内
        try:
            # 使用 commonpath 检查路径是否在安全目录内
            common_path = os.path.commonpath([abs_path, safe_dir_abs])
            if common_path != safe_dir_abs:
                raise PermissionError(
                    f"File operation not allowed outside safe directory. "
                    f"Attempted path: {abs_path}, Safe directory: {safe_dir_abs}"
                )
        except ValueError:
            # 路径不在同一驱动器上（Windows）或完全不同
            raise PermissionError(
                f"File operation not allowed outside safe directory. "
                f"Attempted path: {abs_path}, Safe directory: {safe_dir_abs}"
            )
        
        return abs_path
    
    def _safe_open(self, file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
        """安全的 open 函数，限制文件操作在安全目录内"""
        if isinstance(file, str):
            file = self._check_path_safe(file)
        return self.original_builtins['open'](file, mode, buffering, encoding, errors, newline, closefd, opener)
    
    def _safe_os_remove(self, path):
        """安全的 os.remove，限制在安全目录内"""
        self._check_path_safe(path)
        return self.original_os.remove(path)
    
    def _safe_os_unlink(self, path):
        """安全的 os.unlink，限制在安全目录内"""
        self._check_path_safe(path)
        return self.original_os.unlink(path)
    
    def _safe_os_rmdir(self, path):
        """安全的 os.rmdir，限制在安全目录内"""
        self._check_path_safe(path)
        return self.original_os.rmdir(path)
    
    def _safe_os_makedirs(self, name, mode=0o777, exist_ok=False):
        """安全的 os.makedirs，限制在安全目录内"""
        self._check_path_safe(name)
        return self.original_os.makedirs(name, mode, exist_ok)
    
    def _safe_os_mkdir(self, name, mode=0o777):
        """安全的 os.mkdir，限制在安全目录内"""
        self._check_path_safe(name)
        return self.original_os.mkdir(name, mode)
    
    def _safe_shutil_rmtree(self, path, ignore_errors=False, onerror=None):
        """安全的 shutil.rmtree，限制在安全目录内"""
        self._check_path_safe(path)
        return self.original_shutil.rmtree(path, ignore_errors, onerror)
    
    def _safe_shutil_move(self, src, dst):
        """安全的 shutil.move，限制在安全目录内"""
        self._check_path_safe(src)
        self._check_path_safe(dst)
        return self.original_shutil.move(src, dst)
    
    def _safe_shutil_copy(self, src, dst):
        """安全的 shutil.copy，限制在安全目录内"""
        self._check_path_safe(src)
        self._check_path_safe(dst)
        return self.original_shutil.copy(src, dst)
    
    def _safe_shutil_copy2(self, src, dst):
        """安全的 shutil.copy2，限制在安全目录内"""
        self._check_path_safe(src)
        self._check_path_safe(dst)
        return self.original_shutil.copy2(src, dst)
    
    def _safe_subprocess_run(self, *args, **kwargs):
        """禁止 subprocess 操作"""
        raise PermissionError("subprocess operations are not allowed in safe execution context")
    
    def _safe_subprocess_call(self, *args, **kwargs):
        """禁止 subprocess 操作"""
        raise PermissionError("subprocess operations are not allowed in safe execution context")
    
    def _safe_subprocess_popen(self, *args, **kwargs):
        """禁止 subprocess 操作"""
        raise PermissionError("subprocess operations are not allowed in safe execution context")
    
    def _safe_eval(self, *args, **kwargs):
        """禁止 eval 操作"""
        raise PermissionError("eval operations are not allowed in safe execution context")
    
    def _safe_exec(self, *args, **kwargs):
        """禁止 exec 操作"""
        raise PermissionError("exec operations are not allowed in safe execution context")
    
    def _safe_compile(self, *args, **kwargs):
        """禁止 compile 操作"""
        raise PermissionError("compile operations are not allowed in safe execution context")
    
    def __enter__(self):
        """进入安全执行上下文"""
        import builtins
        import os as os_module
        import shutil
        import subprocess

        # 保存原始函数
        self.original_builtins['open'] = builtins.open
        self.original_builtins['eval'] = builtins.eval
        # 不再拦截 exec 和 compile，因为模块加载需要它们
        # self.original_builtins['exec'] = builtins.exec
        # self.original_builtins['compile'] = builtins.compile
        self.original_os = os_module
        self.original_shutil = shutil
        self.original_subprocess = subprocess

        # 替换为安全版本
        builtins.open = self._safe_open
        builtins.eval = self._safe_eval
        # 不再替换 exec 和 compile
        # builtins.exec = self._safe_exec
        # builtins.compile = self._safe_compile
        
        # 替换 os 模块的危险函数
        os_module.remove = self._safe_os_remove
        os_module.unlink = self._safe_os_unlink
        os_module.rmdir = self._safe_os_rmdir
        os_module.makedirs = self._safe_os_makedirs
        os_module.mkdir = self._safe_os_mkdir
        
        # 替换 shutil 模块的危险函数
        shutil.rmtree = self._safe_shutil_rmtree
        shutil.move = self._safe_shutil_move
        shutil.copy = self._safe_shutil_copy
        shutil.copy2 = self._safe_shutil_copy2
        
        # 替换 subprocess 模块的所有函数
        subprocess.run = self._safe_subprocess_run
        subprocess.call = self._safe_subprocess_call
        subprocess.Popen = self._safe_subprocess_popen
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出安全执行上下文，恢复原始函数"""
        import builtins
        import os as os_module
        import shutil
        import subprocess

        # 恢复原始函数
        builtins.open = self.original_builtins.get('open', builtins.open)
        builtins.eval = self.original_builtins.get('eval', builtins.eval)
        # exec 和 compile 未被修改，无需恢复
        # builtins.exec = self.original_builtins.get('exec', builtins.exec)
        # builtins.compile = self.original_builtins.get('compile', builtins.compile)
        
        if self.original_os:
            os_module.remove = self.original_os.remove
            os_module.unlink = self.original_os.unlink
            os_module.rmdir = self.original_os.rmdir
            os_module.makedirs = self.original_os.makedirs
            os_module.mkdir = self.original_os.mkdir
        
        if self.original_shutil:
            shutil.rmtree = self.original_shutil.rmtree
            shutil.move = self.original_shutil.move
            shutil.copy = self.original_shutil.copy
            shutil.copy2 = self.original_shutil.copy2
        
        if self.original_subprocess:
            subprocess.run = self.original_subprocess.run
            subprocess.call = self.original_subprocess.call
            subprocess.Popen = self.original_subprocess.Popen
        
        return False  # 不抑制异常

RANDOM_WALK_V1_PATH = "/data/lhy/datasets/graph-Toucan/walker_path/path_v1_converted.json"

TOOL_SCHEMA_SUMMARY_PATH = os.path.join(TOOL_INFO_DIR, "tool_schema_with_outputformat.json")
OUTPUT_QUERIES_PATH = os.path.join(FSP_DIR, "fsp_v1.json")
LOG_DIR = os.path.join(ROOT_DIR, "logs")
TOKEN_USAGE_LOG_PATH = os.path.join(LOG_DIR, "token_usage_log.jsonl")
TIME_LOG_PATH = os.path.join(LOG_DIR, "time_log.jsonl")
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
SIMULATE_API_MODEL = config["model"]["simulate_api"]

# 确保日志目录存在
os.makedirs(LOG_DIR, exist_ok=True)


def log_time_and_tokens(func_name: str):
    """
    装饰器函数，用于记录异步函数的执行时间和 token 使用量
    
    Args:
        func_name: 函数名称（用于日志记录）
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            timestamp = datetime.now().isoformat()
            
            try:
                # 执行函数
                result = await func(*args, **kwargs)
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # 提取 token 使用信息（如果返回值中包含）
                token_info = {}
                if isinstance(result, dict):
                    # 检查是否有 token_usage 字段
                    if "token_usage" in result:
                        token_info = result.get("token_usage", {})
                    # 检查是否有 usage 字段（OpenAI API 格式）
                    elif "usage" in result:
                        usage = result.get("usage", {})
                        token_info = {
                            "prompt_tokens": getattr(usage, "prompt_tokens", 0),
                            "completion_tokens": getattr(usage, "completion_tokens", 0),
                            "total_tokens": getattr(usage, "total_tokens", 0),
                        }
                
                # 记录时间日志
                time_log_entry = {
                    "timestamp": timestamp,
                    "function": func_name,
                    "elapsed_time_seconds": round(elapsed_time, 4),
                    "start_time": datetime.fromtimestamp(start_time).isoformat(),
                    "end_time": datetime.fromtimestamp(end_time).isoformat(),
                }
                
                # 记录 token 使用日志
                token_log_entry = {
                    "timestamp": timestamp,
                    "function": func_name,
                    **token_info,
                }
                
                # 写入日志文件
                try:
                    with open(TIME_LOG_PATH, "a", encoding="utf-8") as f:
                        f.write(json.dumps(time_log_entry, ensure_ascii=False) + "\n")
                    
                    if token_info:
                        with open(TOKEN_USAGE_LOG_PATH, "a", encoding="utf-8") as f:
                            f.write(json.dumps(token_log_entry, ensure_ascii=False) + "\n")
                except Exception as e:
                    print(f"[WARNING] Failed to write log: {e}")
                
                # 打印日志信息
                print(f"[LOG] {func_name}: time={elapsed_time:.4f}s", end="")
                if token_info:
                    total_tokens = token_info.get("total_tokens", 0)
                    prompt_tokens = token_info.get("prompt_tokens", 0)
                    completion_tokens = token_info.get("completion_tokens", 0)
                    print(f", tokens={total_tokens} (prompt={prompt_tokens}, completion={completion_tokens})")
                else:
                    print()
                
                return result
                
            except Exception as e:
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                # 记录错误日志
                error_log_entry = {
                    "timestamp": timestamp,
                    "function": func_name,
                    "elapsed_time_seconds": round(elapsed_time, 4),
                    "error": str(e),
                }
                
                try:
                    with open(TIME_LOG_PATH, "a", encoding="utf-8") as f:
                        f.write(json.dumps(error_log_entry, ensure_ascii=False) + "\n")
                except Exception as log_error:
                    print(f"[WARNING] Failed to write error log: {log_error}")
                
                print(f"[LOG] {func_name}: ERROR after {elapsed_time:.4f}s - {e}")
                raise
        
        return wrapper
    return decorator


def load_graph_adjacency(graph_path: str) -> Dict[str, List[str]]:
    """
    从图 JSON 文件中加载邻接关系，返回 function_name -> [successor_function_names] 的映射。
    """
    print(f"Loading graph adjacency from {graph_path}...")
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)
    
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    
    # 构建 index -> name 映射
    index_to_name: Dict[int, str] = {}
    for node in nodes:
        idx = node.get("index")
        func_schema = node.get("function_schema", {}).get("function", {})
        name = func_schema.get("name", f"node_{idx}")
        if idx is not None:
            index_to_name[idx] = name
    
    # 构建 name -> successors 映射
    name_to_successors: Dict[str, List[str]] = {}
    for edge in edges:
        src_idx = edge.get("source")
        tgt_idx = edge.get("target")
        if src_idx is None or tgt_idx is None:
            continue
        src_name = index_to_name.get(src_idx)
        tgt_name = index_to_name.get(tgt_idx)
        if src_name and tgt_name:
            name_to_successors.setdefault(src_name, []).append(tgt_name)
    
    print(f"Loaded adjacency: {len(name_to_successors)} functions with successors")
    return name_to_successors


def load_random_walk_paths_v1(path: str = RANDOM_WALK_V1_PATH) -> List[Dict[str, Any]]:
    """
    加载 random_walk_paths_v1.json，返回 paths 列表。
    """
    print(f"Loading random walk paths v1 from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    paths = data.get("paths", [])
    print(f"Loaded {len(paths)} paths with turns.")
    return paths


def load_tool_schemas(path: str = TOOL_SCHEMA_SUMMARY_PATH) -> Dict[str, Dict[str, Any]]:
    """
    加载 tool_response_schema_v1.json，返回 tool_name -> schema_info 的映射。
    """
    print(f"Loading tool schemas from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} tools from schema summary.")
    return data


def extract_call_external_api_info(file_path: str) -> Optional[Dict[str, Any]]:
    """
    从文件中提取 call_external_api 函数的信息
    
    Args:
        file_path: 文件路径
        
    Returns:
        dict: 包含 docstring 和源代码的字典，或 None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 AST
        tree = ast.parse(content, filename=file_path)
        
        # 查找 call_external_api 函数
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'call_external_api':
                # 提取 docstring
                docstring = ast.get_docstring(node)
                
                # 提取函数代码
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
                lines = content.split('\n')
                function_code = '\n'.join(lines[start_line:end_line])
                
                return {
                    "docstring": docstring or "",
                    "function_code": function_code
                }
        
        return None
    except Exception as e:
        print(f"Error extracting call_external_api from {file_path}: {e}")
        return None


def extract_source_code_without_call_external_api(file_path: str) -> Optional[str]:
    """
    提取源代码，排除 call_external_api 函数
    
    Args:
        file_path: 文件路径
        
    Returns:
        源代码字符串（不包含 call_external_api 函数）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 AST
        tree = ast.parse(content, filename=file_path)
        
        # 找到 call_external_api 函数的位置
        lines = content.split('\n')
        lines_to_remove = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'call_external_api':
                start_line = node.lineno - 1
                end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
                # 标记要移除的行（包括前面的空行）
                for i in range(max(0, start_line - 1), end_line):
                    lines_to_remove.add(i)
        
        # 移除 call_external_api 函数
        filtered_lines = [line for i, line in enumerate(lines) if i not in lines_to_remove]
        
        return '\n'.join(filtered_lines)
    except Exception as e:
        print(f"Error extracting source code from {file_path}: {e}")
        return None


async def simulate_call_external_api(
    call_external_api_docstring: str,
    source_code_without_api: str,
    function_params: Dict[str, Any],
    func_name: str,
    model: str = None
) -> Dict[str, Any]:
    """
    使用大模型模拟 call_external_api 的输出

    Args:
        call_external_api_docstring: call_external_api 函数的 docstring
        source_code_without_api: 源代码（不包含 call_external_api 函数）
        function_params: 主函数的参数字典
        func_name: 主函数名称
        model: 使用的模型名称（默认使用配置文件中的 simulate_api 模型）

    Returns:
        模拟的 call_external_api 输出字典
    """
    if model is None:
        model = SIMULATE_API_MODEL

    # 解析 docstring 中的 Returns 部分
    returns_section = ""
    if call_external_api_docstring:
        lines = call_external_api_docstring.split('\n')
        in_returns = False
        returns_lines = []
        for line in lines:
            if 'Returns:' in line or 'returns:' in line.lower():
                in_returns = True
                continue
            if in_returns:
                if line.strip() and not line.startswith(' ') and not line.startswith('\t') and ':' in line:
                    if not any(keyword in line.lower() for keyword in ['returns', 'return']):
                        break
                if line.strip():
                    returns_lines.append(line)
        returns_section = '\n'.join(returns_lines)
    
    prompt = f"""You need to simulate the output of a `call_external_api` function based on the following information.

Function Name: {func_name}

Function Parameters (that were passed to the main function):
{json.dumps(function_params, indent=2, ensure_ascii=False)}

Source Code (without call_external_api function):
```python
{source_code_without_api}
```

call_external_api Function Docstring (specifying the return format):
{call_external_api_docstring}

Returns Section:
{returns_section}

Requirements:
1. Generate a realistic output that matches the format specified in the docstring's Returns section
2. The output should be semantically coherent with the source code logic
3. The output should be contextually appropriate based on the function parameters
4. If the Returns section specifies fields with types, ensure the output matches those types
5. Generate realistic values that make sense for the function's purpose
6. The output should be a valid JSON object

Generate ONLY the JSON output that call_external_api would return. No explanations, no markdown, just the JSON object."""

    try:
        completion = await async_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert at simulating external API responses. "
                        "Generate realistic, contextually appropriate outputs based on function documentation and code logic."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.7,
            max_completion_tokens=1024,
        )
        
        content = completion.choices[0].message.content.strip()
        
        # 清理可能的 markdown 代码块标记
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        # 提取 token 使用信息
        usage = completion.usage
        token_usage = {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        }
        
        # 解析 JSON
        try:
            result = json.loads(content)
            # 返回包含结果和 token 信息的字典
            return {
                "result": result,
                "token_usage": token_usage,
            }
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse JSON from LLM output: {e}")
            print(f"Content: {content[:200]}...")
            raise RuntimeError(
                f"Failed to parse JSON from LLM output for {func_name}: {e}. "
                f"Content preview: {content[:200]}"
            ) from e
        
    except Exception as e:
        raise RuntimeError(
            f"Failed to simulate call_external_api for {func_name}: {e}"
        ) from e


def load_function_from_file(func_name: str) -> Tuple[Any, Optional[Dict[str, Any]], Optional[str], Any]:
    """
    从 generated_functions 目录加载函数

    Args:
        func_name: 函数名称

    Returns:
        tuple: (函数对象, call_external_api信息, source_without_api, module)

    Raises:
        RuntimeError: 如果函数文件不存在或加载失败
    """
    # 尝试不同的文件名格式
    # 需要考虑斜杠、连字符、下划线、空格的各种组合，以及 -Tool 后缀
    base_names = [
        func_name,  # 原始名称
        func_name.replace(" ", "-"),  # 空格 → 横线
        func_name.replace("/", "_"),  # 斜杠 → 下划线
        func_name.replace("-", "_"),  # 连字符 → 下划线
        func_name.replace(" ", "-").replace("/", "_"),  # 空格 → 横线，斜杠 → 下划线
        func_name.replace("/", "_").replace("-", "_"),  # 斜杠和连字符都 → 下划线
        func_name.replace(" ", "-").replace("/", "_").replace("-", "_"),  # 空格、斜杠、连字符都处理
        func_name.replace("_", "-"),  # 下划线 → 连字符
    ]

    # 生成 possible_names：base_names + base_names with -Tool suffix
    possible_names = []
    for base in base_names:
        possible_names.append(base)
        possible_names.append(base + "-Tool")  # 尝试添加 -Tool 后缀

    last_error = None
    tried_files = []

    for name in possible_names:
        file_path = os.path.join(GENERATED_FUNCTIONS_DIR, f"{name}.py")
        if os.path.exists(file_path):
            tried_files.append(file_path)
            try:
                # 使用唯一的模块名避免冲突
                module_name = f"generated_func_{name.replace('-', '_').replace('/', '_')}"
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec is None or spec.loader is None:
                    last_error = RuntimeError(f"Failed to create spec for module {module_name} from {file_path}")
                    continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 查找函数 - 增强匹配逻辑
                func = None

                # 1. 尝试精确匹配（标准化：使用与 fix_function_names.py 相同的逻辑）
                # 将所有非字母数字字符替换为 _（保留 Unicode 字母，如中文）
                func_name_normalized = re.sub(r'[^\w]', '_', func_name, flags=re.UNICODE)
                # 移除连续的下划线
                func_name_normalized = re.sub(r'_+', '_', func_name_normalized).strip('_')

                # 尝试多种函数名变体（包括带 _Tool 后缀的）
                func_name_variants = [
                    func_name_normalized,
                    func_name_normalized + "_Tool",  # 尝试添加 _Tool 后缀
                    func_name.replace("/", "_").replace("-", "_"),
                    func_name.replace("-", "_"),
                    func_name.replace("/", "_"),
                    func_name,
                ]

                # 如果函数名以数字开头，也尝试 tool_ 前缀版本
                if func_name_normalized and func_name_normalized[0].isdigit():
                    func_name_variants.append(f'tool_{func_name_normalized}')

                # 尝试所有变体
                for variant in func_name_variants:
                    if hasattr(module, variant):
                        func = getattr(module, variant)
                        if variant != func_name_normalized:
                            print(f"[INFO] Matched function with variant name: {variant}")
                        break

                if func:
                    # 提取 call_external_api 信息
                    api_info = extract_call_external_api_info(file_path)
                    # 提取不包含 call_external_api 的源代码
                    source_without_api = extract_source_code_without_call_external_api(file_path)
                    return func, api_info, source_without_api, module
                else:
                    # 函数不存在于模块中
                    available_funcs = [attr for attr in dir(module) if not attr.startswith('_') and callable(getattr(module, attr))]
                    last_error = RuntimeError(
                        f"Function '{func_name}' (normalized: '{func_name_normalized}') not found in module from {file_path}. "
                        f"Available functions: {available_funcs}"
                    )
            except Exception as e:
                # 重新抛出异常，添加上下文信息
                import traceback
                error_msg = f"Error loading function {func_name} from {file_path}: {str(e)}"
                last_error = RuntimeError(error_msg)
                last_error.__cause__ = e  # 保留原始异常链
    
    # 如果所有尝试都失败了，抛出异常
    if tried_files:
        # 尝试了文件但都失败了
        raise RuntimeError(
            f"Failed to load function '{func_name}' from any of the tried files: {tried_files}. "
            f"Last error: {last_error}"
        ) from last_error
    else:
        # 文件不存在
        raise RuntimeError(
            f"Function file not found for '{func_name}'. "
            f"Tried file names: {[f'{name}.py' for name in possible_names]} "
            f"in directory: {GENERATED_FUNCTIONS_DIR}"
        )


#@log_time_and_tokens("forward_to_fc_params")
async def forward_to_fc_params(
    this_round_query: str,
    last_round_outputs: List[Dict[str, Any]],
    last_round_functions: List[str],
    this_round_functions: List[str],
    tool_schemas: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    根据 this round query 和 last round tool output 以及 this round tool schema，
    通过 LLM 生成 tool calls with params。
    
    Args:
        this_round_query: 当前 round 的用户查询
        last_round_outputs: 上一轮的 tool outputs 列表
        last_round_functions: 上一轮调用的函数列表
        this_round_functions: 当前 round 要调用的函数列表
        tool_schemas: 所有工具的 schema
        
    Returns:
        dict: 包含 think 和 tool_calls 的字典
        {
            "think": "...",
            "tool_calls": [
                {"function": "func1", "parameters": {...}},
                {"function": "func2", "parameters": {...}}
            ]
        }
    """
    # 构建上一轮 tool outputs 信息
    last_round_outputs_text = ""
    if last_round_outputs and last_round_functions:
        output_parts = []
        for func_name, output in zip(last_round_functions, last_round_outputs):
            if output:
                output_parts.append(f"Output from {func_name}:\n{format_tool_output(output)}")
        if output_parts:
            last_round_outputs_text = "\n[Last Round Tool Outputs]\n" + "\n".join(output_parts)
    
    # 构建当前 round 要调用的函数文档
    function_docs = []
    for func_name in this_round_functions:
        meta = tool_schemas.get(func_name)
        function_docs.append(build_function_documentation(func_name, meta))
    functions_doc = "\n".join(function_docs)
    
    prompt = f"""You are a function-calling agent. Based on the user query and available context, generate tool calls with appropriate parameters.

**IMPORTANT: All your responses (think process, explanations) must be in English.**

User Query:
{this_round_query}

Last Round Output
{last_round_outputs_text}

Available Functions to Call:
{functions_doc}

Requirements:
1. First, think about what needs to be done, need to use which parameters and parameters value.(think section)
2. For each function that should be called, extract the appropriate parameters from:
   - The user query
   - The last round tool outputs (if available and relevant)
   - Use reasonable defaults for optional parameters if not specified

3. Make sure all required parameters are provided, but do not provide extra params besides the params listed in the functions_doc parammeters.
4. If a parameter value can be inferred from last round outputs, use that value
5. **IMPORTANT: For each tool call, you must point out which parameters come from the user query or last round outputs in a params_source field. ONLY include parameters that explicitly come from user query or last round output. If ALL parameters are inferred/reasoned by yourself from the tool schema or using defaults, output "EMPTY" for params_source.**
6.Try to generate tool calls for all functions in the list: {', '.join(this_round_functions)} but if you find whatever you try to extract the target tool params from this round query and last_round_tool_output, but the params info can not be extracted, it is lacked, you should explain this in the think process, explain you lack which info, and because that you failed to call the target func. And the tool_call field's value should be empty.


Output format (strictly follow this format):
think: <your thinking process>
tool_call1: <function_name1> with parameters: <JSON object with parameters>
params_source1: <"EMPTY" if all params are inferred/default, OR JSON object mapping parameter names to their source: "user_query" or "last_round_output">
tool_call2: <function_name2> with parameters: <JSON object with parameters>
params_source2: <"EMPTY" if all params are inferred/default, OR JSON object mapping parameter names to their source>
...

Example output 1 (some params from user query):
think: The user wants to search for Airbnb listings in Seattle for 2 adults. The location "Seattle" and adults count "2" are explicitly mentioned in the user query. I will use default values for check_in and check_out dates.
tool_call1: airbnb_search with parameters: {{"location": "Seattle", "adults": 2, "check_in": "2024-01-15", "check_out": "2024-01-20"}}
params_source1: {{"location": "user_query", "adults": "user_query"}}

Example output 2 (all params inferred/default):
think: The user wants to get weather information. No specific location is mentioned, so I will use a default location.
tool_call1: get_weather with parameters: {{"location": "New York", "units": "metric"}}
params_source1: EMPTY
"""

    try:
        completion = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert function-calling agent that extracts parameters "
                        "from user queries and generates appropriate tool calls. "
                        "Follow the output format strictly. "
                        "Always respond in English."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.3,
            max_completion_tokens=1024,
        )
        
        content = completion.choices[0].message.content.strip()
        
        # 提取 token 使用信息
        usage = completion.usage
        token_usage = {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        }
        
        # 解析输出
        result = {
            "think": "",
            "tool_calls": [],
            "token_usage": token_usage,  # 添加 token 使用信息
        }

        lines = content.split('\n')
        current_section = None
        current_tool_call = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 解析 think 部分
            if line.startswith("think:"):
                result["think"] = line[6:].strip()
                current_section = "think"
            elif current_section == "think" and not line.startswith("tool_call") and not line.startswith("params_source"):
                result["think"] += " " + line

            # 解析 tool_call 部分
            elif line.startswith("tool_call"):
                # 格式: tool_call1: function_name with parameters: {...}
                try:
                    # 提取函数名和参数
                    if "with parameters:" in line:
                        parts = line.split("with parameters:")
                        func_part = parts[0].strip()
                        params_part = parts[1].strip()

                        # 提取函数名 (tool_call1: function_name)
                        func_name = func_part.split(":")[-1].strip()

                        # 解析 JSON 参数
                        try:
                            params = json.loads(params_part)
                        except json.JSONDecodeError:
                            # 如果 JSON 解析失败，尝试提取
                            params = {}

                        current_tool_call = {
                            "function": func_name,
                            "parameters": params,
                            "params_source": None  # 默认为 None，等待解析 params_source
                        }
                        result["tool_calls"].append(current_tool_call)
                        current_section = "tool_call"
                except Exception as e:
                    print(f"Warning: Failed to parse tool_call line: {line}, error: {e}")
                    current_tool_call = None

            # 解析 params_source 部分
            elif line.startswith("params_source"):
                # 格式: params_source1: {"param": "user_query"} 或 params_source1: EMPTY
                try:
                    source_part = line.split(":", 1)[1].strip()

                    if source_part.upper() == "EMPTY":
                        params_source = {}
                    else:
                        try:
                            params_source = json.loads(source_part)
                        except json.JSONDecodeError:
                            params_source = {}

                    # 将 params_source 添加到最近的 tool_call
                    if current_tool_call is not None:
                        current_tool_call["params_source"] = params_source
                except Exception as e:
                    print(f"Warning: Failed to parse params_source line: {line}, error: {e}")

        return result

    except Exception as e:
        # 重新抛出异常，让上层 process_single_path_v1 捕获
        raise RuntimeError(
            f"forward_to_fc_params failed: {e}"
        ) from e


#@log_time_and_tokens("execute_function_call")
async def execute_function_call(
    func_name: str,
    parameters: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    执行函数调用并获取 tool output

    Args:
        func_name: 函数名称
        parameters: 函数参数字典（从 forward_to_fc_params 获取）

    Returns:
        tool output 字典（包含 token_usage 字段）或 None
    """
    # 在 SafeExecutionContext 外部导入，避免触发 exec 拦截
    import inspect

    # 加载函数和相关信息（如果失败会抛出异常）
    func, api_info, source_without_api, module = load_function_from_file(func_name)
    
    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }
    
    # 如果函数依赖外部 API，需要替换 call_external_api 的实现
    if api_info and source_without_api and module:
        # 模拟 call_external_api 的输出
        simulated_api_result = await simulate_call_external_api(
            call_external_api_docstring=api_info.get("docstring", ""),
            source_code_without_api=source_without_api,
            function_params=parameters,
            func_name=func_name,
        )
        
        # 提取 token 使用信息
        if isinstance(simulated_api_result, dict) and "token_usage" in simulated_api_result:
            token_usage = simulated_api_result.get("token_usage", {})
            total_token_usage["prompt_tokens"] += token_usage.get("prompt_tokens", 0)
            total_token_usage["completion_tokens"] += token_usage.get("completion_tokens", 0)
            total_token_usage["total_tokens"] += token_usage.get("total_tokens", 0)
            simulated_api_output = simulated_api_result.get("result", {})
        else:
            # 向后兼容：如果没有 token_usage，假设是旧格式
            simulated_api_output = simulated_api_result
        
        # 创建新的 call_external_api 函数
        def mock_call_external_api(tool_name: str) -> Dict[str, Any]:
            """Mock implementation of call_external_api"""
            return simulated_api_output
        
        # 保存原始的 call_external_api（如果有）
        original_call_external_api = getattr(module, 'call_external_api', None)
        
        # 替换模块中的 call_external_api
        setattr(module, 'call_external_api', mock_call_external_api)
        
        try:
            # 在安全执行上下文中执行函数调用
            with SafeExecutionContext():
                # 执行函数调用
                if parameters:
                    result = func(**parameters)
                else:
                    # 尝试无参数调用或使用默认值
                    sig = inspect.signature(func)
                    call_params = {}
                    for param_name, param in sig.parameters.items():
                        if param.default != inspect.Parameter.empty:
                            call_params[param_name] = param.default
                        elif param_name == "tool_name":
                            call_params[param_name] = func_name
                    result = func(**call_params) if call_params else func()
            
            # 恢复原始的 call_external_api（如果有）
            if original_call_external_api:
                setattr(module, 'call_external_api', original_call_external_api)
            else:
                # 如果没有原始函数，删除 mock
                if hasattr(module, 'call_external_api'):
                    delattr(module, 'call_external_api')
            
            final_result = result if isinstance(result, dict) else {"result": result}
            final_result["token_usage"] = total_token_usage
            return final_result
        except Exception as e:
            # 恢复原始的 call_external_api（如果有）
            if original_call_external_api:
                setattr(module, 'call_external_api', original_call_external_api)
            else:
                if hasattr(module, 'call_external_api'):
                    delattr(module, 'call_external_api')
            # 重新抛出异常，添加上下文信息
            raise RuntimeError(
                f"Error executing function {func_name} with parameters {parameters}: {e}"
            ) from e
    
    # 如果没有 call_external_api 或替换失败，正常执行
    try:
        # 在安全执行上下文中执行函数调用
        with SafeExecutionContext():
            # 执行函数调用
            if parameters:
                result = func(**parameters)
            else:
                # 尝试无参数调用或使用默认值
                sig = inspect.signature(func)
                call_params = {}
                for param_name, param in sig.parameters.items():
                    if param.default != inspect.Parameter.empty:
                        call_params[param_name] = param.default
                    elif param_name == "tool_name":
                        call_params[param_name] = func_name
                result = func(**call_params) if call_params else func()
        
        final_result = result if isinstance(result, dict) else {"result": result}
        final_result["token_usage"] = total_token_usage
        return final_result
    except Exception as e:
        # 重新抛出异常，添加上下文信息
        raise RuntimeError(
            f"Error executing function {func_name} with parameters {parameters}: {e}"
        ) from e


def build_function_documentation(
    func_name: str,
    tool_meta: Optional[Dict[str, Any]],
) -> str:
    """
    为单个函数构造文档字符串，包括名称、描述、参数（required/optional）。
    """
    if not tool_meta:
        return f"- {func_name}: (no schema info found)\n"
    
    tool_schema = tool_meta.get("function_schema", {}) or {}
    func = tool_schema.get("function", {}) or {}
    description = func.get("description", "")
    params = (func.get("parameters", {}) or {}).copy()
    
    # 添加output schema 在output_schema_parsed字段里
    output_schema = tool_meta.get("output_schema_parsed", {}) or {}
    output_fields = output_schema.get("fields", []) or []
    
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
    
    # 构建输出字段信息
    output_lines: List[str] = []
    for field in output_fields:
        fname = field.get("name", "")
        ftype = field.get("type", "")
        fdesc = field.get("description", "")
        if fname:
            output_lines.append(f"  - {fname} ({ftype}): {fdesc}")
    
    output_block = "\n".join(output_lines) if output_lines else "  (no structured output schema)"
    
    doc = (
        f"- {func_name}:\n"
        f"  Description: {description}\n"
        f"  Parameters:\n{param_block}\n"
        #f"  Output fields:\n{output_block}\n"
    )
    return doc


def format_tool_output(tool_output: Any, max_length: int = 200) -> str:
    """
    格式化 tool output 为字符串，用于 prompt
    
    Args:
        tool_output: tool output（可以是 dict、list 或其他类型）
        max_length: 每个字段的最大长度
        
    Returns:
        格式化的字符串
    """
    if tool_output is None:
        return "(No output)"
    
    # 处理 list 类型
    if isinstance(tool_output, list):
        if len(tool_output) == 0:
            return "(Empty list)"
        lines = []
        for idx, item in enumerate(tool_output):
            if isinstance(item, dict):
                # 递归处理字典项
                item_lines = []
                for key, value in item.items():
                    value_str = str(value)
                    if len(value_str) > max_length:
                        value_str = value_str[:max_length] + "..."
                    item_lines.append(f"    {key}: {value_str}")
                item_str = "\n".join(item_lines)
                lines.append(f"  [{idx}]:\n{item_str}")
            elif isinstance(item, list):
                # 嵌套列表，递归处理
                nested_str = format_tool_output(item, max_length)
                lines.append(f"  [{idx}]:\n    {nested_str}")
            else:
                # 简单类型
                item_str = str(item)
                if len(item_str) > max_length:
                    item_str = item_str[:max_length] + "..."
                lines.append(f"  [{idx}]: {item_str}")
        return "\n".join(lines)
    
    # 处理 dict 类型
    if isinstance(tool_output, dict):
        lines = []
        for key, value in tool_output.items():
            # 如果值是复杂类型，递归格式化
            if isinstance(value, (dict, list)):
                value_str = format_tool_output(value, max_length)
                # 为嵌套内容添加缩进
                indented_value = "\n".join(f"    {line}" for line in value_str.split("\n"))
                lines.append(f"  - {key}:\n{indented_value}")
            else:
                value_str = str(value)
                if len(value_str) > max_length:
                    value_str = value_str[:max_length] + "..."
                lines.append(f"  - {key}: {value_str}")
        return "\n".join(lines) if lines else "(Empty output)"
    
    # 其他类型，直接转换为字符串
    result_str = str(tool_output)
    if len(result_str) > max_length:
        result_str = result_str[:max_length] + "..."
    return result_str


def parse_llm_output_for_turn(content: str) -> Dict[str, Any]:
    """
    从 LLM 输出中解析 user query、chose func 和 reason
    
    Args:
        content: LLM 的原始输出文本
        
    Returns:
        dict: 包含 "user_query", "chose_func", "reason" 的字典
    """
    result = {
        "user_query": "",
        "chose_func": [],
        "reason": ""
    }
    
    if not content:
        return result
    
    lines = content.split('\n')
    current_field = None
    current_value = []
    
    for line in lines:
        original_line = line
        line = line.strip()
        if not line:
            if current_field and current_value:
                # 保存当前字段的值
                value = ' '.join(current_value).strip()
                if current_field == "user_query":
                    result["user_query"] = value
                elif current_field == "chose_func":
                    # 解析逗号分隔的函数名列表
                    func_names = [f.strip() for f in value.split(',') if f.strip()]
                    result["chose_func"] = func_names
                elif current_field == "reason":
                    result["reason"] = value
                current_value = []
            continue
        
        # 检查是否是字段开始（支持多种变体）
        line_lower = line.lower()
        
        if line_lower.startswith("user query:") or line_lower.startswith("user_query:"):
            if current_field and current_value:
                # 保存之前的字段
                value = ' '.join(current_value).strip()
                if current_field == "user_query":
                    result["user_query"] = value
                elif current_field == "chose_func":
                    func_names = [f.strip() for f in value.split(',') if f.strip()]
                    result["chose_func"] = func_names
                elif current_field == "reason":
                    result["reason"] = value
            
            current_field = "user_query"
            # 提取冒号后的内容
            colon_idx = line.find(':')
            if colon_idx >= 0:
                value_part = line[colon_idx + 1:].strip()
                if value_part:
                    current_value = [value_part]
                else:
                    current_value = []
            else:
                current_value = []
        
        elif line_lower.startswith("chose func:") or line_lower.startswith("chose_func:") or line_lower.startswith("chosen func:"):
            if current_field and current_value:
                # 保存之前的字段
                value = ' '.join(current_value).strip()
                if current_field == "user_query":
                    result["user_query"] = value
                elif current_field == "chose_func":
                    func_names = [f.strip() for f in value.split(',') if f.strip()]
                    result["chose_func"] = func_names
                elif current_field == "reason":
                    result["reason"] = value
            
            current_field = "chose_func"
            # 提取冒号后的内容
            colon_idx = line.find(':')
            if colon_idx >= 0:
                value_part = line[colon_idx + 1:].strip()
                if value_part:
                    current_value = [value_part]
                else:
                    current_value = []
            else:
                current_value = []
        
        elif line_lower.startswith("reason:") or line_lower.startswith("reasoning:"):
            if current_field and current_value:
                # 保存之前的字段
                value = ' '.join(current_value).strip()
                if current_field == "user_query":
                    result["user_query"] = value
                elif current_field == "chose_func":
                    func_names = [f.strip() for f in value.split(',') if f.strip()]
                    result["chose_func"] = func_names
                elif current_field == "reason":
                    result["reason"] = value
            
            current_field = "reason"
            # 提取冒号后的内容
            colon_idx = line.find(':')
            if colon_idx >= 0:
                value_part = line[colon_idx + 1:].strip()
                if value_part:
                    current_value = [value_part]
                else:
                    current_value = []
            else:
                current_value = []
        
        else:
            # 继续当前字段的内容
            if current_field:
                current_value.append(line)
    
    # 处理最后一个字段
    if current_field and current_value:
        value = ' '.join(current_value).strip()
        if current_field == "user_query":
            result["user_query"] = value
        elif current_field == "chose_func":
            func_names = [f.strip() for f in value.split(',') if f.strip()]
            result["chose_func"] = func_names
        elif current_field == "reason":
            result["reason"] = value
    
    # 如果没有解析到任何字段，尝试将整个内容作为 user_query（向后兼容）
    if not result["user_query"] and not result["chose_func"] and not result["reason"]:
        result["user_query"] = content.strip()
    
    return result


def build_prompt_for_turn(
    history_turns: List[List[str]],
    last_round_functions: List[str],
    last_round_outputs: List[Dict[str, Any]],
    candidate_functions: List[str],
    tool_schemas: Dict[str, Dict[str, Any]],
    error_feedback: Optional[str] = None,
) -> str:
    """
    为当前 turn 构造 prompt，基于历史 turns、上一轮函数调用和 tool outputs、候选函数列表。

    支持第一个 turn（没有历史、没有上一轮）的情况。

    Args:
        history_turns: 历史轮次的函数列表
        last_round_functions: 上一轮的函数列表
        last_round_outputs: 上一轮的输出
        candidate_functions: 候选函数列表
        tool_schemas: 工具 schema
        error_feedback: 如果上次生成的 query 执行失败，这里包含错误信息
    """
    is_first_turn = len(history_turns) == 0 and len(last_round_functions) == 0
    
    # 构建历史函数调用信息
    history_parts: List[str] = []
    for round_idx, func_names in enumerate(history_turns, start=1):
        func_docs = []
        for func_name in func_names:
            meta = tool_schemas.get(func_name)
            func_docs.append(build_function_documentation(func_name, meta))
        history_parts.append(f"Round {round_idx}:\n" + "\n".join(func_docs))
    
    # 构建上一轮函数调用信息和 tool outputs
    if is_first_turn:
        last_round_block = "(This is the first round - no previous function calls)"
        last_round_outputs_block = ""
    else:
        last_round_docs: List[str] = []
        for func_name in last_round_functions:
            meta = tool_schemas.get(func_name)
            last_round_docs.append(build_function_documentation(func_name, meta))
        last_round_block = "[Last Round Functions]\n" + "\n".join(last_round_docs)
        
        # 添加 tool outputs
        output_parts = []
        for i, (func_name, output) in enumerate(zip(last_round_functions, last_round_outputs)):
            if output:
                output_parts.append(f"Output from {func_name}:\n{format_tool_output(output)}")
        last_round_outputs_block = "\n[Last Round Tool Outputs]\n" + "\n".join(output_parts) if output_parts else ""
    
    # 构建候选函数字典格式
    candidate_dict: Dict[str, List[str]] = {}
    if is_first_turn:
        candidate_dict = {}
    else:
        for last_func in last_round_functions:
            candidate_dict[last_func] = candidate_functions
    
    candidate_dict_str = json.dumps(candidate_dict, indent=2, ensure_ascii=False) if candidate_dict else "{}"
    
    # 构建候选函数的完整文档
    candidate_docs: List[str] = []
    for func_name in candidate_functions:
        meta = tool_schemas.get(func_name)
        candidate_docs.append(build_function_documentation(func_name, meta))
    candidate_block = "\n".join(candidate_docs)

    # 构建错误反馈信息
    error_feedback_block = ""
    if error_feedback:
        error_feedback_block = f"""
[PREVIOUS ATTEMPT FAILED]
Your previous query attempt resulted in an error during function execution:
{error_feedback}

Please revise your query to fix this issue. Make sure all required parameters are provided with correct values and types.
"""

    if is_first_turn:
        # 第一个 turn 的特殊 prompt
        prompt = f"""Now you are role-playing as a user that involves in a single turn multi step conversation with a function-calling agent. This is the **first step** of the conversation, so there is no previous history. You will be provided with a list of candidate functions that can be called in this step. I would like you to generate the initial user query which calls one or multiple functions from the candidate function list. When calling multiple functions, make sure you call no more than three functions at a single step.

**IMPORTANT: Generate the user query, reason, and all content in English.**
{error_feedback_block}
Rules:
- The query should be concise and natural, without repeating or describing the tool's functionality.
- Do NOT list or paraphrase the tool's capabilities in your query.
- You should NOT mention which functions to use in your query explicitly.
- **CRITICAL: After deciding which functions to use, ensure your query contains concrete values for ALL required parameters.** Your query must be self-contained with all necessary information.
- For dates/times, be specific: use exact dates like "on October 15th, 2024" or "3 days from now" instead of vague terms like "soon" or "later"
- Use no parameters besides the parameters indicated in the required and optional fields of the function documentation.
- Generate a natural, high-level user query that would naturally lead to calling these functions.
- When you decide to use multi functions to call, notice that these functions you choose belong to one step, so among these tool calls there is no absolute params dependency. Probably these tools are relevant, and their inputs should come from the generated query, not params dependency among these.

Candidate Functions Documentation:
{candidate_block}

Output format (strictly follow this format, each field on a separate line):
user query: <your natural language query here>
chose func: <comma-separated list of function names you chose, e.g., "func1, func2">
reason: <explanation of why you chose these functions and how the query relates to them>
"""
    else:
        # 后续 turns 的 prompt（包含 tool outputs）
        prompt = f"""Now you are role-playing as a user that involves in a single turn multi-step conversation with a function-calling agent. You will be given the functions called by the history of this multi-step conversation, indicated by round numbers. The functions called last round start with [Last Round]. You will also be provided with the tool outputs from the last round functions. You will also be provided with a list of candidate functions in a dictionary format where the keys are the functions called last round and values are related and candidate functions that can be called in this round. I would like you to generate the query of this round which calls one or multiple functions from the candidate function list. When calling multiple functions, make sure you call no more than three functions at a single round.

**IMPORTANT: Generate the user query, reason, and all content in English.**
{error_feedback_block}
Rules:
- The new query should be naturally motivated by the last round's tool outputs. The outputs should serve as context or input for the functions to be called in this round.
- **CRITICAL: Your query must enable determining ALL required parameters for the target functions.** When using indirect references to last round outputs:
  * Include identifying details to make references unambiguous: use "the USD amount" (not just "the amount"), "the Seattle location" (not just "the location"), "the resulting product ID" (not just "the result")
  * For dates/times, be specific and calculable: use "7 days ago", "on October 3rd", "3 days before today" instead of vague terms like "last week", "recently", "the other day"
  * Ensure EVERY required parameter of your target function has a corresponding value or clear reference in your query
  * **Example GOOD**: "Convert the calculated USD amount to EUR using the exchange rate from 7 days ago"
    → Has all params: amount (referenced), from_currency (USD mentioned), to_currency (EUR), date (7 days ago)
  * **Example BAD**: "Convert the amount using the rate from last week"
    → Missing: source currency not mentioned, date too vague
- You should NOT mention which functions to use in your query explicitly.
- After deciding which functions to use, double-check: can ALL required parameters be determined from your query? If not, revise your query to include the missing information (either directly or through clear references to last round outputs).
- Use no parameters besides the parameters indicated in the required and optional fields of the function documentation.
- Do not repeat any queries in the conversation history. This means your new query should not call the same function with the same set of parameters as any of the queries in the conversation, even the function exists in the adjacent list.
- The query should be concise and natural, without repeating or describing the tool's functionality.
- DO NOT list or paraphrase the tool's capabilities in your query.
- When you decide to use multi functions to call, notice that these functions you choose belong to one step, so among these tool calls there is no absolute params dependency. Probably these tools are relevant, and their inputs should come from last round output or generated query, not params dependency among these.
Conversation History:
{chr(10).join(history_parts) if history_parts else "(No previous rounds)"}

{last_round_block}
{last_round_outputs_block}

Candidate Functions Dictionary:
{candidate_dict_str}

Candidate Functions Documentation:
{candidate_block}

Output format (strictly follow this format, each field on a separate line):
user query: <your natural language query here>
chose func: <comma-separated list of function names you chose, e.g., "func1, func2">
reason: <explanation of why you chose these functions and how the query relates to them>
"""
    return prompt


#@log_time_and_tokens("generate_query_for_turn")
async def generate_query_for_turn(
    history_turns: List[List[str]],
    last_round_functions: List[str],
    last_round_outputs: List[Dict[str, Any]],
    candidate_functions: List[str],
    tool_schemas: Dict[str, Dict[str, Any]],
    error_feedback: Optional[str] = None,
) -> Dict[str, Any]:
    """
    调用 LLM 为当前 turn 生成用户查询。

    Args:
        history_turns: 历史轮次的函数列表
        last_round_functions: 上一轮的函数列表
        last_round_outputs: 上一轮的输出
        candidate_functions: 候选函数列表
        tool_schemas: 工具 schema
        error_feedback: 如果上次生成的 query 执行失败，这里包含错误信息

    Returns:
        dict: 包含以下字段的字典
            - ok: bool, 是否成功
            - user_query: str, 用户查询文本
            - chose_func: List[str], 选择的函数名列表
            - reason: str, 选择这些函数的原因
            - raw_output: str, LLM 的原始输出（用于调试）
            - error: str, 错误信息（如果失败）
    """
    prompt = build_prompt_for_turn(
        history_turns, last_round_functions, last_round_outputs, candidate_functions, tool_schemas, error_feedback
    )

    try:
        completion = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert user who generates natural language queries "
                        "for a single turn multi-step conversation with a function-calling agent. "
                        "Follow the rules strictly and generate realistic queries. "
                        "Always generate content in English."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=1,
            max_completion_tokens=512,
        )
        
        content = completion.choices[0].message.content.strip()
        
        # 提取 token 使用信息
        usage = completion.usage
        token_usage = {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        }
        
        # 解析 LLM 输出
        parsed = parse_llm_output_for_turn(content)
        
        result = {
            "ok": True,
            "user_query": parsed["user_query"],
            "chose_func": parsed["chose_func"],
            "reason": parsed["reason"],
            "raw_output": content,  # 保留原始输出用于调试
            "token_usage": token_usage,  # 添加 token 使用信息
        }
        return result
    except Exception as e:
        # 重新抛出异常，让上层 process_single_path_v1 捕获
        raise RuntimeError(
            f"generate_query_for_turn failed: {e}"
        ) from e


#@log_time_and_tokens("merge_atomic_queries")
async def merge_atomic_queries(
    atomic_queries: List[str],
    fc_results: List[Dict[str, Any]],
    tool_schemas: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    合并所有 atomic queries 生成最终的 user query

    Args:
        atomic_queries: atomic query 列表
        fc_results: 每个 atomic query 对应的 fc_result 列表
        tool_schemas: 工具 schema

    Returns:
        包含 merged_query 和 token_usage 的字典
    """
    if len(atomic_queries) == 1:
        return {
            "merged_query": atomic_queries[0],
            "token_usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
        }

    # 提取每个 atomic query 的新信息（来自 user_query 的参数）
    # 判断逻辑（判断是否为中间产物）：
    # 情况1: parameters 不为空 + 有来自 user_query 的参数 → 不是中间产物（有新信息，保留）
    # 情况2: parameters 不为空 + 没有来自 user_query 的参数 → 是中间产物（可能跳过，除非是最后一个）
    # 情况3: parameters 为空（get 类操作）→ 不是中间产物（为了增加复杂性，保留）
    queries_with_new_info = []
    for i, (query, fc_result) in enumerate(zip(atomic_queries, fc_results)):
        tool_calls = fc_result.get("tool_calls", [])

        # 收集来自 user_query 的参数信息
        new_params_info = []
        is_intermediate = False  # 标记是否为中间产物

        for tc in tool_calls:
            func_name = tc.get("function", "")
            parameters = tc.get("parameters", {})
            params_source = tc.get("params_source", {})

            # 只保留来自 user_query 的参数
            user_query_params = {}
            for param_name, param_value in parameters.items():
                source = params_source.get(param_name, "")
                if source == "user_query":
                    user_query_params[param_name] = param_value

            # 判断是否为中间产物（对应情况2）：
            # 条件：parameters 不为空 AND 没有来自 user_query 的参数
            # 注意：如果 parameters 为空（情况3：get 类操作），不会被标记为中间产物
            if parameters and not user_query_params:
                is_intermediate = True

            if user_query_params:
                new_params_info.append({
                    "function": func_name,
                    "user_query_params": user_query_params,
                })

        queries_with_new_info.append({
            "step": i + 1,
            "query": query,
            "new_params": new_params_info,
            "is_intermediate": is_intermediate,  # 标记是否为中间产物
        })

    # 获取最后一个 atomic query 的目标（函数调用）
    last_fc_result = fc_results[-1] if fc_results else {}
    last_tool_calls = last_fc_result.get("tool_calls", [])
    last_functions = [tc.get("function", "") for tc in last_tool_calls if tc.get("function")]

    # 构建 queries_text
    queries_details = []
    num_queries = len(queries_with_new_info)

    for i, info in enumerate(queries_with_new_info):
        step = info["step"]
        query = info["query"]
        new_params = info["new_params"]
        is_intermediate = info["is_intermediate"]
        is_last = (i == num_queries - 1)  # 是否为最后一个

        # 如果是中间产物且不是最后一个，直接用占位符替代，不暴露详细信息
        if is_intermediate and not is_last:
            queries_details.append(
                f"Step {step}:\n"
                f"  [INTERMEDIATE STEP - NO DETAILS PROVIDED]"
            )
            continue

        # 对于非中间产物或最后一个步骤，显示详细信息
        # 获取对应的 fc_result 来显示完整的 tool calls
        fc_result = fc_results[i] if i < len(fc_results) else {}
        tool_calls = fc_result.get("tool_calls", [])

        # 构建 tool calls 描述（显示函数名）
        tool_calls_desc = []
        for tc in tool_calls:
            func_name = tc.get("function", "")
            tool_calls_desc.append(f"    - {func_name}")

        tool_calls_text = "\n".join(tool_calls_desc) if tool_calls_desc else "    (no tool calls)"

        # 构建新参数的描述（只显示来自 user_query 的）
        if new_params:
            params_desc = []
            for np in new_params:
                func = np["function"]
                params = np["user_query_params"]
                params_str = ", ".join([f"{k}={v}" for k, v in params.items()])
                params_desc.append(f"    - {params_str}")
            params_text = "\n".join(params_desc)
            new_info_text = f"\n  New information from user query:\n{params_text}"
        else:
            new_info_text = "\n  New information from user query: (none - all parameters inferred or from last round output)"

        # 对于最后一个步骤（final goal）的显示逻辑：
        # - 如果有新信息（new_params 不为空），显示 query 和新信息
        # - 如果没有新信息（new_params 为空），只显示 tool calls，不显示 query（避免泄漏中间输出引用）
        if is_last:
            if new_params:
                # 有新信息，显示 query
                queries_details.append(
                    f"Step {step}:\n"
                    f"  Query: {query}\n"
                    f"  Tool calls:\n{tool_calls_text}"
                    f"{new_info_text}"
                    f"\n  **[FINAL GOAL]**"
                )
            else:
                # 没有新信息，不显示 query
                queries_details.append(
                    f"Step {step}:\n"
                    f"  Tool calls:\n{tool_calls_text}"
                    f"{new_info_text}"
                    f"\n  **[FINAL GOAL]**"
                )
        else:
            # 对于非最后一个步骤，显示完整信息
            queries_details.append(
                f"Step {step}:\n"
                f"  Query: {query}\n"
                f"  Tool calls:\n{tool_calls_text}"
                f"{new_info_text}"
            )

    queries_text = "\n\n".join(queries_details)

    last_functions_text = ", ".join(last_functions) if last_functions else "unknown"

    prompt = f"""You are given a series of atomic queries from a multi-step conversation. Some steps may show:
1. Full details: query text, tool calls, and new information from user
2. Placeholder: [INTERMEDIATE STEP - NO DETAILS PROVIDED] - these are intermediate processing steps
3. [FINAL GOAL] marker: the ultimate goal to accomplish

Your task is to merge the available queries into a single, natural, coherent user query.

**IMPORTANT: Generate the merged query in English.**

**CRITICAL RULES:**
1. IGNORE steps marked as [INTERMEDIATE STEP - NO DETAILS PROVIDED] - they are internal processing steps not relevant to the user
2. The query marked with [FINAL GOAL] is the ultimate goal - MUST be included
3. ONLY use information from steps that show full details
4. ONLY include the NEW INFORMATION from "New information from user query" sections
5. DO NOT invent or infer information from intermediate steps - you don't have access to their details
6. The merged query should read as if the user is making a single, fresh request
7. The ultimate goal is to accomplish the final step's function call: {last_functions_text}
8. Make it natural, concise, and complete - as if a user asked everything in one go

Atomic Queries with Information:
{queries_text}

Final Goal: The merged query should ultimately accomplish calling {last_functions_text},but you need to use these new information from user query and the query that is not skipped to rewrite and merge query

Return ONLY the merged query, no explanations or extra text."""

    try:
        completion = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert at merging multiple queries into a single coherent query. "
                        "You focus on extracting and combining only the NEW information from user queries, "
                        "excluding any references to previous tool outputs or contextual dependencies. "
                        "Always generate content in English."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.3,
            max_completion_tokens=512,
        )

        merged_query = completion.choices[0].message.content.strip()

        # 提取 token 使用信息
        usage = completion.usage
        token_usage = {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        }

        return {
            "merged_query": merged_query,
            "token_usage": token_usage,
        }
    except Exception as e:
        print(f"[ERROR] merge queries failed: {e}")
        # 如果合并失败，返回用 "and" 连接的简单合并
        return {
            "merged_query": " ".join(atomic_queries),
            "token_usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
        }


async def merge_atomic_queries_v1(
    atomic_queries: List[str],
    fc_results: List[Dict[str, Any]],
    tool_schemas: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    合并所有 atomic queries 生成最终的 user query（v1 版本）

    这个版本会先简化每个 atomic query，只保留调用函数的意图和来自 user_query 的参数信息，
    然后再合并这些简化后的 queries。

    Args:
        atomic_queries: atomic query 列表
        fc_results: 每个 atomic query 对应的 fc_result 列表
        tool_schemas: 工具 schema

    Returns:
        包含 merged_query 和 token_usage 的字典
    """
    if len(atomic_queries) == 1:
        return {
            "merged_query": atomic_queries[0],
            "token_usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            },
        }

    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }

    # 第一步：简化每个 atomic query
    simplified_queries = []
    for i, (query, fc_result) in enumerate(zip(atomic_queries, fc_results)):
        tool_calls = fc_result.get("tool_calls", [])

        # 提取函数名和来自 user_query 的参数
        query_info_parts = []
        for tc in tool_calls:
            func_name = tc.get("function", "")
            parameters = tc.get("parameters", {})
            params_source = tc.get("params_source", {})

            # 只保留来自 user_query 的参数
            user_query_params = {}
            for param_name, param_value in parameters.items():
                source = params_source.get(param_name, "")
                if source == "user_query":
                    user_query_params[param_name] = param_value

            if user_query_params:
                params_str = ", ".join([f"{k}={v}" for k, v in user_query_params.items()])
                query_info_parts.append(f"Function: {func_name}, New params: {params_str}")
            else:
                query_info_parts.append(f"Function: {func_name}, New params: (none)")

        query_info = "\n  ".join(query_info_parts) if query_info_parts else "(no tool calls)"

        # 调用 LLM 简化 query
        simplify_prompt = f"""You are given an atomic query from a multi-step conversation. Your task is to simplify this query by:
1. Keeping the intent to call the specified function(s)
2. ONLY including information that comes from NEW parameters (shown below)
3. REMOVING any references to previous results, last round outputs, or context

**IMPORTANT: Generate the simplified query in English.**

Original Query:
{query}

Function and New Parameters Information:
{query_info}

Requirements:
1. Rewrite the query to express the intent to call the function(s)
2. ONLY include the new parameter values shown above
3. Remove phrases like "based on", "using the", "with that", "from the previous", etc.
4. Make it sound natural, as if the user is providing fresh information
5. If there are no new parameters, just express the intent to call the function without specific values

Return ONLY the simplified query, no explanations."""

        try:
            completion = await async_client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert at simplifying queries by removing contextual references "
                            "and keeping only new information. Always generate content in English."
                        ),
                    },
                    {"role": "user", "content": simplify_prompt},
                ],
                stream=False,
                temperature=0.3,
                max_completion_tokens=256,
            )

            simplified = completion.choices[0].message.content.strip()
            simplified_queries.append(simplified)

            # 累加 token 使用
            usage = completion.usage
            if usage:
                total_token_usage["prompt_tokens"] += usage.prompt_tokens
                total_token_usage["completion_tokens"] += usage.completion_tokens
                total_token_usage["total_tokens"] += usage.total_tokens

        except Exception as e:
            print(f"[ERROR] Failed to simplify query {i}: {e}")
            # 如果简化失败，使用原始 query
            simplified_queries.append(query)

    # 第二步：合并简化后的 queries
    # 获取最后一个函数调用作为目标
    last_fc_result = fc_results[-1] if fc_results else {}
    last_tool_calls = last_fc_result.get("tool_calls", [])
    last_functions = [tc.get("function", "") for tc in last_tool_calls if tc.get("function")]
    last_functions_text = ", ".join(last_functions) if last_functions else "unknown"

    # 构建简化后的 queries 文本
    simplified_queries_text = "\n".join([f"Step {i+1}: {q}" for i, q in enumerate(simplified_queries)])

    merge_prompt = f"""You are given a series of simplified atomic queries. Each query has been cleaned to only contain:
1. The intent to call a specific function
2. NEW information (not from previous results)

Your task is to merge these simplified queries into a single, natural, coherent user query.

**IMPORTANT: Generate the merged query in English.**

**CRITICAL RULES:**
1. Combine all the simplified queries into one natural request
2. Maintain the intent to accomplish the final goal: {last_functions_text}
3. Keep all the NEW information from the simplified queries
4. Make it flow naturally as if the user asked everything in one request
5. The merged query should be concise and complete
6. Do NOT add back any contextual references that were removed during simplification

Simplified Queries:
{simplified_queries_text}

Final Goal: The merged query should ultimately accomplish calling {last_functions_text}

Return ONLY the merged query, no explanations or extra text."""

    try:
        completion = await async_client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert at merging multiple simplified queries into a single coherent query. "
                        "Always generate content in English."
                    ),
                },
                {"role": "user", "content": merge_prompt},
            ],
            stream=False,
            temperature=0.3,
            max_completion_tokens=512,
        )

        merged_query = completion.choices[0].message.content.strip()

        # 累加 token 使用
        usage = completion.usage
        if usage:
            total_token_usage["prompt_tokens"] += usage.prompt_tokens
            total_token_usage["completion_tokens"] += usage.completion_tokens
            total_token_usage["total_tokens"] += usage.total_tokens

        return {
            "merged_query": merged_query,
            "token_usage": total_token_usage,
            "simplified_queries": simplified_queries,  # 额外返回简化后的 queries 用于调试
        }
    except Exception as e:
        print(f"[ERROR] merge simplified queries failed: {e}")
        # 如果合并失败，返回用空格连接的简化 queries
        return {
            "merged_query": " ".join(simplified_queries),
            "token_usage": total_token_usage,
            "simplified_queries": simplified_queries,
        }


async def process_single_path_v1(
    path: Dict[str, Any],
    tool_schemas: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    处理单个 path（v1 版本），生成所有 atomic queries 和最终 merged query

    这个版本专门用于处理没有 turns 结构的 path，直接从 node_names 列表中读取节点，
    将每个节点（函数）当作一个独立的 turn 来处理。
    
    支持处理带有 merge 结构的路径：
    - 如果 path 包含 merge_info，会遍历 merge 后的所有节点（包括 merge 添加的节点）
    - 保留 merge 相关信息在返回结果中

    Args:
        path: path 字典，包含 node_names 列表而非 turns 结构
            如果包含 merge_info，则 node_names 是 merge 后的路径
        tool_schemas: 工具 schema

    Returns:
        包含所有 atomic queries 和最终 query 的字典，如果 path 有 merge 信息，也会包含 merge 相关字段
    """
    # 检查是否有 merge 信息（判断 num_merges > 0）
    has_merge_info = path.get("num_merges", 0) > 0
    
    # 直接从 path 中获取所有 node 名称（如果是 merge 后的路径，这里就是 merge 后的所有节点）
    node_names = path.get("node_names", [])
    if len(node_names) < 1:
        return {"error": "No nodes in path"}

    # 提取对应的 tool schema（包括 merge 后的所有节点）
    nodes_tool_schema = {}
    for node_name in node_names:
        if node_name in tool_schemas:
            nodes_tool_schema[node_name] = tool_schemas[node_name]

    atomic_queries: List[str] = []
    all_tool_outputs: List[Dict[str, Any]] = []
    all_fc_results: List[Dict[str, Any]] = []  # 存储所有 forward_to_fc_params 的结果
    history_turns: List[List[str]] = []
    last_round_functions: List[str] = []
    last_round_outputs: List[Dict[str, Any]] = []
    unmatched_tool_calls: List[Dict[str, Any]] = []  # 记录未匹配的工具调用

    # 统计该 path 内所有 LLM 调用的 token 使用情况
    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }

    # 为每个节点（当作一个 turn）生成 atomic query 并执行函数调用
    # 如果是 merge 后的路径，这里会遍历所有节点（包括 merge 添加的节点）
    # 对于有 merge 的原始节点，会将原始节点和 merge 添加的节点一起处理
    processed_indices = set()  # 记录已处理的节点索引（用于跳过 merge 添加的节点）
    
    for turn_idx, node_name in enumerate(node_names):
        # 如果这个节点已经被处理过（作为 merge 的一部分），跳过
        if turn_idx in processed_indices:
            continue
        
        # 初始化 current_turn_functions，包含当前节点
        current_turn_functions = [node_name]
        
        # 如果是 merge 路径，检查当前节点是否有 merge，如果有则将 merge 的节点也加入
        if has_merge_info:
            merge_info = path.get("merge_info", [])
            original_path_names = path.get("original_path_names", [])
            node_indices = path.get("node_indices", [])
            
            # 检查当前节点是否是原始路径中的节点，且是否有 merge
            if node_name in original_path_names:
                # 找到这个节点在 merge_info 中的信息
                for merge_item in merge_info:
                    if merge_item.get("node_name") == node_name and merge_item.get("merged"):
                        # 这个节点有 merge，检查下一个节点是否是 merge 的候选节点
                        merged_candidate = merge_item.get("merged_candidate")
                        if merged_candidate and turn_idx + 1 < len(node_names):
                            next_node_name = node_names[turn_idx + 1]
                            if next_node_name == merged_candidate:
                                # 下一个节点是 merge 的候选节点，将其加入 current_turn_functions
                                current_turn_functions.append(next_node_name)
                                # 标记下一个节点为已处理
                                processed_indices.add(turn_idx + 1)
                                break
            # 如果当前节点是 merge 添加的节点，检查前一个节点是否是原始节点且有 merge
            elif node_name not in original_path_names and turn_idx > 0:
                # 检查前一个节点是否是原始节点且有 merge，且 merge 的候选节点是当前节点
                prev_node_name = node_names[turn_idx - 1]
                if prev_node_name in original_path_names:
                    for merge_item in merge_info:
                        if (merge_item.get("node_name") == prev_node_name and 
                            merge_item.get("merged") and 
                            merge_item.get("merged_candidate") == node_name):
                            # 前一个节点应该已经处理了这个节点（在之前的迭代中），跳过
                            # 但为了安全起见，如果当前节点还没被标记为已处理，则标记并跳过
                            if turn_idx not in processed_indices:
                                processed_indices.add(turn_idx)
                            continue

        if turn_idx == 0:
            # 第一个 turn：没有历史，没有上一轮
            history_turns_for_prompt = []
            last_round_functions_for_prompt = []
            last_round_outputs_for_prompt = []
        else:
            # 后续 turns：有历史，有上一轮
            last_round_functions_for_prompt = last_round_functions
            history_turns_for_prompt = history_turns[:turn_idx]
            last_round_outputs_for_prompt = all_tool_outputs[-len(last_round_functions_for_prompt):] if all_tool_outputs and last_round_functions_for_prompt else []

        # ===== 重试机制：如果执行失败，重新生成 query =====
        max_retries = 1  # 最多重试1次
        error_feedback = None

        for retry_attempt in range(max_retries + 1):
            if retry_attempt > 0:
                print(f"[RETRY {retry_attempt}/{max_retries}] Regenerating query for turn {turn_idx} due to error")

            # 生成 atomic query
            result = await generate_query_for_turn(
                history_turns_for_prompt,
                last_round_functions_for_prompt,
                last_round_outputs_for_prompt,
                current_turn_functions,
                tool_schemas,
                error_feedback=error_feedback,  # 传递错误信息
            )

            # 现在 generate_query_for_turn 失败时会直接抛出异常，不需要检查 ok 字段
            atomic_query = result.get("user_query", "")
            if not atomic_query:
                # 向后兼容：如果没有解析到 user_query，尝试使用 raw_output
                atomic_query = result.get("raw_output", "")

            # 累加 generate_query_for_turn 的 token 使用
            tq = result.get("token_usage", {})
            total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
            total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
            total_token_usage["total_tokens"] += tq.get("total_tokens", 0)

            # 使用解析出的 chose_func 作为 this_round_functions，如果为空则回退到 current_turn_functions
            chose_func = result.get("chose_func", [])
            this_round_functions = chose_func if chose_func else current_turn_functions

            # 使用 forward_to_fc_params 生成 tool calls with params
            fc_result = await forward_to_fc_params(
                this_round_query=atomic_query,
                last_round_outputs=last_round_outputs_for_prompt,
                last_round_functions=last_round_functions_for_prompt,
                this_round_functions=this_round_functions,
                tool_schemas=tool_schemas,
            )
            # 累加 forward_to_fc_params 的 token 使用
            tq = fc_result.get("token_usage", {})
            total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
            total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
            total_token_usage["total_tokens"] += tq.get("total_tokens", 0)

            # 执行函数调用获取 tool outputs
            turn_outputs = []
            tool_calls = fc_result.get("tool_calls") or []
            cot = fc_result.get("think", "")
            valid_called_funcs: Set[str] = set()
            for tc in tool_calls:
                if not isinstance(tc, dict):
                    continue
                fn = tc.get("function")
                if fn:
                    valid_called_funcs.add(fn)

            expected_funcs: Set[str] = set(this_round_functions or [])
            # 只要两个集合不相同，就直接 raise error
            if expected_funcs != valid_called_funcs:
                error_msg = (
                    f"Function mismatch error:\n"
                    f"Expected functions: {sorted(expected_funcs)}\n"
                    f"Actually called functions: {sorted(valid_called_funcs)}\n"
                    f"\nYour previous reasoning (think process):\n{cot}\n"
                )
                if retry_attempt < max_retries:
                    error_feedback = error_msg
                    print(f"[WARN] Function mismatch at turn {turn_idx}, node {node_name}")
                    continue  # 重试
                else:
                    raise RuntimeError(
                        f"[fc_result mismatch] turn_idx={turn_idx}, node={node_name}, "
                        f"expected_funcs={sorted(expected_funcs)}, "
                        f"valid_called_funcs={sorted(valid_called_funcs)}, "
                        f"llm_explain={cot}"
                    )  # 超过重试次数，抛出异常

            try:
                # 尝试执行所有函数调用
                for tool_call in tool_calls:
                    func_name = tool_call.get("function")
                    parameters = tool_call.get("parameters", {})

                    if func_name in this_round_functions:
                        # execute_function_call 现在会在失败时抛出异常，不再返回 None
                        output_result = await execute_function_call(func_name, parameters)
                        # 提取 token_usage 并从 output_result 中移除
                        if isinstance(output_result, dict):
                            # 累加 execute_function_call / simulate_call_external_api 的 token 使用
                            tq = output_result.get("token_usage", {})
                            total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
                            total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
                            total_token_usage["total_tokens"] += tq.get("total_tokens", 0)
                            # 移除 token_usage 字段，剩余部分作为 output
                            output = {k: v for k, v in output_result.items() if k != "token_usage"}
                        else:
                            output = output_result
                        turn_outputs.append(output)
                        all_tool_outputs.append(output)
                    else:
                        print(f"Warning: Tool call function {func_name} not in this round functions")
                        # 记录未匹配的工具调用信息
                        unmatched_tool_calls.append({
                            "turn_idx": turn_idx,
                            "function": func_name,
                            "parameters": parameters,
                            "this_round_functions": this_round_functions,
                            "atomic_query": atomic_query,
                        })

                # 执行成功，跳出重试循环
                atomic_queries.append(atomic_query)
                all_fc_results.append(fc_result)
                break

            except Exception as e:
                # 执行函数调用失败
                if retry_attempt < max_retries:
                    error_feedback = (
                        f"Function execution failed with error:\n{str(e)}\n"
                        f"\nYour previous reasoning (think process):\n{cot}\n"
                        f"\nGenerated tool calls:\n"
                    )
                    # 添加生成的工具调用信息
                    for tc in tool_calls:
                        func = tc.get("function", "unknown")
                        params = tc.get("parameters", {})
                        error_feedback += f"  - {func}({json.dumps(params, ensure_ascii=False)})\n"

                    print(f"[WARN] Function execution failed at turn {turn_idx}: {str(e)}")
                    continue  # 重试
                else:
                    # 超过重试次数，抛出异常
                    raise

        # 更新历史
        history_turns.append(this_round_functions)
        last_round_functions = this_round_functions
        last_round_outputs = turn_outputs

    
    result = {
        "path_info": {
            "start_index": path.get("start_index"),
            "start_name": path.get("start_name"),
            "walk_id": path.get("walk_id"),
        },
        "atomic_queries": atomic_queries,
        "fc_results": all_fc_results,  # 包含 think 和 tool_calls
        "tool_outputs": all_tool_outputs,
        "token_usage": total_token_usage,
        "unmatched_tool_calls": unmatched_tool_calls,  # 未匹配的工具调用列表
        "unmatched_count": len(unmatched_tool_calls),  # 未匹配的工具调用数量统计
        "nodes_tool_schema": nodes_tool_schema,  # path 中所有 node 的 tool schema
    }
    
    # 如果 path 包含 merge 信息，保留 merge 相关字段
    if has_merge_info:
        result["merge_info"] = {
            "has_merge": True,
            "num_merges": path.get("num_merges", 0),
            "original_path": path.get("original_path", []),
            "original_path_names": path.get("original_path_names", []),
            "merged_path": path.get("node_indices", []),
            "merged_path_names": path.get("node_names", []),
            "merge_info": path.get("merge_info", []),
        }
    else:
        result["merge_info"] = {
            "has_merge": False,
        }
    
    return result


async def process_single_path(
    path: Dict[str, Any],
    tool_schemas: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    处理单个 path，生成所有 atomic queries 和最终 merged query

    Args:
        path: path 字典
        tool_schemas: 工具 schema

    Returns:
        包含所有 atomic queries 和最终 query 的字典
    """
    turns = path.get("turns", [])
    if len(turns) < 1:
        return {"error": "No turns in path"}

    # 直接从 path 中获取所有 node 名称，并提取对应的 tool schema
    all_nodes_in_path = path.get("node_names", [])
    nodes_tool_schema = {}
    for node_name in all_nodes_in_path:
        if node_name in tool_schemas:
            nodes_tool_schema[node_name] = tool_schemas[node_name]
    
    atomic_queries: List[str] = []
    all_tool_outputs: List[Dict[str, Any]] = []
    all_fc_results: List[Dict[str, Any]] = []  # 存储所有 forward_to_fc_params 的结果
    history_turns: List[List[str]] = []
    last_round_functions: List[str] = []
    last_round_outputs: List[Dict[str, Any]] = []
    unmatched_tool_calls: List[Dict[str, Any]] = []  # 记录未匹配的工具调用
    # 统计该 path 内所有 LLM 调用的 token 使用情况
    total_token_usage = {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }
    
    # 为每个 step 生成 atomic query 并执行函数调用
    for turn_idx, turn in enumerate(turns):
        current_turn_functions = turn.get("node_names", [])
        
        if turn_idx == 0:
            # 第一个 turn：没有历史，没有上一轮
            history_turns_for_prompt = []
            last_round_functions_for_prompt = []
            last_round_outputs_for_prompt = []
        else:
            # 后续 turns：有历史，有上一轮
            # 使用上一轮实际使用的函数列表（可能是从 LLM 解析出的 chose_func）
            last_round_functions_for_prompt = last_round_functions
            history_turns_for_prompt = history_turns[:turn_idx]
            last_round_outputs_for_prompt = all_tool_outputs[-len(last_round_functions_for_prompt):] if all_tool_outputs and last_round_functions_for_prompt else []
        
        # 生成 atomic query
        result = await generate_query_for_turn(
            history_turns_for_prompt,
            last_round_functions_for_prompt,
            last_round_outputs_for_prompt,
            current_turn_functions,
            tool_schemas,
        )
        
        if not result.get("ok"):
            print(f"Warning: Failed to generate query for turn {turn_idx}")
            continue
        
        atomic_query = result.get("user_query", "")
        if not atomic_query:
            # 向后兼容：如果没有解析到 user_query，尝试使用 raw_output
            atomic_query = result.get("raw_output", "")
        
        atomic_queries.append(atomic_query)
        # 累加 generate_query_for_turn 的 token 使用
        tq = result.get("token_usage", {})
        total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
        total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
        total_token_usage["total_tokens"] += tq.get("total_tokens", 0)
        
        # 使用解析出的 chose_func 作为 this_round_functions，如果为空则回退到 current_turn_functions
        chose_func = result.get("chose_func", [])
        this_round_functions = chose_func if chose_func else current_turn_functions
        
        # 使用 forward_to_fc_params 生成 tool calls with params
        fc_result = await forward_to_fc_params(
            this_round_query=atomic_query,
            last_round_outputs=last_round_outputs_for_prompt,
            last_round_functions=last_round_functions_for_prompt,
            this_round_functions=this_round_functions,
            tool_schemas=tool_schemas,
        )
        all_fc_results.append(fc_result)
        # 累加 forward_to_fc_params 的 token 使用
        tq = fc_result.get("token_usage", {})
        total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
        total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
        total_token_usage["total_tokens"] += tq.get("total_tokens", 0)
        
        # 执行函数调用获取 tool outputs
        turn_outputs = []
        # check fc_result 的 tool_calls 字段是否和 this_round_functions 能 match，
        # 如果完全无法 match（没有有效的 tool_call，或者出现不在 this_round_functions 里的函数），
        # 最简单的处理方式：直接把这个 path 的 process 标记为失败（抛异常，由上层统计为 error path）
        tool_calls = fc_result.get("tool_calls") or []
        cot = fc_result.get("think","")
        valid_called_funcs: Set[str] = set()
        for tc in tool_calls:
            if not isinstance(tc, dict):
                continue
            fn = tc.get("function")
            if fn:
                valid_called_funcs.add(fn)
        
        expected_funcs: Set[str] = set(this_round_functions or [])
        # 只要两个集合不相同，就直接 raise error
        if expected_funcs != valid_called_funcs:
            raise RuntimeError(
                f"[fc_result mismatch] turn_idx={turn_idx}, "
                f"expected_funcs={sorted(expected_funcs)}, "
                f"valid_called_funcs={sorted(valid_called_funcs)}"
                f"llm_explain={cot}"
            )
        
        for tool_call in tool_calls:
            func_name = tool_call.get("function")
            parameters = tool_call.get("parameters", {})
            
            if func_name in this_round_functions:
                # execute_function_call 现在会在失败时抛出异常，不再返回 None
                output_result = await execute_function_call(func_name, parameters)
                # 提取 token_usage 并从 output_result 中移除
                if isinstance(output_result, dict):
                    # 累加 execute_function_call / simulate_call_external_api 的 token 使用
                    tq = output_result.get("token_usage", {})
                    total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
                    total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
                    total_token_usage["total_tokens"] += tq.get("total_tokens", 0)
                    # 移除 token_usage 字段，剩余部分作为 output
                    output = {k: v for k, v in output_result.items() if k != "token_usage"}
                else:
                    output = output_result
                turn_outputs.append(output)
                all_tool_outputs.append(output)
            else:
                print(f"Warning: Tool call function {func_name} not in this round functions")
                # 记录未匹配的工具调用信息
                unmatched_tool_calls.append({
                    "turn_idx": turn_idx,
                    "function": func_name,
                    "parameters": parameters,
                    "this_round_functions": this_round_functions,
                    "atomic_query": atomic_query,
                })
        
        # 更新历史
        history_turns.append(this_round_functions)
        last_round_functions = this_round_functions
        last_round_outputs = turn_outputs
    
    # 合并所有 atomic queries 生成最终 query,需要把
    merge_result = await merge_atomic_queries(atomic_queries, tool_schemas)
    if isinstance(merge_result, dict):
        final_query = merge_result.get("merged_query", "")
        # 累加 merge_atomic_queries 的 token 使用
        tq = merge_result.get("token_usage", {})
        total_token_usage["prompt_tokens"] += tq.get("prompt_tokens", 0)
        total_token_usage["completion_tokens"] += tq.get("completion_tokens", 0)
        total_token_usage["total_tokens"] += tq.get("total_tokens", 0)
    else:
        final_query = merge_result
    
    return {
        "path_info": {
            "start_index": path.get("start_index"),
            "start_name": path.get("start_name"),
            "walk_id": path.get("walk_id"),
        },
        "atomic_queries": atomic_queries,
        "final_query": final_query,
        "fc_results": all_fc_results,  # 包含 think 和 tool_calls
        "tool_outputs": all_tool_outputs,
        "token_usage": total_token_usage,
        "unmatched_tool_calls": unmatched_tool_calls,  # 未匹配的工具调用列表
        "unmatched_count": len(unmatched_tool_calls),  # 未匹配的工具调用数量统计
        "nodes_tool_schema": nodes_tool_schema,  # path 中所有 node 的 tool schema
    }


async def generate_queries_for_all_turns(
    max_paths: Optional[int] = None,
    batch_size: int = 5,
    resume: bool = False,
    early_stop_batches: int = 3,
) -> None:
    """
    主入口：为所有 paths 生成 atomic queries 和最终 merged queries。

    Args:
        max_paths: 最多处理多少个 paths（用于测试）
        batch_size: 并发批次大小
        resume: 是否启用断点续传（跳过已生成的 paths）
        early_stop_batches: 连续多少个 batch 全部失败后停止（0 表示不启用早停）
    """
    paths = load_random_walk_paths_v1(RANDOM_WALK_V1_PATH)
    tool_schemas = load_tool_schemas(TOOL_SCHEMA_SUMMARY_PATH)


    if max_paths is not None and max_paths < len(paths):
        paths = paths[:max_paths]

    os.makedirs(os.path.dirname(OUTPUT_QUERIES_PATH), exist_ok=True)

    # 断点续传：读取已处理的 paths
    successfully_processed_path_ids = set()

    if resume and os.path.exists(OUTPUT_QUERIES_PATH):
        print(f"\n🔄 Resume mode enabled, reading existing results from {OUTPUT_QUERIES_PATH}...")
        try:
            with open(OUTPUT_QUERIES_PATH, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        path_info = record.get("path_info", {})
                        # 使用 start_index 和 walk_id 作为唯一标识
                        start_idx = path_info.get("start_index")
                        walk_id = path_info.get("walk_id")
                        if start_idx is not None and walk_id is not None:
                            path_id = (start_idx, walk_id)
                            # 文件中只有成功的记录（失败的不会被写入）
                            successfully_processed_path_ids.add(path_id)
                    except json.JSONDecodeError:
                        continue

            print(f"   Found {len(successfully_processed_path_ids)} successfully processed paths")

            # 过滤掉成功处理的 paths
            original_count = len(paths)
            paths = [
                p for p in paths
                if (p.get("start_index"), p.get("walk_id")) not in successfully_processed_path_ids
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

    print(f"\nFound {len(paths)} paths to process.")
    print(f"Output -> {OUTPUT_QUERIES_PATH}\n")

    # 文件写入模式：
    # - 如果是 resume 模式，使用追加模式（a）
    # - 否则，使用覆盖模式（w）
    file_mode = "a" if resume else "w"
    if file_mode == "a":
        print(f"📝 Appending to existing file: {OUTPUT_QUERIES_PATH}\n")

    with open(OUTPUT_QUERIES_PATH, file_mode, encoding="utf-8") as f:
        total = len(paths)
        overall_tokens = 0
        total_errors = 0
        consecutive_failed_batches = 0  # 连续失败的 batch 计数
        num_batches = (total + batch_size - 1) // batch_size

        # 使用 tqdm 显示整体进度（按 path 数量）
        for batch_idx, start in enumerate(tqdm(range(0, total, batch_size),
                                               total=num_batches,
                                               desc="Processing paths",
                                               unit="batch"), start=1):
            batch = paths[start: start + batch_size]
            print(
                f"\n[Batch {batch_idx}/{num_batches}] "
                f"Processing paths {start + 1}-{start + len(batch)} "
                f"out of {total}..."
            )

            batch_start_time = time.time()
            batch_tokens = 0
            batch_errors = 0  # 当前 batch 的错误数

            tasks = [
                process_single_path_v1(path, tool_schemas)
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
                    # 累加该 path 的 token 使用
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
    print(f"\nAll paths processed, queries saved to: {OUTPUT_QUERIES_PATH}")


def main() -> None:
    """
    命令行入口。
    """
    import argparse

    parser = argparse.ArgumentParser(description="Generate queries for all turns in random walk paths")
    parser.add_argument('--max-paths', type=int, default=None,
                        help='Maximum number of paths to process (for testing)')
    parser.add_argument('--batch-size', type=int, default=10,
                        help='Batch size for parallel processing')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from previous run (skip already processed paths)')
    parser.add_argument('--early-stop', type=int, default=1,
                        help='Stop after N consecutive batches with all failures (0 to disable)')
    parser.add_argument('--test', action='store_true',
                        help='Test mode: process only 5 paths')

    args = parser.parse_args()

    if args.test:
        print("🧪 Running in TEST mode (5 paths only)...")
        args.max_paths = 5

    asyncio.run(generate_queries_for_all_turns(
        max_paths=args.max_paths,
        batch_size=args.batch_size,
        resume=args.resume,
        early_stop_batches=args.early_stop,
    ))


if __name__ == "__main__":
    main()
