from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Play app permissions.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - permission_0_permission (str): Description of first permission (e.g., 'modify storage contents')
        - permission_0_type (str): Category of first permission (e.g., 'Storage')
        - permission_1_permission (str): Description of second permission
        - permission_1_type (str): Category of second permission
        - short_mode (bool): Whether short mode was requested (only permission strings)
    """
    return {
        "permission_0_permission": "modify storage contents",
        "permission_0_type": "Storage",
        "permission_1_permission": "access precise location",
        "permission_1_type": "Location",
        "short_mode": False
    }

def app_market_intelligence_google_play_permissions(
    appId: str,
    country: Optional[str] = "us",
    lang: Optional[str] = "en",
    short: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get permissions required by a Google Play app.
    
    Args:
        appId (str): Google Play package name (e.g., 'com.dxco.pandavszombies')
        country (str, optional): Country code to check app (default: us)
        lang (str, optional): Language code for permission text (default: en)
        short (bool, optional): Return only permission names without categories (default: False)
    
    Returns:
        Dict[str, Any]: Dictionary containing a list of permissions with description and type.
        - permissions (List[Dict]): list of permissions, each with 'permission' (description) and 'type' (category)
    
    Raises:
        ValueError: If appId is empty or None
    """
    if not appId:
        raise ValueError("appId is required")

    # Normalize inputs
    country = country.lower() if country else "us"
    lang = lang.lower() if lang else "en"
    short = bool(short)

    # Fetch simulated external data
    api_data = call_external_api("app-market-intelligence-google-play-permissions")
    
    # Construct permissions list from flattened API response
    permissions = [
        {
            "permission": api_data["permission_0_permission"],
            "type": api_data["permission_0_type"]
        },
        {
            "permission": api_data["permission_1_permission"],
            "type": api_data["permission_1_type"]
        }
    ]
    
    # If short mode is requested, return only permission strings in a different structure
    if short:
        return {"permissions": [p["permission"] for p in permissions]}
    
    return {"permissions": permissions}