from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching pitching stats data from an external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - pitching_stats_0_player_name (str): Name of the first player
        - pitching_stats_0_season (int): Season of the first player's stats
        - pitching_stats_0_team (str): Team of the first player
        - pitching_stats_0_ip (float): Innings pitched by the first player
        - pitching_stats_0_era (float): ERA of the first player
        - pitching_stats_0_so (int): Strikeouts by the first player
        - pitching_stats_0_bb (int): Walks issued by the first player
        - pitching_stats_1_player_name (str): Name of the second player
        - pitching_stats_1_season (int): Season of the second player's stats
        - pitching_stats_1_team (str): Team of the second player
        - pitching_stats_1_ip (float): Innings pitched by the second player
        - pitching_stats_1_era (float): ERA of the second player
        - pitching_stats_1_so (int): Strikeouts by the second player
        - pitching_stats_1_bb (int): Walks issued by the second player
        - metadata_start_season (int): Start season used in query
        - metadata_end_season (int): End season used in query
        - metadata_league (str): League filter used
        - metadata_qual (int): Minimum plate appearances qualifier
        - metadata_ind (int): Individual (1) or aggregate (0) flag
        - total_players (int): Total number of players returned
        - source (str): Data source name
    """
    return {
        "pitching_stats_0_player_name": "Max Scherzer",
        "pitching_stats_0_season": 2022,
        "pitching_stats_0_team": "LAD",
        "pitching_stats_0_ip": 175.1,
        "pitching_stats_0_era": 2.29,
        "pitching_stats_0_so": 200,
        "pitching_stats_0_bb": 35,
        "pitching_stats_1_player_name": "Jacob deGrom",
        "pitching_stats_1_season": 2022,
        "pitching_stats_1_team": "NYM",
        "pitching_stats_1_ip": 141.0,
        "pitching_stats_1_era": 3.08,
        "pitching_stats_1_so": 185,
        "pitching_stats_1_bb": 28,
        "metadata_start_season": 2022,
        "metadata_end_season": 2022,
        "metadata_league": "all",
        "metadata_qual": 100,
        "metadata_ind": 1,
        "total_players": 2,
        "source": "FanGraphs"
    }

def mlb_stats_server_get_pitching_stats(
    start_season: int,
    end_season: Optional[int] = None,
    league: Optional[str] = "all",
    qual: Optional[int] = None,
    ind: Optional[int] = 1
) -> Dict[str, Any]:
    """
    Get season-level pitching data from FanGraphs.

    Args:
        start_season (int): First season to retrieve data from (required)
        end_season (Optional[int]): Final season to retrieve data from. If None, only start_season is returned
        league (Optional[str]): League filter - "all", "nl", "al", or "mnl". Default is "all"
        qual (Optional[int]): Minimum number of plate appearances to be included
        ind (Optional[int]): 1 for individual season level, 0 for aggregate data. Default is 1

    Returns:
        Dict containing:
        - pitching_stats (List[Dict]): List of dictionaries with season-level pitching statistics
        - metadata (Dict): Query parameters used
        - total_players (int): Number of players returned
        - source (str): Data source ("FanGraphs")

    Raises:
        ValueError: If start_season is not provided or invalid
    """
    if start_season is None:
        raise ValueError("start_season is required")
    if start_season < 1876 or start_season > 2025:
        raise ValueError("start_season must be a valid MLB season (1876-2025)")
    if end_season is not None and (end_season < start_season or end_season > 2025):
        raise ValueError("end_season must be >= start_season and <= 2025")
    if league not in ["all", "nl", "al", "mnl"]:
        raise ValueError("league must be one of: all, nl, al, mnl")
    if ind not in [0, 1]:
        raise ValueError("ind must be 0 (aggregate) or 1 (individual)")

    # Use default values if not provided
    effective_end_season = end_season if end_season is not None else start_season
    effective_qual = qual if qual is not None else 100
    effective_league = league if league is not None else "all"
    effective_ind = ind if ind is not None else 1

    # Call external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_pitching_stats")

    # Construct pitching_stats list from indexed fields
    pitching_stats = [
        {
            "player_name": api_data["pitching_stats_0_player_name"],
            "season": api_data["pitching_stats_0_season"],
            "team": api_data["pitching_stats_0_team"],
            "ip": api_data["pitching_stats_0_ip"],
            "era": api_data["pitching_stats_0_era"],
            "so": api_data["pitching_stats_0_so"],
            "bb": api_data["pitching_stats_0_bb"]
        },
        {
            "player_name": api_data["pitching_stats_1_player_name"],
            "season": api_data["pitching_stats_1_season"],
            "team": api_data["pitching_stats_1_team"],
            "ip": api_data["pitching_stats_1_ip"],
            "era": api_data["pitching_stats_1_era"],
            "so": api_data["pitching_stats_1_so"],
            "bb": api_data["pitching_stats_1_bb"]
        }
    ]

    # Construct metadata
    metadata = {
        "start_season": api_data["metadata_start_season"],
        "end_season": api_data["metadata_end_season"],
        "league": api_data["metadata_league"],
        "qual": api_data["metadata_qual"],
        "ind": api_data["metadata_ind"]
    }

    # Return final structured response
    return {
        "pitching_stats": pitching_stats,
        "metadata": metadata,
        "total_players": api_data["total_players"],
        "source": api_data["source"]
    }