from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB StatsAPI endpoints.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - endpoint_0_path (str): Path of the first available endpoint
        - endpoint_0_methods (str): Supported HTTP methods for first endpoint (comma-separated)
        - endpoint_0_description (str): Description of the first endpoint
        - endpoint_0_parameters (str): Parameters accepted by first endpoint (comma-separated)
        - endpoint_1_path (str): Path of the second available endpoint
        - endpoint_1_methods (str): Supported HTTP methods for second endpoint (comma-separated)
        - endpoint_1_description (str): Description of the second endpoint
        - endpoint_1_parameters (str): Parameters accepted by second endpoint (comma-separated)
        - total_count (int): Total number of available endpoints
        - api_version (str): Version of the MLB StatsAPI
        - documentation_url (str): URL to the official documentation
        - last_updated (str): Timestamp when the endpoint list was last updated (ISO 8601 format)
    """
    return {
        "endpoint_0_path": "/api/v1/schedule",
        "endpoint_0_methods": "GET",
        "endpoint_0_description": "Retrieve game schedule information for MLB games.",
        "endpoint_0_parameters": "date, teamId, leagueId, sportId",
        "endpoint_1_path": "/api/v1/teams",
        "endpoint_1_methods": "GET",
        "endpoint_1_description": "Get information about MLB teams including roster and details.",
        "endpoint_1_parameters": "teamId, leagueId, sportId, activeStatus",
        "total_count": 2,
        "api_version": "v1",
        "documentation_url": "https://statsapi.mlb.com/docs",
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


def mlb_stats_server_get_available_endpoints() -> Dict[str, Any]:
    """
    Fetches and returns a list of available MLB StatsAPI endpoints with detailed metadata.

    This function simulates querying an external MLB StatsAPI server to retrieve
    available endpoints, their supported methods, descriptions, parameters, and metadata
    such as API version, documentation URL, and last updated timestamp.

    Returns:
        Dict containing:
        - endpoints (List[Dict]): List of endpoint dictionaries with keys:
            - path (str): Endpoint URL path
            - methods (List[str]): HTTP methods supported
            - description (str): Description of the endpoint
            - parameters (List[str]): List of accepted parameter names
        - total_count (int): Total number of endpoints returned
        - api_version (str): Version of the MLB StatsAPI
        - documentation_url (str): Link to official API documentation
        - last_updated (str): ISO 8601 timestamp of when data was generated

    Raises:
        ValueError: If required fields are missing or malformed in the response
    """
    try:
        # Call the simulated external API
        api_data = call_external_api("mlb-stats-server-get_available_endpoints")

        # Construct the endpoints list from flattened fields
        endpoints: List[Dict[str, Any]] = [
            {
                "path": api_data["endpoint_0_path"],
                "methods": [method.strip() for method in api_data["endpoint_0_methods"].split(",")] if api_data["endpoint_0_methods"] else [],
                "description": api_data["endpoint_0_description"],
                "parameters": [param.strip() for param in api_data["endpoint_0_parameters"].split(",")] if api_data["endpoint_0_parameters"] else []
            },
            {
                "path": api_data["endpoint_1_path"],
                "methods": [method.strip() for method in api_data["endpoint_1_methods"].split(",")] if api_data["endpoint_1_methods"] else [],
                "description": api_data["endpoint_1_description"],
                "parameters": [param.strip() for param in api_data["endpoint_1_parameters"].split(",")] if api_data["endpoint_1_parameters"] else []
            }
        ]

        # Build final result structure
        result = {
            "endpoints": endpoints,
            "total_count": api_data["total_count"],
            "api_version": api_data["api_version"],
            "documentation_url": api_data["documentation_url"],
            "last_updated": api_data["last_updated"]
        }

        return result

    except KeyError as e:
        raise ValueError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise ValueError(f"Failed to process MLB StatsAPI endpoint data: {e}")