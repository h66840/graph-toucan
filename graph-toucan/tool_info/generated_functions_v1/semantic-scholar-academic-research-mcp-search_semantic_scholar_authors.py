from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar author search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_name (str): Name of the first author result
        - result_0_affiliation (str): Affiliation of the first author
        - result_0_h_index (int): H-index of the first author
        - result_0_publication_count (int): Publication count of the first author
        - result_0_author_id (str): Semantic Scholar profile ID of the first author
        - result_1_name (str): Name of the second author result
        - result_1_affiliation (str): Affiliation of the second author
        - result_1_h_index (int): H-index of the second author
        - result_1_publication_count (int): Publication count of the second author
        - result_1_author_id (str): Semantic Scholar profile ID of the second author
        - total_count (int): Total number of authors matching the query
        - next_cursor (str): Pagination token for next page of results
        - metadata_query_time_ms (int): Time taken to process the query in milliseconds
        - metadata_api_version (str): Version of the Semantic Scholar API used
        - metadata_warning (str): Any warning message from the service
    """
    return {
        "result_0_name": "Dr. Emily Johnson",
        "result_0_affiliation": "Stanford University",
        "result_0_h_index": 45,
        "result_0_publication_count": 128,
        "result_0_author_id": "S2039485712",
        "result_1_name": "Prof. Michael Chen",
        "result_1_affiliation": "Massachusetts Institute of Technology",
        "result_1_h_index": 38,
        "result_1_publication_count": 97,
        "result_1_author_id": "S2098765431",
        "total_count": 156,
        "next_cursor": "cursor_abc123xyz",
        "metadata_query_time_ms": 142,
        "metadata_api_version": "v1",
        "metadata_warning": "Query returned partial results; consider refining search terms."
    }

def semantic_scholar_academic_research_mcp_search_semantic_scholar_authors(
    query: str, 
    limit: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search for authors on Semantic Scholar using a query string.

    Args:
        query (str): Search query string for author names (required)
        limit (int, optional): Number of results to return (default: 10, max: 100)

    Returns:
        Dict containing:
        - results (List[Dict]): List of author records with name, affiliation, h-index,
          publication count, and Semantic Scholar profile ID
        - total_count (int): Total number of authors found matching the query
        - next_cursor (str): Opaque token for retrieving next page of results
        - metadata (Dict): Additional info including query time, API version, warnings

    Raises:
        ValueError: If query is empty or limit is not within valid range
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty.")
    
    if limit is None:
        limit = 10
    elif not isinstance(limit, int) or limit < 1 or limit > 100:
        raise ValueError("Limit must be an integer between 1 and 100.")

    # Call simulated external API
    api_data = call_external_api("semantic-scholar-academic-research-mcp-search_semantic_scholar_authors")

    # Construct results list from flattened API response
    results = []
    for i in range(min(limit, 2)):  # Only 2 simulated results available
        result_key = f"result_{i}"
        if f"{result_key}_name" in api_data:
            results.append({
                "name": api_data[f"{result_key}_name"],
                "affiliation": api_data[f"{result_key}_affiliation"],
                "h_index": api_data[f"{result_key}_h_index"],
                "publication_count": api_data[f"{result_key}_publication_count"],
                "author_id": api_data[f"{result_key}_author_id"]
            })

    # Construct metadata
    metadata = {
        "query_time_ms": api_data["metadata_query_time_ms"],
        "api_version": api_data["metadata_api_version"],
        "warning": api_data["metadata_warning"]
    }

    # Construct final response
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "next_cursor": api_data["next_cursor"],
        "metadata": metadata
    }