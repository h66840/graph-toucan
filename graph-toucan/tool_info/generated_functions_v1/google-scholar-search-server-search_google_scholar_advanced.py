from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Scholar search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first search result
        - result_0_authors (str): Authors of the first search result
        - result_0_publication_year (int): Publication year of the first result
        - result_0_journal (str): Journal name of the first result
        - result_0_url (str): URL of the first result
        - result_0_snippet (str): Snippet of the first result
        - result_1_title (str): Title of the second search result
        - result_1_authors (str): Authors of the second search result
        - result_1_publication_year (int): Publication year of the second result
        - result_1_journal (str): Journal name of the second result
        - result_1_url (str): URL of the second result
        - result_1_snippet (str): Snippet of the second result
        - total_results (int): Total number of results found
        - query_used (str): The actual query string used
        - status (str): Status of the operation ('success' or 'error')
        - error_message (str): Error description if status is 'error'
    """
    return {
        "result_0_title": "Advancements in Machine Learning Techniques",
        "result_0_authors": "John Doe, Jane Smith",
        "result_0_publication_year": 2022,
        "result_0_journal": "Journal of Artificial Intelligence",
        "result_0_url": "https://example.com/paper1",
        "result_0_snippet": "This paper discusses recent advancements in machine learning models and their applications.",
        "result_1_title": "Deep Learning for Natural Language Processing",
        "result_1_authors": "Alice Johnson, Bob Lee",
        "result_1_publication_year": 2021,
        "result_1_journal": "Neural Computing Reviews",
        "result_1_url": "https://example.com/paper2",
        "result_1_snippet": "A comprehensive review of deep learning architectures applied to NLP tasks.",
        "total_results": 150,
        "query_used": "machine learning",
        "status": "success",
        "error_message": ""
    }

def google_scholar_search_server_search_google_scholar_advanced(
    query: str,
    author: Optional[str] = None,
    num_results: Optional[int] = None,
    year_range: Optional[str] = None
) -> Dict[str, Any]:
    """
    Performs an advanced search on Google Scholar using specified parameters.
    
    Args:
        query (str): The search query string (required).
        author (Optional[str]): Author name to filter results by.
        num_results (Optional[int]): Number of results to return.
        year_range (Optional[str]): Year range in format 'YYYY-YYYY' to filter results.
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of search results with 'title', 'authors', 'publication_year',
          'journal', 'url', and 'snippet' fields.
        - total_results (int): Total number of results found.
        - query_used (str): The actual query used in the search.
        - status (str): Status of the operation ('success' or 'error').
        - error_message (str): Description of error if execution failed.
    """
    # Input validation
    if not query or not query.strip():
        return {
            "results": [],
            "total_results": 0,
            "query_used": "",
            "status": "error",
            "error_message": "Query parameter is required and cannot be empty."
        }

    try:
        # Call simulated external API
        api_data = call_external_api("google-scholar-search-server-search_google_scholar_advanced")

        # Construct results list from flattened API response
        results = [
            {
                "title": api_data["result_0_title"],
                "authors": api_data["result_0_authors"],
                "publication_year": api_data["result_0_publication_year"],
                "journal": api_data["result_0_journal"],
                "url": api_data["result_0_url"],
                "snippet": api_data["result_0_snippet"]
            },
            {
                "title": api_data["result_1_title"],
                "authors": api_data["result_1_authors"],
                "publication_year": api_data["result_1_publication_year"],
                "journal": api_data["result_1_journal"],
                "url": api_data["result_1_url"],
                "snippet": api_data["result_1_snippet"]
            }
        ]

        # Apply num_results limit if specified
        if num_results is not None and num_results > 0:
            results = results[:num_results]

        # Return final structured response
        return {
            "results": results,
            "total_results": api_data["total_results"],
            "query_used": api_data["query_used"],
            "status": api_data["status"],
            "error_message": api_data["error_message"]
        }

    except Exception as e:
        return {
            "results": [],
            "total_results": 0,
            "query_used": query,
            "status": "error",
            "error_message": f"An unexpected error occurred: {str(e)}"
        }