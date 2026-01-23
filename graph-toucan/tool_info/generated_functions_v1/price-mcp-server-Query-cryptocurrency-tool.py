from typing import Dict, List, Any
import random
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cryptocurrency price data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - code (str): Response code, e.g., "200"
        - msg (str): Message describing result, e.g., "success"
        - requestTime (int): Timestamp in milliseconds when request was processed
        - data_0_symbol (str): First cryptocurrency symbol
        - data_0_price_usd (float): First cryptocurrency price in USD
        - data_0_volume_usd_24h (float): First cryptocurrency 24h trading volume in USD
        - data_0_change_percent_24h (float): First cryptocurrency 24h price change percentage
        - data_0_bid_usd (float): First cryptocurrency current bid price in USD
        - data_0_ask_usd (float): First cryptocurrency current ask price in USD
        - data_1_symbol (str): Second cryptocurrency symbol
        - data_1_price_usd (float): Second cryptocurrency price in USD
        - data_1_volume_usd_24h (float): Second cryptocurrency 24h trading volume in USD
        - data_1_change_percent_24h (float): Second cryptocurrency 24h price change percentage
        - data_1_bid_usd (float): Second cryptocurrency current bid price in USD
        - data_1_ask_usd (float): Second cryptocurrency current ask price in USD
    """
    # Simulate realistic cryptocurrency data
    symbols = ["BTC", "ETH", "ADA", "SOL", "XRP", "DOT", "DOGE", "AVAX"]
    selected_symbol = random.choice(symbols)
    
    base_price = {
        "BTC": 40000.0,
        "ETH": 2500.0,
        "ADA": 0.5,
        "SOL": 100.0,
        "XRP": 0.6,
        "DOT": 7.0,
        "DOGE": 0.08,
        "AVAX": 30.0
    }
    
    price = base_price[selected_symbol] * (1 + random.uniform(-0.1, 0.1))
    volume = price * random.uniform(1000000, 100000000)
    change_percent = random.uniform(-10, 10)
    bid = price * 0.995
    ask = price * 1.005
    
    # Generate second symbol (different from first)
    second_symbol = selected_symbol
    while second_symbol == selected_symbol:
        second_symbol = random.choice(symbols)
    
    second_price = base_price[second_symbol] * (1 + random.uniform(-0.1, 0.1))
    second_volume = second_price * random.uniform(1000000, 100000000)
    second_change_percent = random.uniform(-10, 10)
    second_bid = second_price * 0.995
    second_ask = second_price * 1.005
    
    return {
        "code": "200",
        "msg": "success",
        "requestTime": int(time.time() * 1000),
        "data_0_symbol": selected_symbol,
        "data_0_price_usd": round(price, 6),
        "data_0_volume_usd_24h": round(volume, 2),
        "data_0_change_percent_24h": round(change_percent, 4),
        "data_0_bid_usd": round(bid, 6),
        "data_0_ask_usd": round(ask, 6),
        "data_1_symbol": second_symbol,
        "data_1_price_usd": round(second_price, 6),
        "data_1_volume_usd_24h": round(second_volume, 2),
        "data_1_change_percent_24h": round(second_change_percent, 4),
        "data_1_bid_usd": round(second_bid, 6),
        "data_1_ask_usd": round(second_ask, 6),
    }


def price_mcp_server_Query_cryptocurrency_tool(symbol: str) -> Dict[str, Any]:
    """
    Query the current cryptocurrency prices.
    
    Args:
        symbol (str): Cryptocurrency symbol to query (e.g., "BTC", "ETH")
    
    Returns:
        Dict containing:
        - code (str): Response code indicating success or error status
        - msg (str): Message describing the result of the request
        - requestTime (int): Timestamp in milliseconds when the request was processed
        - data (List[Dict]): List of cryptocurrency price data entries with:
            - symbol (str): Cryptocurrency symbol
            - price_usd (float): Current price in USD
            - volume_usd_24h (float): 24-hour trading volume in USD
            - change_percent_24h (float): 24-hour price change percentage
            - bid_usd (float): Current bid price in USD
            - ask_usd (float): Current ask price in USD
    """
    # Input validation
    if not symbol or not isinstance(symbol, str):
        return {
            "code": "400",
            "msg": "Invalid input: symbol must be a non-empty string",
            "requestTime": int(time.time() * 1000),
            "data": []
        }
    
    # Normalize symbol to uppercase
    symbol = symbol.strip().upper()
    
    # Validate symbol format (simple validation)
    valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if not all(c in valid_chars for c in symbol) or len(symbol) < 2 or len(symbol) > 5:
        return {
            "code": "400",
            "msg": f"Invalid symbol format: {symbol}",
            "requestTime": int(time.time() * 1000),
            "data": []
        }
    
    try:
        # Call external API (simulated)
        api_data = call_external_api("price-mcp-server-Query cryptocurrency tool")
        
        # Construct the nested output structure
        data_entries = [
            {
                "symbol": api_data["data_0_symbol"],
                "price_usd": api_data["data_0_price_usd"],
                "volume_usd_24h": api_data["data_0_volume_usd_24h"],
                "change_percent_24h": api_data["data_0_change_percent_24h"],
                "bid_usd": api_data["data_0_bid_usd"],
                "ask_usd": api_data["data_0_ask_usd"]
            },
            {
                "symbol": api_data["data_1_symbol"],
                "price_usd": api_data["data_1_price_usd"],
                "volume_usd_24h": api_data["data_1_volume_usd_24h"],
                "change_percent_24h": api_data["data_1_change_percent_24h"],
                "bid_usd": api_data["data_1_bid_usd"],
                "ask_usd": api_data["data_1_ask_usd"]
            }
        ]
        
        # Filter data if symbol is specified (return only matching entries)
        if symbol:
            filtered_data = [entry for entry in data_entries if entry["symbol"] == symbol]
            if not filtered_data:
                # If no match found, return both entries but with warning
                return {
                    "code": "200",
                    "msg": f"No data found for symbol {symbol}, returning other available cryptocurrencies",
                    "requestTime": api_data["requestTime"],
                    "data": data_entries
                }
            data_entries = filtered_data
        
        return {
            "code": api_data["code"],
            "msg": api_data["msg"],
            "requestTime": api_data["requestTime"],
            "data": data_entries
        }
        
    except Exception as e:
        return {
            "code": "500",
            "msg": f"Internal error occurred: {str(e)}",
            "requestTime": int(time.time() * 1000),
            "data": []
        }