from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching mineral data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success_v (int): API version used for the response
        - success_license (str): license of the data (e.g., CC-BY 4.0)
        - success_data_0_mineral_id (int): unique identifier for the first mineral
        - success_data_0_mineral (str): name of the first mineral
        - success_data_0_mineral_type (str): classification or group type of the first mineral
        - success_data_0_formula (str): chemical formula of the first mineral in plain text
        - success_data_0_formula_tags (str): chemical formula with HTML sub/sup tags
        - success_data_0_url (str): URL to the mineral's page on mindat.org
        - success_data_0_hardness_min (float): minimum Mohs hardness value of the first mineral
        - success_data_0_hardness_max (float): maximum Mohs hardness value of the first mineral
        - success_data_0_crystal_form (str): crystal system or form of the first mineral
        - success_data_0_mineral_color (str): typical color(s) of the first mineral
        - success_data_0_lustre (str): appearance of the mineral's surface
        - success_data_1_mineral_id (int): unique identifier for the second mineral
        - success_data_1_mineral (str): name of the second mineral
        - success_data_1_mineral_type (str): classification or group type of the second mineral
        - success_data_1_formula (str): chemical formula of the second mineral in plain text
        - success_data_1_formula_tags (str): chemical formula with HTML sub/sup tags
        - success_data_1_url (str): URL to the mineral's page on mindat.org
        - success_data_1_hardness_min (float): minimum Mohs hardness value of the second mineral
        - success_data_1_hardness_max (float): maximum Mohs hardness value of the second mineral
        - success_data_1_crystal_form (str): crystal system or form of the second mineral
        - success_data_1_mineral_color (str): typical color(s) of the second mineral
        - success_data_1_lustre (str): appearance of the mineral's surface
    """
    return {
        "success_v": 2,
        "success_license": "CC-BY 4.0",
        "success_data_0_mineral_id": 101,
        "success_data_0_mineral": "Quartz",
        "success_data_0_mineral_type": "Silicate",
        "success_data_0_formula": "SiO2",
        "success_data_0_formula_tags": "SiO<sub>2</sub>",
        "success_data_0_url": "https://www.mindat.org/min-3337.html",
        "success_data_0_hardness_min": 7.0,
        "success_data_0_hardness_max": 7.0,
        "success_data_0_crystal_form": "Trigonal",
        "success_data_0_mineral_color": "Colorless, white, purple, pink, yellow, brown, black",
        "success_data_0_lustre": "Vitreous",
        "success_data_1_mineral_id": 205,
        "success_data_1_mineral": "Galena",
        "success_data_1_mineral_type": "Sulfide",
        "success_data_1_formula": "PbS",
        "success_data_1_formula_tags": "PbS",
        "success_data_1_url": "https://www.mindat.org/min-1652.html",
        "success_data_1_hardness_min": 2.5,
        "success_data_1_hardness_max": 2.5,
        "success_data_1_crystal_form": "Isometric",
        "success_data_1_mineral_color": "Lead gray",
        "success_data_1_lustre": "Metallic"
    }

def macrostrat_api_server_mineral_info(
    element: Optional[str] = None,
    mineral: Optional[str] = None,
    mineral_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get information about a mineral using one property (element, mineral name, or mineral type).
    
    This function simulates querying a mineral database API and returns structured mineral data.
    Only one input parameter should be provided at a time.
    
    Args:
        element (Optional[str]): An element that the mineral is made of (e.g., "Si", "Fe")
        mineral (Optional[str]): The name of the mineral (e.g., "Quartz", "Galena")
        mineral_type (Optional[str]): The type of mineral (e.g., "Silicate", "Sulfide")
    
    Returns:
        Dict containing:
        - success (Dict): contains version, license, and data fields with mineral information
          - v (int): API version used for the response
          - license (str): license of the data
          - data (List[Dict]): list of mineral records with detailed properties
    
    Raises:
        ValueError: If more than one parameter is provided or all are None
    """
    # Input validation
    provided_params = [p for p in [element, mineral, mineral_type] if p is not None]
    if len(provided_params) == 0:
        raise ValueError("At least one parameter (element, mineral, or mineral_type) must be provided")
    if len(provided_params) > 1:
        raise ValueError("Only one parameter (element, mineral, or mineral_type) should be provided")
    
    # Fetch simulated API data
    api_data = call_external_api("macrostrat-api-server-mineral-info")
    
    # Construct the nested result structure
    result = {
        "success": {
            "v": api_data["success_v"],
            "license": api_data["success_license"],
            "data": [
                {
                    "mineral_id": api_data["success_data_0_mineral_id"],
                    "mineral": api_data["success_data_0_mineral"],
                    "mineral_type": api_data["success_data_0_mineral_type"],
                    "formula": api_data["success_data_0_formula"],
                    "formula_tags": api_data["success_data_0_formula_tags"],
                    "url": api_data["success_data_0_url"],
                    "hardness_min": api_data["success_data_0_hardness_min"],
                    "hardness_max": api_data["success_data_0_hardness_max"],
                    "crystal_form": api_data["success_data_0_crystal_form"],
                    "mineral_color": api_data["success_data_0_mineral_color"],
                    "lustre": api_data["success_data_0_lustre"]
                },
                {
                    "mineral_id": api_data["success_data_1_mineral_id"],
                    "mineral": api_data["success_data_1_mineral"],
                    "mineral_type": api_data["success_data_1_mineral_type"],
                    "formula": api_data["success_data_1_formula"],
                    "formula_tags": api_data["success_data_1_formula_tags"],
                    "url": api_data["success_data_1_url"],
                    "hardness_min": api_data["success_data_1_hardness_min"],
                    "hardness_max": api_data["success_data_1_hardness_max"],
                    "crystal_form": api_data["success_data_1_crystal_form"],
                    "mineral_color": api_data["success_data_1_mineral_color"],
                    "lustre": api_data["success_data_1_lustre"]
                }
            ]
        }
    }
    
    return result