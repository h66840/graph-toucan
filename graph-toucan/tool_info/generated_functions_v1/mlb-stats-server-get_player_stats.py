from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB player stats.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - id (int): unique identifier for the player
        - first_name (str): first name of the player
        - last_name (str): last name of the player
        - active (bool): whether the player is currently active in MLB
        - current_team (str): current team name the player is associated with
        - position (str): primary position played by the player
        - nickname (str): player's nickname if available
        - last_played (str or None): date of last professional game played, in 'YYYY-MM-DD' format or null if still active
        - mlb_debut (str): date of MLB debut in 'YYYY-MM-DD' format
        - bat_side (str): which side the player bats on (e.g., 'Right', 'Left')
        - pitch_hand (str): which hand the player uses to pitch (e.g., 'Right', 'Left')
        - stats_0_type (str): type of the first stat group
        - stats_0_group (str): group of the first stat group
        - stats_0_season (str): season of the first stat group
        - stats_0_stats_at_bats (int): at bats for the first stat group
        - stats_0_stats_runs (int): runs for the first stat group
        - stats_0_stats_hits (int): hits for the first stat group
        - stats_1_type (str): type of the second stat group
        - stats_1_group (str): group of the second stat group
        - stats_1_season (str): season of the second stat group
        - stats_1_stats_at_bats (int): at bats for the second stat group
        - stats_1_stats_runs (int): runs for the second stat group
        - stats_1_stats_hits (int): hits for the second stat group
    """
    return {
        "id": 12345,
        "first_name": "Mike",
        "last_name": "Trout",
        "active": True,
        "current_team": "Los Angeles Angels",
        "position": "CF",
        "nickname": "The Millville Meteor",
        "last_played": None,
        "mlb_debut": "2011-07-08",
        "bat_side": "Left",
        "pitch_hand": "Right",
        "stats_0_type": "regularSeason",
        "stats_0_group": "hitting",
        "stats_0_season": "2023",
        "stats_0_stats_at_bats": 520,
        "stats_0_stats_runs": 103,
        "stats_0_stats_hits": 150,
        "stats_1_type": "career",
        "stats_1_group": "hitting",
        "stats_1_season": "career",
        "stats_1_stats_at_bats": 6500,
        "stats_1_stats_runs": 1300,
        "stats_1_stats_hits": 1800,
    }

def mlb_stats_server_get_player_stats(
    player_id: int,
    group: Optional[str] = None,
    season: Optional[Any] = None,
    stats: Optional[str] = None
) -> Dict[str, Any]:
    """
    Returns a list of current season or career stat data for a given player.
    
    Args:
        player_id (int): Unique identifier for the player (required)
        group (str, optional): Stat group to filter by (e.g., 'hitting', 'pitching')
        season (Any, optional): Season to retrieve stats for (e.g., '2023', 'career')
        stats (str, optional): Specific stats to include
    
    Returns:
        Dict containing player information and a list of stat groups with detailed statistics.
        The returned dict includes:
        - id (int): unique identifier for the player
        - first_name (str): first name of the player
        - last_name (str): last name of the player
        - active (bool): whether the player is currently active in MLB
        - current_team (str): current team name the player is associated with
        - position (str): primary position played by the player
        - nickname (str): player's nickname if available
        - last_played (str or None): date of last professional game played, in 'YYYY-MM-DD' format or null if still active
        - mlb_debut (str): date of MLB debut in 'YYYY-MM-DD' format
        - bat_side (str): which side the player bats on (e.g., 'Right', 'Left')
        - pitch_hand (str): which hand the player uses to pitch (e.g., 'Right', 'Left')
        - stats (List[Dict]): list of stat groups, each containing 'type', 'group', 'season', 
          and a nested 'stats' dictionary with specific statistical categories and values
          
    Raises:
        ValueError: If player_id is not provided
    """
    if not player_id:
        raise ValueError("player_id is required")

    # Fetch data from external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_player_stats")
    
    # Construct the stats list from flattened API response
    stats_list = [
        {
            "type": api_data["stats_0_type"],
            "group": api_data["stats_0_group"],
            "season": api_data["stats_0_season"],
            "stats": {
                "at_bats": api_data["stats_0_stats_at_bats"],
                "runs": api_data["stats_0_stats_runs"],
                "hits": api_data["stats_0_stats_hits"]
            }
        },
        {
            "type": api_data["stats_1_type"],
            "group": api_data["stats_1_group"],
            "season": api_data["stats_1_season"],
            "stats": {
                "at_bats": api_data["stats_1_stats_at_bats"],
                "runs": api_data["stats_1_stats_runs"],
                "hits": api_data["stats_1_stats_hits"]
            }
        }
    ]
    
    # Apply filtering based on input parameters
    filtered_stats = stats_list
    
    if group:
        filtered_stats = [s for s in filtered_stats if s["group"] == group]
    
    if season:
        season_str = str(season)
        filtered_stats = [s for s in filtered_stats if s["season"] == season_str]
    
    # Construct final result
    result = {
        "id": api_data["id"],
        "first_name": api_data["first_name"],
        "last_name": api_data["last_name"],
        "active": api_data["active"],
        "current_team": api_data["current_team"],
        "position": api_data["position"],
        "nickname": api_data["nickname"],
        "last_played": api_data["last_played"],
        "mlb_debut": api_data["mlb_debut"],
        "bat_side": api_data["bat_side"],
        "pitch_hand": api_data["pitch_hand"],
        "stats": filtered_stats
    }
    
    return result