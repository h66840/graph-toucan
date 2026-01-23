from typing import Dict, List, Any, Optional
import random
import string
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for funder search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_name (str): Name of the first funder
        - result_0_doi (str): DOI of the first funder
        - result_0_location (str): Location of the first funder
        - result_0_metadata (str): Metadata of the first funder as JSON string
        - result_1_name (str): Name of the second funder
        - result_1_doi (str): DOI of the second funder
        - result_1_location (str): Location of the second funder
        - result_1_metadata (str): Metadata of the second funder as JSON string
        - total_count (int): Total number of funders matching the criteria
        - count (int): Number of results returned
        - next_cursor (str): Cursor token for next page, if available
        - prev_cursor (str): Cursor token for previous page, if available
        - query_time (float): Time taken to execute the query in seconds
        - metadata_api_version (str): API version used
        - metadata_timestamp (str): Timestamp of the response in ISO format
        - metadata_rate_limit_remaining (int): Number of requests remaining in current window
        - metadata_rate_limit_reset (int): Seconds until rate limit resets
    """
    def random_doi():
        return f"10.{random.randint(1000, 9999)}/{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}"

    def random_name():
        prefixes = ["National", "International", "Global", "European", "American", "Asian"]
        subjects = ["Science", "Research", "Innovation", "Technology", "Development", "Studies"]
        types = ["Foundation", "Council", "Institute", "Organization", "Board", "Agency"]
        return f"{random.choice(prefixes)} {random.choice(subjects)} {random.choice(types)}"

    def random_location():
        countries = ["United States", "United Kingdom", "Germany", "France", "Japan", "China", "Canada", "Australia"]
        cities = ["Washington", "London", "Berlin", "Paris", "Tokyo", "Beijing", "Ottawa", "Sydney"]
        return f"{random.choice(cities)}, {random.choice(countries)}"

    return {
        "result_0_name": random_name(),
        "result_0_doi": random_doi(),
        "result_0_location": random_location(),
        "result_0_metadata": '{"affiliation": "public", "funding_level": "national", "active": true}',
        "result_1_name": random_name(),
        "result_1_doi": random_doi(),
        "result_1_location": random_location(),
        "result_1_metadata": '{"affiliation": "private", "funding_level": "international", "active": true}',
        "total_count": random.randint(50, 500),
        "count": 2,
        "next_cursor": ''.join(random.choices(string.ascii_letters + string.digits, k=24)),
        "prev_cursor": ''.join(random.choices(string.ascii_letters + string.digits, k=24)),
        "query_time": round(random.uniform(0.05, 0.5), 3),
        "metadata_api_version": "1.2.0",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_rate_limit_remaining": random.randint(90, 100),
        "metadata_rate_limit_reset": random.randint(55, 60)
    }


def crossref_mcp_server_search_funders(
    limit: Optional[int] = None,
    mailto: Optional[str] = None,
    query: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for funders in the Crossref database using specified criteria.

    Args:
        limit (Optional[int]): Maximum number of results to return. If not provided, defaults to a system-defined limit.
        mailto (Optional[str]): Email address for contact information, used by Crossref for identifying API clients.
        query (Optional[str]): Search query string to filter funders by name, DOI, or other metadata.

    Returns:
        Dict containing:
        - results (List[Dict]): List of funder records with keys: name, doi, location, metadata
        - total_count (int): Total number of matching funders
        - count (int): Number of results returned
        - next_cursor (str): Token for retrieving next page of results
        - prev_cursor (str): Token for retrieving previous page of results
        - query_time (float): Time taken to execute the search in seconds
        - metadata (Dict): Additional response metadata including API version, timestamp, and rate limit info

    Example:
        >>> result = crossref_mcp_server_search_funders(query="National Science", limit=10)
        >>> print(result['total_count'])
        >>> print(result['results'][0]['name'])
    """
    # Input validation
    if limit is not None and (not isinstance(limit, int) or limit <= 0):
        raise ValueError("Limit must be a positive integer")

    if mailto is not None and (not isinstance(mailto, str) or "@" not in mailto):
        raise ValueError("Mailto must be a valid email address")

    if query is not None and not isinstance(query, str):
        raise ValueError("Query must be a string")

    # Call external API (simulated)
    api_data = call_external_api("crossref-mcp-server-search_funders")

    # Construct results list from indexed fields
    results = [
        {
            "name": api_data["result_0_name"],
            "doi": api_data["result_0_doi"],
            "location": api_data["result_0_location"],
            "metadata": api_data["result_0_metadata"]
        },
        {
            "name": api_data["result_1_name"],
            "doi": api_data["result_1_doi"],
            "location": api_data["result_1_location"],
            "metadata": api_data["result_1_metadata"]
        }
    ]

    # Apply limit if specified
    if limit is not None:
        results = results[:limit]
        count = min(len(results), limit)
    else:
        count = api_data["count"]

    # Construct final response structure
    response = {
        "results": results,
        "total_count": api_data["total_count"],
        "count": count,
        "next_cursor": api_data["next_cursor"],
        "prev_cursor": api_data["prev_cursor"],
        "query_time": api_data["query_time"],
        "metadata": {
            "api_version": api_data["metadata_api_version"],
            "timestamp": api_data["metadata_timestamp"],
            "rate_limit": {
                "remaining": api_data["metadata_rate_limit_remaining"],
                "reset": api_data["metadata_rate_limit_reset"]
            }
        }
    }

    return response