from typing import Dict, List, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for health check.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Current health status of the server
        - timestamp (str): ISO 8601 formatted timestamp
        - server (str): Name or identifier of the server
        - version (str): Version of the server software
        - tools_available_0 (str): First available tool name
        - tools_available_1 (str): Second available tool name
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "server": "lyrical-mcp-server-01",
        "version": "1.5.2",
        "tools_available_0": "lyrical-mcp-health_check",
        "tools_available_1": "lyrical-mcp-analyze_sentiment"
    }

def lyrical_mcp_health_check() -> Dict[str, Any]:
    """
    Performs a health check to verify server connectivity and status.
    
    Returns:
        Dict containing:
        - status (str): Current health status of the server (e.g., "healthy")
        - timestamp (str): ISO 8601 formatted timestamp indicating when the health check was performed
        - server (str): Name or identifier of the server being checked
        - version (str): Version of the server software
        - tools_available (List[str]): List of tool names available on the server
    
    Raises:
        Exception: If there is an error communicating with the external service or parsing the response
    """
    try:
        # Call external API to get health check data
        api_data = call_external_api("lyrical-mcp-health_check")
        
        # Construct the result dictionary matching the output schema
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
        raise Exception(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to perform health check: {str(e)}")