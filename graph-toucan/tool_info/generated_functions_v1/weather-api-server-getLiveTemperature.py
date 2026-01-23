def call_external_api(tool_name: str) -> dict:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): Current temperature in degrees Celsius
        - location (str): Name of the city or location corresponding to the coordinates
        - country (str): Full name of the country where the location is situated
        - condition (str): Current weather condition description (e.g., "Sunny", "Partly cloudy", "Light rain shower")
    """
    return {
        "temperature": 22.5,
        "location": "New York",
        "country": "United States",
        "condition": "Sunny"
    }


def weather_api_server_getLiveTemperature(latitude: float, longitude: float) -> dict:
    """
    Get live temperature for a specific location.

    Args:
        latitude (float): The latitude coordinate (e.g., 40.7128 for New York)
        longitude (float): The longitude coordinate (e.g., -74.0060 for New York)

    Returns:
        A dictionary containing temperature information or an error message with the following keys:
        - temperature (float): current temperature in degrees Celsius
        - location (str): name of the city or location corresponding to the coordinates
        - country (str): full name of the country where the location is situated
        - condition (str): current weather condition description (e.g., "Sunny", "Partly cloudy", "Light rain shower")

    Raises:
        ValueError: If latitude or longitude are not within valid ranges.
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        return {"error": "Latitude must be between -90 and 90."}
    if not (-180 <= longitude <= 180):
        return {"error": "Longitude must be between -180 and 180."}

    try:
        # Call external API simulation
        api_data = call_external_api("weather-api-server-getLiveTemperature")

        # Construct result dictionary matching output schema
        result = {
            "temperature": float(api_data["temperature"]),
            "location": str(api_data["location"]),
            "country": str(api_data["country"]),
            "condition": str(api_data["condition"])
        }

        return result

    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}