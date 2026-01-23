from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for NPM package comparison.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - queryPackages_0 (str): First package name queried
        - queryPackages_1 (str): Second package name queried
        - results_0_packageInput (str): Input name of first package
        - results_0_packageName (str): Resolved name of first package
        - results_0_versionQueried (str): Version queried for first package
        - results_0_status (str): Status of first package query
        - results_0_error (str): Error message for first package (if any)
        - results_0_message (str): Message for first package
        - results_0_data_name (str): Name in data for first package
        - results_0_data_version (str): Version in data for first package
        - results_0_data_description (str): Description in data for first package
        - results_0_data_downloads (int): Weekly downloads for first package
        - results_0_data_maintenance (float): Maintenance score for first package
        - results_0_data_security (float): Security score for first package
        - results_1_packageInput (str): Input name of second package
        - results_1_packageName (str): Resolved name of second package
        - results_1_versionQueried (str): Version queried for second package
        - results_1_status (str): Status of second package query
        - results_1_error (str): Error message for second package (if any)
        - results_1_message (str): Message for second package
        - results_1_data_name (str): Name in data for second package
        - results_1_data_version (str): Version in data for second package
        - results_1_data_description (str): Description in data for second package
        - results_1_data_downloads (int): Weekly downloads for second package
        - results_1_data_maintenance (float): Maintenance score for second package
        - results_1_data_security (float): Security score for second package
        - message (str): Summary message about the comparison
    """
    return {
        "queryPackages_0": "lodash",
        "queryPackages_1": "underscore",
        "results_0_packageInput": "lodash",
        "results_0_packageName": "lodash",
        "results_0_versionQueried": "latest",
        "results_0_status": "success",
        "results_0_error": "",
        "results_0_message": "Package data retrieved successfully",
        "results_0_data_name": "lodash",
        "results_0_data_version": "4.17.21",
        "results_0_data_description": "A modern JavaScript utility library delivering modularity, performance, & extras.",
        "results_0_data_downloads": 15000000,
        "results_0_data_maintenance": 0.95,
        "results_0_data_security": 0.98,
        "results_1_packageInput": "underscore",
        "results_1_packageName": "underscore",
        "results_1_versionQueried": "latest",
        "results_1_status": "success",
        "results_1_error": "",
        "results_1_message": "Package data retrieved successfully",
        "results_1_data_name": "underscore",
        "results_1_data_version": "1.13.6",
        "results_1_data_description": "JavaScript's utility _ belt",
        "results_1_data_downloads": 4500000,
        "results_1_data_maintenance": 0.75,
        "results_1_data_security": 0.92,
        "message": "Compared 2 NPM packages successfully"
    }

def npm_sentinel_mcp_npmCompare(packages: List[str]) -> Dict[str, Any]:
    """
    Compare multiple NPM packages based on various metrics.
    
    Args:
        packages (List[str]): List of package names to compare
        
    Returns:
        Dict containing:
        - queryPackages (List[str]): list of package names that were queried in the request
        - results (List[Dict]): list of result objects for each package, containing 
          'packageInput', 'packageName', 'versionQueried', 'status', 'error', 'data' 
          (with package metadata), and 'message'
        - message (str): summary message indicating total number of packages compared or overall status
        
    Raises:
        ValueError: If packages list is empty
    """
    if not packages:
        raise ValueError("At least one package must be specified for comparison")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("npm-sentinel-mcp-npmCompare")
    
    # Construct queryPackages list from available indices
    query_packages = []
    for i in range(2):  # We have up to 2 packages in the mock data
        key = f"queryPackages_{i}"
        if key in api_data and api_data[key]:
            query_packages.append(api_data[key])
    
    # Construct results list
    results = []
    for i in range(2):  # Process up to 2 results
        package_key = f"results_{i}_packageInput"
        if package_key not in api_data:
            break
            
        # Extract data fields for this result
        data = {
            "name": api_data.get(f"results_{i}_data_name", ""),
            "version": api_data.get(f"results_{i}_data_version", ""),
            "description": api_data.get(f"results_{i}_data_description", ""),
            "downloads": api_data.get(f"results_{i}_data_downloads", 0),
            "maintenance": api_data.get(f"results_{i}_data_maintenance", 0.0),
            "security": api_data.get(f"results_{i}_data_security", 0.0)
        }
        
        # Build result object
        result = {
            "packageInput": api_data.get(f"results_{i}_packageInput", ""),
            "packageName": api_data.get(f"results_{i}_packageName", ""),
            "versionQueried": api_data.get(f"results_{i}_versionQueried", ""),
            "status": api_data.get(f"results_{i}_status", "error"),
            "error": api_data.get(f"results_{i}_error", ""),
            "data": data,
            "message": api_data.get(f"results_{i}_message", "")
        }
        results.append(result)
    
    # Return final structured response
    return {
        "queryPackages": query_packages,
        "results": results,
        "message": api_data.get("message", f"Compared {len(results)} NPM packages")
    }