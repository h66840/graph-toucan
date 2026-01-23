from typing import Dict, List, Any, Optional
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
    Simulates fetching data from external API for Old School RuneScape wiki and data server.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matching entry
        - result_0_name (str): Name of the first matching entry
        - result_0_value (str): Value of the first matching entry
        - result_1_id (int): ID of the second matching entry
        - result_1_name (str): Name of the second matching entry
        - result_1_value (str): Value of the second matching entry
        - total_count (int): Total number of matching entries found
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more results exist beyond current page
        - metadata_filename (str): The filename that was searched
        - metadata_query_timestamp (str): ISO format timestamp of the query
        - metadata_file_format (str): Format type of the data file (e.g., 'text/plain')
    """
    return {
        "result_0_id": 12345,
        "result_0_name": "Fire Battlestaff",
        "result_0_value": "200000",
        "result_1_id": 67890,
        "result_1_name": "Mystic Fire Staff",
        "result_1_value": "150000",
        "total_count": 2,
        "page": 1,
        "page_size": 10,
        "has_more": False,
        "metadata_filename": "varptypes.txt",
        "metadata_query_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_file_format": "text/plain"
    }


def old_school_runescape_wiki_and_data_server_search_data_file(
    filename: str,
    query: str,
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search any file in the data directory for matching entries.

    Args:
        filename (str): The filename to search in the data directory (e.g., 'varptypes.txt')
        query (str): The term to search for in the file
        page (Optional[int]): Page number for pagination (default: 1)
        pageSize (Optional[int]): Number of results per page (default: 10)

    Returns:
        Dict containing:
        - results (List[Dict]): List of matching entries with fields like 'id', 'name', 'value'
        - total_count (int): Total number of matching entries found across all pages
        - page (int): Current page number in the paginated result set
        - page_size (int): Number of results returned per page
        - has_more (bool): Indicates whether there are additional results available
        - metadata (Dict): Additional contextual information including filename, timestamp, and format

    Raises:
        ValueError: If filename or query is empty
    """
    if not filename:
        raise ValueError("filename is required")
    if not query:
        raise ValueError("query is required")
    if page is None:
        page = 1
    if pageSize is None:
        pageSize = 10

    # Call external API to get flattened data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_data_file", **locals())

    # Construct results list from indexed fields
    results = [
        {
            "id": api_data["result_0_id"],
            "name": api_data["result_0_name"],
            "value": api_data["result_0_value"]
        },
        {
            "id": api_data["result_1_id"],
            "name": api_data["result_1_name"],
            "value": api_data["result_1_value"]
        }
    ]

    # Apply pagination
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]

    # Construct metadata
    metadata = {
        "filename": api_data["metadata_filename"],
        "query_timestamp": api_data["metadata_query_timestamp"],
        "file_format": api_data["metadata_file_format"]
    }

    # Return full response structure
    return {
        "results": paginated_results,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "page_size": api_data["page_size"],
        "has_more": api_data["has_more"],
        "metadata": metadata
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
