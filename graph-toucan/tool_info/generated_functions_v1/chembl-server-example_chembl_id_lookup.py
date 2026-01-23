from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external ChEMBL API for chembl_id_lookup.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - results_0 (str): First matched ChEMBL ID
        - results_1 (str): Second matched ChEMBL ID
        - count (int): Total number of results returned
        - query_type (str): The type of entity queried (e.g., 'compound', 'target')
        - query_value (str): The exact query string used
        - metadata_database_version (str): Version of the ChEMBL database
        - metadata_timestamp (str): ISO format timestamp of the query
        - metadata_warnings (str): Any warnings from the search (empty if none)
    """
    return {
        "results_0": "CHEMBL12345",
        "results_1": "CHEMBL67890",
        "count": 2,
        "query_type": "compound",
        "query_value": "aspirin",
        "metadata_database_version": "32",
        "metadata_timestamp": "2023-10-01T12:00:00Z",
        "metadata_warnings": ""
    }

def chembl_server_example_chembl_id_lookup(available_type: str, q: str) -> Dict[str, Any]:
    """
    Look up ChEMBL IDs for the specified type and query.
    
    Args:
        available_type (str): The type of entity to query (e.g., 'compound', 'target').
        q (str): The query string to search for.
        
    Returns:
        Dict containing:
        - results (List[str]): List of ChEMBL IDs that match the query and type
        - count (int): Total number of ChEMBL IDs returned in the results
        - query_type (str): The type of entity that was queried
        - query_value (str): The exact query string used in the lookup
        - metadata (Dict): Additional information about the search
        
    Example:
        >>> chembl_server_example_chembl_id_lookup("compound", "aspirin")
        {
            'results': ['CHEMBL12345', 'CHEMBL67890'],
            'count': 2,
            'query_type': 'compound',
            'query_value': 'aspirin',
            'metadata': {
                'database_version': '32',
                'timestamp': '2023-10-01T12:00:00Z',
                'warnings': ''
            }
        }
    """
    # Input validation
    if not available_type or not isinstance(available_type, str):
        raise ValueError("available_type must be a non-empty string")
    if not q or not isinstance(q, str):
        raise ValueError("q must be a non-empty string")
    
    # Call simulated external API
    api_data = call_external_api("chembl-server-example_chembl_id_lookup")
    
    # Construct results list from indexed fields
    results = []
    if "results_0" in api_data and api_data["results_0"]:
        results.append(api_data["results_0"])
    if "results_1" in api_data and api_data["results_1"]:
        results.append(api_data["results_1"])
    
    # Construct metadata dictionary
    metadata = {
        "database_version": api_data.get("metadata_database_version", ""),
        "timestamp": api_data.get("metadata_timestamp", ""),
        "warnings": api_data.get("metadata_warnings", "")
    }
    
    # Return structured response matching output schema
    return {
        "results": results,
        "count": api_data["count"],
        "query_type": api_data["query_type"],
        "query_value": api_data["query_value"],
        "metadata": metadata
    }