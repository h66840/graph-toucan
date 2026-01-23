from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching sea forecast data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - forecast_date (str): Date of the sea forecast in YYYY-MM-DD format
        - location_0_location_id (str): Location ID for first location
        - location_0_latitude (float): Latitude of first location
        - location_0_longitude (float): Longitude of first location
        - location_0_wave_height_swell_min_m (float): Minimum swell wave height in meters for first location
        - location_0_wave_height_swell_max_m (float): Maximum swell wave height in meters for first location
        - location_0_wave_period_swell_min_s (float): Minimum swell wave period in seconds for first location
        - location_0_wave_period_swell_max_s (float): Maximum swell wave period in seconds for first location
        - location_0_predominant_wave_direction (str): Predominant wave direction for first location
        - location_0_total_sea_height_min_m (float): Minimum total sea height in meters for first location
        - location_0_total_sea_height_max_m (float): Maximum total sea height in meters for first location
        - location_0_sea_surface_temperature_min_c (float): Minimum sea surface temperature in Celsius for first location
        - location_0_sea_surface_temperature_max_c (float): Maximum sea surface temperature in Celsius for first location
        - location_1_location_id (str): Location ID for second location
        - location_1_latitude (float): Latitude of second location
        - location_1_longitude (float): Longitude of second location
        - location_1_wave_height_swell_min_m (float): Minimum swell wave height in meters for second location
        - location_1_wave_height_swell_max_m (float): Maximum swell wave height in meters for second location
        - location_1_wave_period_swell_min_s (float): Minimum swell wave period in seconds for second location
        - location_1_wave_period_swell_max_s (float): Maximum swell wave period in seconds for second location
        - location_1_predominant_wave_direction (str): Predominant wave direction for second location
        - location_1_total_sea_height_min_m (float): Minimum total sea height in meters for second location
        - location_1_total_sea_height_max_m (float): Maximum total sea height in meters for second location
        - location_1_sea_surface_temperature_min_c (float): Minimum sea surface temperature in Celsius for second location
        - location_1_sea_surface_temperature_max_c (float): Maximum sea surface temperature in Celsius for second location
    """
    base_date = (datetime.now() + timedelta(days=0)).strftime("%Y-%m-%d")
    return {
        "forecast_date": base_date,
        "location_0_location_id": "porto_north",
        "location_0_latitude": 41.1496,
        "location_0_longitude": -8.6109,
        "location_0_wave_height_swell_min_m": 1.2,
        "location_0_wave_height_swell_max_m": 2.1,
        "location_0_wave_period_swell_min_s": 8.0,
        "location_0_wave_period_swell_max_s": 12.0,
        "location_0_predominant_wave_direction": "NW",
        "location_0_total_sea_height_min_m": 1.5,
        "location_0_total_sea_height_max_m": 2.4,
        "location_0_sea_surface_temperature_min_c": 16.5,
        "location_0_sea_surface_temperature_max_c": 18.0,
        "location_1_location_id": "lisbon_south",
        "location_1_latitude": 38.6965,
        "location_1_longitude": -9.2093,
        "location_1_wave_height_swell_min_m": 0.9,
        "location_1_wave_height_swell_max_m": 1.7,
        "location_1_wave_period_swell_min_s": 7.0,
        "location_1_wave_period_swell_max_s": 10.0,
        "location_1_predominant_wave_direction": "W",
        "location_1_total_sea_height_min_m": 1.1,
        "location_1_total_sea_height_max_m": 1.9,
        "location_1_sea_surface_temperature_min_c": 17.0,
        "location_1_sea_surface_temperature_max_c": 18.5,
    }


def ao_generative_ai_cp3_smithery_server_get_sea_forecast(day: Optional[int] = 0) -> Dict[str, Any]:
    """
    Get daily sea state forecast for Portugal coastal areas.

    Args:
        day (int, optional): 0 = today, 1 = tomorrow, 2 = day after tomorrow. Defaults to 0.

    Returns:
        Dict containing:
        - forecast_date (str): date of the sea forecast in YYYY-MM-DD format
        - locations (List[Dict]): list of location-specific sea forecast entries with keys:
          'location_id', 'coordinates', 'wave_height_swell_min_m', 'wave_height_swell_max_m',
          'wave_period_swell_min_s', 'wave_period_swell_max_s', 'predominant_wave_direction',
          'total_sea_height_min_m', 'total_sea_height_max_m', 'sea_surface_temperature_min_c',
          'sea_surface_temperature_max_c'

    Raises:
        ValueError: If day is not 0, 1, or 2.
    """
    # Input validation
    if day not in [0, 1, 2]:
        raise ValueError("Parameter 'day' must be 0 (today), 1 (tomorrow), or 2 (day after tomorrow).")

    # Fetch data from external API (simulated)
    api_data = call_external_api("ao-generative-ai-cp3-smithery-server-get_sea_forecast")

    # Adjust forecast date based on input day
    forecast_date = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")

    # Construct locations list from flattened API data
    locations: List[Dict[str, Any]] = []

    for i in range(2):  # We have two locations (0 and 1)
        location = {
            "location_id": api_data[f"location_{i}_location_id"],
            "coordinates": [
                api_data[f"location_{i}_latitude"],
                api_data[f"location_{i}_longitude"]
            ],
            "wave_height_swell_min_m": api_data[f"location_{i}_wave_height_swell_min_m"],
            "wave_height_swell_max_m": api_data[f"location_{i}_wave_height_swell_max_m"],
            "wave_period_swell_min_s": api_data[f"location_{i}_wave_period_swell_min_s"],
            "wave_period_swell_max_s": api_data[f"location_{i}_wave_period_swell_max_s"],
            "predominant_wave_direction": api_data[f"location_{i}_predominant_wave_direction"],
            "total_sea_height_min_m": api_data[f"location_{i}_total_sea_height_min_m"],
            "total_sea_height_max_m": api_data[f"location_{i}_total_sea_height_max_m"],
            "sea_surface_temperature_min_c": api_data[f"location_{i}_sea_surface_temperature_min_c"],
            "sea_surface_temperature_max_c": api_data[f"location_{i}_sea_surface_temperature_max_c"],
        }
        locations.append(location)

    # Return structured response
    return {
        "forecast_date": forecast_date,
        "locations": locations
    }