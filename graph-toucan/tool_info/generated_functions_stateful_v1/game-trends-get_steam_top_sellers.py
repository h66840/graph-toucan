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
    Simulates fetching top selling games data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success (bool): Whether the request was successful
        - platform (str): Name of the platform (e.g., "Steam")
        - type (str): Type of data returned (e.g., "Top Sellers")
        - count (int): Number of top-selling items returned
        - data_0_id (str): ID of the first game
        - data_0_name (str): Name of the first game
        - data_0_price (int): Price of the first game in cents
        - data_0_discount (int): Discount percentage for the first game
        - data_0_headerImage (str): URL to the header image of the first game
        - data_0_platform (str): Platform of the first game
        - data_0_releaseDate (str): Release date of the first game (YYYY-MM-DD)
        - data_0_reviewScore (int): Review score of the first game (0-100)
        - data_0_reviewCount (int): Number of reviews for the first game
        - data_0_tags (str): Comma-separated tags for the first game
        - data_0_rank (int): Rank of the first game in top sellers
        - data_0_isTopSeller (bool): Whether the first game is marked as top seller
        - data_0_source (str): Source identifier for the first game
        - data_0_url (str): URL to the game on Steam
        - data_1_id (str): ID of the second game
        - data_1_name (str): Name of the second game
        - data_1_price (int): Price of the second game in cents
        - data_1_discount (int): Discount percentage for the second game
        - data_1_headerImage (str): URL to the header image of the second game
        - data_1_platform (str): Platform of the second game
        - data_1_releaseDate (str): Release date of the second game (YYYY-MM-DD)
        - data_1_reviewScore (int): Review score of the second game (0-100)
        - data_1_reviewCount (int): Number of reviews for the second game
        - data_1_tags (str): Comma-separated tags for the second game
        - data_1_rank (int): Rank of the second game in top sellers
        - data_1_isTopSeller (bool): Whether the second game is marked as top seller
        - data_1_source (str): Source identifier for the second game
        - data_1_url (str): URL to the game on Steam
        - source_type (str): Identifier for the data source (e.g., "top_sellers_api")
        - timestamp (str): ISO 8601 timestamp when the response was generated
    """
    return {
        "success": True,
        "platform": "Steam",
        "type": "Top Sellers",
        "count": 2,
        "data_0_id": "730",
        "data_0_name": "Counter-Strike 2",
        "data_0_price": 0,
        "data_0_discount": 0,
        "data_0_headerImage": "https://steamcdn-a.akamaihd.net/steam/apps/730/header.jpg",
        "data_0_platform": "Windows",
        "data_0_releaseDate": "2012-08-21",
        "data_0_reviewScore": 95,
        "data_0_reviewCount": 25000000,
        "data_0_tags": "FPS,Shooter,Multiplayer,Competitive",
        "data_0_rank": 1,
        "data_0_isTopSeller": True,
        "data_0_source": "steam",
        "data_0_url": "https://store.steampowered.com/app/730",
        "data_1_id": "570",
        "data_1_name": "Dota 2",
        "data_1_price": 0,
        "data_1_discount": 0,
        "data_1_headerImage": "https://steamcdn-a.akamaihd.net/steam/apps/570/header.jpg",
        "data_1_platform": "Windows",
        "data_1_releaseDate": "2013-07-09",
        "data_1_reviewScore": 92,
        "data_1_reviewCount": 18000000,
        "data_1_tags": "MOBA,Strategy,Multiplayer,Free to Play",
        "data_1_rank": 2,
        "data_1_isTopSeller": True,
        "data_1_source": "steam",
        "data_1_url": "https://store.steampowered.com/app/570",
        "source_type": "top_sellers_api",
        "timestamp": datetime.now().isoformat()
    }

def game_trends_get_steam_top_sellers() -> Dict[str, Any]:
    """
    Get real top selling games from Steam platform with live sales data.
    
    This function retrieves the current top-selling games on Steam, including
    pricing, reviews, metadata, and ranking information.
    
    Returns:
        Dict containing:
        - success (bool): Indicates whether the request was successful
        - platform (str): Name of the platform (e.g., "Steam")
        - type (str): Type of data returned, e.g., "Top Sellers"
        - count (int): Number of top-selling items returned
        - data (List[Dict]): List of game entries with fields:
            - id (str): Game ID
            - name (str): Game name
            - price (int): Price in cents
            - discount (int): Discount percentage
            - headerImage (str): URL to header image
            - platform (str): Supported platform
            - releaseDate (str): Release date (YYYY-MM-DD)
            - reviewScore (int): Review score (0-100)
            - reviewCount (int): Number of reviews
            - tags (str): Comma-separated tags
            - rank (int): Sales rank
            - isTopSeller (bool): Whether marked as top seller
            - source (str): Data source
            - url (str): Game URL
        - source_type (str): Identifier for the data source
        - timestamp (str): ISO 8601 timestamp when the response was generated
    """
    try:
        # Call external API to get flattened data
        api_data = call_external_api("game-trends-get_steam_top_sellers", **locals())
        
        # Construct the first game entry
        game_0 = {
            "id": api_data["data_0_id"],
            "name": api_data["data_0_name"],
            "price": api_data["data_0_price"],
            "discount": api_data["data_0_discount"],
            "headerImage": api_data["data_0_headerImage"],
            "platform": api_data["data_0_platform"],
            "releaseDate": api_data["data_0_releaseDate"],
            "reviewScore": api_data["data_0_reviewScore"],
            "reviewCount": api_data["data_0_reviewCount"],
            "tags": api_data["data_0_tags"],
            "rank": api_data["data_0_rank"],
            "isTopSeller": api_data["data_0_isTopSeller"],
            "source": api_data["data_0_source"],
            "url": api_data["data_0_url"]
        }
        
        # Construct the second game entry
        game_1 = {
            "id": api_data["data_1_id"],
            "name": api_data["data_1_name"],
            "price": api_data["data_1_price"],
            "discount": api_data["data_1_discount"],
            "headerImage": api_data["data_1_headerImage"],
            "platform": api_data["data_1_platform"],
            "releaseDate": api_data["data_1_releaseDate"],
            "reviewScore": api_data["data_1_reviewScore"],
            "reviewCount": api_data["data_1_reviewCount"],
            "tags": api_data["data_1_tags"],
            "rank": api_data["data_1_rank"],
            "isTopSeller": api_data["data_1_isTopSeller"],
            "source": api_data["data_1_source"],
            "url": api_data["data_1_url"]
        }
        
        # Construct final result with proper nested structure
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
        # Handle missing fields in API response
        return {
            "success": False,
            "platform": "Steam",
            "type": "Top Sellers",
            "count": 0,
            "data": [],
            "source_type": "top_sellers_api",
            "timestamp": datetime.now().isoformat()
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
