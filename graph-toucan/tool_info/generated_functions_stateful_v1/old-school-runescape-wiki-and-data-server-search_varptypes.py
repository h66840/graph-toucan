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
    Simulates fetching data from external API for Old School RuneScape varptypes search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_line (str): Line content of first matching varp entry
        - result_0_lineNumber (int): Line number of first match
        - result_0_id (int): ID of first varp
        - result_0_value (str): Value of first varp
        - result_0_formatted (str): Formatted string of first varp
        - result_1_line (str): Line content of second matching varp entry
        - result_1_lineNumber (int): Line number of second match
        - result_1_id (int): ID of second varp
        - result_1_value (str): Value of second varp
        - result_1_formatted (str): Formatted string of second varp
        - pagination_page (int): Current page number
        - pagination_pageSize (int): Number of results per page
        - pagination_totalResults (int): Total number of matching results
        - pagination_totalPages (int): Total number of pages
        - pagination_hasNextPage (bool): Whether a next page exists
        - pagination_hasPreviousPage (bool): Whether a previous page exists
    """
    return {
        "result_0_line": "varp 1000=1 // player combat level",
        "result_0_lineNumber": 1000,
        "result_0_id": 1000,
        "result_0_value": "1",
        "result_0_formatted": "Varp ID: 1000, Value: 1 (combat level)",
        "result_1_line": "varp 1001=0 // player skilling level",
        "result_1_lineNumber": 1001,
        "result_1_id": 1001,
        "result_1_value": "0",
        "result_1_formatted": "Varp ID: 1001, Value: 0 (skilling level)",
        "pagination_page": 1,
        "pagination_pageSize": 10,
        "pagination_totalResults": 2,
        "pagination_totalPages": 1,
        "pagination_hasNextPage": False,
        "pagination_hasPreviousPage": False,
    }

def old_school_runescape_wiki_and_data_server_search_varptypes(
    query: str,
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the varptypes.txt file for player variables (varps) that store player state and progress.

    Args:
        query (str): The term to search for in the file (required)
        page (int, optional): Page number for pagination. Defaults to 1.
        pageSize (int, optional): Number of results per page. Defaults to 10.

    Returns:
        Dict containing:
        - results (List[Dict]): List of varp entries matching the query, each with 'line', 'lineNumber', 'id', 'value', and 'formatted'
        - pagination (Dict): Pagination metadata including 'page', 'pageSize', 'totalResults', 'totalPages', 'hasNextPage', 'hasPreviousPage'

    Raises:
        ValueError: If query is empty or None
        ValueError: If page or pageSize are not positive integers
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")
    
    if page is not None and (not isinstance(page, int) or page < 1):
        raise ValueError("Page must be a positive integer")
    
    if pageSize is not None and (not isinstance(pageSize, int) or pageSize < 1):
        raise ValueError("pageSize must be a positive integer")
    
    # Call the external API simulation
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_varptypes", **locals())
    
    # Construct results list from indexed fields
    results = []
    for i in range(2):  # We have 2 results from the API
        line_key = f"result_{i}_line"
        lineNumber_key = f"result_{i}_lineNumber"
        id_key = f"result_{i}_id"
        value_key = f"result_{i}_value"
        formatted_key = f"result_{i}_formatted"
        
        if line_key in api_data:
            results.append({
                "line": api_data[line_key],
                "lineNumber": api_data[lineNumber_key],
                "id": api_data[id_key],
                "value": api_data[value_key],
                "formatted": api_data[formatted_key]
            })
    
    # Construct pagination object
    pagination = {
        "page": api_data["pagination_page"],
        "pageSize": api_data["pagination_pageSize"],
        "totalResults": api_data["pagination_totalResults"],
        "totalPages": api_data["pagination_totalPages"],
        "hasNextPage": api_data["pagination_hasNextPage"],
        "hasPreviousPage": api_data["pagination_hasPreviousPage"]
    }
    
    # Apply pagination if needed
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]
    
    # Update pagination metadata based on actual slicing
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
