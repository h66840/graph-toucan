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
    Simulates fetching data from external API for shell command execution.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - exit_code (int): exit code of the executed shell command (0 for success, non-zero for errors)
        - execution_output (str): captured output or message from the command execution
    """
    return {
        "exit_code": 0,
        "execution_output": "Command executed successfully"
    }

def lilith_shell_execute_command(command: str, directory: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute a shell command in the specified directory.
    
    Args:
        command (str): Command to execute
        directory (Optional[str]): Working directory (optional)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - exit_code (int): exit code of the executed shell command (0 for success, non-zero for errors)
            - execution_output (str): captured output or message from the command execution, if any
    
    Raises:
        ValueError: If command is empty or not a string
        RuntimeError: If there's an error during command execution
    """
    # Input validation
    if not command:
        raise ValueError("Command is required and cannot be empty")
    
    if not isinstance(command, str):
        raise ValueError("Command must be a string")
    
    if directory is not None:
        if not isinstance(directory, str):
            raise ValueError("Directory must be a string")
        # Note: Without os.path, we can't validate directory existence or type
        # This is a limitation of removing dangerous imports, but we maintain interface
    
    try:
        # Simulate command execution using the external API helper
        api_result = call_external_api("shell_command", **locals())
        
        # Return structured output with simulated results
        return {
            "exit_code": api_result["exit_code"],
            "execution_output": api_result["execution_output"]
        }
        
    except Exception as e:
        return {
            "exit_code": -1,
            "execution_output": f"Error executing command: {str(e)}"
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
