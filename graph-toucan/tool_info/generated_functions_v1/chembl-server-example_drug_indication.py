from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching drug indication data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - results_0_drug_name (str): Name of the first drug
        - results_0_chembl_id (str): ChEMBL ID of the first drug
        - results_0_mechanism_of_action (str): Mechanism of action for the first drug
        - results_0_indication_description (str): Indication description for the first drug
        - results_0_efo_id (str): EFO ID for the first drug indication
        - results_0_max_phase (int): Maximum phase of development for the first drug
        - results_1_drug_name (str): Name of the second drug
        - results_1_chembl_id (str): ChEMBL ID of the second drug
        - results_1_mechanism_of_action (str): Mechanism of action for the second drug
        - results_1_indication_description (str): Indication description for the second drug
        - results_1_efo_id (str): EFO ID for the second drug indication
        - results_1_max_phase (int): Maximum phase of development for the second drug
        - count (int): Total number of drug indication records returned
        - mesh_heading (str): The MeSH heading for which indications were retrieved
        - success (bool): Indicates whether the query was executed successfully
        - error_message (str): Optional error message if the request failed
    """
    return {
        "results_0_drug_name": "Aspirin",
        "results_0_chembl_id": "CHEMBL25",
        "results_0_mechanism_of_action": "Cyclooxygenase inhibitor",
        "results_0_indication_description": "Used for pain relief and inflammation reduction",
        "results_0_efo_id": "EFO_0000675",
        "results_0_max_phase": 4,
        "results_1_drug_name": "Ibuprofen",
        "results_1_chembl_id": "CHEMBL521",
        "results_1_mechanism_of_action": "Nonsteroidal anti-inflammatory agent",
        "results_1_indication_description": "Treatment of fever, inflammation, and pain",
        "results_1_efo_id": "EFO_0000675",
        "results_1_max_phase": 4,
        "count": 2,
        "mesh_heading": "Analgesics",
        "success": True,
        "error_message": ""
    }

def chembl_server_example_drug_indication(mesh_heading: str) -> Dict[str, Any]:
    """
    Get drug indication data for the specified MeSH heading.
    
    Args:
        mesh_heading (str): MeSH heading for which to retrieve drug indication data
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of drug indication records with drug details
        - count (int): Total number of records returned
        - mesh_heading (str): The MeSH heading used in the query
        - success (bool): Whether the operation was successful
        - error_message (str): Error message if operation failed, empty otherwise
    """
    # Input validation
    if not mesh_heading or not isinstance(mesh_heading, str):
        return {
            "results": [],
            "count": 0,
            "mesh_heading": "",
            "success": False,
            "error_message": "Invalid or missing MeSH heading"
        }
    
    try:
        # Call external API to get data
        api_data = call_external_api("chembl-server-example_drug_indication")
        
        # Construct results list from indexed fields
        results = [
            {
                "drug_name": api_data["results_0_drug_name"],
                "chembl_id": api_data["results_0_chembl_id"],
                "mechanism_of_action": api_data["results_0_mechanism_of_action"],
                "indication_description": api_data["results_0_indication_description"],
                "efo_id": api_data["results_0_efo_id"],
                "max_phase": api_data["results_0_max_phase"]
            },
            {
                "drug_name": api_data["results_1_drug_name"],
                "chembl_id": api_data["results_1_chembl_id"],
                "mechanism_of_action": api_data["results_1_mechanism_of_action"],
                "indication_description": api_data["results_1_indication_description"],
                "efo_id": api_data["results_1_efo_id"],
                "max_phase": api_data["results_1_max_phase"]
            }
        ]
        
        # Construct final response
        response = {
            "results": results,
            "count": api_data["count"],
            "mesh_heading": api_data["mesh_heading"],
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }
        
        return response
        
    except Exception as e:
        return {
            "results": [],
            "count": 0,
            "mesh_heading": mesh_heading,
            "success": False,
            "error_message": f"An unexpected error occurred: {str(e)}"
        }