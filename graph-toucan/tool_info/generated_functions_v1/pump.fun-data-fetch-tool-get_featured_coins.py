from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for pump.fun featured coins.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - coin_0_name (str): Name of the first featured coin
        - coin_0_symbol (str): Symbol of the first featured coin
        - coin_0_price (float): Current price of the first coin in USD
        - coin_0_market_cap (float): Market cap of the first coin in USD
        - coin_0_created_at (int): Unix timestamp when the first coin was created
        - coin_0_image_url (str): URL to the image/logo of the first coin
        - coin_0_twitter (str): Twitter handle of the first coin
        - coin_0_website (str): Website URL of the first coin
        - coin_1_name (str): Name of the second featured coin
        - coin_1_symbol (str): Symbol of the second featured coin
        - coin_1_price (float): Current price of the second coin in USD
        - coin_1_market_cap (float): Market cap of the second coin in USD
        - coin_1_created_at (int): Unix timestamp when the second coin was created
        - coin_1_image_url (str): URL to the image/logo of the second coin
        - coin_1_twitter (str): Twitter handle of the second coin
        - coin_1_website (str): Website URL of the second coin
        - total_count (int): Total number of featured coins available
        - has_more (bool): Whether more coins are available beyond current page
        - pagination_offset (int): Current pagination offset
        - pagination_limit (int): Current pagination limit
        - pagination_current_page (int): Current page number
        - filters_applied_includeNsfw (bool): Whether NSFW coins were included in results
    """
    return {
        "coin_0_name": "Solana Monkey",
        "coin_0_symbol": "SMONKEY",
        "coin_0_price": 0.45,
        "coin_0_market_cap": 4500000.0,
        "coin_0_created_at": 1700000000,
        "coin_0_image_url": "https://example.com/smonkey.png",
        "coin_0_twitter": "@SolanaMonkey",
        "coin_0_website": "https://solamonkey.example.com",
        "coin_1_name": "Pump Fun Token",
        "coin_1_symbol": "PUMP",
        "coin_1_price": 1.23,
        "coin_1_market_cap": 12300000.0,
        "coin_1_created_at": 1700000100,
        "coin_1_image_url": "https://example.com/pump.png",
        "coin_1_twitter": "@PumpFunToken",
        "coin_1_website": "https://pumpfun.example.com",
        "total_count": 150,
        "has_more": True,
        "pagination_offset": 0,
        "pagination_limit": 24,
        "pagination_current_page": 1,
        "filters_applied_includeNsfw": True
    }

def pump_fun_data_fetch_tool_get_featured_coins(
    includeNsfw: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get a list of featured coins from pump.fun.
    
    Args:
        includeNsfw (Optional[bool]): Include NSFW coins (default: True)
        limit (Optional[int]): The number of coins to return (default: 24)
        offset (Optional[int]): The offset to start from (default: 0)
    
    Returns:
        Dict containing:
        - coins (List[Dict]): List of featured coin objects with name, symbol, price,
          market cap, creation time, and metadata like image URL and social links
        - total_count (int): Total number of featured coins available
        - has_more (bool): Indicates if more coins are available beyond current offset and limit
        - pagination (Dict): Pagination metadata including offset, limit, and current_page
        - filters_applied (Dict): Information about filters applied, such as includeNsfw status
    """
    # Set default values
    if includeNsfw is None:
        includeNsfw = True
    if limit is None:
        limit = 24
    if offset is None:
        offset = 0
    
    # Validate inputs
    if limit < 1:
        raise ValueError("limit must be a positive integer")
    if offset < 0:
        raise ValueError("offset must be a non-negative integer")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("pump.fun-data-fetch-tool-get_featured_coins")
    
    # Construct coins list from indexed fields
    coins = [
        {
            "name": api_data["coin_0_name"],
            "symbol": api_data["coin_0_symbol"],
            "price": api_data["coin_0_price"],
            "market_cap": api_data["coin_0_market_cap"],
            "created_at": api_data["coin_0_created_at"],
            "metadata": {
                "image_url": api_data["coin_0_image_url"],
                "social": {
                    "twitter": api_data["coin_0_twitter"],
                    "website": api_data["coin_0_website"]
                }
            }
        },
        {
            "name": api_data["coin_1_name"],
            "symbol": api_data["coin_1_symbol"],
            "price": api_data["coin_1_price"],
            "market_cap": api_data["coin_1_market_cap"],
            "created_at": api_data["coin_1_created_at"],
            "metadata": {
                "image_url": api_data["coin_1_image_url"],
                "social": {
                    "twitter": api_data["coin_1_twitter"],
                    "website": api_data["coin_1_website"]
                }
            }
        }
    ]
    
    # Apply limit (simulate limiting results)
    coins = coins[:limit]
    
    # Construct result according to output schema
    result = {
        "coins": coins,
        "total_count": api_data["total_count"],
        "has_more": api_data["has_more"],
        "pagination": {
            "offset": api_data["pagination_offset"],
            "limit": api_data["pagination_limit"],
            "current_page": api_data["pagination_current_page"]
        },
        "filters_applied": {
            "includeNsfw": api_data["filters_applied_includeNsfw"]
        }
    }
    
    return result