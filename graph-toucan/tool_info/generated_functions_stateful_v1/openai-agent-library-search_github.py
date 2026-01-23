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
    Simulates fetching data from external API for GitHub repository search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_path (str): File path of first search result
        - result_0_url (str): Direct URL to first file
        - result_0_snippet (str): Text snippet containing match for first result
        - result_0_matched_term (str): Term that matched in query for first result
        - result_1_path (str): File path of second search result
        - result_1_url (str): Direct URL to second file
        - result_1_snippet (str): Text snippet containing match for second result
        - result_1_matched_term (str): Term that matched in query for second result
        - debug_info_search_query (str): Original query string used for search
        - debug_info_search_terms_0 (str): First extracted search term
        - debug_info_search_terms_1 (str): Second extracted search term
        - debug_info_directories_searched_0 (str): First directory scanned
        - debug_info_directories_searched_1 (str): Second directory scanned
        - debug_info_errors_0 (str): First error message encountered
        - debug_info_errors_1 (str): Second error message encountered
    """
    return {
        "result_0_path": "/src/main.py",
        "result_0_url": "https://github.com/example/repo/blob/main/src/main.py",
        "result_0_snippet": 'def search_github(query: str) -> List[Dict]:\n    """Search GitHub repo for given query term."""\n    if not query:',
        "result_0_matched_term": "query",
        "result_1_path": "/docs/README.md",
        "result_1_url": "https://github.com/example/repo/blob/main/docs/README.md",
        "result_1_snippet": '# GitHub Search Tool\nThis tool allows you to search for a specific term across the repository.\nSearch term: "query"',
        "result_1_matched_term": "query",
        "debug_info_search_query": "query",
        "debug_info_search_terms_0": "query",
        "debug_info_search_terms_1": "",
        "debug_info_directories_searched_0": "/src",
        "debug_info_directories_searched_1": "/docs",
        "debug_info_errors_0": "",
        "debug_info_errors_1": ""
    }

def openai_agent_library_search_github(query: str) -> Dict[str, Any]:
    """
    Search for a specific term across the GitHub repository.
    
    Args:
        query (str): The search term to look for in the repository files.
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of dictionaries with keys 'path', 'url', 'snippet', 'matched_term'
        - debug_info (Dict): Dictionary with keys 'search_query', 'search_terms', 'directories_searched', 'errors'
        
    Raises:
        ValueError: If query is empty or not a string.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")
    
    # Call external API to get flattened data
    api_data = call_external_api("openai-agent-library-search_github", **locals())
    
    # Construct results list from indexed fields
    results = [
        {
            "path": api_data["result_0_path"],
            "url": api_data["result_0_url"],
            "snippet": api_data["result_0_snippet"],
            "matched_term": api_data["result_0_matched_term"]
        },
        {
            "path": api_data["result_1_path"],
            "url": api_data["result_1_url"],
            "snippet": api_data["result_1_snippet"],
            "matched_term": api_data["result_1_matched_term"]
        }
    ]
    
    # Construct debug_info dictionary
    debug_info = {
        "search_query": api_data["debug_info_search_query"],
        "search_terms": [
            api_data["debug_info_search_terms_0"],
            api_data["debug_info_search_terms_1"]
        ],
        "directories_searched": [
            api_data["debug_info_directories_searched_0"],
            api_data["debug_info_directories_searched_1"]
        ],
        "errors": []
    }
    
    # Only include non-empty error strings
    if api_data["debug_info_errors_0"]:
        debug_info["errors"].append(api_data["debug_info_errors_0"])
    if api_data["debug_info_errors_1"]:
        debug_info["errors"].append(api_data["debug_info_errors_1"])
    
    return {
        "results": results,
        "debug_info": debug_info
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
