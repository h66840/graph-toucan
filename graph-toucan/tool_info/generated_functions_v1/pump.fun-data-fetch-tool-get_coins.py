from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for pump.fun coin data.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - coin_0_id (str): ID of the first coin
        - coin_0_name (str): Name of the first coin
        - coin_0_symbol (str): Symbol of the first coin
        - coin_0_market_cap (float): Market cap of the first coin
        - coin_0_created_timestamp (str): Creation timestamp of the first coin
        - coin_0_last_trade_timestamp (str): Last trade timestamp of the first coin
        - coin_0_last_reply (str): Last reply timestamp of the first coin
        - coin_0_is_nsfw (bool): Whether the first coin is NSFW
        - coin_0_creator_address (str): Creator address of the first coin
        - coin_0_image_url (str): Image URL of the first coin
        - coin_0_description (str): Description of the first coin
        - coin_1_id (str): ID of the second coin
        - coin_1_name (str): Name of the second coin
        - coin_1_symbol (str): Symbol of the second coin
        - coin_1_market_cap (float): Market cap of the second coin
        - coin_1_created_timestamp (str): Creation timestamp of the second coin
        - coin_1_last_trade_timestamp (str): Last trade timestamp of the second coin
        - coin_1_last_reply (str): Last reply timestamp of the second coin
        - coin_1_is_nsfw (bool): Whether the second coin is NSFW
        - coin_1_creator_address (str): Creator address of the second coin
        - coin_1_image_url (str): Image URL of the second coin
        - coin_1_description (str): Description of the second coin
        - total_count (int): Total number of coins available
        - limit (int): Number of coins returned
        - offset (int): Starting position of results
        - sort (str): Field used for sorting
        - order (str): Direction of sorting ("ASC" or "DESC")
        - has_more (bool): Whether more coins are available
        - filters_applied_includeNsfw (bool): Whether NSFW coins were included in filters
    """
    return {
        "coin_0_id": "coin123",
        "coin_0_name": "Solana Monkey",
        "coin_0_symbol": "SMONK",
        "coin_0_market_cap": 250000.0,
        "coin_0_created_timestamp": "2023-10-01T12:00:00Z",
        "coin_0_last_trade_timestamp": "2023-10-05T14:30:00Z",
        "coin_0_last_reply": "2023-10-04T10:15:00Z",
        "coin_0_is_nsfw": False,
        "coin_0_creator_address": "sol123abc...",
        "coin_0_image_url": "https://example.com/smonk.png",
        "coin_0_description": "A fun Solana-based monkey token.",
        
        "coin_1_id": "coin456",
        "coin_1_name": "Degenerate Frog",
        "coin_1_symbol": "FROG",
        "coin_1_market_cap": 1800000.5,
        "coin_1_created_timestamp": "2023-09-28T08:20:00Z",
        "coin_1_last_trade_timestamp": "2023-10-06T09:45:00Z",
        "coin_1_last_reply": "2023-10-05T16:20:00Z",
        "coin_1_is_nsfw": True,
        "coin_1_creator_address": "sol456def...",
        "coin_1_image_url": "https://example.com/frog.png",
        "coin_1_description": "Ribbiting gains guaranteed.",
        
        "total_count": 1500,
        "limit": 2,
        "offset": 0,
        "sort": "market_cap",
        "order": "DESC",
        "has_more": True,
        "filters_applied_includeNsfw": True
    }

def pump_fun_data_fetch_tool_get_coins(
    includeNsfw: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    order: Optional[str] = None,
    sort: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetches a list of coins from pump.fun with optional filtering and sorting.
    
    Args:
        includeNsfw (bool, optional): Include NSFW coins (default: True)
        limit (int, optional): Number of coins to return (default: 24)
        offset (int, optional): Starting position for pagination (default: 0)
        order (str, optional): Sort order, either "ASC" or "DESC" (default: None)
        sort (str, optional): Field to sort by, e.g., "market_cap", "created_timestamp" (default: None)
    
    Returns:
        Dict containing:
        - coins (List[Dict]): List of coin objects with detailed info
        - total_count (int): Total number of matching coins
        - limit (int): Number of coins returned
        - offset (int): Starting offset
        - sort (str): Field used for sorting
        - order (str): Sort direction
        - has_more (bool): Whether more results exist
        - filters_applied (Dict): Applied filter summary
    
    Raises:
        ValueError: If order is not "ASC" or "DESC", or if limit/offset are negative
    """
    # Set defaults
    if includeNsfw is None:
        includeNsfw = True
    if limit is None:
        limit = 24
    if offset is None:
        offset = 0
    if order is not None and order not in ["ASC", "DESC"]:
        raise ValueError("order must be either 'ASC' or 'DESC'")
    if limit < 0:
        raise ValueError("limit must be non-negative")
    if offset < 0:
        raise ValueError("offset must be non-negative")

    # Call external API (simulated)
    api_data = call_external_api("pump.fun-data-fetch-tool-get_coins")
    
    # Construct coins list from indexed fields
    coins = []
    for i in range(2):  # We have two coins from the API mock
        coin_id_key = f"coin_{i}_id"
        if coin_id_key not in api_data:
            continue
            
        coin = {
            "id": api_data[f"coin_{i}_id"],
            "name": api_data[f"coin_{i}_name"],
            "symbol": api_data[f"coin_{i}_symbol"],
            "market_cap": api_data[f"coin_{i}_market_cap"],
            "created_timestamp": api_data[f"coin_{i}_created_timestamp"],
            "last_trade_timestamp": api_data[f"coin_{i}_last_trade_timestamp"],
            "last_reply": api_data[f"coin_{i}_last_reply"],
            "is_nsfw": api_data[f"coin_{i}_is_nsfw"],
            "creator_address": api_data[f"coin_{i}_creator_address"],
            "image_url": api_data[f"coin_{i}_image_url"],
            "description": api_data[f"coin_{i}_description"]
        }
        # Apply NSFW filter if needed
        if not includeNsfw and coin["is_nsfw"]:
            continue
        coins.append(coin)
    
    # Apply limit and offset manually
    start_idx = min(offset, len(coins))
    end_idx = min(offset + limit, len(coins))
    paginated_coins = coins[start_idx:end_idx]
    
    # Determine actual sort and order used
    actual_sort = sort if sort in ["market_cap", "last_trade_timestamp", "created_timestamp", "last_reply"] else "market_cap"
    actual_order = order if order in ["ASC", "DESC"] else "DESC"
    
    # Build result
    result = {
        "coins": paginated_coins,
        "total_count": api_data["total_count"],
        "limit": len(paginated_coins),
        "offset": offset,
        "sort": actual_sort,
        "order": actual_order,
        "has_more": (offset + limit) < api_data["total_count"],
        "filters_applied": {
            "includeNsfw": includeNsfw
        }
    }
    
    return result