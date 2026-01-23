from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for bioassay search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if request fails
        - message (str): Detailed error explanation including failed URL and reference link
    """
    return {
        "error": "",
        "message": "Success: Bioassay search completed for query 'aspirin'. Max results: 5. See https://pubchem.ncbi.nlm.nih.gov/docs for details."
    }

def pubchem_data_access_server_search_bioassay(query: str, max_results: Optional[int] = 5) -> Dict[str, Any]:
    """
    Search for bioassays related to a compound or target.
    
    Args:
        query (str): Search query (compound name, target name, etc.)
        max_results (int, optional): Maximum number of results to return. Default is 5.
        
    Returns:
        Dictionary with bioassay search results containing:
        - error (str): error message returned when the HTTP request fails, includes HTTP status code and description
        - message (str): detailed error explanation including the failed URL and reference link for troubleshooting
    """
    if not query or not query.strip():
        return {
            "error": "Invalid input",
            "message": "Query parameter is required and cannot be empty."
        }
    
    if max_results is not None and (not isinstance(max_results, int) or max_results <= 0):
        return {
            "error": "Invalid input",
            "message": "max_results must be a positive integer."
        }

    # Call the external API helper to simulate data retrieval
    api_data = call_external_api("pubchem_data_access_server_search_bioassay")
    
    # Construct the result using the data from the external API
    result = {
        "error": api_data["error"],
        "message": api_data["message"].replace("aspirin", query.strip()).replace("5", str(max_results))
    }
    
    return result