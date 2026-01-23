from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for academic author keywords.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): indicates whether the request was successful
        - author (str): full name of the author
        - institution (str): affiliated institution of the author
        - source (str): source of the keyword data
        - total_keywords (int): total number of research keywords
        - keyword_0 (str): first research keyword
        - keyword_1 (str): second research keyword
    """
    return {
        "success": True,
        "author": "John Smith",
        "institution": "Stanford University",
        "source": "Google Scholar",
        "total_keywords": 2,
        "keyword_0": "Machine Learning",
        "keyword_1": "Natural Language Processing"
    }

def academic_author_network_get_author_keywords(name: str, surname: str, institution: Optional[str] = None) -> Dict[str, Any]:
    """
    Get research keywords/areas for a given author from Google Scholar.
    
    Args:
        name (str): Author's first name
        surname (str): Author's last name
        institution (Optional[str]): Optional institution affiliation
    
    Returns:
        Dictionary containing keywords extracted from Google Scholar with the following structure:
        - success (bool): indicates whether the request to retrieve author keywords was successful
        - author (str): full name of the author for whom keywords were retrieved
        - institution (str or None): affiliated institution of the author, if available
        - source (str): source of the keyword data, e.g., "Google Scholar"
        - total_keywords (int): total number of research keywords associated with the author
        - keywords (List[str]): list of research keywords/areas extracted from the author's profile
    """
    # Input validation
    if not name or not isinstance(name, str):
        raise ValueError("Author's first name is required and must be a non-empty string.")
    if not surname or not isinstance(surname, str):
        raise ValueError("Author's last name is required and must be a non-empty string.")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("academic-author-network-get_author_keywords")
    
    # Construct the keywords list from indexed fields
    keywords = [
        api_data["keyword_0"],
        api_data["keyword_1"]
    ]
    
    # Build the final result structure as per output schema
    result = {
        "success": api_data["success"],
        "author": api_data["author"],
        "institution": api_data["institution"] if api_data["institution"] else institution,
        "source": api_data["source"],
        "total_keywords": api_data["total_keywords"],
        "keywords": keywords
    }
    
    return result