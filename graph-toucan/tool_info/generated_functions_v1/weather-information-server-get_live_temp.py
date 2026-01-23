from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): Current temperature in degrees Celsius at the specified coordinates
    """
    # Simulated temperature based on latitude and longitude (for demonstration purposes)
    # This is a mock implementation; actual API would return real data
    return {
        "temperature": 20.5  # Simulated temperature in degrees Celsius
    }

def weather_information_server_get_live_temp(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get live temperature for a given latitude and longitude.
    
    This function retrieves the current temperature in degrees Celsius
    at the specified geographic coordinates by querying an external weather service.
    
    Args:
        latitude (float): The latitude of the location (required)
        longitude (float): The longitude of the location (required)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - temperature (float): current temperature in degrees Celsius at the specified coordinates
    
    Raises:
        ValueError: If latitude is not between -90 and 90 or longitude is not between -180 and 180
    """
    # Input validation
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get weather data (simulated)
    api_data = call_external_api("weather-information-server-get_live_temp")
    
    # Construct result matching output schema
    result = {
        "temperature": api_data["temperature"]
    }
    
    return result