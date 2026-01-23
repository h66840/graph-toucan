from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar papers citations.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - citation_0_title (str): Title of the first cited paper
        - citation_0_year (int): Year of the first cited paper
        - citation_0_authors (str): Comma-separated authors of the first cited paper
        - citation_0_url (str): URL of the first cited paper
        - citation_0_influential (bool): Whether the first citation is influential
        - citation_1_title (str): Title of the second cited paper
        - citation_1_year (int): Year of the second cited paper
        - citation_1_authors (str): Comma-separated authors of the second cited paper
        - citation_1_url (str): URL of the second cited paper
        - citation_1_influential (bool): Whether the second citation is influential
        - next_offset (int): Offset for retrieving the next page of results
        - total_results_note (str): Message indicating additional citations exist
    """
    return {
        "citation_0_title": "A Study on Neural Networks and Deep Learning",
        "citation_0_year": 2021,
        "citation_0_authors": "Alice Johnson, Bob Smith",
        "citation_0_url": "https://example.com/paper1",
        "citation_0_influential": True,
        "citation_1_title": "Advancements in Natural Language Processing",
        "citation_1_year": 2020,
        "citation_1_authors": "Carol Davis, David Wilson",
        "citation_1_url": "https://example.com/paper2",
        "citation_1_influential": False,
        "next_offset": 2,
        "total_results_note": "More citations are available. Use offset=2 to retrieve the next page."
    }

def ai_research_assistant_semantic_scholar_papers_citations(
    paperId: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get papers that cite a specific paper using its Semantic Scholar ID, arXiv ID, or DOI.
    
    Args:
        paperId (str): Required. The ID of the paper (Semantic Scholar ID, arXiv ID, DOI, etc.)
        limit (Optional[int]): Maximum number of citations to return. Defaults to None.
        offset (Optional[int]): Offset for pagination. Defaults to None.
    
    Returns:
        Dict containing:
        - citations (List[Dict]): List of citation entries with 'title', 'year', 'authors', 'url', and optional 'influential'
        - next_offset (int): Offset value to use for retrieving the next page of results
        - total_results_note (str): Message indicating that additional citations exist and how to access them
    
    Raises:
        ValueError: If paperId is empty or not provided
    """
    if not paperId:
        raise ValueError("paperId is required and cannot be empty")

    # Fetch simulated external data
    api_data = call_external_api("ai-research-assistant---semantic-scholar-papers-citations")

    # Construct citations list from flattened API response
    citations = [
        {
            "title": api_data["citation_0_title"],
            "year": api_data["citation_0_year"],
            "authors": api_data["citation_0_authors"].split(", "),
            "url": api_data["citation_0_url"],
            "influential": api_data["citation_0_influential"]
        },
        {
            "title": api_data["citation_1_title"],
            "year": api_data["citation_1_year"],
            "authors": api_data["citation_1_authors"].split(", "),
            "url": api_data["citation_1_url"],
            "influential": api_data["citation_1_influential"]
        }
    ]

    # Apply limit if specified
    if limit is not None and limit > 0:
        citations = citations[:limit]

    # Construct final result
    result = {
        "citations": citations,
        "next_offset": api_data["next_offset"],
        "total_results_note": api_data["total_results_note"]
    }

    return result