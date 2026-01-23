from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar author papers.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - paper_0_title (str): Title of the first paper
        - paper_0_year (int): Publication year of the first paper
        - paper_0_venue (str): Venue/conference of the first paper
        - paper_0_citations (int): Number of citations for the first paper
        - paper_0_url (str): URL to the first paper
        - paper_1_title (str): Title of the second paper
        - paper_1_year (int): Publication year of the second paper
        - paper_1_venue (str): Venue/conference of the second paper
        - paper_1_citations (int): Number of citations for the second paper
        - paper_1_url (str): URL to the second paper
        - has_more (bool): Whether more papers are available beyond this result set
        - next_offset (int): Offset value to use for fetching next page of results
    """
    return {
        "paper_0_title": "Foundations of Machine Learning: A Survey",
        "paper_0_year": 2021,
        "paper_0_venue": "Journal of Artificial Intelligence Research",
        "paper_0_citations": 156,
        "paper_0_url": "https://semanticscholar.org/paper/abc123",
        "paper_1_title": "Deep Neural Networks for Natural Language Processing",
        "paper_1_year": 2019,
        "paper_1_venue": "NeurIPS",
        "paper_1_citations": 234,
        "paper_1_url": "https://semanticscholar.org/paper/def456",
        "has_more": True,
        "next_offset": 2
    }

def ai_research_assistant_semantic_scholar_authors_papers(
    authorId: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get papers written by a specific author using their Semantic Scholar author ID.

    Args:
        authorId (str): Unique identifier for the author (required)
        limit (Optional[int]): Maximum number of papers to return (optional)
        offset (Optional[int]): Offset for pagination (optional)

    Returns:
        Dict containing:
        - papers (List[Dict]): List of paper entries with 'title', 'year', 'venue', 'citations', and 'url'
        - has_more (bool): Indicates if additional papers are available
        - next_offset (int): Recommended offset to fetch next page of results

    Raises:
        ValueError: If authorId is empty or invalid
    """
    if not authorId or not authorId.strip():
        raise ValueError("authorId is required and cannot be empty")

    # Validate limit and offset if provided
    if limit is not None and limit < 1:
        raise ValueError("limit must be a positive integer")
    if offset is not None and offset < 0:
        raise ValueError("offset must be a non-negative integer")

    # Call external API to get flattened data
    api_data = call_external_api("ai-research-assistant---semantic-scholar-authors-papers")

    # Construct papers list from indexed fields
    papers = [
        {
            "title": api_data["paper_0_title"],
            "year": api_data["paper_0_year"],
            "venue": api_data["paper_0_venue"],
            "citations": api_data["paper_0_citations"],
            "url": api_data["paper_0_url"]
        },
        {
            "title": api_data["paper_1_title"],
            "year": api_data["paper_1_year"],
            "venue": api_data["paper_1_venue"],
            "citations": api_data["paper_1_citations"],
            "url": api_data["paper_1_url"]
        }
    ]

    # Apply limit if specified
    if limit is not None:
        papers = papers[:limit]

    return {
        "papers": papers,
        "has_more": api_data["has_more"],
        "next_offset": api_data["next_offset"]
    }