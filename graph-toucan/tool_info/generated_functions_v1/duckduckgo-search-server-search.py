from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DuckDuckGo search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_occurred (bool): Indicates whether an error occurred during search
        - error_message (str): Detailed message explaining the failure
        - result_0_title (str): Title of the first search result
        - result_0_url (str): URL of the first search result
        - result_0_snippet (str): Snippet of the first search result
        - result_1_title (str): Title of the second search result
        - result_1_url (str): URL of the second search result
        - result_1_snippet (str): Snippet of the second search result
    """
    return {
        "error_occurred": False,
        "error_message": "",
        "result_0_title": "Python Programming Language - Official Website",
        "result_0_url": "https://www.python.org",
        "result_0_snippet": "Official website for the Python programming language. Download, documentation, and community resources.",
        "result_1_title": "Python Tutorial - W3Schools",
        "result_1_url": "https://www.w3schools.com/python",
        "result_1_snippet": "Learn Python with examples. W3Schools provides tutorials and references for Python syntax, functions, and modules."
    }

def duckduckgo_search_server_search(query: str, max_results: Optional[int] = 10) -> Dict[str, Any]:
    """
    Search DuckDuckGo and return formatted results.

    Args:
        query (str): The search query string
        max_results (int, optional): Maximum number of results to return (default: 10)

    Returns:
        Dict containing:
        - error_occurred (bool): indicates whether an error or no results were encountered during the search
        - error_message (str): detailed message explaining the failure, such as bot detection or no matches found
        - results (List[Dict]): list of search results with title, url, and snippet
    """
    if not query or not query.strip():
        return {
            "error_occurred": True,
            "error_message": "Search query cannot be empty"
        }

    # Call external API to simulate search
    api_data = call_external_api("duckduckgo-search-server-search")

    # Extract simple fields and construct nested structure
    error_occurred = api_data["error_occurred"]
    error_message = api_data["error_message"]

    if error_occurred:
        return {
            "error_occurred": True,
            "error_message": error_message
        }

    # Construct results list from indexed fields
    results = []
    num_results = min(max_results or 10, 2)  # Simulate only 2 available results

    for i in range(num_results):
        title_key = f"result_{i}_title"
        url_key = f"result_{i}_url"
        snippet_key = f"result_{i}_snippet"

        if title_key in api_data and api_data[title_key]:
            results.append({
                "title": api_data[title_key],
                "url": api_data[url_key],
                "snippet": api_data[snippet_key]
            })

    return {
        "error_occurred": False,
        "error_message": "",
        "results": results
    }