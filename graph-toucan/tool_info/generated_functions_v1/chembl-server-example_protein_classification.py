from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching protein classification data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - results_0_class_name (str): First result's class name
        - results_0_level (str): First result's taxonomic level
        - results_0_description (str): First result's description
        - results_0_target_count (int): Number of associated targets for first result
        - results_1_class_name (str): Second result's class name
        - results_1_level (str): Second result's taxonomic level
        - results_1_description (str): Second result's description
        - results_1_target_count (int): Number of associated targets for second result
        - count (int): Total number of results returned
        - success (bool): Whether the query was successful
        - error_message (str | None): Error message if failed, otherwise None
        - query_class_name (str): The protein class name used in the query
    """
    return {
        "results_0_class_name": "Serine/threonine-protein kinase",
        "results_0_level": "family",
        "results_0_description": "Enzymes that phosphorylate serine or threonine residues using ATP",
        "results_0_target_count": 456,
        "results_1_class_name": "Tyrosine-protein kinase",
        "results_1_level": "family",
        "results_1_description": "Enzymes that phosphorylate tyrosine residues using ATP",
        "results_1_target_count": 321,
        "count": 2,
        "success": True,
        "error_message": None,
        "query_class_name": "kinase"
    }

def chembl_server_example_protein_classification(protein_class_name: str) -> Dict[str, Any]:
    """
    Get protein classification data for the specified class name.
    
    Args:
        protein_class_name (str): Protein class name to query
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of protein classification records with hierarchical taxonomy and metadata
        - count (int): Total number of protein classification entries returned
        - success (bool): Indicates whether the query was executed successfully
        - error_message (str | None): Error details if the request failed, otherwise None
        - query_class_name (str): The protein class name used in the query
    """
    # Input validation
    if not protein_class_name or not isinstance(protein_class_name, str):
        return {
            "results": [],
            "count": 0,
            "success": False,
            "error_message": "Invalid protein class name provided",
            "query_class_name": protein_class_name
        }
    
    try:
        # Call external API to get data (simulated)
        api_data = call_external_api("chembl-server-example_protein_classification")
        
        # Construct results list from flattened API response
        results = [
            {
                "class_name": api_data["results_0_class_name"],
                "level": api_data["results_0_level"],
                "description": api_data["results_0_description"],
                "target_count": api_data["results_0_target_count"]
            },
            {
                "class_name": api_data["results_1_class_name"],
                "level": api_data["results_1_level"],
                "description": api_data["results_1_description"],
                "target_count": api_data["results_1_target_count"]
            }
        ]
        
        # Return structured response matching output schema
        return {
            "results": results,
            "count": api_data["count"],
            "success": api_data["success"],
            "error_message": api_data["error_message"],
            "query_class_name": protein_class_name
        }
        
    except Exception as e:
        return {
            "results": [],
            "count": 0,
            "success": False,
            "error_message": f"Unexpected error occurred: {str(e)}",
            "query_class_name": protein_class_name
        }