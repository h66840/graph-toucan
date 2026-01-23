from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Minecraft Wiki category members.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - page_0_title (str): Title of the first page in the category
        - page_0_page_id (int): Page ID of the first page
        - page_0_url (str): URL of the first page
        - page_0_category (str): Category name for the first page
        - page_1_title (str): Title of the second page in the category
        - page_1_page_id (int): Page ID of the second page
        - page_1_url (str): URL of the second page
        - page_1_category (str): Category name for the second page
        - total_count (int): Total number of pages in the category
        - category_name (str): Name of the queried category
        - limit (int): Maximum number of results returned
        - truncated (bool): Whether the result was truncated due to limit
        - metadata_query_timestamp (str): ISO format timestamp of the query
        - metadata_source (str): Source of the data
        - metadata_api_version (str): Version of the API
    """
    return {
        "page_0_title": "Diamond Sword",
        "page_0_page_id": 12345,
        "page_0_url": "https://minecraft.fandom.com/wiki/Diamond_Sword",
        "page_0_category": "Items",
        "page_1_title": "Iron Pickaxe",
        "page_1_page_id": 12346,
        "page_1_url": "https://minecraft.fandom.com/wiki/Iron_Pickaxe",
        "page_1_category": "Items",
        "total_count": 150,
        "category_name": "Items",
        "limit": 100,
        "truncated": True,
        "metadata_query_timestamp": datetime.now().isoformat(),
        "metadata_source": "Minecraft Wiki",
        "metadata_api_version": "1.0.0"
    }

def minecraft_wiki_server_MinecraftWiki_listCategoryMembers(category: str, limit: Optional[int] = 100) -> Dict[str, Any]:
    """
    List all pages that are members of a specific category on the Minecraft Wiki.
    
    Args:
        category (str): The name of the category to list members from (e.g., 'Items', 'Blocks', 'Entities', 'Structure Blueprints').
        limit (Optional[int]): The maximum number of pages to return (default: 100, max: 500).
    
    Returns:
        Dict containing:
        - pages (List[Dict]): List of page objects with keys 'title', 'page_id', 'url', and 'category'
        - total_count (int): Total number of pages found in the category
        - category_name (str): Name of the category queried
        - limit (int): Maximum number of results returned in this response
        - truncated (bool): Indicates whether the result list was truncated due to the limit
        - metadata (Dict): Additional information including query timestamp, source, and API version
    
    Raises:
        ValueError: If category is empty or limit is not between 1 and 500
    """
    # Input validation
    if not category or not category.strip():
        raise ValueError("Category parameter is required and cannot be empty")
    
    if limit is None:
        limit = 100
    elif not isinstance(limit, int) or limit < 1:
        raise ValueError("Limit must be a positive integer")
    elif limit > 500:
        raise ValueError("Limit cannot exceed 500")
    
    # Call external API to get data
    api_data = call_external_api("minecraft-wiki-server-MinecraftWiki_listCategoryMembers")
    
    # Construct pages list from indexed fields
    pages = [
        {
            "title": api_data["page_0_title"],
            "page_id": api_data["page_0_page_id"],
            "url": api_data["page_0_url"],
            "category": api_data["page_0_category"]
        },
        {
            "title": api_data["page_1_title"],
            "page_id": api_data["page_1_page_id"],
            "url": api_data["page_1_url"],
            "category": api_data["page_1_category"]
        }
    ]
    
    # Apply limit to pages (though we only have 2 simulated results)
    limited_pages = pages[:limit]
    
    # Construct metadata
    metadata = {
        "query_timestamp": api_data["metadata_query_timestamp"],
        "source": api_data["metadata_source"],
        "api_version": api_data["metadata_api_version"]
    }
    
    # Determine if results were truncated
    actual_limit = min(limit, 500)
    is_truncated = api_data["total_count"] > actual_limit
    
    # Construct final result
    result = {
        "pages": limited_pages,
        "total_count": api_data["total_count"],
        "category_name": api_data["category_name"],
        "limit": actual_limit,
        "truncated": is_truncated,
        "metadata": metadata
    }
    
    return result