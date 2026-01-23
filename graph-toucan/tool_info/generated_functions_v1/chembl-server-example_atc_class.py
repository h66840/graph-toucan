from typing import Dict, List, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching ATC classification data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_level1_code (str): Level1 code of first result
        - result_0_level2_code (str): Level2 code of first result
        - result_0_level2_description (str): Level2 description of first result
        - result_0_level3_code (str): Level3 code of first result
        - result_0_level3_description (str): Level3 description of first result
        - result_0_level4_code (str): Level4 code of first result
        - result_0_level4_description (str): Level4 description of first result
        - result_0_level5_code (str): Level5 code of first result
        - result_0_level5_description (str): Level5 description of first result
        - result_1_level1_code (str): Level1 code of second result
        - result_1_level2_code (str): Level2 code of second result
        - result_1_level2_description (str): Level2 description of second result
        - result_1_level3_code (str): Level3 code of second result
        - result_1_level3_description (str): Level3 description of second result
        - result_1_level4_code (str): Level4 code of second result
        - result_1_level4_description (str): Level4 description of second result
        - result_1_level5_code (str): Level5 code of second result
        - result_1_level5_description (str): Level5 description of second result
        - count (int): Total number of results returned
        - level1_filter (str): The level1 code used for filtering
        - metadata_timestamp (str): ISO format timestamp of request
        - metadata_version (str): Version of ChEMBL database
        - metadata_disclaimer (str): Disclaimer text about data source
    """
    return {
        "result_0_level1_code": "A",
        "result_0_level2_code": "A01",
        "result_0_level2_description": "Stomatological preparations",
        "result_0_level3_code": "A01A",
        "result_0_level3_description": "Stomatological preparations",
        "result_0_level4_code": "A01AA",
        "result_0_level4_description": "Caries prophylactic agents",
        "result_0_level5_code": "A01AA01",
        "result_0_level5_description": "Sodium fluoride",
        "result_1_level1_code": "A",
        "result_1_level2_code": "A02",
        "result_1_level2_description": "Drugs for acid related disorders",
        "result_1_level3_code": "A02B",
        "result_1_level3_description": "Drugs for peptic ulcer and gastro-esophageal reflux disease (GERD)",
        "result_1_level4_code": "A02BC",
        "result_1_level4_description": "Proton pump inhibitors",
        "result_1_level5_code": "A02BC01",
        "result_1_level5_description": "Omeprazole",
        "count": 2,
        "level1_filter": "A",
        "metadata_timestamp": datetime.now().isoformat(),
        "metadata_version": "32",
        "metadata_disclaimer": "Data sourced from ChEMBL database. For research purposes only."
    }

def chembl_server_example_atc_class(level1: str) -> Dict[str, Any]:
    """
    Get ATC classification data for the specified level1.
    
    Args:
        level1 (str): Level1 value of ATC classification (e.g., 'A' for Alimentary tract and metabolism)
        
    Returns:
        Dict containing:
        - results (List[Dict]): A list of dictionaries containing ATC classification entries at the specified level1.
          Each dictionary includes fields such as 'level1_code', 'level2_code', 'level2_description',
          'level3_code', 'level3_description', 'level4_code', 'level4_description',
          'level5_code', and 'level5_description' where applicable.
        - count (int): The total number of ATC classification records returned in the results list.
        - level1_filter (str): The level1 code that was used to filter the ATC classifications.
        - metadata (Dict): Additional information about the response, including 'timestamp' of the request,
          'version' of the ChEMBL database or API, and any relevant disclaimers or source references.
          
    Raises:
        ValueError: If level1 is not provided or invalid
    """
    if not level1 or not isinstance(level1, str) or len(level1.strip()) == 0:
        raise ValueError("level1 parameter is required and must be a non-empty string")
    
    level1 = level1.strip()
    
    # Call external API to get flattened data
    api_data = call_external_api("chembl-server-example_atc_class")
    
    # Construct results list from indexed fields
    results = []
    
    for i in range(2):  # We have 2 results (0 and 1)
        result_key = f"result_{i}_level1_code"
        if result_key not in api_data:
            continue
            
        result = {
            "level1_code": api_data.get(f"result_{i}_level1_code"),
            "level2_code": api_data.get(f"result_{i}_level2_code"),
            "level2_description": api_data.get(f"result_{i}_level2_description"),
            "level3_code": api_data.get(f"result_{i}_level3_code"),
            "level3_description": api_data.get(f"result_{i}_level3_description"),
            "level4_code": api_data.get(f"result_{i}_level4_code"),
            "level4_description": api_data.get(f"result_{i}_level4_description"),
            "level5_code": api_data.get(f"result_{i}_level5_code"),
            "level5_description": api_data.get(f"result_{i}_level5_description")
        }
        results.append(result)
    
    # Construct metadata
    metadata = {
        "timestamp": api_data.get("metadata_timestamp"),
        "version": api_data.get("metadata_version"),
        "disclaimer": api_data.get("metadata_disclaimer")
    }
    
    # Return final structured response
    return {
        "results": results,
        "count": api_data.get("count", 0),
        "level1_filter": api_data.get("level1_filter", level1),
        "metadata": metadata
    }