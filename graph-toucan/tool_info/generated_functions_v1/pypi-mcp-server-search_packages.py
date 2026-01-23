from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PyPI package search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_name (str): Name of the first matching package
        - result_0_version (str): Version of the first package
        - result_0_summary (str): Summary description of the first package
        - result_0_author (str): Author of the first package
        - result_0_license (str): License type of the first package
        - result_0_homepage (str): Homepage URL of the first package
        - result_1_name (str): Name of the second matching package
        - result_1_version (str): Version of the second package
        - result_1_summary (str): Summary description of the second package
        - result_1_author (str): Author of the second package
        - result_1_license (str): License type of the second package
        - result_1_homepage (str): Homepage URL of the second package
        - total_count (int): Total number of packages found matching the query
    """
    return {
        "result_0_name": "requests",
        "result_0_version": "2.31.0",
        "result_0_summary": "A simple, yet elegant HTTP library.",
        "result_0_author": "Kenneth Reitz",
        "result_0_license": "Apache 2.0",
        "result_0_homepage": "https://requests.readthedocs.io",
        "result_1_name": "numpy",
        "result_1_version": "1.24.3",
        "result_1_summary": "Fundamental package for array computing in Python.",
        "result_1_author": "Travis E. Oliphant et al.",
        "result_1_license": "BSD-3-Clause",
        "result_1_homepage": "https://numpy.org",
        "total_count": 2
    }

def pypi_mcp_server_search_packages(query: str) -> Dict[str, Any]:
    """
    Searches PyPI packages based on a text query and returns package metadata.
    
    Args:
        query (str): Search query string to match against package names, summaries, or metadata
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of package entries with keys 'name', 'version', 'summary',
          'author', 'license', and 'homepage'
        - total_count (int): Total number of packages found matching the query
        
    Raises:
        ValueError: If query is empty or not a string
    """
    if not isinstance(query, str):
        raise ValueError("Query must be a string")
    if not query.strip():
        raise ValueError("Query cannot be empty")
    
    # Call external API to get flattened data
    api_data = call_external_api("pypi-mcp-server-search_packages")
    
    # Construct results list from indexed fields
    results = [
        {
            "name": api_data["result_0_name"],
            "version": api_data["result_0_version"],
            "summary": api_data["result_0_summary"],
            "author": api_data["result_0_author"],
            "license": api_data["result_0_license"],
            "homepage": api_data["result_0_homepage"]
        },
        {
            "name": api_data["result_1_name"],
            "version": api_data["result_1_version"],
            "summary": api_data["result_1_summary"],
            "author": api_data["result_1_author"],
            "license": api_data["result_1_license"],
            "homepage": api_data["result_1_homepage"]
        }
    ]
    
    # Return structured response matching output schema
    return {
        "results": results,
        "total_count": api_data["total_count"]
    }