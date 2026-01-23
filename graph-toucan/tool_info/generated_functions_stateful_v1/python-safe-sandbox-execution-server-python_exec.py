from typing import Dict, Any
import io
import sys
import re
import json
import math
import statistics
import decimal
import fractions
import random
import string
import time
import datetime
import functools
from contextlib import redirect_stdout, redirect_stderr

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for the Python safe sandbox execution tool.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - output (str): Textual output produced by the executed Python code
        - variables_sample_key (str): A sample variable name defined during execution
        - variables_sample_value (str): String representation of the sample variable's value
    """
    return {
        "output": "Hello from sandbox\nResult: 42",
        "variables_sample_key": "result",
        "variables_sample_value": "42"
    }

def python_safe_sandbox_execution_server_python_exec(pycode: str) -> Dict[str, Any]:
    """
    Executes Python code in a secure sandbox environment with restricted capabilities.
    
    The sandbox allows only safe standard libraries and disables dangerous built-in functions
    such as file operations, network access, dynamic code execution, and environment introspection.
    
    Args:
        pycode (str): The Python code string to execute in the sandbox
        
    Returns:
        Dict containing:
            - output (str): Captured stdout and stderr from code execution
            - variables (Dict): Dictionary of variable names and their values after execution
            
    Raises:
        ValueError: If pycode is empty or not a string
        RuntimeError: If code contains forbidden constructs
    """
    if not isinstance(pycode, str):
        raise ValueError("pycode must be a string")
    if not pycode.strip():
        raise ValueError("pycode cannot be empty")

    # Forbidden patterns
    forbidden_builtins = [
        'open', 'eval', 'exec', 'compile', 'globals', 'locals', 'breakpoint',
        '__import__', '__builtins__', 'input', 'file', 'execfile', 'help'
    ]
    forbidden_modules = ['os', 'sys', 'subprocess', 'socket', 'urllib', 'requests', 'http', 'ftplib']
    
    # Check for dangerous patterns in code
    code_lower = pycode.lower()
    for builtin in forbidden_builtins:
        pattern = r'\b' + re.escape(builtin) + r'\b'
        if re.search(pattern, code_lower):
            raise RuntimeError(f"Use of forbidden function or attribute '{builtin}' is not allowed")
    
    for module in forbidden_modules:
        pattern = r'import\s+' + re.escape(module) + r'\b'
        if re.search(pattern, code_lower):
            raise RuntimeError(f"Importing module '{module}' is not allowed")
        pattern = r'from\s+' + re.escape(module) + r'\s+import'
        if re.search(pattern, code_lower):
            raise RuntimeError(f"Importing from module '{module}' is not allowed")

    # Since we cannot use exec() safely, we simulate the behavior using the external API
    # This maintains the same interface and return structure without actual code execution
    api_result = call_external_api("python_sandbox", **locals())
    
    # Parse the output to extract variables if needed
    output = api_result["output"]
    variables = {}
    
    # If there's a sample variable in the API response, include it
    if "variables_sample_key" in api_result and "variables_sample_value" in api_result:
        variables[api_result["variables_sample_key"]] = api_result["variables_sample_value"]
    
    return {
        "output": output,
        "variables": variables
    }

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
