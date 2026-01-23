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
    Simulates fetching data from external API for terminal command execution.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - stdout (str): Standard output from command execution
        - stderr (str): Standard error output from command execution
        - exit_code (int): Exit status code of the executed command
    """
    return {
        "stdout": "Command executed successfully",
        "stderr": "",
        "exit_code": 0
    }

def terminal_mcp_server_execute_command(
    command: str,
    env: Optional[Dict[str, str]] = None,
    host: Optional[str] = None,
    session: Optional[str] = None,
    username: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute commands on remote hosts or locally.
    
    This function simulates executing a shell command either locally or on a remote host
    via SSH. It returns the standard output, standard error, and exit code of the command.
    
    Args:
        command (str): Command to execute. Before running commands, it's best to determine the system type (Mac, Linux, etc.)
        env (Optional[Dict[str, str]]): Environment variables to set for the command execution
        host (Optional[str]): Host to connect to (if not provided, command runs locally)
        session (Optional[str]): Session name, defaults to 'default'. Reusing the same session name maintains terminal environment for 20 minutes.
        username (Optional[str]): Username for SSH connection (required when host is specified)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - stdout (str): Output from the command's standard output stream
            - stderr (str): Output from the command's standard error stream
            - exit_code (int): Exit status code of the executed command; 0 indicates success
    
    Raises:
        ValueError: If host is provided but username is missing
    """
    # Input validation
    if host is not None and not username:
        raise ValueError("Username is required when specifying a host for SSH connection")
    
    if not command.strip():
        raise ValueError("Command cannot be empty or whitespace")
    
    # Default session name
    if session is None:
        session = "default"
    
    # Call external API to simulate command execution
    api_data = call_external_api("terminal-mcp-server-execute_command", **locals())
    
    # Construct result matching output schema
    result = {
        "stdout": api_data["stdout"],
        "stderr": api_data["stderr"],
        "exit_code": api_data["exit_code"]
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
