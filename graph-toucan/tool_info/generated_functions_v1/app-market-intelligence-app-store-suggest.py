from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for App Store search suggestions.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - suggestion_0_term (str): First suggested search term
        - suggestion_0_priority (int): Priority score for the first suggestion (0-10000)
        - suggestion_1_term (str): Second suggested search term
        - suggestion_1_priority (int): Priority score for the second suggestion (0-10000)
        - total_suggestions (int): Total number of suggestions returned (2)
        - query_term (str): The original search term used to generate suggestions
        - timestamp (str): ISO 8601 timestamp indicating when the response was generated
    """
    return {
        "suggestion_0_term": "music player",
        "suggestion_0_priority": 9500,
        "suggestion_1_term": "music downloader",
        "suggestion_1_priority": 8700,
        "total_suggestions": 2,
        "query_term": "music",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }


def app_market_intelligence_app_store_suggest(term: str) -> Dict[str, Any]:
    """
    Get search suggestions from the App Store based on a given search term.

    Args:
        term (str): Search term to get suggestions for. Must be a non-empty string.

    Returns:
        Dict containing:
        - suggestions (List[Dict]): List of suggestion objects with 'term' and 'priority'
        - total_suggestions (int): Total number of suggestions returned
        - query_term (str): The original search term used
        - timestamp (str): ISO 8601 formatted timestamp of when the response was generated

    Raises:
        ValueError: If the input term is empty or not a string
    """
    if not isinstance(term, str):
        raise ValueError("Search term must be a string.")
    if not term.strip():
        raise ValueError("Search term cannot be empty or whitespace.")

    # Call the external API simulation
    api_data = call_external_api("app-market-intelligence-app-store-suggest")

    # Construct the suggestions list from flattened API response
    suggestions = [
        {
            "term": api_data["suggestion_0_term"],
            "priority": api_data["suggestion_0_priority"]
        },
        {
            "term": api_data["suggestion_1_term"],
            "priority": api_data["suggestion_1_priority"]
        }
    ]

    # Build final result matching output schema
    result = {
        "suggestions": suggestions,
        "total_suggestions": api_data["total_suggestions"],
        "query_term": api_data["query_term"],
        "timestamp": api_data["timestamp"]
    }

    return result