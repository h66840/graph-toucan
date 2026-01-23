from typing import Dict, List, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external TabNews API for user content retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - contents_0_id (str): ID of the first content item
        - contents_0_title (str): Title of the first content item
        - contents_0_body (str): Body text of the first content item
        - contents_0_publication_date (str): Publication date of the first content item (ISO format)
        - contents_0_upvotes (int): Upvotes count for the first content item
        - contents_0_downvotes (int): Downvotes count for the first content item
        - contents_0_slug (str): Slug of the first content item
        - contents_1_id (str): ID of the second content item
        - contents_1_title (str): Title of the second content item
        - contents_1_body (str): Body text of the second content item
        - contents_1_publication_date (str): Publication date of the second content item (ISO format)
        - contents_1_upvotes (int): Upvotes count for the second content item
        - contents_1_downvotes (int): Downvotes count for the second content item
        - contents_1_slug (str): Slug of the second content item
        - total_count (int): Total number of content items available for the user
        - page (int): Current page number in the pagination sequence
        - per_page (int): Number of content items returned per page
        - has_more (bool): Indicates whether more pages are available
        - strategy (str): Sorting strategy used to retrieve contents
        - username (str): Username for which contents were retrieved
        - metadata_api_version (str): Version of the API
        - metadata_response_timestamp (str): Timestamp of the response (ISO format)
        - metadata_request_duration_ms (int): Duration of the request in milliseconds
    """
    return {
        "contents_0_id": "c1234567890",
        "contents_0_title": "Introduction to Python Programming",
        "contents_0_body": "Python is a powerful and easy-to-learn programming language...",
        "contents_0_publication_date": "2023-10-05T14:30:00Z",
        "contents_0_upvotes": 45,
        "contents_0_downvotes": 2,
        "contents_0_slug": "introduction-to-python-programming",
        "contents_1_id": "c0987654321",
        "contents_1_title": "Building APIs with FastAPI",
        "contents_1_body": "FastAPI is a modern, fast web framework for building APIs...",
        "contents_1_publication_date": "2023-09-28T10:15:00Z",
        "contents_1_upvotes": 38,
        "contents_1_downvotes": 1,
        "contents_1_slug": "building-apis-with-fastapi",
        "total_count": 15,
        "page": 1,
        "per_page": 10,
        "has_more": True,
        "strategy": "new",
        "username": "python_enthusiast",
        "metadata_api_version": "v1",
        "metadata_response_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata_request_duration_ms": 125
    }

def tabnews_integration_get_contents_by_user(
    username: str,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    strategy: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieve content items published by a specific user from the TabNews API.
    
    Args:
        username (str): The username to get the contents (required)
        page (Optional[int]): The page number to retrieve (default: 1)
        per_page (Optional[int]): Number of contents per page (default: 10)
        strategy (Optional[str]): Sorting strategy for contents ('relevant', 'new', 'old') (default: 'relevant')
    
    Returns:
        Dict containing:
        - contents (List[Dict]): List of content items with id, title, body, publication_date, upvotes, downvotes, slug
        - total_count (int): Total number of content items available for the user
        - page (int): Current page number
        - per_page (int): Number of items per page
        - has_more (bool): Whether more pages are available
        - strategy (str): Sorting strategy used
        - username (str): Username for which contents were retrieved
        - metadata (Dict): Additional info like api_version, response_timestamp, request_duration_ms
    
    Raises:
        ValueError: If username is empty or None
    """
    if not username:
        raise ValueError("Username is required")

    # Set defaults if not provided
    page = page if page is not None else 1
    per_page = per_page if per_page is not None else 10
    strategy = strategy if strategy is not None else "relevant"

    # Validate inputs
    if page < 1:
        raise ValueError("Page must be a positive integer")
    if per_page < 1 or per_page > 100:
        raise ValueError("Per page must be between 1 and 100")

    # Supported strategies
    supported_strategies = ["relevant", "new", "old"]
    if strategy not in supported_strategies:
        raise ValueError(f"Strategy must be one of {supported_strategies}")

    # Call external API (simulated)
    api_data = call_external_api("tabnews-integration-get contents by user")

    # Construct contents list from flattened API response
    contents = [
        {
            "id": api_data["contents_0_id"],
            "title": api_data["contents_0_title"],
            "body": api_data["contents_0_body"],
            "publication_date": api_data["contents_0_publication_date"],
            "upvotes": api_data["contents_0_upvotes"],
            "downvotes": api_data["contents_0_downvotes"],
            "slug": api_data["contents_0_slug"]
        },
        {
            "id": api_data["contents_1_id"],
            "title": api_data["contents_1_title"],
            "body": api_data["contents_1_body"],
            "publication_date": api_data["contents_1_publication_date"],
            "upvotes": api_data["contents_1_upvotes"],
            "downvotes": api_data["contents_1_downvotes"],
            "slug": api_data["contents_1_slug"]
        }
    ]

    # Construct metadata
    metadata = {
        "api_version": api_data["metadata_api_version"],
        "response_timestamp": api_data["metadata_response_timestamp"],
        "request_duration_ms": api_data["metadata_request_duration_ms"]
    }

    # Build final result
    result = {
        "contents": contents,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "per_page": api_data["per_page"],
        "has_more": api_data["has_more"],
        "strategy": api_data["strategy"],
        "username": api_data["username"],
        "metadata": metadata
    }

    return result