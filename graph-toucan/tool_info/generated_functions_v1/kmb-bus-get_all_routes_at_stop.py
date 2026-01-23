from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for KMB bus routes at a stop.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - route_0_route_number (str): Route number of first bus route
        - route_0_destination (str): Destination of first bus route
        - route_0_origin (str): Origin of first bus route
        - route_1_route_number (str): Route number of second bus route
        - route_1_destination (str): Destination of second bus route
        - route_1_origin (str): Origin of second bus route
        - stop_name (str): Name of the bus stop queried
        - status (str): Status of the request ('success' or 'no_routes_found')
        - message (str): Human-readable message about the result
    """
    return {
        "route_0_route_number": "970",
        "route_0_destination": "Central (Macau Ferry)",
        "route_0_origin": "Tseung Kwan O (Po Lam)",
        "route_1_route_number": "E22A",
        "route_1_destination": "Tung Chung (North)",
        "route_1_origin": "Kowloon City",
        "stop_name": "Kowloon City Bus Terminus",
        "status": "success",
        "message": "2 routes found for the stop"
    }

def kmb_bus_get_all_routes_at_stop(stop_name: str) -> Dict[str, Any]:
    """
    Get all bus routes that pass through a specified bus stop.
    
    Args:
        stop_name (str): Name of the bus stop
    
    Returns:
        Dict containing:
        - routes (List[Dict]): list of bus routes serving the stop, each with 'route_number', 'destination', and 'origin' fields
        - stop_name (str): name of the bus stop queried
        - status (str): status of the request (e.g., 'success' or 'no_routes_found')
        - message (str): human-readable message describing the result or error
    """
    # Input validation
    if not stop_name or not stop_name.strip():
        return {
            "routes": [],
            "stop_name": "",
            "status": "error",
            "message": "Stop name is required"
        }
    
    # Call external API to get data (simulated)
    api_data = call_external_api("kmb-bus-get_all_routes_at_stop")
    
    # Construct the routes list from flattened API response
    routes = []
    
    # Only process routes if status is success
    if api_data.get("status") == "success":
        # Extract first route if available
        if "route_0_route_number" in api_data:
            routes.append({
                "route_number": api_data["route_0_route_number"],
                "destination": api_data["route_0_destination"],
                "origin": api_data["route_0_origin"]
            })
        
        # Extract second route if available
        if "route_1_route_number" in api_data:
            routes.append({
                "route_number": api_data["route_1_route_number"],
                "destination": api_data["route_1_destination"],
                "origin": api_data["route_1_origin"]
            })
    
    # Return structured response matching output schema
    return {
        "routes": routes,
        "stop_name": api_data.get("stop_name", stop_name),
        "status": api_data.get("status", "no_routes_found"),
        "message": api_data.get("message", "No routes found for this stop")
    }