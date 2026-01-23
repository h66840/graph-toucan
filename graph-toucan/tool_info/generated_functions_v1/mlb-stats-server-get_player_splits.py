from typing import Dict, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB player splits.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - splits_data_home_games (int): Number of games played at home
        - splits_data_home_at_bats (int): At-bats in home games
        - splits_data_home_hits (int): Hits in home games
        - splits_data_away_games (int): Number of games played away
        - splits_data_away_at_bats (int): At-bats in away games
        - splits_data_away_hits (int): Hits in away games
        - splits_data_vs_left_games (int): Games played against left-handed pitchers
        - splits_data_vs_left_at_bats (int): At-bats against left-handed pitchers
        - splits_data_vs_left_hits (int): Hits against left-handed pitchers
        - splits_data_vs_right_games (int): Games played against right-handed pitchers
        - splits_data_vs_right_at_bats (int): At-bats against right-handed pitchers
        - splits_data_vs_right_hits (int): Hits against right-handed pitchers
        - splits_data_jan_games (int): Games played in January
        - splits_data_feb_games (int): Games played in February
        - player_info_position (str): Player's position
        - player_info_batting_hand (str): Batting hand ('Left', 'Right', 'Switch')
        - player_info_throwing_hand (str): Throwing hand ('Left', 'Right')
        - player_info_height (str): Height in format "6'2\""
        - player_info_weight (int): Weight in pounds
        - player_info_team (str): Current team name
        - player_info_status (str): Current status ('Active', 'Inactive', etc.)
        - year (int): The year for which stats are reported
        - player_id (str): Unique player identifier
        - pitching_splits (bool): Whether the splits are for pitching
        - metadata_source (str): Data source name
        - metadata_timestamp (str): ISO format timestamp of query
        - metadata_disclaimer (str): Disclaimer about data accuracy
    """
    return {
        "splits_data_home_games": 45,
        "splits_data_home_at_bats": 180,
        "splits_data_home_hits": 54,
        "splits_data_away_games": 43,
        "splits_data_away_at_bats": 170,
        "splits_data_away_hits": 43,
        "splits_data_vs_left_games": 25,
        "splits_data_vs_left_at_bats": 95,
        "splits_data_vs_left_hits": 30,
        "splits_data_vs_right_games": 63,
        "splits_data_vs_right_at_bats": 245,
        "splits_data_vs_right_hits": 63,
        "splits_data_jan_games": 5,
        "splits_data_feb_games": 8,
        "player_info_position": "CF",
        "player_info_batting_hand": "Left",
        "player_info_throwing_hand": "Right",
        "player_info_height": "6'1\"",
        "player_info_weight": 185,
        "player_info_team": "New York Yankees",
        "player_info_status": "Active",
        "year": 2023,
        "player_id": "123456",
        "pitching_splits": False,
        "metadata_source": "MLB Stats API",
        "metadata_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata_disclaimer": "Data is simulated for demonstration purposes."
    }


def mlb_stats_server_get_player_splits(
    playerid: str,
    pitching_splits: Optional[bool] = False,
    player_info: Optional[bool] = False,
    year: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Returns a dataframe of all split stats for a given player.
    If player_info is True, this will also return a dictionary that includes player position,
    handedness, height, weight, position, and team.

    Args:
        playerid (str): The unique identifier of the player for whom splits are retrieved (required)
        pitching_splits (bool, optional): Whether to return pitching splits (True) or batting splits (False). Defaults to False.
        player_info (bool, optional): Whether to include personal and professional player details. Defaults to False.
        year (int, optional): The year for which split statistics are reported. If None, returns career splits.

    Returns:
        Dict containing:
        - splits_data (Dict): A dictionary where keys represent different split categories (e.g., 'home', 'away', 'vs_left', 'vs_right', 'month')
          and values are structured dictionaries containing corresponding performance statistics.
        - player_info (Dict, optional): Dictionary containing personal and professional details about the player.
        - year (int): The year for which split statistics are reported; may be null if career splits across multiple years are returned.
        - player_id (str): The unique identifier of the player.
        - pitching_splits (bool): Indicates whether the returned splits are for pitching performance.
        - metadata (Dict): Additional context such as data source, query timestamp, and disclaimers.

    Raises:
        ValueError: If playerid is empty or None.
    """
    if not playerid:
        raise ValueError("playerid is required")

    # Call the external API to get flat data
    api_data = call_external_api("mlb-stats-server-get_player_splits")

    # Construct splits_data
    splits_data = {
        "home": {
            "games": api_data["splits_data_home_games"],
            "at_bats": api_data["splits_data_home_at_bats"],
            "hits": api_data["splits_data_home_hits"],
        },
        "away": {
            "games": api_data["splits_data_away_games"],
            "at_bats": api_data["splits_data_away_at_bats"],
            "hits": api_data["splits_data_away_hits"],
        },
        "vs_left": {
            "games": api_data["splits_data_vs_left_games"],
            "at_bats": api_data["splits_data_vs_left_at_bats"],
            "hits": api_data["splits_data_vs_left_hits"],
        },
        "vs_right": {
            "games": api_data["splits_data_vs_right_games"],
            "at_bats": api_data["splits_data_vs_right_at_bats"],
            "hits": api_data["splits_data_vs_right_hits"],
        },
        "month": {
            "January": {"games": api_data["splits_data_jan_games"]},
            "February": {"games": api_data["splits_data_feb_games"]},
        },
    }

    # Construct player_info if requested
    result_player_info = None
    if player_info:
        result_player_info = {
            "position": api_data["player_info_position"],
            "batting_hand": api_data["player_info_batting_hand"],
            "throwing_hand": api_data["player_info_throwing_hand"],
            "height": api_data["player_info_height"],
            "weight": api_data["player_info_weight"],
            "team": api_data["player_info_team"],
            "status": api_data["player_info_status"],
        }

    # Construct metadata
    metadata = {
        "source": api_data["metadata_source"],
        "timestamp": api_data["metadata_timestamp"],
        "disclaimer": api_data["metadata_disclaimer"],
    }

    # Final result
    result = {
        "splits_data": splits_data,
        "player_id": api_data["player_id"],
        "pitching_splits": api_data["pitching_splits"],
        "metadata": metadata,
    }

    # Add optional fields
    if result_player_info is not None:
        result["player_info"] = result_player_info

    # Use provided year if available, otherwise use API year
    result["year"] = year if year is not None else api_data["year"]

    return result