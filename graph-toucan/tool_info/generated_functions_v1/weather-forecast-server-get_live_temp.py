from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): Current temperature in degrees Celsius at the specified location
    """
    # Simulated temperature based on latitude and longitude using a deterministic formula
    # This is a mock implementation; in real case, it would call an actual API
    return {
        "temperature": 20.0  # Mock value; actual implementation would depend on external service
    }

def weather_forecast_server_get_live_temp(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get live temperature for a given latitude and longitude.
    
    This function retrieves the current temperature in degrees Celsius
    for the specified geographic coordinates by querying an external weather service.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - temperature (float): Current temperature in degrees Celsius at the specified location
    
    Raises:
        ValueError: If latitude or longitude are out of valid range
    """
    # Input validation
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API (mocked in this implementation)
    api_data = call_external_api("weather-forecast-server-get_live_temp")
    
    # Construct result matching output schema
    result = {
        "temperature": api_data["temperature"]
    }
    
    return result