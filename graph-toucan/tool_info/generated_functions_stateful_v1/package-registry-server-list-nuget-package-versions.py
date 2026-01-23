from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for NuGet package versions.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - total_count (int): Total number of versions available
        - package_name (str): Name of the NuGet package
        - latest_version (str): Most recent stable version string
        - has_prerelease (bool): Whether any version is prerelease
        - is_deprecated (bool): Whether the package is deprecated
        - pagination_limit (int): Number of items requested
        - pagination_returned (int): Actual number of versions returned
        - version_0_version (str): First version number
        - version_0_published_at (str): Publication date of first version (ISO format)
        - version_0_is_deprecated (bool): Deprecation status of first version
        - version_0_download_count (int): Download count for first version
        - version_0_package_size (int): Package size in bytes for first version
        - version_1_version (str): Second version number
        - version_1_published_at (str): Publication date of second version (ISO format)
        - version_1_is_deprecated (bool): Deprecation status of second version
        - version_1_download_count (int): Download count for second version
        - version_1_package_size (int): Package size in bytes for second version
    """
    # Simulate realistic data based on package name
    base_time = datetime.now() - timedelta(days=1000)
    version1_time = base_time + timedelta(days=random.randint(0, 800))
    version2_time = version1_time + timedelta(days=random.randint(1, 200))
    
    return {
        "total_count": random.randint(5, 50),
        "package_name": "Newtonsoft.Json",
        "latest_version": "13.0.3",
        "has_prerelease": random.choice([True, False]),
        "is_deprecated": False,
        "pagination_limit": 2,
        "pagination_returned": 2,
        "version_0_version": "13.0.1",
        "version_0_published_at": (version1_time).isoformat(),
        "version_0_is_deprecated": random.choice([True, False]),
        "version_0_download_count": random.randint(100000, 10000000),
        "version_0_package_size": random.randint(100000, 2000000),
        "version_1_version": "13.0.3",
        "version_1_published_at": (version2_time).isoformat(),
        "version_1_is_deprecated": False,
        "version_1_download_count": random.randint(500000, 15000000),
        "version_1_package_size": random.randint(100000, 2000000),
    }

def package_registry_server_list_nuget_package_versions(limit: Optional[int] = None, name: str = "") -> Dict[str, Any]:
    """
    List all versions of a specific NuGet package.
    
    Args:
        limit (Optional[int]): Maximum number of versions to return. If not provided, defaults to a reasonable number.
        name (str): Name of the NuGet package to query (required).
    
    Returns:
        Dict containing:
        - versions (List[Dict]): List of version objects with version number, publication date, 
          deprecation status, download count, and package size
        - total_count (int): Total number of versions available
        - package_name (str): Name of the queried package
        - latest_version (str): Most recent stable version
        - has_prerelease (bool): Whether any listed version is prerelease
        - is_deprecated (bool): Whether the package is deprecated
        - pagination (Dict): Pagination details including limit and returned count
    
    Raises:
        ValueError: If name is empty or None
    """
    if not name:
        raise ValueError("Parameter 'name' is required and cannot be empty")
    
    # Use default limit if not provided
    effective_limit = limit if limit is not None else 100
    if effective_limit <= 0:
        effective_limit = 1
    
    # Get data from "external" API (simulated)
    api_data = call_external_api("package-registry-server-list-nuget-package-versions", **locals())
    
    # Construct versions list from indexed fields
    versions = []
    for i in range(api_data["pagination_returned"]):
        version_key = f"version_{i}_version"
        published_at_key = f"version_{i}_published_at"
        is_deprecated_key = f"version_{i}_is_deprecated"
        download_count_key = f"version_{i}_download_count"
        package_size_key = f"version_{i}_package_size"
        
        if version_key in api_data:
            versions.append({
                "version": api_data[version_key],
                "published_at": api_data[published_at_key],
                "is_deprecated": api_data[is_deprecated_key],
                "download_count": api_data[download_count_key],
                "package_size": api_data[package_size_key]
            })
    
    # Apply limit to versions if needed
    actual_returned = min(len(versions), effective_limit)
    limited_versions = versions[:actual_returned]
    
    # Construct final result matching output schema
    result = {
        "versions": limited_versions,
        "total_count": api_data["total_count"],
        "package_name": api_data["package_name"],
        "latest_version": api_data["latest_version"],
        "has_prerelease": api_data["has_prerelease"],
        "is_deprecated": api_data["is_deprecated"],
        "pagination": {
            "limit": effective_limit,
            "returned": actual_returned
        }
    }
    
    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
