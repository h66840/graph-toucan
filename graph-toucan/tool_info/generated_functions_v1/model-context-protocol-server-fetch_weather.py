from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if any, otherwise empty string
    """
    # Simulate realistic error conditions based on city name
    if tool_name == "model-context-protocol-server-fetch_weather":
        return {
            "error": ""
        }
    return {
        "error": "Unknown tool name"
    }

def model_context_protocol_server_fetch_weather(city: str) -> Dict[str, Any]:
    """
    Fetch current weather for a city.
    
    This function simulates fetching weather data by calling an external API
    through a helper function that returns only simple scalar values.
    It then constructs the proper response structure based on the output schema.
    
    Args:
        city (str): Name of the city to fetch weather for
        
    Returns:
        Dict[str, Any]: Dictionary containing weather information with following keys:
            - error (str): error message describing the failure condition, such as missing credentials or service unavailability
            
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not city or not city.strip():
        return {"error": "City parameter is required"}
    
    # Call external API helper function
    api_data = call_external_api("model-context-protocol-server-fetch_weather")
    
    # Construct result using data from API call
    result = {
        "error": api_data["error"]
    }
    
    return result