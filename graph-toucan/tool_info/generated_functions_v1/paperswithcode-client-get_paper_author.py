from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode author retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - author_id (str): The unique ID of the author
        - author_name (str): Full name of the author
        - author_affiliation (str): Current academic or organizational affiliation
        - author_homepage (str): URL to the author's homepage
        - author_paper_0_id (str): ID of the first related paper
        - author_paper_1_id (str): ID of the second related paper
        - success (bool): Whether the request was successful
        - error_message (str): Error message if request failed, otherwise empty string
    """
    return {
        "author_id": "author_12345",
        "author_name": "Dr. Jane Smith",
        "author_affiliation": "Stanford University",
        "author_homepage": "https://janesmith.stanford.edu",
        "author_paper_0_id": "paper_001",
        "author_paper_1_id": "paper_002",
        "success": True,
        "error_message": ""
    }

def paperswithcode_client_get_paper_author(author_id: str) -> Dict[str, Any]:
    """
    Get a paper author by ID in PapersWithCode.
    
    This function retrieves detailed information about an author including their name,
    affiliation, homepage, and related paper IDs using the PapersWithCode API.
    
    Args:
        author_id (str): The unique identifier for the author (required)
    
    Returns:
        Dict containing:
        - author (Dict): Author details with keys 'id', 'name', 'affiliation', 'homepage', 'papers' (List[str])
        - success (bool): Whether the author was successfully retrieved
        - error_message (str): Optional error message if the request failed
    
    Example:
        {
            "author": {
                "id": "author_12345",
                "name": "Dr. Jane Smith",
                "affiliation": "Stanford University",
                "homepage": "https://janesmith.stanford.edu",
                "papers": ["paper_001", "paper_002"]
            },
            "success": True,
            "error_message": ""
        }
    """
    # Input validation
    if not author_id or not isinstance(author_id, str) or not author_id.strip():
        return {
            "author": {
                "id": "",
                "name": "",
                "affiliation": "",
                "homepage": "",
                "papers": []
            },
            "success": False,
            "error_message": "Invalid author_id: must be a non-empty string"
        }
    
    # Call external API (simulated)
    api_data = call_external_api("paperswithcode-client-get_paper_author")
    
    # Construct the author object from flattened API response
    author = {
        "id": api_data.get("author_id", ""),
        "name": api_data.get("author_name", ""),
        "affiliation": api_data.get("author_affiliation", ""),
        "homepage": api_data.get("author_homepage", ""),
        "papers": []
    }
    
    # Add papers if they exist in the response
    paper_0_id = api_data.get("author_paper_0_id")
    paper_1_id = api_data.get("author_paper_1_id")
    
    if paper_0_id:
        author["papers"].append(paper_0_id)
    if paper_1_id:
        author["papers"].append(paper_1_id)
    
    # Get success status and error message
    success = api_data.get("success", False)
    error_message = api_data.get("error_message", "")
    
    return {
        "author": author,
        "success": success,
        "error_message": error_message
    }