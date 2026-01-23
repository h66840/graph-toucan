from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching emoji data from external API by category.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - emoji_0_name (str): First emoji name
        - emoji_0_category (str): First emoji category
        - emoji_0_group (str): First emoji group
        - emoji_0_htmlCode (str): First emoji HTML code
        - emoji_0_unicode (str): First emoji Unicode
        - emoji_1_name (str): Second emoji name
        - emoji_1_category (str): Second emoji category
        - emoji_1_group (str): Second emoji group
        - emoji_1_htmlCode (str): Second emoji HTML code
        - emoji_1_unicode (str): Second emoji Unicode
    """
    return {
        "emoji_0_name": "grinning face",
        "emoji_0_category": "smileys-and-people",
        "emoji_0_group": "face-smiling",
        "emoji_0_htmlCode": "&#128512;",
        "emoji_0_unicode": "U+1F600",
        "emoji_1_name": "beaming face with smiling eyes",
        "emoji_1_category": "smileys-and-people",
        "emoji_1_group": "face-smiling",
        "emoji_1_htmlCode": "&#128513;",
        "emoji_1_unicode": "U+1F601"
    }

def emoji_hub_server_get_emojis_by_category_tool(category: str) -> Dict[str, Any]:
    """
    Get all emojis from a specific category.
    
    Available categories:
    - smileys-and-people
    - animals-and-nature
    - food-and-drink
    - travel-and-places
    - activities
    - objects
    - symbols
    - flags
    
    Args:
        category (str): The emoji category to retrieve emojis from.
        
    Returns:
        Dict containing a list of emoji objects, each with 'name', 'category', 'group', 'htmlCode', and 'unicode' fields.
        
    Raises:
        ValueError: If the provided category is not one of the allowed categories.
    """
    allowed_categories = [
        "smileys-and-people",
        "animals-and-nature",
        "food-and-drink",
        "travel-and-places",
        "activities",
        "objects",
        "symbols",
        "flags"
    ]
    
    if not category:
        raise ValueError("Category parameter is required.")
        
    if category not in allowed_categories:
        raise ValueError(f"Invalid category: {category}. Must be one of {allowed_categories}.")
    
    # Fetch data from simulated external API
    api_data = call_external_api("emoji-hub-server-get_emojis_by_category_tool")
    
    # Construct the list of emoji objects from flattened API response
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
    
    # Filter emojis by the requested category
    filtered_emojis = [emoji for emoji in emojis if emoji["category"] == category]
    
    return {"emojis": filtered_emojis}