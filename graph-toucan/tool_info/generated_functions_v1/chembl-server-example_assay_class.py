from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching assay classification data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_class_id (str): Class ID of the first assay classification
        - result_0_classification (str): Classification name of the first assay
        - result_0_description (str): Description of the first assay classification
        - result_0_target (str): Target of the first assay classification
        - result_1_class_id (str): Class ID of the second assay classification
        - result_1_classification (str): Classification name of the second assay
        - result_1_description (str): Description of the second assay classification
        - result_1_target (str): Target of the second assay classification
        - total_count (int): Total number of assay classifications returned
        - assay_class_type (str): The type of assay classification requested
        - metadata_source_version (str): Version of the data source
        - metadata_timestamp (str): ISO format timestamp of query execution
        - metadata_warnings (str): Any warnings from the query execution
    """
    return {
        "result_0_class_id": "CLASS001",
        "result_0_classification": "Kinase Assay",
        "result_0_description": "Assay targeting protein kinase enzymes",
        "result_0_target": "Protein Kinase A",
        "result_1_class_id": "CLASS002",
        "result_1_classification": "GPCR Assay",
        "result_1_description": "Assay targeting G-protein coupled receptors",
        "result_1_target": "Adrenergic Receptor",
        "total_count": 2,
        "assay_class_type": "biochemical",
        "metadata_source_version": "ChEMBL v32",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_warnings": "",
    }


def chembl_server_example_assay_class(assay_class_type: str) -> Dict[str, Any]:
    """
    Get assay classification data for the specified type.

    Args:
        assay_class_type (str): Assay classification type (e.g., 'biochemical', 'functional')

    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with keys 'class_id', 'classification', 'description', 'target'
        - total_count (int): Total number of assay classifications returned
        - assay_class_type (str): The type of assay classification requested
        - metadata (Dict): Additional info like source version, timestamp, warnings

    Raises:
        ValueError: If assay_class_type is empty or not a string
    """
    if not assay_class_type or not isinstance(assay_class_type, str):
        raise ValueError("assay_class_type must be a non-empty string")

    # Fetch data from simulated external API
    api_data = call_external_api("chembl-server-example_assay_class")

    # Construct results list from indexed fields
    results = [
        {
            "class_id": api_data["result_0_class_id"],
            "classification": api_data["result_0_classification"],
            "description": api_data["result_0_description"],
            "target": api_data["result_0_target"],
        },
        {
            "class_id": api_data["result_1_class_id"],
            "classification": api_data["result_1_classification"],
            "description": api_data["result_1_description"],
            "target": api_data["result_1_target"],
        },
    ]

    # Construct metadata
    metadata = {
        "source_version": api_data["metadata_source_version"],
        "timestamp": api_data["metadata_timestamp"],
        "warnings": api_data["metadata_warnings"] if api_data["metadata_warnings"] else None,
    }

    # Return final structured response
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "assay_class_type": api_data["assay_class_type"],
        "metadata": metadata,
    }