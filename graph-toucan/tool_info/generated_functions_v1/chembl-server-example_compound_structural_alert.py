from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching compound structural alert data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - results_0_alert_type (str): Type of the first structural alert
        - results_0_matched_substructure (str): Matched substructure for the first alert
        - results_0_severity_level (str): Severity level of the first alert
        - results_0_compound_id (str): Associated compound ID for the first alert
        - results_0_properties_logp (float): LogP property value for the first compound
        - results_1_alert_type (str): Type of the second structural alert
        - results_1_matched_substructure (str): Matched substructure for the second alert
        - results_1_severity_level (str): Severity level of the second alert
        - results_1_compound_id (str): Associated compound ID for the second alert
        - results_1_properties_logp (float): LogP property value for the second compound
        - count (int): Total number of structural alerts returned
        - alert_name_used (str): The name of the structural alert that was queried
        - metadata_source_database (str): Source database name (e.g., ChEMBL)
        - metadata_timestamp (str): ISO format timestamp of the response
        - metadata_version (str): Version of the alert system
    """
    return {
        "results_0_alert_type": "PAINS",
        "results_0_matched_substructure": "benzofuran",
        "results_0_severity_level": "high",
        "results_0_compound_id": "CHEMBL12345",
        "results_0_properties_logp": 3.45,
        "results_1_alert_type": "Medicinal Chemistry",
        "results_1_matched_substructure": "nitroaromatic",
        "results_1_severity_level": "medium",
        "results_1_compound_id": "CHEMBL67890",
        "results_1_properties_logp": 2.87,
        "count": 2,
        "alert_name_used": "reactive_groups",
        "metadata_source_database": "ChEMBL",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_version": "2.1.0",
    }


def chembl_server_example_compound_structural_alert(alert_name: str) -> Dict[str, Any]:
    """
    Get compound structural alerts for the specified name.

    Args:
        alert_name (str): The name of the structural alert to query.

    Returns:
        Dict containing:
        - results (List[Dict]): List of compound structural alert entries with details
          such as alert type, matched substructure, severity level, and associated compounds or properties
        - count (int): Total number of structural alerts returned
        - alert_name_used (str): The name of the structural alert that was queried
        - metadata (Dict): Additional contextual information including source database,
          timestamp of response, and version of the alert system

    Raises:
        ValueError: If alert_name is empty or not a string
    """
    if not alert_name or not isinstance(alert_name, str):
        raise ValueError("alert_name must be a non-empty string")

    # Fetch simulated external data
    api_data = call_external_api("chembl-server-example_compound_structural_alert")

    # Construct results list from indexed fields
    results = [
        {
            "alert_type": api_data["results_0_alert_type"],
            "matched_substructure": api_data["results_0_matched_substructure"],
            "severity_level": api_data["results_0_severity_level"],
            "compound_id": api_data["results_0_compound_id"],
            "properties": {
                "logp": api_data["results_0_properties_logp"]
            }
        },
        {
            "alert_type": api_data["results_1_alert_type"],
            "matched_substructure": api_data["results_1_matched_substructure"],
            "severity_level": api_data["results_1_severity_level"],
            "compound_id": api_data["results_1_compound_id"],
            "properties": {
                "logp": api_data["results_1_properties_logp"]
            }
        }
    ]

    # Construct metadata
    metadata = {
        "source_database": api_data["metadata_source_database"],
        "timestamp": api_data["metadata_timestamp"],
        "version": api_data["metadata_version"]
    }

    # Return final structured response
    return {
        "results": results,
        "count": api_data["count"],
        "alert_name_used": alert_name,  # Use input parameter value
        "metadata": metadata
    }