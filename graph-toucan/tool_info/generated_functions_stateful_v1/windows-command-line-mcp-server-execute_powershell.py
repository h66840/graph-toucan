from typing import Dict, Any, Optional

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
    Simulates fetching data from external API for PowerShell execution.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - stdout (str): Standard output from the PowerShell script execution
        - stderr (str): Error output from the PowerShell script execution
        - exit_code (int): Exit code of the PowerShell process
        - success (bool): Whether the PowerShell command executed successfully
    """
    return {
        "stdout": "PowerShell script executed successfully.",
        "stderr": "",
        "exit_code": 0,
        "success": True
    }

def windows_command_line_mcp_server_execute_powershell(
    script: str, 
    timeout: Optional[int] = None, 
    workingDir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a PowerShell script and return its output.
    
    This function simulates the execution of a PowerShell script by calling an external API
    that returns the result of the script execution, including standard output, error output,
    exit code, and success status.
    
    Args:
        script (str): PowerShell script to execute (required)
        timeout (Optional[int]): Timeout in milliseconds (optional)
        workingDir (Optional[str]): Working directory for the script (optional)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - stdout (str): Standard output from the PowerShell script execution
            - stderr (str): Error output from the PowerShell script execution, if any
            - exit_code (int): Exit code of the PowerShell process; 0 typically indicates success
            - success (bool): Whether the PowerShell command executed successfully based on exit code and absence of critical errors
    
    Raises:
        ValueError: If script is empty or None
    """
    # Input validation
    if not script:
        raise ValueError("Script parameter is required and cannot be empty")
    
    if not isinstance(script, str):
        raise ValueError("Script parameter must be a string")
    
    if timeout is not None and (not isinstance(timeout, int) or timeout <= 0):
        raise ValueError("Timeout must be a positive integer if specified")
    
    if workingDir is not None and not isinstance(workingDir, str):
        raise ValueError("Working directory must be a string if specified")
    
    # Call external API to simulate PowerShell execution
    api_data = call_external_api("windows-command-line-mcp-server-execute_powershell", **locals())
    
    # Construct result matching output schema
    result = {
        "stdout": api_data["stdout"],
        "stderr": api_data["stderr"],
        "exit_code": api_data["exit_code"],
        "success": api_data["success"]
    }
    
    return result

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
