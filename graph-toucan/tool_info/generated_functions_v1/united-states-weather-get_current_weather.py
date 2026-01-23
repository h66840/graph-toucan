from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching current weather data from an external API for a US location.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - location (str): geographic coordinates in "lat,lng" format
        - station (str): weather observation station identifier
        - observed_at_local (str): observation timestamp in local time
        - observation_age_minutes (int): minutes since observation was recorded
        - temperature_fahrenheit (float): air temperature in Fahrenheit
        - temperature_celsius (float): air temperature in Celsius
        - conditions (str): current weather conditions description
        - feels_like_fahrenheit (float): apparent temperature in Fahrenheit
        - feels_like_celsius (float): apparent temperature in Celsius
        - feels_like_type (str): type of feels-like index used
        - humidity_percent (float): relative humidity percentage
        - wind_speed_mph (float): wind speed in miles per hour
        - wind_direction_degrees (int): wind direction in degrees from true north
        - pressure_inhg (float): atmospheric pressure in inches of mercury
        - visibility_miles (float): visibility distance in statute miles
    """
    return {
        "location": "40.7128,-74.0060",
        "station": "KOKC",
        "observed_at_local": "3/15/2024, 2:30 PM",
        "observation_age_minutes": 15,
        "temperature_fahrenheit": 72.5,
        "temperature_celsius": 22.5,
        "conditions": "Clear",
        "feels_like_fahrenheit": 75.0,
        "feels_like_celsius": 23.9,
        "feels_like_type": "heat index",
        "humidity_percent": 65.0,
        "wind_speed_mph": 8.5,
        "wind_direction_degrees": 180,
        "pressure_inhg": 29.92,
        "visibility_miles": 10.0
    }

def united_states_weather_get_current_weather(location: str) -> Dict[str, Any]:
    """
    Get current weather conditions for a location in the United States.
    
    This function retrieves real-time weather data including temperature, humidity,
    wind conditions, pressure, visibility, and other meteorological observations
    for any location within US boundaries (including states, territories, and coastal waters).
    
    Args:
        location (str): US location as coordinates (lat,lng) in decimal degrees.
                       Example: '40.7128,-74.0060' for New York City.
                       Must be within US boundaries including states, territories (PR, VI, AS, GU, MP),
                       and coastal waters.
    
    Returns:
        Dict containing current weather conditions with the following fields:
        - location (str): geographic coordinates in "lat,lng" format for the observed location
        - station (str): identifier of the weather observation station (e.g., KOKC, KSLC)
        - observed_at_local (str): date and time of observation in local time, formatted as "M/D/YYYY, H:MM AM/PM"
        - observation_age_minutes (int): number of minutes ago the observation was recorded
        - temperature_fahrenheit (float): current air temperature in degrees Fahrenheit
        - temperature_celsius (float): current air temperature in degrees Celsius
        - conditions (str): current weather conditions description (e.g., Clear, Rainy, Cloudy)
        - feels_like_fahrenheit (float): apparent temperature in degrees Fahrenheit considering humidity or wind
        - feels_like_celsius (float): apparent temperature in degrees Celsius
        - feels_like_type (str): type of feels-like index used (e.g., heat index, wind chill)
        - humidity_percent (float): relative humidity as a percentage
        - wind_speed_mph (float): wind speed in miles per hour
        - wind_direction_degrees (int): wind direction in degrees from true north (0° = north, 90° = east)
        - pressure_inhg (float): atmospheric pressure in inches of mercury
        - visibility_miles (float): visibility distance in statute miles
    
    Raises:
        ValueError: If location is not provided or is not in valid lat,lng format
        ValueError: If latitude or longitude values are outside valid ranges
        ValueError: If location is outside US boundaries (not applicable in simulation but included for completeness)
    """
    # Input validation
    if not location:
        raise ValueError("Location parameter is required")
    
    if not isinstance(location, str):
        raise ValueError("Location must be a string in 'lat,lng' format")
    
    try:
        lat_str, lng_str = location.split(',')
        lat = float(lat_str.strip())
        lng = float(lng_str.strip())
    except (ValueError, AttributeError):
        raise ValueError("Location must be in 'lat,lng' format with valid decimal numbers")
    
    if not (-90 <= lat <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180 <= lng <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # In a real implementation, we would validate if the location is within US boundaries
    # For this simulation, we'll proceed with the API call
    
    # Call external API to get weather data
    api_data = call_external_api("united-states-weather-get_current_weather")
    
    # Construct the result dictionary matching the output schema
    result = {
        "location": api_data["location"],
        "station": api_data["station"],
        "observed_at_local": api_data["observed_at_local"],
        "observation_age_minutes": api_data["observation_age_minutes"],
        "temperature_fahrenheit": api_data["temperature_fahrenheit"],
        "temperature_celsius": api_data["temperature_celsius"],
        "conditions": api_data["conditions"],
        "feels_like_fahrenheit": api_data["feels_like_fahrenheit"],
        "feels_like_celsius": api_data["feels_like_celsius"],
        "feels_like_type": api_data["feels_like_type"],
        "humidity_percent": api_data["humidity_percent"],
        "wind_speed_mph": api_data["wind_speed_mph"],
        "wind_direction_degrees": api_data["wind_direction_degrees"],
        "pressure_inhg": api_data["pressure_inhg"],
        "visibility_miles": api_data["visibility_miles"]
    }
    
    return result