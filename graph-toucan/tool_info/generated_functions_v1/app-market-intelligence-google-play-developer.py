from typing import Dict, List, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Play developer app listing.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - app_0_url (str): Play Store URL of first app
        - app_0_appId (str): Package name of first app
        - app_0_title (str): Title of first app
        - app_0_summary (str): Short description of first app
        - app_0_developer (str): Developer name of first app
        - app_0_developerId (str): Developer ID of first app
        - app_0_icon (str): Icon image URL of first app
        - app_0_score (float): Rating score (0-5) of first app
        - app_0_scoreText (str): Display text for rating of first app
        - app_0_priceText (str): Price display text of first app
        - app_0_free (bool): Whether first app is free
        - app_1_url (str): Play Store URL of second app
        - app_1_appId (str): Package name of second app
        - app_1_title (str): Title of second app
        - app_1_summary (str): Short description of second app
        - app_1_developer (str): Developer name of second app
        - app_1_developerId (str): Developer ID of second app
        - app_1_icon (str): Icon image URL of second app
        - app_1_score (float): Rating score (0-5) of second app
        - app_1_scoreText (str): Display text for rating of second app
        - app_1_priceText (str): Price display text of second app
        - app_1_free (bool): Whether second app is free
        - total_count (int): Total number of apps found
        - country (str): Country code used in query
        - language (str): Language code used in response
        - has_more (bool): Whether more results are available
        - request_metadata_timestamp (str): ISO format timestamp of request
        - request_metadata_fullDetail (bool): Whether full details were requested
        - request_metadata_num_requested (int): Number of results requested
    """
    return {
        "app_0_url": "https://play.google.com/store/apps/details?id=com.example.game1",
        "app_0_appId": "com.example.game1",
        "app_0_title": "Example Game 1",
        "app_0_summary": "An exciting puzzle adventure game with colorful graphics.",
        "app_0_developer": "DxCo Games",
        "app_0_developerId": "DxCo+Games",
        "app_0_icon": "https://play-lh.googleusercontent.com/app-icons/480/com.example.game1.jpg",
        "app_0_score": 4.5,
        "app_0_scoreText": "4.5",
        "app_0_priceText": "Free",
        "app_0_free": True,
        "app_1_url": "https://play.google.com/store/apps/details?id=com.example.game2",
        "app_1_appId": "com.example.game2",
        "app_1_title": "Example Game 2",
        "app_1_summary": "Fast-paced racing game with realistic physics.",
        "app_1_developer": "DxCo Games",
        "app_1_developerId": "DxCo+Games",
        "app_1_icon": "https://play-lh.googleusercontent.com/app-icons/480/com.example.game2.jpg",
        "app_1_score": 4.2,
        "app_1_scoreText": "4.2",
        "app_1_priceText": "Free",
        "app_1_free": True,
        "total_count": 42,
        "country": "us",
        "language": "en",
        "has_more": True,
        "request_metadata_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "request_metadata_fullDetail": False,
        "request_metadata_num_requested": 60,
    }


def app_market_intelligence_google_play_developer(
    devId: str,
    country: Optional[str] = "us",
    lang: Optional[str] = "en",
    fullDetail: Optional[bool] = False,
    num: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Get apps by a developer on Google Play.

    Args:
        devId (str): Developer name (e.g., 'DxCo Games') - required
        country (str, optional): Country code to get results from (default: 'us')
        lang (str, optional): Language code for result text (default: 'en')
        fullDetail (bool, optional): Include full app details in results (default: False)
        num (int, optional): Number of results to retrieve (default: 60)

    Returns:
        Dict containing:
        - apps (List[Dict]): List of app objects with details such as title, appId, URL, rating, pricing, and developer info.
        - total_count (int): Total number of apps found for the developer
        - country (str): Country code used for the query
        - language (str): Language code used for the response text
        - has_more (bool): Indicates if more results are available beyond the current limit
        - request_metadata (Dict): Metadata about the request including timestamp, fullDetail flag, and result count limit.

    Raises:
        ValueError: If devId is not provided
    """
    if not devId:
        raise ValueError("devId is required")

    # Validate and sanitize inputs
    country = country.lower() if country else "us"
    lang = lang.lower() if lang else "en"
    fullDetail = bool(fullDetail)
    num = int(num) if num and num > 0 else 60

    # Call external API (simulated)
    api_data = call_external_api("app-market-intelligence-google-play-developer")

    # Construct apps list from flattened API response
    apps = []
    for i in range(2):  # We only have 2 items from the simulated API
        app_key_prefix = f"app_{i}"
        if f"{app_key_prefix}_appId" not in api_data:
            continue

        app = {
            "url": api_data.get(f"{app_key_prefix}_url", ""),
            "appId": api_data.get(f"{app_key_prefix}_appId", ""),
            "title": api_data.get(f"{app_key_prefix}_title", ""),
            "summary": api_data.get(f"{app_key_prefix}_summary", ""),
            "developer": api_data.get(f"{app_key_prefix}_developer", ""),
            "developerId": api_data.get(f"{app_key_prefix}_developerId", ""),
            "icon": api_data.get(f"{app_key_prefix}_icon", ""),
            "score": float(api_data.get(f"{app_key_prefix}_score", 0.0)),
            "scoreText": api_data.get(f"{app_key_prefix}_scoreText", ""),
            "priceText": api_data.get(f"{app_key_prefix}_priceText", ""),
            "free": bool(api_data.get(f"{app_key_prefix}_free", True)),
        }
        apps.append(app)

    # Construct final result matching output schema
    result = {
        "apps": apps,
        "total_count": int(api_data.get("total_count", 0)),
        "country": str(api_data.get("country", country)),
        "language": str(api_data.get("language", lang)),
        "has_more": bool(api_data.get("has_more", False)),
        "request_metadata": {
            "timestamp": str(api_data.get("request_metadata_timestamp", "")),
            "fullDetail": bool(api_data.get("request_metadata_fullDetail", fullDetail)),
            "num_requested": int(api_data.get("request_metadata_num_requested", num)),
        }
    }

    return result