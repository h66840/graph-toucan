from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external MLB stats server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - leader_0_rank (int): Rank of the first stat leader
        - leader_0_player_name (str): Name of the first stat leader
        - leader_0_team_name (str): Team name of the first stat leader
        - leader_0_stat_value (float): Statistic value for the first leader
        - leader_0_person_id (int): Person ID of the first leader
        - leader_1_rank (int): Rank of the second stat leader
        - leader_1_player_name (str): Name of the second stat leader
        - leader_1_team_name (str): Team name of the second stat leader
        - leader_1_stat_value (float): Statistic value for the second leader
        - leader_1_person_id (int): Person ID of the second leader
        - league_id (int): League identifier (103=AL, 104=NL), or null represented as 0
        - season (int): Season year for the stats
        - stat_category (str): Statistical category (e.g., 'homeRuns')
        - game_type (str): Game type ('R' for regular season, 'P' for playoffs)
        - limit (int): Maximum number of leaders returned
        - total_count (int): Total number of records available before limiting
        - metadata_query_timestamp (str): Timestamp when query was made
        - metadata_source (str): Source of the data
        - metadata_filters_applied (str): Filters applied in the query
    """
    return {
        "leader_0_rank": 1,
        "leader_0_player_name": "Shohei Ohtani",
        "leader_0_team_name": "Los Angeles Dodgers",
        "leader_0_stat_value": 44.0,
        "leader_0_person_id": 660271,
        "leader_1_rank": 2,
        "leader_1_player_name": "Aaron Judge",
        "leader_1_team_name": "New York Yankees",
        "leader_1_stat_value": 37.0,
        "leader_1_person_id": 592154,
        "league_id": 103,
        "season": 2023,
        "stat_category": "homeRuns",
        "game_type": "R",
        "limit": 10,
        "total_count": 30,
        "metadata_query_timestamp": "2023-10-05T12:00:00Z",
        "metadata_source": "MLB Stats API",
        "metadata_filters_applied": "regularSeason,league=AL"
    }

def mlb_stats_server_get_league_leader_data(
    leader_categories: str,
    game_types: Optional[str] = None,
    league_id: Optional[int] = None,
    limit: Optional[int] = None,
    season: Optional[int] = None,
    stat_group: Optional[str] = None
) -> Dict[str, Any]:
    """
    Returns a list of stat leaders overall or for a given league (103=AL, 104=NL).
    
    Args:
        leader_categories (str): Required. The statistical category to get leaders for (e.g., 'homeRuns').
        game_types (Optional[str]): Type of games to include (e.g., 'R' for regular season).
        league_id (Optional[int]): League identifier (103 for AL, 104 for NL). If None, returns overall leaders.
        limit (Optional[int]): Maximum number of leaders to return.
        season (Optional[int]): Season year to retrieve data for.
        stat_group (Optional[str]): Grouping of statistics (e.g., 'hitting', 'pitching').
    
    Returns:
        Dict containing:
        - leaders (List[Dict]): List of player or team stat leader entries with rank, name, stat value, and metadata.
        - league_id (Optional[int]): League identifier if filtered; None if overall.
        - season (int): The season year for which the data applies.
        - stat_category (str): The statistical category reported.
        - game_type (str): Type of games included in the stats.
        - limit (int): Maximum number of leaders returned.
        - total_count (int): Total number of records available before limiting.
        - metadata (Dict): Additional contextual information like timestamp, source, and filters.
    
    Raises:
        ValueError: If leader_categories is not provided.
    """
    if not leader_categories:
        raise ValueError("leader_categories is required")

    # Fetch simulated external data
    api_data = call_external_api("mlb-stats-server-get_league_leader_data")

    # Construct leaders list from indexed fields
    leaders = [
        {
            "rank": api_data["leader_0_rank"],
            "player_name": api_data["leader_0_player_name"],
            "team_name": api_data["leader_0_team_name"],
            "stat_value": api_data["leader_0_stat_value"],
            "person_id": api_data["leader_0_person_id"]
        },
        {
            "rank": api_data["leader_1_rank"],
            "player_name": api_data["leader_1_player_name"],
            "team_name": api_data["leader_1_team_name"],
            "stat_value": api_data["leader_1_stat_value"],
            "person_id": api_data["leader_1_person_id"]
        }
    ]

    # Handle optional league_id (0 means null/overall)
    result_league_id = api_data["league_id"] if api_data["league_id"] != 0 else None

    # Construct final result matching output schema
    result = {
        "leaders": leaders,
        "league_id": result_league_id,
        "season": api_data["season"],
        "stat_category": api_data["stat_category"],
        "game_type": api_data["game_type"],
        "limit": api_data["limit"],
        "total_count": api_data["total_count"],
        "metadata": {
            "query_timestamp": api_data["metadata_query_timestamp"],
            "source": api_data["metadata_source"],
            "filters_applied": api_data["metadata_filters_applied"]
        }
    }

    return result