from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB standings.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - standings_0_team_name (str): Name of the first team in standings
        - standings_0_wins (int): Wins for the first team
        - standings_0_losses (int): Losses for the first team
        - standings_0_win_percentage (float): Win percentage for the first team
        - standings_0_games_back (str): Games back for the first team
        - standings_0_division_rank (int): Division rank for the first team
        - standings_0_league_rank (int): League rank for the first team
        - standings_0_streak (str): Current streak for the first team
        - standings_0_last_10_record (str): Last 10 games record for the first team
        - standings_1_team_name (str): Name of the second team in standings
        - standings_1_wins (int): Wins for the second team
        - standings_1_losses (int): Losses for the second team
        - standings_1_win_percentage (float): Win percentage for the second team
        - standings_1_games_back (str): Games back for the second team
        - standings_1_division_rank (int): Division rank for the second team
        - standings_1_league_rank (int): League rank for the second team
        - standings_1_streak (str): Current streak for the second team
        - standings_1_last_10_record (str): Last 10 games record for the second team
        - league (str): Name of the league
        - division (str): Name of the division, or null if not applicable
        - season (int): The season year
        - standings_type (str): Type of standings (e.g., regularSeason)
        - last_updated (str): ISO 8601 timestamp of last update
        - metadata_source (str): Data source identifier
        - metadata_api_version (str): API version used
        - metadata_disclaimer (str): Disclaimer about data accuracy
    """
    return {
        "standings_0_team_name": "New York Yankees",
        "standings_0_wins": 65,
        "standings_0_losses": 35,
        "standings_0_win_percentage": 0.650,
        "standings_0_games_back": "0.0",
        "standings_0_division_rank": 1,
        "standings_0_league_rank": 1,
        "standings_0_streak": "W3",
        "standings_0_last_10_record": "7-3",
        "standings_1_team_name": "Boston Red Sox",
        "standings_1_wins": 58,
        "standings_1_losses": 42,
        "standings_1_win_percentage": 0.580,
        "standings_1_games_back": "7.0",
        "standings_1_division_rank": 2,
        "standings_1_league_rank": 4,
        "standings_1_streak": "L1",
        "standings_1_last_10_record": "5-5",
        "league": "American League",
        "division": "East",
        "season": 2024,
        "standings_type": "regularSeason",
        "last_updated": "2024-07-05T14:30:00Z",
        "metadata_source": "MLB Stats API",
        "metadata_api_version": "v1",
        "metadata_disclaimer": "Data may be delayed by up to 15 minutes."
    }


def mlb_stats_server_get_standings(
    division_id: Optional[str] = None,
    league_id: Optional[str] = None,
    season: Optional[str] = None,
    standings_types: Optional[str] = None
) -> Dict[str, Any]:
    """
    Returns a dict of standings data for a given league/division and season.

    Args:
        division_id (Optional[str]): The division ID to filter standings by.
        league_id (Optional[str]): The league ID to filter standings by.
        season (Optional[str]): The season year to retrieve standings for.
        standings_types (Optional[str]): The type of standings to retrieve (e.g., 'regularSeason').

    Returns:
        Dict containing:
        - standings (List[Dict]): List of team standings entries with keys like 'team_name', 'wins', etc.
        - league (str): Name of the league.
        - division (str): Name of the division, or None if not applicable.
        - season (int): The season year.
        - standings_type (str): Type of standings returned.
        - last_updated (str): ISO 8601 timestamp of when data was last updated.
        - metadata (Dict): Additional context including source, API version, and disclaimers.
    """
    # Call the external API to get flattened data
    api_data = call_external_api("mlb-stats-server-get_standings")

    # Construct standings list from indexed fields
    standings = [
        {
            "team_name": api_data["standings_0_team_name"],
            "wins": api_data["standings_0_wins"],
            "losses": api_data["standings_0_losses"],
            "win_percentage": api_data["standings_0_win_percentage"],
            "games_back": api_data["standings_0_games_back"],
            "division_rank": api_data["standings_0_division_rank"],
            "league_rank": api_data["standings_0_league_rank"],
            "streak": api_data["standings_0_streak"],
            "last_10_record": api_data["standings_0_last_10_record"]
        },
        {
            "team_name": api_data["standings_1_team_name"],
            "wins": api_data["standings_1_wins"],
            "losses": api_data["standings_1_losses"],
            "win_percentage": api_data["standings_1_win_percentage"],
            "games_back": api_data["standings_1_games_back"],
            "division_rank": api_data["standings_1_division_rank"],
            "league_rank": api_data["standings_1_league_rank"],
            "streak": api_data["standings_1_streak"],
            "last_10_record": api_data["standings_1_last_10_record"]
        }
    ]

    # Construct metadata
    metadata = {
        "source": api_data["metadata_source"],
        "api_version": api_data["metadata_api_version"],
        "disclaimer": api_data["metadata_disclaimer"]
    }

    # Build final result
    result = {
        "standings": standings,
        "league": api_data["league"],
        "division": api_data["division"] if api_data["division"] != "null" else None,
        "season": api_data["season"],
        "standings_type": api_data["standings_type"],
        "last_updated": api_data["last_updated"],
        "metadata": metadata
    }

    return result