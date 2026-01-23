from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cigarette data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (str): ID of the first matching cigarette product
        - result_0_name (str): Name of the first cigarette product
        - result_0_chinese_name (str): Chinese name of the first cigarette product
        - result_0_brand (str): Brand of the first cigarette product
        - result_0_price (float): Price of the first cigarette product
        - result_0_rating (float): Rating of the first cigarette product
        - result_0_image (str): Image URL of the first cigarette product
        - result_0_specifications (str): Specifications of the first cigarette product
        - result_0_production (str): Production information of the first cigarette product
        - result_1_id (str): ID of the second matching cigarette product
        - result_1_name (str): Name of the second cigarette product
        - result_1_chinese_name (str): Chinese name of the second cigarette product
        - result_1_brand (str): Brand of the second cigarette product
        - result_1_price (float): Price of the second cigarette product
        - result_1_rating (float): Rating of the second cigarette product
        - result_1_image (str): Image URL of the second cigarette product
        - result_1_specifications (str): Specifications of the second cigarette product
        - result_1_production (str): Production information of the second cigarette product
        - error_message (str): Error message if any, otherwise empty string
    """
    return {
        "result_0_id": "cig001",
        "result_0_name": "Red Dragonfly Classic",
        "result_0_chinese_name": "红蜻蜓经典",
        "result_0_brand": "Red Dragonfly",
        "result_0_price": 18.5,
        "result_0_rating": 4.3,
        "result_0_image": "https://example.com/images/red_dragonfly.jpg",
        "result_0_specifications": "Pack of 20, Medium strength, Filtered",
        "result_0_production": "Yunnan Tobacco Co., Ltd.",
        "result_1_id": "cig002",
        "result_1_name": "Blue Mountain Mild",
        "result_1_chinese_name": "蓝山之韵",
        "result_1_brand": "Blue Mountain",
        "result_1_price": 25.0,
        "result_1_rating": 4.6,
        "result_1_image": "https://example.com/images/blue_mountain.jpg",
        "result_1_specifications": "Pack of 20, Mild strength, Slim design",
        "result_1_production": "Guizhou Tobacco Co., Ltd.",
        "error_message": ""
    }

def yanyue_cigarette_data_searchCigarettes(keyword: str) -> Dict[str, Any]:
    """
    根据关键词搜索卷烟信息
    
    Args:
        keyword (str): 搜索关键词，用于匹配卷烟名称、品牌等信息
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of cigarette products matching the search, each containing
          'id', 'name', 'chinese_name', 'brand', 'price', 'rating', 'image', 
          'specifications', and 'production' fields
        - error_message (str): Error message if no results found or other failure, otherwise empty string
        
    Example:
        {
            "results": [
                {
                    "id": "cig001",
                    "name": "Red Dragonfly Classic",
                    "chinese_name": "红蜻蜓经典",
                    "brand": "Red Dragonfly",
                    "price": 18.5,
                    "rating": 4.3,
                    "image": "https://example.com/images/red_dragonfly.jpg",
                    "specifications": "Pack of 20, Medium strength, Filtered",
                    "production": "Yunnan Tobacco Co., Ltd."
                }
            ],
            "error_message": ""
        }
    """
    # Input validation
    if not keyword or not keyword.strip():
        return {
            "results": [],
            "error_message": "搜索关键词不能为空"
        }
    
    # Call external API to get data
    api_data = call_external_api("yanyue-cigarette-data-searchCigarettes")
    
    # Extract error message
    error_message = api_data.get("error_message", "")
    
    # Construct results list from flattened API response
    results: List[Dict[str, Any]] = []
    
    # Process first result if available
    if "result_0_id" in api_data and api_data["result_0_id"]:
        result_0 = {
            "id": api_data["result_0_id"],
            "name": api_data["result_0_name"],
            "chinese_name": api_data["result_0_chinese_name"],
            "brand": api_data["result_0_brand"],
            "price": api_data["result_0_price"],
            "rating": api_data["result_0_rating"],
            "image": api_data["result_0_image"],
            "specifications": api_data["result_0_specifications"],
            "production": api_data["result_0_production"]
        }
        results.append(result_0)
    
    # Process second result if available
    if "result_1_id" in api_data and api_data["result_1_id"]:
        result_1 = {
            "id": api_data["result_1_id"],
            "name": api_data["result_1_name"],
            "chinese_name": api_data["result_1_chinese_name"],
            "brand": api_data["result_1_brand"],
            "price": api_data["result_1_price"],
            "rating": api_data["result_1_rating"],
            "image": api_data["result_1_image"],
            "specifications": api_data["result_1_specifications"],
            "production": api_data["result_1_production"]
        }
        results.append(result_1)
    
    # If no results were added, set error message
    if not results and not error_message:
        error_message = "未找到匹配的卷烟信息"
    
    return {
        "results": results,
        "error_message": error_message
    }