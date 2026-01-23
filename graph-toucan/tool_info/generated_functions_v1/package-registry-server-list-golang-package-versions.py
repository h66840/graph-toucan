from typing import Dict, List, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Go module version listing.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - version_0_version (str): First version number
        - version_0_timestamp (str): Publication timestamp of first version
        - version_0_module (str): Module name for first version
        - version_1_version (str): Second version number
        - version_1_timestamp (str): Publication timestamp of second version
        - version_1_module (str): Module name for second version
        - total_count (int): Total number of versions available
        - module (str): Name of the Go module requested
        - latest_version (str): Most recent version of the module
        - has_next_page (bool): Whether more versions are available beyond limit
        - next_cursor (str): Token to fetch next page of results
        - metadata_time (str): Time of listing in ISO format
        - metadata_source_url (str): Source registry URL
        - metadata_cache_hit (bool): Whether result was served from cache
    """
    return {
        "version_0_version": "v1.0.0",
        "version_0_timestamp": "2022-01-15T10:30:00Z",
        "version_0_module": "github.com/example/module",
        "version_1_version": "v1.1.0",
        "version_1_timestamp": "2022-03-20T14:45:00Z",
        "version_1_module": "github.com/example/module",
        "total_count": 5,
        "module": "github.com/example/module",
        "latest_version": "v1.2.0",
        "has_next_page": True,
        "next_cursor": "cursor_123",
        "metadata_time": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata_source_url": "https://proxy.golang.org",
        "metadata_cache_hit": False,
    }

def package_registry_server_list_golang_package_versions(
    module: str, 
    limit: Optional[int] = None
) -> Dict[str, Any]:
    """
    List all versions of a specific Go module/package.
    
    Args:
        module (str): Name of the Go module to query (required)
        limit (Optional[int]): Maximum number of versions to return (optional)
    
    Returns:
        Dict containing:
        - versions (List[Dict]): List of version objects with version, timestamp, and module
        - total_count (int): Total number of versions available
        - module (str): Name of the Go module requested
        - latest_version (str): The most recent version of the module
        - has_next_page (bool): Indicates if more versions are available
        - next_cursor (str): Token to fetch next page of results
        - metadata (Dict): Additional registry-level metadata
    
    Raises:
        ValueError: If module parameter is empty or None
    """
    if not module:
        raise ValueError("Parameter 'module' is required and cannot be empty")
    
    if limit is not None and limit < 1:
        raise ValueError("Parameter 'limit' must be a positive integer if provided")
    
    # Call external API to get flattened data
    api_data = call_external_api("package-registry-server-list-golang-package-versions")
    
    # Construct versions list from indexed fields
    versions = [
        {
            "version": api_data["version_0_version"],
            "timestamp": api_data["version_0_timestamp"],
            "module": api_data["version_0_module"]
        },
        {
            "version": api_data["version_1_version"],
            "timestamp": api_data["version_1_timestamp"],
            "module": api_data["version_1_module"]
        }
    ]
    
    # Apply limit if specified
    if limit is not None:
        versions = versions[:limit]
    
    # Construct metadata dictionary
    metadata = {
        "time": api_data["metadata_time"],
        "source_url": api_data["metadata_source_url"],
        "cache_hit": api_data["metadata_cache_hit"]
    }
    
    # Construct final result matching output schema
    result = {
        "versions": versions,
        "total_count": api_data["total_count"],
        "module": api_data["module"],
        "latest_version": api_data["latest_version"],
        "has_next_page": api_data["has_next_page"],
        "next_cursor": api_data["next_cursor"],
        "metadata": metadata
    }
    
    return result