from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB Statcast batter percentile ranks.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - percentile_ranks_0_player_id (int): Player ID of the first batter
        - percentile_ranks_0_name (str): Name of the first batter
        - percentile_ranks_0_exit_velocity (float): Exit velocity percentile for first batter
        - percentile_ranks_0_launch_angle (float): Launch angle percentile for first batter
        - percentile_ranks_0_barrel_rate (float): Barrel rate percentile for first batter
        - percentile_ranks_1_player_id (int): Player ID of the second batter
        - percentile_ranks_1_name (str): Name of the second batter
        - percentile_ranks_1_exit_velocity (float): Exit velocity percentile for second batter
        - percentile_ranks_1_launch_angle (float): Launch angle percentile for second batter
        - percentile_ranks_1_barrel_rate (float): Barrel rate percentile for second batter
        - total_count (int): Total number of batters in the percentile ranking
        - year (int): The year for which percentile ranks were calculated
        - metadata_min_pa (int): Minimum plate appearances required for inclusion
        - metadata_data_cutoff (str): Data cutoff date in ISO format
        - metadata_source (str): Source system name (e.g., 'Statcast')
        - metadata_version (str): Data version identifier
        - metadata_processed_timestamp (str): Processing timestamp in ISO format
    """
    return {
        "percentile_ranks_0_player_id": 665489,
        "percentile_ranks_0_name": "Shohei Ohtani",
        "percentile_ranks_0_exit_velocity": 98.7,
        "percentile_ranks_0_launch_angle": 85.2,
        "percentile_ranks_0_barrel_rate": 96.3,
        "percentile_ranks_1_player_id": 642164,
        "percentile_ranks_1_name": "Aaron Judge",
        "percentile_ranks_1_exit_velocity": 97.1,
        "percentile_ranks_1_launch_angle": 78.9,
        "percentile_ranks_1_barrel_rate": 94.5,
        "total_count": 342,
        "year": 2023,
        "metadata_min_pa": 250,
        "metadata_data_cutoff": "2023-10-01",
        "metadata_source": "Statcast",
        "metadata_version": "v2.1",
        "metadata_processed_timestamp": datetime.utcnow().isoformat() + "Z"
    }


def mlb_stats_server_get_statcast_batter_percentile_ranks(
    year: int,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieves percentile ranks for batters in a given year.

    This function simulates retrieving Statcast batter percentile rank data for a specified year.
    It supports optional row-based truncation to simulate handling of large datasets.

    Args:
        year (int): The year for which you wish to retrieve percentile data. Format: YYYY.
        start_row (Optional[int]): Starting row index for truncating results (0-based, inclusive).
        end_row (Optional[int]): Ending row index for truncating results (0-based, exclusive).

    Returns:
        Dict containing:
        - percentile_ranks (List[Dict]): List of batter percentile rank entries with player identifiers
          and percentile values across various Statcast metrics.
        - total_count (int): Total number of batters included in the percentile ranking data.
        - year (int): The year for which percentile ranks were calculated.
        - metadata (Dict): Additional contextual information including minimum plate appearance threshold,
          data cutoff date, source system, version, and processing timestamp.

    Raises:
        ValueError: If year is not a positive integer or if row indices are invalid.
    """
    # Input validation
    if not isinstance(year, int) or year <= 0:
        raise ValueError("Year must be a positive integer.")
    
    if start_row is not None and (not isinstance(start_row, int) or start_row < 0):
        raise ValueError("start_row must be a non-negative integer.")
    
    if end_row is not None and (not isinstance(end_row, int) or end_row < 0):
        raise ValueError("end_row must be a non-negative integer.")
    
    if start_row is not None and end_row is not None and start_row >= end_row:
        raise ValueError("start_row must be less than end_row.")

    # Fetch data from external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_statcast_batter_percentile_ranks")

    # Construct percentile ranks list from flattened API response
    raw_ranks = [
        {
            "player_id": api_data["percentile_ranks_0_player_id"],
            "name": api_data["percentile_ranks_0_name"],
            "metric_percentiles": {
                "exit_velocity": api_data["percentile_ranks_0_exit_velocity"],
                "launch_angle": api_data["percentile_ranks_0_launch_angle"],
                "barrel_rate": api_data["percentile_ranks_0_barrel_rate"]
            }
        },
        {
            "player_id": api_data["percentile_ranks_1_player_id"],
            "name": api_data["percentile_ranks_1_name"],
            "metric_percentiles": {
                "exit_velocity": api_data["percentile_ranks_1_exit_velocity"],
                "launch_angle": api_data["percentile_ranks_1_launch_angle"],
                "barrel_rate": api_data["percentile_ranks_1_barrel_rate"]
            }
        }
    ]

    # Apply row slicing if specified
    start = start_row if start_row is not None else 0
    end = end_row if end_row is not None else len(raw_ranks)
    truncated_ranks = raw_ranks[start:end]

    # Construct metadata
    metadata = {
        "min_pa_threshold": api_data["metadata_min_pa"],
        "data_cutoff_date": api_data["metadata_data_cutoff"],
        "source": api_data["metadata_source"],
        "version": api_data["metadata_version"],
        "processed_timestamp": api_data["metadata_processed_timestamp"]
    }

    # Construct final result
    result = {
        "percentile_ranks": truncated_ranks,
        "total_count": api_data["total_count"],
        "year": api_data["year"],
        "metadata": metadata
    }

    return result