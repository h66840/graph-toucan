from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external MLB stats API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - game_id (int): unique identifier for the game (gamePk) from MLB's stats API
        - team_id (int): identifier for the team that played in the game
        - date (str): date of the game in YYYY-MM-DD format
        - status (str): status of the game, e.g., "Final" indicating the game has completed
    """
    # Simulated realistic response data for the given tool
    return {
        "game_id": 715843,
        "team_id": 137,
        "date": "2023-10-01",
        "status": "Final"
    }

def mlb_stats_server_get_last_game(team_id: int) -> Dict[str, Any]:
    """
    Get the gamePk (game_id) for the given team's most recent completed game.
    
    Args:
        team_id (int): Identifier for the MLB team
        
    Returns:
        Dict containing:
        - game_id (int): unique identifier for the game (gamePk) from MLB's stats API
        - team_id (int): identifier for the team that played in the game
        - date (str): date of the game in YYYY-MM-DD format
        - status (str): status of the game, e.g., "Final" indicating the game has completed
        
    Raises:
        ValueError: If team_id is not a positive integer
    """
    # Input validation
    if not isinstance(team_id, int) or team_id <= 0:
        raise ValueError("team_id must be a positive integer")
    
    # Call external API simulation
    api_data = call_external_api("mlb-stats-server-get_last_game")
    
    # Construct result matching output schema
    result = {
        "game_id": api_data["game_id"],
        "team_id": team_id,  # Use input team_id to ensure consistency
        "date": api_data["date"],
        "status": api_data["status"]
    }
    
    return result