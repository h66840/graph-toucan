from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching paper metadata from an external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message when metadata could not be retrieved for the given DOI
    """
    # Simulate possible error conditions based on DOI pattern
    # In a real implementation, this would be determined by actual API response
    return {
        "error": ""
    }

def sci_hub_mcp_server_get_paper_metadata(doi: str) -> Dict[str, Any]:
    """
    Retrieves metadata for a scientific paper using its DOI.
    
    This function simulates querying a Sci-Hub metadata service to retrieve
    bibliographic information about a paper given its Digital Object Identifier (DOI).
    
    Args:
        doi (str): The Digital Object Identifier (DOI) of the paper to retrieve metadata for.
                   Must be a non-empty string in valid DOI format (e.g., 10.1038/nature12373).
    
    Returns:
        Dict[str, Any]: A dictionary containing the following fields:
            - error (str): Error message when metadata could not be retrieved for the given DOI.
                          Empty string if no error occurred.
    
    Raises:
        ValueError: If the DOI is empty or not a string.
    """
    # Input validation
    if not isinstance(doi, str):
        raise ValueError("DOI must be a string")
    if not doi or not doi.strip():
        raise ValueError("DOI cannot be empty")
    
    # Call external API simulation
    api_data = call_external_api("sci-hub-mcp-server-get_paper_metadata")
    
    # Construct result following output schema
    result = {
        "error": api_data["error"]
    }
    
    return result