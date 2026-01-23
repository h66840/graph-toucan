from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching pitching statistics data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - pitching_stats_0_player_id (int): Unique ID for the first player
        - pitching_stats_0_name (str): Name of the first player
        - pitching_stats_0_wins (int): Wins for the first player
        - pitching_stats_0_losses (int): Losses for the first player
        - pitching_stats_0_era (float): ERA for the first player
        - pitching_stats_0_ip (float): Innings pitched for the first player
        - pitching_stats_0_so (int): Strikeouts for the first player
        - pitching_stats_0_bb (int): Walks for the first player
        - pitching_stats_1_player_id (int): Unique ID for the second player
        - pitching_stats_1_name (str): Name of the second player
        - pitching_stats_1_wins (int): Wins for the second player
        - pitching_stats_1_losses (int): Losses for the second player
        - pitching_stats_1_era (float): ERA for the second player
        - pitching_stats_1_ip (float): Innings pitched for the second player
        - pitching_stats_1_so (int): Strikeouts for the second player
        - pitching_stats_1_bb (int): Walks for the second player
        - season (int): The season year for which stats are returned
        - total_players (int): Total number of players included in the response
        - source (str): Identifier for the data source (e.g., 'Baseball-Reference')
        - last_updated (str): Timestamp when stats were last updated in ISO format
        - metadata_league (str): League name (e.g., 'MLB')
        - metadata_level (str): Level of play (e.g., 'MLB')
        - metadata_min_ip_filter (float): Minimum innings pitched threshold applied
    """
    return {
        "pitching_stats_0_player_id": 1001,
        "pitching_stats_0_name": "John Doe",
        "pitching_stats_0_wins": 12,
        "pitching_stats_0_losses": 5,
        "pitching_stats_0_era": 2.89,
        "pitching_stats_0_ip": 145.1,
        "pitching_stats_0_so": 167,
        "pitching_stats_0_bb": 34,
        "pitching_stats_1_player_id": 1002,
        "pitching_stats_1_name": "Jane Smith",
        "pitching_stats_1_wins": 9,
        "pitching_stats_1_losses": 8,
        "pitching_stats_1_era": 3.45,
        "pitching_stats_1_ip": 132.0,
        "pitching_stats_1_so": 142,
        "pitching_stats_1_bb": 45,
        "season": 2024,
        "total_players": 2,
        "source": "Baseball-Reference",
        "last_updated": "2024-06-15T10:30:00Z",
        "metadata_league": "MLB",
        "metadata_level": "MLB",
        "metadata_min_ip_filter": 50.0
    }

def mlb_stats_server_get_pitching_stats_bref(season: Optional[int] = None) -> Dict[str, Any]:
    """
    Get all pitching stats for a set season. If no argument is supplied, gives stats for current season to date.
    
    Args:
        season (Optional[int]): The MLB season year to retrieve pitching stats for. If None, defaults to current year.
    
    Returns:
        Dict containing:
        - pitching_stats (List[Dict]): List of dictionaries with pitching statistics for individual players.
        - season (int): The season year for which stats are returned.
        - total_players (int): Total number of players included.
        - source (str): Data source identifier.
        - last_updated (str): ISO format timestamp of last update.
        - metadata (Dict): Contextual info including league, level, and minimum IP filter.
    
    Example:
        {
            "pitching_stats": [
                {
                    "player_id": 1001,
                    "name": "John Doe",
                    "wins": 12,
                    "losses": 5,
                    "era": 2.89,
                    "ip": 145.1,
                    "so": 167,
                    "bb": 34
                },
                ...
            ],
            "season": 2024,
            "total_players": 2,
            "source": "Baseball-Reference",
            "last_updated": "2024-06-15T10:30:00Z",
            "metadata": {
                "league": "MLB",
                "level": "MLB",
                "min_ip_filter": 50.0
            }
        }
    """
    # Use current year if no season provided
    if season is None:
        season = datetime.now().year

    # Fetch simulated external data
    raw_data = call_external_api("mlb-stats-server-get_pitching_stats_bref")

    # Construct pitching stats list from indexed fields
    pitching_stats = [
        {
            "player_id": raw_data["pitching_stats_0_player_id"],
            "name": raw_data["pitching_stats_0_name"],
            "wins": raw_data["pitching_stats_0_wins"],
            "losses": raw_data["pitching_stats_0_losses"],
            "era": raw_data["pitching_stats_0_era"],
            "ip": raw_data["pitching_stats_0_ip"],
            "so": raw_data["pitching_stats_0_so"],
            "bb": raw_data["pitching_stats_0_bb"]
        },
        {
            "player_id": raw_data["pitching_stats_1_player_id"],
            "name": raw_data["pitching_stats_1_name"],
            "wins": raw_data["pitching_stats_1_wins"],
            "losses": raw_data["pitching_stats_1_losses"],
            "era": raw_data["pitching_stats_1_era"],
            "ip": raw_data["pitching_stats_1_ip"],
            "so": raw_data["pitching_stats_1_so"],
            "bb": raw_data["pitching_stats_1_bb"]
        }
    ]

    # Construct metadata
    metadata = {
        "league": raw_data["metadata_league"],
        "level": raw_data["metadata_level"],
        "min_ip_filter": raw_data["metadata_min_ip_filter"]
    }

    # Assemble final result
    result = {
        "pitching_stats": pitching_stats,
        "season": raw_data["season"],
        "total_players": raw_data["total_players"],
        "source": raw_data["source"],
        "last_updated": raw_data["last_updated"],
        "metadata": metadata
    }

    return result