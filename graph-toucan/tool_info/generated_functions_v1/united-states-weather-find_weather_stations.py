from typing import Dict, Any, List, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather station data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - station_0_name (str): Name of the first weather station
        - station_0_station_id (str): ID of the first weather station
        - station_0_elevation_ft (int): Elevation in feet of the first station
        - station_0_distance_miles (float): Distance in miles to the first station
        - station_0_latest_report_time_local (str): Local time of latest report from first station
        - station_0_latest_report_age_minutes (int): Age in minutes of latest report from first station
        - station_0_temperature_f (float): Temperature in Fahrenheit from first station (if available)
        - station_1_name (str): Name of the second weather station
        - station_1_station_id (str): ID of the second weather station
        - station_1_elevation_ft (int): Elevation in feet of the second station
        - station_1_distance_miles (float): Distance in miles to the second station
        - station_1_latest_report_time_local (str): Local time of latest report from second station
        - station_1_latest_report_age_minutes (int): Age in minutes of latest report from second station
        - station_1_temperature_f (float): Temperature in Fahrenheit from second station (if available)
        - location (str): Input geographic coordinates (latitude,longitude)
        - total_found (int): Total number of stations found near the location
    """
    return {
        "station_0_name": "New York Central Park Weather Station",
        "station_0_station_id": "KNYC",
        "station_0_elevation_ft": 150,
        "station_0_distance_miles": 2.3,
        "station_0_latest_report_time_local": "2023-10-05T14:30:00",
        "station_0_latest_report_age_minutes": 15,
        "station_0_temperature_f": 72.5,
        "station_1_name": "LaGuardia Airport ASOS",
        "station_1_station_id": "KLGA",
        "station_1_elevation_ft": 22,
        "station_1_distance_miles": 8.7,
        "station_1_latest_report_time_local": "2023-10-05T14:25:00",
        "station_1_latest_report_age_minutes": 20,
        "station_1_temperature_f": 70.1,
        "location": "40.7128,-74.0060",
        "total_found": 12
    }

def united_states_weather_find_weather_stations(
    location: str, 
    limit: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Find weather observation stations near a location in the United States.
    
    This function finds automated weather stations (including ASOS, AWOS, and others)
    near a specified geographic location within the United States. Stations are returned
    ordered by distance from the specified location.
    
    Args:
        location (str): US location as coordinates (lat,lng) in decimal degrees. 
                       Example: '40.7128,-74.0060' for New York City.
                       Must be within US boundaries including states, territories, and coastal waters.
        limit (Optional[int]): Maximum number of stations to return (1-20, default 10).
                              If provided, will be clamped to valid range.
    
    Returns:
        Dict containing:
        - stations (List[Dict]): List of weather stations near the specified location,
          each containing 'name', 'station_id', 'elevation_ft', 'distance_miles',
          'latest_report_time_local', 'latest_report_age_minutes', and 'temperature_f'
        - location (str): The input geographic coordinates (latitude,longitude)
        - total_found (int): Total number of stations found matching the query near the location
    
    Raises:
        ValueError: If location is not provided or invalid format, or if limit is out of bounds
        TypeError: If parameters are of incorrect type
    """
    # Input validation
    if not isinstance(location, str) or not location:
        raise ValueError("Location must be a non-empty string in 'lat,lng' format")
    
    try:
        lat_str, lng_str = location.split(',')
        lat = float(lat_str.strip())
        lng = float(lng_str.strip())
        
        # Validate coordinates are within reasonable US bounds
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            raise ValueError("Latitude must be between -90 and 90, longitude between -180 and 180")
            
        # Rough check for US coverage (including territories)
        if not (24 <= lat <= 50 and -130 <= lng <= -65) and not (
            # Check for territories
            (lat >= 17 and lng <= -65) or  # Puerto Rico, Virgin Islands
            (lat >= 14 and lng <= 146)     # Guam, Mariana Islands, American Samoa
        ):
            raise ValueError("Location must be within United States boundaries or territories")
            
    except ValueError as e:
        if "split" in str(e):
            raise ValueError("Location must be in format 'latitude,longitude' with comma separator")
        else:
            raise
    
    if limit is not None:
        if not isinstance(limit, (int, float)):
            raise TypeError("Limit must be a number")
        limit = int(limit)
        if limit < 1:
            raise ValueError("Limit must be at least 1")
        if limit > 20:
            raise ValueError("Limit cannot exceed 20")
    else:
        limit = 10
    
    # Call external API to get data
    api_data = call_external_api("united-states-weather-find_weather_stations")
    
    # Construct the result structure from flat API data
    stations = []
    
    # Process up to 'limit' stations, but we only have 2 simulated in our API response
    max_stations_to_return = min(limit, 2)  # We only have 2 simulated stations
    
    for i in range(max_stations_to_return):
        station_key_prefix = f"station_{i}"
        if f"{station_key_prefix}_name" not in api_data:
            break
            
        station = {
            "name": api_data[f"{station_key_prefix}_name"],
            "station_id": api_data[f"{station_key_prefix}_station_id"],
            "elevation_ft": api_data[f"{station_key_prefix}_elevation_ft"],
            "distance_miles": api_data[f"{station_key_prefix}_distance_miles"],
            "latest_report_time_local": api_data[f"{station_key_prefix}_latest_report_time_local"],
            "latest_report_age_minutes": api_data[f"{station_key_prefix}_latest_report_age_minutes"],
            "temperature_f": api_data[f"{station_key_prefix}_temperature_f"]
        }
        stations.append(station)
    
    # Return final structured result
    return {
        "stations": stations,
        "location": api_data["location"],
        "total_found": api_data["total_found"]
    }