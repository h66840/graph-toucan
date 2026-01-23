from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external weather API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - location_name (str): Name of the location
        - location_country (str): Country code of the location
        - coordinates_lat (float): Latitude of the location
        - coordinates_lon (float): Longitude of the location
        - weather_condition_main (str): General weather state (e.g., Clear, Rain)
        - weather_condition_description (str): Detailed weather description
        - weather_condition_icon (str): Weather icon code
        - temperature_current (float): Current temperature in °C
        - temperature_feels_like (float): Feels-like temperature in °C
        - temperature_min (float): Minimum temperature in °C
        - temperature_max (float): Maximum temperature in °C
        - humidity (int): Humidity percentage
        - pressure (int): Atmospheric pressure in hPa
        - wind_speed (float): Wind speed in m/s
        - rain_last_hour (float): Rainfall amount in mm over the last hour
        - cloudiness (int): Cloud cover percentage
        - recommendation_0 (str): First recommendation based on weather
        - recommendation_1 (str): Second recommendation based on weather
    """
    return {
        "location_name": "Istanbul",
        "location_country": "TR",
        "coordinates_lat": 41.0082,
        "coordinates_lon": 28.9784,
        "weather_condition_main": "Clouds",
        "weather_condition_description": "overcast clouds",
        "weather_condition_icon": "04d",
        "temperature_current": 18.5,
        "temperature_feels_like": 19.1,
        "temperature_min": 16.0,
        "temperature_max": 21.3,
        "humidity": 72,
        "pressure": 1015,
        "wind_speed": 3.6,
        "rain_last_hour": 0.0,
        "cloudiness": 90,
        "recommendation_0": "Carry a light jacket",
        "recommendation_1": "No need for an umbrella"
    }

def deneme_mcp_server_chat_weather_assistant(message: str) -> Dict[str, Any]:
    """
    Hava durumu asistanı ile sohbet et.
    
    Bu araç kullanıcının mesajlarını analiz eder ve uygun yanıtlar verir.
    Koordinat bilgilerini toplar ve hava durumu sorgular.
    
    Args:
        message (str): Kullanıcının mesajı
        
    Returns:
        Dict containing weather report with the following structure:
        - location (Dict): contains 'name', 'country' fields
        - coordinates (Dict): contains 'lat', 'lon' fields
        - weather_condition (Dict): contains 'main', 'description', 'icon' fields
        - temperature (Dict): contains 'current', 'feels_like', 'min', 'max' fields in °C
        - humidity (int): humidity percentage
        - pressure (int): atmospheric pressure in hPa
        - wind_speed (float): wind speed in m/s
        - rain_last_hour (float): rainfall amount in mm over the last hour
        - cloudiness (int): cloud cover percentage
        - recommendations (List[str]): list of suggested actions or tips based on weather
    """
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    
    if not message.strip():
        raise ValueError("Message cannot be empty or whitespace")
    
    # Fetch simulated external data
    api_data = call_external_api("deneme-mcp-server-chat_weather_assistant")
    
    # Construct nested output structure as per schema
    result = {
        "location": {
            "name": api_data["location_name"],
            "country": api_data["location_country"]
        },
        "coordinates": {
            "lat": api_data["coordinates_lat"],
            "lon": api_data["coordinates_lon"]
        },
        "weather_condition": {
            "main": api_data["weather_condition_main"],
            "description": api_data["weather_condition_description"],
            "icon": api_data["weather_condition_icon"]
        },
        "temperature": {
            "current": api_data["temperature_current"],
            "feels_like": api_data["temperature_feels_like"],
            "min": api_data["temperature_min"],
            "max": api_data["temperature_max"]
        },
        "humidity": api_data["humidity"],
        "pressure": api_data["pressure"],
        "wind_speed": api_data["wind_speed"],
        "rain_last_hour": api_data["rain_last_hour"],
        "cloudiness": api_data["cloudiness"],
        "recommendations": [
            api_data["recommendation_0"],
            api_data["recommendation_1"]
        ]
    }
    
    return result