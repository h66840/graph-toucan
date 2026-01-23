from typing import Dict, Any, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather forecast data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - location (str): coordinates in "lat,lng" format
        - updated (str): timestamp of last update in "M/D/YYYY, H:MM AM/PM (local time)" format
        - day_0_period (str): "Day" for first period
        - day_0_temperature (str): temperature for first day period
        - day_0_conditions (str): weather conditions for first day period
        - day_0_precipitation_chance (str): precipitation chance for first day period
        - day_0_wind (str): wind details for first day period
        - day_0_detailed_description (str): detailed description for first day period
        - night_0_period (str): "Night" for first night period
        - night_0_temperature (str): temperature for first night period
        - night_0_conditions (str): weather conditions for first night period
        - night_0_precipitation_chance (str): precipitation chance for first night period
        - night_0_wind (str): wind details for first night period
        - night_0_detailed_description (str): detailed description for first night period
        - day_1_period (str): "Day" for second day period
        - day_1_temperature (str): temperature for second day period
        - day_1_conditions (str): weather conditions for second day period
        - day_1_precipitation_chance (str): precipitation chance for second day period
        - day_1_wind (str): wind details for second day period
        - day_1_detailed_description (str): detailed description for second day period
        - night_1_period (str): "Night" for second night period
        - night_1_temperature (str): temperature for second night period
        - night_1_conditions (str): weather conditions for second night period
        - night_1_precipitation_chance (str): precipitation chance for second night period
        - night_1_wind (str): wind details for second night period
        - night_1_detailed_description (str): detailed description for second night period
    """
    return {
        "location": "40.7128,-74.0060",
        "updated": "9/15/2023, 2:30 PM (local time)",
        "day_0_period": "Day",
        "day_0_temperature": "78°F (25.6°C)",
        "day_0_conditions": "Partly Cloudy",
        "day_0_precipitation_chance": "20% chance",
        "day_0_wind": "5 to 10 mph NW",
        "day_0_detailed_description": "Partly cloudy in the morning with increasing clouds later in the day.",
        "night_0_period": "Night",
        "night_0_temperature": "65°F (18.3°C)",
        "night_0_conditions": "Mostly Cloudy",
        "night_0_precipitation_chance": "10% chance",
        "night_0_wind": "3 to 7 mph SE",
        "night_0_detailed_description": "Mostly cloudy overnight with a slight chance of isolated showers.",
        "day_1_period": "Day",
        "day_1_temperature": "75°F (23.9°C)",
        "day_1_conditions": "Scattered Showers",
        "day_1_precipitation_chance": "60% chance",
        "day_1_wind": "8 to 12 mph NE",
        "day_1_detailed_description": "Scattered showers developing during the afternoon hours.",
        "night_1_period": "Night",
        "night_1_temperature": "62°F (16.7°C)",
        "night_1_conditions": "Showers Likely",
        "night_1_precipitation_chance": "70% chance",
        "night_1_wind": "6 to 10 mph E",
        "night_1_detailed_description": "Rain likely overnight with moderate rainfall at times."
    }

def united_states_weather_get_weather_forecast(days: int = 7, location: str = None) -> Dict[str, Any]:
    """
    Get multi-day weather forecast for a location in the United States.
    
    Args:
        days (int, optional): Number of days to forecast (1-7, default 7). Each day includes both day and night periods.
        location (str): US location as coordinates (lat,lng) in decimal degrees. Example: '40.7128,-74.0060' for New York City.
                       Must be within US boundaries including states, territories (PR, VI, AS, GU, MP), and coastal waters.
    
    Returns:
        Dict containing weather forecast with the following structure:
        - location (str): coordinates in "lat,lng" format for the forecast location
        - updated (str): timestamp of when the forecast was last updated
        - forecast_days (List[Dict]): list of daily forecast periods, each containing 'day' and 'night' entries with weather details
          Each forecast period contains:
          - 'period' (str): either "Day" or "Night"
          - 'temperature' (str): formatted temperature
          - 'conditions' (str): descriptive weather condition
          - 'precipitation_chance' (str): chance of precipitation as percentage
          - 'wind' (str): wind speed and direction
          - 'detailed_description' (str): full prose description of the period's weather
    
    Raises:
        ValueError: If location is not provided or doesn't match lat/lng format, or if days is not between 1-7
    """
    # Input validation
    if location is None:
        raise ValueError("Location is required")
    
    # Validate location format (lat,lng)
    try:
        lat_str, lng_str = location.split(',')
        lat = float(lat_str.strip())
        lng = float(lng_str.strip())
        
        # Validate coordinate ranges for US
        if lat < -14.5 or lat > 71.5 or lng > -66.9 or lng < -172.5:
            raise ValueError("Coordinates must be within US boundaries")
            
    except (ValueError, IndexError):
        raise ValueError("Location must be in 'lat,lng' format with valid decimal degrees")
    
    # Validate days parameter
    if not isinstance(days, int) or days < 1 or days > 7:
        raise ValueError("Days must be an integer between 1 and 7")
    
    # Call external API to get weather data
    api_data = call_external_api("united-states-weather-get_weather_forecast")
    
    # Construct the forecast_days list by mapping flat API data to nested structure
    forecast_days = []
    
    # Process first day (index 0)
    day_0_entry = {
        'period': api_data['day_0_period'],
        'temperature': api_data['day_0_temperature'],
        'conditions': api_data['day_0_conditions'],
        'precipitation_chance': api_data['day_0_precipitation_chance'],
        'wind': api_data['day_0_wind'],
        'detailed_description': api_data['day_0_detailed_description']
    }
    
    night_0_entry = {
        'period': api_data['night_0_period'],
        'temperature': api_data['night_0_temperature'],
        'conditions': api_data['night_0_conditions'],
        'precipitation_chance': api_data['night_0_precipitation_chance'],
        'wind': api_data['night_0_wind'],
        'detailed_description': api_data['night_0_detailed_description']
    }
    
    forecast_days.append({'day': day_0_entry, 'night': night_0_entry})
    
    # Process second day (index 1) if needed
    if days > 1:
        day_1_entry = {
            'period': api_data['day_1_period'],
            'temperature': api_data['day_1_temperature'],
            'conditions': api_data['day_1_conditions'],
            'precipitation_chance': api_data['day_1_precipitation_chance'],
            'wind': api_data['day_1_wind'],
            'detailed_description': api_data['day_1_detailed_description']
        }
        
        night_1_entry = {
            'period': api_data['night_1_period'],
            'temperature': api_data['night_1_temperature'],
            'conditions': api_data['night_1_conditions'],
            'precipitation_chance': api_data['night_1_precipitation_chance'],
            'wind': api_data['night_1_wind'],
            'detailed_description': api_data['night_1_detailed_description']
        }
        
        forecast_days.append({'day': day_1_entry, 'night': night_1_entry})
    
    # For remaining days (2-6), extend with similar patterns based on first two days
    base_conditions = [api_data['day_0_conditions'], api_data['day_1_conditions']]
    base_temps = [api_data['day_0_temperature'], api_data['day_1_temperature']]
    
    for i in range(2, min(days, 7)):
        # Alternate conditions and temperatures for additional days
        condition = base_conditions[i % 2]
        temp = base_temps[i % 2]
        
        day_entry = {
            'period': 'Day',
            'temperature': temp,
            'conditions': condition,
            'precipitation_chance': '30% chance' if 'Cloudy' in condition else '60% chance',
            'wind': '5 to 10 mph W' if i % 2 == 0 else '6 to 12 mph SW',
            'detailed_description': f'{condition} conditions expected during the day.' 
        }
        
        night_condition = 'Mostly Cloudy' if 'Partly' in condition else 'Scattered Showers'
        night_temp = '63°F (17.2°C)' if i % 2 == 0 else '61°F (16.1°C)'
        
        night_entry = {
            'period': 'Night',
            'temperature': night_temp,
            'conditions': night_condition,
            'precipitation_chance': '20% chance' if 'Mostly' in night_condition else '50% chance',
            'wind': '3 to 8 mph N' if i % 2 == 0 else '4 to 9 mph NE',
            'detailed_description': f'Expect {night_condition.lower()} overnight.'
        }
        
        forecast_days.append({'day': day_entry, 'night': night_entry})
    
    # Construct final result
    result = {
        'location': api_data['location'],
        'updated': api_data['updated'],
        'forecast_days': forecast_days
    }
    
    return result