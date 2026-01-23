from typing import Dict, List, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for App Store reviews.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - review_0_id (str): First review ID
        - review_0_userName (str): First reviewer's name
        - review_0_userUrl (str): First reviewer's profile URL
        - review_0_version (str): App version reviewed in first review
        - review_0_score (int): Rating (1-5) for first review
        - review_0_title (str): Title of first review
        - review_0_text (str): Content of first review
        - review_0_url (str): URL of first review
        - review_0_updated (str): ISO format date of first review update
        - review_1_id (str): Second review ID
        - review_1_userName (str): Second reviewer's name
        - review_1_userUrl (str): Second reviewer's profile URL
        - review_1_version (str): App version reviewed in second review
        - review_1_score (int): Rating (1-5) for second review
        - review_1_title (str): Title of second review
        - review_1_text (str): Content of second review
        - review_1_url (str): URL of second review
        - review_1_updated (str): ISO format date of second review update
        - total_results (int): Total number of reviews available
        - current_page (int): Current page number returned
        - has_next_page (bool): Whether more pages exist
        - sort_order (str): Sort method applied ('recent' or 'helpful')
        - country (str): Country code used for fetching reviews
        - app_id (str): Bundle ID of the app
        - metadata_request_timestamp (str): ISO timestamp of request
        - metadata_average_rating (float): Average rating across all reviews
        - metadata_score_1_count (int): Number of 1-star reviews
        - metadata_score_2_count (int): Number of 2-star reviews
        - metadata_score_3_count (int): Number of 3-star reviews
        - metadata_score_4_count (int): Number of 4-star reviews
        - metadata_score_5_count (int): Number of 5-star reviews
        - metadata_pagination_limit (int): Maximum number of pages available
    """
    return {
        "review_0_id": "r123456789",
        "review_0_userName": "Sarah Johnson",
        "review_0_userUrl": "https://apps.apple.com/us/reviewer/sarah-johnson?id=12345",
        "review_0_version": "2.3.1",
        "review_0_score": 5,
        "review_0_title": "Amazing app!",
        "review_0_text": "This app has completely changed how I manage my daily tasks. Highly recommend!",
        "review_0_url": "https://apps.apple.com/us/app/app-name/review?id=r123456789",
        "review_0_updated": "2023-10-15T08:30:00Z",
        "review_1_id": "r987654321",
        "review_1_userName": "Mike Chen",
        "review_1_userUrl": "https://apps.apple.com/us/reviewer/mike-chen?id=67890",
        "review_1_version": "2.3.0",
        "review_1_score": 3,
        "review_1_title": "Good but needs improvement",
        "review_1_text": "The core functionality works well, but there are some bugs in the latest update.",
        "review_1_url": "https://apps.apple.com/us/app/app-name/review?id=r987654321",
        "review_1_updated": "2023-10-14T14:22:00Z",
        "total_results": 1250,
        "current_page": 1,
        "has_next_page": True,
        "sort_order": "recent",
        "country": "us",
        "app_id": "com.example.app",
        "metadata_request_timestamp": datetime.datetime.now().isoformat(),
        "metadata_average_rating": 4.2,
        "metadata_score_1_count": 125,
        "metadata_score_2_count": 85,
        "metadata_score_3_count": 210,
        "metadata_score_4_count": 330,
        "metadata_score_5_count": 500,
        "metadata_pagination_limit": 10
    }

def app_market_intelligence_app_store_reviews(
    appId: Optional[str] = None,
    country: Optional[str] = "us",
    id: Optional[int] = None,
    page: Optional[int] = 1,
    sort: Optional[str] = "recent"
) -> Dict[str, Any]:
    """
    Get reviews for an App Store app.
    
    Either appId or id must be provided to identify the app.
    
    Args:
        appId (Optional[str]): Bundle ID (e.g., 'com.midasplayer.apps.candycrushsaga'). Either this or id must be provided.
        country (Optional[str]): Country code to get reviews from (default: us)
        id (Optional[int]): Numeric App ID (e.g., 553834731). Either this or id must be provided.
        page (Optional[int]): Page number to retrieve (default: 1, max: 10)
        sort (Optional[str]): Sort order (recent or helpful)
    
    Returns:
        Dict containing:
        - reviews (List[Dict]): List of review objects with id, userName, userUrl, version, score, title, text, url, updated
        - total_results (int): Total number of reviews available
        - current_page (int): The page number returned
        - has_next_page (bool): Whether additional pages are available
        - sort_order (str): Applied sort method
        - country (str): Country code used
        - app_id (str): Bundle ID of the app
        - metadata (Dict): Additional contextual information including request timestamp, 
          average rating, score distribution, and pagination limits
    
    Raises:
        ValueError: If neither appId nor id is provided
    """
    # Input validation
    if not appId and not id:
        raise ValueError("Either appId or id must be provided to identify the app")
    
    # Validate sort parameter
    valid_sorts = ["recent", "helpful"]
    if sort and sort not in valid_sorts:
        raise ValueError(f"sort must be one of {valid_sorts}")
    
    # Validate page parameter
    if page and (page < 1 or page > 10):
        raise ValueError("page must be between 1 and 10")
    
    # Use default values if not provided
    effective_country = country or "us"
    effective_page = page or 1
    effective_sort = sort or "recent"
    
    # Call external API (simulated)
    api_data = call_external_api("app-market-intelligence-app-store-reviews")
    
    # Construct reviews list from indexed fields
    reviews = [
        {
            "id": api_data["review_0_id"],
            "userName": api_data["review_0_userName"],
            "userUrl": api_data["review_0_userUrl"],
            "version": api_data["review_0_version"],
            "score": api_data["review_0_score"],
            "title": api_data["review_0_title"],
            "text": api_data["review_0_text"],
            "url": api_data["review_0_url"],
            "updated": api_data["review_0_updated"]
        },
        {
            "id": api_data["review_1_id"],
            "userName": api_data["review_1_userName"],
            "userUrl": api_data["review_1_userUrl"],
            "version": api_data["review_1_version"],
            "score": api_data["review_1_score"],
            "title": api_data["review_1_title"],
            "text": api_data["review_1_text"],
            "url": api_data["review_1_url"],
            "updated": api_data["review_1_updated"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "request_timestamp": api_data["metadata_request_timestamp"],
        "average_rating": api_data["metadata_average_rating"],
        "score_distribution": {
            "1": api_data["metadata_score_1_count"],
            "2": api_data["metadata_score_2_count"],
            "3": api_data["metadata_score_3_count"],
            "4": api_data["metadata_score_4_count"],
            "5": api_data["metadata_score_5_count"]
        },
        "pagination_limits": {
            "max_pages": api_data["metadata_pagination_limit"],
            "results_per_page": 20
        }
    }
    
    # Construct final result
    result = {
        "reviews": reviews,
        "total_results": api_data["total_results"],
        "current_page": api_data["current_page"],
        "has_next_page": api_data["has_next_page"],
        "sort_order": api_data["sort_order"],
        "country": api_data["country"],
        "app_id": api_data["app_id"],
        "metadata": metadata
    }
    
    return result