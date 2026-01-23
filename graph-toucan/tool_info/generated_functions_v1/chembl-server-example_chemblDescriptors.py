from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching ChEMBL descriptors from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_status_code (int): HTTP status code of the error
        - error_title (str): Title of the error
        - error_message (str): Detailed message of the error
    """
    return {
        "error_status_code": 200,
        "error_title": "Success",
        "error_message": "Descriptors generated successfully"
    }

def chembl_server_example_chemblDescriptors(smiles: str) -> Dict[str, Any]:
    """
    Get ChEMBL descriptors for the given SMILES string.
    
    This function simulates querying a ChEMBL server to retrieve molecular descriptors
    based on the provided SMILES (Simplified Molecular Input Line Entry System) string.
    
    Args:
        smiles (str): A SMILES string representing the molecular structure
        
    Returns:
        Dictionary containing an 'error' field with status information.
        The 'error' field is a dictionary with:
        - status_code: HTTP status code
        - title: Error title or success message
        - message: Detailed description of the result
        
    Example:
        >>> chembl_server_example_chemblDescriptors("CCO")
        {'error': {'status_code': 200, 'title': 'Success', 'message': 'Descriptors generated successfully'}}
    """
    # Input validation
    if not smiles:
        return {
            "error": {
                "status_code": 400,
                "title": "Bad Request",
                "message": "SMILES string is required"
            }
        }
    
    if not isinstance(smiles, str):
        return {
            "error": {
                "status_code": 400,
                "title": "Bad Request",
                "message": "SMILES must be a string"
            }
        }
    
    # Call the external API simulation
    api_data = call_external_api("chembl-server-example_chemblDescriptors")
    
    # Construct the response with proper nested structure
    result = {
        "error": {
            "status_code": api_data["error_status_code"],
            "title": api_data["error_title"],
            "message": api_data["error_message"]
        }
    }
    
    return result