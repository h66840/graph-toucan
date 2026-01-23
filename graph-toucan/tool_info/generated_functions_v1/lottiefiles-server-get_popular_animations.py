from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for LottieFiles popular animations.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - count (int): Total number of popular animations returned
        - popular_0_id (str): ID of the first popular animation
        - popular_0_name (str): Name of the first popular animation
        - popular_0_urls (str): URLs JSON string for the first animation
        - popular_0_additional_informations (str): Additional info JSON string for first animation
        - popular_0_pack (str): Pack name for the first animation
        - popular_0_user_id (str): User ID of creator for first animation
        - popular_0_user_name (str): User name of creator for first animation
        - popular_1_id (str): ID of the second popular animation
        - popular_1_name (str): Name of the second popular animation
        - popular_1_urls (str): URLs JSON string for the second animation
        - popular_1_additional_informations (str): Additional info JSON string for second animation
        - popular_1_pack (str): Pack name for the second animation
        - popular_1_user_id (str): User ID of creator for second animation
        - popular_1_user_name (str): User name of creator for second animation
    """
    return {
        "count": 2,
        "popular_0_id": "anim123",
        "popular_0_name": "Bouncing Ball",
        "popular_0_urls": '{"preview": "https://lottie.host/preview/123", "download": "https://lottie.host/download/123"}',
        "popular_0_additional_informations": '{"tags": ["animation", "bounce"], "duration": 2.5}',
        "popular_0_pack": "Basic Animations",
        "popular_0_user_id": "user456",
        "popular_0_user_name": "JohnDoe",
        "popular_1_id": "anim789",
        "popular_1_name": "Loading Spinner",
        "popular_1_urls": '{"preview": "https://lottie.host/preview/789", "download": "https://lottie.host/download/789"}',
        "popular_1_additional_informations": '{"tags": ["loading", "spinner"], "duration": 1.8}',
        "popular_1_pack": "UI Elements",
        "popular_1_user_id": "user999",
        "popular_1_user_name": "JaneSmith",
    }

def lottiefiles_server_get_popular_animations(limit: Optional[int] = None, page: Optional[int] = None) -> Dict[str, Any]:
    """
    Get a list of currently popular Lottie animations.
    
    Args:
        limit (Optional[int]): Number of items per page. If not provided, defaults to a reasonable value.
        page (Optional[int]): Page number, starting from 1. If not provided, defaults to 1.
    
    Returns:
        Dict containing:
        - count (int): total number of popular animations returned
        - popular (List[Dict]): list of animation objects with details like id, name, urls, 
          additional_informations, pack, user, and other metadata
    
    Raises:
        ValueError: If page is less than 1 or limit is less than 1
    """
    # Input validation
    if page is not None and page < 1:
        raise ValueError("Page number must be greater than or equal to 1")
    if limit is not None and limit < 1:
        raise ValueError("Limit must be greater than or equal to 1")
    
    # Use default values if parameters are not provided
    effective_limit = limit if limit is not None else 10
    effective_page = page if page is not None else 1
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("lottiefiles-server-get_popular_animations")
    
    # Construct the popular animations list from flattened API response
    popular_animations: List[Dict[str, Any]] = []
    
    # Process first animation if available
    if "popular_0_id" in api_data:
        animation_0 = {
            "id": api_data["popular_0_id"],
            "name": api_data["popular_0_name"],
            "urls": api_data["popular_0_urls"],
            "additional_informations": api_data["popular_0_additional_informations"],
            "pack": api_data["popular_0_pack"],
            "user": {
                "id": api_data["popular_0_user_id"],
                "name": api_data["popular_0_user_name"]
            }
        }
        popular_animations.append(animation_0)
    
    # Process second animation if available
    if "popular_1_id" in api_data:
        animation_1 = {
            "id": api_data["popular_1_id"],
            "name": api_data["popular_1_name"],
            "urls": api_data["popular_1_urls"],
            "additional_informations": api_data["popular_1_additional_informations"],
            "pack": api_data["popular_1_pack"],
            "user": {
                "id": api_data["popular_1_user_id"],
                "name": api_data["popular_1_user_name"]
            }
        }
        popular_animations.append(animation_1)
    
    # Apply limit to results
    limited_popular = popular_animations[:effective_limit]
    
    # Construct final result
    result = {
        "count": len(limited_popular),
        "popular": limited_popular
    }
    
    return result