from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar academic research.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - paper_0_paperId (str): Paper ID of the first result
        - paper_0_title (str): Title of the first paper
        - paper_0_abstract (str): Abstract of the first paper
        - paper_0_year (int): Publication year of the first paper
        - paper_0_authors (str): Comma-separated authors of the first paper
        - paper_0_url (str): URL to the first paper
        - paper_0_venue (str): Venue of the first paper
        - paper_0_publicationTypes (str): Publication types of the first paper (comma-separated)
        - paper_0_citationCount (int): Citation count of the first paper
        - paper_0_tldr (str): TL;DR summary of the first paper
        - paper_1_paperId (str): Paper ID of the second result
        - paper_1_title (str): Title of the second paper
        - paper_1_abstract (str): Abstract of the second paper
        - paper_1_year (int): Publication year of the second paper
        - paper_1_authors (str): Comma-separated authors of the second paper
        - paper_1_url (str): URL to the second paper
        - paper_1_venue (str): Venue of the second paper
        - paper_1_publicationTypes (str): Publication types of the second paper (comma-separated)
        - paper_1_citationCount (int): Citation count of the second paper
        - paper_1_tldr (str): TL;DR summary of the second paper
    """
    return {
        "paper_0_paperId": "1234567890abcdef",
        "paper_0_title": "A Study on Machine Learning Techniques in Academic Research",
        "paper_0_abstract": "This paper explores various machine learning techniques used in academic research with a focus on reproducibility and scalability.",
        "paper_0_year": 2022,
        "paper_0_authors": "Alice Johnson, Bob Smith",
        "paper_0_url": "https://www.semanticscholar.org/paper/1234567890abcdef",
        "paper_0_venue": "Journal of Artificial Intelligence Research",
        "paper_0_publicationTypes": "JournalArticle,Review",
        "paper_0_citationCount": 45,
        "paper_0_tldr": "We present a comprehensive analysis of ML methods in research, highlighting best practices and common pitfalls.",
        
        "paper_1_paperId": "fedcba0987654321",
        "paper_1_title": "Natural Language Processing for Scholarly Data Mining",
        "paper_1_abstract": "We propose a novel NLP framework for extracting insights from large-scale scholarly datasets.",
        "paper_1_year": 2021,
        "paper_1_authors": "Carol Davis, David Wilson",
        "paper_1_url": "https://www.semanticscholar.org/paper/fedcba0987654321",
        "paper_1_venue": "Conference on Computational Linguistics",
        "paper_1_publicationTypes": "ConferencePaper",
        "paper_1_citationCount": 67,
        "paper_1_tldr": "Our framework improves accuracy in extracting metadata and relationships from academic texts by 15%."
    }

def semantic_scholar_academic_research_mcp_search_semantic_scholar(
    query: str, 
    num_results: Optional[int] = 10
) -> List[Dict[str, Any]]:
    """
    Search for papers on Semantic Scholar using a query string.

    Args:
        query (str): Search query string (required)
        num_results (int, optional): Number of results to return (default: 10)

    Returns:
        List[Dict]: List of dictionaries containing paper information with keys:
            - paperId (str)
            - title (str)
            - abstract (str)
            - year (int)
            - authors (List[str])
            - url (str)
            - venue (str)
            - publicationTypes (List[str])
            - citationCount (int)
            - tldr (str)

    Note:
        This is a simulated implementation. In a real scenario, this would call
        an external API. Here, it uses a mock helper function that returns
        simplified scalar values which are then transformed into the required
        nested structure.
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty")

    if num_results is None:
        num_results = 10
    if num_results <= 0:
        raise ValueError("num_results must be a positive integer")

    # Fetch mock data from "external" API
    api_data = call_external_api("semantic-scholar-academic-research-mcp-search_semantic_scholar")

    # Construct results list
    results: List[Dict[str, Any]] = []

    # Process up to num_results, but we only have 2 mock items
    max_available = 2
    for i in range(min(num_results, max_available)):
        paper_data = {
            "paperId": api_data.get(f"paper_{i}_paperId", ""),
            "title": api_data.get(f"paper_{i}_title", ""),
            "abstract": api_data.get(f"paper_{i}_abstract", ""),
            "year": api_data.get(f"paper_{i}_year", 0),
            "authors": [
                author.strip() 
                for author in api_data.get(f"paper_{i}_authors", "").split(",") 
                if author.strip()
            ],
            "url": api_data.get(f"paper_{i}_url", ""),
            "venue": api_data.get(f"paper_{i}_venue", ""),
            "publicationTypes": [
                pt.strip() 
                for pt in api_data.get(f"paper_{i}_publicationTypes", "").split(",") 
                if pt.strip()
            ],
            "citationCount": api_data.get(f"paper_{i}_citationCount", 0),
            "tldr": api_data.get(f"paper_{i}_tldr", "")
        }
        results.append(paper_data)

    return results