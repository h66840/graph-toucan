def call_external_api(tool_name: str) -> dict:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): Current live temperature in degrees Celsius
    """
    return {
        "temperature": 23.5
    }

def weather_service_get_live_temp(latitude: float, longitude: float) -> dict:
    """
    Get live temperature for a given latitude and longitude.

    This function retrieves the current temperature for a specific geographic location
    using latitude and longitude coordinates by calling an external weather service.

    Args:
        latitude (float): The latitude coordinate of the location (required)
        longitude (float): The longitude coordinate of the location (required)

    Returns:
        dict: A dictionary containing the current temperature with the following structure:
            - temperature (float): Current live temperature in degrees Celsius

    Raises:
        ValueError: If latitude is not between -90 and 90 or longitude is not between -180 and 180
        TypeError: If latitude or longitude are not numeric types
    """
    # Input validation
    if not isinstance(latitude, (int, float)):
        raise TypeError("Latitude must be a number")
    if not isinstance(longitude, (int, float)):
        raise TypeError("Longitude must be a number")
    
    if latitude < -90 or latitude > 90:
        raise ValueError("Latitude must be between -90 and 90 degrees")
    if longitude < -180 or longitude > 180:
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API to get weather data
    api_data = call_external_api("weather-service-get_live_temp")
    
    # Construct result matching output schema
    result = {
        "temperature": float(api_data["temperature"])
    }
    
    return result