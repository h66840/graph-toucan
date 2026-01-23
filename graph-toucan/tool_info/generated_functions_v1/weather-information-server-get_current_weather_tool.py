from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - city (str): Name of the city
        - country (str): Full name of the country
        - region (str): Administrative region or state
        - weather (str): Current weather condition description
        - temperature_c (float): Temperature in Celsius
        - temperature_f (float): Temperature in Fahrenheit
        - feelslike_c (float): Feels like temperature in Celsius
        - feelslike_f (float): Feels like temperature in Fahrenheit
        - humidity (int): Relative humidity percentage
        - wind_kph (float): Wind speed in km/h
        - wind_mph (float): Wind speed in mph
        - wind_dir (str): Wind direction abbreviation
        - pressure_mb (float): Atmospheric pressure in millibars
        - visibility_km (float): Visibility distance in kilometers
        - uv_index (float): UV radiation index level
        - icon (str): URL path to weather icon image
        - last_updated (str): Timestamp of last update in "YYYY-MM-DD HH:MM" format
    """
    return {
        "city": "Istanbul",
        "country": "Turkey",
        "region": "Istanbul Province",
        "weather": "Puslu",
        "temperature_c": 14.5,
        "temperature_f": 58.1,
        "feelslike_c": 13.2,
        "feelslike_f": 55.8,
        "humidity": 85,
        "wind_kph": 12.6,
        "wind_mph": 7.8,
        "wind_dir": "NE",
        "pressure_mb": 1013.0,
        "visibility_km": 6.0,
        "uv_index": 2.0,
        "icon": "/icons/cloudy.png",
        "last_updated": "2023-10-05 14:30"
    }

def weather_information_server_get_current_weather_tool(city: str) -> Dict[str, Any]:
    """
    Get current weather information for a specific city.
    
    Args:
        city (str): Name of the city to get weather for
    
    Returns:
        Dict containing current weather data including:
        - city (str): name of the city
        - country (str): full name of the country
        - region (str): administrative region or state
        - weather (str): current weather condition description
        - temperature_c (float): temperature in degrees Celsius
        - temperature_f (float): temperature in degrees Fahrenheit
        - feelslike_c (float): apparent temperature in Celsius
        - feelslike_f (float): apparent temperature in Fahrenheit
        - humidity (int): relative humidity as percentage
        - wind_kph (float): wind speed in km/h
        - wind_mph (float): wind speed in mph
        - wind_dir (str): wind direction abbreviation
        - pressure_mb (float): atmospheric pressure in millibars
        - visibility_km (float): visibility distance in kilometers
        - uv_index (float): UV radiation index level
        - icon (str): URL path to weather icon image
        - last_updated (str): timestamp of last update in "YYYY-MM-DD HH:MM" format
    
    Raises:
        ValueError: If city is empty or not provided
    """
    if not city or not city.strip():
        raise ValueError("City name is required")
    
    city = city.strip()
    
    # Call external API to get weather data (simulated)
    api_data = call_external_api("weather-information-server-get_current_weather_tool")
    
    # Construct the result using the API data
    result = {
        "city": api_data["city"],
        "country": api_data["country"],
        "region": api_data["region"],
        "weather": api_data["weather"],
        "temperature_c": api_data["temperature_c"],
        "temperature_f": api_data["temperature_f"],
        "feelslike_c": api_data["feelslike_c"],
        "feelslike_f": api_data["feelslike_f"],
        "humidity": api_data["humidity"],
        "wind_kph": api_data["wind_kph"],
        "wind_mph": api_data["wind_mph"],
        "wind_dir": api_data["wind_dir"],
        "pressure_mb": api_data["pressure_mb"],
        "visibility_km": api_data["visibility_km"],
        "uv_index": api_data["uv_index"],
        "icon": api_data["icon"],
        "last_updated": api_data["last_updated"]
    }
    
    return result