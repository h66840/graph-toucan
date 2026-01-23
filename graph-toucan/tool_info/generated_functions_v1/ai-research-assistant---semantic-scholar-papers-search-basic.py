from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar papers search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - total_results (int): Total number of papers matching the query
        - next_offset (int): Offset value for retrieving the next page of results
        - result_0_title (str): Title of the first paper
        - result_0_year (int): Year of publication for the first paper
        - result_0_authors (str): Authors of the first paper as a comma-separated string
        - result_0_venue (str): Venue (conference/journal) of the first paper
        - result_0_citations (int): Number of citations for the first paper
        - result_0_url (str): URL to the first paper
        - result_1_title (str): Title of the second paper
        - result_1_year (int): Year of publication for the second paper
        - result_1_authors (str): Authors of the second paper as a comma-separated string
        - result_1_venue (str): Venue (conference/journal) of the second paper
        - result_1_citations (int): Number of citations for the second paper
        - result_1_url (str): URL to the second paper
    """
    return {
        "total_results": 150,
        "next_offset": 2,
        "result_0_title": "Attention Is All You Need",
        "result_0_year": 2017,
        "result_0_authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar",
        "result_0_venue": "NeurIPS",
        "result_0_citations": 35000,
        "result_0_url": "https://www.semanticscholar.org/paper/Attention-Is-All-You-Need-Vaswani-Shazeer/...",
        "result_1_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "result_1_year": 2018,
        "result_1_authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee",
        "result_1_venue": "NAACL",
        "result_1_citations": 42000,
        "result_1_url": "https://www.semanticscholar.org/paper/BERT-Devlin-Chang/..."
    }

def ai_research_assistant_semantic_scholar_papers_search_basic(query: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Search for academic papers with a simple query using Semantic Scholar.
    
    Args:
        query (str): Search query for papers (required)
        limit (Optional[int]): Maximum number of results to return (optional, default is None)
    
    Returns:
        Dict containing:
        - total_results (int): total number of papers matching the query
        - results (List[Dict]): list of paper entries, each containing 'title', 'year', 'authors', 'venue', 'citations', and 'url' fields
        - next_offset (int): offset value to use for retrieving the next page of results
    
    Raises:
        ValueError: If query is empty or not a string
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    
    # Fetch simulated external data
    api_data = call_external_api("ai-research-assistant---semantic-scholar-papers-search-basic")
    
    # Construct results list from indexed fields
    results = [
        {
            "title": api_data["result_0_title"],
            "year": api_data["result_0_year"],
            "authors": api_data["result_0_authors"],
            "venue": api_data["result_0_venue"],
            "citations": api_data["result_0_citations"],
            "url": api_data["result_0_url"]
        },
        {
            "title": api_data["result_1_title"],
            "year": api_data["result_1_year"],
            "authors": api_data["result_1_authors"],
            "venue": api_data["result_1_venue"],
            "citations": api_data["result_1_citations"],
            "url": api_data["result_1_url"]
        }
    ]
    
    # Apply limit if specified
    if limit is not None and limit > 0:
        results = results[:limit]
    
    # Return structured response matching output schema
    return {
        "total_results": api_data["total_results"],
        "results": results,
        "next_offset": api_data["next_offset"]
    }