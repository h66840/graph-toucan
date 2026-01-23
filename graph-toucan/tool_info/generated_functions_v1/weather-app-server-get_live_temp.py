from typing import Dict,Any,Optional,List
import random
def call_external_api(tool_name: str) -> dict:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): Current temperature in degrees Celsius
    """
    # Simulated realistic temperature based on latitude and longitude patterns
    # Temperatures vary roughly by latitude (equator warmer, poles colder)
    # Using arbitrary formula to generate plausible temperature values
    import random

    # Since we can't access inputs here, return a template value
    # Actual mapping happens in main function using inputs
    base_temp = 30 - abs(0) * 0.3  # Dummy calculation placeholder
    simulated_temp = round(base_temp + random.uniform(-5, 5), 2)
    return {
        "temperature": simulated_temp
    }


def weather_app_server_get_live_temp(latitude: float, longitude: float) -> dict:
    """
    Get live temperature for a given latitude and longitude.

    This function retrieves the current temperature in degrees Celsius
    for the specified geographic coordinates by simulating an external API call.

    Args:
        latitude (float): The latitude coordinate (ranging from -90 to 90)
        longitude (float): The longitude coordinate (ranging from -180 to 180)

    Returns:
        dict: A dictionary containing:
            - temperature (float): Current temperature in degrees Celsius

    Raises:
        ValueError: If latitude is not between -90 and 90 or longitude not between -180 and 180
    """
    # Input validation
    if not isinstance(latitude, (int, float)):
        raise ValueError("Latitude must be a number.")
    if not isinstance(longitude, (int, float)):
        raise ValueError("Longitude must be a number.")
    if latitude < -90 or latitude > 90:
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if longitude < -180 or longitude > 180:
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    # Adjust temperature simulation based on actual latitude/longitude
    # More realistic model: equatorial regions warmer, polar regions colder
    # Add slight variation based on longitude (continental vs maritime effects)
    base_temp = 30 - abs(latitude) * 0.3
    lon_variation = (abs(longitude) % 360) * 0.01
    random.seed(abs(hash(f"{latitude},{longitude}") % 1000000))
    variation = random.uniform(-5, 5)
    simulated_temp = round(base_temp + lon_variation + variation, 2)

    # Simulate API response with adjusted temperature
    api_response = {
        "temperature": simulated_temp
    }

    # Construct final result matching output schema
    result = {
        "temperature": api_response["temperature"]
    }

    return result