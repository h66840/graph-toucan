from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for App Store list.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): App Store ID number of first app
        - result_0_appId (str): Bundle ID of first app
        - result_0_title (str): Title of first app
        - result_0_icon (str): Icon URL of first app
        - result_0_url (str): App Store URL of first app
        - result_0_price (float): Price in USD of first app
        - result_0_currency (str): Currency code of first app
        - result_0_free (bool): Whether first app is free
        - result_0_description (str): Description of first app
        - result_0_developer (str): Developer name of first app
        - result_0_developerUrl (str): Developer URL of first app
        - result_0_developerId (int): Developer ID of first app
        - result_0_genre (str): Genre name of first app
        - result_0_genreId (int): Genre ID of first app
        - result_0_released (str): Release date (ISO string) of first app
        - result_1_id (int): App Store ID number of second app
        - result_1_appId (str): Bundle ID of second app
        - result_1_title (str): Title of second app
        - result_1_icon (str): Icon URL of second app
        - result_1_url (str): App Store URL of second app
        - result_1_price (float): Price in USD of second app
        - result_1_currency (str): Currency code of second app
        - result_1_free (bool): Whether second app is free
        - result_1_description (str): Description of second app
        - result_1_developer (str): Developer name of second app
        - result_1_developerUrl (str): Developer URL of second app
        - result_1_developerId (int): Developer ID of second app
        - result_1_genre (str): Genre name of second app
        - result_1_genreId (int): Genre ID of second app
        - result_1_released (str): Release date (ISO string) of second app
        - total_count (int): Total number of apps returned
        - collection (str): Collection type fetched
        - country (str): Country code used
        - category_id (int): Optional category ID filter applied
        - category_name (str): Human-readable category name
        - full_detail_requested (bool): Whether full detail mode was requested
        - language (str): Language code used
        - fetched_at (str): ISO 8601 timestamp when data was retrieved
    """
    return {
        "result_0_id": 123456789,
        "result_0_appId": "com.example.game",
        "result_0_title": "Amazing Puzzle Game",
        "result_0_icon": "https://example.com/icon1.jpg",
        "result_0_url": "https://apps.apple.com/us/app/amazing-puzzle-game/id123456789",
        "result_0_price": 0.0,
        "result_0_currency": "USD",
        "result_0_free": True,
        "result_0_description": "A fun and challenging puzzle game for all ages.",
        "result_0_developer": "Example Games Inc.",
        "result_0_developerUrl": "https://apps.apple.com/us/developer/example-games-inc/id987654321",
        "result_0_developerId": 987654321,
        "result_0_genre": "GAMES",
        "result_0_genreId": 6014,
        "result_0_released": "2023-01-15T10:00:00Z",
        "result_1_id": 987654321,
        "result_1_appId": "com.example.fitness",
        "result_1_title": "FitLife Tracker",
        "result_1_icon": "https://example.com/icon2.jpg",
        "result_1_url": "https://apps.apple.com/us/app/fitlife-tracker/id987654321",
        "result_1_price": 4.99,
        "result_1_currency": "USD",
        "result_1_free": False,
        "result_1_description": "Track your workouts and nutrition with ease.",
        "result_1_developer": "HealthTech Solutions",
        "result_1_developerUrl": "https://apps.apple.com/us/developer/healthtech-solutions/id112233445",
        "result_1_developerId": 112233445,
        "result_1_genre": "HEALTH_AND_FITNESS",
        "result_1_genreId": 6013,
        "result_1_released": "2022-11-20T08:30:00Z",
        "total_count": 2,
        "collection": "topfreeapplications",
        "country": "us",
        "category_id": 6014,
        "category_name": "GAMES",
        "full_detail_requested": False,
        "language": "en",
        "fetched_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }

def app_market_intelligence_app_store_list(
    collection: str,
    category: Optional[int] = None,
    country: Optional[str] = "us",
    fullDetail: Optional[bool] = False,
    lang: Optional[str] = None,
    num: Optional[int] = 50
) -> Dict[str, Any]:
    """
    Get apps from iTunes collections. Returns a list of apps with detailed metadata.

    Args:
        collection (str): Collection to fetch from. Required. One of:
            - newapplications
            - newfreeapplications
            - newpaidapplications
            - topfreeapplications
            - topfreeipadapplications
            - topgrossingapplications
            - topgrossingipadapplications
            - toppaidapplications
            - toppaidipadapplications
        category (int, optional): Category ID to filter by.
        country (str, optional): Country code (default: us)
        fullDetail (bool, optional): Get full app details including ratings, reviews etc (default: false)
        lang (str, optional): Language code for result text.
        num (int, optional): Number of results (default: 50, max: 200)

    Returns:
        Dict containing:
        - results (List[Dict]): List of app objects with metadata
        - total_count (int): Total number of apps returned
        - collection (str): The collection type that was fetched
        - country (str): The country code used
        - category_id (int): Optional category ID filter applied
        - category_name (str): Human-readable category name
        - full_detail_requested (bool): Whether full detail mode was requested
        - language (str): Language code used
        - fetched_at (str): ISO 8601 timestamp when data was retrieved

    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Validate required parameter
    if not collection:
        raise ValueError("Parameter 'collection' is required")

    valid_collections = [
        "newapplications", "newfreeapplications", "newpaidapplications",
        "topfreeapplications", "topfreeipadapplications", "topgrossingapplications",
        "topgrossingipadapplications", "toppaidapplications", "toppaidipadapplications"
    ]
    
    if collection not in valid_collections:
        raise ValueError(f"Invalid collection. Must be one of: {', '.join(valid_collections)}")

    # Validate num parameter
    if num is not None and (num <= 0 or num > 200):
        raise ValueError("Parameter 'num' must be between 1 and 200")

    # Map category ID to name
    category_map = {
        6000: "BUSINESS", 6001: "WEATHER", 6002: "UTILITIES", 6003: "TRAVEL",
        6004: "SPORTS", 6005: "SOCIAL_NETWORKING", 6006: "REFERENCE",
        6007: "PRODUCTIVITY", 6008: "PHOTO_AND_VIDEO", 6009: "NEWS",
        6010: "NAVIGATION", 6011: "MUSIC", 6012: "LIFESTYLE",
        6013: "HEALTH_AND_FITNESS", 6014: "GAMES", 6015: "FINANCE",
        6016: "ENTERTAINMENT", 6017: "EDUCATION", 6018: "BOOKS",
        6020: "MEDICAL"
    }