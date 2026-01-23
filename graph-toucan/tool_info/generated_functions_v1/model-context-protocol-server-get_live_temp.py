from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature (float): Current temperature in degrees Celsius at the specified location
    """
    # Simulated temperature calculation based on latitude and longitude
    # This is a simplified model for demonstration purposes
    import math
    # Base temperature influenced by latitude (equator = warmer, poles = colder)
    base_temp = 30.0 - (abs(tool_name) * 0.3)  # Dummy influence of coordinates
    # Add some variation based on longitude (e.g., continental vs maritime effects)
    variation = math.sin(tool_name) * 5.0
    # Final temperature with some randomness simulation
    temp = base_temp + variation + 2.0
    
    return {
        "temperature": round(temp, 2)
    }

def model_context_protocol_server_get_live_temp(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get live temperature for a given latitude and longitude.
    
    This function retrieves the current temperature in degrees Celsius
    at the specified geographic coordinates by simulating an external API call.
    
    Args:
        latitude (float): The latitude of the location (required)
        longitude (float): The longitude of the location (required)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - temperature (float): current temperature in degrees Celsius at the specified location
    
    Raises:
        ValueError: If latitude is not between -90 and 90 or longitude is not between -180 and 180
    """
    # Input validation
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Generate a unique identifier for the tool call to simulate different results
    # based on coordinates without making real API calls
    coordinate_hash = hash(f"{latitude},{longitude}") % 100000
    
    # Call external API simulation
    api_data = call_external_api(coordinate_hash)
    
    # Construct result matching output schema
    result = {
        "temperature": api_data["temperature"]
    }
    
    return result