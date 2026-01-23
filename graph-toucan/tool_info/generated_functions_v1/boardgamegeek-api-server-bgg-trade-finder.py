from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for boardgamegeek trade finder.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - user1_username (str): Username of the first user (owner of collection)
        - user2_username (str): Username of the second user (owner of wishlist)
        - user1_has_wanted_0_game_id (int): Game ID of first wanted game owned by user1
        - user1_has_wanted_0_name (str): Name of first wanted game owned by user1
        - user1_has_wanted_0_year_published (int): Year published of first wanted game
        - user1_has_wanted_0_for_trade (bool): Whether first game is for trade
        - user1_has_wanted_0_want_in_trade (bool): Whether user2 wants first game in trade
        - user1_has_wanted_1_game_id (int): Game ID of second wanted game owned by user1
        - user1_has_wanted_1_name (str): Name of second wanted game owned by user1
        - user1_has_wanted_1_year_published (int): Year published of second wanted game
        - user1_has_wanted_1_for_trade (bool): Whether second game is for trade
        - user1_has_wanted_1_want_in_trade (bool): Whether user2 wants second game in trade
        - user2_wishlist_0_game_id (int): Game ID of first game in user2's wishlist
        - user2_wishlist_0_name (str): Name of first game in user2's wishlist
        - user2_wishlist_0_year_published (int): Year published of first wishlist game
        - user2_wishlist_0_for_trade (bool): Whether first wishlist game is for trade
        - user2_wishlist_0_want_in_trade (bool): Whether user2 wants first wishlist game in trade
        - user2_wishlist_1_game_id (int): Game ID of second game in user2's wishlist
        - user2_wishlist_1_name (str): Name of second game in user2's wishlist
        - user2_wishlist_1_year_published (int): Year published of second wishlist game
        - user2_wishlist_1_for_trade (bool): Whether second wishlist game is for trade
        - user2_wishlist_1_want_in_trade (bool): Whether user2 wants second wishlist game in trade
        - user1_has_wanted_count (int): Count of games owned by user1 that are wanted by user2
        - user2_wishlist_count (int): Total count of games in user2's wishlist
        - has_trade_opportunity (bool): Whether there is at least one trade opportunity
    """
    return {
        "user1_username": "SELF" if tool_name == "boardgamegeek-api-server-bgg-trade-finder" else "user1_test",
        "user2_username": "user2_test",
        "user1_has_wanted_0_game_id": 12345,
        "user1_has_wanted_0_name": "Pandemic",
        "user1_has_wanted_0_year_published": 2008,
        "user1_has_wanted_0_for_trade": True,
        "user1_has_wanted_0_want_in_trade": True,
        "user1_has_wanted_1_game_id": 67890,
        "user1_has_wanted_1_name": "Catan",
        "user1_has_wanted_1_year_published": 1995,
        "user1_has_wanted_1_for_trade": True,
        "user1_has_wanted_1_want_in_trade": True,
        "user2_wishlist_0_game_id": 12345,
        "user2_wishlist_0_name": "Pandemic",
        "user2_wishlist_0_year_published": 2008,
        "user2_wishlist_0_for_trade": True,
        "user2_wishlist_0_want_in_trade": True,
        "user2_wishlist_1_game_id": 54321,
        "user2_wishlist_1_name": "Ticket to Ride",
        "user2_wishlist_1_year_published": 2004,
        "user2_wishlist_1_for_trade": True,
        "user2_wishlist_1_want_in_trade": True,
        "user1_has_wanted_count": 2,
        "user2_wishlist_count": 2,
        "has_trade_opportunity": True
    }

def boardgamegeek_api_server_bgg_trade_finder(user1: str, user2: str) -> Dict[str, Any]:
    """
    Find what games user1 owns that user2 has on their wishlist. Shows potential trading opportunities.

    Args:
        user1 (str): BGG username whose collection will be checked. Use 'SELF' for current user.
        user2 (str): BGG username whose wishlist will be checked against user1's collection.

    Returns:
        Dict containing:
        - user1_username (str): username of the first user (owner of the collection)
        - user2_username (str): username of the second user (owner of the wishlist)
        - user1_has_wanted (List[Dict]): list of games owned by user1 that are wanted by user2
        - user2_wishlist (List[Dict] or None): list of games in user2's wishlist
        - summary (Dict): summary statistics with user1_has_wanted_count, user2_wishlist_count, has_trade_opportunity

    Raises:
        ValueError: If user1 or user2 is not provided
    """
    if not user1:
        raise ValueError("user1 is required")
    if not user2:
        raise ValueError("user2 is required")

    # Call external API to get data (simulated)
    api_data = call_external_api("boardgamegeek-api-server-bgg-trade-finder")

    # Construct user1_has_wanted list
    user1_has_wanted = [
        {
            "game_id": api_data["user1_has_wanted_0_game_id"],
            "name": api_data["user1_has_wanted_0_name"],
            "year_published": api_data["user1_has_wanted_0_year_published"],
            "for_trade": api_data["user1_has_wanted_0_for_trade"],
            "want_in_trade": api_data["user1_has_wanted_0_want_in_trade"]
        },
        {
            "game_id": api_data["user1_has_wanted_1_game_id"],
            "name": api_data["user1_has_wanted_1_name"],
            "year_published": api_data["user1_has_wanted_1_year_published"],
            "for_trade": api_data["user1_has_wanted_1_for_trade"],
            "want_in_trade": api_data["user1_has_wanted_1_want_in_trade"]
        }
    ]

    # Construct user2_wishlist list
    user2_wishlist = [
        {
            "game_id": api_data["user2_wishlist_0_game_id"],
            "name": api_data["user2_wishlist_0_name"],
            "year_published": api_data["user2_wishlist_0_year_published"],
            "for_trade": api_data["user2_wishlist_0_for_trade"],
            "want_in_trade": api_data["user2_wishlist_0_want_in_trade"]
        },
        {
            "game_id": api_data["user2_wishlist_1_game_id"],
            "name": api_data["user2_wishlist_1_name"],
            "year_published": api_data["user2_wishlist_1_year_published"],
            "for_trade": api_data["user2_wishlist_1_for_trade"],
            "want_in_trade": api_data["user2_wishlist_1_want_in_trade"]
        }
    ]

    # Construct summary
    summary = {
        "user1_has_wanted_count": api_data["user1_has_wanted_count"],
        "user2_wishlist_count": api_data["user2_wishlist_count"],
        "has_trade_opportunity": api_data["has_trade_opportunity"]
    }

    # Return final structured result
    return {
        "user1_username": user1,
        "user2_username": user2,
        "user1_has_wanted": user1_has_wanted,
        "user2_wishlist": user2_wishlist,
        "summary": summary
    }