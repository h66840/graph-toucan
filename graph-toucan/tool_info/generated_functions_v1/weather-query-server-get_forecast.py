from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - forecast_0_period (str): Description of the first forecast period
        - forecast_0_temperature (float): Temperature in Celsius for the first period
        - forecast_0_wind (str): Wind conditions for the first period
        - forecast_0_forecast (str): Weather forecast text for the first period
        - forecast_1_period (str): Description of the second forecast period
        - forecast_1_temperature (float): Temperature in Celsius for the second period
        - forecast_1_wind (str): Wind conditions for the second period
        - forecast_1_forecast (str): Weather forecast text for the second period
    """
    return {
        "forecast_0_period": "Today",
        "forecast_0_temperature": 22.5,
        "forecast_0_wind": "10 km/h NW",
        "forecast_0_forecast": "Sunny with clear skies throughout the day.",
        "forecast_1_period": "Tonight",
        "forecast_1_temperature": 16.3,
        "forecast_1_wind": "5 km/h SE",
        "forecast_1_forecast": "Clear skies with mild temperatures."
    }

def weather_query_server_get_forecast(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get weather forecast for a location based on latitude and longitude.
    
    Args:
        latitude (float): Latitude of the location
        longitude (float): Longitude of the location
    
    Returns:
        Dict containing a list of forecast periods with details:
        - forecast_periods (List[Dict]): list of forecast periods, each containing:
            - period (str): Description of the time period
            - temperature (float): Temperature in Celsius
            - wind (str): Wind speed and direction
            - forecast (str): Detailed weather forecast text
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Fetch simulated external data
    api_data = call_external_api("weather-query-server-get_forecast")
    
    # Construct forecast periods list from flattened API data
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