from typing import Dict, List, Any, Optional
import random
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
    Simulates fetching data from external API for Old School RuneScape spritetypes search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matching sprite type
        - result_0_name (str): Name of the first sprite type
        - result_0_file (str): File path of the first sprite image
        - result_0_index (int): Index within the file for the first sprite
        - result_0_description (str): Description of the first sprite
        - result_1_id (int): ID of the second matching sprite type
        - result_1_name (str): Name of the second sprite type
        - result_1_file (str): File path of the second sprite image
        - result_1_index (int): Index within the file for the second sprite
        - result_1_description (str): Description of the second sprite
        - total_count (int): Total number of matching sprite entries
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more results exist beyond this page
        - query (str): The search query used
        - metadata_timestamp (str): ISO format timestamp of the request
        - metadata_source_version (str): Version/revision of spritetypes.txt
        - metadata_file_size (int): Size of the source file in bytes
    """
    return {
        "result_0_id": 1024,
        "result_0_name": "Combat Tab",
        "result_0_file": "interface/combat.tab",
        "result_0_index": 0,
        "result_0_description": "Combat interface tab icon",
        "result_1_id": 1025,
        "result_1_name": "Skills Tab",
        "result_1_file": "interface/skills.tab",
        "result_1_index": 1,
        "result_1_description": "Skills interface tab icon",
        "total_count": 2,
        "page": 1,
        "page_size": 10,
        "has_more": False,
        "query": "tab",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_source_version": "rev-385",
        "metadata_file_size": 20480
    }


def old_school_runescape_wiki_and_data_server_search_spritetypes(
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10,
    query: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search the spritetypes.txt file for sprite image definitions used in the interface.

    Args:
        page (int, optional): Page number for pagination (default: 1)
        pageSize (int, optional): Number of results per page (default: 10)
        query (str, required): The term to search for in the file

    Returns:
        Dict containing:
        - results (List[Dict]): List of sprite type entries matching the query
        - total_count (int): Total number of matching entries
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more results are available
        - query (str): The search query used
        - metadata (Dict): Additional info about the search operation

    Raises:
        ValueError: If query is None or empty
    """
    if not query:
        raise ValueError("Query parameter is required")

    if page is None:
        page = 1
    if pageSize is None:
        pageSize = 10

    if page < 1:
        page = 1
    if pageSize < 1:
        pageSize = 10

    # Call external API to get flattened data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_spritetypes", **locals())

    # Construct results list from indexed fields
    results = [
        {
            "id": api_data["result_0_id"],
            "name": api_data["result_0_name"],
            "file": api_data["result_0_file"],
            "index": api_data["result_0_index"],
            "description": api_data["result_0_description"]
        },
        {
            "id": api_data["result_1_id"],
            "name": api_data["result_1_name"],
            "file": api_data["result_1_file"],
            "index": api_data["result_1_index"],
            "description": api_data["result_1_description"]
        }
    ]

    # Apply pagination
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]

    # Determine if there are more results
    has_more = end_idx < api_data["total_count"]

    # Construct final response
    response = {
        "results": paginated_results,
        "total_count": api_data["total_count"],
        "page": page,
        "page_size": pageSize,
        "has_more": has_more,
        "query": api_data["query"],
        "metadata": {
            "timestamp": api_data["metadata_timestamp"],
            "source_version": api_data["metadata_source_version"],
            "file_size": api_data["metadata_file_size"]
        }
    }

    return response

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
