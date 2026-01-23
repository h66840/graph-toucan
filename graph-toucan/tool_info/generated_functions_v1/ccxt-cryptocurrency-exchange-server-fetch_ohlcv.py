from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching OHLCV data from an external cryptocurrency exchange API via CCXT.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - ohlcv_0_timestamp (int): First candle timestamp in milliseconds
        - ohlcv_0_open (float): First candle open price
        - ohlcv_0_high (float): First candle high price
        - ohlcv_0_low (float): First candle low price
        - ohlcv_0_close (float): First candle close price
        - ohlcv_0_volume (float): First candle volume
        - ohlcv_1_timestamp (int): Second candle timestamp in milliseconds
        - ohlcv_1_open (float): Second candle open price
        - ohlcv_1_high (float): Second candle high price
        - ohlcv_1_low (float): Second candle low price
        - ohlcv_1_close (float): Second candle close price
        - ohlcv_1_volume (float): Second candle volume
        - error (str): Error message if any, otherwise empty string
    """
    return {
        "ohlcv_0_timestamp": 1700000000000,
        "ohlcv_0_open": 45000.0,
        "ohlcv_0_high": 45200.0,
        "ohlcv_0_low": 44800.0,
        "ohlcv_0_close": 45100.0,
        "ohlcv_0_volume": 15.5,
        "ohlcv_1_timestamp": 1700000300000,
        "ohlcv_1_open": 45100.0,
        "ohlcv_1_high": 45300.0,
        "ohlcv_1_low": 45050.0,
        "ohlcv_1_close": 45250.0,
        "ohlcv_1_volume": 18.2,
        "error": ""
    }

def ccxt_cryptocurrency_exchange_server_fetch_ohlcv(
    exchange_id: str,
    symbol: str,
    timeframe: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    since: Optional[int] = None,
    limit: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetches historical Open-High-Low-Close-Volume (OHLCV) candlestick data for a specific trading symbol and timeframe.
    
    Authentication (api_key, secret_key) is optional; some exchanges might provide more data or higher rate limits with authentication.
    Use `params` for exchange-specific options, like requesting 'mark' or 'index' price OHLCV for derivatives,
    or to set `defaultType` for client instantiation if fetching for non-spot markets.
    
    Args:
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'kraken'). Case-insensitive.
        symbol (str): The trading symbol to fetch OHLCV data for (e.g., 'BTC/USDT', 'ETH/BTC', 'BTC/USDT:USDT' for futures).
        timeframe (str): The length of time each candle represents (e.g., '1m', '5m', '1h', '1d', '1w').
        api_key (Optional[str]): Optional API key for authentication.
        secret_key (Optional[str]): Optional secret key for authentication.
        passphrase (Optional[str]): Optional passphrase for exchanges that require it.
        since (Optional[int]): Earliest time in milliseconds (UTC epoch) to fetch data from.
        limit (Optional[int]): Maximum number of OHLCV candles to return.
        params (Optional[Dict[str, Any]]): Extra parameters for CCXT fetchOHLCV or client instantiation.
    
    Returns:
        Dict with the following keys:
        - ohlcv_data (List[List]): List of OHLCV candles, each as [timestamp (ms), open, high, low, close, volume]
        - error (Optional[str]): Error message if request failed, otherwise None
    """
    # Validate required inputs
    if not exchange_id:
        return {"ohlcv_data": [], "error": "exchange_id is required"}
    if not symbol:
        return {"ohlcv_data": [], "error": "symbol is required"}
    if not timeframe:
        return {"ohlcv_data": [], "error": "timeframe is required"}

    # Call external API simulation
    try:
        api_data = call_external_api("ccxt-cryptocurrency-exchange-server-fetch_ohlcv")
        error_msg = api_data.get("error", "")
        
        if error_msg:
            return {"ohlcv_data": [], "error": error_msg}
        
        # Construct OHLCV list from flattened fields
        ohlcv_data: List[List] = [
            [
                api_data["ohlcv_0_timestamp"],
                api_data["ohlcv_0_open"],
                api_data["ohlcv_0_high"],
                api_data["ohlcv_0_low"],
                api_data["ohlcv_0_close"],
                api_data["ohlcv_0_volume"]
            ],
            [
                api_data["ohlcv_1_timestamp"],
                api_data["ohlcv_1_open"],
                api_data["ohlcv_1_high"],
                api_data["ohlcv_1_low"],
                api_data["ohlcv_1_close"],
                api_data["ohlcv_1_volume"]
            ]
        ]
        
        return {
            "ohlcv_data": ohlcv_data,
            "error": None
        }
        
    except Exception as e:
        return {
            "ohlcv_data": [],
            "error": f"Failed to fetch OHLCV data: {str(e)}"
        }