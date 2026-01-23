from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - location (str): Name of the location including city and country
        - condition (str): General weather condition (e.g., clear, partly cloudy)
        - temperature_current (float): Current temperature in Celsius
        - temperature_feels_like (float): Perceived temperature in Celsius
        - temperature_min (float): Minimum temperature of the day in Celsius
        - temperature_max (float): Maximum temperature of the day in Celsius
        - humidity (int): Relative humidity as percentage
        - pressure (int): Atmospheric pressure in hPa
        - wind_speed (float): Wind speed in meters per second
        - advice_summary (str): Brief summary advice about what to wear or how to prepare
        - advice_details_0 (str): First specific recommendation
        - advice_details_1 (str): Second specific recommendation
    """
    return {
        "location": "Istanbul, Turkey",
        "condition": "Partly Cloudy",
        "temperature_current": 18.5,
        "temperature_feels_like": 19.2,
        "temperature_min": 16.0,
        "temperature_max": 21.0,
        "humidity": 65,
        "pressure": 1013,
        "wind_speed": 3.4,
        "advice_summary": "Light jacket recommended",
        "advice_details_0": "Wear a light jacket in the evening.",
        "advice_details_1": "Stay hydrated during the day."
    }

def weather_forecast_server_with_ai_assistant_get_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Kullanıcı dostu hava durumu asistanı - koordinatlara göre hava durumu getirir.
    
    Bu araç, kullanıcıyla dostane iletişim kurar ve hava durumu bilgilerini
    anlaşılır şekilde sunar.
    
    Args:
        latitude (float): Enlem (-90 ile 90 arasında)
        longitude (float): Boylam (-180 ile 180 arasında)
    
    Returns:
        Dict[str, Any]: Kullanıcı dostu formatta hava durumu bilgileri:
            - location (str): name of the location for which weather is provided, including city and country
            - condition (str): general weather condition such as clear, partly cloudy, etc.
            - temperature_current (float): current temperature in degrees Celsius
            - temperature_feels_like (float): perceived temperature in degrees Celsius
            - temperature_min (float): minimum temperature of the day in degrees Celsius
            - temperature_max (float): maximum temperature of the day in degrees Celsius
            - humidity (int): relative humidity as a percentage
            - pressure (int): atmospheric pressure in hPa
            - wind_speed (float): wind speed in meters per second
            - advice_summary (str): brief summary advice about what to wear or how to prepare for the weather
            - advice_details (List[str]): list of specific recommendations based on weather conditions
    
    Raises:
        ValueError: If latitude or longitude is out of valid range
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get weather data (simulated)
    api_data = call_external_api("weather-forecast-server-with-ai-assistant-get_weather")
    
    # Construct the result with proper nested structure
    result = {
        "location": api_data["location"],
        "condition": api_data["condition"],
        "temperature_current": api_data["temperature_current"],
        "temperature_feels_like": api_data["temperature_feels_like"],
        "temperature_min": api_data["temperature_min"],
        "temperature_max": api_data["temperature_max"],
        "humidity": api_data["humidity"],
        "pressure": api_data["pressure"],
        "wind_speed": api_data["wind_speed"],
        "advice_summary": api_data["advice_summary"],
        "advice_details": [
            api_data["advice_details_0"],
            api_data["advice_details_1"]
        ]
    }
    
    return result