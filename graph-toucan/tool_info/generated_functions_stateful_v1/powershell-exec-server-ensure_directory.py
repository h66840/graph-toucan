from typing import Dict, Any

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
    Simulates fetching data from external API for ensuring directory exists.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - absolute_path (str): The full absolute path to the ensured directory, formatted with a leading '/app/' prefix and using backslashes within the Windows path
    """
    return {
        "absolute_path": "/app\\C:\\Users\\Admin\\Documents"
    }

def powershell_exec_server_ensure_directory(path: str) -> Dict[str, Any]:
    """
    Ensure directory exists and return absolute path.
    
    This function simulates ensuring that a directory exists on a server and returns 
    the absolute path formatted with a leading '/app/' prefix and using backslashes 
    for Windows-style paths.
    
    Args:
        path (str): The input path to ensure exists. If relative, it will be converted 
                   to absolute. If it doesn't exist, it's assumed to be created.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - absolute_path (str): The full absolute path to the ensured directory, 
              formatted with a leading '/app/' prefix and using backslashes within 
              the Windows path.
    
    Raises:
        ValueError: If path is None or empty string.
    """
    if not path or not path.strip():
        raise ValueError("Path parameter is required and cannot be empty")
    
    # Since we cannot use os.path.abspath due to security restrictions,
    # we simulate path normalization by stripping and using the API response
    cleaned_path = path.strip()
    
    # For relative paths, we'd normally resolve them, but without os module we rely on API
    # The external API call simulates the server-side path resolution
    api_data = call_external_api("powershell-exec-server-ensure_directory", **locals())
    
    # Extract the base path from API and ensure it uses backslashes
    # In a real scenario, this would be based on cleaned_path, but we're simulating
    # We use the API response as the source of truth for the resolved path
    api_path = api_data["absolute_path"]
    
    # Ensure the format is consistent: /app\ followed by Windows-style path
    if not api_path.startswith("/app\\"):
        # If API returns unexpected format, we construct it properly
        windows_path = cleaned_path.replace("/", "\\")
        final_path = f"/app\\{windows_path}"
    else:
        final_path = api_path
    
    # Return result matching output schema exactly
    return {
        "absolute_path": final_path
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
