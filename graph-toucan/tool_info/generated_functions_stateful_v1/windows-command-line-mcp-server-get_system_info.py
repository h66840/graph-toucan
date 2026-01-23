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
    Simulates fetching system information from an external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if tool cannot run outside Windows
        - platform (str): Operating system platform where the tool was executed
    """
    return {
        "error": "This tool can only be executed in a Windows environment.",
        "platform": "Linux"
    }

def windows_command_line_mcp_server_get_system_info(detail: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve system information including OS, hardware, and user details.
    
    This function simulates retrieving system information by calling an external API.
    The level of detail can be specified via the 'detail' parameter.
    
    Args:
        detail (Optional[str]): Level of detail for the system information. 
                               Can be 'basic' or 'full'. Defaults to 'basic'.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - error (str): Error message if tool cannot run outside Windows environment
            - platform (str): Current operating system platform where the tool was executed
    
    Note:
        This tool is designed to run on Windows systems. When executed elsewhere,
        it will return an error indicating the incompatible environment.
    """
    # Validate input
    if detail is not None and detail not in ['basic', 'full']:
        return {
            "error": "Invalid detail level. Use 'basic' or 'full'.",
            "platform": "Unknown"
        }
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("windows-command-line-mcp-server-get_system_info", **locals())
    
    # Construct result matching output schema
    result = {
        "error": api_data["error"],
        "platform": api_data["platform"]
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
