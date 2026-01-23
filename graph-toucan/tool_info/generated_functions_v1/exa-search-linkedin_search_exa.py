from typing import Dict, List, Any, Optional
import random
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching LinkedIn search results from Exa AI API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_title (str): Title of the first result (e.g., person name or company)
        - result_0_url (str): URL of the first LinkedIn result
        - result_0_snippet (str): Snippet/description of the first result
        - result_0_type (str): Type of the first result (profile, company, etc.)
        - result_1_title (str): Title of the second result
        - result_1_url (str): URL of the second LinkedIn result
        - result_1_snippet (str): Snippet/description of the second result
        - result_1_type (str): Type of the second result
        - total_count (int): Total number of matching results found
        - search_metadata_query_timestamp (str): ISO format timestamp of the search
        - search_metadata_search_type (str): Type of search performed
        - search_metadata_source (str): Source of the search results
        - has_more (bool): Whether more results are available beyond this batch
    """
    return {
        "result_0_title": "Sarah Chen",
        "result_0_url": "https://www.linkedin.com/in/sarahchen",
        "result_0_snippet": "Senior Software Engineer at Google | Python & AI Specialist",
        "result_0_type": "profile",
        "result_1_title": "TechNova Solutions",
        "result_1_url": "https://www.linkedin.com/company/technova-solutions",
        "result_1_snippet": "Innovative tech company focused on AI and cloud solutions",
        "result_1_type": "company",
        "total_count": 42,
        "search_metadata_query_timestamp": datetime.utcnow().isoformat() + "Z",
        "search_metadata_search_type": "all",
        "search_metadata_source": "exa-ai-linkedin",
        "has_more": True,
    }


def exa_search_linkedin_search_exa(
    query: str,
    numResults: Optional[int] = 5,
    searchType: Optional[str] = "all"
) -> Dict[str, Any]:
    """
    Search LinkedIn profiles and companies using Exa AI - finds professional profiles, 
    company pages, and business-related content on LinkedIn. Useful for networking, 
    recruitment, and business research.

    Args:
        query (str): LinkedIn search query (e.g., person name, company, job title)
        numResults (int, optional): Number of LinkedIn results to return. Defaults to 5.
        searchType (str, optional): Type of LinkedIn content to search. Defaults to "all".

    Returns:
        Dict containing:
        - results (List[Dict]): List of LinkedIn search results with keys 'title', 'url', 'snippet', 'type'
        - total_count (int): Total number of matching results found
        - search_metadata (Dict): Metadata about the search execution
        - has_more (bool): Whether additional results are available beyond current batch

    Raises:
        ValueError: If query is empty or None
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")

    if numResults is None:
        numResults = 5
    if searchType is None:
        searchType = "all"

    # Call external API to get flattened data
    api_data = call_external_api("exa-search-linkedin_search_exa")

    # Construct results list from indexed fields
    results = [
        {
            "title": api_data["result_0_title"],
            "url": api_data["result_0_url"],
            "snippet": api_data["result_0_snippet"],
            "type": api_data["result_0_type"]
        },
        {
            "title": api_data["result_1_title"],
            "url": api_data["result_1_url"],
            "snippet": api_data["result_1_snippet"],
            "type": api_data["result_1_type"]
        }
    ]

    # Trim results to requested number
    results = results[:numResults]

    # Construct final response matching output schema
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "search_metadata": {
            "query_timestamp": api_data["search_metadata_query_timestamp"],
            "search_type": api_data["search_metadata_search_type"],
            "source": api_data["search_metadata_source"]
        },
        "has_more": api_data["has_more"]
    }