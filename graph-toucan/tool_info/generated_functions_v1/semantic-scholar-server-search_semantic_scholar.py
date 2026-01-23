from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external Semantic Scholar API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_paperId (str): Paper ID of the first result
        - result_0_title (str): Title of the first paper
        - result_0_abstract (str): Abstract of the first paper
        - result_0_year (int): Publication year of the first paper
        - result_0_authors (str): Comma-separated authors of the first paper
        - result_0_url (str): URL to the first paper
        - result_0_venue (str): Venue of the first paper
        - result_0_publicationTypes_0 (str): First publication type of the first paper
        - result_0_citationCount (int): Citation count of the first paper
        - result_1_paperId (str): Paper ID of the second result
        - result_1_title (str): Title of the second paper
        - result_1_abstract (str): Abstract of the second paper
        - result_1_year (int): Publication year of the second paper
        - result_1_authors (str): Comma-separated authors of the second paper
        - result_1_url (str): URL to the second paper
        - result_1_venue (str): Venue of the second paper
        - result_1_publicationTypes_0 (str): First publication type of the second paper
        - result_1_citationCount (int): Citation count of the second paper
    """
    return {
        "result_0_paperId": "1a2b3c4d5e6f7g8h9i0j",
        "result_0_title": "A Study on Machine Learning Techniques",
        "result_0_abstract": "This paper explores various machine learning algorithms and their applications in real-world scenarios.",
        "result_0_year": 2022,
        "result_0_authors": "John Doe, Jane Smith",
        "result_0_url": "https://www.semanticscholar.org/paper/1a2b3c4d5e6f7g8h9i0j",
        "result_0_venue": "International Conference on Machine Learning",
        "result_0_publicationTypes_0": "Conference",
        "result_0_citationCount": 45,
        "result_1_paperId": "9z8y7x6w5v4u3t2s1r0q",
        "result_1_title": "Deep Learning for Natural Language Processing",
        "result_1_abstract": "We present a novel deep learning architecture for improving NLP tasks such as translation and summarization.",
        "result_1_year": 2021,
        "result_1_authors": "Alice Johnson, Bob Williams",
        "result_1_url": "https://www.semanticscholar.org/paper/9z8y7x6w5v4u3t2s1r0q",
        "result_1_venue": "NeurIPS",
        "result_1_publicationTypes_0": "Journal",
        "result_1_citationCount": 123,
    }

def semantic_scholar_server_search_semantic_scholar(query: str, num_results: Optional[int] = None) -> Dict[str, Any]:
    """
    Searches Semantic Scholar for academic papers based on a query string.
    
    Args:
        query (str): The search query string (required).
        num_results (Optional[int]): The number of results to return (optional, default is 2).
    
    Returns:
        Dict containing a single key 'results' with a list of paper objects.
        Each paper object is a dict with keys:
        - paperId (str)
        - title (str)
        - abstract (str)
        - year (int)
        - authors (List[str])
        - url (str)
        - venue (str)
        - publicationTypes (List[str])
        - citationCount (int)
    
    Raises:
        ValueError: If query is empty or None.
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty.")
    
    # Default to 2 results if not specified or invalid
    if num_results is None or num_results <= 0:
        num_results = 2
    
    # Fetch simulated API data
    api_data = call_external_api("semantic-scholar-server-search_semantic_scholar")
    
    # Construct results list
    results: List[Dict[str, Any]] = []
    
    # Process up to num_results (max 2 available in simulation)
    max_available = 2
    for i in range(min(num_results, max_available)):
        prefix = f"result_{i}"
        try:
            paper = {
                "paperId": api_data[f"{prefix}_paperId"],
                "title": api_data[f"{prefix}_title"],
                "abstract": api_data[f"{prefix}_abstract"],
                "year": api_data[f"{prefix}_year"],
                "authors": [author.strip() for author in api_data[f"{prefix}_authors"].split(",")],
                "url": api_data[f"{prefix}_url"],
                "venue": api_data[f"{prefix}_venue"],
                "publicationTypes": [api_data[f"{prefix}_publicationTypes_0"]],
                "citationCount": api_data[f"{prefix}_citationCount"]
            }
            results.append(paper)
        except KeyError as e:
            # In case some expected field is missing
            raise RuntimeError(f"Missing expected field in API response: {e}")
    
    return {"results": results}