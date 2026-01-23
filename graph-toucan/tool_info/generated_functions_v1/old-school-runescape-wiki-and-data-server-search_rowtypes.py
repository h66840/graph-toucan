from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Old School RuneScape Wiki and Data Server.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matched rowtype entry
        - result_0_type (str): Type of the first rowtype entry
        - result_0_parameters (str): Parameters of the first rowtype entry
        - result_0_description (str): Description of the first rowtype entry
        - result_1_id (int): ID of the second matched rowtype entry
        - result_1_type (str): Type of the second rowtype entry
        - result_1_parameters (str): Parameters of the second rowtype entry
        - result_1_description (str): Description of the second rowtype entry
        - total_count (int): Total number of rowtype entries matching the query
        - page (int): Current page number in the paginated result set
        - page_size (int): Number of results returned per page
        - has_more (bool): Whether there are additional results beyond the current page
        - query_echo (str): Echo of the search query that was performed
        - metadata_source_version (str): Version of the source file
        - metadata_timestamp (str): Timestamp of when the data was parsed
        - metadata_parsing_status (str): Status of the parsing process
    """
    return {
        "result_0_id": 1001,
        "result_0_type": "BUTTON",
        "result_0_parameters": "action=1, target=inventory",
        "result_0_description": "Standard inventory item interaction button",
        "result_1_id": 1002,
        "result_1_type": "TEXT",
        "result_1_parameters": "font=1, color=FFFFFF",
        "result_1_description": "White text with standard font for interface labels",
        "total_count": 2,
        "page": 1,
        "page_size": 10,
        "has_more": False,
        "query_echo": "button",
        "metadata_source_version": "v3.5.2",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_parsing_status": "success"
    }


def old_school_runescape_wiki_and_data_server_search_rowtypes(
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10,
    query: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search the rowtypes.txt file for row definitions used in various interfaces.

    Args:
        page (int, optional): Page number for pagination. Defaults to 1.
        pageSize (int, optional): Number of results per page. Defaults to 10.
        query (str, required): The term to search for in the file.

    Returns:
        Dict containing:
            - results (List[Dict]): List of matched rowtype entries with 'id', 'type', 'parameters', and 'description'
            - total_count (int): Total number of matching entries
            - page (int): Current page number
            - page_size (int): Number of results per page
            - has_more (bool): Whether more results exist beyond current page
            - query (str): Echo of the search query
            - metadata (Dict): Contextual info like source version, timestamp, parsing status

    Raises:
        ValueError: If query is None or empty
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")

    # Normalize pagination inputs
    page = page if page and page > 0 else 1
    pageSize = pageSize if pageSize and pageSize > 0 else 10

    # Call external API to get flat data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_rowtypes")

    # Construct results list from indexed fields
    results = [
        {
            "id": api_data["result_0_id"],
            "type": api_data["result_0_type"],
            "parameters": api_data["result_0_parameters"],
            "description": api_data["result_0_description"]
        },
        {
            "id": api_data["result_1_id"],
            "type": api_data["result_1_type"],
            "parameters": api_data["result_1_parameters"],
            "description": api_data["result_1_description"]
        }
    ]

    # Apply pagination
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]

    # Determine if there are more results
    has_more = end_idx < api_data["total_count"]

    # Construct final response
    return {
        "results": paginated_results,
        "total_count": api_data["total_count"],
        "page": page,
        "page_size": pageSize,
        "has_more": has_more,
        "query": api_data["query_echo"],
        "metadata": {
            "source_version": api_data["metadata_source_version"],
            "timestamp": api_data["metadata_timestamp"],
            "parsing_status": api_data["metadata_parsing_status"]
        }
    }