from typing import Dict, List, Any, Optional
import random
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Old School RuneScape inventory types search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matching inventory item
        - result_0_name (str): Name of the first matching inventory item
        - result_0_description (str): Description of the first inventory item
        - result_0_type (str): Type/category of the first inventory item
        - result_0_weight (float): Weight in kg of the first inventory item
        - result_0_noted (bool): Whether the first item is noted
        - result_0_tradeable (bool): Whether the first item is tradeable
        - result_1_id (int): ID of the second matching inventory item
        - result_1_name (str): Name of the second matching inventory item
        - result_1_description (str): Description of the second inventory item
        - result_1_type (str): Type/category of the second inventory item
        - result_1_weight (float): Weight in kg of the second inventory item
        - result_1_noted (bool): Whether the second item is noted
        - result_1_tradeable (bool): Whether the second item is tradeable
        - total_count (int): Total number of inventory items matching the query
        - page (int): Current page number in the paginated result set
        - page_size (int): Number of results returned per page
        - has_more (bool): Whether more results are available on subsequent pages
        - metadata_query_time (float): Time taken to execute the search in seconds
        - metadata_source_file (str): Name of the data file queried
        - metadata_timestamp (str): ISO 8601 timestamp of the response
    """
    return {
        "result_0_id": 1234,
        "result_0_name": "Iron Dagger",
        "result_0_description": "A sharp iron dagger.",
        "result_0_type": "Weapon",
        "result_0_weight": 0.5,
        "result_0_noted": False,
        "result_0_tradeable": True,
        "result_1_id": 1235,
        "result_1_name": "Iron Axe",
        "result_1_description": "An iron axe used for chopping wood.",
        "result_1_type": "Tool",
        "result_1_weight": 1.2,
        "result_1_noted": False,
        "result_1_tradeable": True,
        "total_count": 42,
        "page": 1,
        "page_size": 10,
        "has_more": True,
        "metadata_query_time": round(random.uniform(0.05, 0.3), 3),
        "metadata_source_file": "invtypes.txt",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z"
    }


def old_school_runescape_wiki_and_data_server_search_invtypes(
    query: str,
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the invtypes.txt file for inventory type definitions in Old School RuneScape.

    Args:
        query (str): The term to search for in the inventory types file.
        page (int, optional): Page number for pagination (default is 1).
        pageSize (int, optional): Number of results per page (default is 10).

    Returns:
        Dict containing:
        - results (List[Dict]): List of inventory type entries with keys 'id', 'name',
          'description', 'type', 'weight', 'noted', 'tradeable'.
        - total_count (int): Total number of matching inventory items.
        - page (int): Current page number.
        - page_size (int): Number of results per page.
        - has_more (bool): Whether additional pages exist.
        - metadata (Dict): Additional info including 'query_time', 'source_file', 'timestamp'.

    Raises:
        ValueError: If query is empty or invalid pagination parameters are provided.
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty.")
    if page is not None and page < 1:
        raise ValueError("Page number must be at least 1.")
    if pageSize is not None and (pageSize < 1 or pageSize > 100):
        raise ValueError("Page size must be between 1 and 100.")

    # Normalize inputs
    page = max(1, page or 1)
    pageSize = max(1, min(100, pageSize or 10))

    # Call external API (simulated)
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_invtypes")

    # Construct results list from indexed fields
    results = [
        {
            "id": api_data["result_0_id"],
            "name": api_data["result_0_name"],
            "description": api_data["result_0_description"],
            "type": api_data["result_0_type"],
            "weight": api_data["result_0_weight"],
            "noted": api_data["result_0_noted"],
            "tradeable": api_data["result_0_tradeable"]
        },
        {
            "id": api_data["result_1_id"],
            "name": api_data["result_1_name"],
            "description": api_data["result_1_description"],
            "type": api_data["result_1_type"],
            "weight": api_data["result_1_weight"],
            "noted": api_data["result_1_noted"],
            "tradeable": api_data["result_1_tradeable"]
        }
    ]

    # Apply pagination
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]

    total_count = api_data["total_count"]
    has_more = end_idx < total_count

    # Construct final response
    return {
        "results": paginated_results,
        "total_count": total_count,
        "page": page,
        "page_size": pageSize,
        "has_more": has_more,
        "metadata": {
            "query_time": api_data["metadata_query_time"],
            "source_file": api_data["metadata_source_file"],
            "timestamp": api_data["metadata_timestamp"]
        }
    }