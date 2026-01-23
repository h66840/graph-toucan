from typing import Dict, Any

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
    Simulates fetching data from external BoardGameGeek API for a user.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - user_id (int): Unique identifier for the user on BoardGameGeek
        - username (str): The user's BoardGameGeek username
        - display_name (str): The name displayed on the user's profile
        - avatar_url (str): URL to the user's avatar image
        - year_registered (int): Year the user registered on BoardGameGeek
        - last_login (str): Timestamp of last login in ISO 8601 format
        - state_or_province (str): User-provided state or province
        - country (str): User-provided country
        - is_publisher (bool): Whether the user is associated with a game publisher
        - about (str): The 'About Me' text from the user's profile
        - website (str): Personal website URL provided by the user
        - trader_rating (float): Average rating given by other users in trades
        - trade_count (int): Number of completed trades reported by the user
        - collection_summary_owned (int): Count of games owned
        - collection_summary_wanting (int): Count of games wanting
        - collection_summary_prev_owned (int): Count of previously owned games
        - collection_summary_for_trade (int): Count of games for trade
        - collection_summary_want_to_play (int): Count of games user wants to play
        - collection_summary_want_to_buy (int): Count of games user wants to buy
        - stats_total_ratings (int): Total number of ratings submitted
        - stats_average_rating (float): Average rating given by user
        - stats_complexity_avg (float): Average complexity rating preferred by user
        - api_last_modified (str): Timestamp when data was last updated by BGG API (ISO 8601)
    """
    return {
        "user_id": 123456,
        "username": "bgg_user_123",
        "display_name": "BoardGameFan",
        "avatar_url": "https://cf.geekdo-images.com/avatars/avatar-12345.jpg",
        "year_registered": 2015,
        "last_login": "2023-10-05T14:30:00Z",
        "state_or_province": "California",
        "country": "United States",
        "is_publisher": False,
        "about": "I love playing board games every weekend with friends.",
        "website": "https://myboardgamesite.com",
        "trader_rating": 4.8,
        "trade_count": 27,
        "collection_summary_owned": 89,
        "collection_summary_wanting": 45,
        "collection_summary_prev_owned": 12,
        "collection_summary_for_trade": 5,
        "collection_summary_want_to_play": 33,
        "collection_summary_want_to_buy": 21,
        "stats_total_ratings": 342,
        "stats_average_rating": 7.6,
        "stats_complexity_avg": 2.8,
        "api_last_modified": "2023-10-05T14:30:00Z"
    }

def boardgamegeek_api_server_bgg_user(username: str) -> Dict[str, Any]:
    """
    Find details about a specific user on BoardGameGeek (BGG).
    
    Args:
        username (str): The username of the BoardGameGeek (BGG) user. 
                       When the user refers to themselves (me, my, I), use 'SELF' as the value.
    
    Returns:
        Dict containing detailed information about the BGG user with the following structure:
        - user_id (int): Unique identifier for the user on BoardGameGeek
        - username (str): The user's BoardGameGeek username
        - display_name (str): The name displayed on the user's profile
        - avatar_url (str): URL to the user's avatar image
        - year_registered (int): Year the user registered on BoardGameGeek
        - last_login (str): Timestamp of last login in ISO 8601 format
        - state_or_province (str): User-provided state or province
        - country (str): User-provided country
        - is_publisher (bool): Whether the user is associated with a game publisher
        - about (str): The 'About Me' text from the user's profile
        - website (str): Personal website URL provided by the user
        - trader_rating (float): Average rating given by other users in trades
        - trade_count (int): Number of completed trades reported by the user
        - collection_summary (Dict): Summary of user's game collection with keys:
            'owned', 'wanting', 'prev_owned', 'for_trade', 'want_to_play', 'want_to_buy'
        - stats (Dict): Aggregate statistics with keys:
            'total_ratings', 'average_rating', 'complexity_avg'
        - api_last_modified (str): Timestamp when data was last updated by BGG API (ISO 8601)
    
    Raises:
        ValueError: If username is empty or None
    """
    if not username:
        raise ValueError("Username is required")
    
    # Simulate API call to fetch user data
    api_data = call_external_api("boardgamegeek-api-server-bgg-user", **locals())
    
    # Construct nested structure matching output schema
    result = {
        "user_id": api_data["user_id"],
        "username": api_data["username"],
        "display_name": api_data["display_name"],
        "avatar_url": api_data["avatar_url"],
        "year_registered": api_data["year_registered"],
        "last_login": api_data["last_login"],
        "state_or_province": api_data["state_or_province"],
        "country": api_data["country"],
        "is_publisher": api_data["is_publisher"],
        "about": api_data["about"],
        "website": api_data["website"],
        "trader_rating": api_data["trader_rating"],
        "trade_count": api_data["trade_count"],
        "collection_summary": {
            "owned": api_data["collection_summary_owned"],
            "wanting": api_data["collection_summary_wanting"],
            "prev_owned": api_data["collection_summary_prev_owned"],
            "for_trade": api_data["collection_summary_for_trade"],
            "want_to_play": api_data["collection_summary_want_to_play"],
            "want_to_buy": api_data["collection_summary_want_to_buy"]
        },
        "stats": {
            "total_ratings": api_data["stats_total_ratings"],
            "average_rating": api_data["stats_average_rating"],
            "complexity_avg": api_data["stats_complexity_avg"]
        },
        "api_last_modified": api_data["api_last_modified"]
    }
    
    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # POST
        if "post" in tool_name or "send" in tool_name:
            content = kwargs.get("content") or kwargs.get("text") or kwargs.get("message")
            if content:
                sys_state.post_content(content)
                
        # FEED
        if "get" in tool_name or "feed" in tool_name or "timeline" in tool_name:
            posts = sys_state.get_feed()
            if posts:
                 result["content"] = posts
    except Exception:
        pass
    return result
