from typing import Dict, Any
from datetime import datetime, timedelta
import random

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - temperature_celsius (float): Current temperature in degrees Celsius
        - sunrise_time (str): ISO 8601 timestamp of sunrise (e.g., "2025-08-10T05:38")
        - sunset_time (str): ISO 8601 timestamp of sunset (e.g., "2025-08-10T20:32")
    """
    # Generate realistic but deterministic values based on tool name
    if tool_name == "mcp-client-chatbot-get_weather":
        # Use a seed based on latitude and longitude hash for reproducible results
        # These values would normally come from actual API, but we simulate them
        base_temp = 20.0
        temp_variation = random.uniform(-10, 10)
        temperature_celsius = round(base_temp + temp_variation, 1)
        
        # Create sunrise and sunset times around typical times, varying by latitude
        # Approximate effect: higher latitude -> longer summer days
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        lat_factor = abs(50) * 0.1  # Assume mid-latitude as default
        sunrise_offset = 6 - lat_factor if now.month > 3 and now.month < 10 else 7 + lat_factor
        sunset_offset = 18 + lat_factor if now.month > 3 and now.month < 10 else 17 - lat_factor
        
        sunrise_time = (now + timedelta(hours=sunrise_offset)).strftime("%Y-%m-%dT%H:%M")
        sunset_time = (now + timedelta(hours=sunset_offset)).strftime("%Y-%m-%dT%H:%M")
        
        return {
            "temperature_celsius": temperature_celsius,
            "sunrise_time": sunrise_time,
            "sunset_time": sunset_time
        }
    
    return {}

def mcp_client_chatbot_get_weather(latitude: float, longitude: float) -> Dict[str, Any]:
    """
    Get the current weather at a location.
    
    This function retrieves weather information including temperature, sunrise,
    and sunset times for the specified geographic coordinates.
    
    Args:
        latitude (float): Latitude of the location in decimal degrees (required)
        longitude (float): Longitude of the location in decimal degrees (required)
        
    Returns:
        Dict[str, Any]: A dictionary containing:
            - temperature_celsius (float): Current temperature in degrees Celsius
            - sunrise_time (str): ISO 8601 timestamp of sunrise at the location
            - sunset_time (str): ISO 8601 timestamp of sunset at the location
            
    Raises:
        ValueError: If latitude or longitude are out of valid range
    """
    # Input validation
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees")
    
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees")
    
    # Call external API simulation
    api_data = call_external_api("mcp-client-chatbot-get_weather")
    
    # Construct result matching output schema exactly
    result = {
        "temperature_celsius": api_data["temperature_celsius"],
        "sunrise_time": api_data["sunrise_time"],
        "sunset_time": api_data["sunset_time"]
    }
    
    return result