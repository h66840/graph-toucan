from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for the Met Museum object search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - total_objects (int): Total number of objects found matching the search criteria
        - object_0_id (int): First object ID from the search results
        - object_1_id (int): Second object ID from the search results
    """
    return {
        "total_objects": 2,
        "object_0_id": 12345,
        "object_1_id": 67890
    }

def met_museum_server_search_museum_objects(
    q: str,
    departmentId: Optional[int] = None,
    hasImages: Optional[bool] = False,
    title: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Search for objects in the Metropolitan Museum of Art (Met Museum).
    
    This function simulates searching the Met Museum's collection based on a query and optional filters.
    It returns the total number of matching objects and a list of their unique IDs.
    
    Args:
        q (str): The search query. Required. Returns objects that contain the query in their data.
        departmentId (int, optional): Filter objects by department ID. Should come from 'list-departments' tool.
        hasImages (bool, optional): If True, only return objects that have images. Default is False.
        title (bool, optional): If True, search only within object titles. If hasImages is True, title must be False.

    Returns:
        Dict with the following keys:
        - total_objects (int): Total number of objects found matching the criteria
        - object_ids (List[int]): List of unique Met Museum object IDs that match the search query and filters

    Raises:
        ValueError: If both hasImages is True and title is True, which is not allowed.
    """
    # Validate input: hasImages and title cannot both be True
    if hasImages and title:
        raise ValueError("Cannot set both hasImages=True and title=True. If hasImages is True, title must be False.")

    # Simulate calling external API
    api_data = call_external_api("met-museum-server-search-museum-objects")

    # Construct output structure from flat API response
    result = {
        "total_objects": api_data["total_objects"],
        "object_ids": [
            api_data["object_0_id"],
            api_data["object_1_id"]
        ]
    }

    return result