from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Sci-Hub paper search by keyword.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first search result
        - result_0_authors (str): Authors of the first search result
        - result_0_year (int): Publication year of the first search result
        - result_0_doi (str): DOI of the first search result
        - result_0_url (str): URL to the paper in Sci-Hub for the first result
        - result_1_title (str): Title of the second search result
        - result_1_authors (str): Authors of the second search result
        - result_1_year (int): Publication year of the second search result
        - result_1_doi (str): DOI of the second search result
        - result_1_url (str): URL to the paper in Sci-Hub for the second result
        - error (str): Error message if any occurred, otherwise empty string
    """
    return {
        "result_0_title": "Advances in Machine Learning for Scientific Research",
        "result_0_authors": "Alice Johnson, Bob Smith",
        "result_0_year": 2022,
        "result_0_doi": "10.1234/ml.2022.001",
        "result_0_url": "https://sci-hub.se/10.1234/ml.2022.001",
        "result_1_title": "Neural Networks in Climate Modeling",
        "result_1_authors": "Carol Davis, David Lee",
        "result_1_year": 2021,
        "result_1_doi": "10.1234/climate.2021.005",
        "result_1_url": "https://sci-hub.se/10.1234/climate.2021.005",
        "error": ""
    }

def sci_hub_mcp_server_search_scihub_by_keyword(keyword: str, num_results: Optional[int] = None) -> Dict[str, Any]:
    """
    Searches Sci-Hub for academic papers using a keyword and returns metadata for the top results.
    
    Args:
        keyword (str): The search keyword or phrase to look for in academic papers.
        num_results (Optional[int]): The number of results to return. Defaults to 2 if not specified.
    
    Returns:
        Dict containing:
            - results (List[Dict]): List of paper search results, each with 'title', 'authors', 'year', 'doi', 'url' fields.
            - error (str): Error message if the search failed, otherwise empty string.
    
    Example:
        >>> sci_hub_mcp_server_search_scihub_by_keyword("machine learning")
        {
            'results': [
                {
                    'title': 'Advances in Machine Learning for Scientific Research',
                    'authors': 'Alice Johnson, Bob Smith',
                    'year': 2022,
                    'doi': '10.1234/ml.2022.001',
                    'url': 'https://sci-hub.se/10.1234/ml.2022.001'
                },
                {
                    'title': 'Neural Networks in Climate Modeling',
                    'authors': 'Carol Davis, David Lee',
                    'year': 2021,
                    'doi': '10.1234/climate.2021.005',
                    'url': 'https://sci-hub.se/10.1234/climate.2021.005'
                }
            ],
            'error': ''
        }
    """
    if not keyword or not keyword.strip():
        return {
            "results": [],
            "error": "Keyword is required and cannot be empty."
        }

    # Default to 2 results if num_results is not provided or invalid
    if num_results is None or num_results <= 0:
        num_results = 2

    # Fetch simulated external data
    api_data = call_external_api("sci-hub-mcp-server-search_scihub_by_keyword")

    # Construct results list from flattened API response
    results: List[Dict[str, Any]] = []
    for i in range(min(num_results, 2)):  # Only 2 results available from API
        title_key = f"result_{i}_title"
        authors_key = f"result_{i}_authors"
        year_key = f"result_{i}_year"
        doi_key = f"result_{i}_doi"
        url_key = f"result_{i}_url"

        if title_key in api_data and api_data[title_key]:
            results.append({
                "title": api_data[title_key],
                "authors": api_data[authors_key],
                "year": api_data[year_key],
                "doi": api_data[doi_key],
                "url": api_data[url_key]
            })

    # Return structured response
    return {
        "results": results,
        "error": api_data.get("error", "")
    }