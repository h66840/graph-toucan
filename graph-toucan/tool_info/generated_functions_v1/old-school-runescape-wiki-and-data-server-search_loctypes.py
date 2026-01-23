from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Old School RuneScape loctypes search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matching location/object type
        - result_0_name (str): Name of the first matching location/object type
        - result_0_description (str): Description of the first entry
        - result_0_object_type (str): Object type of the first entry
        - result_0_interactable (bool): Whether the first object is interactable
        - result_0_walkable (bool): Whether the first object is walkable
        - result_0_x (int): X coordinate of the first object
        - result_0_y (int): Y coordinate of the first object
        - result_0_z (int): Z coordinate (level) of the first object
        - result_1_id (int): ID of the second matching location/object type
        - result_1_name (str): Name of the second matching location/object type
        - result_1_description (str): Description of the second entry
        - result_1_object_type (str): Object type of the second entry
        - result_1_interactable (bool): Whether the second object is interactable
        - result_1_walkable (bool): Whether the second object is walkable
        - result_1_x (int): X coordinate of the second object
        - result_1_y (int): Y coordinate of the second object
        - result_1_z (int): Z coordinate (level) of the second object
        - total_count (int): Total number of matching entries across all pages
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more pages exist
        - metadata_timestamp (str): ISO format timestamp of data retrieval
        - metadata_source_version (str): Version/revision of loctypes.txt
        - metadata_game_build_date (str): Game patch/build date
    """
    return {
        "result_0_id": 1234,
        "result_0_name": "Bank Booth",
        "result_0_description": "A secure booth used to access your bank account.",
        "result_0_object_type": "NPC",
        "result_0_interactable": True,
        "result_0_walkable": False,
        "result_0_x": 3210,
        "result_0_y": 3456,
        "result_0_z": 0,
        "result_1_id": 5678,
        "result_1_name": "Fishing Spot",
        "result_1_description": "A place where you can catch trout and salmon.",
        "result_1_object_type": "Object",
        "result_1_interactable": True,
        "result_1_walkable": True,
        "result_1_x": 3100,
        "result_1_y": 3500,
        "result_1_z": 0,
        "total_count": 42,
        "page": 1,
        "page_size": 10,
        "has_more": True,
        "metadata_timestamp": datetime.utcnow().isoformat(),
        "metadata_source_version": "rev-38291",
        "metadata_game_build_date": "2023-10-15"
    }


def old_school_runescape_wiki_and_data_server_search_loctypes(
    query: str,
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the loctypes.txt file for location/object type definitions in the game world.

    Args:
        query (str): The term to search for in the file (required)
        page (int, optional): Page number for pagination (default: 1)
        pageSize (int, optional): Number of results per page (default: 10)

    Returns:
        Dict containing:
        - results (List[Dict]): List of location/object type entries with fields like 'id', 'name', 'description',
          'object_type', 'interactable', 'walkable', and coordinate data
        - total_count (int): Total number of matching entries across all pages
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether additional pages exist
        - metadata (Dict): Contextual info including timestamp, source version, and game build date

    Raises:
        ValueError: If query is empty or None
        TypeError: If page or pageSize are not integers
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty.")
    
    if not isinstance(page, int) or page < 1:
        raise ValueError("Page must be a positive integer.")
    
    if not isinstance(pageSize, int) or pageSize < 1:
        raise ValueError("pageSize must be a positive integer.")

    # Fetch simulated external data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_loctypes")

    # Construct results list from indexed flat fields
    results = [
        {
            "id": api_data["result_0_id"],
            "name": api_data["result_0_name"],
            "description": api_data["result_0_description"],
            "object_type": api_data["result_0_object_type"],
            "interactable": api_data["result_0_interactable"],
            "walkable": api_data["result_0_walkable"],
            "x": api_data["result_0_x"],
            "y": api_data["result_0_y"],
            "z": api_data["result_0_z"]
        },
        {
            "id": api_data["result_1_id"],
            "name": api_data["result_1_name"],
            "description": api_data["result_1_description"],
            "object_type": api_data["result_1_object_type"],
            "interactable": api_data["result_1_interactable"],
            "walkable": api_data["result_1_walkable"],
            "x": api_data["result_1_x"],
            "y": api_data["result_1_y"],
            "z": api_data["result_1_z"]
        }
    ]

    # Apply pagination logic
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]

    # Construct metadata
    metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "source_version": api_data["metadata_source_version"],
        "game_build_date": api_data["metadata_game_build_date"]
    }

    # Final response structure
    return {
        "results": paginated_results,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "page_size": api_data["page_size"],
        "has_more": api_data["has_more"],
        "metadata": metadata
    }