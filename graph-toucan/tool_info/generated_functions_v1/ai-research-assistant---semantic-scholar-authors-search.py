from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar authors search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_name (str): Name of the first author
        - result_0_paper_count (int): Paper count of the first author
        - result_0_citation_count (int): Citation count of the first author
        - result_0_h_index (int): H-index of the first author
        - result_0_url (str): Profile URL of the first author
        - result_1_name (str): Name of the second author
        - result_1_paper_count (int): Paper count of the second author
        - result_1_citation_count (int): Citation count of the second author
        - result_1_h_index (int): H-index of the second author
        - result_1_url (str): Profile URL of the second author
        - total_count (int): Total number of authors matching the query
    """
    return {
        "result_0_name": "Dr. Emily Johnson",
        "result_0_paper_count": 142,
        "result_0_citation_count": 8765,
        "result_0_h_index": 48,
        "result_0_url": "https://semanticscholar.org/author/12345",
        "result_1_name": "Prof. Michael Chen",
        "result_1_paper_count": 98,
        "result_1_citation_count": 5432,
        "result_1_h_index": 37,
        "result_1_url": "https://semanticscholar.org/author/67890",
        "total_count": 256
    }

def ai_research_assistant_semantic_scholar_authors_search(
    query: str, 
    limit: Optional[int] = None, 
    offset: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for authors by name or affiliation using Semantic Scholar.
    
    Args:
        query (str): Search query for authors (required)
        limit (Optional[int]): Maximum number of results to return
        offset (Optional[int]): Offset for pagination
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of author objects with 'name', 'paper_count', 
          'citation_count', 'h_index', and 'url' fields
        - total_count (int): Total number of authors matching the query
    
    Raises:
        ValueError: If query is empty or None
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")
    
    if limit is not None and limit < 1:
        raise ValueError("Limit must be a positive integer")
    
    if offset is not None and offset < 0:
        raise ValueError("Offset must be a non-negative integer")
    
    # Fetch data from simulated external API
    api_data = call_external_api("ai-research-assistant---semantic-scholar-authors-search")
    
    # Construct results list from flattened API response
    results = [
        {
            "name": api_data["result_0_name"],
            "paper_count": api_data["result_0_paper_count"],
            "citation_count": api_data["result_0_citation_count"],
            "h_index": api_data["result_0_h_index"],
            "url": api_data["result_0_url"]
        },
        {
            "name": api_data["result_1_name"],
            "paper_count": api_data["result_1_paper_count"],
            "citation_count": api_data["result_1_citation_count"],
            "h_index": api_data["result_1_h_index"],
            "url": api_data["result_1_url"]
        }
    ]
    
    # Apply limit if specified
    if limit is not None:
        results = results[:limit]
    
    # Apply offset if specified
    if offset is not None:
        results = results[offset:] if offset < len(results) else []
    
    return {
        "results": results,
        "total_count": api_data["total_count"]
    }