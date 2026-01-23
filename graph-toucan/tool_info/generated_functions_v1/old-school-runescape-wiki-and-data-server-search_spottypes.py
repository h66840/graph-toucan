from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Old School RuneScape spottypes search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matching spot animation
        - result_0_name (str): Name of the first spot animation
        - result_0_type (str): Type of the first spot animation
        - result_0_animation_id (int): Animation ID of the first spot
        - result_0_width (int): Width of the first spot in pixels
        - result_0_height (int): Height of the first spot in pixels
        - result_0_texture (str): Texture file name for the first spot
        - result_1_id (int): ID of the second matching spot animation
        - result_1_name (str): Name of the second spot animation
        - result_1_type (str): Type of the second spot animation
        - result_1_animation_id (int): Animation ID of the second spot
        - result_1_width (int): Width of the second spot in pixels
        - result_1_height (int): Height of the second spot in pixels
        - result_1_texture (str): Texture file name for the second spot
        - total_count (int): Total number of matching entries
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more pages exist
        - metadata_source_file (str): Source file name
        - metadata_total_entries_in_file (int): Total entries in the source file
        - metadata_search_timestamp (str): ISO format timestamp of search
    """
    return {
        "result_0_id": 1234,
        "result_0_name": "Fire Burst",
        "result_0_type": "projectile",
        "result_0_animation_id": 567,
        "result_0_width": 2,
        "result_0_height": 2,
        "result_0_texture": "fire_burst.png",
        "result_1_id": 1235,
        "result_1_name": "Water Splash",
        "result_1_type": "effect",
        "result_1_animation_id": 568,
        "result_1_width": 1,
        "result_1_height": 1,
        "result_1_texture": "water_splash.png",
        "total_count": 25,
        "page": 1,
        "page_size": 2,
        "has_more": True,
        "metadata_source_file": "spottypes.txt",
        "metadata_total_entries_in_file": 3500,
        "metadata_search_timestamp": datetime.utcnow().isoformat() + "Z"
    }

def old_school_runescape_wiki_and_data_server_search_spottypes(
    query: str, 
    page: Optional[int] = 1, 
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the spottypes.txt file for spot animation (graphical effect) definitions.
    
    Args:
        query (str): The term to search for in the file (required)
        page (int, optional): Page number for pagination (default: 1)
        pageSize (int, optional): Number of results per page (default: 10)
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of matching spot animation definitions with properties
        - total_count (int): Total number of matching entries
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more pages exist
        - metadata (Dict): Contextual information about the search and data source
    
    Raises:
        ValueError: If query is empty or None
        ValueError: If page or pageSize is less than 1
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty")
    
    if page is not None and page < 1:
        raise ValueError("Page number must be at least 1")
    
    if pageSize is not None and pageSize < 1:
        raise ValueError("Page size must be at least 1")
    
    # Normalize inputs
    page = page if page is not None else 1
    pageSize = pageSize if pageSize is not None else 10
    
    # Call external API to get flattened data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_spottypes")
    
    # Extract results from flattened API response
    results = [
        {
            "id": api_data["result_0_id"],
            "name": api_data["result_0_name"],
            "type": api_data["result_0_type"],
            "animation_id": api_data["result_0_animation_id"],
            "width": api_data["result_0_width"],
            "height": api_data["result_0_height"],
            "texture": api_data["result_0_texture"]
        },
        {
            "id": api_data["result_1_id"],
            "name": api_data["result_1_name"],
            "type": api_data["result_1_type"],
            "animation_id": api_data["result_1_animation_id"],
            "width": api_data["result_1_width"],
            "height": api_data["result_1_height"],
            "texture": api_data["result_1_texture"]
        }
    ]
    
    # Apply pagination
    total_count = api_data["total_count"]
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]
    
    # Determine if there are more pages
    has_more = end_idx < total_count
    
    # Construct metadata
    metadata = {
        "source_file": api_data["metadata_source_file"],
        "total_entries_in_file": api_data["metadata_total_entries_in_file"],
        "search_timestamp": api_data["metadata_search_timestamp"]
    }
    
    return {
        "results": paginated_results,
        "total_count": total_count,
        "page": page,
        "page_size": pageSize,
        "has_more": has_more,
        "metadata": metadata
    }