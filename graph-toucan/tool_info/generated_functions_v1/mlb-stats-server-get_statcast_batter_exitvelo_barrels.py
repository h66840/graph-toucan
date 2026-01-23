from typing import Dict, List, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching batted ball statistics data from an external MLB Stats API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool), representing
        flattened version of the actual nested response structure.

    Flattened fields:
        - result_0_player_id (int): Player ID for first batter
        - result_0_name (str): Name of first batter
        - result_0_team (str): Team of first batter
        - result_0_position (str): Position of first batter
        - result_0_bbes (int): Number of batted ball events for first batter
        - result_0_avg_exit_velocity (float): Average exit velocity for first batter
        - result_0_barrel_rate (float): Barrel rate for first batter
        - result_0_ev95_plus_pct (float): Percentage of hits at 95+ mph for first batter
        - result_0_hard_hit_rate (float): Hard hit rate for first batter
        - result_0_launch_angle_avg (float): Average launch angle for first batter
        - result_0_max_exit_velocity (float): Maximum exit velocity for first batter

        - result_1_player_id (int): Player ID for second batter
        - result_1_name (str): Name of second batter
        - result_1_team (str): Team of second batter
        - result_1_position (str): Position of second batter
        - result_1_bbes (int): Number of batted ball events for second batter
        - result_1_avg_exit_velocity (float): Average exit velocity for second batter
        - result_1_barrel_rate (float): Barrel rate for second batter
        - result_1_ev95_plus_pct (float): Percentage of hits at 95+ mph for second batter
        - result_1_hard_hit_rate (float): Hard hit rate for second batter
        - result_1_launch_angle_avg (float): Average launch angle for second batter
        - result_1_max_exit_velocity (float): Maximum exit velocity for second batter

        - total_players (int): Total number of players returned
        - year (int): The year for which data was retrieved
        - min_bbe_applied (int): Minimum BBE threshold applied
        - metadata_timestamp (str): ISO format timestamp of data generation
        - metadata_source (str): Data source name
        - metadata_disclaimer (str): Disclaimer text about qualification criteria
    """
    return {
        "result_0_player_id": 12345,
        "result_0_name": "Mike Trout",
        "result_0_team": "LAA",
        "result_0_position": "CF",
        "result_0_bbes": 450,
        "result_0_avg_exit_velocity": 92.3,
        "result_0_barrel_rate": 0.125,
        "result_0_ev95_plus_pct": 0.52,
        "result_0_hard_hit_rate": 0.48,
        "result_0_launch_angle_avg": 10.2,
        "result_0_max_exit_velocity": 118.4,

        "result_1_player_id": 67890,
        "result_1_name": "Aaron Judge",
        "result_1_team": "NYY",
        "result_1_position": "RF",
        "result_1_bbes": 430,
        "result_1_avg_exit_velocity": 94.1,
        "result_1_barrel_rate": 0.142,
        "result_1_ev95_plus_pct": 0.58,
        "result_1_hard_hit_rate": 0.51,
        "result_1_launch_angle_avg": 12.5,
        "result_1_max_exit_velocity": 121.7,

        "total_players": 2,
        "year": 2023,
        "min_bbe_applied": 100,
        "metadata_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata_source": "Statcast",
        "metadata_disclaimer": "Qualified batters only; minimum 100 BBE applied."
    }


def mlb_stats_server_get_statcast_batter_exitvelo_barrels(
    year: int,
    minBBE: Optional[int] = None,
    start_row: Optional[int] = None,
    end_row: Optional[int] = None
) -> Dict[str, Any]:
    """
    Retrieves batted ball data for all batters in a given year.

    Args:
        year (int): The year for which you wish to retrieve batted ball data. Format: YYYY.
        minBBE (Optional[int]): Minimum number of batted ball events for each player.
            Players below this threshold are excluded. If not specified, a system default is used.
        start_row (Optional[int]): Starting row index for truncating large results (0-based, inclusive).
        end_row (Optional[int]): Ending row index for truncating large results (0-based, exclusive).

    Returns:
        Dict containing:
            - results (List[Dict]): List of batted ball event statistics per qualified batter.
            - total_players (int): Number of players returned after filtering.
            - year (int): Year of the data.
            - min_bbe_applied (int): Minimum BBE threshold used.
            - metadata (Dict): Contextual info including timestamp, source, and disclaimers.

    Raises:
        ValueError: If year is not a valid positive integer.
    """
    if not isinstance(year, int) or year < 1900 or year > datetime.datetime.now().year + 1:
        raise ValueError("Year must be a valid year between 1900 and next year.")

    if start_row is not None and start_row < 0:
        start_row = 0
    if end_row is not None and end_row < (start_row or 0):
        end_row = start_row

    # Call external API to get flattened data
    raw_data = call_external_api("mlb-stats-server-get_statcast_batter_exitvelo_barrels")

    # Construct results list from indexed fields
    results = []
    for i in range(2):  # We generated 2 items
        prefix = f"result_{i}"
        try:
            player_data = {
                "player_id": raw_data[f"{prefix}_player_id"],
                "name": raw_data[f"{prefix}_name"],
                "team": raw_data[f"{prefix}_team"],
                "position": raw_data[f"{prefix}_position"],
                "bbes": raw_data[f"{prefix}_bbes"],
                "avg_exit_velocity": raw_data[f"{prefix}_avg_exit_velocity"],
                "barrel_rate": raw_data[f"{prefix}_barrel_rate"],
                "ev95_plus_pct": raw_data[f"{prefix}_ev95_plus_pct"],
                "hard_hit_rate": raw_data[f"{prefix}_hard_hit_rate"],
                "launch_angle_avg": raw_data[f"{prefix}_launch_angle_avg"],
                "max_exit_velocity": raw_data[f"{prefix}_max_exit_velocity"]
            }
            results.append(player_data)
        except KeyError:
            break  # No more indexed results

    # Apply row slicing if specified
    if start_row is not None or end_row is not None:
        results = results[start_row:end_row]

    # Reconstruct final output structure
    output = {
        "results": results,
        "total_players": len(results),
        "year": raw_data["year"],
        "min_bbe_applied": raw_data["min_bbe_applied"],
        "metadata": {
            "timestamp": raw_data["metadata_timestamp"],
            "source": raw_data["metadata_source"],
            "disclaimer": raw_data["metadata_disclaimer"]
        }
    }

    return output