from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB pitcher pitch arsenal stats.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - pitcher_arsenal_stats_0_player_name (str): First pitcher's name
        - pitcher_arsenal_stats_0_player_id (int): First pitcher's ID
        - pitcher_arsenal_stats_0_pitch_type (str): Pitch type for first pitcher
        - pitcher_arsenal_stats_0_average_speed (float): Average speed of pitch for first pitcher
        - pitcher_arsenal_stats_0_n_ (float): Percentage share of pitch type for first pitcher
        - pitcher_arsenal_stats_0_average_spin (float): Average spin rate for first pitcher
        - pitcher_arsenal_stats_1_player_name (str): Second pitcher's name
        - pitcher_arsenal_stats_1_player_id (int): Second pitcher's ID
        - pitcher_arsenal_stats_1_pitch_type (str): Pitch type for second pitcher
        - pitcher_arsenal_stats_1_average_speed (float): Average speed of pitch for second pitcher
        - pitcher_arsenal_stats_1_n_ (float): Percentage share of pitch type for second pitcher
        - pitcher_arsenal_stats_1_average_spin (float): Average spin rate for second pitcher
        - total_pitchers_returned (int): Number of pitchers returned after filtering
        - query_metadata_year (int): Year used in query
        - query_metadata_minP (int): Minimum pitch threshold applied
        - query_metadata_arsenal_type (str): Type of arsenal stat returned
        - query_metadata_start_row (int): Starting row index used
        - query_metadata_end_row (int): Ending row index used
        - has_more_data (bool): Whether more data exists beyond current window
    """
    return {
        "pitcher_arsenal_stats_0_player_name": "Max Scherzer",
        "pitcher_arsenal_stats_0_player_id": 453286,
        "pitcher_arsenal_stats_0_pitch_type": "FF",
        "pitcher_arsenal_stats_0_average_speed": 95.2,
        "pitcher_arsenal_stats_0_n_": 0.65,
        "pitcher_arsenal_stats_0_average_spin": 2350.1,
        "pitcher_arsenal_stats_1_player_name": "Jacob deGrom",
        "pitcher_arsenal_stats_1_player_id": 594795,
        "pitcher_arsenal_stats_1_pitch_type": "FF",
        "pitcher_arsenal_stats_1_average_speed": 99.1,
        "pitcher_arsenal_stats_1_n_": 0.58,
        "pitcher_arsenal_stats_1_average_spin": 2580.3,
        "total_pitchers_returned": 2,
        "query_metadata_year": 2022,
        "query_metadata_minP": 1000,
        "query_metadata_arsenal_type": "average_speed",
        "query_metadata_start_row": 0,
        "query_metadata_end_row": 2,
        "has_more_data": True
    }

def mlb_stats_server_get_statcast_pitcher_pitch_arsenal(
    year: int,
    minP: Optional[int] = None,
    arsenal_type: Optional[str] = None,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieves high level stats on each pitcher's arsenal in a given year.
    
    Args:
        year (int): The year for which you wish to retrieve expected stats data. Format: YYYY.
        minP (int, optional): The minimum number of pitches thrown. If a player falls below 
                             this threshold, they will be excluded from the results. 
                             If not specified, only qualified pitchers are returned.
        arsenal_type (str, optional): The type of stat to retrieve for the pitchers' arsenals.
                                     Options: ["average_speed", "n_", "average_spin"]. 
                                     Defaults to "average_speed".
        start_row (int, optional): Starting row index for truncating large results (0-based, inclusive).
        end_row (int, optional): Ending row index for truncating large results (0-based, exclusive).
    
    Returns:
        Dict containing:
        - pitcher_arsenal_stats (List[Dict]): List of dictionaries with per-pitcher pitch arsenal stats
        - total_pitchers_returned (int): Number of pitchers included after filters
        - query_metadata (Dict): Metadata about the query parameters used
        - has_more_data (bool): Whether additional pitchers exist beyond current window
    
    Raises:
        ValueError: If year is not a valid 4-digit year or if row indices are invalid
    """
    # Input validation
    if not isinstance(year, int) or year < 1900 or year > 2100:
        raise ValueError("Year must be a valid 4-digit year between 1900 and 2100")
    
    if start_row is not None and (not isinstance(start_row, int) or start_row < 0):
        raise ValueError("start_row must be a non-negative integer")
    
    if end_row is not None and (not isinstance(end_row, int) or (start_row is not None and end_row <= start_row)):
        raise ValueError("end_row must be a positive integer greater than start_row")
    
    # Set defaults
    if arsenal_type not in ["average_speed", "n_", "average_spin"]:
        arsenal_type = "average_speed"
    
    if minP is None:
        minP = 1000  # Default minimum pitch threshold for qualified pitchers
    
    if start_row is None:
        start_row = 0
    
    if end_row is None:
        end_row = start_row + 100  # Default page size
    
    # Call external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_statcast_pitcher_pitch_arsenal")
    
    # Extract and construct pitcher arsenal stats list
    pitcher_arsenal_stats = []
    
    for i in range(2):  # We have two items from the API response
        player_name_key = f"pitcher_arsenal_stats_{i}_player_name"
        player_id_key = f"pitcher_arsenal_stats_{i}_player_id"
        pitch_type_key = f"pitcher_arsenal_stats_{i}_pitch_type"
        
        if player_name_key not in api_data:
            continue
            
        pitcher_data = {
            "player_name": api_data[player_name_key],
            "player_id": api_data[player_id_key],
            "pitch_type": api_data[pitch_type_key]
        }
        
        # Add the selected arsenal metric
        metric_key = f"pitcher_arsenal_stats_{i}_{arsenal_type}"
        if metric_key in api_data:
            pitcher_data[arsenal_type] = api_data[metric_key]
        else:
            # Default to average_speed if requested metric not available
            default_key = f"pitcher_arsenal_stats_{i}_average_speed"
            pitcher_data[arsenal_type] = api_data.get(default_key, 90.0)
            
        pitcher_arsenal_stats.append(pitcher_data)
    
    # Apply row filtering
    filtered_stats = []
    for i, stat in enumerate(pitcher_arsenal_stats):
        if start_row <= i < end_row:
            # Apply minP filtering logic (simulated - in real case this would be server-side)
            # Here we assume all returned pitchers meet minP threshold
            filtered_stats.append(stat)
    
    # Construct final result
    result = {
        "pitcher_arsenal_stats": filtered_stats,
        "total_pitchers_returned": len(filtered_stats),
        "query_metadata": {
            "year": year,
            "minP": minP,
            "arsenal_type": arsenal_type,
            "start_row": start_row,
            "end_row": end_row
        },
        "has_more_data": api_data["has_more_data"]
    }
    
    return result