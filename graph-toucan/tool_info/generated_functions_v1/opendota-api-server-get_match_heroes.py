from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching match hero data from external OpenDota API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success (bool): Whether the request was successful
        - match_id (int): The ID of the match
        - duration_seconds (int): Duration of the match in seconds
        - start_time (int): Unix timestamp when the match started
        - region (int): Server region identifier
        - game_mode (int): Game mode code
        - lobby_type (int): Lobby type code
        - player_0_slot (int): Player slot for first player
        - player_0_hero_id (int): Hero ID played by first player
        - player_0_hero_name (str): Hero name played by first player
        - player_1_slot (int): Player slot for second player
        - player_1_hero_id (int): Hero ID played by second player
        - player_1_hero_name (str): Hero name played by second player
    """
    return {
        "success": True,
        "match_id": 5000000000,
        "duration_seconds": 2400,
        "start_time": 1672531200,
        "region": 3,
        "game_mode": 22,
        "lobby_type": 7,
        "player_0_slot": 0,
        "player_0_hero_id": 1,
        "player_0_hero_name": "Anti-Mage",
        "player_1_slot": 1,
        "player_1_hero_id": 2,
        "player_1_hero_name": "Axe"
    }

def opendota_api_server_get_match_heroes(match_id: int) -> Dict[str, Any]:
    """
    Get heroes played in a specific match.
    
    Args:
        match_id: ID of the match to retrieve
        
    Returns:
        Dictionary containing:
        - heroes (List[Dict]): List of player-hero mappings with 'player_slot', 'hero_id', and 'hero_name'
        - match_id (int): The ID of the match
        - success (bool): Whether the request was successful
        - duration_seconds (int): Match duration in seconds
        - start_time (int): Unix timestamp of match start
        - region (int): Server region identifier
        - game_mode (int): Game mode code
        - lobby_type (int): Lobby type code
    """
    # Input validation
    if not isinstance(match_id, int) or match_id <= 0:
        return {
            "heroes": [],
            "match_id": match_id,
            "success": False,
            "duration_seconds": 0,
            "start_time": 0,
            "region": 0,
            "game_mode": 0,
            "lobby_type": 0
        }
    
    # Call external API to get match data
    api_data = call_external_api("opendota-api-server-get_match_heroes")
    
    # Construct heroes list from indexed player data
    heroes = [
        {
            "player_slot": api_data["player_0_slot"],
            "hero_id": api_data["player_0_hero_id"],
            "hero_name": api_data["player_0_hero_name"]
        },
        {
            "player_slot": api_data["player_1_slot"],
            "hero_id": api_data["player_1_hero_id"],
            "hero_name": api_data["player_1_hero_name"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "heroes": heroes,
        "match_id": api_data["match_id"],
        "success": api_data["success"],
        "duration_seconds": api_data["duration_seconds"],
        "start_time": api_data["start_time"],
        "region": api_data["region"],
        "game_mode": api_data["game_mode"],
        "lobby_type": api_data["lobby_type"]
    }
    
    return result