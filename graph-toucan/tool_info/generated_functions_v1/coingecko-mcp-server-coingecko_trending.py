from typing import Dict, List, Any
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching trending coins data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - trending_coin_0_name (str): Name of the first trending coin
        - trending_coin_0_symbol (str): Symbol of the first trending coin
        - trending_coin_0_price_change_percentage_24h (float): 24h price change % of first coin
        - trending_coin_0_current_price (float): Current price of first coin in USD
        - trending_coin_1_name (str): Name of the second trending coin
        - trending_coin_1_symbol (str): Symbol of the second trending coin
        - trending_coin_1_price_change_percentage_24h (float): 24h price change % of second coin
        - trending_coin_1_current_price (float): Current price of second coin in USD
        - total_count (int): Total number of trending coins returned
        - updated_at (str): ISO 8601 timestamp when data was last updated
        - note (str): Additional message or disclaimer from the API
    """
    return {
        "trending_coin_0_name": "Bitcoin",
        "trending_coin_0_symbol": "btc",
        "trending_coin_0_price_change_percentage_24h": 5.25,
        "trending_coin_0_current_price": 35000.0,
        "trending_coin_1_name": "Ethereum",
        "trending_coin_1_symbol": "eth",
        "trending_coin_1_price_change_percentage_24h": 3.8,
        "trending_coin_1_current_price": 2400.0,
        "total_count": 2,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "note": "Data is for demonstration purposes and not real-time."
    }


def coingecko_mcp_server_coingecko_trending() -> Dict[str, Any]:
    """
    Get trending coins on CoinGecko in the last 24 hours.

    Returns:
        Dict containing:
        - trending_coins (List[Dict]): List of coin objects currently trending, each containing
          name, symbol, market data, and price change information
        - total_count (int): Total number of trending coins returned
        - updated_at (str): ISO 8601 timestamp indicating when the data was last updated
        - note (str): Additional message or disclaimer from the API

    Example:
        {
            "trending_coins": [
                {
                    "name": "Bitcoin",
                    "symbol": "btc",
                    "market_data": {
                        "current_price": 35000.0,
                        "price_change_percentage_24h": 5.25
                    }
                },
                {
                    "name": "Ethereum",
                    "symbol": "eth",
                    "market_data": {
                        "current_price": 2400.0,
                        "price_change_percentage_24h": 3.8
                    }
                }
            ],
            "total_count": 2,
            "updated_at": "2023-11-25T12:34:56.789Z",
            "note": "Data is for demonstration purposes and not real-time."
        }
    """
    # Fetch data from simulated external API
    api_data = call_external_api("coingecko-mcp-server-coingecko_trending")

    # Construct trending coins list from indexed fields
    trending_coins = [
        {
            "name": api_data["trending_coin_0_name"],
            "symbol": api_data["trending_coin_0_symbol"],
            "market_data": {
                "current_price": api_data["trending_coin_0_current_price"],
                "price_change_percentage_24h": api_data["trending_coin_0_price_change_percentage_24h"]
            }
        },
        {
            "name": api_data["trending_coin_1_name"],
            "symbol": api_data["trending_coin_1_symbol"],
            "market_data": {
                "current_price": api_data["trending_coin_1_current_price"],
                "price_change_percentage_24h": api_data["trending_coin_1_price_change_percentage_24h"]
            }
        }
    ]

    # Build final result matching output schema
    result = {
        "trending_coins": trending_coins,
        "total_count": api_data["total_count"],
        "updated_at": api_data["updated_at"],
        "note": api_data["note"]
    }

    return result