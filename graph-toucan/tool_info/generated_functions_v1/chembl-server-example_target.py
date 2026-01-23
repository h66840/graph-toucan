from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching target data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - results_0_target_chembl_id (str): ChEMBL ID of the first target
        - results_0_target_type (str): Type of the first target
        - results_0_target_name (str): Name of the first target
        - results_0_organism (str): Organism of the first target
        - results_0_bioactivity_count (int): Number of bioactivities for the first target
        - results_1_target_chembl_id (str): ChEMBL ID of the second target
        - results_1_target_type (str): Type of the second target
        - results_1_target_name (str): Name of the second target
        - results_1_organism (str): Organism of the second target
        - results_1_bioactivity_count (int): Number of bioactivities for the second target
        - count (int): Total number of targets returned
        - target_type (str): The queried target type
        - metadata_database_version (str): Version of the ChEMBL database
        - metadata_request_time (str): ISO format timestamp of the request
        - metadata_warnings (str): Any warnings from the query execution
    """
    return {
        "results_0_target_chembl_id": "CHEMBL236",
        "results_0_target_type": "kinase",
        "results_0_target_name": "Proto-oncogene tyrosine-protein kinase Src",
        "results_0_organism": "Homo sapiens",
        "results_0_bioactivity_count": 1542,
        "results_1_target_chembl_id": "CHEMBL3037",
        "results_1_target_type": "kinase",
        "results_1_target_name": "Epidermal growth factor receptor",
        "results_1_organism": "Homo sapiens",
        "results_1_bioactivity_count": 2103,
        "count": 2,
        "target_type": "kinase",
        "metadata_database_version": "32",
        "metadata_request_time": "2023-10-15T10:30:00Z",
        "metadata_warnings": "Limited to 2 results for demonstration"
    }

def chembl_server_example_target(target_type: str) -> Dict[str, Any]:
    """
    Get target data for the specified type.
    
    Args:
        target_type (str): Target type (e.g., 'kinase', 'gpcr', 'ion channel')
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with detailed target information
        - count (int): Total number of targets returned
        - target_type (str): The type of target that was queried
        - metadata (Dict): Additional information about the query execution
        
    Raises:
        ValueError: If target_type is empty or not a string
    """
    if not target_type or not isinstance(target_type, str):
        raise ValueError("target_type must be a non-empty string")
    
    # Call external API to get data
    api_data = call_external_api("chembl-server-example_target")
    
    # Construct results list from indexed fields
    results = [
        {
            "target_chembl_id": api_data["results_0_target_chembl_id"],
            "target_type": api_data["results_0_target_type"],
            "target_name": api_data["results_0_target_name"],
            "organism": api_data["results_0_organism"],
            "bioactivity_count": api_data["results_0_bioactivity_count"]
        },
        {
            "target_chembl_id": api_data["results_1_target_chembl_id"],
            "target_type": api_data["results_1_target_type"],
            "target_name": api_data["results_1_target_name"],
            "organism": api_data["results_1_organism"],
            "bioactivity_count": api_data["results_1_bioactivity_count"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "database_version": api_data["metadata_database_version"],
        "request_time": api_data["metadata_request_time"],
        "warnings": api_data["metadata_warnings"]
    }
    
    # Return final structured response
    return {
        "results": results,
        "count": api_data["count"],
        "target_type": api_data["target_type"],
        "metadata": metadata
    }