from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Minecraft Wiki sections.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Minecraft wiki page
        - section_0_index (int): Index of the first section
        - section_0_title (str): Title of the first section
        - section_1_index (int): Index of the second section
        - section_1_title (str): Title of the second section
    """
    return {
        "title": "Redstone",
        "section_0_index": 1,
        "section_0_title": "Overview",
        "section_1_index": 2,
        "section_1_title": "History"
    }

def minecraft_wiki_server_MinecraftWiki_getSectionsInPage(title: str) -> Dict[str, Any]:
    """
    Retrieves an overview of all sections in the Minecraft Wiki page.

    Args:
        title (str): Title of the page to retrieve sections for.

    Returns:
        Dict containing:
        - title (str): Title of the Minecraft wiki page
        - sections (List[Dict]): List of section objects with 'index' and 'title' fields
    """
    if not title or not title.strip():
        raise ValueError("Title parameter is required and cannot be empty.")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("minecraft-wiki-server-MinecraftWiki_getSectionsInPage")
    
    # Construct sections list from flattened API response
    sections = [
        {
            "index": api_data["section_0_index"],
            "title": api_data["section_0_title"]
        },
        {
            "index": api_data["section_1_index"],
            "title": api_data["section_1_title"]
        }
    ]
    
    # Return result matching output schema
    return {
        "title": api_data["title"],
        "sections": sections
    }