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
    Simulates fetching data from external API for executing a Windows command.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - output (str): Simulated command output
        - error (str): Simulated error message, if any
        - exit_code (int): Simulated exit code of the command
    """
    # Simulate different responses based on the command
    # For simplicity, we assume the command is 'dir' or 'echo' as per allowed list
    return {
        "output": " Volume in drive C has no label.\n Volume Serial Number is 1234-5678\n Directory of C:\\test\n.\n..\nfile1.txt\nfile2.txt\n       2 File(s)            512 bytes\n       2 Dir(s)  123,456,789,012 bytes free",
        "error": None,
        "exit_code": 0
    }

def windows_command_line_mcp_server_execute_command(command: str, timeout: Optional[int] = None, workingDir: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute a Windows command and return its output. Only commands in the allowed list can be executed.
    This function simulates running simple commands like 'dir', 'echo', etc.

    Parameters:
        command (str): The command to execute (required)
        timeout (Optional[int]): Timeout in milliseconds (optional)
        workingDir (Optional[str]): Working directory for the command (optional)

    Returns:
        Dict containing:
        - output (str): The raw textual output from executing the Windows command
        - error (Optional[str]): Any error message produced during command execution; present only if failed
        - exit_code (int): The exit status code of the executed command (0 for success)

    Raises:
        ValueError: If command is empty or not in allowed list
    """
    # Input validation
    if not command or not command.strip():
        raise ValueError("Command is required and cannot be empty")

    command = command.strip()
    allowed_commands = ['dir', 'echo', 'cd', 'cls', 'ver', 'vol', 'type', 'ping']
    
    # Check if the command (first word) is in allowed list
    base_command = command.split()[0].lower()
    if base_command not in allowed_commands:
        return {
            "output": "",
            "error": f"Command '{base_command}' is not allowed. Only {', '.join(allowed_commands)} are permitted.",
            "exit_code": 1
        }

    # Call the external API simulation
    api_data = call_external_api("windows-command-line-mcp-server-execute_command", **locals())
    
    # Construct the result using the simulated data
    result: Dict[str, Any] = {
        "output": api_data["output"],
        "exit_code": api_data["exit_code"]
    }
    
    # Add error field only if it exists and is not None
    if api_data["error"] is not None:
        result["error"] = api_data["error"]
    
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
