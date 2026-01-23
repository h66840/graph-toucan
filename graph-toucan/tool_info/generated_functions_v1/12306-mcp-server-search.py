from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external 12306 API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - train_0_train_number (str): Train number for first train
        - train_0_departure_station (str): Departure station name for first train
        - train_0_arrival_station (str): Arrival station name for first train
        - train_0_departure_time (str): Departure time (HH:MM) for first train
        - train_0_arrival_time (str): Arrival time (HH:MM) for first train
        - train_0_duration (str): Duration in format HH:MM for first train
        - train_0_status (str): Ticket status for first train (e.g., "Available")
        - train_0_ticket_0_type (str): First ticket type for first train (e.g., "Second Class")
        - train_0_ticket_0_price (float): Price for first ticket type of first train
        - train_0_ticket_0_count (int): Available count for first ticket type of first train
        - train_0_ticket_1_type (str): Second ticket type for first train (e.g., "First Class")
        - train_0_ticket_1_price (float): Price for second ticket type of first train
        - train_0_ticket_1_count (int): Available count for second ticket type of first train
        - train_1_train_number (str): Train number for second train
        - train_1_departure_station (str): Departure station name for second train
        - train_1_arrival_station (str): Arrival station name for second train
        - train_1_departure_time (str): Departure time (HH:MM) for second train
        - train_1_arrival_time (str): Arrival time (HH:MM) for second train
        - train_1_duration (str): Duration in format HH:MM for second train
        - train_1_status (str): Ticket status for second train (e.g., "Sold Out")
        - train_1_ticket_0_type (str): First ticket type for second train
        - train_1_ticket_0_price (float): Price for first ticket type of second train
        - train_1_ticket_0_count (int): Available count for first ticket type of second train
        - train_1_ticket_1_type (str): Second ticket type for second train
        - train_1_ticket_1_price (float): Price for second ticket type of second train
        - train_1_ticket_1_count (int): Available count for second ticket type of second train
    """
    return {
        "train_0_train_number": "G123",
        "train_0_departure_station": "Beijing South",
        "train_0_arrival_station": "Shanghai Hongqiao",
        "train_0_departure_time": "08:00",
        "train_0_arrival_time": "14:30",
        "train_0_duration": "6:30",
        "train_0_status": "Available",
        "train_0_ticket_0_type": "Second Class",
        "train_0_ticket_0_price": 553.0,
        "train_0_ticket_0_count": 120,
        "train_0_ticket_1_type": "First Class",
        "train_0_ticket_1_price": 933.0,
        "train_0_ticket_1_count": 45,
        
        "train_1_train_number": "D456",
        "train_1_departure_station": "Beijing South",
        "train_1_arrival_station": "Shanghai Hongqiao",
        "train_1_departure_time": "10:15",
        "train_1_arrival_time": "18:45",
        "train_1_duration": "8:30",
        "train_1_status": "Sold Out",
        "train_1_ticket_0_type": "Second Class",
        "train_1_ticket_0_price": 453.0,
        "train_1_ticket_0_count": 0,
        "train_1_ticket_1_type": "First Class",
        "train_1_ticket_1_price": 783.0,
        "train_1_ticket_1_count": 0,
    }

def tool_12306_mcp_server_search(date: str, fromCity: str, toCity: str) -> Dict[str, Any]:
    """
    查询12306火车票信息。
    
    Args:
        date (str): 出发日期，格式：YYYY-MM-DD
        fromCity (str): 出发城市
        toCity (str): 到达城市
    
    Returns:
        Dict containing 'trains' key with list of train details. Each train contains:
        - train_number (str)
        - departure_station (str)
        - arrival_station (str)
        - departure_time (str)
        - arrival_time (str)
        - duration (str)
        - status (str)
        - tickets (List[Dict]): list of ticket types with 'type', 'price', 'count'
    
    Raises:
        ValueError: If date is not in valid format or required fields are empty
    """
    # Input validation
    if not date:
        raise ValueError("date is required")
    if not fromCity:
        raise ValueError("fromCity is required")
    if not toCity:
        raise ValueError("toCity is required")
        
    # Basic date format validation
    try:
        year, month, day = date.split('-')
        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            raise ValueError
        int(year), int(month), int(day)
    except:
        raise ValueError("date must be in YYYY-MM-DD format")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("12306-mcp-server-search")
    
    # Construct trains list from flattened API data
    trains = []
    
    # Process first train (index 0)
    train_0_tickets = [
        {
            "type": api_data["train_0_ticket_0_type"],
            "price": api_data["train_0_ticket_0_price"],
            "count": api_data["train_0_ticket_0_count"]
        },
        {
            "type": api_data["train_0_ticket_1_type"],
            "price": api_data["train_0_ticket_1_price"],
            "count": api_data["train_0_ticket_1_count"]
        }
    ]
    
    trains.append({
        "train_number": api_data["train_0_train_number"],
        "departure_station": api_data["train_0_departure_station"],
        "arrival_station": api_data["train_0_arrival_station"],
        "departure_time": api_data["train_0_departure_time"],
        "arrival_time": api_data["train_0_arrival_time"],
        "duration": api_data["train_0_duration"],
        "status": api_data["train_0_status"],
        "tickets": train_0_tickets
    })
    
    # Process second train (index 1)
    train_1_tickets = [
        {
            "type": api_data["train_1_ticket_0_type"],
            "price": api_data["train_1_ticket_0_price"],
            "count": api_data["train_1_ticket_0_count"]
        },
        {
            "type": api_data["train_1_ticket_1_type"],
            "price": api_data["train_1_ticket_1_price"],
            "count": api_data["train_1_ticket_1_count"]
        }
    ]
    
    trains.append({
        "train_number": api_data["train_1_train_number"],
        "departure_station": api_data["train_1_departure_station"],
        "arrival_station": api_data["train_1_arrival_station"],
        "departure_time": api_data["train_1_departure_time"],
        "arrival_time": api_data["train_1_arrival_time"],
        "duration": api_data["train_1_duration"],
        "status": api_data["train_1_status"],
        "tickets": train_1_tickets
    })
    
    return {
        "trains": trains
    }