from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): Current live temperature in degrees Celsius
    """
    # Simulated temperature based on latitude and longitude (for demonstration purposes)
    # This is a mock implementation; actual API would return real data
    return {
        "temperature": 20.5  # Simulated live temperature
    }

def weather_forecast_get_live_temp(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get live temperature for a given latitude and longitude.
    
    This function retrieves the current temperature for the specified geographic coordinates
    by calling an external weather service API (simulated here).
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - temperature (float): Current live temperature in degrees Celsius
    
    Raises:
        ValueError: If latitude or longitude are not within valid ranges
    """
    # Input validation
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get weather data (simulated)
    api_data = call_external_api("weather-forecast-get_live_temp")
    
    # Construct result matching output schema
    result = {
        "temperature": api_data["temperature"]
    }
    
    return result