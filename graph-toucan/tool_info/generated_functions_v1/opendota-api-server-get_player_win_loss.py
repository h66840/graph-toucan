from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for player win/loss statistics.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - wins (int): Number of games the player has won
        - losses (int): Number of games the player has lost
        - total_games (int): Total number of games played (sum of wins and losses)
        - win_rate (float): Win rate as a percentage (0.0 to 100.0)
    """
    # Simulated realistic data based on account_id (not used in simulation)
    return {
        "wins": 1250,
        "losses": 1120,
        "total_games": 2370,
        "win_rate": 52.74
    }

def opendota_api_server_get_player_win_loss(account_id: int) -> Dict[str, Any]:
    """
    Get win/loss statistics for a player.
    
    Args:
        account_id (int): Steam32 account ID of the player
    
    Returns:
        Dict containing:
        - wins (int): number of games the player has won
        - losses (int): number of games the player has lost
        - total_games (int): total number of games played (sum of wins and losses)
        - win_rate (float): win rate as a percentage (0.0 to 100.0)
    
    Raises:
        ValueError: If account_id is not a positive integer
    """
    # Input validation
    if not isinstance(account_id, int):
        raise ValueError("account_id must be an integer")
    if account_id <= 0:
        raise ValueError("account_id must be a positive integer")
    
    # Fetch data from external API simulation
    api_data = call_external_api("opendota-api-server-get_player_win_loss")
    
    # Construct result matching output schema
    result = {
        "wins": int(api_data["wins"]),
        "losses": int(api_data["losses"]),
        "total_games": int(api_data["total_games"]),
        "win_rate": float(api_data["win_rate"])
    }
    
    return result