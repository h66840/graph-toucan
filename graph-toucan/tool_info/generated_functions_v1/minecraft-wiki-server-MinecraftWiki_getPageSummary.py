from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Minecraft Wiki page summary.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Minecraft Wiki page as returned by the API
        - summary (str): Summary text providing an overview of the page content
        - section_0_index (int): Index of the first section
        - section_0_title (str): Title of the first section
        - section_1_index (int): Index of the second section
        - section_1_title (str): Title of the second section
    """
    return {
        "title": "Creeper",
        "summary": "The creeper is a hostile mob that silently approaches players and explodes, destroying blocks and dealing damage.",
        "section_0_index": 1,
        "section_0_title": "Spawning",
        "section_1_index": 2,
        "section_1_title": "Behavior"
    }

def minecraft_wiki_server_MinecraftWiki_getPageSummary(title: str) -> Dict[str, Any]:
    """
    Retrieves a summary of a Minecraft Wiki page along with a list of available sections.
    
    Args:
        title (str): Title of the Minecraft Wiki page
        
    Returns:
        Dict containing:
        - title (str): Title of the page
        - summary (str): Overview summary of the page content
        - sections (List[Dict]): List of section objects with 'index' and 'title' fields
        
    Raises:
        ValueError: If title is empty or not a string
    """
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string")
    
    # Call external API to get flat data
    api_data = call_external_api("minecraft-wiki-server-MinecraftWiki_getPageSummary")
    
    # Construct sections list from indexed fields
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
    
    # Build final result matching output schema
    result = {
        "title": api_data["title"],
        "summary": api_data["summary"],
        "sections": sections
    }
    
    return result