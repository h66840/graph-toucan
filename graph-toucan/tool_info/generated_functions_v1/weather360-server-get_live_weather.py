from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather360-server-get_live_weather.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - current_time (str): Current time in ISO format
        - current_temperature_2m (float): Temperature at 2m height in °C
        - current_relative_humidity_2m (int): Relative humidity at 2m in %
        - current_apparent_temperature (float): Apparent temperature in °C
        - current_is_day (int): 1 if day, 0 if night
        - current_precipitation (float): Precipitation in mm
        - current_rain (float): Rain volume in mm
        - current_showers (float): Showers volume in mm
        - current_snowfall (float): Snowfall in cm
        - current_weather_code (int): Weather condition code
        - current_cloud_cover (int): Cloud cover in %
        - current_pressure_msl (float): Mean sea level pressure in hPa
        - current_surface_pressure (float): Surface pressure in hPa
        - current_wind_speed_10m (float): Wind speed at 10m in km/h
        - current_wind_direction_10m (int): Wind direction at 10m in degrees
        - current_wind_gusts_10m (float): Wind gusts at 10m in km/h
        - current_cape (float): Convective available potential energy in J/kg
        - current_freezing_level_height (float): Freezing level height in meters
        - hourly_00_00_temperature_2m (float): Hourly temperature at 00:00
        - hourly_00_00_relative_humidity_2m (int): Hourly humidity at 00:00
        - hourly_00_00_dew_point_2m (float): Dew point at 2m at 00:00
        - hourly_00_00_apparent_temperature (float): Apparent temp at 00:00
        - hourly_00_00_precipitation_probability (int): Precipitation probability at 00:00 in %
        - hourly_00_00_precipitation (float): Precipitation at 00:00 in mm
        - hourly_00_00_rain (float): Rain at 00:00 in mm
        - hourly_00_00_showers (float): Showers at 00:00 in mm
        - hourly_00_00_snowfall (float): Snowfall at 00:00 in cm
        - hourly_00_00_snow_depth (float): Snow depth at 00:00 in meters
        - hourly_00_00_weather_code (int): Weather code at 00:00
        - hourly_00_00_cloud_cover (int): Cloud cover at 00:00 in %
        - hourly_00_00_cloud_cover_low (int): Low cloud cover at 00:00 in %
        - hourly_00_00_cloud_cover_mid (int): Mid cloud cover at 00:00 in %
        - hourly_00_00_cloud_cover_high (int): High cloud cover at 00:00 in %
        - hourly_00_00_visibility (float): Visibility at 00:00 in meters
        - hourly_00_00_evapotranspiration (float): Evapotranspiration at 00:00 in mm
        - hourly_00_00_wind_speed_10m (float): Wind speed at 10m at 00:00 in km/h
        - hourly_00_00_wind_direction_10m (int): Wind direction at 10m at 00:00 in degrees
        - hourly_00_00_wind_gusts_10m (float): Wind gusts at 10m at 00:00 in km/h
        - hourly_00_00_uv_index (float): UV index at 00:00
        - hourly_00_00_uv_index_clear_sky (float): Clear sky UV index at 00:00
        - hourly_00_00_is_day (int): 1 if day, 0 if night at 00:00
        - hourly_00_00_cape (float): CAPE at 00:00 in J/kg
        - hourly_00_00_surface_pressure (float): Surface pressure at 00:00 in hPa
        - hourly_00_00_pressure_msl (float): MSL pressure at 00:00 in hPa
        - daily_2023_10_05_weather_code (int): Daily weather code for 2023-10-05
        - daily_2023_10_05_temperature_2m_max (float): Max temp at 2m on 2023-10-05
        - daily_2023_10_05_temperature_2m_min (float): Min temp at 2m on 2023-10-05
        - daily_2023_10_05_apparent_temperature_max (float): Max apparent temp on 2023-10-05
        - daily_2023_10_05_apparent_temperature_min (float): Min apparent temp on 2023-10-05
        - daily_2023_10_05_sunrise (str): Sunrise time on 2023-10-05
        - daily_2023_10_05_sunset (str): Sunset time on 2023-10-05
        - daily_2023_10_05_daylight_duration (float): Daylight duration in seconds
        - daily_2023_10_05_sunshine_duration (float): Sunshine duration in seconds
        - daily_2023_10_05_uv_index_max (float): Max UV index on 2023-10-05
        - daily_2023_10_05_uv_index_clear_sky_max (float): Max clear sky UV index on 2023-10-05
        - daily_2023_10_05_precipitation_sum (float): Total precipitation on 2023-10-05 in mm
        - daily_2023_10_05_rain_sum (float): Total rain on 2023-10-05 in mm
        - daily_2023_10_05_showers_sum (float): Total showers on 2023-10-05 in mm
        - daily_2023_10_05_snowfall_sum (float): Total snowfall on 2023-10-05 in cm
        - daily_2023_10_05_precipitation_hours (float): Hours with precipitation on 2023-10-05
        - daily_2023_10_05_precipitation_probability_max (int): Max precipitation probability on 2023-10-05
        - daily_2023_10_05_wind_speed_10m_max (float): Max wind speed at 10m on 2023-10-05 in km/h
        - daily_2023_10_05_wind_gusts_10m_max (float): Max wind gusts at 10m on 2023-10-05 in km/h
        - daily_2023_10_05_wind_direction_10m_dominant (int): Dominant wind direction on 2023-10-05 in degrees
        - daily_2023_10_05_shortwave_radiation_sum (float): Shortwave radiation sum in MJ/m²
        - daily_2023_10_05_et0_fao_evapotranspiration (float): Evapotranspiration on 2023-10-05 in mm
    """
    return {
        "current_time": "2023-10-05T12:00:00",
        "current_temperature_2m": 22.5,
        "current_relative_humidity_2m": 65,
        "current_apparent_temperature": 24.1,
        "current_is_day": 1,
        "current_precipitation": 0.0,
        "current_rain": 0.0,
        "current_showers": 0.0,
        "current_snowfall": 0.0,
        "current_weather_code": 1,
        "current_cloud_cover": 30,
        "current_pressure_msl": 1013.25,
        "current_surface_pressure": 1008.7,
        "current_wind_speed_10m": 12.5,
        "current_wind_direction_10m": 180,
        "current_wind_gusts_10m": 20.0,
        "current_cape": 500.0,
        "current_freezing_level_height": 3500.0,
        "hourly_00_00_temperature_2m": 18.0,
        "hourly_00_00_relative_humidity_2m": 75,
        "hourly_00_00_dew_point_2m": 14.2,
        "hourly_00_00_apparent_temperature": 18.0,
        "hourly_00_00_precipitation_probability": 10,
        "hourly_00_00_precipitation": 0.1,
        "hourly_00_00_rain": 0.1,
        "hourly_00_00_showers": 0.0,
        "hourly_00_00_snowfall": 0.0,
        "hourly_00_00_snow_depth": 0.0,
        "hourly_00_00_weather_code": 2,
        "hourly_00_00_cloud_cover": 50,
        "hourly_00_00_cloud_cover_low": 30,
        "hourly_00_00_cloud_cover_mid": 20,
        "hourly_00_00_cloud_cover_high": 10,
        "hourly_00_00_visibility": 10000.0,
        "hourly_00_00_evapotranspiration": 0.5,
        "hourly_00_00_wind_speed_10m": 10.0,
        "hourly_00_00_wind_direction_10m": 170,
        "hourly_00_00_wind_gusts_10m": 18.0,
        "hourly_00_00_uv_index": 0.5,
        "hourly_00_00_uv_index_clear_sky": 1.0,
        "hourly_00_00_is_day": 0,
        "hourly_00_00_cape": 200.0,
        "hourly_00_00_surface_pressure": 1010.0,
        "hourly_00_00_pressure_msl": 1015.0,
        "daily_2023_10_05_weather_code": 1,
        "daily_2023_10_05_temperature_2m_max": 25.0,
        "daily_2023_10_05_temperature_2m_min": 16.0,
        "daily_2023_10_05_apparent_temperature_max": 26.5,
        "daily_2023_10_05_apparent_temperature_min": 17.0,
        "daily_2023_10_05_sunrise": "2023-10-05T06:15:00",
        "daily_2023_10_05_sunset": "2023-10-05T18:25:00",
        "daily_2023_10_05_daylight_duration": 42600.0,
        "daily_2023_10_05_sunshine_duration": 35400.0,
        "daily_2023_10_05_uv_index_max": 5.0,
        "daily_2023_10_05_uv_index_clear_sky_max": 6.0,
        "daily_2023_10_05_precipitation_sum": 0.5,
        "daily_2023_10_05_rain_sum": 0.5,
        "daily_2023_10_05_showers_sum": 0.0,
        "daily_2023_10_05_snowfall_sum": 0.0,
        "daily_2023_10_05_precipitation_hours": 2.0,
        "daily_2023_10_05_precipitation_probability_max": 40,
        "daily_2023_10_05_wind_speed_10m_max": 25.0,
        "daily_2023_10_05_wind_gusts_10m_max": 40.0,
        "daily_2023_10_05_wind_direction_10m_dominant": 185,
        "daily_2023_10_05_shortwave_radiation_sum": 15.0,
        "daily_2023_10_05_et0_fao_evapotranspiration": 3.2
    }

def weather360_server_get_live_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get live weather details for a given latitude and longitude.
    
    This function retrieves current weather conditions, hourly forecast,
    and daily summary for the specified geographic coordinates.
    
    Args:
        latitude (float): Latitude coordinate in decimal degrees (required)
        longitude (float): Longitude coordinate in decimal degrees (required)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - current (Dict): Current weather data with time, temperature, humidity,
              precipitation, wind, and other meteorological parameters
            - hourly (Dict): Time-indexed hourly weather forecast with HH:MM keys
              containing temperature, precipitation probability, wind, UV index, etc.
            - daily (Dict): Date-indexed daily weather summary with YYYY-MM-DD keys
              containing daily extremes, sunrise/sunset, radiation, and other metrics
    
    Raises:
        ValueError: If latitude is not between -90 and 90 or
                    if longitude is not between -180 and 180
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("weather360-server-get_live_weather")
    
    # Construct current weather data
    current = {
        "time": api_data["current_time"],
        "temperature_2m": api_data["current_temperature_2m"],
        "relative_humidity_2m": api_data["current_relative_humidity_2m"],
        "apparent_temperature": api_data["current_apparent_temperature"],
        "is_day": api_data["current_is_day"],
        "precipitation": api_data["current_precipitation"],
        "rain": api_data["current_rain"],
        "showers": api_data["current_showers"],
        "snowfall": api_data["current_snowfall"],
        "weather_code": api_data["current_weather_code"],
        "cloud_cover": api_data["current_cloud_cover"],
        "pressure_msl": api_data["current_pressure_msl"],
        "surface_pressure": api_data["current_surface_pressure"],
        "wind_speed_10m": api_data["current_wind_speed_10m"],
        "wind_direction_10m": api_data["current_wind_direction_10m"],
        "wind_gusts_10m": api_data["current_wind_gusts_10m"],
        "cape": api_data["current_cape"],
        "freezing_level_height": api_data["current_freezing_level_height"]
    }
    
    # Construct hourly forecast
    hourly = {
        "00:00": {
            "temperature_2m": api_data["hourly_00_00_temperature_2m"],
            "relative_humidity_2m": api_data["hourly_00_00_relative_humidity_2m"],
            "dew_point_2m": api_data["hourly_00_00_dew_point_2m"],
            "apparent_temperature": api_data["hourly_00_00_apparent_temperature"],
            "precipitation_probability": api_data["hourly_00_00_precipitation_probability"],
            "precipitation": api_data["hourly_00_00_precipitation"],
            "rain": api_data["hourly_00_00_rain"],
            "showers": api_data["hourly_00_00_showers"],
            "snowfall": api_data["hourly_00_00_snowfall"],
            "snow_depth": api_data["hourly_00_00_snow_depth"],
            "weather_code": api_data["hourly_00_00_weather_code"],
            "cloud_cover": api_data["hourly_00_00_cloud_cover"],
            "cloud_cover_low": api_data["hourly_00_00_cloud_cover_low"],
            "cloud_cover_mid": api_data["hourly_00_00_cloud_cover_mid"],
            "cloud_cover_high": api_data["hourly_00_00_cloud_cover_high"],
            "visibility": api_data["hourly_00_00_visibility"],
            "evapotranspiration": api_data["hourly_00_00_evapotranspiration"],
            "wind_speed_10m": api_data["hourly_00_00_wind_speed_10m"],
            "wind_direction_10m": api_data["hourly_00_00_wind_direction_10m"],
            "wind_gusts_10m": api_data["hourly_00_00_wind_gusts_10m"],
            "uv_index": api_data["hourly_00_00_uv_index"],
            "uv_index_clear_sky": api_data["hourly_00_00_uv_index_clear_sky"],
            "is_day": api_data["hourly_00_00_is_day"],
            "cape": api_data["hourly_00_00_cape"],
            "surface_pressure": api_data["hourly_00_00_surface_pressure"],
            "pressure_msl": api_data["hourly_00_00_pressure_msl"]
        }
    }
    
    # Construct daily summary
    daily = {
        "2023-10-05": {
            "weather_code": api_data["daily_2023_10_05_weather_code"],
            "temperature_2m_max": api_data["daily_2023_10_05_temperature_2m_max"],
            "temperature_2m_min": api_data["daily_2023_10_05_temperature_2m_min"],
            "apparent_temperature_max": api_data["daily_2023_10_05_apparent_temperature_max"],
            "apparent_temperature_min": api_data["daily_2023_10_05_apparent_temperature_min"],
            "sunrise": api_data["daily_2023_10_05_sunrise"],
            "sunset": api_data["daily_2023_10_05_sunset"],
            "daylight_duration": api_data["daily_2023_10_05_daylight_duration"],
            "sunshine_duration": api_data["daily_2023_10_05_sunshine_duration"],
            "uv_index_max": api_data["daily_2023_10_05_uv_index_max"],
            "uv_index_clear_sky_max": api_data["daily_2023_10_05_uv_index_clear_sky_max"],
            "precipitation_sum": api_data["daily_2023_10_05_precipitation_sum"],
            "rain_sum": api_data["daily_2023_10_05_rain_sum"],
            "showers_sum": api_data["daily_2023_10_05_showers_sum"],
            "snowfall_sum": api_data["daily_2023_10_05_snowfall_sum"],
            "precipitation_hours": api_data["daily_2023_10_05_precipitation_hours"],
            "precipitation_probability_max": api_data["daily_2023_10_05_precipitation_probability_max"],
            "wind_speed_10m_max": api_data["daily_2023_10_05_wind_speed_10m_max"],
            "wind_gusts_10m_max": api_data["daily_2023_10_05_wind_gusts_10m_max"],
            "wind_direction_10m_dominant": api_data["daily_2023_10_05_wind_direction_10m_dominant"],
            "shortwave_radiation_sum": api_data["daily_2023_10_05_shortwave_radiation_sum"],
            "et0_fao_evapotranspiration": api_data["daily_2023_10_05_et0_fao_evapotranspiration"]
        }
    }
    
    return {
        "current": current,
        "hourly": hourly,
        "daily": daily
    }