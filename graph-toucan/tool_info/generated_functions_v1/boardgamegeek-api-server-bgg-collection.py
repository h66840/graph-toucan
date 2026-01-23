from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external BoardGameGeek API for a user's collection.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - collection_status (str): Status of the collection query (e.g., "success", "no_items_found")
        - message (str): Human-readable message about the result
        - total_count (int): Total number of items returned
        - item_0_id (int): ID of the first board game
        - item_0_name (str): Name of the first board game
        - item_0_year_published (int): Year the first game was published
        - item_0_status_owned (bool): Whether the first game is owned
        - item_0_status_for_trade (bool): Whether the first game is marked for trade
        - item_0_status_preordered (bool): Whether the first game is preordered
        - item_0_status_want_to_buy (bool): Whether the user wants to buy the first game
        - item_0_status_want_to_play (bool): Whether the user wants to play the first game
        - item_0_status_wishlist (bool): Whether the first game is wishlisted
        - item_0_personal_rating (float): User's personal rating for the first game
        - item_0_bgg_rating (float): BGG average rating for the first game
        - item_0_plays (int): Number of times the first game has been played
        - item_0_wishlist_priority (int): Wishlist priority of the first game (1-5)
        - item_0_has_parts (bool): Whether the first game has spare parts
        - item_1_id (int): ID of the second board game
        - item_1_name (str): Name of the second board game
        - item_1_year_published (int): Year the second game was published
        - item_1_status_owned (bool): Whether the second game is owned
        - item_1_status_for_trade (bool): Whether the second game is marked for trade
        - item_1_status_preordered (bool): Whether the second game is preordered
        - item_1_status_want_to_buy (bool): Whether the user wants to buy the second game
        - item_1_status_want_to_play (bool): Whether the user wants to play the second game
        - item_1_status_wishlist (bool): Whether the second game is wishlisted
        - item_1_personal_rating (float): User's personal rating for the second game
        - item_1_bgg_rating (float): BGG average rating for the second game
        - item_1_plays (int): Number of times the second game has been played
        - item_1_wishlist_priority (int): Wishlist priority of the second game (1-5)
        - item_1_has_parts (bool): Whether the second game has spare parts
    """
    return {
        "collection_status": "success",
        "message": "Collection retrieved successfully",
        "total_count": 2,
        "item_0_id": 123456,
        "item_0_name": "Wingspan",
        "item_0_year_published": 2019,
        "item_0_status_owned": True,
        "item_0_status_for_trade": False,
        "item_0_status_preordered": False,
        "item_0_status_want_to_buy": False,
        "item_0_status_want_to_play": True,
        "item_0_status_wishlist": False,
        "item_0_personal_rating": 9.5,
        "item_0_bgg_rating": 8.15,
        "item_0_plays": 12,
        "item_0_wishlist_priority": 3,
        "item_0_has_parts": True,
        "item_1_id": 789012,
        "item_1_name": "Terraforming Mars",
        "item_1_year_published": 2016,
        "item_1_status_owned": True,
        "item_1_status_for_trade": True,
        "item_1_status_preordered": False,
        "item_1_status_want_to_buy": False,
        "item_1_status_want_to_play": False,
        "item_1_status_wishlist": False,
        "item_1_personal_rating": 9.8,
        "item_1_bgg_rating": 8.39,
        "item_1_plays": 25,
        "item_1_wishlist_priority": 1,
        "item_1_has_parts": False
    }

def boardgamegeek_api_server_bgg_collection(
    username: str,
    fortrade: Optional[bool] = None,
    hasparts: Optional[bool] = None,
    maxbggrating: Optional[float] = None,
    maxplays: Optional[int] = None,
    maxrating: Optional[float] = None,
    minbggrating: Optional[float] = None,
    minplays: Optional[int] = None,
    minrating: Optional[float] = None,
    owned: Optional[bool] = None,
    played: Optional[bool] = None,
    preordered: Optional[bool] = None,
    rated: Optional[bool] = None,
    subtype: Optional[str] = None,
    wanttobuy: Optional[bool] = None,
    wanttoplay: Optional[bool] = None,
    wishlist: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Find the details about a specific user's board game collection on BoardGameGeek (BGG).
    
    Applies filtering based on ownership, ratings, plays, trade status, and other collection flags.
    
    Args:
        username (str): The username of the BoardGameGeek (BGG) user who owns the collection. 
                       Use 'SELF' when referring to the current user.
        fortrade (bool, optional): Filter for games marked for trade.
        hasparts (bool, optional): Filter for games that have spare parts.
        maxbggrating (float, optional): Maximum global BGG rating.
        maxplays (int, optional): Maximum number of plays.
        maxrating (float, optional): Maximum personal rating.
        minbggrating (float, optional): Minimum global BGG rating.
        minplays (int, optional): Minimum number of plays.
        minrating (float, optional): Minimum personal rating.
        owned (bool, optional): Filter for owned games (default: True if no ownership filter specified).
        played (bool, optional): Filter for games with recorded plays.
        preordered (bool, optional): Filter for preordered games.
        rated (bool, optional): Filter for rated games.
        subtype (str, optional): Filter by game subtype ('boardgame' or 'boardgameexpansion').
        wanttobuy (bool, optional): Filter for games user wants to buy.
        wanttoplay (bool, optional): Filter for games user wants to play.
        wishlist (bool, optional): Filter for wishlisted games.
    
    Returns:
        Dict containing:
        - collection_status (str): Status of the query ("success", "no_items_found")
        - message (str): Human-readable result message
        - items (List[Dict]): List of board games with details like id, name, year, status, ratings, plays
        - total_count (int): Number of items returned
    """
    # Validate required input
    if not username:
        return {
            "collection_status": "error",
            "message": "Username is required",
            "items": [],
            "total_count": 0
        }

    # Simulate API call to external service
    api_data = call_external_api("boardgamegeek-api-server-bgg-collection")
    
    # Extract flat data and reconstruct nested structure
    items = []
    
    # Process item 0
    if api_data.get("item_0_id") is not None:
        item_0 = {
            "id": api_data["item_0_id"],
            "name": api_data["item_0_name"],
            "year_published": api_data["item_0_year_published"],
            "status_flags": {
                "owned": api_data["item_0_status_owned"],
                "for_trade": api_data["item_0_status_for_trade"],
                "preordered": api_data["item_0_status_preordered"],
                "want_to_buy": api_data["item_0_status_want_to_buy"],
                "want_to_play": api_data["item_0_status_want_to_play"],
                "wishlist": api_data["item_0_status_wishlist"]
            },
            "personal_rating": api_data["item_0_personal_rating"],
            "bgg_rating": api_data["item_0_bgg_rating"],
            "plays": api_data["item_0_plays"],
            "wishlist_priority": api_data["item_0_wishlist_priority"],
            "has_parts": api_data["item_0_has_parts"]
        }
        items.append(item_0)
    
    # Process item 1
    if api_data.get("item_1_id") is not None:
        item_1 = {
            "id": api_data["item_1_id"],
            "name": api_data["item_1_name"],
            "year_published": api_data["item_1_year_published"],
            "status_flags": {
                "owned": api_data["item_1_status_owned"],
                "for_trade": api_data["item_1_status_for_trade"],
                "preordered": api_data["item_1_status_preordered"],
                "want_to_buy": api_data["item_1_status_want_to_buy"],
                "want_to_play": api_data["item_1_status_want_to_play"],
                "wishlist": api_data["item_1_status_wishlist"]
            },
            "personal_rating": api_data["item_1_personal_rating"],
            "bgg_rating": api_data["item_1_bgg_rating"],
            "plays": api_data["item_1_plays"],
            "wishlist_priority": api_data["item_1_wishlist_priority"],
            "has_parts": api_data["item_1_has_parts"]
        }
        items.append(item_1)
    
    # Apply filtering based on parameters
    filtered_items = []
    for item in items:
        include = True
        
        # Ownership filter
        if owned is not None and item["status_flags"]["owned"] != owned:
            include = False
        
        # Trade filter
        if fortrade is not None and item["status_flags"]["for_trade"] != fortrade:
            include = False
        
        # Preordered filter
        if preordered is not None and item["status_flags"]["preordered"] != preordered:
            include = False
        
        # Want to buy filter
        if wanttobuy is not None and item["status_flags"]["want_to_buy"] != wanttobuy:
            include = False
        
        # Want to play filter
        if wanttoplay is not None and item["status_flags"]["want_to_play"] != wanttoplay:
            include = False
        
        # Wishlist filter
        if wishlist is not None and item["status_flags"]["wishlist"] != wishlist:
            include = False
        
        # Has parts filter
        if hasparts is not None and item["has_parts"] != hasparts:
            include = False
        
        # Played filter
        if played is not None:
            if played and item["plays"] <= 0:
                include = False
            elif not played and item["plays"] > 0:
                include = False
        
        # Rated filter
        if rated is not None:
            has_rating = item["personal_rating"] > 0
            if rated and not has_rating:
                include = False
            elif not rated and has_rating:
                include = False
        
        # Subtype filter (not available in current data model, but could be added)
        # BGG rating filters
        if minbggrating is not None and item["bgg_rating"] < minbggrating:
            include = False
        if maxbggrating is not None and item["bgg_rating"] > maxbggrating:
            include = False
        
        # Personal rating filters
        if minrating is not None and item["personal_rating"] < minrating:
            include = False
        if maxrating is not None and item["personal_rating"] > maxrating:
            include = False
        
        # Plays filters
        if minplays is not None and item["plays"] < minplays:
            include = False
        if maxplays is not None and item["plays"] > maxplays:
            include = False
        
        # Subtype filter (placeholder - would require additional data)
        if subtype is not None:
            # This would require actual subtype data from API
            pass
        
        if include:
            filtered_items.append(item)
    
    # Return result
    return {
        "collection_status": "success" if filtered_items else "no_items_found",
        "message": "Collection retrieved successfully" if filtered_items else "No items found matching the criteria",
        "items": filtered_items,
        "total_count": len(filtered_items)
    }