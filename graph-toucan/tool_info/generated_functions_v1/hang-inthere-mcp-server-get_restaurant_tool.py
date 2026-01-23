from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for restaurant search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - restaurant_0_name (str): Name of the first nearby restaurant
        - restaurant_0_address (str): Address of the first restaurant
        - restaurant_0_rating (float): Rating of the first restaurant (out of 5)
        - restaurant_0_cuisine (str): Cuisine type of the first restaurant
        - restaurant_1_name (str): Name of the second nearby restaurant
        - restaurant_1_address (str): Address of the second restaurant
        - restaurant_1_rating (float): Rating of the second restaurant (out of 5)
        - restaurant_1_cuisine (str): Cuisine type of the second restaurant
        - error_message (str): Error message if any occurred during the API call
    """
    return {
        "restaurant_0_name": "Delicious Bites",
        "restaurant_0_address": "123 Foodie Lane, Near Central Park",
        "restaurant_0_rating": 4.5,
        "restaurant_0_cuisine": "Chinese",
        "restaurant_1_name": "Urban Grill",
        "restaurant_1_address": "456 Taste Avenue, Downtown",
        "restaurant_1_rating": 4.7,
        "restaurant_1_cuisine": "American",
        "error_message": ""
    }

def hang_inthere_mcp_server_get_restaurant_tool(address: str) -> List[Dict[str, Any]]:
    """
    获取附近的饭店信息
    
    :param address: 公司地址
    :return: 饭店信息列表，每个饭店包含名称、地址、评分和菜系
             如果发生错误，则返回包含 error_message 的字典列表
    """
    # Input validation
    if not isinstance(address, str):
        return [{"error_message": "Address must be a string."}]
    
    if not address.strip():
        return [{"error_message": "Address cannot be empty or whitespace."}]

    try:
        # Call the external API simulation
        api_data = call_external_api("hang-inthere-mcp-server-get_restaurant_tool")
        
        # Check for error from API
        if api_data.get("error_message"):
            return [{"error_message": api_data["error_message"]}]

        # Construct restaurant list from flat API response
        restaurants = [
            {
                "name": api_data["restaurant_0_name"],
                "address": api_data["restaurant_0_address"],
                "rating": api_data["restaurant_0_rating"],
                "cuisine": api_data["restaurant_0_cuisine"]
            },
            {
                "name": api_data["restaurant_1_name"],
                "address": api_data["restaurant_1_address"],
                "rating": api_data["restaurant_1_rating"],
                "cuisine": api_data["restaurant_1_cuisine"]
            }
        ]
        
        return restaurants

    except KeyError as e:
        return [{"error_message": f"Missing expected data field: {str(e)}"}]
    except Exception as e:
        return [{"error_message": f"Unexpected error occurred: {str(e)}"}]