from typing import Dict, Any, List
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
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the server (e.g., "healthy")
        - timestamp (str): ISO 8601 timestamp indicating when the health check was performed
        - server (str): Name or identifier of the weather server (e.g., "weather-mcp")
        - version (str): Version string of the server software (e.g., "1.0.0")
        - tool_0 (str): First tool name available on the server
        - tool_1 (str): Second tool name available on the server
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "server": "weather-mcp",
        "version": "1.0.0",
        "tool_0": "weather-server-health_check",
        "tool_1": "weather-forecast-retrieve"
    }

def weather_server_health_check() -> Dict[str, Any]:
    """
    Health check to verify server connectivity and status.
    
    Returns:
        Dict containing:
        - status (str): Status of the server (e.g., "healthy")
        - timestamp (str): ISO 8601 timestamp indicating when the health check was performed
        - server (str): Name or identifier of the weather server (e.g., "weather-mcp")
        - version (str): Version string of the server software (e.g., "1.0.0")
        - tools_available (List[str]): List of tool names available on the server
    
    Raises:
        RuntimeError: If there is an issue communicating with the external service
        KeyError: If expected fields are missing from the response
        ValueError: If required fields have invalid values
    """
    try:
        # Call external API to get health check data
        api_data = call_external_api("weather-server-health_check", **locals())
        
        # Validate required fields are present
        required_fields = ["status", "timestamp", "server", "version", "tool_0", "tool_1"]
        for field in required_fields:
            if field not in api_data:
                raise KeyError(f"Missing required field in API response: {field}")
        
        # Extract and validate scalar values
        status = str(api_data["status"])
        if not status:
            raise ValueError("Status cannot be empty")
            
        timestamp = str(api_data["timestamp"])
        server = str(api_data["server"])
        version = str(api_data["version"])
        
        # Construct tools_available list from indexed fields
        tools_available: List[str] = []
        for i in range(2):  # We expect 2 tools based on tool_0 and tool_1
            tool_key = f"tool_{i}"
            if tool_key in api_data:
                tool_value = api_data[tool_key]
                if tool_value is not None:
                    tools_available.append(str(tool_value))
        
        # Construct final result matching output schema
        result = {
            "status": status,
            "timestamp": timestamp,
            "server": server,
            "version": version,
            "tools_available": tools_available
        }
        
        return result
        
    except Exception as e:
        if isinstance(e, (KeyError, ValueError)):
            raise
        else:
            raise RuntimeError(f"Failed to perform health check: {str(e)}")

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
