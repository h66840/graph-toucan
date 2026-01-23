from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external OSRS data server for seqtypes.txt search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matching animation sequence
        - result_0_name (str): Name of the first animation sequence
        - result_0_frame_count (int): Frame count of the first sequence
        - result_0_frame_delay (int): Frame delay of the first sequence
        - result_0_priority (str): Priority level of the first sequence
        - result_0_repeat_mode (int): Repeat mode of the first sequence
        - result_1_id (int): ID of the second matching animation sequence
        - result_1_name (str): Name of the second animation sequence
        - result_1_frame_count (int): Frame count of the second sequence
        - result_1_frame_delay (int): Frame delay of the second sequence
        - result_1_priority (str): Priority level of the second sequence
        - result_1_repeat_mode (int): Repeat mode of the second sequence
        - total_count (int): Total number of matching animation sequences
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more pages exist
        - query (str): Search query used
        - metadata_source_file (str): Source data file name
        - metadata_timestamp (str): ISO format timestamp of data retrieval
        - metadata_version (str): OSRS data version
    """
    return {
        "result_0_id": 1024,
        "result_0_name": "Attack Stab",
        "result_0_frame_count": 8,
        "result_0_frame_delay": 4,
        "result_0_priority": "low",
        "result_0_repeat_mode": 0,
        "result_1_id": 1025,
        "result_1_name": "Attack Slash",
        "result_1_frame_count": 9,
        "result_1_frame_delay": 4,
        "result_1_priority": "low",
        "result_1_repeat_mode": 0,
        "total_count": 2,
        "page": 1,
        "page_size": 10,
        "has_more": False,
        "query": "Attack",
        "metadata_source_file": "seqtypes.txt",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_version": "2024.08.01"
    }


def old_school_runescape_wiki_and_data_server_search_seqtypes(
    query: str,
    page: Optional[int] = 1,
    page_size: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the seqtypes.txt file for animation sequence definitions.

    Args:
        query (str): The term to search for in the file (required)
        page (int, optional): Page number for pagination (default: 1)
        page_size (int, optional): Number of results per page (default: 10)

    Returns:
        Dict containing:
        - results (List[Dict]): List of matching animation sequence entries with fields like 'id', 'name', 'frame_count', etc.
        - total_count (int): Total number of animation sequences matching the query
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether there are additional results on later pages
        - query (str): The search term used
        - metadata (Dict): Additional context including source file, timestamp, and data version

    Raises:
        ValueError: If query is empty or None
        TypeError: If page or page_size are not integers
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")

    if not isinstance(page, int) or page < 1:
        raise ValueError("Page must be a positive integer")
    
    if not isinstance(page_size, int) or page_size < 1:
        raise ValueError("Page size must be a positive integer")

    # Call external API to get flattened data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_seqtypes")

    # Construct results list from indexed fields
    results = [
        {
            "id": api_data["result_0_id"],
            "name": api_data["result_0_name"],
            "frame_count": api_data["result_0_frame_count"],
            "frame_delay": api_data["result_0_frame_delay"],
            "priority": api_data["result_0_priority"],
            "repeat_mode": api_data["result_0_repeat_mode"]
        },
        {
            "id": api_data["result_1_id"],
            "name": api_data["result_1_name"],
            "frame_count": api_data["result_1_frame_count"],
            "frame_delay": api_data["result_1_frame_delay"],
            "priority": api_data["result_1_priority"],
            "repeat_mode": api_data["result_1_repeat_mode"]
        }
    ]

    # Apply pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_results = results[start_idx:end_idx]
    has_more = end_idx < len(results)

    # Construct metadata
    metadata = {
        "source_file": api_data["metadata_source_file"],
        "timestamp": api_data["metadata_timestamp"],
        "version": api_data["metadata_version"]
    }

    return {
        "results": paginated_results,
        "total_count": api_data["total_count"],
        "page": page,
        "page_size": page_size,
        "has_more": has_more,
        "query": api_data["query"],
        "metadata": metadata
    }