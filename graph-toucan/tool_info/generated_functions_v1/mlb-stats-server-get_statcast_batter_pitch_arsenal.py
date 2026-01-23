from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB statcast batter pitch arsenal.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - pitch_arsenal_data_0_player_id (int): Player ID for first qualifying batter
        - pitch_arsenal_data_0_player_name (str): Name of first qualifying batter
        - pitch_arsenal_data_0_pitch_type (str): Pitch type for first entry
        - pitch_arsenal_data_0_batting_average (float): Batting average against this pitch
        - pitch_arsenal_data_0_slugging_percentage (float): Slugging percentage against this pitch
        - pitch_arsenal_data_0_woba (float): Weighted on-base average against this pitch
        - pitch_arsenal_data_0_plate_appearances (int): Plate appearances against this pitch
        - pitch_arsenal_data_1_player_id (int): Player ID for second qualifying batter
        - pitch_arsenal_data_1_player_name (str): Name of second qualifying batter
        - pitch_arsenal_data_1_pitch_type (str): Pitch type for second entry
        - pitch_arsenal_data_1_batting_average (float): Batting average against this pitch
        - pitch_arsenal_data_1_slugging_percentage (float): Slugging percentage against this pitch
        - pitch_arsenal_data_1_woba (float): Weighted on-base average against this pitch
        - pitch_arsenal_data_1_plate_appearances (int): Plate appearances against this pitch
        - total_players (int): Total number of batters returned after filtering
        - year (int): Year for which data was retrieved
        - query_filters_minPA (int): Minimum plate appearances threshold applied
        - query_filters_start_row (int): Starting row index used for truncation
        - query_filters_end_row (int): Ending row index used for truncation
        - pagination_start_row (int): Start row in pagination metadata
        - pagination_end_row (int): End row in pagination metadata
        - pagination_has_more (bool): Whether more data is available beyond current range
    """
    return {
        "pitch_arsenal_data_0_player_id": 12345,
        "pitch_arsenal_data_0_player_name": "John Doe",
        "pitch_arsenal_data_0_pitch_type": "Fastball",
        "pitch_arsenal_data_0_batting_average": 0.285,
        "pitch_arsenal_data_0_slugging_percentage": 0.512,
        "pitch_arsenal_data_0_woba": 0.354,
        "pitch_arsenal_data_0_plate_appearances": 120,
        "pitch_arsenal_data_1_player_id": 67890,
        "pitch_arsenal_data_1_player_name": "Jane Smith",
        "pitch_arsenal_data_1_pitch_type": "Curveball",
        "pitch_arsenal_data_1_batting_average": 0.241,
        "pitch_arsenal_data_1_slugging_percentage": 0.410,
        "pitch_arsenal_data_1_woba": 0.312,
        "pitch_arsenal_data_1_plate_appearances": 85,
        "total_players": 2,
        "year": 2023,
        "query_filters_minPA": 25,
        "query_filters_start_row": 0,
        "query_filters_end_row": 100,
        "pagination_start_row": 0,
        "pagination_end_row": 100,
        "pagination_has_more": False
    }

def mlb_stats_server_get_statcast_batter_pitch_arsenal(
    year: int,
    minPA: Optional[int] = None,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieves outcome data for batters split by the pitch type in a given year.

    Args:
        year (int): The year for which you wish to retrieve pitch arsenal data. Format: YYYY.
        minPA (int, optional): The minimum number of plate appearances for each player.
            Players below this threshold are excluded. Defaults to 25 if not specified.
        start_row (int, optional): Starting row index for truncating large results (0-based, inclusive).
        end_row (int, optional): Ending row index for truncating large results (0-based, exclusive).

    Returns:
        Dict containing:
        - pitch_arsenal_data (List[Dict]): List of dictionaries with per-pitch-type performance stats.
        - total_players (int): Number of batters returned after minPA filter.
        - year (int): The year for which data was retrieved.
        - query_filters (Dict): Applied filters including minPA, start_row, and end_row.
        - pagination (Dict): Pagination metadata including start_row, end_row, and has_more flag.

    Raises:
        ValueError: If year is not a valid positive integer or minPA is negative.
    """
    # Input validation
    if not isinstance(year, int) or year <= 0:
        raise ValueError("Year must be a positive integer.")
    if minPA is not None and (not isinstance(minPA, int) or minPA < 0):
        raise ValueError("minPA must be a non-negative integer.")
    if start_row is not None and (not isinstance(start_row, int) or start_row < 0):
        raise ValueError("start_row must be a non-negative integer.")
    if end_row is not None and (not isinstance(end_row, int) or (start_row is not None and end_row <= start_row)):
        raise ValueError("end_row must be a positive integer greater than start_row.")

    # Set default minPA
    minPA = minPA if minPA is not None else 25

    # Call external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_statcast_batter_pitch_arsenal")

    # Construct pitch_arsenal_data list from flattened API response
    pitch_arsenal_data = [
        {
            "player_id": api_data["pitch_arsenal_data_0_player_id"],
            "player_name": api_data["pitch_arsenal_data_0_player_name"],
            "pitch_type": api_data["pitch_arsenal_data_0_pitch_type"],
            "batting_average": api_data["pitch_arsenal_data_0_batting_average"],
            "slugging_percentage": api_data["pitch_arsenal_data_0_slugging_percentage"],
            "woba": api_data["pitch_arsenal_data_0_woba"],
            "plate_appearances": api_data["pitch_arsenal_data_0_plate_appearances"]
        },
        {
            "player_id": api_data["pitch_arsenal_data_1_player_id"],
            "player_name": api_data["pitch_arsenal_data_1_player_name"],
            "pitch_type": api_data["pitch_arsenal_data_1_pitch_type"],
            "batting_average": api_data["pitch_arsenal_data_1_batting_average"],
            "slugging_percentage": api_data["pitch_arsenal_data_1_slugging_percentage"],
            "woba": api_data["pitch_arsenal_data_1_woba"],
            "plate_appearances": api_data["pitch_arsenal_data_1_plate_appearances"]
        }
    ]

    # Apply start_row and end_row filtering if specified
    start_idx = start_row if start_row is not None else 0
    end_idx = end_row if end_row is not None else len(pitch_arsenal_data)
    paginated_data = pitch_arsenal_data[start_idx:end_idx]

    # Determine if more data is available
    has_more = end_idx < len(pitch_arsenal_data)

    # Construct final result
    result = {
        "pitch_arsenal_data": paginated_data,
        "total_players": api_data["total_players"],
        "year": api_data["year"],
        "query_filters": {
            "minPA": minPA,
            "start_row": start_row,
            "end_row": end_row
        },
        "pagination": {
            "start_row": start_idx,
            "end_row": end_idx,
            "has_more": has_more
        }
    }

    return result