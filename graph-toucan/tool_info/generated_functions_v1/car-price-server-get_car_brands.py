from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for car brands.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - brand_0_name (str): Name of the first car brand
        - brand_0_code (int): Code of the first car brand
        - brand_1_name (str): Name of the second car brand
        - brand_1_code (int): Code of the second car brand
        - total_count (int): Total number of available car brands
        - status (str): Status of the request ('success' or 'error')
        - error_message (str): Error description if failed, otherwise None
    """
    return {
        "brand_0_name": "Fiat",
        "brand_0_code": 1,
        "brand_1_name": "Volkswagen",
        "brand_1_code": 2,
        "total_count": 2,
        "status": "success",
        "error_message": None
    }

def car_price_server_get_car_brands() -> Dict[str, Any]:
    """
    Get all available car brands from FIPE API.

    Returns:
        Dict containing:
        - brands (List[Dict]): list of car brands, each with 'name' (str) and 'code' (int) fields
        - total_count (int): total number of available car brands
        - status (str): status of the request: 'success' or 'error'
        - error_message (str): description of the error if the request failed, otherwise None
    """
    try:
        api_data = call_external_api("car-price-server-get_car_brands")
        
        # Construct the list of brands from flattened API response
        brands = [
            {
                "name": api_data["brand_0_name"],
                "code": api_data["brand_0_code"]
            },
            {
                "name": api_data["brand_1_name"],
                "code": api_data["brand_1_code"]
            }
        ]
        
        result = {
            "brands": brands,
            "total_count": api_data["total_count"],
            "status": api_data["status"],
            "error_message": api_data["error_message"]
        }
        
        return result
        
    except KeyError as e:
        return {
            "brands": [],
            "total_count": 0,
            "status": "error",
            "error_message": f"Missing required field in API response: {str(e)}"
        }
    except Exception as e:
        return {
            "brands": [],
            "total_count": 0,
            "status": "error",
            "error_message": f"Unexpected error occurred: {str(e)}"
        }