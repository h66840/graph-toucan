from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - current_condition_0_temp_C (float): Temperature in Celsius
        - current_condition_0_temp_F (float): Temperature in Fahrenheit
        - current_condition_0_feelslikeC (float): Feels like temperature in Celsius
        - current_condition_0_feelslikeF (float): Feels like temperature in Fahrenheit
        - current_condition_0_humidity (int): Humidity percentage
        - current_condition_0_cloudcover (int): Cloud cover percentage
        - current_condition_0_visibility (float): Visibility in km
        - current_condition_0_pressure (float): Atmospheric pressure in hPa
        - current_condition_0_precipMM (float): Precipitation in mm
        - current_condition_0_windspeedKmph (float): Wind speed in km/h
        - current_condition_0_winddirDegree (int): Wind direction in degrees
        - current_condition_0_weatherCode (int): Weather condition code
        - current_condition_0_weatherDesc_0_value (str): Description of weather
        - nearest_area_0_areaName_0_value (str): Name of the area
        - nearest_area_0_country_0_value (str): Country name
        - nearest_area_0_region_0_value (str): Region name
        - nearest_area_0_latitude (float): Latitude of the area
        - nearest_area_0_longitude (float): Longitude of the area
        - nearest_area_0_population (int): Population of the area
        - nearest_area_0_weatherUrl_0_value (str): URL for weather details
        - request_0_query (str): Geographic query string
        - request_0_type (str): Type of request (e.g., LatLon)
        - weather_0_date (str): Forecast date (YYYY-MM-DD)
        - weather_0_avgtempC (float): Average temperature in Celsius
        - weather_0_avgtempF (float): Average temperature in Fahrenheit
        - weather_0_maxtempC (float): Maximum temperature in Celsius
        - weather_0_mintempC (float): Minimum temperature in Celsius
        - weather_0_sunHour (float): Sunshine hours
        - weather_0_totalSnow_cm (float): Total snow in cm
        - weather_0_uvIndex (int): UV index
        - weather_0_hourly_0_time (int): Hourly forecast time (HHMM)
        - weather_0_hourly_0_tempC (float): Hourly temperature in Celsius
        - weather_0_hourly_0_tempF (float): Hourly temperature in Fahrenheit
        - weather_0_hourly_0_windspeedKmph (float): Hourly wind speed in km/h
        - weather_0_hourly_0_winddirDegree (int): Hourly wind direction in degrees
        - weather_0_hourly_0_weatherCode (int): Hourly weather condition code
        - weather_0_hourly_0_weatherDesc_0_value (str): Hourly weather description
        - weather_0_hourly_0_precipMM (float): Hourly precipitation in mm
        - weather_0_astronomy_0_sunrise (str): Sunrise time (HH:MM PM)
        - weather_0_astronomy_0_sunset (str): Sunset time (HH:MM PM)
        - weather_0_astronomy_0_moonrise (str): Moonrise time (HH:MM PM)
        - weather_0_astronomy_0_moonset (str): Moonset time (HH:MM PM)
    """
    return {
        "current_condition_0_temp_C": 22.0,
        "current_condition_0_temp_F": 71.6,
        "current_condition_0_feelslikeC": 24.0,
        "current_condition_0_feelslikeF": 75.2,
        "current_condition_0_humidity": 65,
        "current_condition_0_cloudcover": 40,
        "current_condition_0_visibility": 10.0,
        "current_condition_0_pressure": 1013.0,
        "current_condition_0_precipMM": 0.0,
        "current_condition_0_windspeedKmph": 15.0,
        "current_condition_0_winddirDegree": 180,
        "current_condition_0_weatherCode": 113,
        "current_condition_0_weatherDesc_0_value": "Partly Cloudy",
        "nearest_area_0_areaName_0_value": "London",
        "nearest_area_0_country_0_value": "United Kingdom",
        "nearest_area_0_region_0_value": "Greater London",
        "nearest_area_0_latitude": 51.5074,
        "nearest_area_0_longitude": -0.1278,
        "nearest_area_0_population": 9648110,
        "nearest_area_0_weatherUrl_0_value": "http://www.worldweatheronline.com/london-weather-text.aspx",
        "request_0_query": "51.5074,-0.1278",
        "request_0_type": "LatLon",
        "weather_0_date": "2023-10-05",
        "weather_0_avgtempC": 18.0,
        "weather_0_avgtempF": 64.4,
        "weather_0_maxtempC": 21.0,
        "weather_0_mintempC": 15.0,
        "weather_0_sunHour": 6.5,
        "weather_0_totalSnow_cm": 0.0,
        "weather_0_uvIndex": 4,
        "weather_0_hourly_0_time": 600,
        "weather_0_hourly_0_tempC": 16.0,
        "weather_0_hourly_0_tempF": 60.8,
        "weather_0_hourly_0_windspeedKmph": 12.0,
        "weather_0_hourly_0_winddirDegree": 170,
        "weather_0_hourly_0_weatherCode": 116,
        "weather_0_hourly_0_weatherDesc_0_value": "Partly cloudy",
        "weather_0_hourly_0_precipMM": 0.1,
        "weather_0_astronomy_0_sunrise": "6:04 AM",
        "weather_0_astronomy_0_sunset": "6:28 PM",
        "weather_0_astronomy_0_moonrise": "3:15 PM",
        "weather_0_astronomy_0_moonset": "12:47 AM"
    }

def region_weather_get_weather(region_name: str) -> Dict[str, Any]:
    """
    MCP handler to get weather information for a specified region.
    
    Args:
        region_name (str): Name of the region to get weather for
        
    Returns:
        dict: Weather information for the specified region with the following structure:
            - current_condition (List[Dict]): List of current weather observations containing:
                temp_C, temp_F, feelslikeC, feelslikeF, humidity, cloudcover, visibility,
                pressure, precipMM, windspeedKmph, winddirDegree, weatherCode, weatherDesc
            - nearest_area (List[Dict]): List of geolocated area details including:
                areaName, country, region, latitude, longitude, population, weatherUrl
            - request (List[Dict]): Details of the original query including:
                query, type
            - weather (List[Dict]): Daily forecast data with:
                date, avgtempC, avgtempF, maxtempC, mintempC, sunHour, totalSnow_cm,
                uvIndex, hourly (list of hourly forecasts), astronomy (sunrise/sunset, moon data)
                
    Raises:
        ValueError: If region_name is empty or not a string
    """
    # Input validation
    if not region_name:
        raise ValueError("region_name is required")
    if not isinstance(region_name, str):
        raise ValueError("region_name must be a string")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("region-weather-get_weather")
    
    # Construct current_condition list
    current_condition = [
        {
            "temp_C": api_data["current_condition_0_temp_C"],
            "temp_F": api_data["current_condition_0_temp_F"],
            "feelslikeC": api_data["current_condition_0_feelslikeC"],
            "feelslikeF": api_data["current_condition_0_feelslikeF"],
            "humidity": api_data["current_condition_0_humidity"],
            "cloudcover": api_data["current_condition_0_cloudcover"],
            "visibility": api_data["current_condition_0_visibility"],
            "pressure": api_data["current_condition_0_pressure"],
            "precipMM": api_data["current_condition_0_precipMM"],
            "windspeedKmph": api_data["current_condition_0_windspeedKmph"],
            "winddirDegree": api_data["current_condition_0_winddirDegree"],
            "weatherCode": api_data["current_condition_0_weatherCode"],
            "weatherDesc": [
                {"value": api_data["current_condition_0_weatherDesc_0_value"]}
            ]
        }
    ]
    
    # Construct nearest_area list
    nearest_area = [
        {
            "areaName": [
                {"value": api_data["nearest_area_0_areaName_0_value"]}
            ],
            "country": [
                {"value": api_data["nearest_area_0_country_0_value"]}
            ],
            "region": [
                {"value": api_data["nearest_area_0_region_0_value"]}
            ],
            "latitude": api_data["nearest_area_0_latitude"],
            "longitude": api_data["nearest_area_0_longitude"],
            "population": api_data["nearest_area_0_population"],
            "weatherUrl": [
                {"value": api_data["nearest_area_0_weatherUrl_0_value"]}
            ]
        }
    ]
    
    # Construct request list
    request = [
        {
            "query": api_data["request_0_query"],
            "type": api_data["request_0_type"]
        }
    ]
    
    # Construct hourly forecast list
    hourly_forecast = [
        {
            "time": api_data["weather_0_hourly_0_time"],
            "tempC": api_data["weather_0_hourly_0_tempC"],
            "tempF": api_data["weather_0_hourly_0_tempF"],
            "windspeedKmph": api_data["weather_0_hourly_0_windspeedKmph"],
            "winddirDegree": api_data["weather_0_hourly_0_winddirDegree"],
            "weatherCode": api_data["weather_0_hourly_0_weatherCode"],
            "weatherDesc": [
                {"value": api_data["weather_0_hourly_0_weatherDesc_0_value"]}
            ],
            "precipMM": api_data["weather_0_hourly_0_precipMM"]
        }
    ]
    
    # Construct astronomy data
    astronomy_data = [
        {
            "sunrise": api_data["weather_0_astronomy_0_sunrise"],
            "sunset": api_data["weather_0_astronomy_0_sunset"],
            "moonrise": api_data["weather_0_astronomy_0_moonrise"],
            "moonset": api_data["weather_0_astronomy_0_moonset"]
        }
    ]
    
    # Construct weather forecast list
    weather = [
        {
            "date": api_data["weather_0_date"],
            "avgtempC": api_data["weather_0_avgtempC"],
            "avgtempF": api_data["weather_0_avgtempF"],
            "maxtempC": api_data["weather_0_maxtempC"],
            "mintempC": api_data["weather_0_mintempC"],
            "sunHour": api_data["weather_0_sunHour"],
            "totalSnow_cm": api_data["weather_0_totalSnow_cm"],
            "uvIndex": api_data["weather_0_uvIndex"],
            "hourly": hourly_forecast,
            "astronomy": astronomy_data
        }
    ]
    
    # Construct final result
    result = {
        "current_condition": current_condition,
        "nearest_area": nearest_area,
        "request": request,
        "weather": weather
    }
    
    return result