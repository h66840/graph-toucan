from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching statcast pitch-level data for a batter from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - pitch_data_0_pitch_type (str): Type of the first pitch (e.g., 'FF', 'SL')
        - pitch_data_0_velocity (float): Velocity in mph of the first pitch
        - pitch_data_0_launch_angle (float): Launch angle in degrees for the first pitch
        - pitch_data_0_exit_velocity (float): Exit velocity in mph for the first pitch
        - pitch_data_0_outcome (str): Outcome of the first pitch (e.g., 'strike', 'single')
        - pitch_data_0_inning (int): Inning number for the first pitch
        - pitch_data_0_balls (int): Ball count before the first pitch
        - pitch_data_0_strikes (int): Strike count before the first pitch
        - pitch_data_0_game_date (str): Game date for the first pitch (YYYY-MM-DD)
        - pitch_data_1_pitch_type (str): Type of the second pitch
        - pitch_data_1_velocity (float): Velocity in mph of the second pitch
        - pitch_data_1_launch_angle (float): Launch angle in degrees for the second pitch
        - pitch_data_1_exit_velocity (float): Exit velocity in mph for the second pitch
        - pitch_data_1_outcome (str): Outcome of the second pitch
        - pitch_data_1_inning (int): Inning number for the second pitch
        - pitch_data_1_balls (int): Ball count before the second pitch
        - pitch_data_1_strikes (int): Strike count before the second pitch
        - pitch_data_1_game_date (str): Game date for the second pitch (YYYY-MM-DD)
        - total_pitches (int): Total number of pitch records returned
        - player_id (int): MLBAM player ID of the batter
        - query_metadata_start_dt (str): Effective start date used in query (YYYY-MM-DD)
        - query_metadata_end_dt (str): Effective end date used in query (YYYY-MM-DD)
        - query_metadata_start_row (int): Starting row index used (0-based, inclusive)
        - query_metadata_end_row (int): Ending row index used (0-based, exclusive)
        - query_metadata_truncated (bool): Whether the result was truncated due to size
        - has_more_data (bool): Indicates if more data is available beyond current window
    """
    return {
        "pitch_data_0_pitch_type": "FF",
        "pitch_data_0_velocity": 95.3,
        "pitch_data_0_launch_angle": 12.4,
        "pitch_data_0_exit_velocity": 103.2,
        "pitch_data_0_outcome": "single",
        "pitch_data_0_inning": 3,
        "pitch_data_0_balls": 2,
        "pitch_data_0_strikes": 1,
        "pitch_data_0_game_date": "2023-07-15",
        "pitch_data_1_pitch_type": "SL",
        "pitch_data_1_velocity": 86.7,
        "pitch_data_1_launch_angle": -15.1,
        "pitch_data_1_exit_velocity": 0.0,
        "pitch_data_1_outcome": "strike",
        "pitch_data_1_inning": 4,
        "pitch_data_1_balls": 0,
        "pitch_data_1_strikes": 1,
        "pitch_data_1_game_date": "2023-07-15",
        "total_pitches": 2,
        "player_id": 660271,
        "query_metadata_start_dt": "2023-07-01",
        "query_metadata_end_dt": "2023-07-31",
        "query_metadata_start_row": 0,
        "query_metadata_end_row": 2,
        "query_metadata_truncated": False,
        "has_more_data": False,
    }

def mlb_stats_server_get_statcast_batter_data(
    player_id: int,
    start_dt: Optional[str] = None,
    end_dt: Optional[str] = None,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Pulls statcast pitch-level data from Baseball Savant for a given batter.
    
    Args:
        start_dt (Optional[str]): The first date for which you want a player's statcast data (YYYY-MM-DD).
        end_dt (Optional[str]): The final date for which you want data (YYYY-MM-DD).
        player_id (int): The player's MLBAM ID. Find this via the get_playerid_lookup tool.
        start_row (Optional[int]): Starting row index for truncating large results (0-based, inclusive).
        end_row (Optional[int]): Ending row index for truncating large results (0-based, exclusive).
    
    Returns:
        Dict containing:
        - pitch_data (List[Dict]): List of pitch-level events for the batter with detailed metrics.
        - total_pitches (int): Total number of pitch records returned after filtering.
        - player_id (int): MLBAM player ID of the batter.
        - query_metadata (Dict): Metadata about the query parameters used.
        - has_more_data (bool): Indicates if more data is available beyond current response window.
    """
    # Validate required input
    if player_id is None:
        raise ValueError("player_id is required and cannot be None")
    
    # Call external API to get flattened data
    api_data = call_external_api("mlb-stats-server-get_statcast_batter_data")
    
    # Construct pitch_data list from indexed fields
    pitch_data = [
        {
            "pitch_type": api_data["pitch_data_0_pitch_type"],
            "velocity": api_data["pitch_data_0_velocity"],
            "launch_angle": api_data["pitch_data_0_launch_angle"],
            "exit_velocity": api_data["pitch_data_0_exit_velocity"],
            "outcome": api_data["pitch_data_0_outcome"],
            "inning": api_data["pitch_data_0_inning"],
            "balls": api_data["pitch_data_0_balls"],
            "strikes": api_data["pitch_data_0_strikes"],
            "game_date": api_data["pitch_data_0_game_date"]
        },
        {
            "pitch_type": api_data["pitch_data_1_pitch_type"],
            "velocity": api_data["pitch_data_1_velocity"],
            "launch_angle": api_data["pitch_data_1_launch_angle"],
            "exit_velocity": api_data["pitch_data_1_exit_velocity"],
            "outcome": api_data["pitch_data_1_outcome"],
            "inning": api_data["pitch_data_1_inning"],
            "balls": api_data["pitch_data_1_balls"],
            "strikes": api_data["pitch_data_1_strikes"],
            "game_date": api_data["pitch_data_1_game_date"]
        }
    ]
    
    # Construct query metadata
    query_metadata = {
        "start_dt": api_data["query_metadata_start_dt"],
        "end_dt": api_data["query_metadata_end_dt"],
        "start_row": api_data["query_metadata_start_row"],
        "end_row": api_data["query_metadata_end_row"],
        "truncated": api_data["query_metadata_truncated"]
    }
    
    # Build final result structure
    result = {
        "pitch_data": pitch_data,
        "total_pitches": api_data["total_pitches"],
        "player_id": api_data["player_id"],
        "query_metadata": query_metadata,
        "has_more_data": api_data["has_more_data"]
    }
    
    return result