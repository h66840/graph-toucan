from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ChEMBL official name lookup.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - official_name (str): The official name corresponding to the given ChEMBL ID
        - chembl_id (str): The ChEMBL ID that was queried
        - success (bool): Indicates whether the lookup was successful
        - error_message (str): Descriptive message if the lookup failed
    """
    return {
        "official_name": "Aspirin",
        "chembl_id": "CHEMBL25",
        "success": True,
        "error_message": ""
    }

def chembl_server_example_official_utils(chembl_id: str) -> Dict[str, Any]:
    """
    Get official name for the ChEMBL ID.
    
    Args:
        chembl_id (str): ChEMBL ID
        
    Returns:
        Dict containing:
        - official_name (str): The official name corresponding to the given ChEMBL ID
        - chembl_id (str): The ChEMBL ID that was queried
        - success (bool): Indicates whether the lookup was successful
        - error_message (str): Descriptive message if the lookup failed
    """
    if not chembl_id or not isinstance(chembl_id, str):
        return {
            "official_name": "",
            "chembl_id": chembl_id or "",
            "success": False,
            "error_message": "Invalid ChEMBL ID provided"
        }
    
    # Call external API simulation
    api_data = call_external_api("chembl-server-example_official_utils")
    
    # Construct result matching output schema
    result = {
        "official_name": api_data["official_name"],
        "chembl_id": api_data["chembl_id"],
        "success": api_data["success"],
        "error_message": api_data["error_message"]
    }
    
    return result