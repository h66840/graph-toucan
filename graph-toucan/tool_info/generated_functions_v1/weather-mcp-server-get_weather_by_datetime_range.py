from typing import Dict, List, Any
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API for a given city and date range.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - city (str): Name of the city in English
        - start_date (str): Start date in ISO 8601 format (YYYY-MM-DD)
        - end_date (str): End date in ISO 8601 format (YYYY-MM-DD)
        - weather_0_time (str): Time of first hourly observation (ISO 8601 format)
        - weather_0_temperature_c (float): Temperature in Celsius for first observation
        - weather_0_humidity_percent (int): Humidity percentage for first observation
        - weather_0_dew_point_c (float): Dew point in Celsius for first observation
        - weather_0_weather_description (str): Weather condition description for first observation
        - weather_1_time (str): Time of second hourly observation (ISO 8601 format)
        - weather_1_temperature_c (float): Temperature in Celsius for second observation
        - weather_1_humidity_percent (int): Humidity percentage for second observation
        - weather_1_dew_point_c (float): Dew point in Celsius for second observation
        - weather_1_weather_description (str): Weather condition description for second observation
    """
    return {
        "city": "London",
        "start_date": "2023-10-01",
        "end_date": "2023-10-02",
        "weather_0_time": "2023-10-01T00:00:00",
        "weather_0_temperature_c": 15.5,
        "weather_0_humidity_percent": 78,
        "weather_0_dew_point_c": 12.1,
        "weather_0_weather_description": "Partly cloudy",
        "weather_1_time": "2023-10-01T01:00:00",
        "weather_1_temperature_c": 14.8,
        "weather_1_humidity_percent": 80,
        "weather_1_dew_point_c": 11.9,
        "weather_1_weather_description": "Clear sky"
    }

def weather_mcp_server_get_weather_by_datetime_range(city: str, start_date: str, end_date: str) -> Dict[str, Any]:
    """
    Get weather information for a specified city between start and end dates.
    
    Args:
        city (str): The name of the city to fetch weather information for. Must be in English.
        start_date (str): Start date in ISO 8601 format (YYYY-MM-DD).
        end_date (str): End date in ISO 8601 format (YYYY-MM-DD).
    
    Returns:
        Dict containing:
        - city (str): Name of the city
        - start_date (str): Start date in ISO 8601 format
        - end_date (str): End date in ISO 8601 format
        - weather (List[Dict]): List of hourly weather observations with time, temperature_c,
          humidity_percent, dew_point_c, and weather_description
    
    Raises:
        ValueError: If dates are not in valid ISO 8601 format or if start_date > end_date
        TypeError: If any input is of incorrect type
    """
    # Input validation
    if not isinstance(city, str) or not city.strip():
        raise ValueError("City must be a non-empty string")
    
    if not isinstance(start_date, str) or not isinstance(end_date, str):
        raise TypeError("Start date and end date must be strings")
    
    try:
        start_dt = datetime.datetime.fromisoformat(start_date)
    except ValueError:
        raise ValueError(f"Start date '{start_date}' is not in valid ISO 8601 format (YYYY-MM-DD)")
    
    try:
        end_dt = datetime.datetime.fromisoformat(end_date)
    except ValueError:
        raise ValueError(f"End date '{end_date}' is not in valid ISO 8601 format (YYYY-MM-DD)")
    
    if start_dt > end_dt:
        raise ValueError("Start date cannot be after end date")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("weather-mcp-server-get_weather_by_datetime_range")
    
    # Construct weather observations list from flattened API response
    weather_observations = [
        {
            "time": api_data["weather_0_time"],
            "temperature_c": api_data["weather_0_temperature_c"],
            "humidity_percent": api_data["weather_0_humidity_percent"],
            "dew_point_c": api_data["weather_0_dew_point_c"],
            "weather_description": api_data["weather_0_weather_description"]
        },
        {
            "time": api_data["weather_1_time"],
            "temperature_c": api_data["weather_1_temperature_c"],
            "humidity_percent": api_data["weather_1_humidity_percent"],
            "dew_point_c": api_data["weather_1_dew_point_c"],
            "weather_description": api_data["weather_1_weather_description"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "city": api_data["city"],
        "start_date": api_data["start_date"],
        "end_date": api_data["end_date"],
        "weather": weather_observations
    }
    
    return result