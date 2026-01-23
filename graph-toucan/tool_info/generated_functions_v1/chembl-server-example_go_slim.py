from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching GO Slim data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_go_id (str): GO identifier for first result
        - result_0_term_name (str): Term name for first result
        - result_0_category (str): Category for first result
        - result_0_definition (str): Definition for first result
        - result_1_go_id (str): GO identifier for second result
        - result_1_term_name (str): Term name for second result
        - result_1_category (str): Category for second result
        - result_1_definition (str): Definition for second result
        - count (int): Total number of results
        - category_summary_biological_process (int): Count of biological_process terms
        - category_summary_molecular_function (int): Count of molecular_function terms
        - category_summary_cellular_component (int): Count of cellular_component terms
        - has_results (bool): Whether any results were found
        - metadata_source (str): Source database name
        - metadata_version (str): Database release version
        - metadata_timestamp (str): ISO format timestamp of data retrieval
    """
    return {
        "result_0_go_id": "GO:0008150",
        "result_0_term_name": "biological_process",
        "result_0_category": "biological_process",
        "result_0_definition": "A biological process represents a specific objective that the organism is genetically programmed to achieve.",
        "result_1_go_id": "GO:0003674",
        "result_1_term_name": "molecular_function",
        "result_1_category": "molecular_function",
        "result_1_definition": "The action of a gene product at the molecular level.",
        "count": 2,
        "category_summary_biological_process": 1,
        "category_summary_molecular_function": 1,
        "category_summary_cellular_component": 0,
        "has_results": True,
        "metadata_source": "ChEMBL",
        "metadata_version": "32",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z"
    }


def chembl_server_example_go_slim(go_slim_term: str) -> Dict[str, Any]:
    """
    Get data for the specified GO Slim term.

    Args:
        go_slim_term (str): GO Slim term to query

    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with keys 'go_id', 'term_name', 'category', 'definition'
        - count (int): Total number of GO Slim terms returned
        - category_summary (Dict): Summary counts by high-level GO categories
        - has_results (bool): Whether any data was found
        - metadata (Dict): Source, version, and timestamp information

    Raises:
        ValueError: If go_slim_term is empty or not a string
    """
    if not go_slim_term:
        raise ValueError("go_slim_term is required")
    if not isinstance(go_slim_term, str):
        raise ValueError("go_slim_term must be a string")

    # Call external API to get flattened data
    api_data = call_external_api("chembl-server-example_go_slim")

    # Construct results list from indexed fields
    results = [
        {
            "go_id": api_data["result_0_go_id"],
            "term_name": api_data["result_0_term_name"],
            "category": api_data["result_0_category"],
            "definition": api_data["result_0_definition"]
        },
        {
            "go_id": api_data["result_1_go_id"],
            "term_name": api_data["result_1_term_name"],
            "category": api_data["result_1_category"],
            "definition": api_data["result_1_definition"]
        }
    ]

    # Construct category summary
    category_summary = {
        "biological_process": api_data["category_summary_biological_process"],
        "molecular_function": api_data["category_summary_molecular_function"],
        "cellular_component": api_data["category_summary_cellular_component"]
    }

    # Construct metadata
    metadata = {
        "source": api_data["metadata_source"],
        "version": api_data["metadata_version"],
        "timestamp": api_data["metadata_timestamp"]
    }

    # Build final result
    return {
        "results": results,
        "count": api_data["count"],
        "category_summary": category_summary,
        "has_results": api_data["has_results"],
        "metadata": metadata
    }