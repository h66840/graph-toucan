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
    Simulates fetching data from external API for Old School RuneScape varbittypes search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matching varbit
        - result_0_value (str): Value of the first matching varbit
        - result_0_line (str): Full line text of the first matching varbit
        - result_0_lineNumber (int): Line number in the file for the first match
        - result_0_formatted (str): Formatted representation of the first varbit
        - result_1_id (int): ID of the second matching varbit
        - result_1_value (str): Value of the second matching varbit
        - result_1_line (str): Full line text of the second matching varbit
        - result_1_lineNumber (int): Line number in the file for the second match
        - result_1_formatted (str): Formatted representation of the second varbit
        - pagination_page (int): Current page number
        - pagination_pageSize (int): Number of results per page
        - pagination_totalResults (int): Total number of matching results
        - pagination_totalPages (int): Total number of pages
        - pagination_hasNextPage (bool): Whether a next page exists
        - pagination_hasPreviousPage (bool): Whether a previous page exists
    """
    return {
        "result_0_id": 1001,
        "result_0_value": "1",
        "result_0_line": "varbit 1001 100 0 1",
        "result_0_lineNumber": 45,
        "result_0_formatted": "Varbit 1001: stores bit 0-0 from varp 100",
        "result_1_id": 1002,
        "result_1_value": "2",
        "result_1_line": "varbit 1002 101 0 1",
        "result_1_lineNumber": 46,
        "result_1_formatted": "Varbit 1002: stores bit 0-0 from varp 101",
        "pagination_page": 1,
        "pagination_pageSize": 10,
        "pagination_totalResults": 25,
        "pagination_totalPages": 3,
        "pagination_hasNextPage": True,
        "pagination_hasPreviousPage": False
    }

def old_school_runescape_wiki_and_data_server_search_varbittypes(
    query: str,
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the varbittypes.txt file for variable bits (varbits) that store individual bits from varps.
    
    Args:
        query (str): The term to search for in the file (required)
        page (int, optional): Page number for pagination (default: 1)
        pageSize (int, optional): Number of results per page (default: 10)
    
    Returns:
        Dict containing:
        - results (List[Dict]): list of varbit entries matching the query, each containing 
          'id', 'value', 'line', 'lineNumber', and 'formatted' fields
        - pagination (Dict): contains pagination metadata including 'page', 'pageSize', 
          'totalResults', 'totalPages', 'hasNextPage', and 'hasPreviousPage'
    
    Raises:
        ValueError: If query is empty or None
        TypeError: If page or pageSize are not integers
    """
    # Input validation
    if not query or not isinstance(query, str):
        raise ValueError("Query parameter is required and must be a non-empty string")
    
    if page is not None:
        if not isinstance(page, int):
            raise TypeError("Page must be an integer")
        if page < 1:
            raise ValueError("Page must be a positive integer")
    
    if pageSize is not None:
        if not isinstance(pageSize, int):
            raise TypeError("PageSize must be an integer")
        if pageSize < 1:
            raise ValueError("PageSize must be a positive integer")
    
    # Use defaults if parameters are None
    page = page if page is not None else 1
    pageSize = pageSize if pageSize is not None else 10
    
    # Call external API to get data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_varbittypes", **locals())
    
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
    
    # Construct pagination object
    pagination = {
        "page": api_data["pagination_page"],
        "pageSize": api_data["pagination_pageSize"],
        "totalResults": api_data["pagination_totalResults"],
        "totalPages": api_data["pagination_totalPages"],
        "hasNextPage": api_data["pagination_hasNextPage"],
        "hasPreviousPage": api_data["pagination_hasPreviousPage"]
    }
    
    # Apply pagination to results (slice based on page and pageSize)
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]
    
    # Adjust pagination metadata based on current page and results
    total_results = len(results)
    total_pages = max(1, (total_results + pageSize - 1) // pageSize)
    
    pagination["page"] = page
    pagination["pageSize"] = pageSize
    pagination["totalResults"] = total_results
    pagination["totalPages"] = total_pages
    pagination["hasNextPage"] = page < total_pages
    pagination["hasPreviousPage"] = page > 1
    
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
