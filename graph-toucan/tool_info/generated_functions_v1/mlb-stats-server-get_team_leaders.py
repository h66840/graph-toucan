from typing import Dict, List, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external MLB Stats API for team leaders.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - leaders_0_playerId (int): Player ID of the first leader
        - leaders_0_fullName (str): Full name of the first leader
        - leaders_0_teamId (int): Team ID of the first leader
        - leaders_0_statValue (float): Stat value of the first leader
        - leaders_0_rank (int): Rank of the first leader
        - leaders_1_playerId (int): Player ID of the second leader
        - leaders_1_fullName (str): Full name of the second leader
        - leaders_1_teamId (int): Team ID of the second leader
        - leaders_1_statValue (float): Stat value of the second leader
        - leaders_1_rank (int): Rank of the second leader
        - category (str): Statistical category (e.g., 'homeRuns')
        - gameType (str): Game type ('R' for regular season, etc.)
        - season (int): Season year; null represented as 0 if not applicable
        - teamId (int): The team ID queried
        - limit (int): Maximum number of leaders returned; 0 if null
        - totalLeadersAvailable (int): Total number of players in leaderboard
        - metadata_requestTime (str): ISO format datetime string of request
        - metadata_dataSource (str): Source of data (e.g., 'MLB Stats API')
        - metadata_isOfficial (bool): Whether the data is official
    """
    return {
        "leaders_0_playerId": 12345,
        "leaders_0_fullName": "Mike Trout",
        "leaders_0_teamId": 123,
        "leaders_0_statValue": 35.5,
        "leaders_0_rank": 1,
        "leaders_1_playerId": 67890,
        "leaders_1_fullName": "Shohei Ohtani",
        "leaders_1_teamId": 123,
        "leaders_1_statValue": 32.0,
        "leaders_1_rank": 2,
        "category": "homeRuns",
        "gameType": "R",
        "season": 2023,
        "teamId": 123,
        "limit": 2,
        "totalLeadersAvailable": 50,
        "metadata_requestTime": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata_dataSource": "MLB Stats API",
        "metadata_isOfficial": True
    }

def mlb_stats_server_get_team_leaders(
    team_id: int,
    leader_category: Optional[str] = None,
    leader_game_type: Optional[str] = None,
    limit: Optional[int] = None,
    season: Optional[int] = None
) -> Dict[str, Any]:
    """
    Returns a list of stat leader data for a given MLB team.
    
    Args:
        team_id (int): The required team ID to retrieve leaders for.
        leader_category (str, optional): The statistical category to query (e.g., 'homeRuns', 'hits').
        leader_game_type (str, optional): The game type context (e.g., 'R' for regular season).
        limit (int, optional): Maximum number of leaders to return.
        season (int, optional): The season year to query; defaults to current season if not provided.
    
    Returns:
        Dict containing:
        - leaders (List[Dict]): List of player leader entries with keys: 'playerId', 'fullName', 
          'teamId', 'statValue', 'rank'.
        - category (str): The statistical category queried.
        - gameType (str): Game type context used.
        - season (int): Season year; None if not specified.
        - teamId (int): The team ID queried.
        - limit (int): Max number of leaders returned; None if no limit.
        - totalLeadersAvailable (int): Total players available in this leaderboard.
        - metadata (Dict): Additional info including 'requestTime', 'dataSource', 'isOfficial'.
    
    Raises:
        ValueError: If team_id is not a positive integer.
    """
    if not isinstance(team_id, int) or team_id <= 0:
        raise ValueError("team_id must be a positive integer")

    # Prepare parameters for API call (used in simulation)
    _ = leader_category, leader_game_type, limit, season

    # Fetch simulated external data
    api_data = call_external_api("mlb-stats-server-get_team_leaders")

    # Construct leaders list from indexed flat fields
    leaders = [
        {
            "playerId": api_data["leaders_0_playerId"],
            "fullName": api_data["leaders_0_fullName"],
            "teamId": api_data["leaders_0_teamId"],
            "statValue": api_data["leaders_0_statValue"],
            "rank": api_data["leaders_0_rank"]
        },
        {
            "playerId": api_data["leaders_1_playerId"],
            "fullName": api_data["leaders_1_fullName"],
            "teamId": api_data["leaders_1_teamId"],
            "statValue": api_data["leaders_1_statValue"],
            "rank": api_data["leaders_1_rank"]
        }
    ]

    # Construct metadata
    metadata = {
        "requestTime": api_data["metadata_requestTime"],
        "dataSource": api_data["metadata_dataSource"],
        "isOfficial": api_data["metadata_isOfficial"]
    }

    # Handle nulls
    result_season = api_data["season"] if api_data["season"] != 0 else None
    result_limit = api_data["limit"] if api_data["limit"] != 0 else None

    # Build final result matching output schema
    result = {
        "leaders": leaders,
        "category": api_data["category"],
        "gameType": api_data["gameType"],
        "season": result_season,
        "teamId": api_data["teamId"],
        "limit": result_limit,
        "totalLeadersAvailable": api_data["totalLeadersAvailable"],
        "metadata": metadata
    }

    return result