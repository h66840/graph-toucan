from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for npm license compatibility check.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - query_package_0 (str): First package name queried
        - query_package_1 (str): Second package name queried
        - result_0_package_input (str): Input package string for first result
        - result_0_package_name (str): Resolved package name for first result
        - result_0_version_queried (str): Version specified in query for first result
        - result_0_version_fetched (str): Actual version fetched for first result
        - result_0_status (str): Status of the check ('success' or 'error')
        - result_0_error (str): Error message if any, otherwise empty string
        - result_0_data_license (str): License type found for first package
        - result_0_data_license_spdx (str): SPDX identifier for first package license
        - result_0_message (str): Additional message for first result
        - result_1_package_input (str): Input package string for second result
        - result_1_package_name (str): Resolved package name for second result
        - result_1_version_queried (str): Version specified in query for second result
        - result_1_version_fetched (str): Actual version fetched for second result
        - result_1_status (str): Status of the check ('success' or 'error')
        - result_1_error (str): Error message if any, otherwise empty string
        - result_1_data_license (str): License type found for second package
        - result_1_data_license_spdx (str): SPDX identifier for second package license
        - result_1_message (str): Additional message for second result
        - analysis_summary (str): High-level summary of compatibility analysis
        - analysis_warning_0 (str): First warning message
        - analysis_warning_1 (str): Second warning message
        - analysis_unique_license_0 (str): First unique license found
        - analysis_unique_license_1 (str): Second unique license found
        - message (str): Overall message or disclaimer about the check
    """
    return {
        "query_package_0": "express",
        "query_package_1": "lodash",
        "result_0_package_input": "express",
        "result_0_package_name": "express",
        "result_0_version_queried": "latest",
        "result_0_version_fetched": "4.18.2",
        "result_0_status": "success",
        "result_0_error": "",
        "result_0_data_license": "MIT",
        "result_0_data_license_spdx": "MIT",
        "result_0_message": "License information retrieved successfully",
        "result_1_package_input": "lodash",
        "result_1_package_name": "lodash",
        "result_1_version_queried": "latest",
        "result_1_version_fetched": "4.17.21",
        "result_1_status": "success",
        "result_1_error": "",
        "result_1_data_license": "MIT",
        "result_1_data_license_spdx": "MIT",
        "result_1_message": "License information retrieved successfully",
        "analysis_summary": "All packages have compatible MIT licenses.",
        "analysis_warning_0": "MIT license requires proper attribution in your project.",
        "analysis_warning_1": "No copyleft licenses detected; standard commercial use permitted.",
        "analysis_unique_license_0": "MIT",
        "analysis_unique_license_1": "MIT",
        "message": "This is a simulated license compatibility check. Always verify licenses for production use. Does not constitute legal advice."
    }

def npm_sentinel_mcp_npmLicenseCompatibility(packages: List[str]) -> Dict[str, Any]:
    """
    Check license compatibility between multiple npm packages.
    
    This function simulates checking the license compatibility of a list of npm packages
    by querying an external service and analyzing the results for potential conflicts.
    
    Args:
        packages (List[str]): List of package names to check for license compatibility
        
    Returns:
        Dict containing:
        - queryPackages (List[str]): list of package names that were queried
        - results (List[Dict]): list of individual package check results with detailed info
        - analysis (Dict): high-level analysis including summary, warnings, and unique licenses
        - message (str): overall message or disclaimer about the check
        
    Raises:
        ValueError: If packages list is empty
    """
    if not packages:
        raise ValueError("packages list cannot be empty")
    
    # Call external API to get license data (simulated)
    api_data = call_external_api("npm-sentinel-mcp-npmLicenseCompatibility")
    
    # Construct queryPackages from input
    query_packages = packages[:2]  # Limit to first two for consistency with API mock
    
    # Construct results list from indexed fields
    results = []
    for i in range(2):
        result_key = f"result_{i}"
        if f"{result_key}_package_input" in api_data:
            result = {
                "packageInput": api_data[f"{result_key}_package_input"],
                "packageName": api_data[f"{result_key}_package_name"],
                "versionQueried": api_data[f"{result_key}_version_queried"],
                "versionFetched": api_data[f"{result_key}_version_fetched"],
                "status": api_data[f"{result_key}_status"],
                "error": api_data[f"{result_key}_error"],
                "data": {
                    "license": api_data[f"{result_key}_data_license"],
                    "license_spdx": api_data[f"{result_key}_data_license_spdx"]
                },
                "message": api_data[f"{result_key}_message"]
            }
            results.append(result)
    
    # Construct analysis object
    analysis = {
        "summary": api_data["analysis_summary"],
        "warnings": [
            api_data["analysis_warning_0"],
            api_data["analysis_warning_1"]
        ],
        "uniqueLicensesFound": [
            api_data["analysis_unique_license_0"],
            api_data["analysis_unique_license_1"]
        ]
    }
    
    # Final result structure
    return {
        "queryPackages": query_packages,
        "results": results,
        "analysis": analysis,
        "message": api_data["message"]
    }