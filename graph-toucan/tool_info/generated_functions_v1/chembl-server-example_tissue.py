from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching tissue data from external ChEMBL server API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_name (str): Name of the first matching tissue
        - result_0_anatomical_context (str): Anatomical location of the first tissue
        - result_0_expression_level (str): Expression level in the first tissue
        - result_0_target_name (str): Associated target name for the first tissue
        - result_0_species (str): Species of the first tissue
        - result_0_cell_type (str): Cell type of the first tissue
        - result_1_name (str): Name of the second matching tissue
        - result_1_anatomical_context (str): Anatomical location of the second tissue
        - result_1_expression_level (str): Expression level in the second tissue
        - result_1_target_name (str): Associated target name for the second tissue
        - result_1_species (str): Species of the second tissue
        - result_1_cell_type (str): Cell type of the second tissue
        - count (int): Total number of tissue records returned
        - success (bool): Whether the request was successful
        - message (str): Optional message about the result
        - metadata_database_version (str): Version of the ChEMBL database
        - metadata_query_timestamp (str): ISO format timestamp of the query
        - metadata_source (str): Source identifier for the data
    """
    return {
        "result_0_name": "liver",
        "result_0_anatomical_context": "hepatic lobule",
        "result_0_expression_level": "high",
        "result_0_target_name": "CYP3A4",
        "result_0_species": "Homo sapiens",
        "result_0_cell_type": "hepatocyte",
        "result_1_name": "kidney",
        "result_1_anatomical_context": "renal cortex",
        "result_1_expression_level": "moderate",
        "result_1_target_name": "SLC34A1",
        "result_1_species": "Homo sapiens",
        "result_1_cell_type": "proximal tubule cell",
        "count": 2,
        "success": True,
        "message": "Tissue data retrieved successfully.",
        "metadata_database_version": "ChEMBL 32",
        "metadata_query_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_source": "ChEMBL-webres.net",
    }


def chembl_server_example_tissue(tissue_name: str) -> Dict[str, Any]:
    """
    Get tissue data for the specified name.

    Args:
        tissue_name (str): The name of the tissue to search for (e.g., 'liver', 'kidney').

    Returns:
        Dict containing:
        - results (List[Dict]): List of tissue data entries matching the query.
          Each dictionary includes: name, anatomical_context, expression_level,
          target_name, species, and cell_type.
        - count (int): Total number of tissue records returned.
        - success (bool): Whether the request was processed successfully.
        - message (str): Optional descriptive message.
        - metadata (Dict): Additional context such as database version,
          query timestamp, and source identifier.

    Raises:
        ValueError: If tissue_name is empty or not a string.
    """
    if not tissue_name or not isinstance(tissue_name, str):
        return {
            "results": [],
            "count": 0,
            "success": False,
            "message": "Invalid input: tissue_name must be a non-empty string.",
            "metadata": {
                "database_version": "ChEMBL 32",
                "query_timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "ChEMBL-webres.net",
            },
        }

    # Fetch simulated external data
    api_data = call_external_api("chembl-server-example_tissue")

    # Construct results list from indexed flat fields
    results = [
        {
            "name": api_data["result_0_name"],
            "anatomical_context": api_data["result_0_anatomical_context"],
            "expression_level": api_data["result_0_expression_level"],
            "target_name": api_data["result_0_target_name"],
            "species": api_data["result_0_species"],
            "cell_type": api_data["result_0_cell_type"],
        },
        {
            "name": api_data["result_1_name"],
            "anatomical_context": api_data["result_1_anatomical_context"],
            "expression_level": api_data["result_1_expression_level"],
            "target_name": api_data["result_1_target_name"],
            "species": api_data["result_1_species"],
            "cell_type": api_data["result_1_cell_type"],
        },
    ]

    # Construct metadata
    metadata = {
        "database_version": api_data["metadata_database_version"],
        "query_timestamp": api_data["metadata_query_timestamp"],
        "source": api_data["metadata_source"],
    }

    return {
        "results": results,
        "count": api_data["count"],
        "success": api_data["success"],
        "message": api_data["message"],
        "metadata": metadata,
    }