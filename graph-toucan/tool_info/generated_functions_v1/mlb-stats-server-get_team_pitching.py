from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB team pitching statistics.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - pitching_stats_0_season (int): Season year for first record
        - pitching_stats_0_team (str): Team abbreviation for first record
        - pitching_stats_0_league (str): League for first record
        - pitching_stats_0_wins (int): Wins in first season
        - pitching_stats_0_losses (int): Losses in first season
        - pitching_stats_0_era (float): Earned Run Average in first season
        - pitching_stats_0_games (int): Games pitched in first season
        - pitching_stats_0_games_started (int): Games started in first season
        - pitching_stats_0_complete_games (int): Complete games in first season
        - pitching_stats_0_shutouts (int): Shutouts in first season
        - pitching_stats_0_saves (int): Saves in first season
        - pitching_stats_0_innings_pitched (float): Innings pitched in first season
        - pitching_stats_0_hits (int): Hits allowed in first season
        - pitching_stats_0_runs (int): Runs allowed in first season
        - pitching_stats_0_earned_runs (int): Earned runs allowed in first season
        - pitching_stats_0_home_runs (int): Home runs allowed in first season
        - pitching_stats_0_walks (int): Walks issued in first season
        - pitching_stats_0_strikeouts (int): Strikeouts recorded in first season
        - pitching_stats_0_whip (float): WHIP (Walks + Hits per Inning Pitched) in first season
        - pitching_stats_1_season (int): Season year for second record
        - pitching_stats_1_team (str): Team abbreviation for second record
        - pitching_stats_1_league (str): League for second record
        - pitching_stats_1_wins (int): Wins in second season
        - pitching_stats_1_losses (int): Losses in second season
        - pitching_stats_1_era (float): Earned Run Average in second season
        - pitching_stats_1_games (int): Games pitched in second season
        - pitching_stats_1_games_started (int): Games started in second season
        - pitching_stats_1_complete_games (int): Complete games in second season
        - pitching_stats_1_shutouts (int): Shutouts in second season
        - pitching_stats_1_saves (int): Saves in second season
        - pitching_stats_1_innings_pitched (float): Innings pitched in second season
        - pitching_stats_1_hits (int): Hits allowed in second season
        - pitching_stats_1_runs (int): Runs allowed in second season
        - pitching_stats_1_earned_runs (int): Earned runs allowed in second season
        - pitching_stats_1_home_runs (int): Home runs allowed in second season
        - pitching_stats_1_walks (int): Walks issued in second season
        - pitching_stats_1_strikeouts (int): Strikeouts recorded in second season
        - pitching_stats_1_whip (float): WHIP in second season
        - source (str): Data source attribution
        - query_parameters_team (str): Team used in query
        - query_parameters_start_season (int): Start season used in query
        - query_parameters_end_season (int): End season used in query
        - query_parameters_league (str): League used in query
        - metadata_retrieval_timestamp (str): ISO format timestamp of data retrieval
        - metadata_data_coverage (str): Description of season range returned
        - metadata_notes_0 (str): First note or disclaimer
        - metadata_notes_1 (str): Second note or disclaimer
    """
    return {
        "pitching_stats_0_season": 2022,
        "pitching_stats_0_team": "NYY",
        "pitching_stats_0_league": "AL",
        "pitching_stats_0_wins": 99,
        "pitching_stats_0_losses": 63,
        "pitching_stats_0_era": 3.48,
        "pitching_stats_0_games": 162,
        "pitching_stats_0_games_started": 158,
        "pitching_stats_0_complete_games": 5,
        "pitching_stats_0_shutouts": 3,
        "pitching_stats_0_saves": 45,
        "pitching_stats_0_innings_pitched": 1456.1,
        "pitching_stats_0_hits": 1320,
        "pitching_stats_0_runs": 620,
        "pitching_stats_0_earned_runs": 565,
        "pitching_stats_0_home_runs": 189,
        "pitching_stats_0_walks": 480,
        "pitching_stats_0_strikeouts": 1678,
        "pitching_stats_0_whip": 1.23,
        "pitching_stats_1_season": 2023,
        "pitching_stats_1_team": "NYY",
        "pitching_stats_1_league": "AL",
        "pitching_stats_1_wins": 82,
        "pitching_stats_1_losses": 80,
        "pitching_stats_1_era": 4.12,
        "pitching_stats_1_games": 162,
        "pitching_stats_1_games_started": 159,
        "pitching_stats_1_complete_games": 4,
        "pitching_stats_1_shutouts": 2,
        "pitching_stats_1_saves": 38,
        "pitching_stats_1_innings_pitched": 1420.2,
        "pitching_stats_1_hits": 1410,
        "pitching_stats_1_runs": 720,
        "pitching_stats_1_earned_runs": 652,
        "pitching_stats_1_home_runs": 210,
        "pitching_stats_1_walks": 520,
        "pitching_stats_1_strikeouts": 1580,
        "pitching_stats_1_whip": 1.35,
        "source": "Baseball-Reference",
        "query_parameters_team": "NYY",
        "query_parameters_start_season": 2022,
        "query_parameters_end_season": 2023,
        "query_parameters_league": "AL",
        "metadata_retrieval_timestamp": "2024-04-01T12:00:00Z",
        "metadata_data_coverage": "2022 to 2023",
        "metadata_notes_0": "Data may be subject to revision.",
        "metadata_notes_1": "Postseason stats are not included."
    }


def mlb_stats_server_get_team_pitching(
    team: str,
    start_season: int,
    end_season: Optional[int] = None,
    ind: Optional[int] = None,
    league: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get season-level Pitching Statistics for Specific Team (from Baseball-Reference).

    Args:
        team (str): The Team Abbreviation (i.e. 'NYY' for Yankees) of the Team you want data for
        start_season (int): First season you want data for (required)
        end_season (int, optional): Final season you want data for. Defaults to start_season if not provided.
        ind (int, optional): Optional indicator (usage context not specified). Not used in current implementation.
        league (str, optional): League filter (e.g., 'AL', 'NL'). If not provided, defaults to 'MLB'.

    Returns:
        Dict containing:
        - pitching_stats (List[Dict]): List of season-level pitching statistics for the specified team
        - source (str): Attribution indicating the data source
        - query_parameters (Dict): Summary of effective parameters used in the query
        - metadata (Dict): Additional information about the response including timestamp, coverage, and notes

    Raises:
        ValueError: If team is empty or start_season is invalid
    """
    if not team:
        raise ValueError("Team abbreviation is required.")
    if start_season < 1871:  # First MLB season
        raise ValueError("start_season must be a valid year (>= 1871).")
    if end_season is not None and end_season < start_season:
        raise ValueError("end_season cannot be earlier than start_season.")

    # Resolve optional parameters
    effective_end_season = end_season if end_season is not None else start_season
    effective_league = league if league is not None else "MLB"

    # Call external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_team_pitching")

    # Construct pitching_stats list from indexed fields
    pitching_stats = [
        {
            "season": api_data["pitching_stats_0_season"],
            "team": api_data["pitching_stats_0_team"],
            "league": api_data["pitching_stats_0_league"],
            "wins": api_data["pitching_stats_0_wins"],
            "losses": api_data["pitching_stats_0_losses"],
            "era": api_data["pitching_stats_0_era"],
            "games": api_data["pitching_stats_0_games"],
            "games_started": api_data["pitching_stats_0_games_started"],
            "complete_games": api_data["pitching_stats_0_complete_games"],
            "shutouts": api_data["pitching_stats_0_shutouts"],
            "saves": api_data["pitching_stats_0_saves"],
            "innings_pitched": api_data["pitching_stats_0_innings_pitched"],
            "hits": api_data["pitching_stats_0_hits"],
            "runs": api_data["pitching_stats_0_runs"],
            "earned_runs": api_data["pitching_stats_0_earned_runs"],
            "home_runs": api_data["pitching_stats_0_home_runs"],
            "walks": api_data["pitching_stats_0_walks"],
            "strikeouts": api_data["pitching_stats_0_strikeouts"],
            "whip": api_data["pitching_stats_0_whip"]
        },
        {
            "season": api_data["pitching_stats_1_season"],
            "team": api_data["pitching_stats_1_team"],
            "league": api_data["pitching_stats_1_league"],
            "wins": api_data["pitching_stats_1_wins"],
            "losses": api_data["pitching_stats_1_losses"],
            "era": api_data["pitching_stats_1_era"],
            "games": api_data["pitching_stats_1_games"],
            "games_started": api_data["pitching_stats_1_games_started"],
            "complete_games": api_data["pitching_stats_1_complete_games"],
            "shutouts": api_data["pitching_stats_1_shutouts"],
            "saves": api_data["pitching_stats_1_saves"],
            "innings_pitched": api_data["pitching_stats_1_innings_pitched"],
            "hits": api_data["pitching_stats_1_hits"],
            "runs": api_data["pitching_stats_1_runs"],
            "earned_runs": api_data["pitching_stats_1_earned_runs"],
            "home_runs": api_data["pitching_stats_1_home_runs"],
            "walks": api_data["pitching_stats_1_walks"],
            "strikeouts": api_data["pitching_stats_1_strikeouts"],
            "whip": api_data["pitching_stats_1_whip"]
        }
    ]

    # Filter out seasons not in the requested range
    pitching_stats = [
        stat for stat in pitching_stats
        if start_season <= stat["season"] <= effective_end_season
    ]

    # Construct response
    response = {
        "pitching_stats": pitching_stats,
        "source": api_data["source"],
        "query_parameters": {
            "team": team,
            "start_season": start_season,
            "end_season": effective_end_season,
            "league": effective_league,
            "ind": ind
        },
        "metadata": {
            "retrieval_timestamp": api_data["metadata_retrieval_timestamp"],
            "data_coverage": api_data["metadata_data_coverage"],
            "notes": [
                api_data["metadata_notes_0"],
                api_data["metadata_notes_1"]
            ]
        }
    }

    return response