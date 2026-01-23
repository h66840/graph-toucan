from typing import Dict, Any
import random
from datetime import datetime, timedelta

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock



def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching player statistics from Steam API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - last_played_game_game_name (str): Name of the most recently played game
        - last_played_game_app_id (int): Steam App ID of the game
        - last_played_game_playtime_minutes (int): Total playtime in minutes
        - last_played_game_last_played_timestamp (int): Unix timestamp of last session
        - steam_profile_steam_id (str): User's Steam ID
        - steam_profile_profile_url (str): Public profile URL
        - steam_profile_persona_name (str): Display name on Steam
        - steam_profile_avatar_url (str): URL to profile avatar image
        - player_stats_summary_total_games_owned (int): Number of games owned
        - player_stats_summary_total_playtime (int): Lifetime playtime in minutes
        - player_stats_summary_achievements_unlocked (int): Total achievements unlocked
        - player_stats_summary_days_since_last_play (int): Days since last game session
        - success (bool): Whether data retrieval was successful
        - error_message (str): Error description if failed, else empty string
    """
    # Simulate occasional failure
    success = random.choice([True, True, True, True, True])  # 80% success rate
    error_message = "" if success else "User profile is private or not found"

    # Generate realistic fake data
    game_names = [
        "Counter-Strike: Global Offensive",
        "Dota 2",
        "Team Fortress 2",
        "Portal 2",
        "The Witcher 3: Wild Hunt",
        "Cyberpunk 2077",
        "Hades",
        "Stardew Valley"
    ]
    chosen_game = random.choice(game_names)
    app_id = 730 if chosen_game == "Counter-Strike: Global Offensive" else random.randint(100000, 999999)

    now = datetime.now()
    last_played = now - timedelta(hours=random.randint(1, 72))
    days_since_last_play = random.randint(0, 30)

    return {
        "last_played_game_game_name": chosen_game,
        "last_played_game_app_id": app_id,
        "last_played_game_playtime_minutes": random.randint(100, 20000),
        "last_played_game_last_played_timestamp": int(last_played.timestamp()),
        "steam_profile_steam_id": f"7656{random.randint(100000000, 999999999)}",
        "steam_profile_profile_url": f"https://steamcommunity.com/id/{random.randint(1000000, 9999999)}",
        "steam_profile_persona_name": f"Player{random.randint(1000, 9999)}",
        "steam_profile_avatar_url": f"https://avatars.steamstatic.com/{random.randint(1000000, 9999999)}.jpg",
        "player_stats_summary_total_games_owned": random.randint(20, 500),
        "player_stats_summary_total_playtime": random.randint(5000, 100000),
        "player_stats_summary_achievements_unlocked": random.randint(100, 5000),
        "player_stats_summary_days_since_last_play": days_since_last_play,
        "success": success,
        "error_message": error_message
    }


def steam_statistics_get_player_stats(steam_id: str) -> Dict[str, Any]:
    """
    Retrieves a Steam user's gaming statistics including last played game, profile info, and activity summary.

    Args:
        steam_id (str): The Steam ID of the user to fetch statistics for

    Returns:
        Dict containing:
        - last_played_game (Dict): Details about the most recently played game
        - steam_profile (Dict): Basic Steam profile information
        - player_stats_summary (Dict): Aggregated statistics about the player's gaming activity
        - success (bool): Whether the data was retrieved successfully
        - error_message (str): Error description if request failed, otherwise None
    """
    # Input validation
    if not steam_id or not isinstance(steam_id, str) or len(steam_id.strip()) == 0:
        return {
            "last_played_game": None,
            "steam_profile": None,
            "player_stats_summary": None,
            "success": False,
            "error_message": "Invalid Steam ID provided"
        }

    # Fetch data from external API simulation
    api_data = call_external_api("steam-statistics-get_player_stats", **locals())

    # Construct nested output structure based on API response
    result = {
        "last_played_game": {
            "game_name": api_data["last_played_game_game_name"],
            "app_id": api_data["last_played_game_app_id"],
            "playtime_minutes": api_data["last_played_game_playtime_minutes"],
            "last_played_timestamp": api_data["last_played_game_last_played_timestamp"]
        } if api_data["success"] else None,
        "steam_profile": {
            "steam_id": api_data["steam_profile_steam_id"],
            "profile_url": api_data["steam_profile_profile_url"],
            "persona_name": api_data["steam_profile_persona_name"],
            "avatar_url": api_data["steam_profile_avatar_url"]
        } if api_data["success"] else None,
        "player_stats_summary": {
            "total_games_owned": api_data["player_stats_summary_total_games_owned"],
            "total_playtime": api_data["player_stats_summary_total_playtime"],
            "achievements_unlocked": api_data["player_stats_summary_achievements_unlocked"],
            "days_since_last_play": api_data["player_stats_summary_days_since_last_play"]
        } if api_data["success"] else None,
        "success": api_data["success"],
        "error_message": api_data["error_message"] if api_data["error_message"] else None
    }

    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        if "inventory" in tool_name:
            inv = sys_state.get_inventory()
            result["inventory"] = inv
            result["content"] = str(inv)
            
        if "add" in tool_name or "buy" in tool_name:
             item = kwargs.get("item")
             if item:
                 sys_state.add_item(item)
    except Exception:
        pass
    return result
