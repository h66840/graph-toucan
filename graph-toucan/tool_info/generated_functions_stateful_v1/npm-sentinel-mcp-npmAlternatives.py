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
    Simulates fetching data from external API for npm package alternatives.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - query_packages_0 (str): First queried package name
        - query_packages_1 (str): Second queried package name (if applicable)
        - results_0_package_input (str): Original input string for first package
        - results_0_package_name (str): Resolved name of first package
        - results_0_status (str): Status of first query (e.g., 'success')
        - results_0_error (str or None): Error message if failed, else None
        - results_0_message (str): Human-readable summary for first result
        - results_0_original_package_stats_name (str): Name of original package
        - results_0_original_package_stats_monthly_downloads (int): Monthly downloads of original
        - results_0_original_package_stats_keywords_0 (str): First keyword of original package
        - results_0_original_package_stats_keywords_1 (str): Second keyword of original package
        - results_0_data_alternatives_0_name (str): First alternative package name
        - results_0_data_alternatives_0_description (str): Description of first alternative
        - results_0_data_alternatives_0_version (str): Version of first alternative
        - results_0_data_alternatives_0_monthly_downloads (int): Monthly downloads of first alternative
        - results_0_data_alternatives_0_score (float): Relevance score of first alternative
        - results_0_data_alternatives_0_repository_url (str): Repository URL of first alternative
        - results_0_data_alternatives_0_keywords_0 (str): First keyword of first alternative
        - results_0_data_alternatives_0_keywords_1 (str): Second keyword of first alternative
        - results_0_data_alternatives_1_name (str): Second alternative package name
        - results_0_data_alternatives_1_description (str): Description of second alternative
        - results_0_data_alternatives_1_version (str): Version of second alternative
        - results_0_data_alternatives_1_monthly_downloads (int): Monthly downloads of second alternative
        - results_0_data_alternatives_1_score (float): Relevance score of second alternative
        - results_0_data_alternatives_1_repository_url (str): Repository URL of second alternative
        - results_0_data_alternatives_1_keywords_0 (str): First keyword of second alternative
        - results_0_data_alternatives_1_keywords_1 (str): Second keyword of second alternative
        - results_1_package_input (str): Original input string for second package (if exists)
        - results_1_package_name (str): Resolved name of second package (if exists)
        - results_1_status (str): Status of second query (if exists)
        - results_1_error (str or None): Error message for second query (if exists)
        - results_1_message (str): Message for second result (if exists)
        - results_1_original_package_stats_name (str): Name of second original package
        - results_1_original_package_stats_monthly_downloads (int): Monthly downloads of second original
        - results_1_original_package_stats_keywords_0 (str): First keyword of second original
        - results_1_original_package_stats_keywords_1 (str): Second keyword of second original
        - results_1_data_alternatives_0_name (str): First alternative for second package
        - results_1_data_alternatives_0_description (str): Description of first alternative for second
        - results_1_data_alternatives_0_version (str): Version of first alternative for second
        - results_1_data_alternatives_0_monthly_downloads (int): Monthly downloads of first alternative
        - results_1_data_alternatives_0_score (float): Score of first alternative for second
        - results_1_data_alternatives_0_repository_url (str): Repository URL of first alternative
        - results_1_data_alternatives_0_keywords_0 (str): First keyword of first alternative
        - results_1_data_alternatives_0_keywords_1 (str): Second keyword of first alternative
        - results_1_data_alternatives_1_name (str): Second alternative for second package
        - results_1_data_alternatives_1_description (str): Description of second alternative
        - results_1_data_alternatives_1_version (str): Version of second alternative
        - results_1_data_alternatives_1_monthly_downloads (int): Monthly downloads of second alternative
        - results_1_data_alternatives_1_score (float): Score of second alternative
        - results_1_data_alternatives_1_repository_url (str): Repository URL of second alternative
        - results_1_data_alternatives_1_keywords_0 (str): First keyword of second alternative
        - results_1_data_alternatives_1_keywords_1 (str): Second keyword of second alternative
    """
    return {
        "query_packages_0": "lodash",
        "query_packages_1": "underscore",
        "results_0_package_input": "lodash",
        "results_0_package_name": "lodash",
        "results_0_status": "success",
        "results_0_error": None,
        "results_0_message": "Successfully found alternatives for lodash",
        "results_0_original_package_stats_name": "lodash",
        "results_0_original_package_stats_monthly_downloads": 25000000,
        "results_0_original_package_stats_keywords_0": "util",
        "results_0_original_package_stats_keywords_1": "functional",
        "results_0_data_alternatives_0_name": "underscore",
        "results_0_data_alternatives_0_description": "JavaScript's utility _ belt",
        "results_0_data_alternatives_0_version": "1.13.6",
        "results_0_data_alternatives_0_monthly_downloads": 5000000,
        "results_0_data_alternatives_0_score": 0.92,
        "results_0_data_alternatives_0_repository_url": "https://github.com/jashkenas/underscore",
        "results_0_data_alternatives_0_keywords_0": "util",
        "results_0_data_alternatives_0_keywords_1": "functional",
        "results_0_data_alternatives_1_name": "ramda",
        "results_0_data_alternatives_1_description": "Practical functional programming in JavaScript",
        "results_0_data_alternatives_1_version": "0.29.0",
        "results_0_data_alternatives_1_monthly_downloads": 3000000,
        "results_0_data_alternatives_1_score": 0.85,
        "results_0_data_alternatives_1_repository_url": "https://github.com/ramda/ramda",
        "results_0_data_alternatives_1_keywords_0": "functional",
        "results_0_data_alternatives_1_keywords_1": "immutable",
        "results_1_package_input": "underscore",
        "results_1_package_name": "underscore",
        "results_1_status": "success",
        "results_1_error": None,
        "results_1_message": "Successfully found alternatives for underscore",
        "results_1_original_package_stats_name": "underscore",
        "results_1_original_package_stats_monthly_downloads": 5000000,
        "results_1_original_package_stats_keywords_0": "util",
        "results_1_original_package_stats_keywords_1": "functional",
        "results_1_data_alternatives_0_name": "lodash",
        "results_1_data_alternatives_0_description": "A modern JavaScript utility library delivering modularity, performance & extras",
        "results_1_data_alternatives_0_version": "4.17.21",
        "results_1_data_alternatives_0_monthly_downloads": 25000000,
        "results_1_data_alternatives_0_score": 0.95,
        "results_1_data_alternatives_0_repository_url": "https://github.com/lodash/lodash",
        "results_1_data_alternatives_0_keywords_0": "util",
        "results_1_data_alternatives_0_keywords_1": "functional",
        "results_1_data_alternatives_1_name": "dashjs",
        "results_1_data_alternatives_1_description": "Minimal functional utility library",
        "results_1_data_alternatives_1_version": "1.5.0",
        "results_1_data_alternatives_1_monthly_downloads": 100000,
        "results_1_data_alternatives_1_score": 0.75,
        "results_1_data_alternatives_1_repository_url": "https://github.com/username/dashjs",
        "results_1_data_alternatives_1_keywords_0": "util",
        "results_1_data_alternatives_1_keywords_1": "lightweight"
    }


def npm_sentinel_mcp_npmAlternatives(packages: List[str]) -> Dict[str, Any]:
    """
    Find alternative packages with similar functionality to the given npm packages.

    Args:
        packages (List[str]): List of package names to find alternatives for

    Returns:
        Dict with scalar fields only (str, int, float, bool) describing package alternatives
    """
    if not packages:
        return {}

    result = call_external_api("npm-alternatives", **locals())
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
