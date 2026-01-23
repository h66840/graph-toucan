from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather forecast data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - forecast_0_period (str): Time period for first forecast (e.g., "This Afternoon")
        - forecast_0_temperature (str): Temperature for first period (e.g., "85°F")
        - forecast_0_wind (str): Wind description for first period (e.g., "5 to 10 mph SW")
        - forecast_0_forecast_text (str): Detailed weather description for first period
        - forecast_0_chance_of_precipitation (str): Chance of precipitation for first period (e.g., "20%"), empty if none
        - forecast_1_period (str): Time period for second forecast (e.g., "Tonight")
        - forecast_1_temperature (str): Temperature for second period (e.g., "63°F")
        - forecast_1_wind (str): Wind description for second period (e.g., "0 to 5 mph SSW")
        - forecast_1_forecast_text (str): Detailed weather description for second period
        - forecast_1_chance_of_precipitation (str): Chance of precipitation for second period (e.g., "10%"), empty if none
    """
    return {
        "forecast_0_period": "This Afternoon",
        "forecast_0_temperature": "85°F",
        "forecast_0_wind": "5 to 10 mph SW",
        "forecast_0_forecast_text": "Sunny, with a high near 85. Southwest wind 5 to 10 mph.",
        "forecast_0_chance_of_precipitation": "20%",
        "forecast_1_period": "Tonight",
        "forecast_1_temperature": "63°F",
        "forecast_1_wind": "0 to 5 mph SSW",
        "forecast_1_forecast_text": "Partly cloudy, with a low around 63. Light and variable wind becoming south-southwest 0 to 5 mph.",
        "forecast_1_chance_of_precipitation": ""
    }

def mcp_server_test_get_forecast(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get weather forecast for a location based on latitude and longitude.
    
    Args:
        latitude (float): Latitude of the location (must be between -90 and 90)
        longitude (float): Longitude of the location (must be between -180 and 180)
    
    Returns:
        Dict containing list of forecast periods with detailed weather information:
        - forecast_periods (List[Dict]): List of forecast period dictionaries containing:
            - period (str): The time period for the forecast (e.g., "This Afternoon", "Tonight")
            - temperature (str): Temperature value for the period (e.g., "85°F")
            - wind (str): Description of wind conditions (e.g., "5 to 10 mph SW")
            - forecast_text (str): Detailed weather description for the period
            - chance_of_precipitation (Optional[str]): Chance of rain as percentage string if available
    
    Raises:
        ValueError: If latitude or longitude are outside valid ranges
        TypeError: If inputs are not numeric types
    """
    # Input validation
    if not isinstance(latitude, (int, float)):
        raise TypeError("Latitude must be a number")
    if not isinstance(longitude, (int, float)):
        raise TypeError("Longitude must be a number")
    
    if latitude < -90 or latitude > 90:
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if longitude < -180 or longitude > 180:
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get flattened data
    api_data = call_external_api("mcp-server-test-get_forecast")
    
    # Construct forecast periods list by mapping flat fields to nested structure
    forecast_periods: List[Dict[str, Any]] = []
    
    # Process first forecast period
    period_0: Dict[str, Any] = {
        "period": api_data["forecast_0_period"],
        "temperature": api_data["forecast_0_temperature"],
        "wind": api_data["forecast_0_wind"],
        "forecast_text": api_data["forecast_0_forecast_text"]
    }
    
    # Add chance_of_precipitation only if it has a value
    if api_data["forecast_0_chance_of_precipitation"]:
        period_0["chance_of_precipitation"] = api_data["forecast_0_chance_of_precipitation"]
    
    forecast_periods.append(period_0)
    
    # Process second forecast period
    period_1: Dict[str, Any] = {
        "period": api_data["forecast_1_period"],
        "temperature": api_data["forecast_1_temperature"],
        "wind": api_data["forecast_1_wind"],
        "forecast_text": api_data["forecast_1_forecast_text"]
    }
    
    # Add chance_of_precipitation only if it has a value
    if api_data["forecast_1_chance_of_precipitation"]:
        period_1["chance_of_precipitation"] = api_data["forecast_1_chance_of_precipitation"]
    
    forecast_periods.append(period_1)
    
    return {
        "forecast_periods": forecast_periods
    }