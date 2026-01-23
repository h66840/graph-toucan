from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for structural alerts.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_status (str): HTTP error status string such as "422 Unprocessable Entity"
        - error_title (str): title of the error page, e.g., "Error: 422 Unprocessable Entity"
        - requested_url (str): the URL that caused the error, typically from the 'tt' tag in response
        - error_message (str): detailed error message from the 'pre' block, e.g., "Unprocessable Entity"
        - html_response (str): full raw HTML content returned by the server, for fallback parsing or logging
        - alert_0_description (str): Description of the first structural alert
        - alert_0_rule_set (str): Rule set name for the first structural alert
        - alert_1_description (str): Description of the second structural alert
        - alert_1_rule_set (str): Rule set name for the second structural alert
    """
    return {
        "error_status": "",
        "error_title": "",
        "requested_url": "https://example.chembl/structural_alerts?smiles=Cc1ccc2c(N)ncnc2n1",
        "error_message": "",
        "html_response": "<html><body>No critical alerts found.</body></html>",
        "alert_0_description": "Aromatic nitro group present",
        "alert_0_rule_set": "Derek Nexus",
        "alert_1_description": "Potential mutagenicity alert",
        "alert_1_rule_set": "SARpy"
    }

def chembl_server_example_structuralAlerts(smiles: str) -> Dict[str, Any]:
    """
    Get structural alerts for a given SMILES string.

    Args:
        smiles (str): SMILES string representing the chemical structure

    Returns:
        Dict containing either structural alerts or error information with the following keys:
        - error_status (str): HTTP error status string such as "422 Unprocessable Entity"
        - error_title (str): title of the error page, e.g., "Error: 422 Unprocessable Entity"
        - requested_url (str): the URL that caused the error, typically from the 'tt' tag in response
        - error_message (str): detailed error message from the 'pre' block, e.g., "Unprocessable Entity"
        - html_response (str): full raw HTML content returned by the server, for fallback parsing or logging
        - structural_alerts (List[Dict]): List of structural alert dictionaries with keys 'description' and 'rule_set'

    Note:
        This is a simulated implementation that returns example data.
        In a real implementation, this would connect to the ChEMBL structural alerts service.
    """
    if not smiles or not isinstance(smiles, str) or not smiles.strip():
        return {
            "error_status": "422 Unprocessable Entity",
            "error_title": "Error: 422 Unprocessable Entity",
            "requested_url": "",
            "error_message": "Invalid SMILES string provided",
            "html_response": "<html><head><title>Error: 422 Unprocessable Entity</title></head><body><h1>Unprocessable Entity</h1><p>The provided SMILES string is invalid or empty.</p></body></html>",
            "structural_alerts": []
        }

    api_data = call_external_api("chembl-server-example_structuralAlerts")
    
    # Construct structural alerts list from flattened API response
    structural_alerts = [
        {
            "description": api_data["alert_0_description"],
            "rule_set": api_data["alert_0_rule_set"]
        },
        {
            "description": api_data["alert_1_description"],
            "rule_set": api_data["alert_1_rule_set"]
        }
    ]
    
    return {
        "error_status": api_data["error_status"],
        "error_title": api_data["error_title"],
        "requested_url": api_data["requested_url"],
        "error_message": api_data["error_message"],
        "html_response": api_data["html_response"],
        "structural_alerts": structural_alerts
    }