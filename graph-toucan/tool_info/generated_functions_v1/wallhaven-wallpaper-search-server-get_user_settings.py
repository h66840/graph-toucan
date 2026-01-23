from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wallhaven user settings.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - user_id (str): Unique identifier of the authenticated user
        - username (str): Username of the authenticated user
        - email (str): Email address associated with the user account
        - account_level (int): User's account level (e.g., 0 = basic, 1 = premium)
        - api_key_enabled (bool): Whether the user has API key access enabled
        - default_purity_0 (str): First default content filter (e.g., 'sfw')
        - default_purity_1 (str): Second default content filter (e.g., 'sketchy')
        - default_category (str): Default wallpaper category preference
        - default_sorting (str): Default sorting method for search results
        - default_order (str): Order direction for sorting: 'desc' or 'asc'
        - avatar_url (str): URL to the user's profile avatar image
        - background_url (str): URL to the user's profile background image
        - created_at (str): Timestamp when the user account was created, in ISO 8601 format
        - last_login (str): Timestamp of the user's last login, in ISO 8601 format
        - favorites_count (int): Number of wallpapers the user has favorited
        - collections_count (int): Number of collections created by the user
        - settings_last_updated (str): Timestamp when settings were last modified, in ISO 8601 format
        - metadata_theme (str): Interface theme preference
        - metadata_language (str): Preferred language setting
        - metadata_notifications_enabled (bool): Whether notifications are enabled
    """
    return {
        "user_id": "usr_7x9abc123def",
        "username": "wallhaven_user_42",
        "email": "user42@wallhaven.cc",
        "account_level": 1,
        "api_key_enabled": True,
        "default_purity_0": "sfw",
        "default_purity_1": "sketchy",
        "default_category": "general",
        "default_sorting": "date_added",
        "default_order": "desc",
        "avatar_url": "https://wallhaven.cc/avatar/7x9abc123def.jpg",
        "background_url": "https://wallhaven.cc/bg/7x9abc123def.jpg",
        "created_at": "2022-03-15T08:45:30Z",
        "last_login": "2023-11-20T14:22:10Z",
        "favorites_count": 156,
        "collections_count": 8,
        "settings_last_updated": "2023-11-18T10:05:44Z",
        "metadata_theme": "dark",
        "metadata_language": "en",
        "metadata_notifications_enabled": True
    }

def wallhaven_wallpaper_search_server_get_user_settings() -> Dict[str, Any]:
    """
    Get authenticated user settings from Wallhaven API.
    
    This function retrieves the current user's account settings including preferences,
    account details, and metadata. Requires a valid API key to be configured in the
    environment or context.
    
    Returns:
        Dict containing user settings with the following structure:
        - user_id (str): Unique identifier of the authenticated user
        - username (str): Username of the authenticated user
        - email (str): Email address associated with the user account
        - account_level (int): User's account level (e.g., 0 = basic, 1 = premium)
        - api_key_enabled (bool): Whether the user has API key access enabled
        - default_purity (List[str]): Default content filters selected by the user
        - default_category (str): Default wallpaper category preference
        - default_sorting (str): Default sorting method for search results
        - default_order (str): Order direction for sorting: 'desc' or 'asc'
        - avatar_url (str): URL to the user's profile avatar image
        - background_url (str): URL to the user's profile background image
        - created_at (str): Timestamp when the user account was created
        - last_login (str): Timestamp of the user's last login
        - favorites_count (int): Number of wallpapers the user has favorited
        - collections_count (int): Number of collections created by the user
        - settings_last_updated (str): Timestamp when settings were last modified
        - metadata (Dict): Additional provider-specific settings or flags
    
    Raises:
        Exception: If there is an issue retrieving the data from the external API
    """
    try:
        api_data = call_external_api("wallhaven-wallpaper-search-server-get_user_settings")
        
        # Construct default_purity list from indexed fields
        default_purity = [
            api_data["default_purity_0"],
            api_data["default_purity_1"]
        ]
        
        # Construct metadata dictionary from flattened fields
        metadata = {
            "theme": api_data["metadata_theme"],
            "language": api_data["metadata_language"],
            "notifications_enabled": api_data["metadata_notifications_enabled"]
        }
        
        # Build final result structure matching output schema
        result = {
            "user_id": api_data["user_id"],
            "username": api_data["username"],
            "email": api_data["email"],
            "account_level": api_data["account_level"],
            "api_key_enabled": api_data["api_key_enabled"],
            "default_purity": default_purity,
            "default_category": api_data["default_category"],
            "default_sorting": api_data["default_sorting"],
            "default_order": api_data["default_order"],
            "avatar_url": api_data["avatar_url"],
            "background_url": api_data["background_url"],
            "created_at": api_data["created_at"],
            "last_login": api_data["last_login"],
            "favorites_count": api_data["favorites_count"],
            "collections_count": api_data["collections_count"],
            "settings_last_updated": api_data["settings_last_updated"],
            "metadata": metadata
        }
        
        return result
        
    except KeyError as e:
        raise Exception(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve user settings: {str(e)}")