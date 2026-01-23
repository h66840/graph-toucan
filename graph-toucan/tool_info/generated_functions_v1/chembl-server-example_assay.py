from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching assay data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_assay_id (str): Unique identifier for the first assay
        - result_0_target_organism (str): Organism of the target for the first assay
        - result_0_target_type (str): Type of target for the first assay
        - result_0_activity_value (float): Measured activity value for the first assay
        - result_0_standard_type (str): Standard measurement type for the first assay
        - result_1_assay_id (str): Unique identifier for the second assay
        - result_1_target_organism (str): Organism of the target for the second assay
        - result_1_target_type (str): Type of target for the second assay
        - result_1_activity_value (float): Measured activity value for the second assay
        - result_1_standard_type (str): Standard measurement type for the second assay
        - count (int): Total number of assays returned
        - available_type_0 (str): First supported assay type
        - available_type_1 (str): Second supported assay type
        - metadata_timestamp (str): ISO format timestamp of query execution
        - metadata_requested_assay_type (str): The assay type requested
        - metadata_warnings (str): Any warnings from the query execution
        - metadata_filters_applied (str): Filters applied during query
    """
    return {
        "result_0_assay_id": "CHEMBL12345",
        "result_0_target_organism": "Homo sapiens",
        "result_0_target_type": "Single protein",
        "result_0_activity_value": 8.5,
        "result_0_standard_type": "IC50",
        "result_1_assay_id": "CHEMBL67890",
        "result_1_target_organism": "Mus musculus",
        "result_1_target_type": "Cell-based",
        "result_1_activity_value": 7.2,
        "result_1_standard_type": "EC50",
        "count": 2,
        "available_type_0": "B",
        "available_type_1": "F",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_requested_assay_type": "B",
        "metadata_warnings": "",
        "metadata_filters_applied": "standard_type in [IC50, EC50]"
    }


def chembl_server_example_assay(assay_type: str) -> Dict[str, Any]:
    """
    Get assay data for the specified type.

    Args:
        assay_type (str): The type of assay to retrieve (e.g., 'B' for biochemical, 'F' for functional).

    Returns:
        Dict containing:
        - results (List[Dict]): List of assay records with details like assay ID, target info, activity data.
        - count (int): Total number of assays returned.
        - available_types (List[str]): List of valid assay types supported.
        - metadata (Dict): Information about the query execution including timestamp, requested type, warnings, and filters.

    Raises:
        ValueError: If assay_type is empty or not a string.
    """
    if not assay_type or not isinstance(assay_type, str):
        raise ValueError("assay_type must be a non-empty string")

    # Fetch simulated external data
    api_data = call_external_api("chembl-server-example_assay")

    # Construct results list from indexed fields
    results = [
        {
            "assay_id": api_data["result_0_assay_id"],
            "target": {
                "organism": api_data["result_0_target_organism"],
                "type": api_data["result_0_target_type"]
            },
            "activity": {
                "value": api_data["result_0_activity_value"],
                "standard_type": api_data["result_0_standard_type"]
            }
        },
        {
            "assay_id": api_data["result_1_assay_id"],
            "target": {
                "organism": api_data["result_1_target_organism"],
                "type": api_data["result_1_target_type"]
            },
            "activity": {
                "value": api_data["result_1_activity_value"],
                "standard_type": api_data["result_1_standard_type"]
            }
        }
    ]

    # Construct metadata
    metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "requested_assay_type": api_data["metadata_requested_assay_type"],
        "warnings": api_data["metadata_warnings"] if api_data["metadata_warnings"] else None,
        "filters_applied": api_data["metadata_filters_applied"]
    }

    # Construct final response
    return {
        "results": results,
        "count": api_data["count"],
        "available_types": [api_data["available_type_0"], api_data["available_type_1"]],
        "metadata": metadata
    }