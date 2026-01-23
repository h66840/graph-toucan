from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wallhaven collection wallpapers.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - wallpapers_0_id (str): ID of the first wallpaper
        - wallpapers_0_url (str): URL of the first wallpaper
        - wallpapers_0_resolution (str): Resolution of the first wallpaper (e.g., "1920x1080")
        - wallpapers_0_tags (str): Comma-separated tags for the first wallpaper
        - wallpapers_0_file_size (int): File size in bytes of the first wallpaper
        - wallpapers_1_id (str): ID of the second wallpaper
        - wallpapers_1_url (str): URL of the second wallpaper
        - wallpapers_1_resolution (str): Resolution of the second wallpaper (e.g., "3840x2160")
        - wallpapers_1_tags (str): Comma-separated tags for the second wallpaper
        - wallpapers_1_file_size (int): File size in bytes of the second wallpaper
        - total_count (int): Total number of wallpapers in the collection
        - current_page (int): Current page number returned
        - last_page (int): Total number of pages available
        - per_page (int): Number of wallpapers per page
        - filters_applied_purity (str): Purity filter applied (e.g., "100")
        - collection_info_id (int): Collection ID
        - collection_info_name (str): Name of the collection
        - collection_info_username (str): Username of the collection owner
        - has_more (bool): Whether more pages are available
    """
    return {
        "wallpapers_0_id": "wp123456",
        "wallpapers_0_url": "https://wallhaven.cc/w/wp123456",
        "wallpapers_0_resolution": "1920x1080",
        "wallpapers_0_tags": "nature,landscape,mountain",
        "wallpapers_0_file_size": 2457600,
        "wallpapers_1_id": "wp789012",
        "wallpapers_1_url": "https://wallhaven.cc/w/wp789012",
        "wallpapers_1_resolution": "3840x2160",
        "wallpapers_1_tags": "space,galaxy,stars",
        "wallpapers_1_file_size": 5824768,
        "total_count": 42,
        "current_page": 1,
        "last_page": 3,
        "per_page": 20,
        "filters_applied_purity": "100",
        "collection_info_id": 98765,
        "collection_info_name": "Beautiful Landscapes",
        "collection_info_username": "nature_lover",
        "has_more": True
    }

def wallhaven_wallpaper_search_server_get_collection_wallpapers(
    collection_id: int,
    username: str,
    purity: Optional[str] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get wallpapers from a specific collection on Wallhaven.

    Args:
        collection_id (int): ID of the collection (required)
        username (str): Username who owns the collection (required)
        purity (str, optional): Purity filter (e.g., "100" for SFW only)
        page (int, optional): Page number to retrieve

    Returns:
        Dict containing:
        - wallpapers (List[Dict]): List of wallpaper objects with details such as ID, URL, resolution, tags, and other metadata
        - total_count (int): Total number of wallpapers in the collection across all pages
        - current_page (int): The current page number returned in the response
        - last_page (int): The total number of pages available for this collection
        - per_page (int): Number of wallpapers returned per page
        - filters_applied (Dict): Information about filters that were applied, including purity setting used
        - collection_info (Dict): Metadata about the collection itself, including ID, name, and owner username
        - has_more (bool): Whether additional pages are available beyond the current one

    Raises:
        ValueError: If collection_id or username is missing
    """
    if not collection_id:
        raise ValueError("collection_id is required")
    if not username:
        raise ValueError("username is required")

    # Call external API to get flattened data
    api_data = call_external_api("wallhaven-wallpaper-search-server-get_collection_wallpapers")

    # Construct wallpapers list from indexed fields
    wallpapers = [
        {
            "id": api_data["wallpapers_0_id"],
            "url": api_data["wallpapers_0_url"],
            "resolution": api_data["wallpapers_0_resolution"],
            "tags": api_data["wallpapers_0_tags"].split(","),
            "file_size": api_data["wallpapers_0_file_size"]
        },
        {
            "id": api_data["wallpapers_1_id"],
            "url": api_data["wallpapers_1_url"],
            "resolution": api_data["wallpapers_1_resolution"],
            "tags": api_data["wallpapers_1_tags"].split(","),
            "file_size": api_data["wallpapers_1_file_size"]
        }
    ]

    # Construct filters_applied dict
    filters_applied = {
        "purity": api_data["filters_applied_purity"]
    }

    # Construct collection_info dict
    collection_info = {
        "id": api_data["collection_info_id"],
        "name": api_data["collection_info_name"],
        "username": api_data["collection_info_username"]
    }

    # Build final result matching output schema
    result = {
        "wallpapers": wallpapers,
        "total_count": api_data["total_count"],
        "current_page": api_data["current_page"],
        "last_page": api_data["last_page"],
        "per_page": api_data["per_page"],
        "filters_applied": filters_applied,
        "collection_info": collection_info,
        "has_more": api_data["has_more"]
    }

    return result