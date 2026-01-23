from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for location search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - location_0_name (str): First matching location name
        - location_0_region (str): Region of first location
        - location_0_country (str): Country of first location
        - location_0_lat (float): Latitude of first location
        - location_0_lon (float): Longitude of first location
        - location_0_url (str): URL for first location
        - location_1_name (str): Second matching location name
        - location_1_region (str): Region of second location
        - location_1_country (str): Country of second location
        - location_1_lat (float): Latitude of second location
        - location_1_lon (float): Longitude of second location
        - location_1_url (str): URL for second location
    """
    return {
        "location_0_name": "London",
        "location_0_region": "Greater London",
        "location_0_country": "United Kingdom",
        "location_0_lat": 51.5085,
        "location_0_lon": -0.1257,
        "location_0_url": "https://example.com/weather/london-uk",
        "location_1_name": "London",
        "location_1_region": "Ohio",
        "location_1_country": "United States",
        "location_1_lat": 39.8865,
        "location_1_lon": -83.4483,
        "location_1_url": "https://example.com/weather/london-oh",
    }

def weather_information_server_search_locations_tool(query: str) -> List[Dict[str, Any]]:
    """
    Search for locations by name or partial name.
    
    Args:
        query (str): Location name or partial name to search for
        
    Returns:
        List of matching locations with their details. Each location contains:
        - name (str): Name of the location
        - region (str): Region or state of the location
        - country (str): Country of the location
        - lat (float): Latitude coordinate
        - lon (float): Longitude coordinate
        - url (str): URL for accessing weather information for this location
        
    Raises:
        ValueError: If query is empty or not a string
    """
    if not query:
        raise ValueError("Query parameter is required")
    
    if not isinstance(query, str):
        raise ValueError("Query must be a string")
    
    # Call external API to get location data
    api_data = call_external_api("weather-information-server-search_locations_tool")
    
    # Construct list of location objects from flattened API response
    locations = [
        {
            "name": api_data["location_0_name"],
            "region": api_data["location_0_region"],
            "country": api_data["location_0_country"],
            "lat": api_data["location_0_lat"],
            "lon": api_data["location_0_lon"],
            "url": api_data["location_0_url"]
        },
        {
            "name": api_data["location_1_name"],
            "region": api_data["location_1_region"],
            "country": api_data["location_1_country"],
            "lat": api_data["location_1_lat"],
            "lon": api_data["location_1_lon"],
            "url": api_data["location_1_url"]
        }
    ]
    
    # Filter locations based on query (case-insensitive substring match)
    filtered_locations = [
        loc for loc in locations
        if query.lower() in loc["name"].lower()
    ]
    
    return filtered_locations