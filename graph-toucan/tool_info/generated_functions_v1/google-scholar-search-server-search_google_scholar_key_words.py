from typing import Dict, List, Any, Optional
import random
import string
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Scholar search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first search result
        - result_0_authors (str): Authors of the first result
        - result_0_publication_year (int): Publication year of the first result
        - result_0_journal (str): Journal name of the first result
        - result_0_cited_count (int): Number of citations for the first result
        - result_0_link (str): URL link to the first result
        - result_1_title (str): Title of the second search result
        - result_1_authors (str): Authors of the second result
        - result_1_publication_year (int): Publication year of the second result
        - result_1_journal (str): Journal name of the second result
        - result_1_cited_count (int): Number of citations for the second result
        - result_1_link (str): URL link to the second result
        - total_results_found (int): Total number of scholarly results found
        - query_time (str): Timestamp when the query was executed
        - next_page_token (str): Token to retrieve the next page of results
    """
    return {
        "result_0_title": "Advancements in Machine Learning for Natural Language Processing",
        "result_0_authors": "A. Smith, B. Johnson, C. Lee",
        "result_0_publication_year": 2022,
        "result_0_journal": "Journal of Artificial Intelligence Research",
        "result_0_cited_count": 145,
        "result_0_link": "https://scholar.google.com/scholar_article1",
        "result_1_title": "Deep Learning Approaches to Text Classification",
        "result_1_authors": "D. Wang, E. Brown",
        "result_1_publication_year": 2021,
        "result_1_journal": "Neural Networks Quarterly",
        "result_1_cited_count": 89,
        "result_1_link": "https://scholar.google.com/scholar_article2",
        "total_results_found": 1240,
        "query_time": datetime.now().isoformat(),
        "next_page_token": "next_page_abc123xyz"
    }


def google_scholar_search_server_search_google_scholar_key_words(
    query: str,
    num_results: Optional[int] = None
) -> Dict[str, Any]:
    """
    Performs a Google Scholar search based on provided keywords.

    Args:
        query (str): The search query string (required).
        num_results (Optional[int]): The number of results to return (optional, default is 2).

    Returns:
        Dict containing:
            - results (List[Dict]): List of search results with keys 'title', 'authors',
              'publication_year', 'journal', 'cited_count', 'link'
            - total_results_found (int): Total number of scholarly results found
            - query_time (str): ISO format timestamp indicating when the query was executed
            - next_page_token (str): Token for retrieving the next page of results

    Raises:
        ValueError: If query is empty or None.
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty.")

    # Default to 2 results if num_results is not specified or invalid
    if num_results is None or num_results <= 0:
        num_results = 2

    # Fetch simulated external data
    api_data = call_external_api("google-scholar-search-server-search_google_scholar_key_words")

    # Construct results list with up to num_results entries (max 2 available)
    results = []
    for i in range(min(num_results, 2)):
        result = {
            "title": api_data[f"result_{i}_title"],
            "authors": api_data[f"result_{i}_authors"],
            "publication_year": api_data[f"result_{i}_publication_year"],
            "journal": api_data[f"result_{i}_journal"],
            "cited_count": api_data[f"result_{i}_cited_count"],
            "link": api_data[f"result_{i}_link"]
        }
        results.append(result)

    # Return structured response matching output schema
    return {
        "results": results,
        "total_results_found": api_data["total_results_found"],
        "query_time": api_data["query_time"],
        "next_page_token": api_data["next_page_token"]
    }