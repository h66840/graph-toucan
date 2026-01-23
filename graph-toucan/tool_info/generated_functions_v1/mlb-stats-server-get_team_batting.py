from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB team batting statistics.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - batting_stats_0_g (int): Games played in first season
        - batting_stats_0_ab (int): At-bats in first season
        - batting_stats_0_r (int): Runs scored in first season
        - batting_stats_0_h (int): Hits in first season
        - batting_stats_0_hr (int): Home runs in first season
        - batting_stats_0_rbi (int): RBIs in first season
        - batting_stats_0_avg (float): Batting average in first season
        - batting_stats_0_obp (float): On-base percentage in first season
        - batting_stats_0_slg (float): Slugging percentage in first season
        - batting_stats_1_g (int): Games played in second season
        - batting_stats_1_ab (int): At-bats in second season
        - batting_stats_1_r (int): Runs scored in second season
        - batting_stats_1_h (int): Hits in second season
        - batting_stats_1_hr (int): Home runs in second season
        - batting_stats_1_rbi (int): RBIs in second season
        - batting_stats_1_avg (float): Batting average in second season
        - batting_stats_1_obp (float): On-base percentage in second season
        - batting_stats_1_slg (float): Slugging percentage in second season
        - team (str): Team abbreviation (e.g., 'NYY')
        - seasons_0 (int): First season in range
        - seasons_1 (int): Second season in range
        - source (str): Data source identifier, e.g., 'Baseball-Reference'
        - metadata_retrieval_timestamp (str): ISO format timestamp of data retrieval
        - metadata_league_scope (str): League scope ('all', 'AL', 'NL')
        - metadata_notes (str): Any disclaimers or notes about data
    """
    return {
        "batting_stats_0_g": 162,
        "batting_stats_0_ab": 5500,
        "batting_stats_0_r": 850,
        "batting_stats_0_h": 1450,
        "batting_stats_0_hr": 210,
        "batting_stats_0_rbi": 820,
        "batting_stats_0_avg": 0.264,
        "batting_stats_0_obp": 0.330,
        "batting_stats_0_slg": 0.445,
        "batting_stats_1_g": 162,
        "batting_stats_1_ab": 5480,
        "batting_stats_1_r": 870,
        "batting_stats_1_h": 1480,
        "batting_stats_1_hr": 230,
        "batting_stats_1_rbi": 845,
        "batting_stats_1_avg": 0.270,
        "batting_stats_1_obp": 0.338,
        "batting_stats_1_slg": 0.460,
        "team": "NYY",
        "seasons_0": 2022,
        "seasons_1": 2023,
        "source": "Baseball-Reference",
        "metadata_retrieval_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_league_scope": "all",
        "metadata_notes": "Data includes regular season only. No postseason stats included."
    }


def mlb_stats_server_get_team_batting(
    team: str,
    start_season: int,
    end_season: Optional[int] = None,
    ind: Optional[int] = None,
    league: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get season-level Batting Statistics for a Specific MLB Team (simulated from Baseball-Reference).

    Args:
        team (str): The Team Abbreviation (e.g., 'NYY' for Yankees) of the team to retrieve data for.
        start_season (int): The first season to include in the data (required).
        end_season (int, optional): The final season to include. If not provided, only start_season is used.
        ind (int, optional): Optional indicator; behavior unspecified in documentation.
        league (str, optional): League filter ('AL', 'NL', or 'all'). Defaults to 'all' if not specified.

    Returns:
        Dict containing:
            - batting_stats (List[Dict]): List of season-level batting statistics per season.
            - team (str): The team abbreviation.
            - seasons (List[int]): List of seasons covered.
            - source (str): Identifier for the data source.
            - metadata (Dict): Additional contextual information including timestamp, league scope, and notes.

    Example:
        >>> data = mlb_stats_server_get_team_batting(team='NYY', start_season=2022, end_season=2023)
        >>> print(data['batting_stats'][0]['h'])  # Access hits from first season
    """
    # Input validation
    if not team:
        raise ValueError("Team abbreviation is required.")
    if start_season < 1871:
        raise ValueError("start_season must be a valid MLB year (1871 or later).")
    if end_season is not None and end_season < start_season:
        raise ValueError("end_season cannot be earlier than start_season.")

    # Set end_season to start_season if not provided
    if end_season is None:
        end_season = start_season

    # Determine number of seasons (limit to 2 for simulation consistency with call_external_api)
    seasons = list(range(start_season, min(end_season + 1, start_season + 2)))
    if len(seasons) > 2:
        seasons = seasons[:2]

    # Call external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_team_batting")

    # Construct batting_stats list from indexed fields
    batting_stats = []
    for i, season in enumerate(seasons):
        prefix = f"batting_stats_{i}_"
        try:
            stat = {
                "g": api_data[f"{prefix}g"],
                "ab": api_data[f"{prefix}ab"],
                "r": api_data[f"{prefix}r"],
                "h": api_data[f"{prefix}h"],
                "hr": api_data[f"{prefix}hr"],
                "rbi": api_data[f"{prefix}rbi"],
                "avg": round(float(api_data[f"{prefix}avg"]), 3),
                "obp": round(float(api_data[f"{prefix}obp"]), 3),
                "slg": round(float(api_data[f"{prefix}slg"]), 3),
            }
            batting_stats.append(stat)
        except KeyError as e:
            raise KeyError(f"Missing expected field in API response: {e}")

    # Construct metadata
    metadata = {
        "retrieval_timestamp": api_data["metadata_retrieval_timestamp"],
        "league_scope": league if league in ("AL", "NL") else "all",
        "notes": api_data["metadata_notes"]
    }

    # Final result structure
    result = {
        "batting_stats": batting_stats,
        "team": team.upper(),
        "seasons": seasons,
        "source": api_data["source"],
        "metadata": metadata
    }

    return result