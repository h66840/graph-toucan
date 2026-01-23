from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar academic research tool.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_snippet (str): Text snippet from the first matching paper
        - result_0_title (str): Title of the first paper
        - result_0_authors (str): Authors of the first paper as a comma-separated string
        - result_0_year (int): Publication year of the first paper
        - result_0_paperId (str): Unique paper ID of the first paper
        - result_0_url (str): URL to the first paper
        - result_0_citationCount (int): Citation count of the first paper
        - result_1_snippet (str): Text snippet from the second matching paper
        - result_1_title (str): Title of the second paper
        - result_1_authors (str): Authors of the second paper as a comma-separated string
        - result_1_year (int): Publication year of the second paper
        - result_1_paperId (str): Unique paper ID of the second paper
        - result_1_url (str): URL to the second paper
        - result_1_citationCount (int): Citation count of the second paper
        - total_count (int): Total number of matching snippets found
        - next_cursor (str): Cursor token for pagination (or empty string if none)
        - query_time_ms (int): Time taken for the query in milliseconds
        - metadata_ranking_criteria (str): Ranking method used (e.g., relevance)
        - metadata_data_freshness (str): Date of latest data ingestion
        - metadata_partial_results (bool): Whether results are partial due to limits
    """
    return {
        "result_0_snippet": "Recent advances in transformer models have significantly improved performance in natural language processing tasks.",
        "result_0_title": "Transformers in NLP: A Comprehensive Review",
        "result_0_authors": "Alice Johnson, Bob Smith",
        "result_0_year": 2022,
        "result_0_paperId": "abcd1234efgh5678",
        "result_0_url": "https://www.semanticscholar.org/paper/abcd1234efgh5678",
        "result_0_citationCount": 154,
        "result_1_snippet": "Attention mechanisms allow models to focus on relevant parts of input sequences, enhancing interpretability and accuracy.",
        "result_1_title": "Attention Is All You Need",
        "result_1_authors": "Vaswani Ashish, Shazeer Noam",
        "result_1_year": 2017,
        "result_1_paperId": "efgh9012ijkl3456",
        "result_1_url": "https://www.semanticscholar.org/paper/efgh9012ijkl3456",
        "result_1_citationCount": 35000,
        "total_count": 842,
        "next_cursor": "cursor_98765",
        "query_time_ms": 45,
        "metadata_ranking_criteria": "relevance",
        "metadata_data_freshness": "2023-10-01",
        "metadata_partial_results": False
    }

def semantic_scholar_academic_research_mcp_search_semantic_scholar_snippets(
    query: str, 
    limit: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search for text snippets from academic papers that match the given query.
    
    Args:
        query (str): Plain-text search query (required)
        limit (int, optional): Number of results to return (default: 10, max: 1000)
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with snippet and paper metadata
        - total_count (int): Total number of matching snippets found
        - next_cursor (str): Pagination cursor for next page of results
        - query_time_ms (int): Backend query execution time in milliseconds
        - metadata (Dict): Additional context about the search (ranking, freshness, warnings)
    
    Raises:
        ValueError: If query is empty or limit is not between 1 and 1000
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty.")
    
    if limit is None:
        limit = 10
    elif not (1 <= limit <= 1000):
        raise ValueError("Limit must be between 1 and 1000.")
    
    # Fetch simulated external API data
    api_data = call_external_api("semantic-scholar-academic-research-mcp-search_semantic_scholar_snippets")
    
    # Construct results list from indexed fields
    results: List[Dict[str, Any]] = []
    
    for i in range(2):  # Only two results available from mock API
        snippet_key = f"result_{i}_snippet"
        if snippet_key not in api_data:
            break
            
        result = {
            "snippet": api_data[f"result_{i}_snippet"],
            "title": api_data[f"result_{i}_title"],
            "authors": api_data[f"result_{i}_authors"].split(", "),
            "year": api_data[f"result_{i}_year"],
            "paperId": api_data[f"result_{i}_paperId"],
            "url": api_data[f"result_{i}_url"],
            "citationCount": api_data[f"result_{i}_citationCount"]
        }
        results.append(result)
    
    # Truncate results to requested limit
    results = results[:limit]
    
    # Build metadata dictionary
    metadata = {
        "ranking_criteria": api_data["metadata_ranking_criteria"],
        "data_freshness": api_data["metadata_data_freshness"],
        "partial_results": api_data["metadata_partial_results"]
    }
    
    # Construct final response
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "next_cursor": api_data["next_cursor"] if api_data["next_cursor"] else None,
        "query_time_ms": api_data["query_time_ms"],
        "metadata": metadata
    }