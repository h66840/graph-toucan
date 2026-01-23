from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wallhaven wallpaper search server.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - collection_0_id (int): ID of the first collection
        - collection_0_name (str): Name of the first collection
        - collection_0_description (str): Description of the first collection
        - collection_0_total_images (int): Total number of images in the first collection
        - collection_0_created_at (str): Creation timestamp of the first collection
        - collection_1_id (int): ID of the second collection
        - collection_1_name (str): Name of the second collection
        - collection_1_description (str): Description of the second collection
        - collection_1_total_images (int): Total number of images in the second collection
        - collection_1_created_at (str): Creation timestamp of the second collection
        - total_collections (int): Total number of collections returned
        - user (str): Username for which collections were retrieved
        - authenticated_access (bool): Whether the request used authentication
        - metadata_rate_limit_remaining (int): API rate limit remaining
        - metadata_rate_limit_reset (int): API rate limit reset time in seconds
        - metadata_timestamp (str): Timestamp of the request
        - metadata_has_next_page (bool): Whether there is a next page of results
        - metadata_has_prev_page (bool): Whether there is a previous page of results
    """
    return {
        "collection_0_id": 1001,
        "collection_0_name": "Nature Landscapes",
        "collection_0_description": "Beautiful natural scenery from around the world",
        "collection_0_total_images": 42,
        "collection_0_created_at": "2023-01-15T08:30:00Z",
        "collection_1_id": 1002,
        "collection_1_name": "Space Exploration",
        "collection_1_description": "Astronomy and space imagery",
        "collection_1_total_images": 28,
        "collection_1_created_at": "2023-02-20T14:45:00Z",
        "total_collections": 2,
        "user": "wallhaven_user",
        "authenticated_access": True,
        "metadata_rate_limit_remaining": 98,
        "metadata_rate_limit_reset": 3600,
        "metadata_timestamp": "2023-11-10T12:00:00Z",
        "metadata_has_next_page": False,
        "metadata_has_prev_page": False,
    }

def wallhaven_wallpaper_search_server_get_collections(username: Optional[str] = None) -> Dict[str, Any]:
    """
    Get user collections from Wallhaven wallpaper search server.
    
    Args:
        username (Optional[str]): Username to get collections for. If None, gets authenticated user's collections.
    
    Returns:
        Dict containing:
        - collections (List[Dict]): List of collection objects with 'id', 'name', 'description', 'total_images', and 'created_at'
        - total_collections (int): Total number of collections returned
        - user (str): Username for which collections were retrieved
        - authenticated_access (bool): Whether the request used authentication
        - metadata (Dict): Additional metadata including rate limit info, timestamp, and pagination status
    """
    # Validate input
    if username is not None and not isinstance(username, str):
        raise TypeError("Username must be a string or None")
    
    # Call external API to get data
    api_data = call_external_api("wallhaven-wallpaper-search-server-get_collections")
    
    # Construct collections list from flattened API data
    collections = [
        {
            "id": api_data["collection_0_id"],
            "name": api_data["collection_0_name"],
            "description": api_data["collection_0_description"],
            "total_images": api_data["collection_0_total_images"],
            "created_at": api_data["collection_0_created_at"]
        },
        {
            "id": api_data["collection_1_id"],
            "name": api_data["collection_1_name"],
            "description": api_data["collection_1_description"],
            "total_images": api_data["collection_1_total_images"],
            "created_at": api_data["collection_1_created_at"]
        }
    ]
    
    # Construct metadata dictionary
    metadata = {
        "rate_limit_remaining": api_data["metadata_rate_limit_remaining"],
        "rate_limit_reset": api_data["metadata_rate_limit_reset"],
        "timestamp": api_data["metadata_timestamp"],
        "has_next_page": api_data["metadata_has_next_page"],
        "has_prev_page": api_data["metadata_has_prev_page"]
    }
    
    # Return structured response matching output schema
    return {
        "collections": collections,
        "total_collections": api_data["total_collections"],
        "user": api_data["user"],
        "authenticated_access": api_data["authenticated_access"],
        "metadata": metadata
    }