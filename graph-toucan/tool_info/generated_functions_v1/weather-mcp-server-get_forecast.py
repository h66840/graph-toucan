from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - current_temperature (str): Current temperature reading in °F with unit
        - period_0_period_name (str): Name of the first forecast period
        - period_0_temperature (str): Temperature for the first forecast period
        - period_0_wind (str): Wind conditions for the first forecast period
        - period_0_forecast_text (str): Forecast description for the first period
        - period_1_period_name (str): Name of the second forecast period
        - period_1_temperature (str): Temperature for the second forecast period
        - period_1_wind (str): Wind conditions for the second forecast period
        - period_1_forecast_text (str): Forecast description for the second period
    """
    return {
        "current_temperature": "72°F",
        "period_0_period_name": "Today",
        "period_0_temperature": "75°F",
        "period_0_wind": "5 mph NW",
        "period_0_forecast_text": "Sunny with clear skies throughout the day.",
        "period_1_period_name": "Tonight",
        "period_1_temperature": "60°F",
        "period_1_wind": "3 mph SE",
        "period_1_forecast_text": "Partly cloudy with mild temperatures."
    }

def weather_mcp_server_get_forecast(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get weather forecast for a location based on latitude and longitude.
    
    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location
    
    Returns:
        Dict containing:
        - periods (List[Dict]): List of forecast periods, each with 'period_name', 'temperature', 'wind', and 'forecast_text'
        - current_temperature (str): Current temperature reading in °F with unit
    
    Raises:
        ValueError: If latitude or longitude is outside valid range
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get weather data (simulated)
    api_data = call_external_api("weather-mcp-server-get_forecast")
    
    # Construct the periods list from flattened API response
    periods = [
        {
            "period_name": api_data["period_0_period_name"],
            "temperature": api_data["period_0_temperature"],
            "wind": api_data["period_0_wind"],
            "forecast_text": api_data["period_0_forecast_text"]
        },
        {
            "period_name": api_data["period_1_period_name"],
            "temperature": api_data["period_1_temperature"],
            "wind": api_data["period_1_wind"],
            "forecast_text": api_data["period_1_forecast_text"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "periods": periods,
        "current_temperature": api_data["current_temperature"]
    }
    
    return result