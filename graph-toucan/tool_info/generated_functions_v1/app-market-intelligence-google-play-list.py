from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Play app listings.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - app_0_appId (str): Package name of first app
        - app_0_title (str): Title of first app
        - app_0_url (str): Play Store URL of first app
        - app_0_summary (str): Short description of first app
        - app_0_developer (str): Developer name of first app
        - app_0_developerId (str): Developer ID of first app
        - app_0_icon (str): Icon URL of first app
        - app_0_score (float): Rating (0-5) of first app
        - app_0_scoreText (str): Rating display text of first app
        - app_0_priceText (str): Price display text of first app
        - app_0_free (bool): Whether first app is free
        - app_1_appId (str): Package name of second app
        - app_1_title (str): Title of second app
        - app_1_url (str): Play Store URL of second app
        - app_1_summary (str): Short description of second app
        - app_1_developer (str): Developer name of second app
        - app_1_developerId (str): Developer ID of second app
        - app_1_icon (str): Icon URL of second app
        - app_1_score (float): Rating (0-5) of second app
        - app_1_scoreText (str): Rating display text of second app
        - app_1_priceText (str): Price display text of second app
        - app_1_free (bool): Whether second app is free
        - total_count (int): Total number of apps returned
        - collection (str): Collection type queried
        - category (str): Category filtered by
        - country (str): Country code used
        - language (str): Language code used
        - full_detail_requested (bool): Whether full details were requested
        - metadata_timestamp (str): Timestamp of request
        - metadata_source_platform (str): Source platform name
        - metadata_disclaimer (str): Disclaimer from data source
    """
    return {
        "app_0_appId": "com.example.game",
        "app_0_title": "Example Game",
        "app_0_url": "https://play.google.com/store/apps/details?id=com.example.game",
        "app_0_summary": "An exciting example game with fun gameplay.",
        "app_0_developer": "Example Games Studio",
        "app_0_developerId": "ExampleGamesStudio",
        "app_0_icon": "https://example.com/icon1.png",
        "app_0_score": 4.5,
        "app_0_scoreText": "4.5",
        "app_0_priceText": "Free",
        "app_0_free": True,
        "app_1_appId": "com.example.tool",
        "app_1_title": "Example Tool",
        "app_1_url": "https://play.google.com/store/apps/details?id=com.example.tool",
        "app_1_summary": "A useful tool for everyday tasks.",
        "app_1_developer": "Example Tools Inc",
        "app_1_developerId": "ExampleToolsInc",
        "app_1_icon": "https://example.com/icon2.png",
        "app_1_score": 4.2,
        "app_1_scoreText": "4.2",
        "app_1_priceText": "$2.99",
        "app_1_free": False,
        "total_count": 2,
        "collection": "TOP_FREE",
        "category": "GAME",
        "country": "us",
        "language": "en",
        "full_detail_requested": False,
        "metadata_timestamp": "2023-10-01T12:00:00Z",
        "metadata_source_platform": "Google Play",
        "metadata_disclaimer": "Data is simulated for demonstration purposes."
    }

def app_market_intelligence_google_play_list(
    age: Optional[str] = None,
    category: Optional[str] = None,
    collection: Optional[str] = None,
    country: Optional[str] = None,
    fullDetail: Optional[bool] = None,
    lang: Optional[str] = None,
    num: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get apps from Google Play collections. Returns a list of apps with metadata.
    
    Args:
        age (Optional[str]): Age range filter (only for FAMILY category). Options: FIVE_UNDER, SIX_EIGHT, NINE_UP
        category (Optional[str]): Category to filter by. See available categories in tool description.
        collection (Optional[str]): Collection to fetch apps from. Default: TOP_FREE.
            Options: TOP_FREE, TOP_PAID, GROSSING
        country (Optional[str]): Country code to get results from. Default: us
        fullDetail (Optional[bool]): Include full app details in results. Default: False
        lang (Optional[str]): Language code for result text. Default: en
        num (Optional[int]): Number of apps to retrieve. Default: 500
    
    Returns:
        Dict containing:
        - apps (List[Dict]): List of app objects with details
        - total_count (int): Total number of apps returned
        - collection (str): The collection type that was queried
        - category (str): The category filtered by
        - country (str): The country code used
        - language (str): The language code used
        - full_detail_requested (bool): Whether full details were requested
        - metadata (Dict): Additional contextual information about the response
    """
    # Set default values
    collection = collection or "TOP_FREE"
    country = country or "us"
    lang = lang or "en"
    fullDetail = fullDetail if fullDetail is not None else False
    num = num or 500
    
    # Validate inputs
    valid_collections = ["TOP_FREE", "TOP_PAID", "GROSSING"]
    if collection and collection not in valid_collections:
        raise ValueError(f"collection must be one of {valid_collections}")
    
    valid_ages = ["FIVE_UNDER", "SIX_EIGHT", "NINE_UP"]
    if age and age not in valid_ages:
        raise ValueError(f"age must be one of {valid_ages}")
    
    # Call external API (simulated)
    api_data = call_external_api("app-market-intelligence-google-play-list")
    
    # Construct apps list from flattened API response
    apps = [
        {
            "appId": api_data["app_0_appId"],
            "title": api_data["app_0_title"],
            "url": api_data["app_0_url"],
            "summary": api_data["app_0_summary"],
            "developer": api_data["app_0_developer"],
            "developerId": api_data["app_0_developerId"],
            "icon": api_data["app_0_icon"],
            "score": api_data["app_0_score"],
            "scoreText": api_data["app_0_scoreText"],
            "priceText": api_data["app_0_priceText"],
            "free": api_data["app_0_free"]
        },
        {
            "appId": api_data["app_1_appId"],
            "title": api_data["app_1_title"],
            "url": api_data["app_1_url"],
            "summary": api_data["app_1_summary"],
            "developer": api_data["app_1_developer"],
            "developerId": api_data["app_1_developerId"],
            "icon": api_data["app_1_icon"],
            "score": api_data["app_1_score"],
            "scoreText": api_data["app_1_scoreText"],
            "priceText": api_data["app_1_priceText"],
            "free": api_data["app_1_free"]
        }
    ]
    
    # Apply num limit
    apps = apps[:num]
    
    # Construct final result
    result = {
        "apps": apps,
        "total_count": api_data["total_count"],
        "collection": api_data["collection"],
        "category": api_data["category"],
        "country": api_data["country"],
        "language": api_data["language"],
        "full_detail_requested": api_data["full_detail_requested"],
        "metadata": {
            "timestamp": api_data["metadata_timestamp"],
            "source_platform": api_data["metadata_source_platform"],
            "disclaimer": api_data["metadata_disclaimer"]
        }
    }
    
    return result