from typing import Dict, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): The overall health status of the API (e.g., 'healthy', 'degraded', 'unavailable')
        - is_healthy (bool): Boolean indicator of whether the API is currently functioning properly
        - timestamp (str): ISO 8601 timestamp indicating when the health check was performed
        - version (str): The current version of the Gaming Trend Analytics API
        - response_time_ms (float): The time in milliseconds it took for the API to respond to the health check
        - dependency_database_status (str): Health status of the database dependency
        - dependency_cache_status (str): Health status of the cache dependency
        - error_message (str): Optional error message if the health check failed or a component is unhealthy
    """
    return {
        "status": "healthy",
        "is_healthy": True,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "2.1.5",
        "response_time_ms": 47.8,
        "dependency_database_status": "up",
        "dependency_cache_status": "degraded",
        "error_message": ""
    }

def game_trends_get_api_health() -> Dict[str, Any]:
    """
    Check the health status of the Gaming Trend Analytics API.
    
    This function performs a health check on the Gaming Trend Analytics API by querying
    an external service and returning detailed information about the API's status,
    response time, dependencies, and other relevant metrics.
    
    Returns:
        Dict containing:
        - status (str): The overall health status of the API (e.g., 'healthy', 'degraded', 'unavailable')
        - is_healthy (bool): Boolean indicator of whether the API is currently functioning properly
        - timestamp (str): ISO 8601 timestamp indicating when the health check was performed
        - version (str): The current version of the Gaming Trend Analytics API
        - response_time_ms (float): The time in milliseconds it took for the API to respond to the health check
        - dependencies (Dict): Health status of downstream services or databases the API depends on
        - error_message (str): Optional error message if the health check failed or a component is unhealthy
    """
    try:
        # Call external API to get health data
        api_data = call_external_api("game-trends-get_api_health")
        
        # Construct dependencies dictionary from flattened fields
        dependencies = {
            "database": api_data["dependency_database_status"],
            "cache": api_data["dependency_cache_status"]
        }
        
        # Build final result structure matching output schema
        result = {
            "status": api_data["status"],
            "is_healthy": api_data["is_healthy"],
            "timestamp": api_data["timestamp"],
            "version": api_data["version"],
            "response_time_ms": api_data["response_time_ms"],
            "dependencies": dependencies,
            "error_message": api_data["error_message"] if api_data["error_message"] else None
        }
        
        return result
        
    except KeyError as e:
        return {
            "status": "unavailable",
            "is_healthy": False,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "unknown",
            "response_time_ms": float("inf"),
            "dependencies": {},
            "error_message": f"Missing required field in API response: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "unavailable",
            "is_healthy": False,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "unknown",
            "response_time_ms": float("inf"),
            "dependencies": {},
            "error_message": f"Unexpected error during health check: {str(e)}"
        }