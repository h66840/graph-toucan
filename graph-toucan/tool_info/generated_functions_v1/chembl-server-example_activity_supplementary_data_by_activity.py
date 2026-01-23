from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ChEMBL supplementary activity data.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - supplementary_data_0_key (str): Key of the first supplementary data entry
        - supplementary_data_0_value (str): Value of the first supplementary data entry
        - supplementary_data_1_key (str): Key of the second supplementary data entry
        - supplementary_data_1_value (str): Value of the second supplementary data entry
        - count (int): Total number of supplementary data entries returned
        - activity_chembl_id (str): The ChEMBL ID of the activity
        - success (bool): Whether the request was successful
        - error_message (str): Error message if request failed, null otherwise
    """
    return {
        "supplementary_data_0_key": "assay_condition",
        "supplementary_data_0_value": "pH 7.4, 37°C",
        "supplementary_data_1_key": "vendor_info",
        "supplementary_data_1_value": "Compound sourced from Sigma-Aldrich",
        "count": 2,
        "activity_chembl_id": "ACT1234567",
        "success": True,
        "error_message": None
    }

def chembl_server_example_activity_supplementary_data_by_activity(activity_chembl_id: str) -> Dict[str, Any]:
    """
    Get supplementary activity data for the specified activity_chembl_id.
    
    Args:
        activity_chembl_id (str): ChEMBL activity ID
        
    Returns:
        Dict containing:
        - supplementary_data (List[Dict]): List of supplementary activity data entries
        - count (int): Total number of supplementary data entries returned
        - activity_chembl_id (str): The ChEMBL ID of the activity
        - success (bool): Whether the request was successful
        - error_message (str): Error message if request failed, None otherwise
    """
    # Input validation
    if not activity_chembl_id or not isinstance(activity_chembl_id, str):
        return {
            "supplementary_data": [],
            "count": 0,
            "activity_chembl_id": "",
            "success": False,
            "error_message": "Invalid activity_chembl_id: must be a non-empty string"
        }
    
    try:
        # Call external API to get flat data
        api_data = call_external_api("chembl-server-example_activity_supplementary_data_by_activity")
        
        # Construct supplementary_data list from indexed fields
        supplementary_data = [
            {
                "key": api_data["supplementary_data_0_key"],
                "value": api_data["supplementary_data_0_value"]
            },
            {
                "key": api_data["supplementary_data_1_key"],
                "value": api_data["supplementary_data_1_value"]
            }
        ]
        
        # Build final result structure matching output schema
        result = {
            "supplementary_data": supplementary_data,
            "count": api_data["count"],
            "activity_chembl_id": api_data["activity_chembl_id"],
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }
        
        return result
        
    except Exception as e:
        return {
            "supplementary_data": [],
            "count": 0,
            "activity_chembl_id": activity_chembl_id,
            "success": False,
            "error_message": f"Unexpected error occurred: {str(e)}"
        }