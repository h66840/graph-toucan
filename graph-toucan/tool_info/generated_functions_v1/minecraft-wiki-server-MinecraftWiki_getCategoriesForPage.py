from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Minecraft Wiki categories.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Minecraft Wiki page
        - category_0 (str): First category the page belongs to, starting with "Category:"
        - category_1 (str): Second category the page belongs to, starting with "Category:"
    """
    return {
        "title": "Creeper",
        "category_0": "Category:Mobs",
        "category_1": "Category:Hostile Mobs"
    }

def minecraft_wiki_server_MinecraftWiki_getCategoriesForPage(title: str) -> Dict[str, Any]:
    """
    Get categories associated with a specific Minecraft Wiki page.

    Args:
        title (str): Title of the Minecraft Wiki page

    Returns:
        Dict containing:
        - title (str): Title of the Minecraft Wiki page for which categories were retrieved
        - categories (List[str]): List of category strings that the page belongs to, each starting with "Category:"
    
    Raises:
        ValueError: If title is empty or not a string
    """
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string")

    # Call external API to get data (simulated)
    api_data = call_external_api("minecraft-wiki-server-MinecraftWiki_getCategoriesForPage")

    # Construct the result according to the output schema
    result = {
        "title": api_data["title"],
        "categories": [
            api_data["category_0"],
            api_data["category_1"]
        ]
    }

    return result