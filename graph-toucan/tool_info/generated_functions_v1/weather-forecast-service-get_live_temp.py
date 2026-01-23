import math
def call_external_api(tool_name: str) -> dict:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): current live temperature in degrees Celsius at the specified latitude and longitude
    """
    # Simulated realistic temperature based on latitude and longitude
    # Basic heuristic: temperatures vary by latitude (equator warmer, poles colder)
    # Using a simplified model for demonstration
    import math
    lat = 0.0
    lon = 0.0
    if tool_name == "weather-forecast-service-get_live_temp":
        # These would normally come from actual API inputs, but here we simulate
        # Since we can't access inputs in this function, we return a placeholder
        # Actual values will be computed in the main function
        pass

    # Placeholder return; actual mapping happens in main function
    return {
        "temperature": 20.0  # Placeholder value
    }


def weather_forecast_service_get_live_temp(latitude: float, longitude: float) -> dict:
    """
    Get live temperature for a given latitude and longitude.

    This function simulates calling an external weather service to retrieve
    the current temperature at the specified geographic coordinates.

    Args:
        latitude (float): The latitude coordinate of the location (required).
        longitude (float): The longitude coordinate of the location (required).

    Returns:
        dict: A dictionary containing the following keys:
            - temperature (float): Current live temperature in degrees Celsius
              at the specified latitude and longitude.

    Raises:
        ValueError: If latitude is not between -90 and 90 or longitude is not between -180 and 180.
    """
    # Input validation
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    # Simulate realistic temperature generation based on location
    # Approximate real-world patterns:
    # - Equatorial regions are warmer (~25-35°C)
    # - Temperate zones vary with season (we'll use average ~10-20°C)
    # - Polar regions are colder (~-20 to 0°C)
    # Use a deterministic formula to generate plausible temperature

    # Base temperature decreases as we move away from equator
    base_temp = 30.0 - 0.3 * abs(latitude)

    # Add small variation based on longitude (simulating continental vs maritime effects)
    longitude_influence = (math.sin(longitude * math.pi / 180) * 5)
    
    # Add random-like but deterministic variation using hash of coordinates
    coordinate_hash = hash((round(latitude, 3), round(longitude, 3))) % 1000 / 100.0
    fluctuation = (coordinate_hash - 5)  # Range roughly -5 to +5

    simulated_temperature = base_temp + longitude_influence + fluctuation

    # Clamp to reasonable Earth temperature range
    simulated_temperature = max(-50.0, min(60.0, simulated_temperature))

    # Call external API simulation (must be called with tool name)
    api_data = call_external_api("weather-forecast-service-get_live_temp")

    # Construct result using both computed logic and API data pattern
    # Override placeholder with our computed value
    result = {
        "temperature": round(simulated_temperature, 2)
    }

    return result