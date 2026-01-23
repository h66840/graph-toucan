from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for App Store search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - id (int): App Store ID number
        - appId (str): Bundle ID of the app (e.g. 'com.company.app')
        - title (str): Name of the app
        - icon (str): URL to the app's icon image
        - url (str): App Store URL for the app
        - description (str): Detailed description of the app
        - developer (str): Name of the app developer
        - developerUrl (str): App Store URL for the developer's page
        - developerId (int): Unique identifier for the developer on the App Store
        - developerWebsite (str): Official website of the developer
        - genre (str): Primary category name of the app (e.g. 'Social Networking')
        - genreId (int): Primary category ID
        - genres_0 (str): First genre name the app belongs to
        - genreIds_0 (int): First genre ID the app belongs to
        - contentRating (str): Age rating of the app (e.g. '12+')
        - languages_0 (str): First language code supported by the app
        - size (str): App size in bytes as a string
        - requiredOsVersion (str): Minimum iOS version required (e.g. '15.1')
        - released (str): Release date in ISO format
        - updated (str): Last update date in ISO format
        - releaseNotes (str): Notes describing changes in the latest version
        - version (str): Current version string of the app
        - price (float): Price of the app in USD
        - currency (str): Currency code for the price (e.g. 'USD')
        - free (bool): Whether the app is free
        - score (float): Average user rating (0–5)
        - reviews (int): Total number of user reviews
        - currentVersionScore (float): Average rating for the current version
        - currentVersionReviews (int): Number of reviews for the current version
        - screenshots_0 (str): First iPhone screenshot URL
        - ipadScreenshots_0 (str): First iPad screenshot URL
        - appletvScreenshots_0 (str): First Apple TV screenshot URL
        - supportedDevices_0 (str): First supported device identifier
    """
    return {
        "id": 123456789,
        "appId": "com.example.app",
        "title": "Example App",
        "icon": "https://example.com/icon.png",
        "url": "https://apps.apple.com/app/example/id123456789",
        "description": "This is an example app for demonstration purposes.",
        "developer": "Example Company",
        "developerUrl": "https://apps.apple.com/developer/example-company/id987654321",
        "developerId": 987654321,
        "developerWebsite": "https://example.com",
        "genre": "Utilities",
        "genreId": 21,
        "genres_0": "Utilities",
        "genreIds_0": 21,
        "contentRating": "4+",
        "languages_0": "en",
        "size": "123456789",
        "requiredOsVersion": "15.0",
        "released": "2020-01-01T12:00:00Z",
        "updated": "2023-01-01T12:00:00Z",
        "releaseNotes": "Fixed bugs and improved performance.",
        "version": "2.0.1",
        "price": 0.0,
        "currency": "USD",
        "free": True,
        "score": 4.5,
        "reviews": 1234,
        "currentVersionScore": 4.3,
        "currentVersionReviews": 567,
        "screenshots_0": "https://example.com/screenshot1.png",
        "ipadScreenshots_0": "https://example.com/ipad_screenshot1.png",
        "appletvScreenshots_0": "https://example.com/tv_screenshot1.png",
        "supportedDevices_0": "iPhone5s-iPhone5s"
    }

def app_market_intelligence_app_store_search(
    term: str,
    country: Optional[str] = "us",
    idsOnly: Optional[bool] = False,
    lang: Optional[str] = "en-us",
    num: Optional[int] = 50,
    page: Optional[int] = 1
) -> List[Dict[str, Any]]:
    """
    Search for apps on the App Store based on a search term and optional filters.
    
    Args:
        term (str): Search term (required)
        country (str, optional): Two letter country code (default: us)
        idsOnly (bool, optional): Skip extra lookup request. Returns array of application IDs only (default: False)
        lang (str, optional): Language code for result text (default: en-us)
        num (int, optional): Number of results to retrieve (default: 50)
        page (int, optional): Page of results to retrieve (default: 1)
    
    Returns:
        List[Dict[str, Any]]: List of apps with detailed information including:
            - id (int): App Store ID number
            - appId (str): Bundle ID of the app
            - title (str): Name of the app
            - icon (str): URL to the app's icon image
            - url (str): App Store URL for the app
            - description (str): Detailed description of the app
            - developer (str): Name of the app developer
            - developerUrl (str): App Store URL for the developer's page
            - developerId (int): Unique identifier for the developer
            - developerWebsite (str): Official website of the developer
            - genre (str): Primary category name
            - genreId (int): Primary category ID
            - genres (List[str]): List of all genre names
            - genreIds (List[int]): List of all genre IDs
            - contentRating (str): Age rating of the app
            - languages (List[str]): List of language codes supported
            - size (str): App size in bytes as string
            - requiredOsVersion (str): Minimum iOS version required
            - released (str): Release date in ISO format
            - updated (str): Last update date in ISO format
            - releaseNotes (str): Notes describing changes in latest version
            - version (str): Current version string
            - price (float): Price of the app in USD
            - currency (str): Currency code for the price
            - free (bool): Whether the app is free
            - score (float): Average user rating (0–5)
            - reviews (int): Total number of user reviews
            - currentVersionScore (float): Average rating for current version
            - currentVersionReviews (int): Number of reviews for current version
            - screenshots (List[str]): List of iPhone screenshot URLs
            - ipadScreenshots (List[str]): List of iPad screenshot URLs
            - appletvScreenshots (List[str]): List of Apple TV screenshot URLs
            - supportedDevices (List[str]): List of supported device identifiers
    
    Raises:
        ValueError: If term is empty or None
        TypeError: If parameters are of incorrect type
    """
    # Input validation
    if not term:
        raise ValueError("Search term is required")
    
    if not isinstance(term, str):
        raise TypeError("Search term must be a string")
    
    if country and not isinstance(country, str):
        raise TypeError("Country must be a string")
    
    if idsOnly and not isinstance(idsOnly, bool):
        raise TypeError("idsOnly must be a boolean")
    
    if lang and not isinstance(lang, str):
        raise TypeError("Language must be a string")
    
    if num and not isinstance(num, int):
        raise TypeError("Number of results must be an integer")
    
    if page and not isinstance(page, int):
        raise TypeError("Page must be an integer")
    
    if num and num <= 0:
        raise ValueError("Number of results must be positive")
    
    if page and page <= 0:
        raise ValueError("Page number must be positive")
    
    # If idsOnly is True, return only IDs (simulated)
    if idsOnly:
        # Simulate multiple IDs based on term
        base_id = hash(term) % 1000000000
        return [{"id": base_id + i} for i in range(min(num or 50, 50))]
    
    # Call external API to get data
    api_data = call_external_api("app-market-intelligence-app-store-search")
    
    # Construct the full result structure from flat API data
    result = {
        "id": api_data["id"],
        "appId": api_data["appId"],
        "title": api_data["title"],
        "icon": api_data["icon"],
        "url": api_data["url"],
        "description": api_data["description"],
        "developer": api_data["developer"],
        "developerUrl": api_data["developerUrl"],
        "developerId": api_data["developerId"],
        "developerWebsite": api_data["developerWebsite"],
        "genre": api_data["genre"],
        "genreId": api_data["genreId"],
        "genres": [api_data["genres_0"]] if api_data.get("genres_0") else [],
        "genreIds": [api_data["genreIds_0"]] if api_data.get("genreIds_0") else [],
        "contentRating": api_data["contentRating"],
        "languages": [api_data["languages_0"]] if api_data.get("languages_0") else [],
        "size": api_data["size"],
        "requiredOsVersion": api_data["requiredOsVersion"],
        "released": api_data["released"],
        "updated": api_data["updated"],
        "releaseNotes": api_data["releaseNotes"],
        "version": api_data["version"],
        "price": api_data["price"],
        "currency": api_data["currency"],
        "free": api_data["free"],
        "score": api_data["score"],
        "reviews": api_data["reviews"],
        "currentVersionScore": api_data["currentVersionScore"],
        "currentVersionReviews": api_data["currentVersionReviews"],
        "screenshots": [api_data["screenshots_0"]] if api_data.get("screenshots_0") else [],
        "ipadScreenshots": [api_data["ipadScreenshots_0"]] if api_data.get("ipadScreenshots_0") else [],
        "appletvScreenshots": [api_data["appletvScreenshots_0"]] if api_data.get("appletvScreenshots_0") else [],
        "supportedDevices": [api_data["supportedDevices_0"]] if api_data.get("supportedDevices_0") else []
    }
    
    # Return list with one item (simulating search results)
    return [result]