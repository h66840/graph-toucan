from typing import Dict, List, Any, Optional
import time
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching trade volume data from Coinglass API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - symbol (str): Cryptocurrency symbol requested (e.g., BTC)
        - granularity (str): Time interval for each data point (e.g., '1h')
        - lookback_count (int): Number of data points returned
        - exchange (str): Name of the exchange or aggregated source (e.g., 'Aggregate')
        - unit (str): Unit of volume measurement (e.g., 'USD')
        - fetched_at (int): Unix timestamp in milliseconds when data was fetched
        - is_aggregated (bool): Whether volume data is aggregated across exchanges
        - volume_data_0_timestamp (int): First data point timestamp (Unix ms)
        - volume_data_0_volume (float): First data point volume
        - volume_data_0_open (float): First data point open price
        - volume_data_0_close (float): First data point close price
        - volume_data_0_high (float): First data point high price
        - volume_data_0_low (float): First data point low price
        - volume_data_1_timestamp (int): Second data point timestamp (Unix ms)
        - volume_data_1_volume (float): Second data point volume
        - volume_data_1_open (float): Second data point open price
        - volume_data_1_close (float): Second data point close price
        - volume_data_1_high (float): Second data point high price
        - volume_data_1_low (float): Second data point low price
    """
    current_time_ms = int(time.time() * 1000)
    interval_ms = {
        '1m': 60 * 1000,
        '3m': 3 * 60 * 1000,
        '5m': 5 * 60 * 1000,
        '15m': 15 * 60 * 1000,
        '30m': 30 * 60 * 1000,
        '1h': 60 * 60 * 1000,
        '4h': 4 * 60 * 60 * 1000,
        '6h': 6 * 60 * 60 * 1000,
        '12h': 12 * 60 * 60 * 1000,
        '24h': 24 * 60 * 60 * 1000,
        '1d': 24 * 60 * 60 * 1000,
        '1w': 7 * 24 * 60 * 60 * 1000,
    }.get('1h', 60 * 60 * 1000)  # default to 1h

    return {
        "symbol": "BTC",
        "granularity": "1h",
        "lookback_count": 2,
        "exchange": "Aggregate",
        "unit": "USD",
        "fetched_at": current_time_ms,
        "is_aggregated": True,
        "volume_data_0_timestamp": current_time_ms - interval_ms,
        "volume_data_0_volume": round(random.uniform(50000000, 200000000), 2),
        "volume_data_0_open": round(random.uniform(30000, 70000), 2),
        "volume_data_0_close": round(random.uniform(30000, 70000), 2),
        "volume_data_0_high": round(random.uniform(30000, 70000), 2),
        "volume_data_0_low": round(random.uniform(30000, 70000), 2),
        "volume_data_1_timestamp": current_time_ms,
        "volume_data_1_volume": round(random.uniform(50000000, 200000000), 2),
        "volume_data_1_open": round(random.uniform(30000, 70000), 2),
        "volume_data_1_close": round(random.uniform(30000, 70000), 2),
        "volume_data_1_high": round(random.uniform(30000, 70000), 2),
        "volume_data_1_low": round(random.uniform(30000, 70000), 2),
    }


def 虚拟币价格查询服务_get_trade_volume(
    symbol: str,
    granularity: Optional[str] = "1h",
    lookback_count: Optional[int] = 100
) -> Dict[str, Any]:
    """
    获取虚拟币合约的成交量信息 (Coinglass API)

    Args:
        symbol (str): 币种符号，例如BTC、ETH（必填）
        granularity (str, optional): K线粒度，默认1h (可选: 1m, 3m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 24h, 1d, 1w等)
        lookback_count (int, optional): 需要获取的K线数量，默认100条

    Returns:
        Dict containing:
        - volume_data (List[Dict]): List of candlestick-style volume entries with timestamp, volume, and price data
        - symbol (str): The cryptocurrency symbol requested
        - granularity (str): The time interval for each data point
        - lookback_count (int): Number of data points returned
        - exchange (str): Name of the exchange or aggregated source
        - unit (str): Unit of volume measurement
        - fetched_at (int): Unix timestamp in milliseconds when the data was fetched
        - is_aggregated (bool): Whether the volume data is aggregated across multiple exchanges
    """
    if not symbol:
        raise ValueError("Parameter 'symbol' is required and cannot be empty.")
    
    if lookback_count is None:
        lookback_count = 100
    if granularity is None:
        granularity = "1h"
    
    if lookback_count <= 0:
        raise ValueError("lookback_count must be a positive integer.")
    
    # Call external API to get flattened data
    api_data = call_external_api("虚拟币价格查询服务_get_trade_volume")
    
    # Construct volume_data list from indexed fields
    volume_data = [
        {
            "timestamp": api_data["volume_data_0_timestamp"],
            "volume": api_data["volume_data_0_volume"],
            "open": api_data["volume_data_0_open"],
            "close": api_data["volume_data_0_close"],
            "high": api_data["volume_data_0_high"],
            "low": api_data["volume_data_0_low"]
        },
        {
            "timestamp": api_data["volume_data_1_timestamp"],
            "volume": api_data["volume_data_1_volume"],
            "open": api_data["volume_data_1_open"],
            "close": api_data["volume_data_1_close"],
            "high": api_data["volume_data_1_high"],
            "low": api_data["volume_data_1_low"]
        }
    ]
    
    # Limit volume_data to requested lookback_count (simulate truncation)
    effective_count = min(lookback_count, len(volume_data))
    volume_data = volume_data[:effective_count]
    
    # Build final result structure
    result = {
        "volume_data": volume_data,
        "symbol": symbol,
        "granularity": granularity,
        "lookback_count": effective_count,
        "exchange": api_data["exchange"],
        "unit": api_data["unit"],
        "fetched_at": api_data["fetched_at"],
        "is_aggregated": api_data["is_aggregated"]
    }
    
    return result