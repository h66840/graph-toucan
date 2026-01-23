from typing import Dict, List, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching target relation data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_target_1 (str): First target in the relationship
        - result_0_target_2 (str): Second target in the relationship
        - result_0_relationship_type (str): Type of relationship for first result
        - result_0_relation_description (str): Description of first relationship
        - result_0_source_database (str): Source database for first relationship
        - result_1_target_1 (str): Second target in the relationship
        - result_1_target_2 (str): Second target in the relationship
        - result_1_relationship_type (str): Type of relationship for second result
        - result_1_relation_description (str): Description of second relationship
        - result_1_source_database (str): Source database for second relationship
        - count (int): Total number of relationships returned
        - metadata_relationship_type_used (str): The relationship type used in query
        - metadata_timestamp (str): ISO format timestamp of query execution
        - metadata_api_version (str): Version of the API used
        - metadata_source_attribution (str): Attribution info for data source
        - metadata_database_release (str): Database release version
    """
    return {
        "result_0_target_1": "CHEMBL1234",
        "result_0_target_2": "CHEMBL5678",
        "result_0_relationship_type": "homolog",
        "result_0_relation_description": "Homologous target in different species",
        "result_0_source_database": "ChEMBL",
        "result_1_target_1": "CHEMBL2468",
        "result_1_target_2": "CHEMBL1357",
        "result_1_relationship_type": "homolog",
        "result_1_relation_description": "Evolutionary related target",
        "result_1_source_database": "ChEMBL",
        "count": 2,
        "metadata_relationship_type_used": "homolog",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_api_version": "2.1.0",
        "metadata_source_attribution": "EMBL-EBI ChEMBL database",
        "metadata_database_release": "32"
    }

def chembl_server_example_target_relation(relationship_type: str) -> Dict[str, Any]:
    """
    Get target relationship data for the specified relationship type.
    
    Args:
        relationship_type (str): The type of relationship to query (e.g., 'homolog', 'pathway')
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with target relationship data
        - count (int): Total number of relationships returned
        - metadata (Dict): Information about the query execution including relationship type used,
          timestamp, API version, source attribution, and database release info
    
    Raises:
        ValueError: If relationship_type is empty or not a string
    """
    if not relationship_type:
        raise ValueError("relationship_type is required")
    if not isinstance(relationship_type, str):
        raise ValueError("relationship_type must be a string")
    
    # Call external API to get flattened data
    api_data = call_external_api("chembl-server-example_target_relation")
    
    # Construct results list from indexed fields
    results = [
        {
            "target_1": api_data["result_0_target_1"],
            "target_2": api_data["result_0_target_2"],
            "relationship_type": api_data["result_0_relationship_type"],
            "relation_description": api_data["result_0_relation_description"],
            "source_database": api_data["result_0_source_database"]
        },
        {
            "target_1": api_data["result_1_target_1"],
            "target_2": api_data["result_1_target_2"],
            "relationship_type": api_data["result_1_relationship_type"],
            "relation_description": api_data["result_1_relation_description"],
            "source_database": api_data["result_1_source_database"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "relationship_type_used": api_data["metadata_relationship_type_used"],
        "timestamp": api_data["metadata_timestamp"],
        "api_version": api_data["metadata_api_version"],
        "source_attribution": api_data["metadata_source_attribution"],
        "database_release": api_data["metadata_database_release"]
    }
    
    # Return final structured response
    return {
        "results": results,
        "count": api_data["count"],
        "metadata": metadata
    }