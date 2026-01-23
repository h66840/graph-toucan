from typing import Dict, List, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for GitHub search using Exa AI.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_title (str): Title of the first search result
        - result_0_url (str): URL of the first search result
        - result_0_description (str): Description of the first search result
        - result_0_type (str): Type of the first result (e.g., repository, user, code)
        - result_0_extra_info (str): Additional info specific to result type
        - result_1_title (str): Title of the second search result
        - result_1_url (str): URL of the second search result
        - result_1_description (str): Description of the second search result
        - result_1_type (str): Type of the second result
        - result_1_extra_info (str): Additional info specific to result type
        - total_count (int): Total number of results found
        - query_used (str): The actual query executed
        - search_type (str): Type of content searched ('repositories', 'code', 'users', 'all')
        - metadata_timestamp (str): ISO format timestamp of search execution
        - metadata_source (str): Source of the data ('GitHub')
        - metadata_filters (str): Filters applied during search
        - metadata_ranking (str): Ranking criteria used
    """
    return {
        "result_0_title": "Awesome Python Projects",
        "result_0_url": "https://github.com/example/python-projects",
        "result_0_description": "A collection of awesome Python scripts and tools.",
        "result_0_type": "repository",
        "result_0_extra_info": "stars:1500,forks:300",
        "result_1_title": "def search_github(query)",
        "result_1_url": "https://github.com/dev-snippets/python-utils/blob/main/github_search.py",
        "result_1_description": "Code snippet for searching GitHub repositories using API.",
        "result_1_type": "code",
        "result_1_extra_info": "language:Python,lines:45",
        "total_count": 127,
        "query_used": "python github search",
        "search_type": "all",
        "metadata_timestamp": datetime.datetime.utcnow().isoformat(),
        "metadata_source": "GitHub",
        "metadata_filters": "sort:best_match",
        "metadata_ranking": "relevance"
    }


def exa_search_github_search_exa(
    query: str,
    numResults: Optional[int] = 5,
    searchType: Optional[str] = "all"
) -> Dict[str, Any]:
    """
    Search GitHub repositories and code using Exa AI - finds repositories, code snippets, 
    documentation, and developer profiles on GitHub. Useful for finding open source projects, 
    code examples, and technical resources.

    Args:
        query (str): GitHub search query (repository name, programming language, username, etc.)
        numResults (int, optional): Number of GitHub results to return (default: 5)
        searchType (str, optional): Type of GitHub content to search (default: 'all').
                                    One of: 'repositories', 'code', 'users', 'all'

    Returns:
        Dict containing:
        - results (List[Dict]): List of search results with keys: title, url, description, type, extra_info
        - total_count (int): Total number of results found for the query
        - query_used (str): The actual search query that was executed
        - search_type (str): Type of GitHub content searched
        - result_metadata (Dict): Metadata about the search execution including timestamp, source, filters, ranking

    Raises:
        ValueError: If query is empty or searchType is not one of the allowed values
    """
    # Input validation
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty.")
    
    allowed_search_types = ["all", "repositories", "code", "users"]
    if searchType not in allowed_search_types:
        raise ValueError(f"searchType must be one of {allowed_search_types}, got '{searchType}'")

    # Normalize query
    cleaned_query = query.strip()

    # Call external API (simulated)
    api_data = call_external_api("exa-search-github_search_exa")

    # Construct results list from indexed flat fields
    results = []
    for i in range(2):  # We have 2 results from the mock API
        title_key = f"result_{i}_title"
        url_key = f"result_{i}_url"
        desc_key = f"result_{i}_description"
        type_key = f"result_{i}_type"
        extra_key = f"result_{i}_extra_info"

        if title_key in api_data:
            results.append({
                "title": api_data[title_key],
                "url": api_data[url_key],
                "description": api_data[desc_key],
                "type": api_data[type_key],
                "extra_info": api_data[extra_key]
            })

    # Limit results based on numResults parameter
    limited_results = results[:numResults] if numResults else results

    # Construct metadata
    result_metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "source": api_data["metadata_source"],
        "filters": api_data["metadata_filters"],
        "ranking_criteria": api_data["metadata_ranking"]
    }

    # Return final structured response
    return {
        "results": limited_results,
        "total_count": api_data["total_count"],
        "query_used": api_data["query_used"],
        "search_type": api_data["search_type"],
        "result_metadata": result_metadata
    }