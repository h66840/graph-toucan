from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Play app search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_title (str): Title of the first app result
        - result_0_appId (str): Package name of the first app
        - result_0_url (str): Play Store URL of the first app
        - result_0_icon (str): Icon image URL of the first app
        - result_0_developer (str): Developer name of the first app
        - result_0_developerId (str): Developer ID of the first app
        - result_0_priceText (str): Price display text of the first app
        - result_0_free (bool): Whether the first app is free
        - result_0_summary (str): Short description of the first app
        - result_0_scoreText (str): Rating display text of the first app
        - result_0_score (float): Rating score (0-5) of the first app
        - result_1_title (str): Title of the second app result
        - result_1_appId (str): Package name of the second app
        - result_1_url (str): Play Store URL of the second app
        - result_1_icon (str): Icon image URL of the second app
        - result_1_developer (str): Developer name of the second app
        - result_1_developerId (str): Developer ID of the second app
        - result_1_priceText (str): Price display text of the second app
        - result_1_free (bool): Whether the second app is free
        - result_1_summary (str): Short description of the second app
        - result_1_scoreText (str): Rating display text of the second app
        - result_1_score (float): Rating score (0-5) of the second app
    """
    return {
        "result_0_title": "Example App Free",
        "result_0_appId": "com.example.freeapp",
        "result_0_url": "https://play.google.com/store/apps/details?id=com.example.freeapp",
        "result_0_icon": "https://example.com/icon1.png",
        "result_0_developer": "Example Developer Inc.",
        "result_0_developerId": "ExampleDevInc",
        "result_0_priceText": "Free",
        "result_0_free": True,
        "result_0_summary": "A great example app that does amazing things for free.",
        "result_0_scoreText": "4.5",
        "result_0_score": 4.5,
        "result_1_title": "Example App Pro",
        "result_1_appId": "com.example.proapp",
        "result_1_url": "https://play.google.com/store/apps/details?id=com.example.proapp",
        "result_1_icon": "https://example.com/icon2.png",
        "result_1_developer": "Example Developer Inc.",
        "result_1_developerId": "ExampleDevInc",
        "result_1_priceText": "$4.99",
        "result_1_free": False,
        "result_1_summary": "Premium version with advanced features and no ads.",
        "result_1_scoreText": "4.8",
        "result_1_score": 4.8,
    }

def app_market_intelligence_google_play_search(
    term: str,
    country: Optional[str] = "us",
    fullDetail: Optional[bool] = False,
    lang: Optional[str] = "en",
    num: Optional[int] = 20,
    price: Optional[str] = "all"
) -> Dict[str, Any]:
    """
    Search for apps on Google Play using simulated external API call.
    
    Args:
        term (str): Search term to query apps (required)
        country (str, optional): Country code to get results from (default: us)
        fullDetail (bool, optional): Include full app details in results (default: false)
        lang (str, optional): Language code for result text (default: en)
        num (int, optional): Number of results to retrieve (default: 20, max: 250)
        price (str, optional): Filter by price: all, free, or paid (default: all)
    
    Returns:
        Dict containing a list of app search results with the following structure:
        - results (List[Dict]): list of app search results, each containing:
            - title (str): App name
            - appId (str): Package name
            - url (str): Play Store URL
            - icon (str): Icon image URL
            - developer (str): Developer name
            - developerId (str): Developer ID
            - priceText (str): Price display text
            - free (bool): Boolean indicating if app is free
            - summary (str): Short description
            - scoreText (str): Rating display text
            - score (float): Rating (0-5)
    
    Raises:
        ValueError: If required term is empty or invalid price filter is provided
    """
    # Input validation
    if not term or not term.strip():
        raise ValueError("Search term is required and cannot be empty")
    
    if price not in ["all", "free", "paid"]:
        raise ValueError("Price filter must be one of: all, free, paid")
    
    if num is not None and (num <= 0 or num > 250):
        raise ValueError("Number of results must be between 1 and 250")
    
    # Call external API to get flat data
    api_data = call_external_api("app-market-intelligence-google-play-search")
    
    # Construct results list from flattened API response
    results = [
        {
            "title": api_data["result_0_title"],
            "appId": api_data["result_0_appId"],
            "url": api_data["result_0_url"],
            "icon": api_data["result_0_icon"],
            "developer": api_data["result_0_developer"],
            "developerId": api_data["result_0_developerId"],
            "priceText": api_data["result_0_priceText"],
            "free": api_data["result_0_free"],
            "summary": api_data["result_0_summary"],
            "scoreText": api_data["result_0_scoreText"],
            "score": api_data["result_0_score"]
        },
        {
            "title": api_data["result_1_title"],
            "appId": api_data["result_1_appId"],
            "url": api_data["result_1_url"],
            "icon": api_data["result_1_icon"],
            "developer": api_data["result_1_developer"],
            "developerId": api_data["result_1_developerId"],
            "priceText": api_data["result_1_priceText"],
            "free": api_data["result_1_free"],
            "summary": api_data["result_1_summary"],
            "scoreText": api_data["result_1_scoreText"],
            "score": api_data["result_1_score"]
        }
    ]
    
    # Apply price filtering if specified
    if price == "free":
        results = [app for app in results if app["free"]]
    elif price == "paid":
        results = [app for app in results if not app["free"]]
    
    # Limit number of results based on num parameter
    if num is not None:
        results = results[:min(num, len(results))]
    
    return {"results": results}