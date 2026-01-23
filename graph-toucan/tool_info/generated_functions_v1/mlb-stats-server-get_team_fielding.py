from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB team fielding statistics.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - team_fielding_stats_0_season (int): Season year for first entry
        - team_fielding_stats_0_team (str): Team abbreviation for first entry
        - team_fielding_stats_0_league (str): League for first entry
        - team_fielding_stats_0_g (int): Games played in first entry
        - team_fielding_stats_0_gs (int): Games started in first entry
        - team_fielding_stats_0_ip (float): Innings played in first entry
        - team_fielding_stats_0_po (int): Putouts in first entry
        - team_fielding_stats_0_a (int): Assists in first entry
        - team_fielding_stats_0_e (int): Errors in first entry
        - team_fielding_stats_0_dp (int): Double plays in first entry
        - team_fielding_stats_1_season (int): Season year for second entry
        - team_fielding_stats_1_team (str): Team abbreviation for second entry
        - team_fielding_stats_1_league (str): League for second entry
        - team_fielding_stats_1_g (int): Games played in second entry
        - team_fielding_stats_1_gs (int): Games started in second entry
        - team_fielding_stats_1_ip (float): Innings played in second entry
        - team_fielding_stats_1_po (int): Putouts in second entry
        - team_fielding_stats_1_a (int): Assists in second entry
        - team_fielding_stats_1_e (int): Errors in second entry
        - team_fielding_stats_1_dp (int): Double plays in second entry
        - metadata_team (str): Team abbreviation in metadata
        - metadata_start_season (int): Start season in metadata
        - metadata_end_season (int): End season in metadata
        - metadata_league (str): League filter in metadata
        - metadata_source (str): Data source name
        - source_url (str): URL of the Baseball-Reference page
    """
    return {
        "team_fielding_stats_0_season": 2022,
        "team_fielding_stats_0_team": "NYY",
        "team_fielding_stats_0_league": "AL",
        "team_fielding_stats_0_g": 162,
        "team_fielding_stats_0_gs": 162,
        "team_fielding_stats_0_ip": 1458.0,
        "team_fielding_stats_0_po": 1650,
        "team_fielding_stats_0_a": 1350,
        "team_fielding_stats_0_e": 78,
        "team_fielding_stats_0_dp": 112,
        "team_fielding_stats_1_season": 2023,
        "team_fielding_stats_1_team": "NYY",
        "team_fielding_stats_1_league": "AL",
        "team_fielding_stats_1_g": 162,
        "team_fielding_stats_1_gs": 162,
        "team_fielding_stats_1_ip": 1458.0,
        "team_fielding_stats_1_po": 1670,
        "team_fielding_stats_1_a": 1365,
        "team_fielding_stats_1_e": 72,
        "team_fielding_stats_1_dp": 115,
        "metadata_team": "NYY",
        "metadata_start_season": 2022,
        "metadata_end_season": 2023,
        "metadata_league": "AL",
        "metadata_source": "Baseball-Reference",
        "source_url": "https://www.baseball-reference.com/teams/NYY/"
    }

def mlb_stats_server_get_team_fielding(
    team: str,
    start_season: int,
    end_season: Optional[int] = None,
    ind: Optional[int] = None,
    league: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get season-level Fielding Statistics for Specific Team (from Baseball-Reference).
    
    Args:
        team (str): The Team Abbreviation (i.e., 'NYY' for Yankees) of the team you want data for.
        start_season (int): First season you want data for (or the only season if end_season is not specified).
        end_season (Optional[int]): Final season you want data for. If not provided, defaults to start_season.
        ind (Optional[int]): Indicator for data aggregation (e.g., 0 for overall, 1 for per game). Not used in simulation.
        league (Optional[str]): League filter (e.g., 'AL', 'NL'). If not provided, defaults to 'MLB'.
    
    Returns:
        Dict containing:
        - team_fielding_stats (List[Dict]): List of season-level fielding statistics for the specified team.
        - metadata (Dict): Information about the query parameters and data source.
        - source_url (str): URL of the Baseball-Reference page from which the data was retrieved.
    
    Raises:
        ValueError: If team is empty or start_season is invalid.
    """
    if not team:
        raise ValueError("Team abbreviation is required.")
    if start_season <= 0:
        raise ValueError("Start season must be a positive integer.")
    
    if end_season is None:
        end_season = start_season
    if end_season < start_season:
        raise ValueError("End season cannot be earlier than start season.")
    
    if league is None:
        league = "MLB"
    
    # Fetch simulated external data
    api_data = call_external_api("mlb-stats-server-get_team_fielding")
    
    # Construct team_fielding_stats list from indexed fields
    team_fielding_stats = [
        {
            "season": api_data["team_fielding_stats_0_season"],
            "team": api_data["team_fielding_stats_0_team"],
            "league": api_data["team_fielding_stats_0_league"],
            "g": api_data["team_fielding_stats_0_g"],
            "gs": api_data["team_fielding_stats_0_gs"],
            "ip": api_data["team_fielding_stats_0_ip"],
            "po": api_data["team_fielding_stats_0_po"],
            "a": api_data["team_fielding_stats_0_a"],
            "e": api_data["team_fielding_stats_0_e"],
            "dp": api_data["team_fielding_stats_0_dp"]
        },
        {
            "season": api_data["team_fielding_stats_1_season"],
            "team": api_data["team_fielding_stats_1_team"],
            "league": api_data["team_fielding_stats_1_league"],
            "g": api_data["team_fielding_stats_1_g"],
            "gs": api_data["team_fielding_stats_1_gs"],
            "ip": api_data["team_fielding_stats_1_ip"],
            "po": api_data["team_fielding_stats_1_po"],
            "a": api_data["team_fielding_stats_1_a"],
            "e": api_data["team_fielding_stats_1_e"],
            "dp": api_data["team_fielding_stats_1_dp"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "team": api_data["metadata_team"],
        "requested_season_range": [api_data["metadata_start_season"], api_data["metadata_end_season"]],
        "league_filter": api_data["metadata_league"],
        "data_origin": api_data["metadata_source"]
    }
    
    # Return final structured result
    return {
        "team_fielding_stats": team_fielding_stats,
        "metadata": metadata,
        "source_url": api_data["source_url"]
    }