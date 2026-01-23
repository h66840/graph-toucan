from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Sci-Hub paper search by title.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - doi (str): Digital Object Identifier of the paper if found
        - status (str): status of the search request; possible values include "not_found" or "found"
    """
    # Simulated response based on tool name
    if tool_name == "sci-hub-mcp-server-search_scihub_by_title":
        return {
            "doi": "10.1038/nature12373",
            "status": "found"
        }
    else:
        return {
            "doi": "",
            "status": "not_found"
        }

def sci_hub_mcp_server_search_scihub_by_title(title: str) -> Dict[str, str]:
    """
    Searches Sci-Hub for a paper by its title and returns the DOI and status.
    
    Args:
        title (str): The title of the scientific paper to search for. Must be a non-empty string.
    
    Returns:
        Dict[str, str]: A dictionary containing:
            - 'doi' (str): The Digital Object Identifier of the paper if found, otherwise empty string.
            - 'status' (str): The status of the search, either 'found' or 'not_found'.
    
    Raises:
        ValueError: If the title is empty or not a string.
    """
    # Input validation
    if not isinstance(title, str):
        raise ValueError("Title must be a string.")
    if not title.strip():
        raise ValueError("Title cannot be empty or whitespace.")
    
    # Call external API simulation
    api_data = call_external_api("sci-hub-mcp-server-search_scihub_by_title")
    
    # Construct result matching output schema
    result = {
        "doi": api_data["doi"] if api_data["status"] == "found" else "",
        "status": api_data["status"]
    }
    
    return result