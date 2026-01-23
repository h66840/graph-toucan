from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for KMB bus routes.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - route_0_from_location (str): Departure location of first bus route
        - route_0_route_number (str): Route number of first bus
        - route_0_to_destination (str): Destination of first bus route
        - route_0_direction (str): Direction of first bus route
        - route_1_from_location (str): Departure location of second bus route
        - route_1_route_number (str): Route number of second bus
        - route_1_to_destination (str): Destination of second bus route
        - route_1_direction (str): Direction of second bus route
    """
    return {
        "route_0_from_location": "Tsim Sha Tsui",
        "route_0_route_number": "269B",
        "route_0_to_destination": "Yuen Long",
        "route_0_direction": "Outbound",
        "route_1_from_location": "Kowloon Tong",
        "route_1_route_number": "268B",
        "route_1_to_destination": "Yuen Long",
        "route_1_direction": "Outbound"
    }

def kmb_bus_find_buses_to_destination(destination: str) -> Dict[str, Any]:
    """
    Find bus routes that go to a specified destination.
    
    Args:
        destination (str): The destination to search for (e.g., "Central", "Mong Kok", "Airport")
    
    Returns:
        Dict containing:
            - routes (List[Dict]): list of bus routes, each with 'from_location', 'route_number', 'to_destination', and 'direction' fields
    
    Raises:
        ValueError: If destination is empty or not a string
    """
    if not destination:
        raise ValueError("Destination must be a non-empty string")
    
    if not isinstance(destination, str):
        raise ValueError("Destination must be a string")
    
    # Call external API to get flat data
    api_data = call_external_api("kmb-bus-find_buses_to_destination")
    
    # Construct the nested structure matching the output schema
    routes = [
        {
            "from_location": api_data["route_0_from_location"],
            "route_number": api_data["route_0_route_number"],
            "to_destination": api_data["route_0_to_destination"],
            "direction": api_data["route_0_direction"]
        },
        {
            "from_location": api_data["route_1_from_location"],
            "route_number": api_data["route_1_route_number"],
            "to_destination": api_data["route_1_to_destination"],
            "direction": api_data["route_1_direction"]
        }
    ]
    
    # Filter routes based on destination (case-insensitive)
    filtered_routes = [
        route for route in routes 
        if destination.lower() in route["to_destination"].lower()
    ]
    
    return {
        "routes": filtered_routes
    }