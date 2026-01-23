from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for NPM package READMEs.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - readme_0_package (str): First requested package name
        - readme_0_readme (str): README content for first package
        - readme_1_package (str): Second requested package name
        - readme_1_readme (str): README content for second package
        - not_found_0 (str): First package not found
        - not_found_1 (str): Second package not found
        - total_requested (int): Total number of packages requested
        - total_retrieved (int): Number of READMEs successfully retrieved
        - metadata_timestamp (str): ISO format timestamp of the request
    """
    return {
        "readme_0_package": "lodash",
        "readme_0_readme": "# Lodash\nA modern JavaScript utility library delivering modularity, performance, and extras.",
        "readme_1_package": "express",
        "readme_1_readme": "# Express\nFast, unopinionated, minimalist web framework for Node.js.",
        "not_found_0": "nonexistent-package",
        "not_found_1": "fake-package-404",
        "total_requested": 4,
        "total_retrieved": 2,
        "metadata_timestamp": datetime.now().isoformat()
    }

def npm_sentinel_mcp_npmPackageReadme(packages: List[str]) -> Dict[str, Any]:
    """
    Get the README content for NPM packages.
    
    Args:
        packages (List[str]): List of package names to get READMEs for
        
    Returns:
        Dict containing:
        - readmes (List[Dict]): List of dictionaries with 'package' and 'readme' keys
        - not_found (List[str]): List of package names that were not found
        - metadata (Dict): Information about the request execution including 
          total_requested, total_retrieved, and timestamp
          
    Raises:
        ValueError: If packages list is empty
    """
    if not packages:
        raise ValueError("Packages list cannot be empty")
    
    # Call external API to simulate data retrieval
    api_data = call_external_api("npm-sentinel-mcp-npmPackageReadme")
    
    # Construct readmes list from indexed fields
    readmes: List[Dict[str, str]] = []
    for i in range(2):  # Two items as per requirements
        package_key = f"readme_{i}_package"
        readme_key = f"readme_{i}_readme"
        if package_key in api_data and readme_key in api_data:
            readmes.append({
                "package": api_data[package_key],
                "readme": api_data[readme_key]
            })
    
    # Construct not_found list from indexed fields
    not_found: List[str] = []
    for i in range(2):
        key = f"not_found_{i}"
        if key in api_data and api_data[key]:
            not_found.append(api_data[key])
    
    # Construct metadata
    metadata = {
        "total_requested": api_data["total_requested"],
        "total_retrieved": api_data["total_retrieved"],
        "timestamp": api_data["metadata_timestamp"]
    }
    
    return {
        "readmes": readmes,
        "not_found": not_found,
        "metadata": metadata
    }