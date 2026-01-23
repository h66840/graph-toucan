from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - location_latitude (float): Latitude of the city
        - location_longitude (float): Longitude of the city
        - location_city (str): City name
        - location_country (str): Country code
        - weather_main_condition (str): Main weather condition (e.g., Clear, Clouds)
        - weather_description (str): Detailed weather description
        - weather_icon (str): Weather icon code
        - temperature_current (float): Current temperature
        - temperature_feels_like (float): Feels like temperature
        - temperature_min (float): Minimum temperature
        - temperature_max (float): Maximum temperature
        - temperature_unit (str): Temperature unit (kelvin, celsius, fahrenheit)
        - atmosphere_pressure (int): Atmospheric pressure in hPa
        - atmosphere_humidity (int): Humidity percentage
        - atmosphere_visibility (int): Visibility in meters
        - wind_speed (float): Wind speed
        - wind_direction (int): Wind direction in degrees
        - wind_unit (str): Wind speed unit (m/s, mph, etc.)
        - cloudiness_percentage (int): Cloud coverage percentage
        - sun_sunrise (int): Sunrise time as Unix timestamp
        - sun_sunset (int): Sunset time as Unix timestamp
        - time_data_time (int): Data retrieval time as Unix timestamp
        - time_timezone_offset (int): Timezone offset in seconds
    """
    return {
        "location_latitude": 41.0082,
        "location_longitude": 28.9784,
        "location_city": "Istanbul",
        "location_country": "TR",
        "weather_main_condition": "Clear",
        "weather_description": "clear sky",
        "weather_icon": "01d",
        "temperature_current": 22.5,
        "temperature_feels_like": 24.1,
        "temperature_min": 20.3,
        "temperature_max": 25.6,
        "temperature_unit": "celsius",
        "atmosphere_pressure": 1012,
        "atmosphere_humidity": 65,
        "atmosphere_visibility": 10000,
        "wind_speed": 3.6,
        "wind_direction": 180,
        "wind_unit": "m/s",
        "cloudiness_percentage": 10,
        "sun_sunrise": 1678881245,
        "sun_sunset": 1678926433,
        "time_data_time": 1678897645,
        "time_timezone_offset": 10800
    }

def weather_forecast_server_get_weather_by_city(
    city_name: str, 
    country_code: Optional[str] = None, 
    units: Optional[str] = None
) -> Dict[str, Any]:
    """
    Şehir adına göre hava durumu bilgilerini getirir.
    
    Args:
        city_name (str): Şehir adı
        country_code (str, optional): Ülke kodu (örn: TR, US)
        units (str, optional): Ölçü birimi (metric, imperial, standard). Varsayılan: metric (celsius)
    
    Returns:
        Dict[str, Any]: JSON formatında hava durumu bilgileri şemasına uygun yapıda:
            - location (Dict): 'latitude', 'longitude', 'city', 'country' alanlarını içerir
            - weather (Dict): 'main_condition', 'description', 'icon' alanlarını içerir
            - temperature (Dict): 'current', 'feels_like', 'min', 'max', 'unit' alanlarını içerir
            - atmosphere (Dict): 'pressure', 'humidity', 'visibility' alanlarını içerir
            - wind (Dict): 'speed', 'direction', 'unit' alanlarını içerir
            - cloudiness (Dict): 'percentage' alanını içerir
            - sun (Dict): 'sunrise', 'sunset' alanlarını içerir (Unix zaman damgaları)
            - time (Dict): 'data_time', 'timezone_offset' alanlarını içerir (Unix zaman damgası ve saniye cinsinden ofset)
    
    Raises:
        ValueError: Gerekli parametreler eksikse veya geçersizse
    """
    # Input validation
    if not city_name or not city_name.strip():
        raise ValueError("city_name is required and cannot be empty")
    
    city_name = city_name.strip()
    
    # Validate units parameter if provided
    valid_units = {"metric", "imperial", "standard"}
    if units and units not in valid_units:
        raise ValueError(f"units must be one of {valid_units}")
    
    # Default to metric if units not specified
    if not units:
        units = "metric"
    
    # Call external API to get weather data (returns flat structure)
    api_data = call_external_api("weather-forecast-server-get_weather_by_city")
    
    # Map flat API response to nested output schema
    result = {
        "location": {
            "latitude": float(api_data["location_latitude"]),
            "longitude": float(api_data["location_longitude"]),
            "city": str(api_data["location_city"]),
            "country": str(api_data["location_country"])
        },
        "weather": {
            "main_condition": str(api_data["weather_main_condition"]),
            "description": str(api_data["weather_description"]),
            "icon": str(api_data["weather_icon"])
        },
        "temperature": {
            "current": float(api_data["temperature_current"]),
            "feels_like": float(api_data["temperature_feels_like"]),
            "min": float(api_data["temperature_min"]),
            "max": float(api_data["temperature_max"]),
            "unit": str(api_data["temperature_unit"])
        },
        "atmosphere": {
            "pressure": int(api_data["atmosphere_pressure"]),
            "humidity": int(api_data["atmosphere_humidity"]),
            "visibility": int(api_data["atmosphere_visibility"])
        },
        "wind": {
            "speed": float(api_data["wind_speed"]),
            "direction": int(api_data["wind_direction"]),
            "unit": str(api_data["wind_unit"])
        },
        "cloudiness": {
            "percentage": int(api_data["cloudiness_percentage"])
        },
        "sun": {
            "sunrise": int(api_data["sun_sunrise"]),
            "sunset": int(api_data["sun_sunset"])
        },
        "time": {
            "data_time": int(api_data["time_data_time"]),
            "timezone_offset": int(api_data["time_timezone_offset"])
        }
    }
    
    # Apply business logic based on input parameters
    # Update city and country if provided
    result["location"]["city"] = city_name
    if country_code:
        result["location"]["country"] = country_code.upper()
    
    # Adjust temperature unit display based on requested units
    unit_map = {
        "metric": "celsius",
        "imperial": "fahrenheit",
        "standard": "kelvin"
    }
    result["temperature"]["unit"] = unit_map.get(units, "celsius")
    
    return result