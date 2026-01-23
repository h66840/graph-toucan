from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for listing NPM package versions.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): Name of the NPM package
        - totalVersions (int): Total number of versions available
        - versionsShown (int): Number of versions included in response
        - latestVersion (str): Version string of the most recent release
        - version_0 (str): First version in the list (latest)
        - version_1 (str): Second version in the list (older than latest)
    """
    return {
        "name": "express",
        "totalVersions": 150,
        "versionsShown": 2,
        "latestVersion": "4.18.2",
        "version_0": "4.18.2",
        "version_1": "4.18.1"
    }

def package_registry_server_list_npm_package_versions(limit: Optional[int] = None, name: str = "") -> Dict[str, Any]:
    """
    List all versions of a specific NPM package.
    
    Args:
        limit (Optional[int]): Maximum number of versions to return. If not provided, defaults to 2.
        name (str): Name of the NPM package (required).
    
    Returns:
        Dict containing:
        - name (str): name of the NPM package
        - totalVersions (int): total number of versions available for the package
        - versionsShown (int): number of versions included in this response
        - latestVersion (str): version string of the most recent release
        - versions (List[str]): list of available version strings, ordered from latest to oldest
    
    Raises:
        ValueError: If name is not provided or is empty.
    """
    if not name:
        raise ValueError("Parameter 'name' is required and cannot be empty.")
    
    # Set default limit
    effective_limit = limit if limit is not None else 2
    if effective_limit < 1:
        effective_limit = 1
    
    # Fetch data from "external" API (simulated)
    api_data = call_external_api("package-registry-server-list-npm-package-versions")
    
    # Construct versions list from indexed fields
    versions = []
    for i in range(min(effective_limit, 2)):  # We only have 2 mock versions
        version_key = f"version_{i}"
        if version_key in api_data:
            versions.append(api_data[version_key])
    
    # Adjust versionsShown based on actual number of versions returned
    versions_shown = len(versions)
    
    # Construct result according to output schema
    result = {
        "name": api_data["name"],
        "totalVersions": api_data["totalVersions"],
        "versionsShown": versions_shown,
        "latestVersion": api_data["latestVersion"],
        "versions": versions
    }
    
    return result