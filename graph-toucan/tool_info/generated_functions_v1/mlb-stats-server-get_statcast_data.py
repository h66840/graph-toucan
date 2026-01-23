from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching statcast data from Baseball Savant API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - results_0_play_id (str): Unique ID for the first play
        - results_0_game_date (str): Game date for first play (YYYY-MM-DD)
        - results_0_home_team (str): Home team abbreviation for first game
        - results_0_away_team (str): Away team abbreviation for first game
        - results_0_pitch_type (str): Pitch type for first pitch (e.g., 'FF', 'SL')
        - results_0_exit_velocity (float): Exit velocity for first at-bat
        - results_0_launch_angle (int): Launch angle in degrees for first at-bat
        - results_0_batter_id (int): MLBAM ID of batter for first at-bat
        - results_0_pitcher_id (int): MLBAM ID of pitcher for first at-bat
        - results_0_events (str): Outcome of first at-bat (e.g., 'single', 'strikeout')
        - results_1_play_id (str): Unique ID for the second play
        - results_1_game_date (str): Game date for second play (YYYY-MM-DD)
        - results_1_home_team (str): Home team abbreviation for second game
        - results_1_away_team (str): Away team abbreviation for second game
        - results_1_pitch_type (str): Pitch type for second pitch
        - results_1_exit_velocity (float): Exit velocity for second at-bat
        - results_1_launch_angle (int): Launch angle in degrees for second at-bat
        - results_1_batter_id (int): MLBAM ID of batter for second at-bat
        - results_1_pitcher_id (int): MLBAM ID of pitcher for second at-bat
        - results_1_events (str): Outcome of second at-bat
        - total_count (int): Total number of statcast events returned
        - date_range_start (str): Start date of query range (YYYY-MM-DD)
        - date_range_end (str): End date of query range (YYYY-MM-DD)
        - team_filter (str): Team filter applied (e.g., 'BOS'), or empty string if none
        - metadata_source (str): Data source ('Baseball Savant')
        - metadata_query_timestamp (str): ISO timestamp of query execution
        - metadata_warnings (str): Warning message if truncated, else empty string
        - truncated (bool): Whether results were truncated via start_row/end_row
    """
    # Generate deterministic but realistic mock data
    play_id_1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    play_id_2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    
    # Default to yesterday if no dates provided
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    pitch_types = ['FF', 'SL', 'CH', 'CU', 'FC', 'SI']
    events = ['single', 'strikeout', 'home_run', 'ground_out', 'fly_out', 'walk']
    
    return {
        "results_0_play_id": play_id_1,
        "results_0_game_date": yesterday,
        "results_0_home_team": "LAD",
        "results_0_away_team": "SFG",
        "results_0_pitch_type": random.choice(pitch_types),
        "results_0_exit_velocity": round(random.uniform(85.0, 105.0), 1),
        "results_0_launch_angle": random.randint(-30, 45),
        "results_0_batter_id": random.randint(500000, 700000),
        "results_0_pitcher_id": random.randint(500000, 700000),
        "results_0_events": random.choice(events),
        
        "results_1_play_id": play_id_2,
        "results_1_game_date": yesterday,
        "results_1_home_team": "NYY",
        "results_1_away_team": "BOS",
        "results_1_pitch_type": random.choice(pitch_types),
        "results_1_exit_velocity": round(random.uniform(85.0, 105.0), 1),
        "results_1_launch_angle": random.randint(-30, 45),
        "results_1_batter_id": random.randint(500000, 700000),
        "results_1_pitcher_id": random.randint(500000, 700000),
        "results_1_events": random.choice(events),
        
        "total_count": 150,
        "date_range_start": yesterday,
        "date_range_end": yesterday,
        "team_filter": "",
        "metadata_source": "Baseball Savant",
        "metadata_query_timestamp": datetime.now().isoformat(),
        "metadata_warnings": "",
        "truncated": False
    }

def mlb_stats_server_get_statcast_data(
    start_dt: Optional[str] = None,
    end_dt: Optional[str] = None,
    team: Optional[str] = None,
    verbose: bool = True,
    parallel: bool = True,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Pulls statcast play-level data from Baseball Savant for a given date range.
    
    If no arguments are provided, returns yesterday's statcast data.
    If one date is provided, returns that date's statcast data.
    
    Args:
        start_dt (Optional[str]): Start date in YYYY-MM-DD format
        end_dt (Optional[str]): End date in YYYY-MM-DD format
        team (Optional[str]): Team abbreviation to filter by (e.g., 'BOS', 'LAD')
        verbose (bool): Whether to print progress updates
        parallel (bool): Whether to parallelize HTTP requests
        start_row (Optional[int]): Starting row index for truncation (0-based, inclusive)
        end_row (Optional[int]): Ending row index for truncation (0-based, exclusive)
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of play-level statcast records
        - total_count (int): Total number of statcast events returned
        - date_range (Dict): Object with 'start' and 'end' date strings
        - team_filter (str): Team abbreviation if filtering applied, else None
        - metadata (Dict): Additional info including source, query_timestamp, warnings
        - truncated (bool): Whether results were truncated
    
    Raises:
        ValueError: If date format is invalid or start date after end date
    """
    # Input validation
    date_format = "%Y-%m-%d"
    today = datetime.now().date()
    
    # Handle default case: no dates provided -> use yesterday
    if start_dt is None and end_dt is None:
        yesterday = (datetime.now() - timedelta(days=1)).date()
        start_dt = yesterday.strftime(date_format)
        end_dt = yesterday.strftime(date_format)
    elif start_dt is not None and end_dt is None:
        end_dt = start_dt
    elif start_dt is None and end_dt is not None:
        start_dt = end_dt
    
    try:
        start_date = datetime.strptime(start_dt, date_format).date()
        end_date = datetime.strptime(end_dt, date_format).date()
    except ValueError as e:
        raise ValueError(f"Invalid date format. Please use YYYY-MM-DD: {e}")
    
    if start_date > end_date:
        raise ValueError("start_dt cannot be after end_dt")
    
    if start_date > today or end_date > today:
        raise ValueError("Cannot query future dates")
    
    if team is not None and (not isinstance(team, str) or len(team) != 3):
        raise ValueError("Team must be a 3-letter abbreviation (e.g., 'BOS')")
    
    if start_row is not None and start_row < 0:
        raise ValueError("start_row must be non-negative")
    
    if end_row is not None and end_row <= 0:
        raise ValueError("end_row must be positive")
    
    if start_row is not None and end_row is not None and start_row >= end_row:
        raise ValueError("start_row must be less than end_row")
    
    # Call external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_statcast_data")
    
    # Update team filter if provided
    actual_team_filter = team if team is not None else ""
    api_data["team_filter"] = actual_team_filter
    
    # Update date range
    api_data["date_range_start"] = start_dt
    api_data["date_range_end"] = end_dt
    
    # Apply truncation logic
    needs_truncation = (start_row is not None or end_row is not None)
    if needs_truncation:
        api_data["truncated"] = True
        api_data["metadata_warnings"] = "Results truncated due to start_row/end_row parameters"
        
        # Simulate effect on total count
        simulated_count = api_data["total_count"]
        if start_row is not None and end_row is not None:
            simulated_count = min(end_row, api_data["total_count"]) - start_row
            if simulated_count < 0:
                simulated_count = 0
        elif start_row is not None:
            simulated_count = api_data["total_count"] - start_row
            if simulated_count < 0:
                simulated_count = 0
        elif end_row is not None:
            simulated_count = min(end_row, api_data["total_count"])
        
        api_data["total_count"] = simulated_count
    
    # Convert flat API response into structured format
    results = []
    for i in range(2):  # We have two results in mock data
        result = {
            "play_id": api_data[f"results_{i}_play_id"],
            "game_date": api_data[f"results_{i}_game_date"],
            "home_team": api_data[f"results_{i}_home_team"],
            "away_team": api_data[f"results_{i}_away_team"],
            "pitch_type": api_data[f"results_{i}_pitch_type"],
            "exit_velocity": api_data[f"results_{i}_exit_velocity"],
            "launch_angle": api_data[f"results_{i}_launch_angle"],
            "batter_id": api_data[f"results_{i}_batter_id"],
            "pitcher_id": api_data[f"results_{i}_pitcher_id"],
            "events": api_data[f"results_{i}_events"]
        }
        results.append(result)
    
    # Build final response
    response = {
        "results": results,
        "total_count": api_data["total_count"],
        "date_range": {
            "start": api_data["date_range_start"],
            "end": api_data["date_range_end"]
        },
        "team_filter": api_data["team_filter"] if api_data["team_filter"] else None,
        "metadata": {
            "source": api_data["metadata_source"],
            "query_timestamp": api_data["metadata_query_timestamp"],
            "warnings": api_data["metadata_warnings"]
        },
        "truncated": api_data["truncated"]
    }
    
    return response