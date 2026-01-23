from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Minecraft Wiki redirect resolution.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - originalTitle (str): The original page title that was queried
        - resolvedTitle (str): The final canonical page title after resolving redirects
    """
    return {
        "originalTitle": "Minecraft",
        "resolvedTitle": "Minecraft (game)"
    }

def minecraft_wiki_server_MinecraftWiki_resolveRedirect(title: str) -> Dict[str, str]:
    """
    Resolve a redirect and return the title of the target page.
    
    This function simulates resolving a Minecraft Wiki page redirect by querying
    an external API (simulated) to get the canonical page title after following redirects.
    
    Args:
        title (str): Title of the page to resolve the redirect for. Must be a non-empty string.
        
    Returns:
        Dict[str, str]: A dictionary containing:
            - originalTitle (str): The original page title that was queried
            - resolvedTitle (str): The final canonical page title after resolving any redirects
            
    Raises:
        ValueError: If the title is empty or not a string
    """
    if not isinstance(title, str):
        raise ValueError("Title must be a string")
    if not title.strip():
        raise ValueError("Title cannot be empty or whitespace")
    
    # Call external API to simulate redirect resolution
    api_data = call_external_api("minecraft-wiki-server-MinecraftWiki_resolveRedirect")
    
    # Construct result matching output schema
    result = {
        "originalTitle": api_data["originalTitle"],
        "resolvedTitle": api_data["resolvedTitle"]
    }
    
    return result