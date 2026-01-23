from typing import Dict, List, Any
from datetime import datetime

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
    Simulates fetching data from external API for health check.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Current health status of the server
        - timestamp (str): ISO 8601 timestamp of the health check
        - server (str): Name or identifier of the server
        - version (str): Version of the server software
        - tools_available_0 (str): First available tool name
        - tools_available_1 (str): Second available tool name
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "server": "weather-server-01",
        "version": "1.5.3",
        "tools_available_0": "weather-information-server-health_check",
        "tools_available_1": "weather-forecast-retrieve"
    }

def weather_information_server_health_check() -> Dict[str, Any]:
    """
    Health check to verify server connectivity and status.

    Returns:
        Dict containing:
        - status (str): Current health status of the server (e.g., "healthy")
        - timestamp (str): ISO 8601 timestamp indicating when the health check was performed
        - server (str): Name or identifier of the server being checked
        - version (str): Version of the server software
        - tools_available (List[str]): List of tool names that are available and operational on the server
    """
    try:
        # Fetch data from external API simulation
        api_data = call_external_api("weather-information-server-health_check", **locals())
        
        # Construct the result with proper nested structure
        result = {
            "status": api_data["status"],
            "timestamp": api_data["timestamp"],
            "server": api_data["server"],
            "version": api_data["version"],
            "tools_available": [
                api_data["tools_available_0"],
                api_data["tools_available_1"]
            ]
        }
        
        return result
        
    except KeyError as e:
        # Handle missing expected fields
        raise KeyError(f"Missing required field in API response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise Exception(f"Failed to perform health check: {str(e)}")

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
