from typing import Dict, Any, Optional, List

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
    Simulates fetching data from external API for PowerShell script generation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - script_path (str): Path where the generated PowerShell script was saved
    """
    return {
        "script_path": "C:\\scripts\\generated_script.ps1"
    }

def powershell_exec_server_generate_custom_script(
    description: str,
    script_type: str,
    parameters: Optional[List[str]] = None,
    include_logging: Optional[bool] = False,
    include_error_handling: Optional[bool] = False,
    output_path: Optional[str] = None,
    timeout: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Generate a custom PowerShell script based on description and options.
    
    Args:
        description: Natural language description of what the script should do
        script_type: Type of script to generate (e.g., file_ops, service_mgmt)
        parameters: List of parameters the script should accept
        include_logging: Whether to include logging functions
        include_error_handling: Whether to include error handling
        output_path: Where to save the generated script (optional)
        timeout: Command timeout in seconds (1-300, default 60)
        
    Returns:
        Dictionary containing:
        - script_path (str): path where the generated PowerShell script was saved
    
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not description:
        raise ValueError("Description is required")
    
    if not script_type:
        raise ValueError("Script type is required")
    
    if timeout is not None:
        if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
            raise ValueError("Timeout must be an integer between 1 and 300 seconds")
    
    # Call external API to simulate script generation
    api_data = call_external_api("powershell-exec-server-generate_custom_script", **locals())
    
    # Construct result matching output schema
    result = {
        "script_path": api_data["script_path"]
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
