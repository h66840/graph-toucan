from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Minecraft Wiki search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_resultId (str): ID of the first search result
        - result_0_title (str): Title of the first search result
        - result_0_snippet (str): Snippet of the first search result
        - result_1_resultId (str): ID of the second search result
        - result_1_title (str): Title of the second search result
        - result_1_snippet (str): Snippet of the second search result
    """
    return {
        "result_0_resultId": "minecraft:diamond_sword",
        "result_0_title": "Diamond Sword",
        "result_0_snippet": "A powerful sword made from diamonds, used to deal high damage.",
        "result_1_resultId": "minecraft:iron_ore",
        "result_1_title": "Iron Ore",
        "result_1_snippet": "An ore that generates in the overworld and can be mined for iron ingots."
    }

def minecraft_wiki_server_MinecraftWiki_searchWiki(query: str) -> List[Dict[str, str]]:
    """
    Search the Minecraft Wiki for a specific structure, entity, item or block.
    
    Note: Only use for basic search terms like item/block/structure/entity names.
    Complex queries (like 'loot table of X' or 'how to craft Y') will not work.
    
    Args:
        query (str): Search term to find on the Minecraft Wiki.
        
    Returns:
        List[Dict[str, str]]: List of search results, each containing 'resultId', 'title', and 'snippet' fields.
        
    Raises:
        ValueError: If query is empty or not a string.
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty.")
    
    if not isinstance(query, str):
        raise ValueError("Query parameter must be a string.")
    
    # Call the external API simulation
    api_data = call_external_api("minecraft-wiki-server-MinecraftWiki_searchWiki")
    
    # Construct the results list from flattened API response
    results = [
        {
            "resultId": api_data["result_0_resultId"],
            "title": api_data["result_0_title"],
            "snippet": api_data["result_0_snippet"]
        },
        {
            "resultId": api_data["result_1_resultId"],
            "title": api_data["result_1_title"],
            "snippet": api_data["result_1_snippet"]
        }
    ]
    
    return results