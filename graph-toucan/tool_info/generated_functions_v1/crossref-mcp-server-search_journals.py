from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for journal search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_title (str): Title of the first journal result
        - result_0_publisher (str): Publisher of the first journal
        - result_0_issn_print (str): Print ISSN of the first journal
        - result_0_issn_online (str): Online ISSN of the first journal
        - result_0_subject_category_0 (str): First subject category of the first journal
        - result_0_subject_category_1 (str): Second subject category of the first journal
        - result_1_title (str): Title of the second journal result
        - result_1_publisher (str): Publisher of the second journal
        - result_1_issn_print (str): Print ISSN of the second journal
        - result_1_issn_online (str): Online ISSN of the second journal
        - result_1_subject_category_0 (str): First subject category of the second journal
        - result_1_subject_category_1 (str): Second subject category of the second journal
        - total_count (int): Total number of journals matching the criteria
        - items_returned (int): Number of items returned in this response
        - next_cursor (str): Opaque token for next page of results
        - prev_cursor (str): Opaque token for previous page of results
        - query_time (float): Time taken to execute the query in seconds
        - metadata_api_version (str): Version of the API used
        - metadata_rate_limit_remaining (int): Number of requests remaining in current window
        - metadata_rate_limit_reset (int): Time in seconds until rate limit resets
        - metadata_timestamp (str): ISO timestamp of the request
    """
    return {
        "result_0_title": "Journal of Computational Physics",
        "result_0_publisher": "Elsevier",
        "result_0_issn_print": "0021-9991",
        "result_0_issn_online": "1090-2716",
        "result_0_subject_category_0": "Physics and Astronomy",
        "result_0_subject_category_1": "Numerical Analysis",
        "result_1_title": "Nature Communications",
        "result_1_publisher": "Nature Publishing Group",
        "result_1_issn_print": "2041-1723",
        "result_1_issn_online": "2041-1723",
        "result_1_subject_category_0": "Multidisciplinary",
        "result_1_subject_category_1": "Science",
        "total_count": 1500,
        "items_returned": 2,
        "next_cursor": "cursor_next_abc123",
        "prev_cursor": None,
        "query_time": 0.125,
        "metadata_api_version": "1.2.0",
        "metadata_rate_limit_remaining": 98,
        "metadata_rate_limit_reset": 3600,
        "metadata_timestamp": "2023-10-05T12:34:56Z"
    }

def crossref_mcp_server_search_journals(
    limit: Optional[int] = None,
    mailto: Optional[str] = None,
    query: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search journals via Crossref API with optional filtering and limiting.
    
    Args:
        limit (Optional[int]): Maximum number of results to return. Defaults to 20 if not specified.
        mailto (Optional[str]): Email address for API contact, used for rate limiting purposes.
        query (Optional[str]): Search query string to filter journals by title, publisher, or subject.

    Returns:
        Dict containing:
        - results (List[Dict]): List of journal records with metadata like title, publisher, ISSN, subjects
        - total_count (int): Total number of matching journals
        - items_returned (int): Number of items in this response
        - next_cursor (str): Token for next page, or None if no more results
        - prev_cursor (str): Token for previous page, or None if first page
        - query_time (float): Time taken to execute the query in seconds
        - metadata (Dict): Additional context including API version, rate limits, and timestamp
    """
    # Input validation
    if limit is not None and (not isinstance(limit, int) or limit <= 0):
        raise ValueError("limit must be a positive integer")
    
    if mailto is not None and (not isinstance(mailto, str) or "@" not in mailto):
        raise ValueError("mailto must be a valid email address")
    
    if query is not None and not isinstance(query, str):
        raise ValueError("query must be a string")
    
    # Fetch simulated API data
    api_data = call_external_api("crossref-mcp-server-search_journals")
    
    # Construct results list from flattened fields
    results = [
        {
            "title": api_data["result_0_title"],
            "publisher": api_data["result_0_publisher"],
            "issn": {
                "print": api_data["result_0_issn_print"],
                "online": api_data["result_0_issn_online"]
            },
            "subject_categories": [
                api_data["result_0_subject_category_0"],
                api_data["result_0_subject_category_1"]
            ]
        },
        {
            "title": api_data["result_1_title"],
            "publisher": api_data["result_1_publisher"],
            "issn": {
                "print": api_data["result_1_issn_print"],
                "online": api_data["result_1_issn_online"]
            },
            "subject_categories": [
                api_data["result_1_subject_category_0"],
                api_data["result_1_subject_category_1"]
            ]
        }
    ]
    
    # Apply limit if specified
    if limit is not None:
        results = results[:limit]
    
    items_returned = len(results)
    
    # Build metadata dictionary
    metadata = {
        "api_version": api_data["metadata_api_version"],
        "rate_limit_status": {
            "remaining": api_data["metadata_rate_limit_remaining"],
            "reset": api_data["metadata_rate_limit_reset"]
        },
        "timestamp": api_data["metadata_timestamp"]
    }
    
    # Construct final response
    response = {
        "results": results,
        "total_count": api_data["total_count"],
        "items_returned": items_returned,
        "next_cursor": api_data["next_cursor"],
        "prev_cursor": api_data["prev_cursor"],
        "query_time": api_data["query_time"],
        "metadata": metadata
    }
    
    return response