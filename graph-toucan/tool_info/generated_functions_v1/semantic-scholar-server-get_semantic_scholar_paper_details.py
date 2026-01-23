from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar paper details.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - paperId (str): Unique identifier of the paper in Semantic Scholar
        - title (str): Title of the academic paper
        - abstract (str): Summary of the paper's content and contributions
        - year (int): Publication year of the paper
        - author_0_name (str): Name of the first author
        - author_0_authorId (str): Author ID of the first author
        - author_1_name (str): Name of the second author
        - author_1_authorId (str): Author ID of the second author
        - url (str): Direct URL to the paper on Semantic Scholar
        - venue (str): Publication venue or conference where the paper was presented
        - publicationTypes_0 (str): First publication type (e.g., "JournalArticle")
        - publicationTypes_1 (str): Second publication type (e.g., "Conference")
        - citationCount (int): Total number of citations the paper has received
    """
    return {
        "paperId": "1234567890abcdef",
        "title": "A Study on Machine Learning Techniques in Academic Research",
        "abstract": "This paper explores the application of machine learning techniques in analyzing academic research trends. We present a novel framework for identifying impactful research areas using citation networks and natural language processing.",
        "year": 2023,
        "author_0_name": "Alice Johnson",
        "author_0_authorId": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
        "author_1_name": "Bob Smith",
        "author_1_authorId": "n8m7l6k5-j4i3-2109-h8g7-f6e5d4c3b2a1",
        "url": "https://www.semanticscholar.org/paper/1234567890abcdef",
        "venue": "NeurIPS",
        "publicationTypes_0": "Conference",
        "publicationTypes_1": "JournalArticle",
        "citationCount": 42
    }

def semantic_scholar_server_get_semantic_scholar_paper_details(paper_id: str) -> Dict[str, Any]:
    """
    Retrieves detailed information about an academic paper from Semantic Scholar by its paper ID.
    
    Args:
        paper_id (str): The unique identifier of the paper in Semantic Scholar. Required.
    
    Returns:
        Dict containing the following fields:
        - paperId (str): Unique identifier of the paper in Semantic Scholar
        - title (str): Title of the academic paper
        - abstract (str): Summary of the paper's content and contributions
        - year (int): Publication year of the paper
        - authors (List[Dict]): List of author objects, each with 'name' (str) and 'authorId' (str)
        - url (str): Direct URL to the paper on Semantic Scholar
        - venue (str): Publication venue or conference where the paper was presented
        - publicationTypes (List[str]): Types of publication (e.g., "JournalArticle", "Conference")
        - citationCount (int): Total number of citations the paper has received
    
    Raises:
        ValueError: If paper_id is empty or None
    """
    if not paper_id:
        raise ValueError("paper_id is required and cannot be empty")
    
    # Fetch simulated external data
    api_data = call_external_api("semantic-scholar-server-get_semantic_scholar_paper_details")
    
    # Construct authors list from flattened fields
    authors = [
        {
            "name": api_data["author_0_name"],
            "authorId": api_data["author_0_authorId"]
        },
        {
            "name": api_data["author_1_name"],
            "authorId": api_data["author_1_authorId"]
        }
    ]
    
    # Construct publicationTypes list from flattened fields
    publication_types = [
        api_data["publicationTypes_0"],
        api_data["publicationTypes_1"]
    ]
    
    # Build final result structure matching output schema
    result = {
        "paperId": api_data["paperId"],
        "title": api_data["title"],
        "abstract": api_data["abstract"],
        "year": api_data["year"],
        "authors": authors,
        "url": api_data["url"],
        "venue": api_data["venue"],
        "publicationTypes": publication_types,
        "citationCount": api_data["citationCount"]
    }
    
    return result