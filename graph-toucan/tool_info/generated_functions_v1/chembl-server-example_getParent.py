from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ChEMBL parent lookup.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - parent_chembl_id (str): The parent ChEMBL ID corresponding to the input ChEMBL ID
        - success (bool): Indicates whether the parent lookup was successful
        - error_message (str): Descriptive error message if the operation failed
    """
    # Simulated response data
    return {
        "parent_chembl_id": "CHEMBL12345",
        "success": True,
        "error_message": ""
    }

def chembl_server_example_getParent(chembl_id: str) -> Dict[str, Any]:
    """
    Get parent ChEMBL ID for the given ChEMBL ID.
    
    Args:
        chembl_id (str): ChEMBL ID (e.g., 'CHEMBL100')
        
    Returns:
        Dict containing:
        - parent_chembl_id (str): The parent ChEMBL ID corresponding to the input ChEMBL ID, if one exists
        - success (bool): Indicates whether the parent lookup was successful (e.g., valid ID and parent exists)
        - error_message (str): Descriptive error message if the operation failed, e.g., invalid ID format or no parent found
    """
    # Input validation
    if not chembl_id:
        return {
            "parent_chembl_id": "",
            "success": False,
            "error_message": "ChEMBL ID is required"
        }
    
    if not isinstance(chembl_id, str):
        return {
            "parent_chembl_id": "",
            "success": False,
            "error_message": "ChEMBL ID must be a string"
        }
    
    if not chembl_id.startswith("CHEMBL"):
        return {
            "parent_chembl_id": "",
            "success": False,
            "error_message": "Invalid ChEMBL ID format. Must start with 'CHEMBL'"
        }
    
    try:
        # Extract numeric part and validate
        id_number_str = chembl_id[6:]
        if not id_number_str.isdigit():
            return {
                "parent_chembl_id": "",
                "success": False,
                "error_message": "Invalid ChEMBL ID format. Numeric part must be digits"
            }
        
        # Call external API simulation
        api_data = call_external_api("chembl_server_example_getParent")
        
        # Construct result using API data
        result = {
            "parent_chembl_id": api_data["parent_chembl_id"],
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }
        
        return result
        
    except Exception as e:
        return {
            "parent_chembl_id": "",
            "success": False,
            "error_message": f"Unexpected error occurred: {str(e)}"
        }