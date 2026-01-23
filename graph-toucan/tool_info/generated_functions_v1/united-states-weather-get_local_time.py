from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - local_time (str): Current local date and time in format "M/D/YYYY, H:MM AM/PM"
    """
    return {
        "local_time": "6/15/2023, 3:45 PM"
    }

def united_states_weather_get_local_time(location: str) -> Dict[str, str]:
    """
    Get the current local time for a US location. Shows what time it is right now at the specified location.
    
    Args:
        location (str): US location as coordinates (lat,lng) in decimal degrees. Example: '40.7128,-74.0060' for New York City.
        
    Returns:
        Dict containing:
            - local_time (str): current local date and time in the format "M/D/YYYY, H:MM AM/PM"
            
    Raises:
        ValueError: If location is not provided or invalid format
    """
    if not location:
        raise ValueError("Location parameter is required")
    
    try:
        lat_str, lng_str = location.split(',')
        lat = float(lat_str.strip())
        lng = float(lng_str.strip())
        
        # Validate coordinate ranges
        if not (-90 <= lat <= 90):
            raise ValueError(f"Latitude {lat} out of range [-90, 90]")
        if not (-180 <= lng <= 180):
            raise ValueError(f"Longitude {lng} out of range [-180, 180]")
            
    except ValueError as e:
        if "could not convert" in str(e) or "not enough values" in str(e):
            raise ValueError("Location must be in format 'lat,lng' with numeric values")
        else:
            raise e
    
    # Call external API to get the data
    api_data = call_external_api("united-states-weather-get_local_time")
    
    # Construct result matching output schema
    result = {
        "local_time": api_data["local_time"]
    }
    
    return result