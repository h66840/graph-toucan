from typing import Dict, List, Any, Optional
import random
import time

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
    Simulates fetching data from external API for Old School RuneScape soundtypes search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matching sound effect
        - result_0_name (str): Name of the first sound effect
        - result_0_description (str): Description of the first sound effect
        - result_0_file_path (str): File path of the first sound effect
        - result_0_category (str): Category of the first sound effect
        - result_0_parameters (str): Parameters of the first sound effect (as JSON string)
        - result_1_id (int): ID of the second matching sound effect
        - result_1_name (str): Name of the second sound effect
        - result_1_description (str): Description of the second sound effect
        - result_1_file_path (str): File path of the second sound effect
        - result_1_category (str): Category of the second sound effect
        - result_1_parameters (str): Parameters of the second sound effect (as JSON string)
        - total_count (int): Total number of matching sound effects
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more results exist beyond this page
        - query_time_ms (int): Time taken for the query in milliseconds
        - indexed_version (str): Version of the indexed data
        - source_file (str): Name of the source file
    """
    # Simulate realistic delay
    time.sleep(0.1)
    
    return {
        "result_0_id": 1024,
        "result_0_name": "door_creak",
        "result_0_description": "A rusty door slowly opening",
        "result_0_file_path": "/sounds/environment/door_creak.wav",
        "result_0_category": "environment",
        "result_0_parameters": '{"volume": 0.8, "pitch": 0.95, "loop": false}',
        
        "result_1_id": 2048,
        "result_1_name": "sword_swing",
        "result_1_description": "Metallic swoosh of a sword cutting through air",
        "result_1_file_path": "/sounds/combat/sword_swing_01.wav",
        "result_1_category": "combat",
        "result_1_parameters": '{"volume": 0.7, "pitch": 1.0, "loop": false}',
        
        "total_count": 42,
        "page": 1,
        "page_size": 2,
        "has_more": True,
        "query_time_ms": 134,
        "indexed_version": "2023.10.05",
        "source_file": "soundtypes.txt"
    }


def old_school_runescape_wiki_and_data_server_search_soundtypes(
    query: str, 
    page: Optional[int] = 1, 
    pageSize: Optional[int] = 2
) -> Dict[str, Any]:
    """
    Search the soundtypes.txt file for sound effect definitions in Old School RuneScape.

    Args:
        query (str): The term to search for in the soundtypes file (required)
        page (int, optional): Page number for pagination (default: 1)
        pageSize (int, optional): Number of results per page (default: 2)

    Returns:
        Dict containing:
        - results (List[Dict]): List of sound effect definitions with fields: 
            id (int), name (str), description (str), file_path (str), 
            category (str), parameters (Dict)
        - total_count (int): Total number of matching sound effects
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more results are available
        - metadata (Dict): Additional info including query_time_ms (int), 
            indexed_version (str), source_file (str)

    Raises:
        ValueError: If query is empty or None
        ValueError: If page or pageSize is less than 1
    """
    # Input validation
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty")
    
    if page is not None and page < 1:
        raise ValueError("Page number must be at least 1")
    
    if pageSize is not None and pageSize < 1:
        raise ValueError("Page size must be at least 1")
    
    # Set defaults if None
    page = page if page is not None else 1
    pageSize = pageSize if pageSize is not None else 2
    
    # Call external API (simulated)
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_soundtypes", **locals())
    
    # Construct results list from flattened API response
    results = []
    
    for i in range(2):  # We have 2 results from API
        result_key = f"result_{i}_id"
        if result_key not in api_data:
            continue
            
        try:
            import json
            parameters = json.loads(api_data[f"result_{i}_parameters"])
        except:
            parameters = {}
            
        result = {
            "id": api_data[f"result_{i}_id"],
            "name": api_data[f"result_{i}_name"],
            "description": api_data[f"result_{i}_description"],
            "file_path": api_data[f"result_{i}_file_path"],
            "category": api_data[f"result_{i}_category"],
            "parameters": parameters
        }
        results.append(result)
    
    # Construct final response matching output schema
    response = {
        "results": results,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "page_size": api_data["page_size"],
        "has_more": api_data["has_more"],
        "metadata": {
            "query_time_ms": api_data["query_time_ms"],
            "indexed_version": api_data["indexed_version"],
            "source_file": api_data["source_file"]
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
