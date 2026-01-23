from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching target component data from external ChEMBL API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_component_id (int): Component ID of the first result
        - result_0_target_type (str): Target type of the first result
        - result_0_organism (str): Organism of the first result
        - result_0_accession (str): Accession number of the first result
        - result_0_description (str): Description of the first result
        - result_0_sequence (str): Protein sequence of the first result
        - result_1_component_id (int): Component ID of the second result
        - result_1_target_type (str): Target type of the second result
        - result_1_organism (str): Organism of the second result
        - result_1_accession (str): Accession number of the second result
        - result_1_description (str): Description of the second result
        - result_1_sequence (str): Protein sequence of the second result
        - count (int): Total number of results returned
        - component_type (str): The component type queried
        - metadata_db_version (str): ChEMBL database version
        - metadata_timestamp (str): ISO format timestamp of response generation
        - metadata_query_params_component_type (str): Echo of input component_type parameter
    """
    return {
        "result_0_component_id": 101,
        "result_0_target_type": "PROTEIN",
        "result_0_organism": "Homo sapiens",
        "result_0_accession": "P12345",
        "result_0_description": "Serine/threonine-protein kinase A-Raf",
        "result_0_sequence": "MVRAASGKGSGGKGSSSSRA...",
        "result_1_component_id": 102,
        "result_1_target_type": "PROTEIN",
        "result_1_organism": "Homo sapiens",
        "result_1_accession": "Q99988",
        "result_1_description": "Cyclin-dependent kinase 2",
        "result_1_sequence": "MAHAKELGSGAFG...",
        "count": 2,
        "component_type": "PROTEIN",
        "metadata_db_version": "32",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_query_params_component_type": "PROTEIN"
    }


def chembl_server_example_target_component(component_type: str) -> Dict[str, Any]:
    """
    Get target component data for the specified type from ChEMBL database.

    Args:
        component_type (str): The type of component to query (e.g., 'PROTEIN', 'DNA', 'RNA')

    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with target component data including
          'component_id', 'target_type', 'organism', 'accession', 'description', and 'sequence'
        - count (int): Total number of target components returned
        - component_type (str): The type of component that was queried
        - metadata (Dict): Additional information including db_version, timestamp, and query_params

    Raises:
        ValueError: If component_type is not provided or not a valid string
    """
    if not component_type or not isinstance(component_type, str):
        raise ValueError("component_type must be a non-empty string")

    # Normalize component type
    valid_types = {"PROTEIN", "DNA", "RNA"}
    normalized_type = component_type.strip().upper()
    if normalized_type not in valid_types:
        raise ValueError(f"component_type must be one of {valid_types}")

    # Fetch data from external API (simulated)
    api_data = call_external_api("chembl-server-example_target_component")

    # Construct results list from indexed fields
    results = [
        {
            "component_id": api_data["result_0_component_id"],
            "target_type": api_data["result_0_target_type"],
            "organism": api_data["result_0_organism"],
            "accession": api_data["result_0_accession"],
            "description": api_data["result_0_description"],
            "sequence": api_data["result_0_sequence"]
        },
        {
            "component_id": api_data["result_1_component_id"],
            "target_type": api_data["result_1_target_type"],
            "organism": api_data["result_1_organism"],
            "accession": api_data["result_1_accession"],
            "description": api_data["result_1_description"],
            "sequence": api_data["result_1_sequence"]
        }
    ]

    # Construct metadata
    metadata = {
        "db_version": api_data["metadata_db_version"],
        "timestamp": api_data["metadata_timestamp"],
        "query_params": {
            "component_type": api_data["metadata_query_params_component_type"]
        }
    }

    # Return final structured response
    return {
        "results": results,
        "count": api_data["count"],
        "component_type": api_data["component_type"],
        "metadata": metadata
    }