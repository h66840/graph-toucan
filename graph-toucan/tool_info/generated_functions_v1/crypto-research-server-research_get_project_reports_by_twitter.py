from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for crypto-research-server-research_get_project_reports_by_twitter.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message when the request fails, including HTTP status and description
        - status_code (int): HTTP status code returned by the API, e.g., 404 for not found
    """
    # Simulated response based on tool name
    if tool_name == "crypto-research-server-research_get_project_reports_by_twitter":
        return {
            "error": "",
            "status_code": 200
        }
    else:
        return {
            "error": "Unknown tool name",
            "status_code": 500
        }

def crypto_research_server_research_get_project_reports_by_twitter(username: str) -> Dict[str, Any]:
    """
    Get project reports by Twitter username on Research knowledge base.
    
    This function retrieves project reports associated with a given Twitter username
    from the crypto research server's knowledge base.
    
    Args:
        username (str): Twitter username of the project (required)
        
    Returns:
        Dict containing:
        - error (str): Error message when the request fails, including HTTP status and description
        - status_code (int): HTTP status code returned by the API
        
    Example:
        >>> crypto_research_server_research_get_project_reports_by_twitter("bitcoin")
        {'error': '', 'status_code': 200}
    """
    # Input validation
    if not username:
        return {
            "error": "Username is required",
            "status_code": 400
        }
    
    # Call external API simulation
    api_data = call_external_api("crypto-research-server-research_get_project_reports_by_twitter")
    
    # Construct result matching output schema
    result = {
        "error": api_data["error"],
        "status_code": api_data["status_code"]
    }
    
    return result