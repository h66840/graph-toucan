from typing import Dict, List, Any, Optional
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
    Simulates fetching trending games data from external API for Steam platform.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success (bool): Whether the request was successful
        - platform (str): Platform name, e.g., "Steam"
        - type (str): Type of data returned, e.g., "Trending Games"
        - count (int): Total number of trending games
        - data_0_id (int): First game's ID
        - data_0_name (str): First game's name
        - data_0_price (float): First game's price in USD
        - data_0_headerImage (str): URL to first game's header image
        - data_0_category (str): Category of first game
        - data_0_isTrending (bool): Whether first game is trending
        - data_0_source (str): Data source for first game
        - data_0_url (str): Store URL for first game
        - data_0_releaseDate (str): Release date of first game (ISO format)
        - data_0_reviewScore (int): Review score (0-100) for first game
        - data_0_tags_0 (str): First tag for first game
        - data_0_tags_1 (str): Second tag for first game
        - data_0_discount (int): Discount percentage for first game
        - data_1_id (int): Second game's ID
        - data_1_name (str): Second game's name
        - data_1_price (float): Second game's price in USD
        - data_1_headerImage (str): URL to second game's header image
        - data_1_category (str): Category of second game
        - data_1_isTrending (bool): Whether second game is trending
        - data_1_source (str): Data source for second game
        - data_1_url (str): Store URL for second game
        - data_1_releaseDate (str): Release date of second game (ISO format)
        - data_1_reviewScore (int): Review score (0-100) for second game
        - data_1_tags_0 (str): First tag for second game
        - data_1_tags_1 (str): Second tag for second game
        - data_1_discount (int): Discount percentage for second game
        - sources_consulted_0 (str): First data source used
        - sources_consulted_1 (str): Second data source used
        - timestamp (str): ISO 8601 timestamp when data was fetched
    """
    return {
        "success": True,
        "platform": "Steam",
        "type": "Trending Games",
        "count": 2,
        "data_0_id": 108600,
        "data_0_name": "Counter-Strike 2",
        "data_0_price": 0.0,
        "data_0_headerImage": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/730/header.jpg",
        "data_0_category": "FPS",
        "data_0_isTrending": True,
        "data_0_source": "featured_home",
        "data_0_url": "https://store.steampowered.com/app/730/CounterStrike_2/",
        "data_0_releaseDate": "2012-08-21T00:00:00",
        "data_0_reviewScore": 85,
        "data_0_tags_0": "FPS",
        "data_0_tags_1": "Multiplayer",
        "data_0_discount": 0,
        "data_1_id": 292030,
        "data_1_name": "Palworld",
        "data_1_price": 29.99,
        "data_1_headerImage": "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/1623730/header.jpg",
        "data_1_category": "Survival",
        "data_1_isTrending": True,
        "data_1_source": "new_trending_api",
        "data_1_url": "https://store.steampowered.com/app/1623730/Palworld/",
        "data_1_releaseDate": "2024-01-19T00:00:00",
        "data_1_reviewScore": 78,
        "data_1_tags_0": "Survival",
        "data_1_tags_1": "Open World",
        "data_1_discount": 10,
        "sources_consulted_0": "featured_home",
        "sources_consulted_1": "new_trending_api",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def game_trends_get_steam_trending_games() -> Dict[str, Any]:
    """
    Get real trending games from Steam platform with live data from multiple sources.
    
    This function simulates fetching trending games data from Steam by calling an external API
    and transforming the flat response into a structured nested format.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - platform (str): Platform name (e.g., "Steam")
        - type (str): Type of data returned (e.g., "Trending Games")
        - count (int): Number of trending games returned
        - data (List[Dict]): List of game entries with details including:
            - id (int)
            - name (str)
            - price (float)
            - headerImage (str)
            - category (str)
            - isTrending (bool)
            - source (str)
            - url (str)
            - releaseDate (str, optional)
            - reviewScore (int, optional)
            - tags (List[str], optional)
            - discount (int, optional)
        - sources_consulted (List[str]): List of data sources used
        - timestamp (str): ISO 8601 timestamp when data was fetched
    """
    try:
        # Call external API to get flat data
        api_data = call_external_api("game-trends-get_steam_trending_games", **locals())
        
        # Construct the first game data
        game_0 = {
            "id": api_data["data_0_id"],
            "name": api_data["data_0_name"],
            "price": api_data["data_0_price"],
            "headerImage": api_data["data_0_headerImage"],
            "category": api_data["data_0_category"],
            "isTrending": api_data["data_0_isTrending"],
            "source": api_data["data_0_source"],
            "url": api_data["data_0_url"],
            "releaseDate": api_data["data_0_releaseDate"],
            "reviewScore": api_data["data_0_reviewScore"],
            "tags": [api_data["data_0_tags_0"], api_data["data_0_tags_1"]],
            "discount": api_data["data_0_discount"]
        }
        
        # Construct the second game data
        game_1 = {
            "id": api_data["data_1_id"],
            "name": api_data["data_1_name"],
            "price": api_data["data_1_price"],
            "headerImage": api_data["data_1_headerImage"],
            "category": api_data["data_1_category"],
            "isTrending": api_data["data_1_isTrending"],
            "source": api_data["data_1_source"],
            "url": api_data["data_1_url"],
            "releaseDate": api_data["data_1_releaseDate"],
            "reviewScore": api_data["data_1_reviewScore"],
            "tags": [api_data["data_1_tags_0"], api_data["data_1_tags_1"]],
            "discount": api_data["data_1_discount"]
        }
        
        # Construct sources consulted list
        sources_consulted = [
            api_data["sources_consulted_0"],
            api_data["sources_consulted_1"]
        ]
        
        # Build final result structure
        result = {
            "success": api_data["success"],
            "platform": api_data["platform"],
            "type": api_data["type"],
            "count": api_data["count"],
            "data": [game_0, game_1],
            "sources_consulted": sources_consulted,
            "timestamp": api_data["timestamp"]
        }
        
        return result
        
    except KeyError as e:
        # Handle missing keys in API response
        return {
            "success": False,
            "platform": "Steam",
            "type": "Trending Games",
            "count": 0,
            "data": [],
            "sources_consulted": [],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        # Handle any other unexpected errors
        return {
            "success": False,
            "platform": "Steam",
            "type": "Trending Games",
            "count": 0,
            "data": [],
            "sources_consulted": [],
            "timestamp": datetime.utcnow().isoformat() + "Z"
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
