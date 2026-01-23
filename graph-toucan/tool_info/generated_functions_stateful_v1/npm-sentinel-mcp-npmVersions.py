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
    Simulates fetching data from external API for NPM package versions.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_packageInput (str): Original package name input for first result
        - result_0_packageName (str): Normalized package name for first result
        - result_0_status (str): Status of operation ('success' or 'error')
        - result_0_error (str or None): Error message if failed, else None
        - result_0_message (str): Human-readable message for first result
        - result_0_data_allVersions_0 (str): First version in allVersions list
        - result_0_data_allVersions_1 (str): Second version in allVersions list
        - result_0_data_tags_latest (str): Version string for 'latest' tag
        - result_0_data_latestVersionTag (str): Version corresponding to 'latest' tag
        - result_1_packageInput (str): Original package name input for second result
        - result_1_packageName (str): Normalized package name for second result
        - result_1_status (str): Status of operation ('success' or 'error')
        - result_1_error (str or None): Error message if failed, else None
        - result_1_message (str): Human-readable message for second result
        - result_1_data_allVersions_0 (str): First version in allVersions list
        - result_1_data_allVersions_1 (str): Second version in allVersions list
        - result_1_data_tags_latest (str): Version string for 'latest' tag
        - result_1_data_latestVersionTag (str): Version corresponding to 'latest' tag
    """
    return {
        "result_0_packageInput": "express",
        "result_0_packageName": "express",
        "result_0_status": "success",
        "result_0_error": None,
        "result_0_message": "Successfully retrieved versions",
        "result_0_data_allVersions_0": "1.0.0",
        "result_0_data_allVersions_1": "1.0.1",
        "result_0_data_tags_latest": "1.0.1",
        "result_0_data_latestVersionTag": "1.0.1",
        "result_1_packageInput": "nonexistent-package-xyz",
        "result_1_packageName": "nonexistent-package-xyz",
        "result_1_status": "error",
        "result_1_error": "Package not found",
        "result_1_message": "Failed to retrieve versions: Package not found",
        "result_1_data_allVersions_0": "0.0.1",
        "result_1_data_allVersions_1": "0.0.2",
        "result_1_data_tags_latest": "0.0.2",
        "result_1_data_latestVersionTag": "0.0.2",
    }

def npm_sentinel_mcp_npmVersions(packages: List[str]) -> Dict[str, Any]:
    """
    Get all available versions of an NPM package.

    Args:
        packages (List[str]): List of package names to get versions for

    Returns:
        Dict containing 'results' key with a list of result objects. Each result contains:
        - packageInput (str): original package name input
        - packageName (str): normalized package name
        - status (str): operation status ('success' or 'error')
        - error (str or None): error message if failed, otherwise None
        - message (str): human-readable message summarizing outcome
        - data (Dict): version-related data including:
            - allVersions (List[str]): list of all published versions
            - tags (Dict): mapping of dist-tags to version strings
            - latestVersionTag (str): version string for 'latest' tag
    """
    if not isinstance(packages, list):
        return {
            "results": [
                {
                    "packageInput": "",
                    "packageName": "",
                    "status": "error",
                    "error": "Invalid input: packages must be a list",
                    "message": "Invalid input: packages must be a list",
                    "data": {
                        "allVersions": [],
                        "tags": {},
                        "latestVersionTag": ""
                    }
                }
            ]
        }

    if len(packages) == 0:
        return {"results": []}

    api_data = call_external_api("npm-sentinel-mcp-npmVersions", **locals())
    results: List[Dict[str, Any]] = []

    for i, package in enumerate(packages[:2]):  # Only process up to 2 packages
        result_key = f"result_{i}"
        if f"{result_key}_packageInput" in api_data:
            all_versions = [
                api_data.get(f"{result_key}_data_allVersions_0", ""),
                api_data.get(f"{result_key}_data_allVersions_1", "")
            ]
            # Filter out empty strings
            all_versions = [v for v in all_versions if v]

            result = {
                "packageInput": api_data[f"{result_key}_packageInput"],
                "packageName": api_data[f"{result_key}_packageName"],
                "status": api_data[f"{result_key}_status"],
                "error": api_data[f"{result_key}_error"],
                "message": api_data[f"{result_key}_message"],
                "data": {
                    "allVersions": all_versions,
                    "tags": {
                        "latest": api_data.get(f"{result_key}_data_tags_latest", "")
                    },
                    "latestVersionTag": api_data.get(f"{result_key}_data_latestVersionTag", "")
                }
            }
        else:
            # Fallback for any package not covered by API mock
            result = {
                "packageInput": package,
                "packageName": package,
                "status": "error",
                "error": "Package not found",
                "message": "Failed to retrieve versions: Package not found",
                "data": {
                    "allVersions": [],
                    "tags": {},
                    "latestVersionTag": ""
                }
            }
        
        results.append(result)

    return {"results": results}

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
