from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for KMB bus stop search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - stop_0_name (str): Name of first matching bus stop
        - stop_0_code (str): Code of first matching bus stop
        - stop_0_id (str): ID of first matching bus stop
        - stop_0_location (str): Location description of first matching bus stop
        - stop_1_name (str): Name of second matching bus stop
        - stop_1_code (str): Code of second matching bus stop
        - stop_1_id (str): ID of second matching bus stop
        - stop_1_location (str): Location description of second matching bus stop
        - found (bool): Whether any stops were found
        - message (str): Human-readable summary message about the search result
    """
    # Simulate realistic data based on partial name match
    return {
        "stop_0_name": "Kowloon Mosque and Islamic Centre",
        "stop_0_code": "KMB00123",
        "stop_0_id": "100123",
        "stop_0_location": "Nathan Road, Tsim Sha Tsui",
        "stop_1_name": "Kowloon City Ferry",
        "stop_1_code": "KMB00456",
        "stop_1_id": "100456",
        "stop_1_location": "Chatham Road North, Kowloon City",
        "found": True,
        "message": "Found 2 bus stops matching 'Kowloon'"
    }

def kmb_bus_find_stop_by_name(stop_name: str) -> Dict[str, Any]:
    """
    Find bus stops matching a name or partial name.
    
    Args:
        stop_name (str): Full or partial name of the bus stop to search for
        
    Returns:
        Dict containing:
        - stops (List[Dict]): list of bus stop objects with 'name', 'code', 'id', 'location'
        - message (str): human-readable summary message about the search result
        - found (bool): whether any stops were found matching the query
    
    Raises:
        ValueError: If stop_name is empty or not a string
    """
    # Input validation
    if not stop_name:
        return {
            "stops": [],
            "message": "Stop name cannot be empty",
            "found": False
        }
    
    if not isinstance(stop_name, str):
        return {
            "stops": [],
            "message": "Stop name must be a string",
            "found": False
        }
    
    # Call external API to get data
    api_data = call_external_api("kmb-bus-find_stop_by_name")
    
    # Construct the stops list from flattened API response
    stops = []
    
    if api_data["found"]:
        # Add first stop if available
        stops.append({
            "name": api_data["stop_0_name"],
            "code": api_data["stop_0_code"],
            "id": api_data["stop_0_id"],
            "location": api_data["stop_0_location"]
        })
        
        # Add second stop if available
        stops.append({
            "name": api_data["stop_1_name"],
            "code": api_data["stop_1_code"],
            "id": api_data["stop_1_id"],
            "location": api_data["stop_1_location"]
        })
        
        message = api_data["message"]
        found = True
    else:
        stops = []
        message = "No bus stops found matching the given name"
        found = False
    
    return {
        "stops": stops,
        "message": message,
        "found": found
    }