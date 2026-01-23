from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Minecraft Wiki page section retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Minecraft Wiki page
        - sectionIndex (int): Index of the section retrieved
        - content (str): Main content of the requested section, including text and inline HTML/Markdown formatting
    """
    return {
        "title": "Redstone",
        "sectionIndex": 1,
        "content": "<p>Redstone is a material in Minecraft that can be used to create <em>logic circuits</em> and <strong>mechanical devices</strong>.</p><ul><li>Found in caves below layer 16</li><li>Mined with an iron pickaxe or better</li></ul>"
    }

def minecraft_wiki_server_MinecraftWiki_getPageSection(sectionIndex: int, title: str) -> Dict[str, Any]:
    """
    Get a specific section from a Minecraft Wiki page. Should be used as step 3 after searching for the page and getting its summary.
    The section index corresponds to the order of sections on the page, starting with 0 for the main content, 1 for the first section, 2 for the second section, etc.
    
    Args:
        sectionIndex (int): Index of the section to retrieve (0 = main, 1 = first section, 2 = second section, etc.)
        title (str): Title of the Minecraft Wiki page
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - title (str): Title of the Minecraft Wiki page
            - sectionIndex (int): Index of the section retrieved from the page
            - content (str): Main content of the requested section, including text and inline HTML/Markdown formatting
    """
    # Input validation
    if not isinstance(sectionIndex, int):
        raise TypeError("sectionIndex must be an integer")
    if sectionIndex < 0:
        raise ValueError("sectionIndex must be non-negative")
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not title.strip():
        raise ValueError("title must not be empty or whitespace")
    
    # Call external API (simulated)
    api_data = call_external_api("minecraft-wiki-server-MinecraftWiki_getPageSection")
    
    # Construct result matching output schema
    result = {
        "title": api_data["title"],
        "sectionIndex": api_data["sectionIndex"],
        "content": api_data["content"]
    }
    
    return result