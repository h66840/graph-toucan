from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): current status of the API, e.g., "Online" or "Offline"
    """
    return {
        "status": "Online"
    }

def erick_wendel_contributions_check_status() -> Dict[str, Any]:
    """
    Check if the API is alive and responding.
    
    This function queries the external API to determine its current status.
    It returns a dictionary with the status field indicating whether the API is online or offline.
    
    Returns:
        Dict[str, Any]: A dictionary containing the following field:
            - status (str): current status of the API, e.g., "Online" or "Offline"
    """
    try:
        # Fetch data from external API
        api_data = call_external_api("erick-wendel-contributions-check_status")
        
        # Construct result matching output schema
        result = {
            "status": api_data["status"]
        }
        
        return result
    except Exception as e:
        # In case of any error, return offline status
        return {
            "status": "Offline"
        }