from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching citation data from external API for a given resource.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - citation_type (str): Type of citation (e.g., 'journal-article', 'misc')
        - title (str): Title of the cited work
        - journal (str): Name of the journal where the work was published
        - volume (str): Volume number of the journal
        - number (str): Issue number within the volume
        - pages (str): Page range of the article
        - year (str): Year of publication
        - publisher (str): Publishing organization or institution
        - author (str): Full list of authors as a formatted string
    """
    return {
        "citation_type": "journal-article",
        "title": "A Comprehensive Study on Machine Learning Techniques",
        "journal": "Journal of Artificial Intelligence Research",
        "volume": "15",
        "number": "3",
        "pages": "112-130",
        "year": "2023",
        "publisher": "AI Press",
        "author": "John Doe and Jane Smith and Robert Johnson"
    }

def citeassist_mcp_get_citeas_data(resource: str) -> Dict[str, Any]:
    """
    Retrieve BibTeX-formatted citation data for the specified resource from CiteAs.
    
    Args:
        resource (str): The resource identifier (e.g., DOI, URL, keyword) to retrieve citation for.
    
    Returns:
        Dict[str, Any]: A dictionary containing citation metadata with the following keys:
            - citation_type (str): Type of citation (e.g., 'journal-article', 'misc')
            - title (str): Title of the cited work
            - journal (str): Name of the journal where the work was published
            - volume (str): Volume number of the journal
            - number (str): Issue number within the volume
            - pages (str): Page range of the article
            - year (str): Year of publication
            - publisher (str): Publishing organization or institution
            - author (str): Full list of authors as a formatted string
    
    Raises:
        ValueError: If the resource is empty or not a string.
    """
    if not resource:
        raise ValueError("Resource parameter is required and cannot be empty.")
    
    if not isinstance(resource, str):
        raise ValueError("Resource must be a string.")
    
    # Fetch data from simulated external API
    api_data = call_external_api("citeassist-mcp-get_citeas_data")
    
    # Construct the result dictionary matching the expected output schema
    result = {
        "citation_type": api_data["citation_type"],
        "title": api_data["title"],
        "journal": api_data["journal"],
        "volume": api_data["volume"],
        "number": api_data["number"],
        "pages": api_data["pages"],
        "year": api_data["year"],
        "publisher": api_data["publisher"],
        "author": api_data["author"]
    }
    
    return result