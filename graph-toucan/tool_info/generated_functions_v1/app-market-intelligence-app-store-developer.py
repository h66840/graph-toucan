from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for App Store developer apps.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - app_0_id (int): App Store ID of first app
        - app_0_appId (str): Bundle ID of first app
        - app_0_title (str): Name of first app
        - app_0_icon (str): URL to icon image of first app
        - app_0_url (str): App Store URL of first app
        - app_0_price (float): Price in USD of first app
        - app_0_currency (str): Currency code of first app
        - app_0_free (bool): Whether first app is free
        - app_0_description (str): Description of first app
        - app_0_developer (str): Developer name of first app
        - app_0_developerUrl (str): Developer's App Store URL of first app
        - app_0_developerId (str): Developer's iTunes artist ID of first app
        - app_0_genre (str): Category name of first app
        - app_0_genreId (str): Category ID of first app
        - app_0_released (str): Release date (ISO format) of first app
        - app_1_id (int): App Store ID of second app
        - app_1_appId (str): Bundle ID of second app
        - app_1_title (str): Name of second app
        - app_1_icon (str): URL to icon image of second app
        - app_1_url (str): App Store URL of second app
        - app_1_price (float): Price in USD of second app
        - app_1_currency (str): Currency code of second app
        - app_1_free (bool): Whether second app is free
        - app_1_description (str): Description of second app
        - app_1_developer (str): Developer name of second app
        - app_1_developerUrl (str): Developer's App Store URL of second app
        - app_1_developerId (str): Developer's iTunes artist ID of second app
        - app_1_genre (str): Category name of second app
        - app_1_genreId (str): Category ID of second app
        - app_1_released (str): Release date (ISO format) of second app
        - total_count (int): Total number of apps returned
        - developer_name (str): Name of the developer
        - developer_id (str): iTunes artist ID of the developer
        - country (str): Country code used
        - language (str): Language code used
        - fetched_at (str): Timestamp when data was fetched (ISO format)
    """
    return {
        "app_0_id": 123456789,
        "app_0_appId": "com.example.app1",
        "app_0_title": "Example App One",
        "app_0_icon": "https://example.com/icon1.png",
        "app_0_url": "https://apps.apple.com/us/app/example-app-one/id123456789",
        "app_0_price": 0.0,
        "app_0_currency": "USD",
        "app_0_free": True,
        "app_0_description": "This is an example app for demonstration purposes.",
        "app_0_developer": "Example Developer Inc.",
        "app_0_developerUrl": "https://apps.apple.com/us/developer/example-developer/id284882218",
        "app_0_developerId": "284882218",
        "app_0_genre": "Productivity",
        "app_0_genreId": "6018",
        "app_0_released": "2020-01-15T08:00:00Z",
        "app_1_id": 987654321,
        "app_1_appId": "com.example.app2",
        "app_1_title": "Example App Two",
        "app_1_icon": "https://example.com/icon2.png",
        "app_1_url": "https://apps.apple.com/us/app/example-app-two/id987654321",
        "app_1_price": 4.99,
        "app_1_currency": "USD",
        "app_1_free": False,
        "app_1_description": "Another example app with premium features.",
        "app_1_developer": "Example Developer Inc.",
        "app_1_developerUrl": "https://apps.apple.com/us/developer/example-developer/id284882218",
        "app_1_developerId": "284882218",
        "app_1_genre": "Entertainment",
        "app_1_genreId": "6011",
        "app_1_released": "2021-03-22T10:30:00Z",
        "total_count": 2,
        "developer_name": "Example Developer Inc.",
        "developer_id": "284882218",
        "country": "us",
        "language": "en",
        "fetched_at": datetime.utcnow().isoformat() + "Z"
    }

def app_market_intelligence_app_store_developer(
    devId: str,
    country: Optional[str] = "us",
    lang: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get apps by a developer on the App Store.

    Args:
        devId (str): iTunes artist ID of the developer (required)
        country (str, optional): Country code to get app details from (default: us)
        lang (str, optional): Language code for result text. If not provided, uses country-specific language.

    Returns:
        Dict containing:
        - apps (List[Dict]): List of app details with keys: 'id', 'appId', 'title', 'icon', 'url', 'price',
          'currency', 'free', 'description', 'developer', 'developerUrl', 'developerId', 'genre',
          'genreId', 'released'
        - total_count (int): Total number of apps returned
        - developer_name (str): Name of the developer
        - developer_id (str): iTunes artist ID of the developer
        - country (str): Country code used
        - language (str): Language code used
        - fetched_at (str): Timestamp when data was fetched (ISO format)

    Raises:
        ValueError: If devId is not provided
    """
    if not devId:
        raise ValueError("devId is required")

    # Set default country and language
    resolved_country = country or "us"
    resolved_lang = lang or ("en" if resolved_country == "us" else resolved_country)

    # Call external API (simulation)
    api_data = call_external_api("app-market-intelligence-app-store-developer")

    # Construct apps list from indexed fields
    apps = [
        {
            "id": api_data["app_0_id"],
            "appId": api_data["app_0_appId"],
            "title": api_data["app_0_title"],
            "icon": api_data["app_0_icon"],
            "url": api_data["app_0_url"],
            "price": api_data["app_0_price"],
            "currency": api_data["app_0_currency"],
            "free": api_data["app_0_free"],
            "description": api_data["app_0_description"],
            "developer": api_data["app_0_developer"],
            "developerUrl": api_data["app_0_developerUrl"],
            "developerId": api_data["app_0_developerId"],
            "genre": api_data["app_0_genre"],
            "genreId": api_data["app_0_genreId"],
            "released": api_data["app_0_released"]
        },
        {
            "id": api_data["app_1_id"],
            "appId": api_data["app_1_appId"],
            "title": api_data["app_1_title"],
            "icon": api_data["app_1_icon"],
            "url": api_data["app_1_url"],
            "price": api_data["app_1_price"],
            "currency": api_data["app_1_currency"],
            "free": api_data["app_1_free"],
            "description": api_data["app_1_description"],
            "developer": api_data["app_1_developer"],
            "developerUrl": api_data["app_1_developerUrl"],
            "developerId": api_data["app_1_developerId"],
            "genre": api_data["app_1_genre"],
            "genreId": api_data["app_1_genreId"],
            "released": api_data["app_1_released"]
        }
    ]

    # Construct final result
    result = {
        "apps": apps,
        "total_count": api_data["total_count"],
        "developer_name": api_data["developer_name"],
        "developer_id": api_data["developer_id"],
        "country": api_data["country"],
        "language": api_data["language"],
        "fetched_at": api_data["fetched_at"]
    }

    return result