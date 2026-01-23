from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching trade amount data from Coinglass API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - symbol (str): Cryptocurrency symbol queried, e.g., 'BTC'
        - granularity (str): Time interval per data point, e.g., '1h'
        - lookback_count (int): Number of data points returned
        - unit (str): Unit of trade amount, typically 'USD'
        - fetched_at (str): ISO 8601 timestamp when data was retrieved
        - trade_amount_data_0_timestamp (str): ISO 8601 timestamp for first record
        - trade_amount_data_0_symbol (str): Symbol for first record
        - trade_amount_data_0_trade_amount_usd (float): Trade volume in USD for first record
        - trade_amount_data_1_timestamp (str): ISO 8601 timestamp for second record
        - trade_amount_data_1_symbol (str): Symbol for second record
        - trade_amount_data_1_trade_amount_usd (float): Trade volume in USD for second record
    """
    now = datetime.utcnow()
    fetched_at = now.isoformat() + "Z"
    
    # Generate two sample timestamps based on granularity
    granularity = "1h"  # default
    minutes_map = {
        "1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30,
        "1h": 60, "4h": 240, "6h": 360, "12h": 720, "24h": 1440,
        "1d": 1440, "1w": 10080
    }
    interval_minutes = minutes_map.get(granularity, 60)
    
    timestamp_1 = (now - timedelta(minutes=interval_minutes * 1)).isoformat() + "Z"
    timestamp_2 = (now - timedelta(minutes=interval_minutes * 2)).isoformat() + "Z"
    
    return {
        "symbol": "BTC",
        "granularity": granularity,
        "lookback_count": 100,
        "unit": "USD",
        "fetched_at": fetched_at,
        "trade_amount_data_0_timestamp": timestamp_1,
        "trade_amount_data_0_symbol": "BTC",
        "trade_amount_data_0_trade_amount_usd": round(random.uniform(1000000, 5000000), 2),
        "trade_amount_data_1_timestamp": timestamp_2,
        "trade_amount_data_1_symbol": "BTC",
        "trade_amount_data_1_trade_amount_usd": round(random.uniform(1000000, 5000000), 2),
    }

def 虚拟币价格查询服务_get_trade_amount(
    symbol: str,
    granularity: Optional[str] = "1h",
    lookback_count: Optional[int] = 100
) -> Dict[str, Any]:
    """
    获取虚拟币的成交额信息 (Coinglass API)
    
    Args:
        symbol (str): 币种符号，例如BTC、ETH（必填）
        granularity (str, optional): K线粒度，默认为'1h'。可选值包括: 
            1m, 3m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 24h, 1d, 1w 等
        lookback_count (int, optional): 需要获取的K线数量，默认100条
    
    Returns:
        Dict containing:
        - trade_amount_data (List[Dict]): List of historical trade amount records with keys:
            'timestamp' (ISO 8601), 'symbol' (str), 'trade_amount_usd' (float)
        - granularity (str): The time interval used for each data point
        - lookback_count (int): Number of data points returned
        - symbol (str): The cryptocurrency symbol queried
        - unit (str): Unit of trade amount, typically 'USD'
        - fetched_at (str): ISO 8601 timestamp when data was retrieved
    
    Raises:
        ValueError: If symbol is empty or invalid
    """
    if not symbol or not symbol.strip():
        raise ValueError("Parameter 'symbol' is required and cannot be empty.")
    
    if lookback_count is None:
        lookback_count = 100
    if lookback_count <= 0:
        raise ValueError("Parameter 'lookback_count' must be a positive integer.")
    
    if granularity is None:
        granularity = "1h"
    
    # Call external API (simulated)
    api_data = call_external_api("虚拟币价格查询服务_get_trade_amount")
    
    # Override with actual input values
    api_data["symbol"] = symbol.upper()
    api_data["granularity"] = granularity
    api_data["lookback_count"] = lookback_count
    
    # Construct trade amount data list from flattened API response
    trade_amount_data = [
        {
            "timestamp": api_data["trade_amount_data_0_timestamp"],
            "symbol": api_data["trade_amount_data_0_symbol"],
            "trade_amount_usd": api_data["trade_amount_data_0_trade_amount_usd"]
        },
        {
            "timestamp": api_data["trade_amount_data_1_timestamp"],
            "symbol": api_data["trade_amount_data_1_symbol"],
            "trade_amount_usd": api_data["trade_amount_data_1_trade_amount_usd"]
        }
    ]
    
    # Generate realistic timestamps based on granularity and lookback count
    # We'll keep only 2 records as per API simulation, but scale timestamps accordingly
    minutes_map = {
        "1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30,
        "1h": 60, "4h": 240, "6h": 360, "12h": 720, "24h": 1440,
        "1d": 1440, "1w": 10080
    }
    interval_minutes = minutes_map.get(granularity, 60)
    now = datetime.utcnow()
    
    # Recalculate timestamps based on actual lookback and granularity
    timestamp_1 = (now - timedelta(minutes=interval_minutes * 1)).isoformat() + "Z"
    timestamp_2 = (now - timedelta(minutes=interval_minutes * 2)).isoformat() + "Z"
    
    # Update timestamps to reflect correct lookback
    trade_amount_data[0]["timestamp"] = timestamp_1
    trade_amount_data[1]["timestamp"] = timestamp_2
    trade_amount_data[0]["symbol"] = symbol.upper()
    trade_amount_data[1]["symbol"] = symbol.upper()
    
    # Return final structured response
    return {
        "trade_amount_data": trade_amount_data,
        "granularity": api_data["granularity"],
        "lookback_count": api_data["lookback_count"],
        "symbol": api_data["symbol"],
        "unit": api_data["unit"],
        "fetched_at": api_data["fetched_at"]
    }