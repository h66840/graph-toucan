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
    Simulates fetching data from external API for NPM maintainers.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - queryPackages_0 (str): First queried package identifier
        - queryPackages_1 (str): Second queried package identifier
        - results_0_packageInput (str): Original input string for first package
        - results_0_packageName (str): Resolved name of first package
        - results_0_status (str): Status of first query ('success' or 'error')
        - results_0_error (str or None): Error message if first query failed
        - results_0_message (str): Human-readable message for first result
        - results_0_data_maintainersCount (int): Number of maintainers for first package
        - results_0_data_maintainers_0_name (str): First maintainer's name for first package
        - results_0_data_maintainers_0_email (str): First maintainer's email for first package
        - results_0_data_maintainers_0_url (str or None): First maintainer's URL for first package
        - results_0_data_maintainers_1_name (str): Second maintainer's name for first package
        - results_0_data_maintainers_1_email (str): Second maintainer's email for first package
        - results_0_data_maintainers_1_url (str or None): Second maintainer's URL for first package
        - results_1_packageInput (str): Original input string for second package
        - results_1_packageName (str): Resolved name of second package
        - results_1_status (str): Status of second query ('success' or 'error')
        - results_1_error (str or None): Error message if second query failed
        - results_1_message (str): Human-readable message for second result
        - results_1_data_maintainersCount (int): Number of maintainers for second package
        - results_1_data_maintainers_0_name (str): First maintainer's name for second package
        - results_1_data_maintainers_0_email (str): First maintainer's email for second package
        - results_1_data_maintainers_0_url (str or None): First maintainer's URL for second package
        - results_1_data_maintainers_1_name (str): Second maintainer's name for second package
        - results_1_data_maintainers_1_email (str): Second maintainer's email for second package
        - results_1_data_maintainers_1_url (str or None): Second maintainer's URL for second package
        - message (str): Summary message about the overall operation
    """
    return {
        "queryPackages_0": "express@4.18.2",
        "queryPackages_1": "lodash@4.17.21",
        "results_0_packageInput": "express@4.18.2",
        "results_0_packageName": "express",
        "results_0_status": "success",
        "results_0_error": None,
        "results_0_message": "Successfully retrieved maintainer information",
        "results_0_data_maintainersCount": 2,
        "results_0_data_maintainers_0_name": "dougwilson",
        "results_0_data_maintainers_0_email": "doug@somethingdoug.com",
        "results_0_data_maintainers_0_url": None,
        "results_0_data_maintainers_1_name": "tjholowaychuk",
        "results_0_data_maintainers_1_email": "tj@vision-media.ca",
        "results_0_data_maintainers_1_url": None,
        "results_1_packageInput": "lodash@4.17.21",
        "results_1_packageName": "lodash",
        "results_1_status": "success",
        "results_1_error": None,
        "results_1_message": "Successfully retrieved maintainer information",
        "results_1_data_maintainersCount": 2,
        "results_1_data_maintainers_0_name": "jdalton",
        "results_1_data_maintainers_0_email": "john.david.dalton@gmail.com",
        "results_1_data_maintainers_0_url": None,
        "results_1_data_maintainers_1_name": "mathias",
        "results_1_data_maintainers_1_email": "mathias@qiwi.com",
        "results_1_data_maintainers_1_url": None,
        "message": "Processed 2 packages successfully"
    }

def npm_sentinel_mcp_npmMaintainers(packages: List[str]) -> Dict[str, Any]:
    """
    Get maintainers information for NPM packages.

    Args:
        packages (List[str]): List of package names to get maintainers for, optionally with version specifiers.

    Returns:
        Dict containing:
        - queryPackages (List[str]): list of package identifiers as queried
        - results (List[Dict]): list of result objects for each queried package
        - message (str): summary message about the overall operation

        Each result contains:
        - packageInput (str): original input string for the package
        - packageName (str): resolved name of the package (without version)
        - status (str): outcome status ('success' or 'error')
        - error (str or None): error details if query failed
        - data (Dict): maintainer information including 'maintainers' list and 'maintainersCount'
        - message (str): human-readable message about the result

        Within data:
        - maintainers (List[Dict]): list of maintainer objects with 'name', 'email', 'url'
        - maintainersCount (int): total number of maintainers

        Each maintainer contains:
        - name (str): maintainer's username on NPM
        - email (str or None): contact email address
        - url (str or None): associated URL (typically null)
    """
    if not packages:
        return {
            "queryPackages": [],
            "results": [],
            "message": "No packages provided"
        }

    # Call external API to get flattened data
    api_data = call_external_api("npm-sentinel-mcp-npmMaintainers", **locals())

    # Construct queryPackages from input or use API data if available
    query_packages = packages[:2]  # Use provided packages, limit to 2 for consistency with API mock
    if len(query_packages) < 2:
        # Pad with default values if needed
        while len(query_packages) < 2:
            query_packages.append("package@latest")

    # Construct results list
    results = []

    for i in range(2):  # Process two results as per API mock
        prefix = f"results_{i}"
        
        # Extract package name from input (remove version specifier)
        package_input = api_data.get(f"{prefix}_packageInput", query_packages[i])
        package_name = package_input.split('@')[0] if '@' in package_input else package_input

        # Build maintainers list
        maintainers = []
        for j in range(2):  # Two maintainers per package
            maintainer_name = api_data.get(f"{prefix}_data_maintainers_{j}_name")
            if maintainer_name is not None:
                maintainers.append({
                    "name": maintainer_name,
                    "email": api_data.get(f"{prefix}_data_maintainers_{j}_email"),
                    "url": api_data.get(f"{prefix}_data_maintainers_{j}_url")
                })

        # Build data object
        data = {
            "maintainers": maintainers,
            "maintainersCount": api_data.get(f"{prefix}_data_maintainersCount", len(maintainers))
        }

        # Build result object
        result = {
            "packageInput": package_input,
            "packageName": package_name,
            "status": api_data.get(f"{prefix}_status", "success"),
            "error": api_data.get(f"{prefix}_error"),
            "data": data,
            "message": api_data.get(f"{prefix}_message", "Operation completed")
        }

        results.append(result)

    # Return final structured response
    return {
        "queryPackages": query_packages,
        "results": results,
        "message": api_data.get("message", f"Processed {len(query_packages)} packages")
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
