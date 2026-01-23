from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for file search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - match_0_name (str): Name of the first matched file
        - match_0_path (str): Path of the first matched file
        - match_0_url (str): URL of the first matched file
        - match_1_name (str): Name of the second matched file
        - match_1_path (str): Path of the second matched file
        - match_1_url (str): URL of the second matched file
        - error (str): Error message if any occurred
        - debug_info_search_pattern (str): The search pattern used
        - debug_info_directories_searched_0 (str): First directory searched
        - debug_info_directories_searched_1 (str): Second directory searched
        - debug_info_errors_0 (str): First error in debug info
        - debug_info_errors_1 (str): Second error in debug info
    """
    return {
        "match_0_name": "README.md",
        "match_0_path": "/docs/README.md",
        "match_0_url": "https://github.com/example/repo/blob/main/docs/README.md",
        "match_1_name": "requirements.txt",
        "match_1_path": "/project/requirements.txt",
        "match_1_url": "https://github.com/example/repo/blob/main/project/requirements.txt",
        "error": "",
        "debug_info_search_pattern": "README",
        "debug_info_directories_searched_0": "/docs",
        "debug_info_directories_searched_1": "/project",
        "debug_info_errors_0": "",
        "debug_info_errors_1": ""
    }

def openai_agent_library_search_files(filename_pattern: str) -> Dict[str, Any]:
    """
    Search for files by name across the GitHub repository.
    
    Args:
        filename_pattern (str): Part of the filename to search for. Can be a full filename or a partial name.
    
    Returns:
        Dict containing:
        - matches (List[Dict]): list of matched files, each with 'name', 'path', and 'url' fields
        - error (str): error message if the search failed or no files were found
        - debug_info (Dict): contains 'search_pattern', 'directories_searched', and 'errors' from the search execution
    """
    if not filename_pattern or not isinstance(filename_pattern, str):
        return {
            "matches": [],
            "error": "Invalid input: filename_pattern must be a non-empty string",
            "debug_info": {
                "search_pattern": "",
                "directories_searched": [],
                "errors": ["Invalid input: filename_pattern must be a non-empty string"]
            }
        }

    api_data = call_external_api("openai-agent-library-search_files")
    
    # Construct matches list from indexed fields
    matches: List[Dict[str, str]] = []
    for i in range(2):
        name_key = f"match_{i}_name"
        path_key = f"match_{i}_path"
        url_key = f"match_{i}_url"
        
        if name_key in api_data and api_data[name_key]:
            matches.append({
                "name": api_data[name_key],
                "path": api_data[path_key],
                "url": api_data[url_key]
            })
    
    # Construct debug_info
    directories_searched = []
    if "debug_info_directories_searched_0" in api_data and api_data["debug_info_directories_searched_0"]:
        directories_searched.append(api_data["debug_info_directories_searched_0"])
    if "debug_info_directories_searched_1" in api_data and api_data["debug_info_directories_searched_1"]:
        directories_searched.append(api_data["debug_info_directories_searched_1"])
    
    debug_errors = []
    if "debug_info_errors_0" in api_data and api_data["debug_info_errors_0"]:
        debug_errors.append(api_data["debug_info_errors_0"])
    if "debug_info_errors_1" in api_data and api_data["debug_info_errors_1"]:
        debug_errors.append(api_data["debug_info_errors_1"])
    
    debug_info = {
        "search_pattern": api_data.get("debug_info_search_pattern", filename_pattern),
        "directories_searched": directories_searched,
        "errors": debug_errors
    }
    
    error = api_data.get("error", "")
    
    return {
        "matches": matches,
        "error": error,
        "debug_info": debug_info
    }