from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching emoji data from external API for a given group.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - emoji_0_name (str): First emoji name
        - emoji_0_category (str): First emoji category
        - emoji_0_group (str): First emoji group
        - emoji_0_htmlCode (str): First emoji HTML code
        - emoji_0_unicode (str): First emoji Unicode value
        - emoji_1_name (str): Second emoji name
        - emoji_1_category (str): Second emoji category
        - emoji_1_group (str): Second emoji group
        - emoji_1_htmlCode (str): Second emoji HTML code
        - emoji_1_unicode (str): Second emoji Unicode value
    """
    return {
        "emoji_0_name": "smiling_face",
        "emoji_0_category": "face-positive",
        "emoji_0_group": "face-positive",
        "emoji_0_htmlCode": "&#128512;",
        "emoji_0_unicode": "U+1F600",
        "emoji_1_name": "grinning_face",
        "emoji_1_category": "face-positive",
        "emoji_1_group": "face-positive",
        "emoji_1_htmlCode": "&#128513;",
        "emoji_1_unicode": "U+1F601"
    }

def emoji_hub_server_get_emojis_by_group_tool(group: str) -> Dict[str, Any]:
    """
    Get all emojis from a specific group.
    
    Args:
        group (str): The emoji group to retrieve (e.g., 'face-positive', 'animal-bird', 'food-fruit')
    
    Returns:
        Dict containing a list of emoji objects with 'name', 'category', 'group', 'htmlCode', and 'unicode' fields.
    
    Raises:
        ValueError: If group is empty or not a string
    """
    if not group:
        raise ValueError("Group parameter is required")
    if not isinstance(group, str):
        raise ValueError("Group parameter must be a string")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("emoji-hub-server-get_emojis_by_group_tool")
    
    # Construct the emojis list from flattened API response
    emojis = [
        {
            "name": api_data["emoji_0_name"],
            "category": api_data["emoji_0_category"],
            "group": api_data["emoji_0_group"],
            "htmlCode": api_data["emoji_0_htmlCode"],
            "unicode": api_data["emoji_0_unicode"]
        },
        {
            "name": api_data["emoji_1_name"],
            "category": api_data["emoji_1_category"],
            "group": api_data["emoji_1_group"],
            "htmlCode": api_data["emoji_1_htmlCode"],
            "unicode": api_data["emoji_1_unicode"]
        }
    ]
    
    # Filter emojis by the requested group (simulated filtering logic)
    filtered_emojis = [emoji for emoji in emojis if emoji["group"] == group]
    
    return {
        "emojis": filtered_emojis
    }