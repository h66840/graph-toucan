from typing import Dict, List, Any, Optional
from datetime import datetime
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for web search using Exa AI.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - request_id (str): Unique identifier for the search request
        - autoprompt_string (str): Processed version of the search query
        - auto_date (str): ISO formatted date string when search was performed
        - resolved_search_type (str): Type of search algorithm used
        - search_time (float): Time taken to perform the search in milliseconds
        - cost_dollars_total (float): Total cost in dollars
        - cost_dollars_search (float): Cost for search component in dollars
        - cost_dollars_contents (float): Cost for content retrieval in dollars
        - result_0_id (str): ID of first result
        - result_0_title (str): Title of first result
        - result_0_url (str): URL of first result
        - result_0_published_date (str): Published date of first result
        - result_0_author (str): Author of first result
        - result_0_text (str): Text content of first result
        - result_0_image (str): Image URL of first result
        - result_0_favicon (str): Favicon URL of first result
        - result_1_id (str): ID of second result
        - result_1_title (str): Title of second result
        - result_1_url (str): URL of second result
        - result_1_published_date (str): Published date of second result
        - result_1_author (str): Author of second result
        - result_1_text (str): Text content of second result
        - result_1_image (str): Image URL of second result
        - result_1_favicon (str): Favicon URL of second result
    """
    now_iso = datetime.utcnow().isoformat() + "Z"
    return {
        "request_id": f"req_{random.randint(100000, 999999)}",
        "autoprompt_string": "best practices for Python programming",
        "auto_date": now_iso,
        "resolved_search_type": "neural",
        "search_time": round(random.uniform(100.0, 500.0), 2),
        "cost_dollars_total": round(random.uniform(0.01, 0.05), 4),
        "cost_dollars_search": round(random.uniform(0.005, 0.02), 4),
        "cost_dollars_contents": round(random.uniform(0.005, 0.03), 4),
        "result_0_id": "res_001",
        "result_0_title": "Python Best Practices: A Complete Guide",
        "result_0_url": "https://example.com/python-best-practices",
        "result_0_published_date": "2023-10-15T08:00:00Z",
        "result_0_author": "John Doe",
        "result_0_text": "This guide covers the most important best practices in Python development including code style, testing, and performance optimization.",
        "result_0_image": "https://example.com/images/python-guide.jpg",
        "result_0_favicon": "https://example.com/favicon.ico",
        "result_1_id": "res_002",
        "result_1_title": "Top 10 Python Tips Every Developer Should Know",
        "result_1_url": "https://example.org/python-tips",
        "result_1_published_date": "2023-09-22T12:30:00Z",
        "result_1_author": "Jane Smith",
        "result_1_text": "Discover the top 10 tips that will improve your Python coding skills and make your programs more efficient and readable.",
        "result_1_image": "https://example.org/images/python-tips.jpg",
        "result_1_favicon": "https://example.org/favicon.ico",
    }


def exa_search_web_search_exa(query: str, numResults: Optional[int] = 5) -> Dict[str, Any]:
    """
    Search the web using Exa AI - performs real-time web searches and can scrape content from specific URLs.
    Supports configurable result counts and returns the content from the most relevant websites.

    Args:
        query (str): Search query (required)
        numResults (int, optional): Number of search results to return (default: 5)

    Returns:
        Dict containing:
        - requestId (str): unique identifier for the search request
        - autopromptString (str): the processed version of the search query used by the system
        - autoDate (str): ISO formatted date string representing when the search was performed
        - resolvedSearchType (str): type of search algorithm used (e.g., "neural")
        - searchTime (float): time taken to perform the search in milliseconds
        - costDollars (Dict): contains cost breakdown with 'total' and nested 'search' and 'contents' fields indicating dollar costs
        - results (List[Dict]): list of search result items, each containing 'id', 'title', 'url', 'publishedDate', 'author', 'text', 'image', and 'favicon' fields

    Raises:
        ValueError: If query is empty or not a string
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")

    if numResults is None:
        numResults = 5

    # Fetch simulated external data
    api_data = call_external_api("exa-search-web_search_exa")

    # Construct cost dictionary
    cost_dollars = {
        "total": api_data["cost_dollars_total"],
        "search": api_data["cost_dollars_search"],
        "contents": api_data["cost_dollars_contents"],
    }

    # Construct results list with up to numResults items (using 2 simulated results)
    max_results = min(numResults, 2)  # We only have 2 simulated results
    results = []
    for i in range(max_results):
        result_data = {
            "id": api_data[f"result_{i}_id"],
            "title": api_data[f"result_{i}_title"],
            "url": api_data[f"result_{i}_url"],
            "publishedDate": api_data[f"result_{i}_published_date"],
            "author": api_data[f"result_{i}_author"],
            "text": api_data[f"result_{i}_text"],
            "image": api_data[f"result_{i}_image"],
            "favicon": api_data[f"result_{i}_favicon"],
        }
        results.append(result_data)

    # Construct final response
    response = {
        "requestId": api_data["request_id"],
        "autopromptString": api_data["autoprompt_string"],
        "autoDate": api_data["auto_date"],
        "resolvedSearchType": api_data["resolved_search_type"],
        "searchTime": api_data["search_time"],
        "costDollars": cost_dollars,
        "results": results,
    }

    return response