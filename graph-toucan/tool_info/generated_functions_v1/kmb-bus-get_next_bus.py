from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for KMB bus next arrival information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - arrival_0_route (str): First arrival bus route number
        - arrival_0_stop_name (str): First arrival stop name
        - arrival_0_stop_code (str): First arrival stop code
        - arrival_0_arrival_time (str): First arrival estimated time (HH:MM)
        - arrival_0_destination_chinese (str): First arrival destination in Chinese
        - arrival_0_destination_english (str): First arrival destination in English
        - arrival_0_is_scheduled (bool): Whether first arrival is scheduled
        - arrival_1_route (str): Second arrival bus route number
        - arrival_1_stop_name (str): Second arrival stop name
        - arrival_1_stop_code (str): Second arrival stop code
        - arrival_1_arrival_time (str): Second arrival estimated time (HH:MM)
        - arrival_1_destination_chinese (str): Second arrival destination in Chinese
        - arrival_1_destination_english (str): Second arrival destination in English
        - arrival_1_is_scheduled (bool): Whether second arrival is scheduled
        - unavailable_0_route (str): First unavailable stop route
        - unavailable_0_stop_name (str): First unavailable stop name
        - unavailable_0_stop_code (str): First unavailable stop code
        - unavailable_0_message (str): Message explaining unavailability
        - unavailable_1_route (str): Second unavailable stop route
        - unavailable_1_stop_name (str): Second unavailable stop name
        - unavailable_1_stop_code (str): Second unavailable stop code
        - unavailable_1_message (str): Message explaining unavailability
    """
    return {
        "arrival_0_route": "1A",
        "arrival_0_stop_name": "Tsim Sha Tsui Ferry",
        "arrival_0_stop_code": "TSF01",
        "arrival_0_arrival_time": "14:23",
        "arrival_0_destination_chinese": "觀塘",
        "arrival_0_destination_english": "Kwun Tong",
        "arrival_0_is_scheduled": False,
        "arrival_1_route": "1A",
        "arrival_1_stop_name": "Tsim Sha Tsui Ferry",
        "arrival_1_stop_code": "TSF01",
        "arrival_1_arrival_time": "14:35",
        "arrival_1_destination_chinese": "觀塘",
        "arrival_1_destination_english": "Kwun Tong",
        "arrival_1_is_scheduled": False,
        "unavailable_0_route": "6",
        "unavailable_0_stop_name": "Lai Chi Kok Park",
        "unavailable_0_stop_code": "LCK05",
        "unavailable_0_message": "No real-time data available",
        "unavailable_1_route": "960",
        "unavailable_1_stop_name": "Tuen Mun Ferry Pier",
        "unavailable_1_stop_code": "TMP03",
        "unavailable_1_message": "No real-time data available"
    }

def kmb_bus_get_next_bus(route: str, stop_name: str) -> Dict[str, Any]:
    """
    Get the next arrival time for a specified bus route at a stop.
    
    Args:
        route (str): The bus route number (e.g., "1A", "6", "960")
        stop_name (str): The name of the bus stop
    
    Returns:
        Dict containing:
        - arrivals (List[Dict]): list of arrival entries with route, stop_name, stop_code,
          arrival_time, destination_chinese, destination_english, and is_scheduled
        - unavailable_stops (List[Dict]): list of stops with no arrival data, each containing
          route, stop_name, stop_code, and message
    """
    if not route:
        raise ValueError("Route parameter is required")
    if not stop_name:
        raise ValueError("Stop name parameter is required")
    
    api_data = call_external_api("kmb-bus-get_next_bus")
    
    # Construct arrivals list
    arrivals = [
        {
            "route": api_data["arrival_0_route"],
            "stop_name": api_data["arrival_0_stop_name"],
            "stop_code": api_data["arrival_0_stop_code"],
            "arrival_time": api_data["arrival_0_arrival_time"],
            "destination_chinese": api_data["arrival_0_destination_chinese"],
            "destination_english": api_data["arrival_0_destination_english"],
            "is_scheduled": api_data["arrival_0_is_scheduled"]
        },
        {
            "route": api_data["arrival_1_route"],
            "stop_name": api_data["arrival_1_stop_name"],
            "stop_code": api_data["arrival_1_stop_code"],
            "arrival_time": api_data["arrival_1_arrival_time"],
            "destination_chinese": api_data["arrival_1_destination_chinese"],
            "destination_english": api_data["arrival_1_destination_english"],
            "is_scheduled": api_data["arrival_1_is_scheduled"]
        }
    ]
    
    # Construct unavailable_stops list
    unavailable_stops = [
        {
            "route": api_data["unavailable_0_route"],
            "stop_name": api_data["unavailable_0_stop_name"],
            "stop_code": api_data["unavailable_0_stop_code"],
            "message": api_data["unavailable_0_message"]
        },
        {
            "route": api_data["unavailable_1_route"],
            "stop_name": api_data["unavailable_1_stop_name"],
            "stop_code": api_data["unavailable_1_stop_code"],
            "message": api_data["unavailable_1_message"]
        }
    ]
    
    return {
        "arrivals": arrivals,
        "unavailable_stops": unavailable_stops
    }