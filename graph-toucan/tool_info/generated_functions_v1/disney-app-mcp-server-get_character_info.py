from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Disney character information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): Official name of the Disney character
        - film_0 (str): First film title the character appeared in
        - film_1 (str): Second film title the character appeared in
        - tv_show_0 (str): First TV show the character appeared in
        - tv_show_1 (str): Second TV show the character appeared in
        - video_game_0 (str): First video game the character appeared in
        - video_game_1 (str): Second video game the character appeared in
        - ally_0 (str): First known ally character
        - ally_1 (str): Second known ally character
        - enemy_0 (str): First known enemy character
        - enemy_1 (str): Second known enemy character
    """
    return {
        "name": "Mickey Mouse",
        "film_0": "Steamboat Willie",
        "film_1": "Fantasia",
        "tv_show_0": "The Mickey Mouse Club",
        "tv_show_1": "Mickey Mouse Works",
        "video_game_0": "Kingdom Hearts",
        "video_game_1": "Disney Infinity",
        "ally_0": "Minnie Mouse",
        "ally_1": "Donald Duck",
        "enemy_0": "Pete",
        "enemy_1": "The Phantom Blot"
    }

def disney_app_mcp_server_get_character_info(medicine_name: str) -> Dict[str, Any]:
    """
    Get information about a Disney character by name.
    
    Args:
        medicine_name (str): The name of the Disney character to retrieve information for.
    
    Returns:
        Dict containing the following keys:
        - name (str): Official name of the Disney character
        - films (List[str]): List of film titles in which the character has appeared
        - tvShows (List[str]): List of TV shows in which the character has appeared
        - videoGames (List[str]): List of video games in which the character has appeared
        - allies (List[str]): List of known ally characters associated with the character
        - enemies (List[str]): List of known enemy characters associated with the character
    
    Raises:
        ValueError: If medicine_name is empty or not a string
    """
    if not medicine_name or not isinstance(medicine_name, str):
        raise ValueError("medicine_name must be a non-empty string")
    
    # Call external API to get character data (with flattened structure)
    api_data = call_external_api("disney-app-mcp-server-get_character_info")
    
    # Construct nested structure matching output schema
    result = {
        "name": api_data["name"],
        "films": [
            api_data["film_0"],
            api_data["film_1"]
        ],
        "tvShows": [
            api_data["tv_show_0"],
            api_data["tv_show_1"]
        ],
        "videoGames": [
            api_data["video_game_0"],
            api_data["video_game_1"]
        ],
        "allies": [
            api_data["ally_0"],
            api_data["ally_1"]
        ],
        "enemies": [
            api_data["enemy_0"],
            api_data["enemy_1"]
        ]
    }
    
    return result