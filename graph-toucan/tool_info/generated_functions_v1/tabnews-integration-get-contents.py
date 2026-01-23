from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for TabNews content retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - content_0_id (str): ID of the first content item
        - content_0_title (str): Title of the first content item
        - content_0_body (str): Body text of the first content item
        - content_0_author (str): Author username of the first content item
        - content_0_published_at (str): Publication timestamp of the first content item
        - content_0_upvotes (int): Number of upvotes for the first content item
        - content_0_tags_0 (str): First tag of the first content item
        - content_0_tags_1 (str): Second tag of the first content item
        - content_0_topic (str): Topic of the first content item
        - content_1_id (str): ID of the second content item
        - content_1_title (str): Title of the second content item
        - content_1_body (str): Body text of the second content item
        - content_1_author (str): Author username of the second content item
        - content_1_published_at (str): Publication timestamp of the second content item
        - content_1_upvotes (int): Number of upvotes for the second content item
        - content_1_tags_0 (str): First tag of the second content item
        - content_1_tags_1 (str): Second tag of the second content item
        - content_1_topic (str): Topic of the second content item
        - total_count (int): Total number of available content items matching criteria
        - page (int): Current page number returned
        - per_page (int): Number of items per page
        - has_more (bool): Whether more pages are available
        - strategy (str): Strategy used for sorting/filtering results
        - metadata_cache_status (str): Cache status of the response
        - metadata_rate_limit_remaining (int): Remaining rate limit count
        - metadata_processing_time_ms (int): Processing time in milliseconds
    """
    return {
        "content_0_id": "c1a2b3d4e5f6",
        "content_0_title": "Introduction to Machine Learning",
        "content_0_body": "Machine learning is a subset of artificial intelligence...",
        "content_0_author": "ml_expert",
        "content_0_published_at": "2023-10-05T08:30:00Z",
        "content_0_upvotes": 125,
        "content_0_tags_0": "machine-learning",
        "content_0_tags_1": "ai",
        "content_0_topic": "technology",
        "content_1_id": "f6e5d4c3b2a1",
        "content_1_title": "Building REST APIs with FastAPI",
        "content_1_body": "FastAPI is a modern, fast web framework for building APIs...",
        "content_1_author": "api_developer",
        "content_1_published_at": "2023-10-04T14:20:00Z",
        "content_1_upvotes": 89,
        "content_1_tags_0": "fastapi",
        "content_1_tags_1": "python",
        "content_1_topic": "programming",
        "total_count": 1573,
        "page": 1,
        "per_page": 20,
        "has_more": True,
        "strategy": "relevant",
        "metadata_cache_status": "HIT",
        "metadata_rate_limit_remaining": 98,
        "metadata_processing_time_ms": 45
    }

def tabnews_integration_get_contents(page: Optional[int] = None, per_page: Optional[int] = None, strategy: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve content items from the TabNews API based on specified parameters.
    
    Args:
        page (Optional[int]): The page number to retrieve (default: 1)
        per_page (Optional[int]): Number of content items per page (default: 20, max: 100)
        strategy (Optional[str]): Strategy to sort/filter content ('relevant', 'new', 'old') (default: 'relevant')
    
    Returns:
        Dict containing:
        - contents (List[Dict]): List of content items with fields like id, title, body, author, etc.
        - total_count (int): Total number of available content items matching criteria
        - page (int): Current page number returned
        - per_page (int): Number of items per page
        - has_more (bool): Whether more pages are available
        - strategy (str): Strategy used for sorting/filtering
        - metadata (Dict): Additional contextual information about the response
    
    Raises:
        ValueError: If page or per_page are invalid, or strategy is not supported
    """
    # Input validation
    if page is not None and (not isinstance(page, int) or page < 1):
        raise ValueError("Page must be a positive integer")
    
    if per_page is not None and (not isinstance(per_page, int) or per_page < 1 or per_page > 100):
        raise ValueError("Per page must be a positive integer and not exceed 100")
    
    valid_strategies = ['relevant', 'new', 'old']
    if strategy is not None and strategy not in valid_strategies:
        raise ValueError(f"Strategy must be one of {valid_strategies}")
    
    # Set defaults
    effective_page = page if page is not None else 1
    effective_per_page = per_page if per_page is not None else 20
    effective_strategy = strategy if strategy is not None else 'relevant'
    
    # Call external API (simulated)
    api_data = call_external_api("tabnews-integration-get contents")
    
    # Construct contents list from flattened API data
    contents = [
        {
            "id": api_data["content_0_id"],
            "title": api_data["content_0_title"],
            "body": api_data["content_0_body"],
            "author": api_data["content_0_author"],
            "published_at": api_data["content_0_published_at"],
            "upvotes": api_data["content_0_upvotes"],
            "tags": [api_data["content_0_tags_0"], api_data["content_0_tags_1"]],
            "topic": api_data["content_0_topic"]
        },
        {
            "id": api_data["content_1_id"],
            "title": api_data["content_1_title"],
            "body": api_data["content_1_body"],
            "author": api_data["content_1_author"],
            "published_at": api_data["content_1_published_at"],
            "upvotes": api_data["content_1_upvotes"],
            "tags": [api_data["content_1_tags_0"], api_data["content_1_tags_1"]],
            "topic": api_data["content_1_topic"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "cache_status": api_data["metadata_cache_status"],
        "rate_limit_remaining": api_data["metadata_rate_limit_remaining"],
        "processing_time_ms": api_data["metadata_processing_time_ms"]
    }
    
    # Construct final result
    result = {
        "contents": contents,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "per_page": api_data["per_page"],
        "has_more": api_data["has_more"],
        "strategy": api_data["strategy"],
        "metadata": metadata
    }
    
    return result