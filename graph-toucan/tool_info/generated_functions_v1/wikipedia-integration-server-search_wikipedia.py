from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wikipedia search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - query (str): The original search query
        - result_0_title (str): Title of the first result
        - result_0_snippet (str): Snippet of the first result
        - result_0_pageid (int): Page ID of the first result
        - result_0_wordcount (int): Word count of the first result
        - result_0_timestamp (str): Timestamp of the first result
        - result_1_title (str): Title of the second result
        - result_1_snippet (str): Snippet of the second result
        - result_1_pageid (int): Page ID of the second result
        - result_1_wordcount (int): Word count of the second result
        - result_1_timestamp (str): Timestamp of the second result
    """
    return {
        "query": "Python programming",
        "result_0_title": "Python (programming language)",
        "result_0_snippet": "Python is a high-level, interpreted programming language...",
        "result_0_pageid": 28316,
        "result_0_wordcount": 15000,
        "result_0_timestamp": "2023-10-01T12:00:00Z",
        "result_1_title": "CPython",
        "result_1_snippet": "CPython is the reference implementation of Python...",
        "result_1_pageid": 56789,
        "result_1_wordcount": 4500,
        "result_1_timestamp": "2023-09-15T08:30:00Z"
    }

def wikipedia_integration_server_search_wikipedia(query: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Search Wikipedia for articles matching a query.

    Args:
        query (str): The search query to look up on Wikipedia.
        limit (Optional[int]): Maximum number of results to return. Defaults to 2 if not specified.

    Returns:
        Dict containing:
        - query (str): The original search query used.
        - results (List[Dict]): List of article results, each with 'title', 'snippet', 'pageid', 'wordcount', and 'timestamp'.

    Raises:
        ValueError: If query is empty or None.
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty.")

    # Set default limit if not provided
    result_limit = limit if limit is not None else 2

    # Fetch simulated external data
    api_data = call_external_api("wikipedia-integration-server-search_wikipedia")

    # Construct results list from flattened API response
    results: List[Dict[str, Any]] = []
    for i in range(min(result_limit, 2)):  # We only have 2 simulated results
        title_key = f"result_{i}_title"
        snippet_key = f"result_{i}_snippet"
        pageid_key = f"result_{i}_pageid"
        wordcount_key = f"result_{i}_wordcount"
        timestamp_key = f"result_{i}_timestamp"

        if title_key in api_data:
            results.append({
                "title": api_data[title_key],
                "snippet": api_data[snippet_key],
                "pageid": api_data[pageid_key],
                "wordcount": api_data[wordcount_key],
                "timestamp": api_data[timestamp_key]
            })

    return {
        "query": query,
        "results": results
    }