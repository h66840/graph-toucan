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

def call_external_api(tool_name: str) -> Dict[str, Any]:
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
    api_result = call_external_api("python_sandbox")
    
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