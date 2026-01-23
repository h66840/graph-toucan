from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for coin search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_name (str): Name of the first matching coin
        - result_0_symbol (str): Symbol of the first coin (e.g., BTC)
        - result_0_price_usd (float): Current price in USD for first coin
        - result_0_market_cap_usd (float): Market cap in USD for first coin
        - result_0_volume_24h_usd (float): 24h trading volume in USD for first coin
        - result_0_change_24h_percent (float): 24h price change percentage for first coin
        - result_0_last_updated (str): Last updated timestamp for first coin (ISO format)
        - result_1_name (str): Name of the second matching coin
        - result_1_symbol (str): Symbol of the second coin (e.g., ETH)
        - result_1_price_usd (float): Current price in USD for second coin
        - result_1_market_cap_usd (float): Market cap in USD for second coin
        - result_1_volume_24h_usd (float): 24h trading volume in USD for second coin
        - result_1_change_24h_percent (float): 24h price change percentage for second coin
        - result_1_last_updated (str): Last updated timestamp for second coin (ISO format)
        - total_count (int): Total number of coins matching the query
        - query_used (str): The actual search keyword used
        - timestamp (str): ISO 8601 timestamp when result was generated
        - metadata_limit (int): Limit applied to results
        - metadata_source (str): Source of price data
        - metadata_currency_base (str): Base currency for prices (e.g., USD)
    """
    return {
        "result_0_name": "Bitcoin",
        "result_0_symbol": "BTC",
        "result_0_price_usd": 43520.65,
        "result_0_market_cap_usd": 857200000000.0,
        "result_0_volume_24h_usd": 24500000000.0,
        "result_0_change_24h_percent": 2.45,
        "result_0_last_updated": "2023-10-05T12:34:56Z",
        "result_1_name": "Bitcoin Cash",
        "result_1_symbol": "BCH",
        "result_1_price_usd": 320.15,
        "result_1_market_cap_usd": 6120000000.0,
        "result_1_volume_24h_usd": 320000000.0,
        "result_1_change_24h_percent": -1.23,
        "result_1_last_updated": "2023-10-05T12:34:50Z",
        "total_count": 2,
        "query_used": "bitcoin",
        "timestamp": "2023-10-05T12:35:00Z",
        "metadata_limit": 10,
        "metadata_source": "CoinGecko",
        "metadata_currency_base": "USD"
    }

def 虚拟币价格查询服务_search_coins(query: str, limit: Optional[int] = 10) -> Dict[str, Any]:
    """
    搜索虚拟币信息。

    Args:
        query (str): 搜索关键词，用于匹配虚拟币名称或符号
        limit (int, optional): 返回结果数量上限，默认为10

    Returns:
        Dict containing:
        - results (List[Dict]): List of coin search results with keys:
            - name (str): Coin name
            - symbol (str): Coin symbol
            - price_usd (float): Current price in USD
            - market_cap_usd (float): Market capitalization in USD
            - volume_24h_usd (float): 24-hour trading volume in USD
            - change_24h_percent (float): 24-hour price change percentage
            - last_updated (str): ISO 8601 timestamp of last update
        - total_count (int): Total number of matching coins found
        - query_used (str): The actual search keyword used
        - timestamp (str): ISO 8601 timestamp when the search result was generated
        - metadata (Dict): Additional metadata including:
            - limit (int): Applied result limit
            - source (str): Data source name
            - currency_base (str): Base currency for pricing (e.g., USD)

    Raises:
        ValueError: If query is empty or None
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")

    # Normalize query
    normalized_query = query.strip()

    # Call external API (simulated)
    api_data = call_external_api("虚拟币价格查询服务_search_coins")

    # Construct results list from indexed flat fields
    results = []
    for i in range(2):  # We have two results from the API mock
        name_key = f"result_{i}_name"
        if name_key not in api_data or api_data[name_key] is None:
            continue
        if len(results) >= (limit or 10):
            break

        result = {
            "name": api_data[f"result_{i}_name"],
            "symbol": api_data[f"result_{i}_symbol"],
            "price_usd": api_data[f"result_{i}_price_usd"],
            "market_cap_usd": api_data[f"result_{i}_market_cap_usd"],
            "volume_24h_usd": api_data[f"result_{i}_volume_24h_usd"],
            "change_24h_percent": api_data[f"result_{i}_change_24h_percent"],
            "last_updated": api_data[f"result_{i}_last_updated"]
        }
        results.append(result)

    # Construct metadata
    metadata = {
        "limit": api_data["metadata_limit"],
        "source": api_data["metadata_source"],
        "currency_base": api_data["metadata_currency_base"]
    }

    # Final result structure
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "query_used": api_data["query_used"],
        "timestamp": api_data["timestamp"],
        "metadata": metadata
    }