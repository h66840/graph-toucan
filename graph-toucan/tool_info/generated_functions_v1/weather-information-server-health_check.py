from typing import Dict, List, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
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
        api_data = call_external_api("weather-information-server-health_check")
        
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