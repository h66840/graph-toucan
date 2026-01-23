from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB Statcast pitcher data.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - pitch_data_0_pitch_type (str): Type of the first pitch (e.g., 'FF', 'SL')
        - pitch_data_0_velocity (float): Velocity in mph for the first pitch
        - pitch_data_0_spin_rate (int): Spin rate in rpm for the first pitch
        - pitch_data_0_launch_angle (float): Launch angle in degrees for the first pitch
        - pitch_data_0_exit_velocity (float): Exit velocity in mph for the first pitch
        - pitch_data_0_result (str): Outcome of the first pitch (e.g., 'strike', 'ball')
        - pitch_data_1_pitch_type (str): Type of the second pitch
        - pitch_data_1_velocity (float): Velocity in mph for the second pitch
        - pitch_data_1_spin_rate (int): Spin rate in rpm for the second pitch
        - pitch_data_1_launch_angle (float): Launch angle in degrees for the second pitch
        - pitch_data_1_exit_velocity (float): Exit velocity in mph for the second pitch
        - pitch_data_1_result (str): Outcome of the second pitch
        - total_pitches (int): Total number of pitches returned after filtering
        - player_info_name_first (str): First name of the pitcher
        - player_info_name_last (str): Last name of the pitcher
        - player_info_hand (str): Pitching hand ('L' or 'R')
        - player_info_team (str): Current team of the player at time of query
        - player_info_player_id (int): MLBAM ID of the player
        - query_metadata_start_dt (str): Effective start date in YYYY-MM-DD
        - query_metadata_end_dt (str): Effective end date in YYYY-MM-DD
        - query_metadata_start_row (int): Start row index used in query
        - query_metadata_end_row (int): End row index used in query
        - query_metadata_timestamp (str): ISO format timestamp of the request
        - has_more_data (bool): Whether more data exists beyond current window
    """
    return {
        "pitch_data_0_pitch_type": "FF",
        "pitch_data_0_velocity": 95.3,
        "pitch_data_0_spin_rate": 2350,
        "pitch_data_0_launch_angle": 12.4,
        "pitch_data_0_exit_velocity": 102.1,
        "pitch_data_0_result": "strike",
        "pitch_data_1_pitch_type": "SL",
        "pitch_data_1_velocity": 87.6,
        "pitch_data_1_spin_rate": 2600,
        "pitch_data_1_launch_angle": -5.2,
        "pitch_data_1_exit_velocity": 88.3,
        "pitch_data_1_result": "ball",
        "total_pitches": 2,
        "player_info_name_first": "Max",
        "player_info_name_last": "Scherzer",
        "player_info_hand": "R",
        "player_info_team": "NYM",
        "player_info_player_id": 453286,
        "query_metadata_start_dt": "2023-04-01",
        "query_metadata_end_dt": "2023-04-30",
        "query_metadata_start_row": 0,
        "query_metadata_end_row": 100,
        "query_metadata_timestamp": "2023-10-05T14:30:00Z",
        "has_more_data": False
    }

def mlb_stats_server_get_statcast_pitcher_data(
    player_id: int,
    start_dt: Optional[str] = None,
    end_dt: Optional[str] = None,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Pulls statcast pitch-level data from Baseball Savant for a given pitcher.

    Args:
        start_dt (Optional[str]): The first date for which you want a player's statcast data (YYYY-MM-DD).
        end_dt (Optional[str]): The final date for which you want data (YYYY-MM-DD).
        player_id (int): The player's MLBAM ID. Find this by calling the get_playerid_lookup tool,
                         finding the correct player, and selecting their key_mlbam.
        start_row (Optional[int]): Starting row index for truncating large results (0-based, inclusive).
        end_row (Optional[int]): Ending row index for truncating large results (0-based, exclusive).

    Returns:
        Dict containing:
        - pitch_data (List[Dict]): List of pitch-level records with detailed Statcast metrics.
        - total_pitches (int): Total number of pitches returned after filtering.
        - player_info (Dict): Information about the queried pitcher.
        - query_metadata (Dict): Metadata about the query parameters used.
        - has_more_data (bool): Indicates if additional data exists beyond current window.

    Note:
        This function simulates an API call and returns realistic dummy data structured according to the schema.
        In a real implementation, this would make an actual HTTP request to the Statcast server.
    """
    # Validate required input
    if not isinstance(player_id, int) or player_id <= 0:
        raise ValueError("player_id must be a positive integer")

    # Call external API (simulated)
    raw_data = call_external_api("mlb-stats-server-get_statcast_pitcher_data")

    # Construct pitch_data list from indexed fields
    pitch_data = [
        {
            "pitch_type": raw_data["pitch_data_0_pitch_type"],
            "velocity": raw_data["pitch_data_0_velocity"],
            "spin_rate": raw_data["pitch_data_0_spin_rate"],
            "launch_angle": raw_data["pitch_data_0_launch_angle"],
            "exit_velocity": raw_data["pitch_data_0_exit_velocity"],
            "result": raw_data["pitch_data_0_result"]
        },
        {
            "pitch_type": raw_data["pitch_data_1_pitch_type"],
            "velocity": raw_data["pitch_data_1_velocity"],
            "spin_rate": raw_data["pitch_data_1_spin_rate"],
            "launch_angle": raw_data["pitch_data_1_launch_angle"],
            "exit_velocity": raw_data["pitch_data_1_exit_velocity"],
            "result": raw_data["pitch_data_1_result"]
        }
    ]

    # Construct player_info
    player_info = {
        "name": f"{raw_data['player_info_name_first']} {raw_data['player_info_name_last']}",
        "first_name": raw_data["player_info_name_first"],
        "last_name": raw_data["player_info_name_last"],
        "handedness": raw_data["player_info_hand"],
        "team": raw_data["player_info_team"],
        "player_id": raw_data["player_info_player_id"]
    }

    # Construct query_metadata
    query_metadata = {
        "start_dt": start_dt or raw_data["query_metadata_start_dt"],
        "end_dt": end_dt or raw_data["query_metadata_end_dt"],
        "start_row": start_row if start_row is not None else raw_data["query_metadata_start_row"],
        "end_row": end_row if end_row is not None else raw_data["query_metadata_end_row"],
        "timestamp": raw_data["query_metadata_timestamp"]
    }

    # Final result structure
    result = {
        "pitch_data": pitch_data,
        "total_pitches": raw_data["total_pitches"],
        "player_info": player_info,
        "query_metadata": query_metadata,
        "has_more_data": raw_data["has_more_data"]
    }

    return result