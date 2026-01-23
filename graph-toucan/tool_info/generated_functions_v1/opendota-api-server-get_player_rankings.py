from typing import Dict, List, Any
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for player hero rankings.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - rankings_0_hero_id (int): Hero ID for the first ranked hero
        - rankings_0_hero_name (str): Name of the first ranked hero
        - rankings_0_score (float): Performance score for the first hero
        - rankings_0_rank (int): Rank of the player with the first hero
        - rankings_0_games_played (int): Number of games played with the first hero
        - rankings_0_win_rate (float): Win rate percentage with the first hero
        - rankings_0_is_active (bool): Whether the player is active with the first hero
        - rankings_1_hero_id (int): Hero ID for the second ranked hero
        - rankings_1_hero_name (str): Name of the second ranked hero
        - rankings_1_score (float): Performance score for the second hero
        - rankings_1_rank (int): Rank of the player with the second hero
        - rankings_1_games_played (int): Number of games played with the second hero
        - rankings_1_win_rate (float): Win rate percentage with the second hero
        - rankings_1_is_active (bool): Whether the player is active with the second hero
        - total_rankings (int): Total number of ranking entries returned
        - player_id (int): Steam32 account ID of the player
        - last_updated (str): ISO 8601 timestamp when the data was last updated
    """
    return {
        "rankings_0_hero_id": 1,
        "rankings_0_hero_name": "Anti-Mage",
        "rankings_0_score": 95.7,
        "rankings_0_rank": 482,
        "rankings_0_games_played": 124,
        "rankings_0_win_rate": 62.1,
        "rankings_0_is_active": True,
        "rankings_1_hero_id": 2,
        "rankings_1_hero_name": "Axe",
        "rankings_1_score": 88.3,
        "rankings_1_rank": 1156,
        "rankings_1_games_played": 97,
        "rankings_1_win_rate": 58.7,
        "rankings_1_is_active": False,
        "total_rankings": 2,
        "player_id": 123456789,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }


def opendota_api_server_get_player_rankings(account_id: int) -> Dict[str, Any]:
    """
    Get player hero rankings from OpenDota API.

    Args:
        account_id (int): Steam32 account ID of the player

    Returns:
        Dict containing:
        - rankings (List[Dict]): List of player hero ranking entries with performance metrics
        - total_rankings (int): Total number of ranking entries returned
        - player_id (int): The Steam32 account ID of the player
        - last_updated (str): ISO 8601 timestamp indicating when the data was last updated

        Each ranking entry contains:
        - hero_id (int): Unique identifier for the hero
        - hero_name (str): Display name of the hero
        - score (float): Performance score or percentile
        - rank (int): Numerical rank among others for this hero
        - games_played (int): Number of games played with this hero
        - win_rate (float): Win rate percentage when playing this hero
        - is_active (bool): Whether the player is currently active with this hero

    Raises:
        ValueError: If account_id is not a positive integer
    """
    if not isinstance(account_id, int) or account_id <= 0:
        raise ValueError("account_id must be a positive integer")

    # Fetch data from external API (simulated)
    api_data = call_external_api("opendota-api-server-get_player_rankings")

    # Construct rankings list from flattened API response
    rankings = [
        {
            "hero_id": api_data["rankings_0_hero_id"],
            "hero_name": api_data["rankings_0_hero_name"],
            "score": api_data["rankings_0_score"],
            "rank": api_data["rankings_0_rank"],
            "games_played": api_data["rankings_0_games_played"],
            "win_rate": api_data["rankings_0_win_rate"],
            "is_active": api_data["rankings_0_is_active"]
        },
        {
            "hero_id": api_data["rankings_1_hero_id"],
            "hero_name": api_data["rankings_1_hero_name"],
            "score": api_data["rankings_1_score"],
            "rank": api_data["rankings_1_rank"],
            "games_played": api_data["rankings_1_games_played"],
            "win_rate": api_data["rankings_1_win_rate"],
            "is_active": api_data["rankings_1_is_active"]
        }
    ]

    # Construct final result matching output schema
    result = {
        "rankings": rankings,
        "total_rankings": api_data["total_rankings"],
        "player_id": api_data["player_id"],
        "last_updated": api_data["last_updated"]
    }

    return result