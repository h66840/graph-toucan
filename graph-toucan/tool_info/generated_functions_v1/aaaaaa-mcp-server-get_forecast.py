from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather forecast data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - forecast_0_period (str): Name of the first forecast period
        - forecast_0_description (str): Weather description for first period
        - forecast_0_temperature (float): Temperature in Celsius for first period
        - forecast_0_wind (str): Wind conditions for first period
        - forecast_0_precipitation_chance (float): Chance of precipitation (0-100) for first period
        - forecast_1_period (str): Name of the second forecast period
        - forecast_1_description (str): Weather description for second period
        - forecast_1_temperature (float): Temperature in Celsius for second period
        - forecast_1_wind (str): Wind conditions for second period
        - forecast_1_precipitation_chance (float): Chance of precipitation (0-100) for second period
    """
    return {
        "forecast_0_period": "Today",
        "forecast_0_description": "Partly cloudy with sunny intervals",
        "forecast_0_temperature": 22.5,
        "forecast_0_wind": "NW 15 km/h",
        "forecast_0_precipitation_chance": 20.0,
        "forecast_1_period": "Tonight",
        "forecast_1_description": "Clear skies and cool",
        "forecast_1_temperature": 14.0,
        "forecast_1_wind": "Calm",
        "forecast_1_precipitation_chance": 5.0,
    }

def aaaaaa_mcp_server_get_forecast(lat: float, lon: float) -> Dict[str, Any]:
    """
    Get weather forecast for a given latitude and longitude.
    
    This function simulates retrieving a weather forecast by calling an external API
    and transforming the flat response into the required nested structure.
    
    Args:
        lat (float): Latitude coordinate (required)
        lon (float): Longitude coordinate (required)
    
    Returns:
        Dict containing:
            forecast_periods (List[Dict]): List of forecast periods with keys:
                - period (str): Name of the time period
                - description (str): Weather condition description
                - temperature (float): Temperature in Celsius
                - wind (str): Wind speed and direction
                - precipitation_chance (Optional[float]): Chance of precipitation (0-100)
    
    Raises:
        ValueError: If latitude or longitude are outside valid ranges
    """
    # Input validation
    if not -90 <= lat <= 90:
        raise ValueError("Latitude must be between -90 and 90 degrees")
    if not -180 <= lon <= 180:
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get flat data
    api_data = call_external_api("aaaaaa-mcp-server-get_forecast")
    
    # Construct forecast periods list from flat API data
    forecast_periods: List[Dict[str, Any]] = [
        {
            "period": api_data["forecast_0_period"],
            "description": api_data["forecast_0_description"],
            "temperature": api_data["forecast_0_temperature"],
            "wind": api_data["forecast_0_wind"],
            "precipitation_chance": api_data["forecast_0_precipitation_chance"]
        },
        {
            "period": api_data["forecast_1_period"],
            "description": api_data["forecast_1_description"],
            "temperature": api_data["forecast_1_temperature"],
            "wind": api_data["forecast_1_wind"],
            "precipitation_chance": api_data["forecast_1_precipitation_chance"]
        }
    ]
    
    return {
        "forecast_periods": forecast_periods
    }