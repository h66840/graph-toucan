from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external MLB Stats API for pitcher exit velocity and barrel stats.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - pitcher_0_id (int): First pitcher's MLB player ID
        - pitcher_0_name (str): First pitcher's full name
        - pitcher_0_exit_velocity (float): Average exit velocity allowed by first pitcher
        - pitcher_0_barrel_rate (float): Barrel rate (per BBE) for first pitcher
        - pitcher_0_bbe (int): Number of batted ball events against first pitcher
        - pitcher_0_qualified (bool): Whether first pitcher meets qualification criteria
        - pitcher_1_id (int): Second pitcher's MLB player ID
        - pitcher_1_name (str): Second pitcher's full name
        - pitcher_1_exit_velocity (float): Average exit velocity allowed by second pitcher
        - pitcher_1_barrel_rate (float): Barrel rate (per BBE) for second pitcher
        - pitcher_1_bbe (int): Number of batted ball events against second pitcher
        - pitcher_1_qualified (bool): Whether second pitcher meets qualification criteria
        - total_pitchers (int): Total number of pitchers returned after filtering
        - year (int): The year for which data was retrieved
        - min_bbe_applied (int): Minimum BBE threshold applied in filtering
        - pagination_start_row (int): Starting row index used in pagination
        - pagination_end_row (int): Ending row index used in pagination
        - pagination_total_possible_records (int): Total possible records in full dataset
        - metadata_timestamp (str): ISO format timestamp when data was generated
        - metadata_source (str): Data source identifier
        - metadata_query_duration_ms (int): Time taken to execute query in milliseconds
    """
    return {
        "pitcher_0_id": 660271,
        "pitcher_0_name": "Shohei Ohtani",
        "pitcher_0_exit_velocity": 88.7,
        "pitcher_0_barrel_rate": 0.052,
        "pitcher_0_bbe": 87,
        "pitcher_0_qualified": True,
        "pitcher_1_id": 543283,
        "pitcher_1_name": "Gerrit Cole",
        "pitcher_1_exit_velocity": 89.1,
        "pitcher_1_barrel_rate": 0.061,
        "pitcher_1_bbe": 94,
        "pitcher_1_qualified": True,
        "total_pitchers": 2,
        "year": 2023,
        "min_bbe_applied": 50,
        "pagination_start_row": 0,
        "pagination_end_row": 2,
        "pagination_total_possible_records": 187,
        "metadata_timestamp": "2024-03-15T10:30:45Z",
        "metadata_source": "MLB Statcast",
        "metadata_query_duration_ms": 142
    }

def mlb_stats_server_get_statcast_pitcher_exitvelo_barrels(
    year: int,
    minBBE: Optional[int] = None,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieves batted ball against data for all qualified pitchers in a given year.
    
    Args:
        year (int): The year for which you wish to retrieve batted ball against data. Format: YYYY.
        minBBE (Optional[int]): Minimum number of batted ball events to qualify. If not provided,
            default qualification thresholds are used.
        start_row (Optional[int]): Starting row index for truncating results (0-based, inclusive).
        end_row (Optional[int]): Ending row index for truncating results (0-based, exclusive).
    
    Returns:
        Dict containing:
        - pitchers (List[Dict]): List of pitcher performance records with exit velocity and barrel stats
        - total_pitchers (int): Number of pitchers returned after filtering
        - year (int): Year of the data
        - min_bbe_applied (int): Minimum BBE threshold used
        - pagination (Dict): Pagination metadata including start_row, end_row, total_possible_records
        - metadata (Dict): Additional context like data source and generation timestamp
    
    Raises:
        ValueError: If year is not a valid positive integer or if row indices are invalid
    """
    # Input validation
    if not isinstance(year, int) or year < 1900 or year > 2100:
        raise ValueError("Year must be a valid year between 1900 and 2100")
    
    if start_row is not None and (not isinstance(start_row, int) or start_row < 0):
        raise ValueError("start_row must be a non-negative integer")
    
    if end_row is not None and (not isinstance(end_row, int) or (start_row is not None and end_row <= start_row)):
        raise ValueError("end_row must be a positive integer greater than start_row")
    
    # Call external API to get flat data
    api_data = call_external_api("mlb-stats-server-get_statcast_pitcher_exitvelo_barrels")
    
    # Apply input parameters to determine actual values used
    applied_min_bbe = minBBE if minBBE is not None else api_data["min_bbe_applied"]
    
    # Determine pagination bounds
    actual_start_row = start_row if start_row is not None else api_data["pagination_start_row"]
    actual_end_row = end_row if end_row is not None else api_data["pagination_end_row"]
    
    # Construct pitchers list from indexed fields
    pitchers = []
    
    # Process first pitcher if within pagination range
    if 0 >= actual_start_row and (actual_end_row is None or 0 < actual_end_row):
        pitchers.append({
            "player_id": api_data["pitcher_0_id"],
            "name": api_data["pitcher_0_name"],
            "exit_velocity": api_data["pitcher_0_exit_velocity"],
            "barrel_rate": api_data["pitcher_0_barrel_rate"],
            "bbe": api_data["pitcher_0_bbe"],
            "qualified": api_data["pitcher_0_qualified"]
        })
    
    # Process second pitcher if within pagination range
    if 1 >= actual_start_row and (actual_end_row is None or 1 < actual_end_row):
        pitchers.append({
            "player_id": api_data["pitcher_1_id"],
            "name": api_data["pitcher_1_name"],
            "exit_velocity": api_data["pitcher_1_exit_velocity"],
            "barrel_rate": api_data["pitcher_1_barrel_rate"],
            "bbe": api_data["pitcher_1_bbe"],
            "qualified": api_data["pitcher_1_qualified"]
        })
    
    # Adjust total_pitchers based on actual results after pagination
    total_pitchers = len(pitchers)
    
    # Construct final result matching output schema
    result = {
        "pitchers": pitchers,
        "total_pitchers": total_pitchers,
        "year": api_data["year"],
        "min_bbe_applied": applied_min_bbe,
        "pagination": {
            "start_row": actual_start_row,
            "end_row": actual_end_row,
            "total_possible_records": api_data["pagination_total_possible_records"]
        },
        "metadata": {
            "timestamp": api_data["metadata_timestamp"],
            "source": api_data["metadata_source"],
            "query_duration_ms": api_data["metadata_query_duration_ms"]
        }
    }
    
    return result