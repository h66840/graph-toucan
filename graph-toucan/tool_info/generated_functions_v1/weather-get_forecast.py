from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather forecast.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - forecast_0_period (str): Period name for first forecast (e.g., 'Today')
        - forecast_0_temperature (int): Temperature in °F for first period
        - forecast_0_wind (str): Wind description for first period
        - forecast_0_forecast (str): Detailed weather description for first period
        - forecast_1_period (str): Period name for second forecast (e.g., 'Tonight')
        - forecast_1_temperature (int): Temperature in °F for second period
        - forecast_1_wind (str): Wind description for second period
        - forecast_1_forecast (str): Detailed weather description for second period
    """
    return {
        "forecast_0_period": "Today",
        "forecast_0_temperature": 75,
        "forecast_0_wind": "10 mph NW",
        "forecast_0_forecast": "Sunny with clear skies throughout the day.",
        "forecast_1_period": "Tonight",
        "forecast_1_temperature": 58,
        "forecast_1_wind": "5 mph SE",
        "forecast_1_forecast": "Partly cloudy with mild temperatures."
    }

def weather_get_forecast(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get weather forecast for a location based on latitude and longitude.
    
    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location
    
    Returns:
        Dict containing:
            - forecast_periods (List[Dict]): List of forecast periods, each containing:
                - period (str): Name of the period (e.g., 'Today', 'Tonight')
                - temperature (int): Temperature in °F
                - wind (str): Description of wind speed and direction
                - forecast (str): Detailed weather description
    
    Raises:
        ValueError: If latitude or longitude is out of valid range
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Fetch data from external API simulation
    api_data = call_external_api("weather-get_forecast")
    
    # Construct forecast_periods list from flattened API response
    forecast_periods = [
        {
            "period": api_data["forecast_0_period"],
            "temperature": api_data["forecast_0_temperature"],
            "wind": api_data["forecast_0_wind"],
            "forecast": api_data["forecast_0_forecast"]
        },
        {
            "period": api_data["forecast_1_period"],
            "temperature": api_data["forecast_1_temperature"],
            "wind": api_data["forecast_1_wind"],
            "forecast": api_data["forecast_1_forecast"]
        }
    ]
    
    return {
        "forecast_periods": forecast_periods
    }