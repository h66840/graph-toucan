from typing import Dict, List, Any
from datetime import datetime

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
    Simulates fetching data from external API for Epic Games Store trending games.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Whether the request was successful
        - platform (str): Name of the gaming platform
        - type (str): Type of data returned
        - count (int): Number of trending games
        - data_0_title (str): Title of the first trending game
        - data_0_trend_score (float): Trend score of the first game
        - data_0_release_date (str): Release date of the first game
        - data_1_title (str): Title of the second trending game
        - data_1_trend_score (float): Trend score of the second game
        - data_1_release_date (str): Release date of the second game
        - source_type (str): Identifier for the data source method
        - timestamp (str): ISO 8601 timestamp when data was fetched
    """
    return {
        "success": True,
        "platform": "Epic Games Store",
        "type": "Trending Games",
        "count": 2,
        "data_0_title": "Fortnite",
        "data_0_trend_score": 98.7,
        "data_0_release_date": "2017-07-25",
        "data_1_title": "Rocket League",
        "data_1_trend_score": 89.3,
        "data_1_release_date": "2015-07-07",
        "source_type": "epic_store_scrape",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }


def game_trends_get_epic_trending_games() -> Dict[str, Any]:
    """
    Get trending games from Epic Games Store.

    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - platform (str): Name of the gaming platform where trends were collected
        - type (str): Type of data returned (e.g., "Trending Games")
        - count (int): Number of trending games in the response
        - data (List[Dict]): List of game entries with title, trend metrics, and metadata
        - source_type (str): Identifier for the data source method
        - timestamp (str): ISO 8601 timestamp of when the data was fetched

    Example:
        {
            "success": True,
            "platform": "Epic Games Store",
            "type": "Trending Games",
            "count": 2,
            "data": [
                {
                    "title": "Fortnite",
                    "trend_score": 98.7,
                    "release_date": "2017-07-25"
                },
                {
                    "title": "Rocket League",
                    "trend_score": 89.3,
                    "release_date": "2015-07-07"
                }
            ],
            "source_type": "epic_store_scrape",
            "timestamp": "2023-10-05T12:34:56Z"
        }
    """
    try:
        api_data = call_external_api("game-trends-get_epic_trending_games", **locals())

        # Construct the data list from indexed fields
        data = [
            {
                "title": api_data["data_0_title"],
                "trend_score": api_data["data_0_trend_score"],
                "release_date": api_data["data_0_release_date"]
            },
            {
                "title": api_data["data_1_title"],
                "trend_score": api_data["data_1_trend_score"],
                "release_date": api_data["data_1_release_date"]
            }
        ]

        result = {
            "success": api_data["success"],
            "platform": api_data["platform"],
            "type": api_data["type"],
            "count": api_data["count"],
            "data": data,
            "source_type": api_data["source_type"],
            "timestamp": api_data["timestamp"]
        }

        return result

    except KeyError as e:
        return {
            "success": False,
            "platform": "Epic Games Store",
            "type": "Trending Games",
            "count": 0,
            "data": [],
            "source_type": "epic_store_scrape",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "Epic Games Store",
            "type": "Trending Games",
            "count": 0,
            "data": [],
            "source_type": "epic_store_scrape",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }

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
