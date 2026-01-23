from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - city (str): Name of the city for which weather is reported
        - condition (str): Human-readable weather condition description
        - temperature_celsius (float): Current temperature in degrees Celsius
        - relative_humidity_percent (float): Relative humidity at 2 meters as a percentage
        - dew_point_celsius (float): Dew point temperature at 2 meters in degrees Celsius
    """
    return {
        "city": "London",
        "condition": "Partly cloudy",
        "temperature_celsius": 18.5,
        "relative_humidity_percent": 65.0,
        "dew_point_celsius": 12.3
    }

def weather_mcp_server_get_current_weather(city: str) -> Dict[str, Any]:
    """
    Get current weather information for a specified city.
    
    This function retrieves current weather data including temperature, weather condition,
    humidity, and dew point for the given city. The city name must be in English.
    
    Args:
        city (str): The name of the city to fetch weather information for. 
                   If not in English, it should be translated before calling this function.
                   
    Returns:
        Dict[str, Any]: A dictionary containing weather information with the following keys:
            - city (str): name of the city for which weather is reported
            - condition (str): human-readable weather condition description
            - temperature_celsius (float): current temperature in degrees Celsius
            - relative_humidity_percent (float): relative humidity at 2 meters as a percentage
            - dew_point_celsius (float): dew point temperature at 2 meters in degrees Celsius
    
    Raises:
        ValueError: If the city parameter is empty or None
    """
    if not city:
        raise ValueError("City parameter is required")
    
    # Simulate API call to get weather data
    api_data = call_external_api("weather-mcp-server-get_current_weather")
    
    # Construct result using API data
    result = {
        "city": api_data["city"],
        "condition": api_data["condition"],
        "temperature_celsius": api_data["temperature_celsius"],
        "relative_humidity_percent": api_data["relative_humidity_percent"],
        "dew_point_celsius": api_data["dew_point_celsius"]
    }
    
    return result