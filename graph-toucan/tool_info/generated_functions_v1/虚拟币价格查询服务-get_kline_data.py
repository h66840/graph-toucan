from typing import Dict, List, Any, Optional
import datetime
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching K-line data from external API (Coinglass).

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - symbol (str): The cryptocurrency symbol (e.g., BTC)
        - granularity (str): Time interval of each K-line (e.g., 1h)
        - lookback_count (int): Number of K-line periods returned
        - exchange (str): Name of the exchange or data source (e.g., Binance)
        - timestamp_range_start (int): Start timestamp in milliseconds
        - timestamp_range_end (int): End timestamp in milliseconds
        - kline_0_timestamp (int): Timestamp of first K-line point
        - kline_0_open (float): Open price of first K-line
        - kline_0_high (float): High price of first K-line
        - kline_0_low (float): Low price of first K-line
        - kline_0_close (float): Close price of first K-line
        - kline_0_volume (float): Volume of first K-line
        - kline_1_timestamp (int): Timestamp of second K-line point
        - kline_1_open (float): Open price of second K-line
        - kline_1_high (float): High price of second K-line
        - kline_1_low (float): Low price of second K-line
        - kline_1_close (float): Close price of second K-line
        - kline_1_volume (float): Volume of second K-line
    """
    now = int(datetime.datetime.now().timestamp() * 1000)
    one_hour_ms = 60 * 60 * 1000
    granularity_ms = one_hour_ms  # default to 1h
    if "1m" in tool_name:
        granularity_ms = 60 * 1000
    elif "5m" in tool_name:
        granularity_ms = 5 * 60 * 1000
    elif "15m" in tool_name:
        granularity_ms = 15 * 60 * 1000
    elif "30m" in tool_name:
        granularity_ms = 30 * 60 * 1000
    elif "4h" in tool_name:
        granularity_ms = 4 * 60 * 60 * 1000
    elif "1d" in tool_name:
        granularity_ms = 24 * 60 * 60 * 1000

    lookback_count = 100
    start_time = now - lookback_count * granularity_ms

    base_price = 50000.0 if "BTC" in tool_name else 3000.0

    return {
        "symbol": "BTC",
        "granularity": "1h",
        "lookback_count": lookback_count,
        "exchange": "Binance",
        "timestamp_range_start": start_time,
        "timestamp_range_end": now,
        "kline_0_timestamp": now - 1 * granularity_ms,
        "kline_0_open": round(base_price + random.uniform(-500, 500), 2),
        "kline_0_high": round(base_price + random.uniform(0, 500), 2),
        "kline_0_low": round(base_price - random.uniform(0, 500), 2),
        "kline_0_close": round(base_price + random.uniform(-500, 500), 2),
        "kline_0_volume": round(random.uniform(100, 1000), 2),
        "kline_1_timestamp": now - 2 * granularity_ms,
        "kline_1_open": round(base_price + random.uniform(-500, 500), 2),
        "kline_1_high": round(base_price + random.uniform(0, 500), 2),
        "kline_1_low": round(base_price - random.uniform(0, 500), 2),
        "kline_1_close": round(base_price + random.uniform(-500, 500), 2),
        "kline_1_volume": round(random.uniform(100, 1000), 2),
    }


def 虚拟币价格查询服务_get_kline_data(
    symbol: str, granularity: Optional[str] = "1h", lookback_count: Optional[int] = 100
) -> Dict[str, Any]:
    """
    获取虚拟币合约的K线数据 (模拟Coinglass API)

    Args:
        symbol (str): 币种符号，例如BTC、ETH（必填）
        granularity (str, optional): K线粒度，默认为"1h"。可选值包括: 1m, 3m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 24h, 1d, 1w等
        lookback_count (int, optional): 需要获取的K线数量，默认100条

    Returns:
        Dict containing:
        - kline_data (List[Dict]): 包含时间戳、开盘价、最高价、最低价、收盘价和成交量的K线数据点列表
        - symbol (str): 查询的币种符号
        - granularity (str): K线时间粒度
        - lookback_count (int): 返回的K线周期数量
        - exchange (str): 提供数据的交易所或数据源名称
        - timestamp_range (Dict): 包含'start'和'end'的时间戳范围

    Raises:
        ValueError: 当symbol为空时抛出异常
    """
    if not symbol:
        raise ValueError("Parameter 'symbol' is required and cannot be empty.")

    # Normalize inputs
    granularity = granularity or "1h"
    lookback_count = lookback_count or 100

    # Call external API (simulated)
    api_data = call_external_api("虚拟币价格查询服务_get_kline_data")

    # Construct K-line data list from indexed fields
    kline_data = [
        {
            "timestamp": api_data["kline_0_timestamp"],
            "open": api_data["kline_0_open"],
            "high": api_data["kline_0_high"],
            "low": api_data["kline_0_low"],
            "close": api_data["kline_0_close"],
            "volume": api_data["kline_0_volume"],
        },
        {
            "timestamp": api_data["kline_1_timestamp"],
            "open": api_data["kline_1_open"],
            "high": api_data["kline_1_high"],
            "low": api_data["kline_1_low"],
            "close": api_data["kline_1_close"],
            "volume": api_data["kline_1_volume"],
        },
    ]

    # Construct final result matching output schema
    result = {
        "kline_data": kline_data,
        "symbol": symbol,
        "granularity": granularity,
        "lookback_count": lookback_count,
        "exchange": api_data["exchange"],
        "timestamp_range": {
            "start": api_data["timestamp_range_start"],
            "end": api_data["timestamp_range_end"],
        },
    }

    return result