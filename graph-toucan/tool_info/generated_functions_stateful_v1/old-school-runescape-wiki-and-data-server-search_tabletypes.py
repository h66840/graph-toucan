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
    Simulates fetching data from external API for Old School RuneScape wiki and data server.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_interface_id (int): Interface ID of the first matching tabletype entry
        - result_0_component_id (int): Component ID of the first entry
        - result_0_type (str): Type of the first entry (e.g., 'container', 'text')
        - result_0_metadata_description (str): Description metadata for the first entry
        - result_0_metadata_file_version (str): File version associated with the first entry
        - result_1_interface_id (int): Interface ID of the second matching tabletype entry
        - result_1_component_id (int): Component ID of the second entry
        - result_1_type (str): Type of the second entry
        - result_1_metadata_description (str): Description metadata for the second entry
        - result_1_metadata_file_version (str): File version associated with the second entry
        - total_count (int): Total number of matching entries in the tabletypes.txt file
        - page (int): Current page number in the paginated result set
        - page_size (int): Number of results per page
        - has_more (bool): Whether more pages exist beyond the current one
        - metadata_timestamp (str): Timestamp of when the data was last updated
        - metadata_source_version (str): Version of the source file (e.g., 'rev159')
        - metadata_warning (str): Any warning message related to the search or data
    """
    return {
        "result_0_interface_id": 1234,
        "result_0_component_id": 5,
        "result_0_type": "container",
        "result_0_metadata_description": "Inventory container for player interface",
        "result_0_metadata_file_version": "rev159",
        "result_1_interface_id": 1235,
        "result_1_component_id": 0,
        "result_1_type": "text",
        "result_1_metadata_description": "Player name display text",
        "result_1_metadata_file_version": "rev159",
        "total_count": 42,
        "page": 1,
        "page_size": 2,
        "has_more": True,
        "metadata_timestamp": "2023-11-15T08:30:00Z",
        "metadata_source_version": "rev159",
        "metadata_warning": "Query returned partial results; consider refining search."
    }

def old_school_runescape_wiki_and_data_server_search_tabletypes(
    query: str,
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the tabletypes.txt file for interface tab definitions.

    Args:
        query (str): The term to search for in the file (required)
        page (int, optional): Page number for pagination (default: 1)
        pageSize (int, optional): Number of results per page (default: 10)

    Returns:
        Dict containing:
        - results (List[Dict]): List of matching tabletype entries with interface tab definition details
        - total_count (int): Total number of matching entries regardless of pagination
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether additional pages are available
        - metadata (Dict): Contextual information including timestamp, source version, and warnings

    Raises:
        ValueError: If query is empty or None
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")

    # Normalize page and pageSize values
    page = max(1, page or 1)
    pageSize = max(1, pageSize or 10)

    # Fetch simulated external data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_tabletypes", **locals())

    # Construct results list from indexed fields
    results = [
        {
            "interface_id": api_data["result_0_interface_id"],
            "component_id": api_data["result_0_component_id"],
            "type": api_data["result_0_type"],
            "metadata": {
                "description": api_data["result_0_metadata_description"],
                "file_version": api_data["result_0_metadata_file_version"]
            }
        },
        {
            "interface_id": api_data["result_1_interface_id"],
            "component_id": api_data["result_1_component_id"],
            "type": api_data["result_1_type"],
            "metadata": {
                "description": api_data["result_1_metadata_description"],
                "file_version": api_data["result_1_metadata_file_version"]
            }
        }
    ]

    # Apply pagination logic
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]

    # Determine if there are more pages
    total_count = api_data["total_count"]
    has_more = end_idx < total_count

    # Construct final response
    return {
        "results": paginated_results,
        "total_count": total_count,
        "page": page,
        "page_size": pageSize,
        "has_more": has_more,
        "metadata": {
            "timestamp": api_data["metadata_timestamp"],
            "source_version": api_data["metadata_source_version"],
            "warning": api_data["metadata_warning"]
        }
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
