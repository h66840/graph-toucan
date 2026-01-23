from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for npm package maintenance analysis.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - queryPackages_0 (str): First package name in query
        - queryPackages_1 (str): Second package name in query
        - result_0_packageInput (str): Original input string for first package
        - result_0_packageName (str): Resolved name of first package
        - result_0_status (str): Status of analysis for first package
        - result_0_error (str or null): Error message if failed, else null
        - result_0_message (str): Human-readable message for first package
        - result_0_data_analyzedAt (str): ISO 8601 timestamp when first package was analyzed
        - result_0_data_versionInScore (str): Version used for scoring first package
        - result_0_data_maintenanceScore (float): Maintenance score for first package
        - result_1_packageInput (str): Original input string for second package
        - result_1_packageName (str): Resolved name of second package
        - result_1_status (str): Status of analysis for second package
        - result_1_error (str or null): Error message if failed, else null
        - result_1_message (str): Human-readable message for second package
        - result_1_data_analyzedAt (str): ISO 8601 timestamp when second package was analyzed
        - result_1_data_versionInScore (str): Version used for scoring second package
        - result_1_data_maintenanceScore (float): Maintenance score for second package
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    return {
        "queryPackages_0": "express",
        "queryPackages_1": "lodash",

        "result_0_packageInput": "express",
        "result_0_packageName": "express",
        "result_0_status": "success",
        "result_0_error": None,
        "result_0_message": "Successfully analyzed maintenance metrics for express",
        "result_0_data_analyzedAt": now_iso,
        "result_0_data_versionInScore": "4.18.2",
        "result_0_data_maintenanceScore": round(random.uniform(0.6, 0.95), 3),

        "result_1_packageInput": "lodash",
        "result_1_packageName": "lodash",
        "result_1_status": "success",
        "result_1_error": None,
        "result_1_message": "Successfully analyzed maintenance metrics for lodash",
        "result_1_data_analyzedAt": now_iso,
        "result_1_data_versionInScore": "4.17.21",
        "result_1_data_maintenanceScore": round(random.uniform(0.6, 0.95), 3),
    }


def npm_sentinel_mcp_npmMaintenance(packages: List[str]) -> Dict[str, Any]:
    """
    Analyze package maintenance metrics for the given list of npm package names.

    Args:
        packages (List[str]): List of package names to analyze.

    Returns:
        Dict containing:
        - queryPackages (List[str]): list of package names that were included in the query
        - results (List[Dict]): list of result objects for each queried package with detailed metrics
          Each result contains:
          - packageInput (str): original input string for the package
          - packageName (str): resolved name of the package as analyzed
          - status (str): status of the analysis process
          - error (str or null): error message if analysis failed, otherwise null
          - message (str): human-readable message summarizing the result
          - data (Dict): detailed maintenance metrics including:
            - analyzedAt (str): ISO 8601 timestamp when analyzed
            - versionInScore (str): version used for scoring
            - maintenanceScore (float): numerical score (0–1) representing maintenance health
    """
    if not packages:
        raise ValueError("Parameter 'packages' is required and must be a non-empty list.")

    # Call external API to get simulated data
    api_data = call_external_api("npm-sentinel-mcp-npmMaintenance")

    # Extract query packages (up to 2 for simulation)
    query_packages = []
    for i in range(2):
        key = f"queryPackages_{i}"
        if key in api_data and api_data[key] is not None:
            query_packages.append(api_data[key])
        else:
            break

    # Construct results list from indexed result data
    results: List[Dict[str, Any]] = []
    for i in range(2):
        package_input_key = f"result_{i}_packageInput"
        if package_input_key not in api_data:
            break

        result: Dict[str, Any] = {
            "packageInput": api_data[f"result_{i}_packageInput"],
            "packageName": api_data[f"result_{i}_packageName"],
            "status": api_data[f"result_{i}_status"],
            "error": api_data[f"result_{i}_error"],
            "message": api_data[f"result_{i}_message"],
            "data": {
                "analyzedAt": api_data[f"result_{i}_data_analyzedAt"],
                "versionInScore": api_data[f"result_{i}_data_versionInScore"],
                "maintenanceScore": api_data[f"result_{i}_data_maintenanceScore"],
            },
        }
        results.append(result)

    return {
        "queryPackages": query_packages,
        "results": results,
    }