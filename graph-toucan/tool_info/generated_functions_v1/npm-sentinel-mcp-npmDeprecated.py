from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for npm package deprecation check.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_package (str): Full package name with version (e.g., "express@5.1.0")
        - result_0_status (str): Status of the check ("success")
        - result_0_error (str or None): Error message if failed, otherwise None
        - result_0_message (str): Human-readable summary of deprecation check
        - result_0_data_isPackageDeprecated (bool): Whether the package is deprecated
        - result_0_data_packageDeprecationMessage (str or None): Deprecation reason if applicable
        - result_0_data_dependencySummary_totalDependencies (int): Total number of dependencies processed
        - result_0_data_dependencySummary_unverifiableDependencies (int): Number of unverifiable dependencies
        - result_0_data_dependencySummary_message (str): Summary message about dependency processing
        - result_0_data_dependencies_direct_0_name (str): Name of first direct dependency
        - result_0_data_dependencies_direct_0_version (str): Version of first direct dependency
        - result_0_data_dependencies_direct_0_isDeprecated (bool): Whether direct dependency is deprecated
        - result_0_data_dependencies_development_0_name (str): Name of first development dependency
        - result_0_data_dependencies_development_0_version (str): Version of first development dependency
        - result_0_data_dependencies_development_0_isDeprecated (bool): Whether dev dependency is deprecated
        - result_0_data_dependencies_peer_0_name (str): Name of first peer dependency
        - result_0_data_dependencies_peer_0_version (str): Version of first peer dependency
        - result_0_data_dependencies_peer_0_isDeprecated (bool): Whether peer dependency is deprecated
    """
    return {
        "result_0_package": "express@5.1.0",
        "result_0_status": "success",
        "result_0_error": None,
        "result_0_message": "Package is not deprecated.",
        "result_0_data_isPackageDeprecated": False,
        "result_0_data_packageDeprecationMessage": None,
        "result_0_data_dependencySummary_totalDependencies": 3,
        "result_0_data_dependencySummary_unverifiableDependencies": 0,
        "result_0_data_dependencySummary_message": "All dependencies verified successfully.",
        "result_0_data_dependencies_direct_0_name": "lodash",
        "result_0_data_dependencies_direct_0_version": "4.17.21",
        "result_0_data_dependencies_direct_0_isDeprecated": False,
        "result_0_data_dependencies_development_0_name": "jest",
        "result_0_data_dependencies_development_0_version": "29.5.0",
        "result_0_data_dependencies_development_0_isDeprecated": False,
        "result_0_data_dependencies_peer_0_name": "react",
        "result_0_data_dependencies_peer_0_version": "18.2.0",
        "result_0_data_dependencies_peer_0_isDeprecated": False,
    }

def npm_sentinel_mcp_npmDeprecated(packages: List[str]) -> Dict[str, Any]:
    """
    Check if the provided npm packages are deprecated.
    
    This function simulates checking deprecation status of npm packages by querying
    an external service and returns detailed information about each package,
    including its deprecation status and the deprecation status of its dependencies.
    
    Args:
        packages (List[str]): List of package names (with optional versions) to check.
        
    Returns:
        Dict[str, Any]: Dictionary containing a list of results. Each result contains:
            - package (str): Full package name with version
            - status (str): Status of the check ("success" or error status)
            - error (str or None): Error message if check failed, otherwise None
            - message (str): Human-readable summary of the result
            - data (Dict): Detailed deprecation and dependency information including:
                - isPackageDeprecated (bool)
                - packageDeprecationMessage (str or None)
                - dependencies (Dict with direct, development, peer lists)
                - dependencySummary (Dict with totals and message)
                
    Raises:
        ValueError: If packages list is empty
    """
    if not packages:
        raise ValueError("At least one package must be specified")

    try:
        # Call external API to get deprecation data (returns flat structure)
        api_data = call_external_api("npm-sentinel-mcp-npmDeprecated")
        
        results: List[Dict[str, Any]] = []
        
        # Process only the first result since we're generating one item per call
        package_name = packages[0] if "@" in packages[0] else f"{packages[0]}@latest"
        
        # Reconstruct nested structure from flat API data
        result_entry: Dict[str, Any] = {
            "package": api_data["result_0_package"],
            "status": api_data["result_0_status"],
            "error": api_data["result_0_error"],
            "message": api_data["result_0_message"],
            "data": {
                "isPackageDeprecated": api_data["result_0_data_isPackageDeprecated"],
                "packageDeprecationMessage": api_data["result_0_data_packageDeprecationMessage"],
                "dependencies": {
                    "direct": [
                        {
                            "name": api_data["result_0_data_dependencies_direct_0_name"],
                            "version": api_data["result_0_data_dependencies_direct_0_version"],
                            "isDeprecated": api_data["result_0_data_dependencies_direct_0_isDeprecated"]
                        }
                    ],
                    "development": [
                        {
                            "name": api_data["result_0_data_dependencies_development_0_name"],
                            "version": api_data["result_0_data_dependencies_development_0_version"],
                            "isDeprecated": api_data["result_0_data_dependencies_development_0_isDeprecated"]
                        }
                    ],
                    "peer": [
                        {
                            "name": api_data["result_0_data_dependencies_peer_0_name"],
                            "version": api_data["result_0_data_dependencies_peer_0_version"],
                            "isDeprecated": api_data["result_0_data_dependencies_peer_0_isDeprecated"]
                        }
                    ]
                },
                "dependencySummary": {
                    "totalDependencies": api_data["result_0_data_dependencySummary_totalDependencies"],
                    "unverifiableDependencies": api_data["result_0_data_dependencySummary_unverifiableDependencies"],
                    "message": api_data["result_0_data_dependencySummary_message"]
                }
            }
        }
        
        results.append(result_entry)
        
        return {"results": results}
        
    except Exception as e:
        # Fallback error response if anything goes wrong
        return {
            "results": [
                {
                    "package": packages[0],
                    "status": "error",
                    "error": str(e),
                    "message": f"Failed to check deprecation status for {packages[0]}",
                    "data": {
                        "isPackageDeprecated": False,
                        "packageDeprecationMessage": None,
                        "dependencies": {
                            "direct": [],
                            "development": [],
                            "peer": []
                        },
                        "dependencySummary": {
                            "totalDependencies": 0,
                            "unverifiableDependencies": 0,
                            "message": "No dependency information available due to error"
                        }
                    }
                }
            ]
        }