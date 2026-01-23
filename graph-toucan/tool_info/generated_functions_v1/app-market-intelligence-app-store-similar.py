from typing import Dict, List, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching similar apps data from external App Store API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - similar_app_0_id (int): App Store ID of first similar app
        - similar_app_0_appId (str): Bundle ID of first similar app
        - similar_app_0_title (str): Title of first similar app
        - similar_app_0_icon (str): Icon URL of first similar app
        - similar_app_0_url (str): App Store URL of first similar app
        - similar_app_0_price (float): Price in USD of first similar app
        - similar_app_0_currency (str): Currency code of first similar app
        - similar_app_0_free (bool): Whether first similar app is free
        - similar_app_0_description (str): Description of first similar app
        - similar_app_0_developer (str): Developer name of first similar app
        - similar_app_0_developerUrl (str): Developer URL of first similar app
        - similar_app_0_developerId (int): Developer ID of first similar app
        - similar_app_0_genre (str): Genre name of first similar app
        - similar_app_0_genreId (int): Genre ID of first similar app
        - similar_app_0_released (str): Release date (ISO format) of first similar app
        - similar_app_1_id (int): App Store ID of second similar app
        - similar_app_1_appId (str): Bundle ID of second similar app
        - similar_app_1_title (str): Title of second similar app
        - similar_app_1_icon (str): Icon URL of second similar app
        - similar_app_1_url (str): App Store URL of second similar app
        - similar_app_1_price (float): Price in USD of second similar app
        - similar_app_1_currency (str): Currency code of second similar app
        - similar_app_1_free (bool): Whether second similar app is free
        - similar_app_1_description (str): Description of second similar app
        - similar_app_1_developer (str): Developer name of second similar app
        - similar_app_1_developerUrl (str): Developer URL of second similar app
        - similar_app_1_developerId (int): Developer ID of second similar app
        - similar_app_1_genre (str): Genre name of second similar app
        - similar_app_1_genreId (int): Genre ID of second similar app
        - similar_app_1_released (str): Release date (ISO format) of second similar app
        - total_count (int): Total number of similar apps returned
        - metadata_query_source (str): Which parameter was used ('appId' or 'id')
        - metadata_timestamp (str): ISO timestamp of request
        - metadata_store_source (str): Store source ('App Store')
    """
    return {
        "similar_app_0_id": 987654321,
        "similar_app_0_appId": "com.example.similarapp1",
        "similar_app_0_title": "Similar App One",
        "similar_app_0_icon": "https://example.com/icon1.png",
        "similar_app_0_url": "https://apps.apple.com/app/id987654321",
        "similar_app_0_price": 0.0,
        "similar_app_0_currency": "USD",
        "similar_app_0_free": True,
        "similar_app_0_description": "A great similar app with amazing features.",
        "similar_app_0_developer": "Example Developer One",
        "similar_app_0_developerUrl": "https://apps.apple.com/developer/id123456",
        "similar_app_0_developerId": 123456,
        "similar_app_0_genre": "Games",
        "similar_app_0_genreId": 6014,
        "similar_app_0_released": "2022-01-15T10:00:00Z",
        "similar_app_1_id": 876543210,
        "similar_app_1_appId": "com.example.similarapp2",
        "similar_app_1_title": "Similar App Two",
        "similar_app_1_icon": "https://example.com/icon2.png",
        "similar_app_1_url": "https://apps.apple.com/app/id876543210",
        "similar_app_1_price": 4.99,
        "similar_app_1_currency": "USD",
        "similar_app_1_free": False,
        "similar_app_1_description": "Another fantastic similar application.",
        "similar_app_1_developer": "Example Developer Two",
        "similar_app_1_developerUrl": "https://apps.apple.com/developer/id789012",
        "similar_app_1_developerId": 789012,
        "similar_app_1_genre": "Productivity",
        "similar_app_1_genreId": 6018,
        "similar_app_1_released": "2021-11-20T14:30:00Z",
        "total_count": 2,
        "metadata_query_source": "appId",
        "metadata_timestamp": datetime.datetime.now().isoformat(),
        "metadata_store_source": "App Store"
    }

def app_market_intelligence_app_store_similar(appId: Optional[str] = None, id: Optional[int] = None) -> Dict[str, Any]:
    """
    Get similar apps ('customers also bought') from the App Store.
    
    Either appId or id must be provided to identify the source app.
    
    Args:
        appId (Optional[str]): Bundle ID (e.g., 'com.company.app'). Either this or id must be provided.
        id (Optional[int]): Numeric App ID (e.g., 553834731). Either this or appId must be provided.
    
    Returns:
        Dict containing:
        - similar_apps (List[Dict]): List of app objects with details such as id, appId, title, icon, url,
          price, currency, free status, description, developer, developerUrl, developerId, genre, genreId, and released date
        - total_count (int): Total number of similar apps returned
        - metadata (Dict): Additional context about the response including query source (appId or id used),
          timestamp of request, and store source ('App Store')
    
    Raises:
        ValueError: If neither appId nor id is provided
    """
    if not appId and not id:
        raise ValueError("Either appId or id must be provided")
    
    # Determine query source
    query_source = "appId" if appId else "id"
    
    # Call external API to get flattened data
    api_data = call_external_api("app-market-intelligence-app-store-similar")
    
    # Construct similar_apps list from indexed fields
    similar_apps = [
        {
            "id": api_data["similar_app_0_id"],
            "appId": api_data["similar_app_0_appId"],
            "title": api_data["similar_app_0_title"],
            "icon": api_data["similar_app_0_icon"],
            "url": api_data["similar_app_0_url"],
            "price": api_data["similar_app_0_price"],
            "currency": api_data["similar_app_0_currency"],
            "free": api_data["similar_app_0_free"],
            "description": api_data["similar_app_0_description"],
            "developer": api_data["similar_app_0_developer"],
            "developerUrl": api_data["similar_app_0_developerUrl"],
            "developerId": api_data["similar_app_0_developerId"],
            "genre": api_data["similar_app_0_genre"],
            "genreId": api_data["similar_app_0_genreId"],
            "released": api_data["similar_app_0_released"]
        },
        {
            "id": api_data["similar_app_1_id"],
            "appId": api_data["similar_app_1_appId"],
            "title": api_data["similar_app_1_title"],
            "icon": api_data["similar_app_1_icon"],
            "url": api_data["similar_app_1_url"],
            "price": api_data["similar_app_1_price"],
            "currency": api_data["similar_app_1_currency"],
            "free": api_data["similar_app_1_free"],
            "description": api_data["similar_app_1_description"],
            "developer": api_data["similar_app_1_developer"],
            "developerUrl": api_data["similar_app_1_developerUrl"],
            "developerId": api_data["similar_app_1_developerId"],
            "genre": api_data["similar_app_1_genre"],
            "genreId": api_data["similar_app_1_genreId"],
            "released": api_data["similar_app_1_released"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "query_source": api_data["metadata_query_source"],
        "timestamp": api_data["metadata_timestamp"],
        "store_source": api_data["metadata_store_source"]
    }
    
    # Return final structured response
    return {
        "similar_apps": similar_apps,
        "total_count": api_data["total_count"],
        "metadata": metadata
    }