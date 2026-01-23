from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB top prospects.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - prospect_0_name (str): Name of the first prospect
        - prospect_0_position (str): Position of the first prospect
        - prospect_0_team (str): Team of the first prospect
        - prospect_0_ranking (int): Ranking of the first prospect
        - prospect_0_velocity (int): Fastball velocity (for pitchers) or power grade (for batters)
        - prospect_1_name (str): Name of the second prospect
        - prospect_1_position (str): Position of the second prospect
        - prospect_1_team (str): Team of the second prospect
        - prospect_1_ranking (int): Ranking of the second prospect
        - prospect_1_velocity (int): Fastball velocity (for pitchers) or power grade (for batters)
        - ranking_type (str): Either 'team-specific' or 'leaguewide'
        - player_category (str): Either 'pitchers', 'batters', or 'both'
        - total_count (int): Total number of prospects returned
        - metadata_timestamp (str): ISO format timestamp of data retrieval
        - metadata_source_version (str): Version of the source database
        - metadata_query_team (str): Team name used in query, or empty if leaguewide
        - metadata_query_player_type (str): Player type filter used ('pitchers', 'batters', or 'both')
    """
    return {
        "prospect_0_name": "Jackson Holliday",
        "prospect_0_position": "SS",
        "prospect_0_team": "Baltimore Orioles",
        "prospect_0_ranking": 1,
        "prospect_0_velocity": 60,
        "prospect_1_name": "Paul Skenes",
        "prospect_1_position": "RHP",
        "prospect_1_team": "Pittsburgh Pirates",
        "prospect_1_ranking": 2,
        "prospect_1_velocity": 98,
        "ranking_type": "leaguewide",
        "player_category": "both",
        "total_count": 2,
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_source_version": "2024.1",
        "metadata_query_team": "",
        "metadata_query_player_type": "both"
    }


def mlb_stats_server_get_top_prospects(team: Optional[str] = None, player_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieves the top prospects by team or leaguewide.
    It can return top prospect pitchers, batters, or both.

    Args:
        team (Optional[str]): The team name for which you wish to retrieve top prospects.
                              If not specified, returns leaguewide top prospects.
        player_type (Optional[str]): Either "pitchers" or "batters".
                                     If not specified, returns both pitchers and batters.

    Returns:
        Dict containing:
        - prospects (List[Dict]): List of prospect player objects with name, position, team, ranking, and key attributes
        - ranking_type (str): Indicates whether the ranking is 'team-specific' or 'leaguewide'
        - player_category (str): The type of players returned: 'pitchers', 'batters', or 'both'
        - total_count (int): Total number of prospects returned
        - metadata (Dict): Additional context such as timestamp, source version, and query parameters

    Raises:
        ValueError: If player_type is provided but not one of 'pitchers' or 'batters'
    """
    # Input validation
    if player_type is not None and player_type not in ["pitchers", "batters"]:
        raise ValueError("player_type must be either 'pitchers' or 'batters'")

    # Simulate API call with query parameters
    api_data = call_external_api("mlb-stats-server-get_top_prospects")

    # Construct prospects list from flattened API data
    prospects = [
        {
            "name": api_data["prospect_0_name"],
            "position": api_data["prospect_0_position"],
            "team": api_data["prospect_0_team"],
            "ranking": api_data["prospect_0_ranking"],
            "velocity": api_data["prospect_0_velocity"]  # Could represent fastball velocity or power grade
        },
        {
            "name": api_data["prospect_1_name"],
            "position": api_data["prospect_1_position"],
            "team": api_data["prospect_1_team"],
            "ranking": api_data["prospect_1_ranking"],
            "velocity": api_data["prospect_1_velocity"]
        }
    ]

    # Determine ranking type based on team parameter
    ranking_type = "team-specific" if team is not None else "leaguewide"

    # Use provided player_type or default to "both"
    player_category = player_type if player_type is not None else "both"

    # Construct metadata
    metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "source_version": api_data["metadata_source_version"],
        "query_parameters": {
            "team": team or api_data["metadata_query_team"],
            "player_type": player_category
        }
    }

    # Return structured response matching output schema
    return {
        "prospects": prospects,
        "ranking_type": ranking_type,
        "player_category": player_category,
        "total_count": api_data["total_count"],
        "metadata": metadata
    }