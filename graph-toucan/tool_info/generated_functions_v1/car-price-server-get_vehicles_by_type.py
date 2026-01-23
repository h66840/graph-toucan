from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for vehicle brands by type.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - brand_0_name (str): Name of the first vehicle brand
        - brand_0_code (int): Code of the first vehicle brand
        - brand_1_name (str): Name of the second vehicle brand
        - brand_1_code (int): Code of the second vehicle brand
        - vehicle_type (str): Type of vehicles returned
        - total_count (int): Total number of brands available for the requested vehicle type
        - next_steps_hint (str): Hint message guiding user to use searchCarPrice with brand name
    """
    return {
        "brand_0_name": "Toyota",
        "brand_0_code": 101,
        "brand_1_name": "Honda",
        "brand_1_code": 102,
        "vehicle_type": "cars",
        "total_count": 25,
        "next_steps_hint": "Use searchCarPrice with a brand name to get available models and their prices."
    }

def car_price_server_get_vehicles_by_type(vehicle_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get vehicles by type (cars, motorcycles, trucks).
    
    Args:
        vehicle_type (str, optional): Type of vehicles to fetch ("carros"/"cars", "motos"/"motorcycles", "caminhoes"/"trucks").
                                      Defaults to "cars" if not provided.
    
    Returns:
        Dict containing:
        - brands (List[Dict]): list of vehicle brands, each with 'name' (str) and 'code' (int) fields
        - vehicle_type (str): type of vehicles returned
        - total_count (int): total number of brands available for the requested vehicle type
        - next_steps_hint (str): hint message guiding user to use searchCarPrice with brand name to get models and prices
    """
    # Validate and normalize input
    valid_types = ["cars", "motorcycles", "trucks", "carros", "motos", "caminhoes"]
    if vehicle_type is None:
        vehicle_type = "cars"
    elif vehicle_type not in valid_types:
        raise ValueError(f"Invalid vehicle_type: {vehicle_type}. Must be one of {valid_types}.")

    # Call external API to get data (simulated)
    api_data = call_external_api("car-price-server-get_vehicles_by_type")

    # Construct the brands list from flattened API response
    brands = [
        {"name": api_data["brand_0_name"], "code": api_data["brand_0_code"]},
        {"name": api_data["brand_1_name"], "code": api_data["brand_1_code"]}
    ]

    # Construct final result matching output schema
    result = {
        "brands": brands,
        "vehicle_type": api_data["vehicle_type"],
        "total_count": api_data["total_count"],
        "next_steps_hint": api_data["next_steps_hint"]
    }

    return result