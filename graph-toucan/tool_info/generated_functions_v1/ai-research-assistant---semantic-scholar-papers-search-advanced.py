from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar paper search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - total_results (int): Total number of papers matching the query
        - next_offset (int): Offset value for retrieving next page of results
        - result_0_title (str): Title of the first paper
        - result_0_year (int): Publication year of the first paper
        - result_0_authors (str): Authors of the first paper (comma-separated)
        - result_0_venue (str): Venue of the first paper
        - result_0_citations (int): Number of citations for the first paper
        - result_0_url (str): URL to the first paper
        - result_0_open_access (bool): Whether the first paper is open access
        - result_1_title (str): Title of the second paper
        - result_1_year (int): Publication year of the second paper
        - result_1_authors (str): Authors of the second paper (comma-separated)
        - result_1_venue (str): Venue of the second paper
        - result_1_citations (int): Number of citations for the second paper
        - result_1_url (str): URL to the second paper
        - result_1_open_access (bool): Whether the second paper is open access
    """
    return {
        "total_results": 42,
        "next_offset": 2,
        "result_0_title": "A Survey on Transformer-based Models in Natural Language Processing",
        "result_0_year": 2023,
        "result_0_authors": "John Doe, Jane Smith",
        "result_0_venue": "Transactions of the ACL",
        "result_0_citations": 156,
        "result_0_url": "https://semanticscholar.org/paper/1234567890",
        "result_0_open_access": True,
        "result_1_title": "Efficient Attention Mechanisms for Long Sequences",
        "result_1_year": 2022,
        "result_1_authors": "Alice Johnson, Bob Lee",
        "result_1_venue": "NeurIPS",
        "result_1_citations": 89,
        "result_1_url": "https://semanticscholar.org/paper/0987654321",
        "result_1_open_access": False,
    }

def ai_research_assistant_semantic_scholar_papers_search_advanced(
    query: str,
    fieldsOfStudy: Optional[List[str]] = None,
    limit: Optional[int] = None,
    minCitations: Optional[int] = None,
    openAccessOnly: Optional[bool] = None,
    publicationTypes: Optional[List[str]] = None,
    sortBy: Optional[str] = None,
    sortOrder: Optional[str] = None,
    yearEnd: Optional[int] = None,
    yearStart: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for academic papers with advanced filtering options using Semantic Scholar.
    
    Args:
        query (str): Search query for papers (required)
        fieldsOfStudy (List[str], optional): Fields of study to filter by
        limit (int, optional): Maximum number of results to return
        minCitations (int, optional): Minimum number of citations
        openAccessOnly (bool, optional): Only include open access papers
        publicationTypes (List[str], optional): Publication types to filter by
        sortBy (str, optional): Field to sort by
        sortOrder (str, optional): Sort order (ascending or descending)
        yearEnd (int, optional): Ending year for filtering (inclusive)
        yearStart (int, optional): Starting year for filtering (inclusive)
    
    Returns:
        Dict containing:
        - total_results (int): total number of papers matching the query
        - results (List[Dict]): list of paper entries with 'title', 'year', 'authors', 
          'venue', 'citations', 'url', and optional 'open_access' fields
        - next_offset (int): offset value to use for retrieving the next page of results
    
    Raises:
        ValueError: If query is empty or None
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")
    
    # Fetch simulated external data
    api_data = call_external_api("ai-research-assistant---semantic-scholar-papers-search-advanced")
    
    # Construct results list from flattened API data
    results = []
    
    # Process first result if available
    if "result_0_title" in api_data:
        result_0 = {
            "title": api_data["result_0_title"],
            "year": api_data["result_0_year"],
            "authors": api_data["result_0_authors"].split(", "),
            "venue": api_data["result_0_venue"],
            "citations": api_data["result_0_citations"],
            "url": api_data["result_0_url"]
        }
        if "result_0_open_access" in api_data:
            result_0["open_access"] = api_data["result_0_open_access"]
        results.append(result_0)
    
    # Process second result if available
    if "result_1_title" in api_data:
        result_1 = {
            "title": api_data["result_1_title"],
            "year": api_data["result_1_year"],
            "authors": api_data["result_1_authors"].split(", "),
            "venue": api_data["result_1_venue"],
            "citations": api_data["result_1_citations"],
            "url": api_data["result_1_url"]
        }
        if "result_1_open_access" in api_data:
            result_1["open_access"] = api_data["result_1_open_access"]
        results.append(result_1)
    
    # Apply limit if specified
    if limit is not None:
        results = results[:limit]
    
    # Apply minCitations filter if specified
    if minCitations is not None:
        results = [r for r in results if r["citations"] >= minCitations]
    
    # Apply openAccessOnly filter if specified
    if openAccessOnly is True:
        results = [r for r in results if r.get("open_access", False) is True]
    
    # Apply year range filter if specified
    filtered_results = []
    for r in results:
        year = r["year"]
        if yearStart is not None and year < yearStart:
            continue
        if yearEnd is not None and year > yearEnd:
            continue
        filtered_results.append(r)
    results = filtered_results
    
    # Sort results if sortBy and sortOrder are specified
    if sortBy and sortOrder and results:
        reverse = sortOrder.lower() == "desc"
        if sortBy == "year":
            results.sort(key=lambda x: x["year"], reverse=reverse)
        elif sortBy == "citations":
            results.sort(key=lambda x: x["citations"], reverse=reverse)
        elif sortBy == "title":
            results.sort(key=lambda x: x["title"].lower(), reverse=reverse)
    
    # Return final structured response
    return {
        "total_results": api_data["total_results"],
        "results": results,
        "next_offset": api_data["next_offset"]
    }