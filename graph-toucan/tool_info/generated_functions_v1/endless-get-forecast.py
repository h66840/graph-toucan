from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather forecast.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - forecast_0_period (str): Description of the first forecast period
        - forecast_0_temperature (int): Temperature in Celsius for the first period
        - forecast_0_wind (str): Wind conditions for the first period
        - forecast_0_condition (str): Weather condition for the first period
        - forecast_1_period (str): Description of the second forecast period
        - forecast_1_temperature (int): Temperature in Celsius for the second period
        - forecast_1_wind (str): Wind conditions for the second period
        - forecast_1_condition (str): Weather condition for the second period
    """
    return {
        "forecast_0_period": "Today",
        "forecast_0_temperature": 22,
        "forecast_0_wind": "10 km/h NW",
        "forecast_0_condition": "Partly cloudy",
        "forecast_1_period": "Tonight",
        "forecast_1_temperature": 16,
        "forecast_1_wind": "5 km/h SE",
        "forecast_1_condition": "Clear"
    }

def endless_get_forecast(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get weather forecast for a location based on latitude and longitude.
    
    This function simulates retrieving a weather forecast by calling an external API
    and transforming the flat response into a structured format with forecast periods.
    
    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)
    
    Returns:
        Dict containing a list of forecast periods with details:
        - forecast_periods (List[Dict]): List of forecast periods, each containing:
            - period (str): Description of the time period
            - temperature (int): Temperature in Celsius
            - wind (str): Wind speed and direction
            - condition (str): Weather condition description
    
    Raises:
        ValueError: If latitude or longitude are not within valid ranges
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get weather data
    api_data = call_external_api("endless-get-forecast")
    
    # Construct forecast periods list from flat API response
    forecast_periods = [
        {
            "period": api_data["forecast_0_period"],
            "temperature": api_data["forecast_0_temperature"],
            "wind": api_data["forecast_0_wind"],
            "condition": api_data["forecast_0_condition"]
        },
        {
            "period": api_data["forecast_1_period"],
            "temperature": api_data["forecast_1_temperature"],
            "wind": api_data["forecast_1_wind"],
            "condition": api_data["forecast_1_condition"]
        }
    ]
    
    # Return structured forecast data
    return {
        "forecast_periods": forecast_periods
    }