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
    Simulates fetching data from external API for remote shell command execution.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - command (str): The shell command that was executed
        - working_directory (str): The working directory where the command was executed
        - success (bool): Whether the command executed successfully
        - stdout (str): Standard output from the command
        - stderr (str): Standard error output from the command
        - error_message (str): Detailed error message if command failed
    """
    return {
        "command": "ls -la",
        "working_directory": "/home/user",
        "success": True,
        "stdout": "total 24\ndrwxr-xr-x  5 user user 4096 Apr 10 10:00 .\ndrwxr-xr-x  3 root root 4096 Apr 10 09:00 ..\n-rw-r--r--  1 user user  220 Apr 10 09:00 .bash_logout",
        "stderr": "",
        "error_message": ""
    }

def remote_shell_server_shell_exec(command: str, cwd: Optional[str] = None, timeout: Optional[int] = 30000) -> Dict[str, Any]:
    """
    Execute shell commands remotely. This tool allows running shell commands on the remote system and returns the output.
    Use with caution as it can execute any command.
    
    Args:
        command (str): The shell command to execute (required)
        cwd (Optional[str]): Working directory for the command (optional)
        timeout (Optional[int]): Timeout in milliseconds (default: 30000)
    
    Returns:
        Dict containing:
        - command (str): the shell command that was executed
        - working_directory (str): the working directory where the command was executed
        - success (bool): whether the command executed successfully
        - stdout (str): standard output from the command, empty if none
        - stderr (str): standard error output from the command, empty if none
        - error_message (str): detailed error message if the command failed, otherwise empty
    
    Raises:
        ValueError: If command is empty or None
    """
    # Input validation
    if not command or not command.strip():
        raise ValueError("Command parameter is required and cannot be empty")
    
    # Prepare parameters for API call
    if cwd is None:
        cwd = ""
    
    # Call external API (simulation)
    api_data = call_external_api("remote-shell-server-shell-exec", **locals())
    
    # Construct result based on API data and inputs
    result = {
        "command": command.strip(),
        "working_directory": cwd if cwd else api_data["working_directory"],
        "success": api_data["success"],
        "stdout": api_data["stdout"],
        "stderr": api_data["stderr"],
        "error_message": api_data["error_message"]
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
