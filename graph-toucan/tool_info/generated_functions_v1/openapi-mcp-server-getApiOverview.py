from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for OpenAPI specification overview.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - api_name (str): Name of the API
        - base_url (str): Base URL of the API endpoint
        - version (str): Version identifier of the API
        - total_endpoints (int): Total number of available endpoints
        - endpoint_0_operation_id (str): Operation ID of first endpoint
        - endpoint_0_method (str): HTTP method of first endpoint
        - endpoint_0_url (str): URL path of first endpoint
        - endpoint_0_description (str): Description of first endpoint
        - endpoint_0_spec_url (str): Spec URL of first endpoint
        - endpoint_1_operation_id (str): Operation ID of second endpoint
        - endpoint_1_method (str): HTTP method of second endpoint
        - endpoint_1_url (str): URL path of second endpoint
        - endpoint_1_description (str): Description of second endpoint
        - endpoint_1_spec_url (str): Spec URL of second endpoint
        - summary_url_template (str): Template URL for detailed endpoint summaries with [idOrRoute] placeholder
    """
    return {
        "api_name": "GitHub API",
        "base_url": "https://api.github.com",
        "version": "v3",
        "total_endpoints": 150,
        "endpoint_0_operation_id": "get_user",
        "endpoint_0_method": "GET",
        "endpoint_0_url": "/users/{username}",
        "endpoint_0_description": "Get a user's public profile information",
        "endpoint_0_spec_url": "https://api.github.com/openapi.json#tag/users/operation/getUser",
        "endpoint_1_operation_id": "create_repo",
        "endpoint_1_method": "POST",
        "endpoint_1_url": "/user/repos",
        "endpoint_1_description": "Create a new repository for the authenticated user",
        "endpoint_1_spec_url": "https://api.github.com/openapi.json#tag/repos/operation/createRepo",
        "summary_url_template": "https://api.github.com/docs/[idOrRoute]"
    }

def openapi_mcp_server_getApiOverview(id: str) -> Dict[str, Any]:
    """
    Get an overview of an OpenAPI specification. This should be the first step when working with any API.
    
    Args:
        id (str): API identifier, can be a known ID from openapisearch.com or a URL leading to a raw OpenAPI file
        
    Returns:
        Dict containing:
        - api_name (str): name of the API as provided in the overview
        - base_url (str): base URL of the API endpoint
        - version (str): version identifier of the API
        - total_endpoints (int): total number of available endpoints in the API
        - endpoints (List[Dict]): list of endpoint objects with 'operation_id', 'method', 'url', 'description', and 'spec_url' fields
        - summary_url_template (str): template URL for accessing detailed endpoint summaries, containing '[idOrRoute]' placeholder
        
    Raises:
        ValueError: If the required 'id' parameter is empty or None
    """
    if not id or not isinstance(id, str):
        raise ValueError("Parameter 'id' must be a non-empty string")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("openapi-mcp-server-getApiOverview")
    
    # Construct endpoints list from flattened fields
    endpoints = [
        {
            "operation_id": api_data["endpoint_0_operation_id"],
            "method": api_data["endpoint_0_method"],
            "url": api_data["endpoint_0_url"],
            "description": api_data["endpoint_0_description"],
            "spec_url": api_data["endpoint_0_spec_url"]
        },
        {
            "operation_id": api_data["endpoint_1_operation_id"],
            "method": api_data["endpoint_1_method"],
            "url": api_data["endpoint_1_url"],
            "description": api_data["endpoint_1_description"],
            "spec_url": api_data["endpoint_1_spec_url"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "api_name": api_data["api_name"],
        "base_url": api_data["base_url"],
        "version": api_data["version"],
        "total_endpoints": api_data["total_endpoints"],
        "endpoints": endpoints,
        "summary_url_template": api_data["summary_url_template"]
    }
    
    return result