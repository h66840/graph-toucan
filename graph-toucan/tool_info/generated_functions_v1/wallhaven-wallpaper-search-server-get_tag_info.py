from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wallhaven tag information.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - data_id (int): The ID of the tag
        - data_name (str): The name of the tag
        - data_alias (str): The alias of the tag
        - data_category_id (int): The category ID of the tag
        - data_category (str): The category name of the tag
        - data_purity (str): The purity level of the tag (e.g., 'sfw', 'sketchy', 'nsfw')
        - data_created_at (str): Creation timestamp of the tag in ISO format
        - success (bool): Indicates whether the request was successful
    """
    return {
        "data_id": 12345,
        "data_name": "nature",
        "data_alias": "natural",
        "data_category_id": 1,
        "data_category": "General",
        "data_purity": "sfw",
        "data_created_at": "2022-01-15T08:30:00Z",
        "success": True
    }

def wallhaven_wallpaper_search_server_get_tag_info(tag_id: int) -> Dict[str, Any]:
    """
    Get information about a specific tag by ID.
    
    Args:
        tag_id (int): The ID of the tag to retrieve information for.
        
    Returns:
        Dict containing:
        - data (Dict): Detailed information about the tag including 'id', 'name', 'alias', 
          'category_id', 'category', 'purity', and 'created_at' fields.
        - success (bool): Indicates whether the request was successful.
        
    Raises:
        ValueError: If tag_id is not a positive integer.
    """
    if not isinstance(tag_id, int) or tag_id <= 0:
        raise ValueError("tag_id must be a positive integer")
    
    # Call external API simulation
    api_data = call_external_api("wallhaven-wallpaper-search-server-get_tag_info")
    
    # Construct the nested data structure as per output schema
    data = {
        "id": api_data["data_id"],
        "name": api_data["data_name"],
        "alias": api_data["data_alias"],
        "category_id": api_data["data_category_id"],
        "category": api_data["data_category"],
        "purity": api_data["data_purity"],
        "created_at": api_data["data_created_at"]
    }
    
    # Return final structured response
    return {
        "data": data,
        "success": api_data["success"]
    }