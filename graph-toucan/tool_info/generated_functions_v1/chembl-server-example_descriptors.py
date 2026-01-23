from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for chemical descriptors.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_title (str): title of the HTTP error, e.g., "Error: 422 Unprocessable Entity"
        - error_status_code (int): numeric HTTP status code extracted from the error title
        - error_message (str): detailed error message describing what went wrong
        - requested_url (str): URL that caused the error, as shown in the error page
        - description (str): human-readable explanation of the error or why the request failed
    """
    return {
        "error_title": "Error: 422 Unprocessable Entity",
        "error_status_code": 422,
        "error_message": "Unprocessable Entity",
        "requested_url": "https://www.ebi.ac.uk/chembl/api/utils/descriptors",
        "description": "The provided SMILES string could not be processed due to invalid format or unsupported characters."
    }

def chembl_server_example_descriptors(smiles: str) -> Dict[str, Any]:
    """
    Get descriptors for the SMILES string.
    
    This function simulates querying a ChEMBL server to retrieve molecular descriptors
    based on a given SMILES (Simplified Molecular Input Line Entry System) string.
    
    Args:
        smiles (str): SMILES string representing the molecular structure (required)
        
    Returns:
        Dictionary containing error information with the following keys:
        - error_title (str): title of the HTTP error, e.g., "Error: 422 Unprocessable Entity"
        - error_status_code (int): numeric HTTP status code extracted from the error title
        - error_message (str): detailed error message describing what went wrong
        - requested_url (str): URL that caused the error, as shown in the error page
        - description (str): human-readable explanation of the error or why the request failed
    
    Note:
        In a real implementation, this would connect to the ChEMBL API and return molecular
        descriptors such as molecular weight, logP, TPSA, etc. This version simulates an error
        response for demonstration purposes.
    """
    if not isinstance(smiles, str):
        raise TypeError("SMILES must be a string")
    
    if not smiles.strip():
        raise ValueError("SMILES string cannot be empty or whitespace")
    
    # Simulate calling external API
    api_data = call_external_api("chembl-server-example_descriptors")
    
    # Construct result dictionary matching expected output schema
    result = {
        "error_title": api_data["error_title"],
        "error_status_code": api_data["error_status_code"],
        "error_message": api_data["error_message"],
        "requested_url": api_data["requested_url"],
        "description": api_data["description"]
    }
    
    return result