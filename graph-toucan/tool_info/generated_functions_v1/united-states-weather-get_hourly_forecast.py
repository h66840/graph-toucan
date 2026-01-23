from typing import Dict, Any, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for US weather hourly forecast.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - location (str): Geographic coordinates in "lat,lng" format
        - updated (str): Timestamp of when the forecast was last updated
        - forecast_hours (int): Number of hours covered in the forecast
        - hourly_0_datetime (str): Datetime of first hourly forecast
        - hourly_0_temperature_f (float): Temperature in Fahrenheit for first hour
        - hourly_0_temperature_c (float): Temperature in Celsius for first hour
        - hourly_0_condition (str): Weather condition description for first hour
        - hourly_0_precipitation_chance_pct (int): Precipitation chance percentage for first hour
        - hourly_1_datetime (str): Datetime of second hourly forecast
        - hourly_1_temperature_f (float): Temperature in Fahrenheit for second hour
        - hourly_1_temperature_c (float): Temperature in Celsius for second hour
        - hourly_1_condition (str): Weather condition description for second hour
        - hourly_1_precipitation_chance_pct (int): Precipitation chance percentage for second hour
    """
    return {
        "location": "40.7128,-74.0060",
        "updated": "2023-10-15 14:30:00",
        "forecast_hours": 24,
        "hourly_0_datetime": "2023-10-15 15:00:00",
        "hourly_0_temperature_f": 72.5,
        "hourly_0_temperature_c": 22.5,
        "hourly_0_condition": "Partly cloudy",
        "hourly_0_precipitation_chance_pct": 10,
        "hourly_1_datetime": "2023-10-15 16:00:00",
        "hourly_1_temperature_f": 71.0,
        "hourly_1_temperature_c": 21.7,
        "hourly_1_condition": "Mostly sunny",
        "hourly_1_precipitation_chance_pct": 5,
    }

def united_states_weather_get_hourly_forecast(hours: int = 24, location: str = "") -> Dict[str, Any]:
    """
    Get hour-by-hour weather forecast for a location in the United States.
    
    This function provides detailed hourly weather conditions including temperature,
    conditions, and precipitation probability for up to 48 hours. It's ideal for answering
    questions about short-term weather patterns like "Will it rain this afternoon?" or
    "What's the hourly forecast for New York?"
    
    Args:
        hours (int, optional): Number of hours to forecast (1-48, default 24)
        location (str): US location as coordinates (lat,lng) in decimal degrees. 
                       Example: '40.7128,-74.0060' for New York City.
                       Must be within US boundaries including states, territories, and coastal waters.
    
    Returns:
        Dict containing:
        - location (str): geographic coordinates in "lat,lng" format
        - updated (str): timestamp of when the forecast was last updated
        - forecast_hours (int): number of hours covered in the forecast
        - hourly (List[Dict]): list of hourly weather conditions with keys:
            - datetime (str)
            - temperature_f (float)
            - temperature_c (float)
            - condition (str)
            - precipitation_chance_pct (int)
    
    Raises:
        ValueError: If hours is not between 1-48 or if location is invalid
    """
    # Input validation
    if not location:
        raise ValueError("Location is required")
        
    if not isinstance(hours, int) or hours < 1 or hours > 48:
        raise ValueError("Hours must be an integer between 1 and 48")
    
    # Validate location format (lat,lng)
    try:
        lat_str, lng_str = location.split(',')
        lat = float(lat_str.strip())
        lng = float(lng_str.strip())
        
        # Basic US boundary check (continental US + common territories)
        if not (-145 <= lng <= -65 and 20 <= lat <= 50):
            # Allow specific territories
            us_territories = [
                (18.2208, -66.5901),  # Puerto Rico
                (14.5995, -61.0007),  # Virgin Islands
                (-14.2710, -170.1322), # American Samoa
                (13.4443, 144.7937),  # Guam
                (15.0979, 145.6760),  # Northern Mariana Islands
            ]
            is_valid_territory = any(
                abs(lat - t_lat) < 20 and abs(lng - t_lng) < 20 
                for t_lat, t_lng in us_territories
            )
            if not is_valid_territory:
                raise ValueError("Location must be within US boundaries")
                
    except (ValueError, IndexError):
        raise ValueError("Location must be in 'lat,lng' format with valid decimal degrees")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("united-states-weather-get_hourly_forecast")
    
    # Construct the result structure from flat API data
    result = {
        "location": api_data["location"],
        "updated": api_data["updated"],
        "forecast_hours": min(api_data["forecast_hours"], hours),  # Respect requested hours
        "hourly": [
            {
                "datetime": api_data["hourly_0_datetime"],
                "temperature_f": api_data["hourly_0_temperature_f"],
                "temperature_c": api_data["hourly_0_temperature_c"],
                "condition": api_data["hourly_0_condition"],
                "precipitation_chance_pct": api_data["hourly_0_precipitation_chance_pct"]
            },
            {
                "datetime": api_data["hourly_1_datetime"],
                "temperature_f": api_data["hourly_1_temperature_f"],
                "temperature_c": api_data["hourly_1_temperature_c"],
                "condition": api_data["hourly_1_condition"],
                "precipitation_chance_pct": api_data["hourly_1_precipitation_chance_pct"]
            }
        ]
    }
    
    return result