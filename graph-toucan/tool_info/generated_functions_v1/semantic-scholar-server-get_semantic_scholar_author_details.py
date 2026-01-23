from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar author details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - authorId (str): unique identifier for the author in Semantic Scholar
        - name (str): full name of the author
        - url (str): public URL to the author's Semantic Scholar profile page
        - affiliations_0 (str): first institutional affiliation
        - affiliations_1 (str): second institutional affiliation
        - paperCount (int): total number of papers authored or co-authored by this researcher
        - citationCount (int): total number of citations received across all their papers
        - hIndex (int): the author's h-index as calculated by Semantic Scholar
    """
    return {
        "authorId": "1234567890",
        "name": "Dr. Jane Smith",
        "url": "https://www.semanticscholar.org/author/Jane-Smith/1234567890",
        "affiliations_0": "Stanford University",
        "affiliations_1": "Google Research",
        "paperCount": 85,
        "citationCount": 3400,
        "hIndex": 28
    }

def semantic_scholar_server_get_semantic_scholar_author_details(author_id: str) -> Dict[str, Any]:
    """
    Fetches and returns detailed information about an author from Semantic Scholar.
    
    Args:
        author_id (str): Unique identifier for the author in Semantic Scholar (required)
    
    Returns:
        Dict containing the following fields:
        - authorId (str): unique identifier for the author in Semantic Scholar
        - name (str): full name of the author
        - url (str): public URL to the author's Semantic Scholar profile page
        - affiliations (List[str]): list of current institutional affiliations of the author
        - paperCount (int): total number of papers authored or co-authored by this researcher
        - citationCount (int): total number of citations received across all their papers
        - hIndex (int): the author's h-index as calculated by Semantic Scholar
    
    Raises:
        ValueError: If author_id is empty or not provided
    """
    if not author_id or not author_id.strip():
        raise ValueError("author_id is required and cannot be empty")
    
    # Call external API to get flattened data
    api_data = call_external_api("semantic-scholar-server-get_semantic_scholar_author_details")
    
    # Construct nested structure matching output schema
    result = {
        "authorId": api_data["authorId"],
        "name": api_data["name"],
        "url": api_data["url"],
        "affiliations": [
            api_data["affiliations_0"],
            api_data["affiliations_1"]
        ],
        "paperCount": api_data["paperCount"],
        "citationCount": api_data["citationCount"],
        "hIndex": api_data["hIndex"]
    }
    
    return result