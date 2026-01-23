from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Minecraft Wiki page content.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Minecraft Wiki page retrieved
        - content (str): Raw wikitext content of the page, including all formatting, sections, tables, and embedded templates
    """
    return {
        "title": "Minecraft",
        "content": "{{Infobox Game\n| title = Minecraft\n| developer = Mojang Studios\n| released = {{Release date and age|2011|11|18}}\n}}\n\nMinecraft is a sandbox video game developed by Mojang Studios."
    }

def minecraft_wiki_server_MinecraftWiki_getPageContent(title: str) -> Dict[str, str]:
    """
    Get the raw wikitext content of a specific Minecraft Wiki page.

    Args:
        title (str): Title of the Minecraft Wiki page to retrieve the raw wikitext content for.

    Returns:
        Dict[str, str]: A dictionary containing:
            - title (str): Title of the Minecraft Wiki page retrieved
            - content (str): Raw wikitext content of the page, including all formatting, sections, tables, and embedded templates

    Raises:
        ValueError: If the title is empty or not a string.
    """
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string.")

    # Call the external API simulation
    api_data = call_external_api("minecraft-wiki-server-MinecraftWiki_getPageContent")

    # Construct the result using the API data
    result = {
        "title": api_data["title"],
        "content": api_data["content"]
    }

    return result