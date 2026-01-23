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
    Simulates fetching data from external API for NuGet package search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_name (str): Name of the first matching package
        - result_0_version (str): Version of the first package
        - result_0_description (str): Description of the first package
        - result_0_author (str): Author of the first package
        - result_0_download_count (int): Download count of the first package
        - result_0_published_date (str): Published date of the first package in ISO format
        - result_1_name (str): Name of the second matching package
        - result_1_version (str): Version of the second package
        - result_1_description (str): Description of the second package
        - result_1_author (str): Author of the second package
        - result_1_download_count (int): Download count of the second package
        - result_1_published_date (str): Published date of the second package in ISO format
        - total_count (int): Total number of packages found
        - took (int): Time in milliseconds the search took
        - incomplete_results (bool): Whether results are incomplete
        - metadata_offset (int): Pagination offset
        - metadata_limit (int): Pagination limit
        - metadata_query (str): The search query used
    """
    return {
        "result_0_name": "Newtonsoft.Json",
        "result_0_version": "13.0.3",
        "result_0_description": "A popular high-performance JSON framework for .NET",
        "result_0_author": "James Newton-King",
        "result_0_download_count": 450000000,
        "result_0_published_date": "2023-01-15T10:30:00Z",
        "result_1_name": "Microsoft.Extensions.DependencyInjection",
        "result_1_version": "7.0.0",
        "result_1_description": "Default IoC container for dependency injection",
        "result_1_author": "Microsoft",
        "result_1_download_count": 320000000,
        "result_1_published_date": "2022-11-08T09:15:00Z",
        "total_count": 2,
        "took": 45,
        "incomplete_results": False,
        "metadata_offset": 0,
        "metadata_limit": 25,
        "metadata_query": "dependency injection"
    }

def package_registry_server_search_nuget_packages(query: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Search the NuGet registry for packages based on a query string.
    
    Args:
        query (str): The search term to look for in NuGet packages (required)
        limit (Optional[int]): Maximum number of results to return (optional)
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of package objects with name, version, description, 
          author, download count, and published date
        - total_count (int): Total number of packages found matching the query
        - took (int): Time in milliseconds the search operation took
        - incomplete_results (bool): Whether the results are incomplete due to rate limiting or timeout
        - metadata (Dict): Pagination and query metadata including offset, limit, and applied filters
    
    Raises:
        ValueError: If query is empty or None
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")
    
    # Call external API to get flattened data
    api_data = call_external_api("package-registry-server-search-nuget-packages", **locals())
    
    # Construct results list from indexed fields
    results = [
        {
            "name": api_data["result_0_name"],
            "version": api_data["result_0_version"],
            "description": api_data["result_0_description"],
            "author": api_data["result_0_author"],
            "download_count": api_data["result_0_download_count"],
            "published_date": api_data["result_0_published_date"]
        },
        {
            "name": api_data["result_1_name"],
            "version": api_data["result_1_version"],
            "description": api_data["result_1_description"],
            "author": api_data["result_1_author"],
            "download_count": api_data["result_1_download_count"],
            "published_date": api_data["result_1_published_date"]
        }
    ]
    
    # Apply limit if specified
    if limit is not None and limit > 0:
        results = results[:limit]
    
    # Construct metadata
    metadata = {
        "offset": api_data["metadata_offset"],
        "limit": api_data["metadata_limit"],
        "filters": {"query": api_data["metadata_query"]}
    }
    
    # Return final structured response
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "took": api_data["took"],
        "incomplete_results": api_data["incomplete_results"],
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
