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
    Simulates fetching data from external API for npm types availability.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_package (str): First package name checked
        - result_0_has_types (bool): Whether first package has TypeScript types
        - result_0_version (str): Version of the types for first package
        - result_0_typings_path (str): Path to typings for first package
        - result_1_package (str): Second package name checked
        - result_1_has_types (bool): Whether second package has TypeScript types
        - result_1_version (str): Version of the types for second package
        - result_1_typings_path (str): Path to typings for second package
        - unavailable_packages_0 (str): First package without available types
        - unavailable_packages_1 (str): Second package without available types
        - summary_total_checked (int): Total number of packages checked
        - summary_with_types (int): Number of packages with types available
        - summary_missing_types (int): Number of packages missing types
    """
    return {
        "result_0_package": "lodash",
        "result_0_has_types": True,
        "result_0_version": "4.17.21",
        "result_0_typings_path": "index.d.ts",
        "result_1_package": "axios",
        "result_1_has_types": True,
        "result_1_version": "0.27.2",
        "result_1_typings_path": "index.d.ts",
        "unavailable_packages_0": "some-legacy-pkg",
        "unavailable_packages_1": "deprecated-module",
        "summary_total_checked": 4,
        "summary_with_types": 2,
        "summary_missing_types": 2
    }

def npm_sentinel_mcp_npmTypes(packages: List[str]) -> Dict[str, Any]:
    """
    Check TypeScript types availability and version for a list of npm packages.

    Args:
        packages (List[str]): List of package names to check types for.

    Returns:
        Dict containing:
        - results (List[Dict]): List of type check results for each requested package,
          including availability, version, and related metadata.
        - unavailable_packages (List[str]): List of package names that do not have
          TypeScript types available.
        - summary (Dict): Summary statistics such as total packages checked,
          number with types available, and number missing types.

    Raises:
        ValueError: If packages list is empty.
    """
    if not packages:
        raise ValueError("packages list cannot be empty")

    # Fetch simulated external data
    api_data = call_external_api("npm-sentinel-mcp-npmTypes", **locals())

    # Construct results list from indexed fields
    results = []
    for i in range(2):  # We expect 2 results based on call_external_api
        pkg_key = f"result_{i}_package"
        has_types_key = f"result_{i}_has_types"
        version_key = f"result_{i}_version"
        typings_path_key = f"result_{i}_typings_path"

        if pkg_key in api_data:
            results.append({
                "package": api_data[pkg_key],
                "has_types": api_data[has_types_key],
                "version": api_data[version_key],
                "typings_path": api_data[typings_path_key]
            })

    # Extract unavailable packages
    unavailable_packages = []
    for i in range(2):
        key = f"unavailable_packages_{i}"
        if key in api_data and isinstance(api_data[key], str) and api_data[key]:
            unavailable_packages.append(api_data[key])

    # Construct summary
    summary = {
        "total_checked": api_data["summary_total_checked"],
        "with_types": api_data["summary_with_types"],
        "missing_types": api_data["summary_missing_types"]
    }

    return {
        "results": results,
        "unavailable_packages": unavailable_packages,
        "summary": summary
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
