from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather forecast.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - forecast_0_period (str): Name of the first forecast period
        - forecast_0_temperature_f (float): Temperature in Fahrenheit for first period
        - forecast_0_wind (str): Wind description for first period
        - forecast_0_description (str): Weather description for first period
        - forecast_1_period (str): Name of the second forecast period
        - forecast_1_temperature_f (float): Temperature in Fahrenheit for second period
        - forecast_1_wind (str): Wind description for second period
        - forecast_1_description (str): Weather description for second period
    """
    return {
        "forecast_0_period": "Today",
        "forecast_0_temperature_f": 72.5,
        "forecast_0_wind": "5 mph NW",
        "forecast_0_description": "Partly cloudy with mild temperatures",
        "forecast_1_period": "Tonight",
        "forecast_1_temperature_f": 58.3,
        "forecast_1_wind": "8 mph SE",
        "forecast_1_description": "Mostly clear and cool"
    }

def weather_get_forecast(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get weather forecast for a location based on latitude and longitude.
    
    This function simulates retrieving a weather forecast by calling an external API
    and transforming the flat response into a structured forecast list.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
    
    Returns:
        Dict[str, Any]: Dictionary containing a list of forecast periods with details
            - forecast (List[Dict]): List of forecast periods, each containing:
                - period (str): Name of the time period
                - temperature_f (float): Temperature in Fahrenheit
                - wind (str): Wind speed and direction
                - description (str): Weather condition description
    
    Raises:
        ValueError: If latitude or longitude are outside valid ranges
    """
    # Input validation
    if not isinstance(latitude, (int, float)):
        raise ValueError("Latitude must be a number")
    if not isinstance(longitude, (int, float)):
        raise ValueError("Longitude must be a number")
    if latitude < -90 or latitude > 90:
        raise ValueError("Latitude must be between -90 and 90 degrees")
    if longitude < -180 or longitude > 180:
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get weather data (simulated)
    api_data = call_external_api("weather-get-forecast")
    
    # Construct forecast list from flat API response
    forecast = [
        {
            "period": api_data["forecast_0_period"],
            "temperature_f": api_data["forecast_0_temperature_f"],
            "wind": api_data["forecast_0_wind"],
            "description": api_data["forecast_0_description"]
        },
        {
            "period": api_data["forecast_1_period"],
            "temperature_f": api_data["forecast_1_temperature_f"],
            "wind": api_data["forecast_1_wind"],
            "description": api_data["forecast_1_description"]
        }
    ]
    
    return {"forecast": forecast}