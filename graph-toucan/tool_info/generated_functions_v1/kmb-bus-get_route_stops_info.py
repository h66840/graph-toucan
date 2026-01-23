from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for KMB bus route stops information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - route_0_direction (str): First route direction (e.g., Outbound)
        - route_0_origin (str): Origin of the first route
        - route_0_destination (str): Destination of the first route
        - route_0_stop_0_name (str): First stop name in first route
        - route_0_stop_0_id (str): First stop ID in first route
        - route_0_stop_1_name (str): Second stop name in first route
        - route_0_stop_1_id (str): Second stop ID in first route
        - route_1_direction (str): Second route direction (e.g., Inbound)
        - route_1_origin (str): Origin of the second route
        - route_1_destination (str): Destination of the second route
        - route_1_stop_0_name (str): First stop name in second route
        - route_1_stop_0_id (str): First stop ID in second route
        - route_1_stop_1_name (str): Second stop name in second route
        - route_1_stop_1_id (str): Second stop ID in second route
    """
    return {
        "route_0_direction": "Outbound",
        "route_0_origin": "Central",
        "route_0_destination": "Kowloon City",
        "route_0_stop_0_name": "Central Ferry Pier",
        "route_0_stop_0_id": "CFP01",
        "route_0_stop_1_name": "Admiralty Station",
        "route_0_stop_1_id": "ADS02",
        "route_1_direction": "Inbound",
        "route_1_origin": "Kowloon City",
        "route_1_destination": "Central",
        "route_1_stop_0_name": "Kowloon City Market",
        "route_1_stop_0_id": "KCM01",
        "route_1_stop_1_name": "Lok Fu Station",
        "route_1_stop_1_id": "LFS02"
    }

def kmb_bus_get_route_stops_info(route: str) -> List[Dict[str, Any]]:
    """
    Get all stops along a specified bus route.
    
    Args:
        route (str): The bus route number (e.g., "1A", "6", "960")
    
    Returns:
        List[Dict]: List of route directions (e.g., Outbound, Inbound), each containing 
                   'direction', 'origin', 'destination', and 'stops' fields.
                   Each stop is a dictionary with 'name' and 'id' keys.
    
    Raises:
        ValueError: If route is empty or not a string
    """
    if not route:
        raise ValueError("Route parameter is required")
    if not isinstance(route, str):
        raise ValueError("Route must be a string")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("kmb-bus-get_route_stops_info")
    
    # Construct the result structure
    routes = []
    
    # Process first route direction (index 0)
    route_0_stops = [
        {
            "name": api_data["route_0_stop_0_name"],
            "id": api_data["route_0_stop_0_id"]
        },
        {
            "name": api_data["route_0_stop_1_name"],
            "id": api_data["route_0_stop_1_id"]
        }
    ]
    
    routes.append({
        "direction": api_data["route_0_direction"],
        "origin": api_data["route_0_origin"],
        "destination": api_data["route_0_destination"],
        "stops": route_0_stops
    })
    
    # Process second route direction (index 1)
    route_1_stops = [
        {
            "name": api_data["route_1_stop_0_name"],
            "id": api_data["route_1_stop_0_id"]
        },
        {
            "name": api_data["route_1_stop_1_name"],
            "id": api_data["route_1_stop_1_id"]
        }
    ]
    
    routes.append({
        "direction": api_data["route_1_direction"],
        "origin": api_data["route_1_origin"],
        "destination": api_data["route_1_destination"],
        "stops": route_1_stops
    })
    
    return routes