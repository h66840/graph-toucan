from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for virtual coin market information.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - price (float): Current market price of the coin
        - change_24h (float): 24-hour price change percentage
        - volume_24h (float): 24-hour trading volume in USD
        - high_24h (float): 24-hour high price
        - low_24h (float): 24-hour low price
        - market_cap (float): Total market capitalization in USD
        - funding_rate (float): Current funding rate for perpetual contracts
        - open_interest (float): Open interest value in USD
        - dominant_broker (str): Name of the dominant exchange/platform
        - leverage_info_max_leverage (int): Maximum leverage available
        - leverage_info_common_levels_0 (float): First common leverage level
        - leverage_info_common_levels_1 (float): Second common leverage level
        - liquidation_price (float): Average liquidation price for long/short positions
        - last_updated (str): Data last updated timestamp in ISO 8601 format
        - symbol (str): Coin symbol requested
    """
    return {
        "price": 43520.15,
        "change_24h": -2.45,
        "volume_24h": 28567890000.0,
        "high_24h": 44890.75,
        "low_24h": 42100.30,
        "market_cap": 857345678900.0,
        "funding_rate": 0.000125,
        "open_interest": 18956789000.0,
        "dominant_broker": "Binance",
        "leverage_info_max_leverage": 125,
        "leverage_info_common_levels_0": 10.0,
        "leverage_info_common_levels_1": 20.0,
        "liquidation_price": 41230.80,
        "last_updated": "2023-10-15T12:34:56Z",
        "symbol": "BTC"
    }

def 虚拟币价格查询服务_get_coin_info(symbol: str) -> Dict[str, Any]:
    """
    获取虚拟币的合约市场信息 (Coinglass API)
    
    Args:
        symbol (str): 币种符号，例如BTC、ETH
    
    Returns:
        Dict containing detailed market information for the cryptocurrency in futures markets:
        - price (float): 当前币种的最新市场价格
        - change_24h (float): 过去24小时的价格变化百分比
        - volume_24h (float): 过去24小时的交易量（以美元计）
        - high_24h (float): 过去24小时内的最高价格
        - low_24h (float): 过去24小时内的最低价格
        - market_cap (float): 该币种的总市值（以美元计）
        - funding_rate (float): 当前资金费率（适用于合约市场）
        - open_interest (float): 未平仓合约总额（以美元计）
        - dominant_broker (str): 主导交易所或平台名称
        - leverage_info (Dict): 杠杆相关信息，包含最大杠杆倍数、常用杠杆区间等
            - max_leverage (int): 最大杠杆倍数
            - common_levels (List[float]): 常用杠杆区间
        - liquidation_price (float): 当前多头/空头平均爆仓价格（如适用）
        - last_updated (str): 数据最后更新时间（ISO 8601格式）
        - symbol (str): 返回的币种符号，与请求一致
    
    Raises:
        ValueError: If symbol is empty or not a string
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string")
    
    # Fetch simulated external data
    api_data = call_external_api("虚拟币价格查询服务_get_coin_info")
    
    # Construct leverage_info with common_levels list from indexed fields
    leverage_info = {
        "max_leverage": api_data["leverage_info_max_leverage"],
        "common_levels": [
            api_data["leverage_info_common_levels_0"],
            api_data["leverage_info_common_levels_1"]
        ]
    }
    
    # Build final result matching output schema exactly
    result = {
        "price": api_data["price"],
        "change_24h": api_data["change_24h"],
        "volume_24h": api_data["volume_24h"],
        "high_24h": api_data["high_24h"],
        "low_24h": api_data["low_24h"],
        "market_cap": api_data["market_cap"],
        "funding_rate": api_data["funding_rate"],
        "open_interest": api_data["open_interest"],
        "dominant_broker": api_data["dominant_broker"],
        "leverage_info": leverage_info,
        "liquidation_price": api_data["liquidation_price"],
        "last_updated": api_data["last_updated"],
        "symbol": api_data["symbol"]
    }
    
    return result