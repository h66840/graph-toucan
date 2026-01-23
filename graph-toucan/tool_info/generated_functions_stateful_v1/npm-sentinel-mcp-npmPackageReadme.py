from typing import Dict, List, Any, Optional
from datetime import datetime

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
    api_data = call_external_api("npm-sentinel-mcp-npmPackageReadme", **locals())
    
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
