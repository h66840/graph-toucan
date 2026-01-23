from typing import Dict, Any, List

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
    Simulates fetching data from external API for gaming trends.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Indicates whether the overall request was successful
        - timestamp (str): ISO 8601 timestamp of when the response was generated
        - partial_failures_occurred (bool): Indicates if any part of the data retrieval failed
        - steam_trending_success (bool): Steam trending games fetch success status
        - steam_trending_platform (str): Platform name for Steam trending ("Steam")
        - steam_trending_type (str): Data type ("trending")
        - steam_trending_count (int): Number of trending games
        - steam_trending_timestamp (str): ISO timestamp for Steam trending data
        - steam_trending_source_0 (str): Source consulted for Steam trending
        - steam_trending_0_id (str): Game ID for first trending game on Steam
        - steam_trending_0_name (str): Name of first trending game on Steam
        - steam_trending_0_price (str): Price string of first trending game
        - steam_trending_0_discount (int): Discount percentage for first game
        - steam_trending_0_headerImage (str): URL to header image of first game
        - steam_trending_0_platform (str): Platform ("Steam") for first game
        - steam_trending_0_category (str): Category ("New & Trending") for first game
        - steam_trending_0_isTrending (bool): Whether first game is trending
        - steam_trending_0_source (str): Source API for first game
        - steam_trending_0_url (str): Store URL for first game
        - steam_trending_0_releaseDate (str): Release date of first game
        - steam_trending_0_reviewScore (str): Review score (usually "null")
        - steam_trending_0_tags_0 (str): First tag for first game (empty string if none)
        - steam_top_sellers_success (bool): Steam top sellers fetch success
        - steam_top_sellers_platform (str): Platform name ("Steam")
        - steam_top_sellers_type (str): Data type ("top_sellers")
        - steam_top_sellers_count (int): Number of top seller games
        - steam_top_sellers_timestamp (str): ISO timestamp for top sellers data
        - steam_top_sellers_source_type (str): Source type ("api")
        - steam_top_sellers_0_id (str): ID of first top seller game
        - steam_top_sellers_0_name (str): Name of first top seller game
        - steam_top_sellers_0_price (str): Price of first top seller
        - steam_top_sellers_0_discount (int): Discount percentage
        - steam_top_sellers_0_headerImage (str): Header image URL
        - steam_top_sellers_0_platform (str): Platform ("Steam")
        - steam_top_sellers_0_category (str): Category ("Top Sellers")
        - steam_top_sellers_0_isTopSeller (bool): Whether game is a top seller
        - steam_top_sellers_0_source (str): Source API
        - steam_top_sellers_0_url (str): Store URL
        - steam_top_sellers_0_releaseDate (str): Release date
        - steam_top_sellers_0_reviewScore (str): Review score (null)
        - steam_top_sellers_0_tags_0 (str): First tag (empty)
        - steam_top_sellers_0_rank (int): Sales rank (1)
        - steam_top_sellers_0_reviewCount (str): Review count (null)
        - steam_most_played_success (bool): Steam most played fetch success
        - steam_most_played_platform (str): Platform ("Steam")
        - steam_most_played_type (str): Data type ("most_played")
        - steam_most_played_count (int): Number of most played games
        - steam_most_played_timestamp (str): ISO timestamp
        - steam_most_played_sources_consulted_0 (str): Source consulted
        - steam_most_played_0_id (str): First most played game ID
        - steam_most_played_0_name (str): First most played game name
        - steam_most_played_0_price (str): Price string
        - steam_most_played_0_discount (int): Discount
        - steam_most_played_0_headerImage (str): Header image URL
        - steam_most_played_0_platform (str): Platform ("Steam")
        - steam_most_played_0_category (str): Category ("Most Played")
        - steam_most_played_0_isTrending (bool): Whether trending
        - steam_most_played_0_source (str): Source API
        - steam_most_played_0_url (str): Store URL
        - steam_most_played_0_releaseDate (str): Release date
        - steam_most_played_0_reviewScore (str): Review score (null)
        - steam_most_played_0_tags_0 (str): First tag (empty)
        - epic_free_games_success (bool): Epic free games fetch success
        - epic_free_games_platform (str): Platform ("Epic Games")
        - epic_free_games_type (str): Data type ("free_games")
        - epic_free_games_count (int): Number of free games
        - epic_free_games_timestamp (str): ISO timestamp
        - epic_free_games_source_type (str): Source type ("api")
        - epic_free_games_0_id (str): First free game ID
        - epic_free_games_0_namespace (str): Namespace identifier
        - epic_free_games_0_name (str): Game name
        - epic_free_games_0_description (str): Game description
        - epic_free_games_0_originalPrice (str): Original price
        - epic_free_games_0_discountPrice (str): Discounted price ("0")
        - epic_free_games_0_platform (str): Platform ("Epic Games")
        - epic_free_games_0_developer (str): Developer (null)
        - epic_free_games_0_publisher (str): Publisher (null)
        - epic_free_games_0_releaseDate (str): Release date (ISO 8601)
        - epic_free_games_0_tags_0 (str): First tag (empty)
        - epic_free_games_0_images_0_type (str): First image type ("OfferImageWide")
        - epic_free_games_0_images_0_url (str): First image URL
        - epic_free_games_0_isFreeNow (bool): Whether free now
        - epic_free_games_0_isUpcomingFree (bool): Whether upcoming free
        - epic_free_games_0_promotionDetails_startDate (str): Promotion start
        - epic_free_games_0_promotionDetails_endDate (str): Promotion end
        - epic_free_games_0_promotionDetails_type (str): Promotion type ("current")
        - epic_free_games_0_productSlug (str): Product slug
        - epic_free_games_0_url (str): Store URL
        - epic_free_games_0_source (str): Source API
        - epic_trending_games_success (bool): Epic trending games fetch success
        - epic_trending_games_platform (str): Platform ("Epic Games")
        - epic_trending_games_type (str): Data type ("trending")
        - epic_trending_games_count (int): Number of trending games
        - epic_trending_games_timestamp (str): ISO timestamp
        - epic_trending_games_source_type (str): Source type ("api")
    """
    return {
        "success": True,
        "timestamp": "2023-11-30T10:00:00Z",
        "partial_failures_occurred": False,
        "steam_trending_success": True,
        "steam_trending_platform": "Steam",
        "steam_trending_type": "trending",
        "steam_trending_count": 1,
        "steam_trending_timestamp": "2023-11-30T10:00:00Z",
        "steam_trending_source_0": "steam_api",
        "steam_trending_0_id": "730",
        "steam_trending_0_name": "Counter-Strike 2",
        "steam_trending_0_price": "$0.00",
        "steam_trending_0_discount": 0,
        "steam_trending_0_headerImage": "https://steamcdn-a.akamaihd.net/steam/apps/730/header.jpg",
        "steam_trending_0_platform": "Steam",
        "steam_trending_0_category": "New & Trending",
        "steam_trending_0_isTrending": True,
        "steam_trending_0_source": "steam_api",
        "steam_trending_0_url": "https://store.steampowered.com/app/730",
        "steam_trending_0_releaseDate": "Aug 21, 2012",
        "steam_trending_0_reviewScore": "null",
        "steam_trending_0_tags_0": "",
        "steam_top_sellers_success": True,
        "steam_top_sellers_platform": "Steam",
        "steam_top_sellers_type": "top_sellers",
        "steam_top_sellers_count": 1,
        "steam_top_sellers_timestamp": "2023-11-30T10:00:00Z",
        "steam_top_sellers_source_type": "api",
        "steam_top_sellers_0_id": "10",
        "steam_top_sellers_0_name": "Grand Theft Auto V",
        "steam_top_sellers_0_price": "$29.99",
        "steam_top_sellers_0_discount": 0,
        "steam_top_sellers_0_headerImage": "https://steamcdn-a.akamaihd.net/steam/apps/10/header.jpg",
        "steam_top_sellers_0_platform": "Steam",
        "steam_top_sellers_0_category": "Top Sellers",
        "steam_top_sellers_0_isTopSeller": True,
        "steam_top_sellers_0_source": "steam_api",
        "steam_top_sellers_0_url": "https://store.steampowered.com/app/10",
        "steam_top_sellers_0_releaseDate": "Apr 13, 2015",
        "steam_top_sellers_0_reviewScore": "null",
        "steam_top_sellers_0_tags_0": "",
        "steam_top_sellers_0_rank": 1,
        "steam_top_sellers_0_reviewCount": "null",
        "steam_most_played_success": True,
        "steam_most_played_platform": "Steam",
        "steam_most_played_type": "most_played",
        "steam_most_played_count": 1,
        "steam_most_played_timestamp": "2023-11-30T10:00:00Z",
        "steam_most_played_sources_consulted_0": "steam_live_api",
        "steam_most_played_0_id": "730",
        "steam_most_played_0_name": "Counter-Strike 2",
        "steam_most_played_0_price": "$0.00",
        "steam_most_played_0_discount": 0,
        "steam_most_played_0_headerImage": "https://steamcdn-a.akamaihd.net/steam/apps/730/header.jpg",
        "steam_most_played_0_platform": "Steam",
        "steam_most_played_0_category": "Most Played",
        "steam_most_played_0_isTrending": True,
        "steam_most_played_0_source": "steam_live_api",
        "steam_most_played_0_url": "https://store.steampowered.com/app/730",
        "steam_most_played_0_releaseDate": "Aug 21, 2012",
        "steam_most_played_0_reviewScore": "null",
        "steam_most_played_0_tags_0": "",
        "epic_free_games_success": True,
        "epic_free_games_platform": "Epic Games",
        "epic_free_games_type": "free_games",
        "epic_free_games_count": 1,
        "epic_free_games_timestamp": "2023-11-30T10:00:00Z",
        "epic_free_games_source_type": "api",
        "epic_free_games_0_id": "5e6b5b3a1e2a4e1d8c5d0a1b2c3d4e5f",
        "epic_free_games_0_namespace": "ue",
        "epic_free_games_0_name": "Unreal Engine: The Game",
        "epic_free_games_0_description": "A game about creating games.",
        "epic_free_games_0_originalPrice": "$19.99",
        "epic_free_games_0_discountPrice": "0",
        "epic_free_games_0_platform": "Epic Games",
        "epic_free_games_0_developer": "null",
        "epic_free_games_0_publisher": "null",
        "epic_free_games_0_releaseDate": "2023-11-30T00:00:00Z",
        "epic_free_games_0_tags_0": "",
        "epic_free_games_0_images_0_type": "OfferImageWide",
        "epic_free_games_0_images_0_url": "https://egscdn.com/ue-game-wide.jpg",
        "epic_free_games_0_isFreeNow": True,
        "epic_free_games_0_isUpcomingFree": False,
        "epic_free_games_0_promotionDetails_startDate": "2023-11-30T00:00:00Z",
        "epic_free_games_0_promotionDetails_endDate": "2023-12-07T00:00:00Z",
        "epic_free_games_0_promotionDetails_type": "current",
        "epic_free_games_0_productSlug": "unreal-engine-game",
        "epic_free_games_0_url": "https://store.epicgames.com/en-US/p/unreal-engine-game",
        "epic_free_games_0_source": "epic_free_games_api",
        "epic_trending_games_success": True,
        "epic_trending_games_platform": "Epic Games",
        "epic_trending_games_type": "trending",
        "epic_trending_games_count": 0,
        "epic_trending_games_timestamp": "2023-11-30T10:00:00Z",
        "epic_trending_games_source_type": "api"
    }

def game_trends_get_all_trending_games() -> Dict[str, Any]:
    """
    Get comprehensive real-time gaming data from all platforms (Steam and Epic Games).
    
    Returns:
        Dict containing:
        - success (bool): indicates whether the overall request was successful
        - timestamp (str): ISO 8601 timestamp of when the response was generated
        - data (Dict): contains all categorized gaming trend data from Steam and Epic Games
        - partial_failures_occurred (bool): indicates if any part of the data retrieval failed
        
        Within data:
        - steam_trending (Dict): Steam trending games data
        - steam_top_sellers (Dict): Steam top-selling games data
        - steam_most_played (Dict): Steam live most-played games data
        - epic_free_games (Dict): currently free games on Epic Games Store
        - epic_trending_games (Dict): trending games on Epic Games Store (often empty)
        
    Each game entry in the data lists contains various fields like id, name, price, etc.,
    following the structure defined in the tool specification.
    """
    try:
        # Fetch flattened data from simulated external API
        api_data = call_external_api("game-trends-get_all_trending_games", **locals())
        
        # Construct steam_trending data
        steam_trending_data = []
        if api_data["steam_trending_count"] > 0:
            steam_trending_data.append({
                "id": api_data["steam_trending_0_id"],
                "name": api_data["steam_trending_0_name"],
                "price": api_data["steam_trending_0_price"],
                "discount": api_data["steam_trending_0_discount"],
                "headerImage": api_data["steam_trending_0_headerImage"],
                "platform": api_data["steam_trending_0_platform"],
                "category": api_data["steam_trending_0_category"],
                "isTrending": api_data["steam_trending_0_isTrending"],
                "source": api_data["steam_trending_0_source"],
                "url": api_data["steam_trending_0_url"],
                "releaseDate": api_data["steam_trending_0_releaseDate"],
                "reviewScore": None if api_data["steam_trending_0_reviewScore"] == "null" else api_data["steam_trending_0_reviewScore"],
                "tags": [] if api_data["steam_trending_0_tags_0"] == "" else [api_data["steam_trending_0_tags_0"]]
            })
        
        steam_trending = {
            "success": api_data["steam_trending_success"],
            "platform": api_data["steam_trending_platform"],
            "type": api_data["steam_trending_type"],
            "count": api_data["steam_trending_count"],
            "data": steam_trending_data,
            "sources_consulted": [api_data["steam_trending_source_0"]],
            "timestamp": api_data["steam_trending_timestamp"]
        }
        
        # Construct steam_top_sellers data
        steam_top_sellers_data = []
        if api_data["steam_top_sellers_count"] > 0:
            steam_top_sellers_data.append({
                "id": api_data["steam_top_sellers_0_id"],
                "name": api_data["steam_top_sellers_0_name"],
                "price": api_data["steam_top_sellers_0_price"],
                "discount": api_data["steam_top_sellers_0_discount"],
                "headerImage": api_data["steam_top_sellers_0_headerImage"],
                "platform": api_data["steam_top_sellers_0_platform"],
                "category": api_data["steam_top_sellers_0_category"],
                "isTopSeller": api_data["steam_top_sellers_0_isTopSeller"],
                "source": api_data["steam_top_sellers_0_source"],
                "url": api_data["steam_top_sellers_0_url"],
                "releaseDate": api_data["steam_top_sellers_0_releaseDate"],
                "reviewScore": None if api_data["steam_top_sellers_0_reviewScore"] == "null" else api_data["steam_top_sellers_0_reviewScore"],
                "tags": [] if api_data["steam_top_sellers_0_tags_0"] == "" else [api_data["steam_top_sellers_0_tags_0"]],
                "rank": api_data["steam_top_sellers_0_rank"],
                "reviewCount": None if api_data["steam_top_sellers_0_reviewCount"] == "null" else api_data["steam_top_sellers_0_reviewCount"]
            })
        
        steam_top_sellers = {
            "success": api_data["steam_top_sellers_success"],
            "platform": api_data["steam_top_sellers_platform"],
            "type": api_data["steam_top_sellers_type"],
            "count": api_data["steam_top_sellers_count"],
            "data": steam_top_sellers_data,
            "source_type": api_data["steam_top_sellers_source_type"],
            "timestamp": api_data["steam_top_sellers_timestamp"]
        }
        
        # Construct steam_most_played data
        steam_most_played_data = []
        if api_data["steam_most_played_count"] > 0:
            steam_most_played_data.append({
                "id": api_data["steam_most_played_0_id"],
                "name": api_data["steam_most_played_0_name"],
                "price": api_data["steam_most_played_0_price"],
                "discount": api_data["steam_most_played_0_discount"],
                "headerImage": api_data["steam_most_played_0_headerImage"],
                "platform": api_data["steam_most_played_0_platform"],
                "category": api_data["steam_most_played_0_category"],
                "isTrending": api_data["steam_most_played_0_isTrending"],
                "source": api_data["steam_most_played_0_source"],
                "url": api_data["steam_most_played_0_url"],
                "releaseDate": api_data["steam_most_played_0_releaseDate"],
                "reviewScore": None if api_data["steam_most_played_0_reviewScore"] == "null" else api_data["steam_most_played_0_reviewScore"],
                "tags": [] if api_data["steam_most_played_0_tags_0"] == "" else [api_data["steam_most_played_0_tags_0"]]
            })
        
        steam_most_played = {
            "success": api_data["steam_most_played_success"],
            "platform": api_data["steam_most_played_platform"],
            "type": api_data["steam_most_played_type"],
            "count": api_data["steam_most_played_count"],
            "data": steam_most_played_data,
            "sources_consulted": [api_data["steam_most_played_sources_consulted_0"]],
            "timestamp": api_data["steam_most_played_timestamp"]
        }
        
        # Construct epic_free_games data
        epic_free_games_data = []
        if api_data["epic_free_games_count"] > 0:
            epic_free_games_data.append({
                "id": api_data["epic_free_games_0_id"],
                "namespace": api_data["epic_free_games_0_namespace"],
                "name": api_data["epic_free_games_0_name"],
                "description": api_data["epic_free_games_0_description"],
                "originalPrice": api_data["epic_free_games_0_originalPrice"],
                "discountPrice": api_data["epic_free_games_0_discountPrice"],
                "platform": api_data["epic_free_games_0_platform"],
                "developer": None if api_data["epic_free_games_0_developer"] == "null" else api_data["epic_free_games_0_developer"],
                "publisher": None if api_data["epic_free_games_0_publisher"] == "null" else api_data["epic_free_games_0_publisher"],
                "releaseDate": api_data["epic_free_games_0_releaseDate"],
                "tags": [] if api_data["epic_free_games_0_tags_0"] == "" else [api_data["epic_free_games_0_tags_0"]],
                "images": [
                    {
                        "type": api_data["epic_free_games_0_images_0_type"],
                        "url": api_data["epic_free_games_0_images_0_url"]
                    }
                ],
                "isFreeNow": api_data["epic_free_games_0_isFreeNow"],
                "isUpcomingFree": api_data["epic_free_games_0_isUpcomingFree"],
                "promotionDetails": {
                    "startDate": api_data["epic_free_games_0_promotionDetails_startDate"],
                    "endDate": api_data["epic_free_games_0_promotionDetails_endDate"],
                    "type": api_data["epic_free_games_0_promotionDetails_type"]
                },
                "productSlug": api_data["epic_free_games_0_productSlug"],
                "url": api_data["epic_free_games_0_url"],
                "source": api_data["epic_free_games_0_source"]
            })
        
        epic_free_games = {
            "success": api_data["epic_free_games_success"],
            "platform": api_data["epic_free_games_platform"],
            "type": api_data["epic_free_games_type"],
            "count": api_data["epic_free_games_count"],
            "data": epic_free_games_data,
            "source_type": api_data["epic_free_games_source_type"],
            "timestamp": api_data["epic_free_games_timestamp"]
        }
        
        # Construct epic_trending_games data
        epic_trending_games = {
            "success": api_data["epic_trending_games_success"],
            "platform": api_data["epic_trending_games_platform"],
            "type": api_data["epic_trending_games_type"],
            "count": api_data["epic_trending_games_count"],
            "data": [],
            "source_type": api_data["epic_trending_games_source_type"],
            "timestamp": api_data["epic_trending_games_timestamp"]
        }
        
        # Assemble final data structure
        result = {
            "success": api_data["success"],
            "timestamp": api_data["timestamp"],
            "data": {
                "steam_trending": steam_trending,
                "steam_top_sellers": steam_top_sellers,
                "steam_most_played": steam_most_played,
                "epic_free_games": epic_free_games,
                "epic_trending_games": epic_trending_games
            },
            "partial_failures_occurred": api_data["partial_failures_occurred"]
        }
        
        return result
        
    except Exception as e:
        # In case of any error during processing, return failure response
        return {
            "success": False,
            "timestamp": "2023-11-30T10:00:00Z",
            "data": {
                "steam_trending": {"success": False, "data": [], "count": 0},
                "steam_top_sellers": {"success": False, "data": [], "count": 0},
                "steam_most_played": {"success": False, "data": [], "count": 0},
                "epic_free_games": {"success": False, "data": [], "count": 0},
                "epic_trending_games": {"success": False, "data": [], "count": 0}
            },
            "partial_failures_occurred": True
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
