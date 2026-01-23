from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching car price data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - brand (str): Name of the car brand
        - model_0_name (str): First car model name
        - model_0_year (int): First car model year
        - model_0_fuel_type (str): First car model fuel type
        - model_0_price_brl (float): First car model price in BRL
        - model_0_reference_month (str): First car model reference month
        - model_0_fipe_code (str): First car model FIPE code
        - model_1_name (str): Second car model name
        - model_1_year (int): Second car model year
        - model_1_fuel_type (str): Second car model fuel type
        - model_1_price_brl (float): Second car model price in BRL
        - model_1_reference_month (str): Second car model reference month
        - model_1_fipe_code (str): Second car model FIPE code
        - total_models (int): Total number of models available for the brand
        - price_reference (str): Description of the price source
        - error (str): Error message if request failed, empty if successful
    """
    return {
        "brand": "Toyota",
        "model_0_name": "Corolla",
        "model_0_year": 2023,
        "model_0_fuel_type": "Gasoline",
        "model_0_price_brl": 125000.0,
        "model_0_reference_month": "2023-10",
        "model_0_fipe_code": "001-2023",
        "model_1_name": "Hilux",
        "model_1_year": 2023,
        "model_1_fuel_type": "Diesel",
        "model_1_price_brl": 240000.0,
        "model_1_reference_month": "2023-10",
        "model_1_fipe_code": "002-2023",
        "total_models": 15,
        "price_reference": "FIPE (Brazilian vehicle price reference)",
        "error": ""
    }

def car_price_server_search_car_price(brand_name: str) -> Dict[str, Any]:
    """
    Search for car models and prices by brand name using FIPE database.
    
    Args:
        brand_name (str): The car brand name to search for (e.g., "Toyota", "Honda", "Ford")
    
    Returns:
        Dict containing:
        - brand (str): name of the car brand for which models and prices are returned
        - models (List[Dict]): list of car models with details including 'name', 'year', 
          'fuel_type', 'price_brl', 'reference_month', and 'fipe_code'
        - total_models (int): total number of models available for the queried brand
        - price_reference (str): description of the price source, typically "FIPE (Brazilian vehicle price reference)"
        - error (str): error message if the request failed, includes status code or reason
    """
    # Input validation
    if not brand_name or not isinstance(brand_name, str) or not brand_name.strip():
        return {
            "brand": "",
            "models": [],
            "total_models": 0,
            "price_reference": "FIPE (Brazilian vehicle price reference)",
            "error": "Invalid brand name provided"
        }
    
    # Call external API to get data
    api_data = call_external_api("car-price-server-search_car_price")
    
    # Extract error if present
    if api_data.get("error"):
        return {
            "brand": "",
            "models": [],
            "total_models": 0,
            "price_reference": "FIPE (Brazilian vehicle price reference)",
            "error": api_data["error"]
        }
    
    # Construct models list from indexed fields
    models: List[Dict[str, Any]] = [
        {
            "name": api_data["model_0_name"],
            "year": api_data["model_0_year"],
            "fuel_type": api_data["model_0_fuel_type"],
            "price_brl": api_data["model_0_price_brl"],
            "reference_month": api_data["model_0_reference_month"],
            "fipe_code": api_data["model_0_fipe_code"]
        },
        {
            "name": api_data["model_1_name"],
            "year": api_data["model_1_year"],
            "fuel_type": api_data["model_1_fuel_type"],
            "price_brl": api_data["model_1_price_brl"],
            "reference_month": api_data["model_1_reference_month"],
            "fipe_code": api_data["model_1_fipe_code"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "brand": api_data["brand"],
        "models": models,
        "total_models": api_data["total_models"],
        "price_reference": api_data["price_reference"],
        "error": ""
    }
    
    return result