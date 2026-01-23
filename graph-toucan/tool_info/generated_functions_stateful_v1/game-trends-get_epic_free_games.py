from typing import Dict, List, Any
import datetime

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
    Simulates fetching free games data from external API for Epic Games Store.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success (bool): Whether the API call succeeded
        - platform (str): Name of the platform offering free games
        - type (str): Type of data returned
        - count (int): Number of free games currently available
        - data_0_id (str): ID of the first game
        - data_0_name (str): Name of the first game
        - data_0_description (str): Description of the first game
        - data_0_originalPrice (float): Original price of the first game
        - data_0_discountPrice (float): Discounted price of the first game
        - data_0_releaseDate (str): Release date of the first game (ISO format)
        - data_0_isFreeNow (bool): Whether the first game is free now
        - data_0_isUpcomingFree (bool): Whether the first game is upcoming free
        - data_0_promotionDetails (str): Promotion details for the first game
        - data_0_url (str): URL to the first game
        - data_0_productSlug (str): Product slug of the first game
        - data_0_images (str): Comma-separated image URLs for the first game
        - data_0_source (str): Source of the first game data
        - data_1_id (str): ID of the second game
        - data_1_name (str): Name of the second game
        - data_1_description (str): Description of the second game
        - data_1_originalPrice (float): Original price of the second game
        - data_1_discountPrice (float): Discounted price of the second game
        - data_1_releaseDate (str): Release date of the second game (ISO format)
        - data_1_isFreeNow (bool): Whether the second game is free now
        - data_1_isUpcomingFree (bool): Whether the second game is upcoming free
        - data_1_promotionDetails (str): Promotion details for the second game
        - data_1_url (str): URL to the second game
        - data_1_productSlug (str): Product slug of the second game
        - data_1_images (str): Comma-separated image URLs for the second game
        - data_1_source (str): Source of the second game data
        - source_type (str): Identifier for the data source
        - timestamp (str): ISO 8601 timestamp of when the response was generated
    """
    return {
        "success": True,
        "platform": "Epic Games",
        "type": "Free Games",
        "count": 2,
        "data_0_id": "fortnite",
        "data_0_name": "Fortnite",
        "data_0_description": "An online multiplayer battle royale game developed by Epic Games.",
        "data_0_originalPrice": 39.99,
        "data_0_discountPrice": 0.0,
        "data_0_releaseDate": "2017-07-25T00:00:00Z",
        "data_0_isFreeNow": True,
        "data_0_isUpcomingFree": False,
        "data_0_promotionDetails": "Free to play indefinitely",
        "data_0_url": "https://www.epicgames.com/store/en-US/p/fortnite",
        "data_0_productSlug": "fortnite",
        "data_0_images": "https://cdn.epicgames.com/fortnite/offer/FN_Keyart_GBRomantic.jpg,https://cdn.epicgames.com/fortnite/offer/FNBR_TwitchDrop.jpg",
        "data_0_source": "epic_games_store",
        "data_1_id": "rocket-league",
        "data_1_name": "Rocket League",
        "data_1_description": "A vehicular soccer video game developed by Psyonix.",
        "data_1_originalPrice": 19.99,
        "data_1_discountPrice": 0.0,
        "data_1_releaseDate": "2015-07-07T00:00:00Z",
        "data_1_isFreeNow": False,
        "data_1_isUpcomingFree": True,
        "data_1_promotionDetails": "Will be free next week",
        "data_1_url": "https://www.epicgames.com/store/en-US/p/rocket-league",
        "data_1_productSlug": "rocket-league",
        "data_1_images": "https://cdn.epicgames.com/rocket-league/offer/RocketLeague_KeyArt.jpg,https://cdn.epicgames.com/rocket-league/offer/RocketLeague_Cars.jpg",
        "data_1_source": "epic_games_store",
        "source_type": "epic_free_games_api",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

def game_trends_get_epic_free_games() -> Dict[str, Any]:
    """
    Get current and upcoming free games from Epic Games Store with real promotion data.
    
    Returns:
        Dict containing:
        - success (bool): Indicates whether the API call was successful
        - platform (str): Name of the platform offering free games
        - type (str): Type of data returned
        - count (int): Number of free games currently available
        - data (List[Dict]): List of game entries with details like id, name, description,
          originalPrice, discountPrice, releaseDate, isFreeNow, isUpcomingFree,
          promotionDetails, url, productSlug, images, and source
        - source_type (str): Identifier for the data source
        - timestamp (str): ISO 8601 timestamp of when the response was generated
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("game-trends-get_epic_free_games", **locals())
        
        # Construct the first game entry
        game_0 = {
            "id": api_data["data_0_id"],
            "name": api_data["data_0_name"],
            "description": api_data["data_0_description"],
            "originalPrice": api_data["data_0_originalPrice"],
            "discountPrice": api_data["data_0_discountPrice"],
            "releaseDate": api_data["data_0_releaseDate"],
            "isFreeNow": api_data["data_0_isFreeNow"],
            "isUpcomingFree": api_data["data_0_isUpcomingFree"],
            "promotionDetails": api_data["data_0_promotionDetails"],
            "url": api_data["data_0_url"],
            "productSlug": api_data["data_0_productSlug"],
            "images": api_data["data_0_images"].split(",") if api_data["data_0_images"] else [],
            "source": api_data["data_0_source"]
        }
        
        # Construct the second game entry
        game_1 = {
            "id": api_data["data_1_id"],
            "name": api_data["data_1_name"],
            "description": api_data["data_1_description"],
            "originalPrice": api_data["data_1_originalPrice"],
            "discountPrice": api_data["data_1_discountPrice"],
            "releaseDate": api_data["data_1_releaseDate"],
            "isFreeNow": api_data["data_1_isFreeNow"],
            "isUpcomingFree": api_data["data_1_isUpcomingFree"],
            "promotionDetails": api_data["data_1_promotionDetails"],
            "url": api_data["data_1_url"],
            "productSlug": api_data["data_1_productSlug"],
            "images": api_data["data_1_images"].split(",") if api_data["data_1_images"] else [],
            "source": api_data["data_1_source"]
        }
        
        # Build final result structure
        result = {
            "success": api_data["success"],
            "platform": api_data["platform"],
            "type": api_data["type"],
            "count": api_data["count"],
            "data": [game_0, game_1],
            "source_type": api_data["source_type"],
            "timestamp": api_data["timestamp"]
        }
        
        return result
        
    except KeyError as e:
        return {
            "success": False,
            "platform": "Epic Games",
            "type": "Free Games",
            "count": 0,
            "data": [],
            "source_type": "epic_free_games_api",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "platform": "Epic Games",
            "type": "Free Games",
            "count": 0,
            "data": [],
            "source_type": "epic_free_games_api",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
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
