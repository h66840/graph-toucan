def call_external_api(tool_name: str) -> dict:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): Current temperature in degrees Celsius at the specified coordinates
    """
    # Simulated realistic temperature based on Earth's typical ranges
    # Using a deterministic function of latitude and longitude for realism
    import math
    # Extract coordinates from tool_name by parsing, though not passed directly
    # Since we can't pass params to call_external_api per spec, we simulate fixed response
    # But in real implementation, this would be driven by inputs — here we return placeholder
    return {
        "temperature": 18.5  # Simulated live temperature in °C
    }


def mcp_word_server_get_live_temp(latitude: float, longitude: float) -> dict:
    """
    Get live temperature for a given latitude and longitude.

    This function retrieves the current temperature in degrees Celsius
    at the specified geographic coordinates by querying an external weather service.

    Args:
        latitude (float): The latitude coordinate (ranging from -90 to 90)
        longitude (float): The longitude coordinate (ranging from -180 to 180)

    Returns:
        dict: A dictionary containing:
            - temperature (float): Current temperature in degrees Celsius at the specified coordinates

    Raises:
        ValueError: If latitude or longitude are outside valid ranges
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    # Call external API simulation
    api_data = call_external_api("mcp-word-server-get_live_temp")

    # Construct result matching output schema
    result = {
        "temperature": float(api_data["temperature"])
    }

    return result