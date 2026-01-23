from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Steam most played games.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - game_0_rank (int): Rank of the first game
        - game_0_title (str): Title of the first game
        - game_0_current_players (int): Current number of players for the first game
        - game_0_peak_today (int): Peak player count today for the first game
        - game_0_24h_peak (int): Peak player count in the last 24 hours for the first game
        - game_0_url (str): URL to the first game's SteamCharts page
        - game_1_rank (int): Rank of the second game
        - game_1_title (str): Title of the second game
        - game_1_current_players (int): Current number of players for the second game
        - game_1_peak_today (int): Peak player count today for the second game
        - game_1_24h_peak (int): Peak player count in the last 24 hours for the second game
        - game_1_url (str): URL to the second game's SteamCharts page
        - last_updated (str): ISO 8601 timestamp when data was last refreshed
        - total_games (int): Total number of games included in the response
        - source (str): Name or URL of the data source
        - metadata_status (str): Retrieval status (e.g., 'success')
        - metadata_region (str): Region covered by the data (e.g., 'global')
        - metadata_time_range (str): Time range covered (e.g., '24h')
    """
    return {
        "game_0_rank": 1,
        "game_0_title": "Counter-Strike 2",
        "game_0_current_players": 850000,
        "game_0_peak_today": 920000,
        "game_0_24h_peak": 950000,
        "game_0_url": "https://steamcharts.com/app/730",
        "game_1_rank": 2,
        "game_1_title": "Dota 2",
        "game_1_current_players": 530000,
        "game_1_peak_today": 580000,
        "game_1_24h_peak": 600000,
        "game_1_url": "https://steamcharts.com/app/570",
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "total_games": 2,
        "source": "SteamCharts",
        "metadata_status": "success",
        "metadata_region": "global",
        "metadata_time_range": "24h"
    }


def game_trends_get_steam_most_played() -> Dict[str, Any]:
    """
    Fetch real-time most played games from Steam with live player statistics from SteamCharts.

    Returns:
        Dict containing:
        - games (List[Dict]): List of games with live player statistics, each containing
          'rank', 'title', 'current_players', 'peak_today', '24h_peak', and 'url' fields
        - last_updated (str): ISO 8601 timestamp indicating when the data was last refreshed
        - total_games (int): Total number of games included in the response
        - source (str): Name or URL of the data source (e.g., 'SteamCharts')
        - metadata (Dict): Additional context such as retrieval status, region, or time range covered
    """
    try:
        api_data = call_external_api("game-trends-get_steam_most_played")

        # Construct games list from indexed fields
        games = [
            {
                "rank": api_data["game_0_rank"],
                "title": api_data["game_0_title"],
                "current_players": api_data["game_0_current_players"],
                "peak_today": api_data["game_0_peak_today"],
                "24h_peak": api_data["game_0_24h_peak"],
                "url": api_data["game_0_url"]
            },
            {
                "rank": api_data["game_1_rank"],
                "title": api_data["game_1_title"],
                "current_players": api_data["game_1_current_players"],
                "peak_today": api_data["game_1_peak_today"],
                "24h_peak": api_data["game_1_24h_peak"],
                "url": api_data["game_1_url"]
            }
        ]

        # Build final result structure
        result = {
            "games": games,
            "last_updated": api_data["last_updated"],
            "total_games": api_data["total_games"],
            "source": api_data["source"],
            "metadata": {
                "status": api_data["metadata_status"],
                "region": api_data["metadata_region"],
                "time_range": api_data["metadata_time_range"]
            }
        }

        return result

    except KeyError as e:
        # Handle missing expected fields
        raise ValueError(f"Missing required data field: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve Steam most played games data: {str(e)}") from e