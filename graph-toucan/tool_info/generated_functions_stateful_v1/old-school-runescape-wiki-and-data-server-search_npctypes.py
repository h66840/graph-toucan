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
    Simulates fetching data from external API for NPC types search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): ID of first matching NPC
        - result_0_name (str): Name of first matching NPC
        - result_0_combat_level (int): Combat level of first NPC
        - result_0_hitpoints (int): Hitpoints of first NPC
        - result_0_attackable (bool): Whether first NPC is attackable
        - result_0_aggressive (bool): Whether first NPC is aggressive
        - result_0_poisonous (bool): Whether first NPC is poisonous
        - result_1_id (int): ID of second matching NPC
        - result_1_name (str): Name of second matching NPC
        - result_1_combat_level (int): Combat level of second NPC
        - result_1_hitpoints (int): Hitpoints of second NPC
        - result_1_attackable (bool): Whether second NPC is attackable
        - result_1_aggressive (bool): Whether second NPC is aggressive
        - result_1_poisonous (bool): Whether second NPC is poisonous
        - total_count (int): Total number of matching NPCs
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more results exist beyond current page
        - metadata_timestamp (str): ISO format timestamp of data
        - metadata_source_version (str): Version of source data file
        - metadata_warning (str): Warning message if applicable
    """
    return {
        "result_0_id": 1234,
        "result_0_name": "Goblin",
        "result_0_combat_level": 2,
        "result_0_hitpoints": 10,
        "result_0_attackable": True,
        "result_0_aggressive": False,
        "result_0_poisonous": False,
        "result_1_id": 1235,
        "result_1_name": "Hill Giant",
        "result_1_combat_level": 15,
        "result_1_hitpoints": 45,
        "result_1_attackable": True,
        "result_1_aggressive": True,
        "result_1_poisonous": False,
        "total_count": 2,
        "page": 1,
        "page_size": 10,
        "has_more": False,
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_source_version": "2023.09",
        "metadata_warning": "Query matched multiple entries; results may vary."
    }


def old_school_runescape_wiki_and_data_server_search_npctypes(
    query: str,
    page: Optional[int] = 1,
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the npctypes.txt file for NPC (non-player character) definitions.

    Args:
        query (str): The term to search for in the file (required)
        page (int, optional): Page number for pagination (default: 1)
        pageSize (int, optional): Number of results per page (default: 10)

    Returns:
        Dict containing:
        - results (List[Dict]): List of NPC entries matching the query
        - total_count (int): Total number of matching NPC entries
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more results are available
        - metadata (Dict): Additional information about the search

    Raises:
        ValueError: If query is empty or None
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty")

    # Validate and sanitize inputs
    page = max(1, page or 1)
    pageSize = max(1, min(100, pageSize or 10))  # Limit page size between 1 and 100

    # Call external API to get flat data
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_npctypes", **locals())

    # Extract results from flat data into structured list
    results = []
    for i in range(2):  # We have two results from the API
        result_key = f"result_{i}_name"
        if result_key in api_data and api_data[result_key]:
            npc = {
                "id": api_data[f"result_{i}_id"],
                "name": api_data[f"result_{i}_name"],
                "combat_level": api_data[f"result_{i}_combat_level"],
                "hitpoints": api_data[f"result_{i}_hitpoints"],
                "attackable": api_data[f"result_{i}_attackable"],
                "aggressive": api_data[f"result_{i}_aggressive"],
                "poisonous": api_data[f"result_{i}_poisonous"]
            }
            results.append(npc)

    # Apply pagination
    start_idx = (page - 1) * pageSize
    end_idx = start_idx + pageSize
    paginated_results = results[start_idx:end_idx]

    # Determine if there are more results
    has_more = end_idx < len(results)

    # Construct final response
    response = {
        "results": paginated_results,
        "total_count": api_data["total_count"],
        "page": page,
        "page_size": pageSize,
        "has_more": has_more,
        "metadata": {
            "timestamp": api_data["metadata_timestamp"],
            "source_version": api_data["metadata_source_version"],
            "warning": api_data["metadata_warning"]
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
