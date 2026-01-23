from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for navigation request.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the navigation request, either "success" or "failure"
        - message (str): Human-readable description of the navigation result including destination city
    """
    return {
        "status": "success",
        "message": f"Successfully navigated to {tool_name.split('_')[-1].title()} City"
    }

def map_mcp_server_navigate_to(city: str) -> Dict[str, Any]:
    """
    Navigate to the specified city.
    
    Args:
        city (str): The destination city name
        
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): Status of the navigation request ("success" or "failure")
            - message (str): Human-readable description of the navigation result, including destination city
            
    Raises:
        ValueError: If city is empty or not a string
    """
    # Input validation
    if not city or not isinstance(city, str):
        return {
            "status": "failure",
            "message": "Invalid input: city must be a non-empty string"
        }
    
    # Call external API simulation
    api_data = call_external_api("map-mcp-server-navigate_to")
    
    # Construct result using the provided city
    if api_data["status"] == "success":
        message = f"Successfully navigated to {city}"
    else:
        message = f"Failed to navigate to {city}"
    
    return {
        "status": "success",
        "message": message
    }