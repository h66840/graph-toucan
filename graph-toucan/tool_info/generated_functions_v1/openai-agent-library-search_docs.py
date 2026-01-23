from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for OpenAI Agents SDK documentation search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_url (str): URL of the first search result
        - result_0_title (str): Title of the first search result
        - result_0_snippet (str): Snippet of the first search result
        - result_1_url (str): URL of the second search result
        - result_1_title (str): Title of the second search result
        - result_1_snippet (str): Snippet of the second search result
        - has_results (bool): Whether any results were found
        - error_message (str): Error or informational message if no results
    """
    # Simulate realistic search results based on query (not used in this mock, but could be)
    return {
        "result_0_url": "https://github.com/openai/agents-sdk/blob/main/docs/quickstart.md",
        "result_0_title": "Quickstart Guide",
        "result_0_snippet": "Get started with the OpenAI Agents SDK by installing the package and running your first agent.",
        "result_1_url": "https://github.com/openai/agents-sdk/blob/main/docs/api-reference.md",
        "result_1_title": "API Reference",
        "result_1_snippet": "Comprehensive reference for all classes and methods available in the Agents SDK.",
        "has_results": True,
        "error_message": ""
    }

def openai_agent_library_search_docs(query: str) -> Dict[str, Any]:
    """
    Search for a specific term across OpenAI Agents SDK documentation.
    
    Args:
        query (str): The search term or phrase to look up in the documentation.
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of search result items, each with 'url', 'title', and 'snippet'
        - error_message (str): Error or informational message when no results are found
        - has_results (bool): Indicates whether the search returned any results
    """
    # Input validation
    if not query or not query.strip():
        return {
            "results": [],
            "error_message": "Query cannot be empty",
            "has_results": False
        }
    
    # Call external API simulation
    api_data = call_external_api("openai-agent-library-search_docs")
    
    # Construct results list from flattened API response
    results: List[Dict[str, str]] = []
    
    if api_data["has_results"]:
        results.append({
            "url": api_data["result_0_url"],
            "title": api_data["result_0_title"],
            "snippet": api_data["result_0_snippet"]
        })
        results.append({
            "url": api_data["result_1_url"],
            "title": api_data["result_1_title"],
            "snippet": api_data["result_1_snippet"]
        })
    
    # Build final response
    return {
        "results": results,
        "error_message": api_data["error_message"],
        "has_results": api_data["has_results"]
    }