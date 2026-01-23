from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Pinterest search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_image_url (str): URL of the first image result
        - result_0_title (str): Title of the first image result
        - result_0_description (str): Description of the first image result
        - result_0_board (str): Source board of the first image result
        - result_1_image_url (str): URL of the second image result
        - result_1_title (str): Title of the second image result
        - result_1_description (str): Description of the second image result
        - result_1_board (str): Source board of the second image result
        - total_count (int): Total number of images found matching the keyword
        - query_time (float): Time in seconds taken to complete the search query
        - has_more (bool): Indicates if more results are available beyond the current limit
        - search_metadata_keyword (str): Resolved search keyword
        - search_metadata_limit (int): Actual limit used in the search
        - search_metadata_region (str): Region setting inferred or applied
        - search_metadata_language (str): Language setting inferred or applied
    """
    return {
        "result_0_image_url": "https://i.pinimg.com/564x/ab/cd/ef/abcdef1234567890abcdef1234567890.jpg",
        "result_0_title": "Modern Living Room Design",
        "result_0_description": "A beautifully designed modern living room with minimalist furniture and natural light.",
        "result_0_board": "Interior Design Ideas",
        "result_1_image_url": "https://i.pinimg.com/564x/xy/zt/uv/xyztuv9876543210xyztuv9876543210.jpg",
        "result_1_title": "Cozy Reading Nook",
        "result_1_description": "A cozy corner with a comfortable chair, bookshelf, and warm lighting.",
        "result_1_board": "Home Inspiration",
        "total_count": 158,
        "query_time": 1.23,
        "has_more": True,
        "search_metadata_keyword": "living room ideas",
        "search_metadata_limit": 10,
        "search_metadata_region": "US",
        "search_metadata_language": "en"
    }

def pinterest_mcp_server_pinterest_search(
    keyword: str,
    headless: Optional[bool] = True,
    limit: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search for images on Pinterest by keyword.

    Args:
        keyword (str): Search keyword (required)
        headless (bool, optional): Whether to use headless browser mode. Defaults to True.
        limit (int, optional): Number of images to return. Defaults to 10.

    Returns:
        Dict containing:
        - results (List[Dict]): List of image result objects with keys: image_url, title, description, board
        - total_count (int): Total number of images found matching the keyword
        - query_time (float): Time in seconds taken to complete the search query
        - has_more (bool): Indicates if more results are available beyond the current limit
        - search_metadata (Dict): Metadata about the search including keyword, limit, region, and language

    Raises:
        ValueError: If keyword is empty or not provided
    """
    if not keyword or not keyword.strip():
        raise ValueError("Keyword is required and cannot be empty")

    # Normalize keyword
    normalized_keyword = keyword.strip()

    # Simulate API call with external service
    api_data = call_external_api("pinterest-mcp-server-pinterest_search")

    # Construct results list from flattened API response
    results = [
        {
            "image_url": api_data["result_0_image_url"],
            "title": api_data["result_0_title"],
            "description": api_data["result_0_description"],
            "board": api_data["result_0_board"]
        },
        {
            "image_url": api_data["result_1_image_url"],
            "title": api_data["result_1_title"],
            "description": api_data["result_1_description"],
            "board": api_data["result_1_board"]
        }
    ]

    # Construct final response matching output schema
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "query_time": api_data["query_time"],
        "has_more": api_data["has_more"],
        "search_metadata": {
            "keyword": api_data["search_metadata_keyword"],
            "limit": api_data["search_metadata_limit"],
            "region": api_data["search_metadata_region"],
            "language": api_data["search_metadata_language"]
        }
    }