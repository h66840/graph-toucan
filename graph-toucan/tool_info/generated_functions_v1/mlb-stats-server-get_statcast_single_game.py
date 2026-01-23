from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB Statcast single game.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - game_pk (int): MLB game ID
        - game_date (str): Game date in YYYY-MM-DD format
        - venue (str): Name of the stadium/venue
        - home_team (str): Home team abbreviation
        - away_team (str): Away team abbreviation
        - start_time (str): Game start time in UTC
        - weather_temperature (int): Temperature in Fahrenheit
        - weather_condition (str): Description of weather conditions
        - total_play_count (int): Total number of plays returned
        - truncation_applied (bool): Whether truncation was applied
        - request_timestamp (str): ISO timestamp of the request
        - request_start_row (int): Start row used in request (optional)
        - request_end_row (int): End row used in request (optional)
        - warning (str): Any warning message from the API
        - play_0_pitch_number (int): Pitch number in at-bat
        - play_0_inning (int): Inning number
        - play_0_batter_id (int): MLBAM ID of batter
        - play_0_pitcher_id (int): MLBAM ID of pitcher
        - play_0_pitch_type (str): Pitch type abbreviation (e.g., 'FF')
        - play_0_release_speed (float): Release speed in mph
        - play_0_estimated_woba (float): Expected wOBA value
        - play_0_launch_angle (float): Launch angle in degrees
        - play_0_exit_velocity (float): Exit velocity in mph
        - play_0_hc_x (float): Hit coordinate x
        - play_0_hc_y (float): Hit coordinate y
        - play_0_events (str): Event type (e.g., 'single', 'home_run')
        - play_0_description (str): Text description of the play
        - play_1_pitch_number (int): Pitch number in at-bat
        - play_1_inning (int): Inning number
        - play_1_batter_id (int): MLBAM ID of batter
        - play_1_pitcher_id (int): MLBAM ID of pitcher
        - play_1_pitch_type (str): Pitch type abbreviation (e.g., 'SL')
        - play_1_release_speed (float): Release speed in mph
        - play_1_estimated_woba (float): Expected wOBA value
        - play_1_launch_angle (float): Launch angle in degrees
        - play_1_exit_velocity (float): Exit velocity in mph
        - play_1_hc_x (float): Hit coordinate x
        - play_1_hc_y (float): Hit coordinate y
        - play_1_events (str): Event type (e.g., 'strikeout')
        - play_1_description (str): Text description of the play
    """
    return {
        "game_pk": 715234,
        "game_date": "2023-06-15",
        "venue": "Dodger Stadium",
        "home_team": "LAD",
        "away_team": "NYY",
        "start_time": "2023-06-15T00:08:00Z",
        "weather_temperature": 72,
        "weather_condition": "Clear",
        "total_play_count": 150,
        "truncation_applied": True,
        "request_timestamp": "2023-06-15T03:22:10Z",
        "request_start_row": 0,
        "request_end_row": 2,
        "warning": "Only first 2 plays returned due to truncation",
        "play_0_pitch_number": 1,
        "play_0_inning": 1,
        "play_0_batter_id": 660271,
        "play_0_pitcher_id": 592740,
        "play_0_pitch_type": "FF",
        "play_0_release_speed": 97.3,
        "play_0_estimated_woba": 0.320,
        "play_0_launch_angle": 12.5,
        "play_0_exit_velocity": 93.4,
        "play_0_hc_x": 112.3,
        "play_0_hc_y": 78.9,
        "play_0_events": "single",
        "play_0_description": "Single on a line drive to center field.",
        "play_1_pitch_number": 2,
        "play_1_inning": 1,
        "play_1_batter_id": 660271,
        "play_1_pitcher_id": 592740,
        "play_1_pitch_type": "SL",
        "play_1_release_speed": 85.1,
        "play_1_estimated_woba": 0.180,
        "play_1_launch_angle": -5.2,
        "play_1_exit_velocity": 88.7,
        "play_1_hc_x": 105.6,
        "play_1_hc_y": 82.1,
        "play_1_events": "ground_out",
        "play_1_description": "Ground out to shortstop."
    }

def mlb_stats_server_get_statcast_single_game(
    game_pk: int,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Pulls statcast play-level data from Baseball Savant for a single game,
    identified by its MLB game ID (game_pk in statcast data).

    Args:
        game_pk (int): 6-digit integer MLB game ID to retrieve
        start_row (Optional[int]): Starting row index for truncating results (0-based, inclusive)
        end_row (Optional[int]): Ending row index for truncating results (0-based, exclusive)

    Returns:
        Dict containing:
        - plays (List[Dict]): List of individual play-level events with Statcast data
        - game_metadata (Dict): High-level information about the game
        - total_play_count (int): Total number of plays returned
        - truncation_applied (bool): Whether row truncation was applied
        - request_metadata (Dict): Information about the API request including timestamp, parameters, warnings
    """
    if not isinstance(game_pk, int) or not (100000 <= game_pk <= 999999):
        raise ValueError("game_pk must be a 6-digit integer")

    if start_row is not None and (not isinstance(start_row, int) or start_row < 0):
        raise ValueError("start_row must be a non-negative integer")

    if end_row is not None and (not isinstance(end_row, int) or (start_row is not None and end_row <= start_row)):
        raise ValueError("end_row must be a positive integer greater than start_row")

    # Call external API to get flattened data
    api_data = call_external_api("mlb-stats-server-get_statcast_single_game")

    # Construct plays list from indexed fields
    plays = [
        {
            "pitch_number": api_data["play_0_pitch_number"],
            "inning": api_data["play_0_inning"],
            "batter_id": api_data["play_0_batter_id"],
            "pitcher_id": api_data["play_0_pitcher_id"],
            "pitch_type": api_data["play_0_pitch_type"],
            "release_speed": api_data["play_0_release_speed"],
            "estimated_woba": api_data["play_0_estimated_woba"],
            "launch_angle": api_data["play_0_launch_angle"],
            "exit_velocity": api_data["play_0_exit_velocity"],
            "hc_x": api_data["play_0_hc_x"],
            "hc_y": api_data["play_0_hc_y"],
            "events": api_data["play_0_events"],
            "description": api_data["play_0_description"]
        },
        {
            "pitch_number": api_data["play_1_pitch_number"],
            "inning": api_data["play_1_inning"],
            "batter_id": api_data["play_1_batter_id"],
            "pitcher_id": api_data["play_1_pitcher_id"],
            "pitch_type": api_data["play_1_pitch_type"],
            "release_speed": api_data["play_1_release_speed"],
            "estimated_woba": api_data["play_1_estimated_woba"],
            "launch_angle": api_data["play_1_launch_angle"],
            "exit_velocity": api_data["play_1_exit_velocity"],
            "hc_x": api_data["play_1_hc_x"],
            "hc_y": api_data["play_1_hc_y"],
            "events": api_data["play_1_events"],
            "description": api_data["play_1_description"]
        }
    ]

    # Apply row slicing if specified
    if start_row is not None or end_row is not None:
        start = start_row if start_row is not None else 0
        end = end_row if end_row is not None else len(plays)
        plays = plays[start:end]
        truncation_applied = True
    else:
        truncation_applied = False

    # Construct return dictionary
    result = {
        "plays": plays,
        "game_metadata": {
            "game_pk": api_data["game_pk"],
            "game_date": api_data["game_date"],
            "venue": api_data["venue"],
            "home_team": api_data["home_team"],
            "away_team": api_data["away_team"],
            "start_time": api_data["start_time"],
            "weather_temperature": api_data["weather_temperature"],
            "weather_condition": api_data["weather_condition"]
        },
        "total_play_count": len(plays),
        "truncation_applied": truncation_applied,
        "request_metadata": {
            "request_timestamp": api_data["request_timestamp"],
            "parameters": {
                "game_pk": game_pk,
                "start_row": start_row,
                "end_row": end_row
            },
            "warning": api_data.get("warning")
        }
    }

    return result