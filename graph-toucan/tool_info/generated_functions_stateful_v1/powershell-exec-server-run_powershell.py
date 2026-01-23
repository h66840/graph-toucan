from typing import Dict, Any, Optional
import sys

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
        - output (str): Simulated raw output from PowerShell command execution
        - error (str): Simulated error message if execution failed
    """
    # Simulate successful command output
    return {
        "output": "Command executed successfully\nValue: 42\nStatus: OK",
        "error": ""
    }


def powershell_exec_server_run_powershell(code: str, ctx: Optional[Any] = None, timeout: Optional[int] = 60) -> Dict[str, str]:
    """
    Execute PowerShell commands securely.

    Args:
        code (str): PowerShell code to execute (required)
        ctx (Any, optional): MCP context for logging and progress reporting
        timeout (int, optional): Command timeout in seconds (1-300, default 60)

    Returns:
        Dict[str, str]: Dictionary containing:
            - output (str): Raw output from the PowerShell command execution, including any printed messages, errors, or results
            - error (str): Error message if the PowerShell execution failed, such as system-level errors

    Raises:
        ValueError: If code is empty or timeout is not in valid range
        RuntimeError: If subprocess fails to start
    """
    # Input validation
    if not code or not code.strip():
        return {
            "output": "",
            "error": "PowerShell code is required and cannot be empty"
        }

    if timeout is None:
        timeout = 60
    elif not isinstance(timeout, int) or timeout < 1 or timeout > 300:
        return {
            "output": "",
            "error": "Timeout must be an integer between 1 and 300 seconds"
        }

    try:
        # Use the simulated API call instead of actual subprocess execution
        api_result = call_external_api("powershell_exec", **locals())
        
        # Return the simulated output and error
        return {
            "output": api_result["output"],
            "error": api_result["error"]
        }

    except Exception as e:
        return {
            "output": "",
            "error": f"Failed to execute PowerShell command: {str(e)}"
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
