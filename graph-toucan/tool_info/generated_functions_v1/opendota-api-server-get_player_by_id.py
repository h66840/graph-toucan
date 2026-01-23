from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for OpenDota player information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - player_name (str): Name of the player
        - account_id (int): Steam32 account ID of the player
        - rank (str): Current rank/league tier of the player (e.g., Archon 2)
        - estimated_mmr (str): Estimated MMR value if available, otherwise 'Unknown'
        - win_count (int): Number of matches won by the player
        - loss_count (int): Number of matches lost by the player
        - win_rate (float): Win rate percentage calculated from win/loss data
        - recent_matches_0_match_id (int): First recent match ID
        - recent_matches_0_date (str): First recent match date (ISO format)
        - recent_matches_0_hero_id (int): Hero ID used in first recent match
        - recent_matches_0_kills (int): Kills in first recent match
        - recent_matches_0_deaths (int): Deaths in first recent match
        - recent_matches_0_assists (int): Assists in first recent match
        - recent_matches_0_result (str): Result of first recent match ('win' or 'loss')
        - recent_matches_1_match_id (int): Second recent match ID
        - recent_matches_1_date (str): Second recent match date (ISO format)
        - recent_matches_1_hero_id (int): Hero ID used in second recent match
        - recent_matches_1_kills (int): Kills in second recent match
        - recent_matches_1_deaths (int): Deaths in second recent match
        - recent_matches_1_assists (int): Assists in second recent match
        - recent_matches_1_result (str): Result of second recent match ('win' or 'loss')
    """
    return {
        "player_name": "DotaLegend",
        "account_id": 123456789,
        "rank": "Archon II",
        "estimated_mmr": "4200",
        "win_count": 1250,
        "loss_count": 980,
        "win_rate": 56.0,
        "recent_matches_0_match_id": 7890123456,
        "recent_matches_0_date": "2023-10-05T14:30:00Z",
        "recent_matches_0_hero_id": 11,
        "recent_matches_0_kills": 14,
        "recent_matches_0_deaths": 6,
        "recent_matches_0_assists": 12,
        "recent_matches_0_result": "win",
        "recent_matches_1_match_id": 7890123455,
        "recent_matches_1_date": "2023-10-04T16:15:00Z",
        "recent_matches_1_hero_id": 25,
        "recent_matches_1_kills": 8,
        "recent_matches_1_deaths": 11,
        "recent_matches_1_assists": 7,
        "recent_matches_1_result": "loss"
    }

def opendota_api_server_get_player_by_id(account_id: int) -> Dict[str, Any]:
    """
    Get a player's information by their account ID from the OpenDota API.
    
    Args:
        account_id (int): The player's Steam32 account ID
        
    Returns:
        Dict containing player information including:
        - player_name (str): name of the player
        - account_id (int): Steam32 account ID of the player
        - rank (str): current rank/league tier of the player (e.g., Archon 2)
        - estimated_mmr (str or None): estimated MMR value if available, otherwise None
        - win_count (int): number of matches won by the player
        - loss_count (int): number of matches lost by the player
        - win_rate (float): win rate percentage calculated from win/loss data
        - recent_matches (List[Dict]): list of recent matches with details including:
            - match_id (int)
            - date (str)
            - hero_id (int)
            - kills (int)
            - deaths (int)
            - assists (int)
            - result (str): 'win' or 'loss'
            
    Raises:
        ValueError: If account_id is not a positive integer
    """
    if not isinstance(account_id, int) or account_id <= 0:
        raise ValueError("account_id must be a positive integer")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("opendota-api-server-get_player_by_id")
    
    # Extract and construct recent matches list
    recent_matches = [
        {
            "match_id": api_data["recent_matches_0_match_id"],
            "date": api_data["recent_matches_0_date"],
            "hero_id": api_data["recent_matches_0_hero_id"],
            "kills": api_data["recent_matches_0_kills"],
            "deaths": api_data["recent_matches_0_deaths"],
            "assists": api_data["recent_matches_0_assists"],
            "result": api_data["recent_matches_0_result"]
        },
        {
            "match_id": api_data["recent_matches_1_match_id"],
            "date": api_data["recent_matches_1_date"],
            "hero_id": api_data["recent_matches_1_hero_id"],
            "kills": api_data["recent_matches_1_kills"],
            "deaths": api_data["recent_matches_1_deaths"],
            "assists": api_data["recent_matches_1_assists"],
            "result": api_data["recent_matches_1_result"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "player_name": api_data["player_name"],
        "account_id": api_data["account_id"],
        "rank": api_data["rank"],
        "estimated_mmr": api_data["estimated_mmr"] if api_data["estimated_mmr"] != "Unknown" else None,
        "win_count": api_data["win_count"],
        "loss_count": api_data["loss_count"],
        "win_rate": round(api_data["win_rate"], 2),
        "recent_matches": recent_matches
    }
    
    return result