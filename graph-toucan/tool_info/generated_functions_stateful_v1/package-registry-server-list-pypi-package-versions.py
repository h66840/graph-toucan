from typing import Dict, List, Any, Optional

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
    Simulates fetching data from external API for listing PyPI package versions.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): Name of the PyPI package
        - totalVersions (int): Total number of versions ever released
        - versionsShown (int): Number of versions included in this response
        - latestVersion (str): Version string of the most recent release
        - version_0 (str): First version in descending chronological order
        - version_1 (str): Second version in descending chronological order
    """
    return {
        "name": "requests",
        "totalVersions": 150,
        "versionsShown": 2,
        "latestVersion": "2.31.0",
        "version_0": "2.31.0",
        "version_1": "2.30.0"
    }

def package_registry_server_list_pypi_package_versions(limit: Optional[int] = None, name: str = "") -> Dict[str, Any]:
    """
    List all versions of a specific PyPI package.
    
    Args:
        limit (Optional[int]): Maximum number of versions to return. If not provided, all versions are returned.
        name (str): Name of the PyPI package (required).
    
    Returns:
        Dict containing:
        - name (str): name of the PyPI package
        - totalVersions (int): total number of versions ever released for the package
        - versionsShown (int): number of versions included in this response, may be limited by the limit parameter
        - latestVersion (str): version string of the most recent release
        - versions (List[str]): list of all available version strings in descending chronological order
    
    Raises:
        ValueError: If name is not provided or empty.
    """
    if not name:
        raise ValueError("Parameter 'name' is required and cannot be empty.")
    
    # Fetch data from simulated external API
    api_data = call_external_api("package-registry-server-list-pypi-package-versions", **locals())
    
    # Extract simple fields from API response
    package_name = api_data["name"]
    total_versions = api_data["totalVersions"]
    latest_version = api_data["latestVersion"]
    
    # Construct versions list from indexed fields
    raw_versions = [
        api_data["version_0"],
        api_data["version_1"]
    ]
    
    # Apply limit if specified
    if limit is not None and limit > 0:
        versions = raw_versions[:limit]
        versions_shown = min(len(raw_versions), limit)
    else:
        versions = raw_versions
        versions_shown = len(raw_versions)
    
    # Construct final result matching output schema
    result = {
        "name": package_name,
        "totalVersions": total_versions,
        "versionsShown": versions_shown,
        "latestVersion": latest_version,
        "versions": versions
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
