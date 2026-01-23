from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - emoji_0_emoji (str): First emoji character
        - emoji_0_name (str): First emoji name
        - emoji_0_category (str): First emoji category
        - emoji_0_tag_0 (str): First tag for first emoji
        - emoji_0_tag_1 (str): Second tag for first emoji
        - emoji_1_emoji (str): Second emoji character
        - emoji_1_name (str): Second emoji name
        - emoji_1_category (str): Second emoji category
        - emoji_1_tag_0 (str): First tag for second emoji
        - emoji_1_tag_1 (str): Second tag for second emoji
        - total_count (int): Total number of emojis returned
        - category_0 (str): First unique category
        - category_1 (str): Second unique category
        - metadata_api_version (str): Version of the API
        - metadata_timestamp (str): Timestamp of the request
        - metadata_source_url (str): Source URL of the API
    """
    return {
        "emoji_0_emoji": "😀",
        "emoji_0_name": "grinning face",
        "emoji_0_category": "smileys & emotion",
        "emoji_0_tag_0": "smile",
        "emoji_0_tag_1": "happy",
        "emoji_1_emoji": "🌍",
        "emoji_1_name": "globe showing Asia-Australia",
        "emoji_1_category": "travel & places",
        "emoji_1_tag_0": "earth",
        "emoji_1_tag_1": "world",
        "total_count": 2,
        "category_0": "smileys & emotion",
        "category_1": "travel & places",
        "metadata_api_version": "1.0.0",
        "metadata_timestamp": "2023-10-05T12:00:00Z",
        "metadata_source_url": "https://api.emojihub.dev/v1/emojis"
    }

def emoji_hub_server_get_all_emojis_tool() -> Dict[str, Any]:
    """
    Get all emojis from the Emoji Hub API.

    Returns:
        Dict containing:
        - emojis (List[Dict]): List of emoji objects with emoji character, name, category, and tags
        - total_count (int): Total number of emojis returned
        - categories (List[str]): List of unique categories
        - metadata (Dict): Additional information including API version, timestamp, and source URL
    """
    try:
        api_data = call_external_api("emoji-hub-server-get_all_emojis_tool")

        # Construct emojis list
        emojis = [
            {
                "emoji": api_data["emoji_0_emoji"],
                "name": api_data["emoji_0_name"],
                "category": api_data["emoji_0_category"],
                "tags": [api_data["emoji_0_tag_0"], api_data["emoji_0_tag_1"]]
            },
            {
                "emoji": api_data["emoji_1_emoji"],
                "name": api_data["emoji_1_name"],
                "category": api_data["emoji_1_category"],
                "tags": [api_data["emoji_1_tag_0"], api_data["emoji_1_tag_1"]]
            }
        ]

        # Construct categories list
        categories = [api_data["category_0"], api_data["category_1"]]

        # Construct metadata
        metadata = {
            "api_version": api_data["metadata_api_version"],
            "timestamp": api_data["metadata_timestamp"],
            "source_url": api_data["metadata_source_url"]
        }

        # Construct final result
        result = {
            "emojis": emojis,
            "total_count": api_data["total_count"],
            "categories": categories,
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve emojis from Emoji Hub API: {str(e)}")