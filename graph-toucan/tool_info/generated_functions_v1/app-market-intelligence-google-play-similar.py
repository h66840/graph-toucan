from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching similar apps data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - similar_app_0_url (str): Play Store URL of first similar app
        - similar_app_0_appId (str): Package name of first similar app
        - similar_app_0_summary (str): Short description of first similar app
        - similar_app_0_developer (str): Developer name of first similar app
        - similar_app_0_developerId (str): Developer ID of first similar app
        - similar_app_0_icon (str): Icon image URL of first similar app
        - similar_app_0_score (float): Rating (0-5) of first similar app
        - similar_app_0_scoreText (str): Rating display text of first similar app
        - similar_app_0_priceText (str): Price display text of first similar app
        - similar_app_0_free (bool): Whether first similar app is free
        - similar_app_1_url (str): Play Store URL of second similar app
        - similar_app_1_appId (str): Package name of second similar app
        - similar_app_1_summary (str): Short description of second similar app
        - similar_app_1_developer (str): Developer name of second similar app
        - similar_app_1_developerId (str): Developer ID of second similar app
        - similar_app_1_icon (str): Icon image URL of second similar app
        - similar_app_1_score (float): Rating (0-5) of second similar app
        - similar_app_1_scoreText (str): Rating display text of second similar app
        - similar_app_1_priceText (str): Price display text of second similar app
        - similar_app_1_free (bool): Whether second similar app is free
        - total_count (int): Total number of similar apps returned
        - metadata_country (str): Country code used in query
        - metadata_lang (str): Language code used in query
        - metadata_fullDetail (bool): Whether full details were requested
    """
    return {
        "similar_app_0_url": "https://play.google.com/store/apps/details?id=com.example.similar1",
        "similar_app_0_appId": "com.example.similar1",
        "similar_app_0_summary": "A popular game similar to the input app",
        "similar_app_0_developer": "Example Games Inc.",
        "similar_app_0_developerId": "ExampleGamesDev",
        "similar_app_0_icon": "https://example.com/icon1.png",
        "similar_app_0_score": 4.5,
        "similar_app_0_scoreText": "4.5",
        "similar_app_0_priceText": "Free",
        "similar_app_0_free": True,
        "similar_app_1_url": "https://play.google.com/store/apps/details?id=com.example.similar2",
        "similar_app_1_appId": "com.example.similar2",
        "similar_app_1_summary": "Another great app in the same category",
        "similar_app_1_developer": "Fun Apps Studio",
        "similar_app_1_developerId": "FunAppsDev",
        "similar_app_1_icon": "https://example.com/icon2.png",
        "similar_app_1_score": 4.2,
        "similar_app_1_scoreText": "4.2",
        "similar_app_1_priceText": "Free",
        "similar_app_1_free": True,
        "total_count": 2,
        "metadata_country": "us",
        "metadata_lang": "en",
        "metadata_fullDetail": False
    }

def app_market_intelligence_google_play_similar(
    appId: str, 
    country: Optional[str] = "us", 
    fullDetail: Optional[bool] = False, 
    lang: Optional[str] = "en"
) -> Dict[str, Any]:
    """
    Get similar apps from Google Play based on a given app ID.
    
    Args:
        appId (str): Google Play package name (e.g., 'com.dxco.pandavszombies')
        country (str, optional): Country code to get results from (default: us)
        fullDetail (bool, optional): Include full app details in results (default: False)
        lang (str, optional): Language code for result text (default: en)
    
    Returns:
        Dict containing:
        - similar_apps (List[Dict]): List of similar app entries with details like url, appId, summary, etc.
        - total_count (int): Total number of similar apps returned
        - metadata (Dict): Query context info including country, lang, and fullDetail status
    
    Raises:
        ValueError: If appId is empty or None
    """
    if not appId:
        raise ValueError("appId is required and cannot be empty")
    
    # Call external API to get flattened data
    api_data = call_external_api("app-market-intelligence-google-play-similar")
    
    # Construct similar_apps list from indexed fields
    similar_apps = [
        {
            "url": api_data["similar_app_0_url"],
            "appId": api_data["similar_app_0_appId"],
            "summary": api_data["similar_app_0_summary"],
            "developer": api_data["similar_app_0_developer"],
            "developerId": api_data["similar_app_0_developerId"],
            "icon": api_data["similar_app_0_icon"],
            "score": api_data["similar_app_0_score"],
            "scoreText": api_data["similar_app_0_scoreText"],
            "priceText": api_data["similar_app_0_priceText"],
            "free": api_data["similar_app_0_free"]
        },
        {
            "url": api_data["similar_app_1_url"],
            "appId": api_data["similar_app_1_appId"],
            "summary": api_data["similar_app_1_summary"],
            "developer": api_data["similar_app_1_developer"],
            "developerId": api_data["similar_app_1_developerId"],
            "icon": api_data["similar_app_1_icon"],
            "score": api_data["similar_app_1_score"],
            "scoreText": api_data["similar_app_1_scoreText"],
            "priceText": api_data["similar_app_1_priceText"],
            "free": api_data["similar_app_1_free"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "country": api_data["metadata_country"],
        "lang": api_data["metadata_lang"],
        "fullDetail": api_data["metadata_fullDetail"]
    }
    
    # Return final structured result
    return {
        "similar_apps": similar_apps,
        "total_count": api_data["total_count"],
        "metadata": metadata
    }