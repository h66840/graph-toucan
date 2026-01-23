from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for CrossRef works search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the response (e.g., "ok")
        - message_type (str): Type of message returned (e.g., "work-list")
        - message_version (str): Version of the message format
        - total_results (int): Total number of results matching the query
        - items_per_page (int): Number of items returned in this response
        - result_0_DOI (str): DOI of the first result
        - result_0_title (str): Title of the first result
        - result_0_author (str): Author list of the first result as string
        - result_0_type (str): Type of the first result (e.g., "journal-article")
        - result_0_publisher (str): Publisher of the first result
        - result_0_published (str): Published date of the first result
        - result_0_URL (str): URL of the first result
        - result_0_ISSN (str): ISSN of the first result
        - result_0_ISBN (str): ISBN of the first result
        - result_0_container_title (str): Container title of the first result
        - result_0_reference_count (int): Reference count of the first result
        - result_0_score (float): Score of the first result
        - result_1_DOI (str): DOI of the second result
        - result_1_title (str): Title of the second result
        - result_1_author (str): Author list of the second result as string
        - result_1_type (str): Type of the second result
        - result_1_publisher (str): Publisher of the second result
        - result_1_published (str): Published date of the second result
        - result_1_URL (str): URL of the second result
        - result_1_ISSN (str): ISSN of the second result
        - result_1_ISBN (str): ISBN of the second result
        - result_1_container_title (str): Container title of the second result
        - result_1_reference_count (int): Reference count of the second result
        - result_1_score (float): Score of the second result
    """
    return {
        "status": "ok",
        "message_type": "work-list",
        "message_version": "1.0.0",
        "total_results": 150,
        "items_per_page": 2,
        "result_0_DOI": "10.1000/xyz123",
        "result_0_title": "An Analysis of Modern Scientific Methods",
        "result_0_author": "Smith, John; Doe, Jane",
        "result_0_type": "journal-article",
        "result_0_publisher": "Springer",
        "result_0_published": "2022-05-15",
        "result_0_URL": "https://doi.org/10.1000/xyz123",
        "result_0_ISSN": "1234-5678",
        "result_0_ISBN": "",
        "result_0_container_title": "Journal of Science and Technology",
        "result_0_reference_count": 45,
        "result_0_score": 0.98,
        "result_1_DOI": "10.1000/abc456",
        "result_1_title": "Advancements in Artificial Intelligence Research",
        "result_1_author": "Brown, Alice; Wilson, Robert",
        "result_1_type": "journal-article",
        "result_1_publisher": "Elsevier",
        "result_1_published": "2023-01-20",
        "result_1_URL": "https://doi.org/10.1000/abc456",
        "result_1_ISSN": "8765-4321",
        "result_1_ISBN": "978-1-23456-789-0",
        "result_1_container_title": "AI Review Quarterly",
        "result_1_reference_count": 67,
        "result_1_score": 0.95,
    }


def crossref_mcp_server_search_works_by_query(
    query: str,
    limit: Optional[int] = None,
    mailto: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search CrossRef works by a query string.

    Args:
        query (str): Required search query string.
        limit (Optional[int]): Maximum number of results to return.
        mailto (Optional[str]): Email address for contact with the service.

    Returns:
        Dict containing:
        - status (str): Status of the response (e.g., "ok")
        - message_type (str): Type of message returned (e.g., "work-list")
        - message_version (str): Version of the message format
        - total_results (int): Total number of results matching the query
        - items_per_page (int): Number of items returned in this response
        - results (List[Dict]): List of publication records with fields like 'DOI', 'title',
          'author', 'type', 'publisher', 'published', 'URL', 'ISSN', 'ISBN',
          'container-title', 'reference-count', 'score', and other metadata.

    Raises:
        ValueError: If query is empty or not provided.
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty.")

    # Fetch simulated external API data
    api_data = call_external_api("crossref-mcp-server-search_works_by_query")

    # Construct results list from flattened fields
    results = [
        {
            "DOI": api_data["result_0_DOI"],
            "title": api_data["result_0_title"],
            "author": api_data["result_0_author"],
            "type": api_data["result_0_type"],
            "publisher": api_data["result_0_publisher"],
            "published": api_data["result_0_published"],
            "URL": api_data["result_0_URL"],
            "ISSN": api_data["result_0_ISSN"],
            "ISBN": api_data["result_0_ISBN"],
            "container-title": api_data["result_0_container_title"],
            "reference-count": api_data["result_0_reference_count"],
            "score": api_data["result_0_score"],
        },
        {
            "DOI": api_data["result_1_DOI"],
            "title": api_data["result_1_title"],
            "author": api_data["result_1_author"],
            "type": api_data["result_1_type"],
            "publisher": api_data["result_1_publisher"],
            "published": api_data["result_1_published"],
            "URL": api_data["result_1_URL"],
            "ISSN": api_data["result_1_ISSN"],
            "ISBN": api_data["result_1_ISBN"],
            "container-title": api_data["result_1_container_title"],
            "reference-count": api_data["result_1_reference_count"],
            "score": api_data["result_1_score"],
        }
    ]

    # Apply limit if specified
    if limit is not None and limit > 0:
        results = results[:limit]
        items_per_page = min(limit, len(results))
    else:
        items_per_page = len(results)

    # Construct final response
    return {
        "status": api_data["status"],
        "message_type": api_data["message_type"],
        "message_version": api_data["message_version"],
        "total_results": api_data["total_results"],
        "items_per_page": items_per_page,
        "results": results,
    }