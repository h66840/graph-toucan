from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching position data from Coinglass API for a given cryptocurrency symbol.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - symbol (str): Cryptocurrency symbol, e.g., BTC
        - granularity (str): Time interval, e.g., 1h
        - exchange (str): Exchange or data source name, e.g., Binance
        - total_long_positions (float): Total long positions
        - total_short_positions (float): Total short positions
        - long_short_ratio (float): Ratio of long to short positions
        - timestamp (str): ISO8601 timestamp of data fetch
        - metadata_data_source (str): Source of data, e.g., Coinglass
        - metadata_status (str): Request status, e.g., success
        - positions_0_side (str): First position side (long/short)
        - positions_0_size (float): First position size
        - positions_0_entry_price (float): First position entry price
        - positions_0_mark_price (float): First position mark price
        - positions_0_unrealized_pnl (float): First position unrealized PnL
        - positions_0_liquidation_price (float): First position liquidation price
        - positions_0_leverage (float): First position leverage
        - positions_0_timestamp (str): First position timestamp
        - positions_1_side (str): Second position side (long/short)
        - positions_1_size (float): Second position size
        - positions_1_entry_price (float): Second position entry price
        - positions_1_mark_price (float): Second position mark price
        - positions_1_unrealized_pnl (float): Second position unrealized PnL
        - positions_1_liquidation_price (float): Second position liquidation price
        - positions_1_leverage (float): Second position leverage
        - positions_1_timestamp (str): Second position timestamp
    """
    return {
        "symbol": "BTC",
        "granularity": "1h",
        "exchange": "Binance",
        "total_long_positions": 125000.0,
        "total_short_positions": 98000.0,
        "long_short_ratio": 1.275,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_data_source": "Coinglass",
        "metadata_status": "success",
        "positions_0_side": "long",
        "positions_0_size": 2.5,
        "positions_0_entry_price": 43500.0,
        "positions_0_mark_price": 44200.0,
        "positions_0_unrealized_pnl": 1750.0,
        "positions_0_liquidation_price": 41000.0,
        "positions_0_leverage": 10.0,
        "positions_0_timestamp": "2023-10-01T12:00:00Z",
        "positions_1_side": "short",
        "positions_1_size": 1.8,
        "positions_1_entry_price": 44800.0,
        "positions_1_mark_price": 44200.0,
        "positions_1_unrealized_pnl": 1080.0,
        "positions_1_liquidation_price": 46500.0,
        "positions_1_leverage": 8.5,
        "positions_1_timestamp": "2023-10-01T11:30:00Z"
    }

def 虚拟币价格查询服务_get_position_info(
    symbol: str,
    granularity: Optional[str] = "1h",
    lookback_count: Optional[int] = 100
) -> Dict[str, Any]:
    """
    获取虚拟币合约的持仓信息 (Coinglass API)
    
    Args:
        symbol (str): 币种符号，例如BTC、ETH（必填）
        granularity (str, optional): K线粒度，默认1h。可选: 1m, 3m, 5m, 15m, 30m, 1h, 4h, 6h, 12h, 24h, 1d, 1w等
        lookback_count (int, optional): 需要获取的K线数量，默认100条
    
    Returns:
        Dict containing:
        - positions (List[Dict]): List of position records with side, size, entry price, etc.
        - symbol (str): Cryptocurrency symbol
        - granularity (str): Time interval used
        - exchange (str): Exchange or data source
        - total_long_positions (float): Total long positions
        - total_short_positions (float): Total short positions
        - long_short_ratio (float): Long/short ratio
        - timestamp (str): ISO8601 timestamp
        - metadata (Dict): Additional context including data source and status
    """
    if not symbol:
        raise ValueError("Parameter 'symbol' is required.")
    
    if lookback_count is not None and lookback_count <= 0:
        raise ValueError("Parameter 'lookback_count' must be a positive integer.")
    
    # Default to "1h" if granularity is not provided
    granularity = granularity or "1h"
    
    # Call external API (simulated)
    raw_data = call_external_api("虚拟币价格查询服务_get_position_info")
    
    # Construct positions list from indexed fields
    positions = [
        {
            "side": raw_data["positions_0_side"],
            "size": raw_data["positions_0_size"],
            "entry_price": raw_data["positions_0_entry_price"],
            "mark_price": raw_data["positions_0_mark_price"],
            "unrealized_pnl": raw_data["positions_0_unrealized_pnl"],
            "liquidation_price": raw_data["positions_0_liquidation_price"],
            "leverage": raw_data["positions_0_leverage"],
            "timestamp": raw_data["positions_0_timestamp"]
        },
        {
            "side": raw_data["positions_1_side"],
            "size": raw_data["positions_1_size"],
            "entry_price": raw_data["positions_1_entry_price"],
            "mark_price": raw_data["positions_1_mark_price"],
            "unrealized_pnl": raw_data["positions_1_unrealized_pnl"],
            "liquidation_price": raw_data["positions_1_liquidation_price"],
            "leverage": raw_data["positions_1_leverage"],
            "timestamp": raw_data["positions_1_timestamp"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "data_source": raw_data["metadata_data_source"],
        "status": raw_data["metadata_status"]
    }
    
    # Build final result matching output schema
    result = {
        "positions": positions,
        "symbol": raw_data["symbol"],
        "granularity": raw_data["granularity"],
        "exchange": raw_data["exchange"],
        "total_long_positions": raw_data["total_long_positions"],
        "total_short_positions": raw_data["total_short_positions"],
        "long_short_ratio": raw_data["long_short_ratio"],
        "timestamp": raw_data["timestamp"],
        "metadata": metadata
    }
    
    return result