from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB standings.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - standings_0_team (str): Name of the first team in standings
        - standings_0_wins (int): Wins for the first team
        - standings_0_losses (int): Losses for the first team
        - standings_0_division_rank (int): Division rank of the first team
        - standings_0_win_percentage (float): Win percentage of the first team
        - standings_0_games_behind (float): Games behind leader for the first team
        - standings_1_team (str): Name of the second team in standings
        - standings_1_wins (int): Wins for the second team
        - standings_1_losses (int): Losses for the second team
        - standings_1_division_rank (int): Division rank of the second team
        - standings_1_win_percentage (float): Win percentage of the second team
        - standings_1_games_behind (float): Games behind leader for the second team
        - season (int): The MLB season year
        - last_updated (str): ISO 8601 timestamp when standings were last updated
        - has_current_standings (bool): Whether the season is currently active
        - league_American_League (str): Comma-separated divisions in American League
        - league_National_League (str): Comma-separated divisions in National League
    """
    return {
        "standings_0_team": "New York Yankees",
        "standings_0_wins": 92,
        "standings_0_losses": 70,
        "standings_0_division_rank": 1,
        "standings_0_win_percentage": 0.568,
        "standings_0_games_behind": 0.0,
        "standings_1_team": "Boston Red Sox",
        "standings_1_wins": 87,
        "standings_1_losses": 75,
        "standings_1_division_rank": 2,
        "standings_1_win_percentage": 0.537,
        "standings_1_games_behind": 5.5,
        "season": 2023,
        "last_updated": "2023-09-25T18:30:00",
        "has_current_standings": True,
        "league_American_League": "East, Central, West",
        "league_National_League": "East, Central, West"
    }


def mlb_stats_server_get_pybaseball_standings(season: Optional[int] = None) -> Dict[str, Any]:
    """
    Returns a dictionary containing MLB standings for a given season, or the most recent standings
    if the season is not specified.

    Args:
        season (Optional[int]): The year of the MLB season. If None, defaults to latest season.

    Returns:
        Dict[str, Any]: A dictionary with the following keys:
            - standings (List[Dict]): List of team standings entries with team name, wins, losses,
              division rank, win percentage, and games behind.
            - season (int): The MLB season year.
            - last_updated (str): ISO 8601 timestamp indicating when the standings were last updated.
            - has_current_standings (bool): Indicates whether the season is currently active.
            - league (Dict): Structure of the MLB leagues and their divisions.
    """
    # Use provided season or default to 2023 if not specified
    current_season = season if season is not None else 2023

    # Fetch simulated external data
    api_data = call_external_api("mlb-stats-server-get_pybaseball_standings")

    # Validate that the returned season matches our requested season
    if api_data["season"] != current_season:
        # Simulate updating the data to match requested season
        api_data["season"] = current_season
        # Adjust last updated timestamp accordingly
        api_data["last_updated"] = f"{current_season}-06-15T12:00:00"
        api_data["has_current_standings"] = True if current_season == datetime.now().year else False

    # Construct standings list from indexed fields
    standings = [
        {
            "team": api_data["standings_0_team"],
            "wins": api_data["standings_0_wins"],
            "losses": api_data["standings_0_losses"],
            "division_rank": api_data["standings_0_division_rank"],
            "win_percentage": api_data["standings_0_win_percentage"],
            "games_behind": api_data["standings_0_games_behind"]
        },
        {
            "team": api_data["standings_1_team"],
            "wins": api_data["standings_1_wins"],
            "losses": api_data["standings_1_losses"],
            "division_rank": api_data["standings_1_division_rank"],
            "win_percentage": api_data["standings_1_win_percentage"],
            "games_behind": api_data["standings_1_games_behind"]
        }
    ]

    # Reconstruct league structure
    league = {
        "American League": [
            division.strip() for division in api_data["league_American_League"].split(",")
        ],
        "National League": [
            division.strip() for division in api_data["league_National_League"].split(",")
        ]
    }

    # Build final result dictionary matching output schema
    result = {
        "standings": standings,
        "season": api_data["season"],
        "last_updated": api_data["last_updated"],
        "has_current_standings": api_data["has_current_standings"],
        "league": league
    }

    return result