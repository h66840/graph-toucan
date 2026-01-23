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
    Simulates fetching data from external API for Old School RuneScape iftypes.txt search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): ID of the first search result
        - result_0_value (str): Value of the first search result
        - result_0_line (str): Full line text of the first result
        - result_0_lineNumber (int): Line number in file for first result
        - result_0_formatted (str): Formatted display string for first result
        - result_1_id (int): ID of the second search result
        - result_1_value (str): Value of the second search result
        - result_1_line (str): Full line text of the second result
        - result_1_lineNumber (int): Line number in file for second result
        - result_1_formatted (str): Formatted display string for second result
        - pagination_page (int): Current page number
        - pagination_pageSize (int): Number of results per page
        - pagination_totalResults (int): Total number of results found
        - pagination_totalPages (int): Total number of pages
        - pagination_hasNextPage (bool): Whether there is a next page
        - pagination_hasPreviousPage (bool): Whether there is a previous page
    """
    return {
        "result_0_id": 12345,
        "result_0_value": "button_cancel",
        "result_0_line": "12345=button_cancel",
        "result_0_lineNumber": 456,
        "result_0_formatted": "Interface 12345: button_cancel",
        "result_1_id": 12346,
        "result_1_value": "button_ok",
        "result_1_line": "12346=button_ok",
        "result_1_lineNumber": 457,
        "result_1_formatted": "Interface 12346: button_ok",
        "pagination_page": 1,
        "pagination_pageSize": 10,
        "pagination_totalResults": 2,
        "pagination_totalPages": 1,
        "pagination_hasNextPage": False,
        "pagination_hasPreviousPage": False
    }

def old_school_runescape_wiki_and_data_server_search_iftypes(
    query: str,
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the iftypes.txt file for interface definitions used in the game's UI.

    Args:
        query (str): The term to search for in the file (required)
        page (int, optional): Page number for pagination. Defaults to 1.
        pageSize (int, optional): Number of results per page. Defaults to 10.

    Returns:
        Dict containing:
        - results (List[Dict]): List of interface definition results, each containing
          'id', 'value', 'line', 'lineNumber', and 'formatted' fields
        - pagination (Dict): Pagination metadata including 'page', 'pageSize',
          'totalResults', 'totalPages', 'hasNextPage', and 'hasPreviousPage'

    Raises:
        ValueError: If query is empty or None
        TypeError: If page or pageSize are not integers
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")
    
    if page is not None and not isinstance(page, int):
        raise TypeError("Page must be an integer")
    
    if pageSize is not None and not isinstance(pageSize, int):
        raise TypeError("pageSize must be an integer")
    
    if page is None:
        page = 1
    if pageSize is None:
        pageSize = 10
    
    # Validate pagination parameters
    if page < 1:
        raise ValueError("Page must be at least 1")
    if pageSize < 1:
        raise ValueError("pageSize must be at least 1")
    
    # Call external API to get flat data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_iftypes", **locals())
    
    # Construct results list from indexed fields
    results = [
        {
            "id": api_data["result_0_id"],
            "value": api_data["result_0_value"],
            "line": api_data["result_0_line"],
            "lineNumber": api_data["result_0_lineNumber"],
            "formatted": api_data["result_0_formatted"]
        },
        {
            "id": api_data["result_1_id"],
            "value": api_data["result_1_value"],
            "line": api_data["result_1_line"],
            "lineNumber": api_data["result_1_lineNumber"],
            "formatted": api_data["result_1_formatted"]
        }
    ]
    
    # Apply pagination logic
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]
    
    # Construct pagination metadata
    total_results = len(results)
    total_pages = max(1, (total_results + pageSize - 1) // pageSize)
    has_next_page = page < total_pages
    has_previous_page = page > 1
    
    # Ensure page number is within valid range
    current_page = min(page, total_pages) if total_pages > 0 else 1
    
    pagination = {
        "page": current_page,
        "pageSize": pageSize,
        "totalResults": total_results,
        "totalPages": total_pages,
        "hasNextPage": has_next_page,
        "hasPreviousPage": has_previousPage
    }
    
    return {
        "results": paginated_results,
        "pagination": pagination
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
