from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB Statcast pitcher percentile ranks.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - percentile_ranks_0_player_id (int): First player's ID
        - percentile_ranks_0_player_name (str): First player's name
        - percentile_ranks_0_xera_percentile (int): xERA percentile for first player (0-100)
        - percentile_ranks_0_spin_rate_percentile (int): Spin rate percentile for first player (0-100)
        - percentile_ranks_0_era_percentile (int): ERA percentile for first player (0-100)
        - percentile_ranks_1_player_id (int): Second player's ID
        - percentile_ranks_1_player_name (str): Second player's name
        - percentile_ranks_1_xera_percentile (int): xERA percentile for second player (0-100)
        - percentile_ranks_1_spin_rate_percentile (int): Spin rate percentile for second player (0-100)
        - percentile_ranks_1_era_percentile (int): ERA percentile for second player (0-100)
        - total_players (int): Total number of players meeting thresholds in the given year
        - year (int): The year for which data was retrieved
        - metadata_min_ip_per_game (float): Minimum innings pitched per team game required (e.g., 1.25)
        - metadata_includes_expected_stats (bool): Whether expected stats like xERA are included
        - metadata_coverage_start_date (str): Start date of data coverage in YYYY-MM-DD format
        - metadata_coverage_end_date (str): End date of data coverage in YYYY-MM-DD format
    """
    return {
        "percentile_ranks_0_player_id": 10123,
        "percentile_ranks_0_player_name": "Jacob deGrom",
        "percentile_ranks_0_xera_percentile": 98,
        "percentile_ranks_0_spin_rate_percentile": 95,
        "percentile_ranks_0_era_percentile": 97,
        "percentile_ranks_1_player_id": 10456,
        "percentile_ranks_1_player_name": "Shane Bieber",
        "percentile_ranks_1_xera_percentile": 92,
        "percentile_ranks_1_spin_rate_percentile": 88,
        "percentile_ranks_1_era_percentile": 90,
        "total_players": 147,
        "year": 2022,
        "metadata_min_ip_per_game": 1.25,
        "metadata_includes_expected_stats": True,
        "metadata_coverage_start_date": "2022-04-07",
        "metadata_coverage_end_date": "2022-10-05"
    }

def mlb_stats_server_get_statcast_pitcher_percentile_ranks(
    year: int,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieves percentile ranks for each player in a given year, including pitchers with at least 1.25 IP per team game.
    Includes percentiles on expected stats (e.g., xERA), batted ball data, and spin rates.

    Args:
        year (int): The year for which to retrieve percentile data (format: YYYY).
        start_row (Optional[int]): Starting row index for truncating results (0-based, inclusive). Defaults to None.
        end_row (Optional[int]): Ending row index for truncating results (0-based, exclusive). Defaults to None.

    Returns:
        Dict containing:
            - percentile_ranks (List[Dict]): List of player percentile rank data with metrics such as expected
              statistics, batted ball characteristics, and spin rates.
            - total_players (int): Total number of players included in the dataset who met the minimum threshold.
            - year (int): The year for which percentile ranks were calculated.
            - metadata (Dict): Additional contextual information including data coverage, thresholds applied,
              and definitions of percentile categories.

    Raises:
        ValueError: If year is not a valid 4-digit year between 2008 and current year.
    """
    # Input validation
    if not isinstance(year, int) or year < 2008 or year > 2024:
        raise ValueError("Year must be an integer between 2008 and 2024.")

    if start_row is not None and end_row is not None and start_row >= end_row:
        raise ValueError("start_row must be less than end_row.")

    # Fetch data from simulated external API
    raw_data = call_external_api("mlb-stats-server-get_statcast_pitcher_percentile_ranks")

    # Construct percentile_ranks list from flattened API response
    percentile_ranks = [
        {
            "player_id": raw_data["percentile_ranks_0_player_id"],
            "player_name": raw_data["percentile_ranks_0_player_name"],
            "xera_percentile": raw_data["percentile_ranks_0_xera_percentile"],
            "spin_rate_percentile": raw_data["percentile_ranks_0_spin_rate_percentile"],
            "era_percentile": raw_data["percentile_ranks_0_era_percentile"]
        },
        {
            "player_id": raw_data["percentile_ranks_1_player_id"],
            "player_name": raw_data["percentile_ranks_1_player_name"],
            "xera_percentile": raw_data["percentile_ranks_1_xera_percentile"],
            "spin_rate_percentile": raw_data["percentile_ranks_1_spin_rate_percentile"],
            "era_percentile": raw_data["percentile_ranks_1_era_percentile"]
        }
    ]

    # Apply row slicing if specified
    if start_row is not None or end_row is not None:
        start = start_row if start_row is not None else 0
        end = end_row if end_row is not None else len(percentile_ranks)
        percentile_ranks = percentile_ranks[start:end]

    # Construct metadata dictionary
    metadata = {
        "min_ip_per_game": raw_data["metadata_min_ip_per_game"],
        "includes_expected_stats": raw_data["metadata_includes_expected_stats"],
        "coverage_start_date": raw_data["metadata_coverage_start_date"],
        "coverage_end_date": raw_data["metadata_coverage_end_date"],
        "description": "Percentile rankings based on Statcast metrics for pitchers meeting minimum playing time thresholds."
    }

    # Final result construction
    result = {
        "percentile_ranks": percentile_ranks,
        "total_players": raw_data["total_players"],
        "year": raw_data["year"],
        "metadata": metadata
    }

    return result