from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - location_latitude (float): Latitude coordinate
        - location_longitude (float): Longitude coordinate
        - location_city (str): City name corresponding to coordinates
        - location_country (str): Country code
        - weather_main_condition (str): Main weather condition (e.g., Clear, Rain)
        - weather_description (str): Detailed weather description
        - weather_icon (str): Weather icon code
        - temperature_current (float): Current temperature
        - temperature_feels_like (float): Feels like temperature
        - temperature_min (float): Minimum temperature
        - temperature_max (float): Maximum temperature
        - temperature_unit (str): Temperature unit (e.g., Celsius, Fahrenheit)
        - atmosphere_pressure (int): Atmospheric pressure in hPa
        - atmosphere_humidity (int): Humidity percentage
        - atmosphere_visibility (int): Visibility in meters
        - wind_speed (float): Wind speed
        - wind_direction (int): Wind direction in degrees
        - wind_unit (str): Wind speed unit
        - cloudiness_percentage (int): Cloud coverage percentage
        - sun_sunrise (int): Sunrise time as Unix timestamp
        - sun_sunset (int): Sunset time as Unix timestamp
        - time_data_time (int): Data calculation time as Unix timestamp
        - time_timezone_offset (int): Timezone offset from UTC in seconds
        - rain_last_1h (float): Rainfall amount in last hour
        - rain_unit (str): Unit for rainfall measurement
    """
    return {
        "location_latitude": 40.7128,
        "location_longitude": -74.006,
        "location_city": "New York",
        "location_country": "US",
        "weather_main_condition": "Clear",
        "weather_description": "clear sky",
        "weather_icon": "01d",
        "temperature_current": 22.5,
        "temperature_feels_like": 23.1,
        "temperature_min": 20.0,
        "temperature_max": 25.0,
        "temperature_unit": "Celsius",
        "atmosphere_pressure": 1013,
        "atmosphere_humidity": 65,
        "atmosphere_visibility": 10000,
        "wind_speed": 3.5,
        "wind_direction": 180,
        "wind_unit": "m/s",
        "cloudiness_percentage": 10,
        "sun_sunrise": 1643219200,
        "sun_sunset": 1643258400,
        "time_data_time": 1643245600,
        "time_timezone_offset": -18000,
        "rain_last_1h": 0.0,
        "rain_unit": "mm"
    }

def weather_forecast_server_get_weather_by_coordinates(
    latitude: float, 
    longitude: float, 
    units: Optional[str] = "metric"
) -> Dict[str, Any]:
    """
    Enlem ve boylam koordinatlarına göre hava durumu bilgilerini getirir.
    
    Args:
        latitude (float): Enlem (-90 ile 90 arasında)
        longitude (float): Boylam (-180 ile 180 arasında)
        units (Optional[str]): Ölçü birimi (metric, imperial, standard). Default: metric
        
    Returns:
        JSON formatında hava durumu bilgileri içeren sözlük. İçerdiği alanlar:
        - location: 'latitude', 'longitude', 'city', 'country' alanlarını içerir
        - weather: 'main_condition', 'description', 'icon' alanlarını içerir
        - temperature: 'current', 'feels_like', 'min', 'max', 'unit' alanlarını içerir
        - atmosphere: 'pressure', 'humidity', 'visibility' alanlarını içerir
        - wind: 'speed', 'direction', 'unit' alanlarını içerir
        - cloudiness: 'percentage' alanını içerir
        - sun: 'sunrise', 'sunset' Unix zaman damgaları
        - time: 'data_time' (Unix timestamp) ve 'timezone_offset' (saniye cinsinden)
        - rain: 'last_1h' yağış miktarı ve 'unit' (varsa)
        
    Raises:
        ValueError: Geçersiz enlem/boylam değerleri için
    """
    # Input validation
    if not isinstance(latitude, (int, float)) or not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be a number between -90 and 90")
    
    if not isinstance(longitude, (int, float)) or not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be a number between -180 and 180")
    
    if units not in [None, "metric", "imperial", "standard"]:
        units = "metric"  # default fallback
    
    # Fetch data from external API simulation
    api_data = call_external_api("weather-forecast-server-get_weather_by_coordinates")
    
    # Construct nested structure matching output schema
    result = {
        "location": {
            "latitude": api_data["location_latitude"],
            "longitude": api_data["location_longitude"],
            "city": api_data["location_city"],
            "country": api_data["location_country"]
        },
        "weather": {
            "main_condition": api_data["weather_main_condition"],
            "description": api_data["weather_description"],
            "icon": api_data["weather_icon"]
        },
        "temperature": {
            "current": api_data["temperature_current"],
            "feels_like": api_data["temperature_feels_like"],
            "min": api_data["temperature_min"],
            "max": api_data["temperature_max"],
            "unit": api_data["temperature_unit"]
        },
        "atmosphere": {
            "pressure": api_data["atmosphere_pressure"],
            "humidity": api_data["atmosphere_humidity"],
            "visibility": api_data["atmosphere_visibility"]
        },
        "wind": {
            "speed": api_data["wind_speed"],
            "direction": api_data["wind_direction"],
            "unit": api_data["wind_unit"]
        },
        "cloudiness": {
            "percentage": api_data["cloudiness_percentage"]
        },
        "sun": {
            "sunrise": api_data["sun_sunrise"],
            "sunset": api_data["sun_sunset"]
        },
        "time": {
            "data_time": api_data["time_data_time"],
            "timezone_offset": api_data["time_timezone_offset"]
        }
    }
    
    # Add rain data if available
    if "rain_last_1h" in api_data and "rain_unit" in api_data:
        result["rain"] = {
            "last_1h": api_data["rain_last_1h"],
            "unit": api_data["rain_unit"]
        }
    
    return result