from typing import Dict, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): Temperature in Celsius
        - location (str): City or location name
        - timestamp (str): Date and time in 'YYYY-MM-DD HH:MM' format
    """
    return {
        "temperature": 22.5,
        "location": "Shanghai",
        "timestamp": "2023-10-05 14:30"
    }

def python_mcp_server_template_weather_tool(location: str) -> Dict[str, Any]:
    """
    Retrieves weather information for a given location.
    
    Args:
        location (str): The city or location for which to retrieve weather data.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - temperature (float): Temperature in degrees Celsius
            - location (str): The city or location name
            - timestamp (str): The observation time in 'YYYY-MM-DD HH:MM' format
    
    Raises:
        ValueError: If location is empty or not a string
    """
    if not location or not isinstance(location, str):
        raise ValueError("Location must be a non-empty string")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("python-mcp-server-template-weather_tool")
    
    # Construct result matching output schema
    result = {
        "temperature": float(api_data["temperature"]),
        "location": str(api_data["location"]),
        "timestamp": str(api_data["timestamp"])
    }
    
    return result