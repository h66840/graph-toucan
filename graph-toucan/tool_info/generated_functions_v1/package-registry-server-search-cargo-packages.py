from typing import Dict, List, Any, Optional
import random
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Cargo package search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_name (str): Name of the first matching package
        - result_0_version (str): Version of the first package
        - result_0_description (str): Description of the first package
        - result_0_authors (str): Comma-separated authors of the first package
        - result_0_published_at (str): Publication date of the first package (ISO format)
        - result_1_name (str): Name of the second matching package
        - result_1_version (str): Version of the second package
        - result_1_description (str): Description of the second package
        - result_1_authors (str): Comma-separated authors of the second package
        - result_1_published_at (str): Publication date of the second package (ISO format)
        - total_count (int): Total number of packages matching the query
        - page (int): Current page of results (1-indexed)
        - has_more (bool): Whether more results are available beyond current limit
        - metadata_timestamp (str): ISO timestamp of the request
        - metadata_registry_url (str): URL of the Cargo registry source
        - metadata_relevance_method (str): Method used for relevance scoring
    """
    base_time = datetime.utcnow()
    return {
        "result_0_name": "serde",
        "result_0_version": "1.0.188",
        "result_0_description": "A generic serialization/deserialization framework",
        "result_0_authors": "Erick Tryzelaar, David Tolnay",
        "result_0_published_at": (base_time).isoformat(),
        "result_1_name": "tokio",
        "result_1_version": "1.37.0",
        "result_1_description": "An asynchronous runtime for the Rust programming language",
        "result_1_authors": "Carl Lerche, Alex Matson, Tokio Contributors",
        "result_1_published_at": (base_time).isoformat(),
        "total_count": 150,
        "page": 1,
        "has_more": True,
        "metadata_timestamp": base_time.isoformat(),
        "metadata_registry_url": "https://crates.io",
        "metadata_relevance_method": "text_similarity_and_popularity"
    }


def package_registry_server_search_cargo_packages(query: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Search the Cargo registry for packages based on a query string.

    Args:
        query (str): The search query string (required). Used to match package names, descriptions, or keywords.
        limit (Optional[int]): Maximum number of results to return. If None, defaults to 2.

    Returns:
        Dict containing:
        - results (List[Dict]): List of package entries with keys: name, version, description, authors, published_at
        - total_count (int): Total number of packages found matching the query
        - page (int): Current page of results (1-indexed)
        - has_more (bool): Whether additional results exist beyond current page/limit
        - metadata (Dict): Contextual info including timestamp, registry URL, and relevance method

    Raises:
        ValueError: If query is empty or not a string
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query parameter is required and must be a non-empty string.")
    
    if limit is None:
        limit = 2
    elif limit < 1:
        limit = 1

    # Fetch simulated external data
    api_data = call_external_api("package-registry-server-search-cargo-packages")

    # Construct results list from indexed fields
    results = []
    for i in range(min(limit, 2)):  # We only have 2 simulated results
        result_key = f"result_{i}"
        if f"{result_key}_name" in api_data:
            results.append({
                "name": api_data[f"{result_key}_name"],
                "version": api_data[f"{result_key}_version"],
                "description": api_data[f"{result_key}_description"],
                "authors": api_data[f"{result_key}_authors"].split(", ") if api_data[f"{result_key}_authors"] else [],
                "published_at": api_data[f"{result_key}_published_at"]
            })

    # Construct metadata
    metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "registry_source_url": api_data["metadata_registry_url"],
        "query_processing": {
            "relevance_scoring_method": api_data["metadata_relevance_method"]
        }
    }

    # Final result structure
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "has_more": api_data["has_more"],
        "metadata": metadata
    }