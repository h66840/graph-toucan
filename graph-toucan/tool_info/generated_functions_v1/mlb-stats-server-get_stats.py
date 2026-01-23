from typing import Dict, List, Any, Optional
import json
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external MLB stats server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - stats_data_0_player_name (str): Name of the first player in stats
        - stats_data_0_team_name (str): Team name of the first player
        - stats_data_0_batting_avg (str): Batting average of the first player
        - stats_data_0_home_runs (int): Home runs for the first player
        - stats_data_0_season (int): Season year for the first player's stats
        - stats_data_1_player_name (str): Name of the second player in stats
        - stats_data_1_team_name (str): Team name of the second player
        - stats_data_1_batting_avg (str): Batting average of the second player
        - stats_data_1_home_runs (int): Home runs for the second player
        - stats_data_1_season (int): Season year for the second player's stats
        - total_count (int): Total number of statistic records returned
        - metadata_query_endpoint (str): The endpoint used in the query
        - metadata_query_params (str): JSON string of the parameters used in the query
        - metadata_timestamp (str): ISO format timestamp of the response
        - metadata_api_version (str): Version of the API used
        - metadata_rate_limit_remaining (int): Number of requests left in current window
        - has_more (bool): Whether more pages of results are available
        - request_status (str): Status of the request ('success' or 'error')
    """
    return {
        "stats_data_0_player_name": "Mike Trout",
        "stats_data_0_team_name": "Los Angeles Angels",
        "stats_data_0_batting_avg": ".289",
        "stats_data_0_home_runs": 35,
        "stats_data_0_season": 2023,
        "stats_data_1_player_name": "Aaron Judge",
        "stats_data_1_team_name": "New York Yankees",
        "stats_data_1_batting_avg": ".305",
        "stats_data_1_home_runs": 42,
        "stats_data_1_season": 2023,
        "total_count": 2,
        "metadata_query_endpoint": "/players/stats",
        "metadata_query_params": json.dumps({"season": 2023, "gameType": "R"}),
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_api_version": "v1",
        "metadata_rate_limit_remaining": 98,
        "has_more": False,
        "request_status": "success"
    }


def mlb_stats_server_get_stats(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieves player or team statistics from the MLB stats server based on the provided endpoint and parameters.
    
    This function simulates querying an external MLB statistics API. It uses a helper function to simulate
    the external API call and then constructs a properly structured response that matches the expected schema.
    
    Args:
        endpoint (str): The API endpoint to query (e.g., '/players/stats', '/teams/stats').
        params (Dict[str, Any]): Query parameters to include in the request, such as season, game type, etc.
    
    Returns:
        Dict containing:
        - stats_data (List[Dict]): List of player or team statistics entries with fields like name, stats, and metadata.
        - total_count (int): Total number of statistic records returned.
        - metadata (Dict): Additional information about the request including query params, timestamp, API version, and rate limit.
        - has_more (bool): Indicates if additional pages of results are available.
        - request_status (str): Status of the API request ('success' or 'error').
    
    Raises:
        ValueError: If endpoint is empty or params is None.
    """
    # Input validation
    if not endpoint:
        raise ValueError("Endpoint is required and cannot be empty.")
    if params is None:
        raise ValueError("Params cannot be None.")
    
    try:
        # Call simulated external API
        api_data = call_external_api("mlb-stats-server-get_stats")
        
        # Construct stats_data list from indexed fields
        stats_data = [
            {
                "player_name": api_data["stats_data_0_player_name"],
                "team_name": api_data["stats_data_0_team_name"],
                "batting_avg": api_data["stats_data_0_batting_avg"],
                "home_runs": api_data["stats_data_0_home_runs"],
                "season": api_data["stats_data_0_season"]
            },
            {
                "player_name": api_data["stats_data_1_player_name"],
                "team_name": api_data["stats_data_1_team_name"],
                "batting_avg": api_data["stats_data_1_batting_avg"],
                "home_runs": api_data["stats_data_1_home_runs"],
                "season": api_data["stats_data_1_season"]
            }
        ]
        
        # Construct metadata dictionary
        metadata = {
            "query": {
                "endpoint": api_data["metadata_query_endpoint"],
                "params": json.loads(api_data["metadata_query_params"])
            },
            "timestamp": api_data["metadata_timestamp"],
            "api_version": api_data["metadata_api_version"],
            "rate_limit": {
                "remaining": api_data["metadata_rate_limit_remaining"]
            }
        }
        
        # Build final result matching output schema
        result = {
            "stats_data": stats_data,
            "total_count": api_data["total_count"],
            "metadata": metadata,
            "has_more": api_data["has_more"],
            "request_status": api_data["request_status"]
        }
        
        return result
        
    except Exception as e:
        # In case of any error during processing, return error response
        return {
            "stats_data": [],
            "total_count": 0,
            "metadata": {
                "query": {"endpoint": endpoint, "params": params},
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "api_version": "v1",
                "rate_limit": {"remaining": 100}
            },
            "has_more": False,
            "request_status": "error"
        }