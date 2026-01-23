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
    Simulates fetching data from external API for Windows service information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_message (str): Error message indicating platform incompatibility
        - platform (str): The current operating system platform
    """
    return {
        "error_message": "This tool is only available on Windows operating systems.",
        "platform": "Linux"
    }

def windows_command_line_mcp_server_get_service_info(action: Optional[str] = None, serviceName: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve information about Windows services. Can query all services or get detailed status of a specific service.
    
    This function simulates interaction with a Windows command-line tool to retrieve service information.
    Since the actual tool is not available on non-Windows platforms, it returns a simulated error response.
    
    Args:
        action (Optional[str]): Action to perform (e.g., 'list', 'status'). Defaults to None.
        serviceName (Optional[str]): Service name to get info about. Defaults to None.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - error_message (str): Error message indicating the tool is not available on the current platform
            - platform (str): The current operating system platform where the tool was attempted to run
    """
    # Call external API to get flat data
    api_data = call_external_api("windows-command-line-mcp-server-get_service_info", **locals())
    
    # Construct result matching output schema
    result = {
        "error_message": api_data["error_message"],
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
