from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): the current live temperature in degrees Celsius at the specified location
    """
    # Simulated temperature based on latitude and longitude (for demonstration purposes)
    # This is a mock implementation; actual API would return real data
    return {
        "temperature": 20.5  # Mock temperature in degrees Celsius
    }

def tool_360_weather_mcp_get_live_temp(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get live temperature for a given latitude and longitude.
    
    This function retrieves the current temperature in degrees Celsius
    for the specified geographic coordinates by querying an external weather service.
    
    Args:
        latitude (float): The latitude of the location (required)
        longitude (float): The longitude of the location (required)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - temperature (float): the current live temperature in degrees Celsius at the specified location
    
    Raises:
        ValueError: If latitude or longitude are out of valid range
    """
    # Input validation
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get temperature data
    api_data = call_external_api("360-weather-mcp-get_live_temp")
    
    # Construct result matching output schema
    result = {
        "temperature": api_data["temperature"]
    }
    
    return result