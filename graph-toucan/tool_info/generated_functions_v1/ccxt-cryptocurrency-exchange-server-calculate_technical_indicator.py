from typing import Dict, List, Any, Optional
import json
import datetime
from random import uniform


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching OHLCV data and calculating a technical indicator from a cryptocurrency exchange API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - error (str): Error message if any; empty string if no error
        - indicator_name (str): Name of the technical indicator calculated
        - symbol (str): Trading symbol used
        - timeframe (str): Timeframe used for OHLCV data
        - params_used_length (int): Length parameter used in calculation
        - params_used_price_source (str): Price source used (e.g., 'close')
        - params_used_ohlcv_limit (int): Number of OHLCV data points fetched
        - price_source_used (str): Price source actually used in calculation
        - data_0_datetime (str): ISO 8601 UTC datetime for first data point
        - data_0_value (float): Indicator value for first data point
        - data_1_datetime (str): ISO 8601 UTC datetime for second data point
        - data_1_value (float): Indicator value for second data point
    """
    now = datetime.datetime.utcnow()
    timestamp_1 = (now - datetime.timedelta(hours=1)).isoformat() + "Z"
    timestamp_2 = now.isoformat() + "Z"

    return {
        "error": "",
        "indicator_name": "RSI",
        "symbol": "BTC/USDT",
        "timeframe": "1h",
        "params_used_length": 14,
        "params_used_price_source": "close",
        "params_used_ohlcv_limit": 50,
        "price_source_used": "close",
        "data_0_datetime": timestamp_1,
        "data_0_value": round(uniform(30.0, 70.0), 2),
        "data_1_datetime": timestamp_2,
        "data_1_value": round(uniform(30.0, 70.0), 2),
    }


def ccxt_cryptocurrency_exchange_server_calculate_technical_indicator(
    exchange_id: str,
    indicator_name: str,
    symbol: str,
    timeframe: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    ohlcv_limit: Optional[int] = 50,
    params: Optional[dict] = None,
    indicator_params: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Fetches OHLCV data for a given symbol and timeframe from a cryptocurrency exchange,
    then calculates the specified technical indicator (e.g., RSI, SMA, EMA, MACD, BBANDS, STOCH, ATR).
    Returns a time series of calculated indicator values.

    Args:
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'upbit'). Case-insensitive.
        indicator_name (str): The name of the technical indicator to calculate. Supported: RSI, SMA, EMA, MACD, BBANDS, STOCH, ATR.
        symbol (str): The trading symbol to calculate the indicator for (e.g., 'BTC/USDT', 'ETH/KRW').
        timeframe (str): The candle timeframe for OHLCV data (e.g., '1h', '1d').
        api_key (Optional[str]): Optional API key for authentication.
        secret_key (Optional[str]): Optional secret key for authentication.
        passphrase (Optional[str]): Optional passphrase for exchanges requiring it.
        ohlcv_limit (Optional[int]): Number of OHLCV data points to fetch. Default is 50.
        params (Optional[dict]): Extra parameters for CCXT client (e.g., market type).
        indicator_params (Optional[str]): JSON string of indicator-specific parameters.

    Returns:
        Dict containing:
            - error (str): Error message if any
            - indicator_name (str): Name of the calculated indicator
            - symbol (str): Trading symbol
            - timeframe (str): Timeframe used
            - params_used (Dict): Parameters used in calculation
            - price_source_used (str): Price source used (e.g., 'close')
            - data (List[Dict]): List of dicts with 'datetime' (ISO 8601 UTC) and 'value' (float)
    """
    # Validate required inputs
    if not exchange_id:
        return {"error": "exchange_id is required"}
    if not indicator_name:
        return {"error": "indicator_name is required"}
    if not symbol:
        return {"error": "symbol is required"}
    if not timeframe:
        return {"error": "timeframe is required"}

    # Normalize indicator name
    indicator_name = indicator_name.upper()
    supported_indicators = ["RSI", "SMA", "EMA", "MACD", "BBANDS", "STOCH", "ATR"]
    if indicator_name not in supported_indicators:
        return {
            "error": f"Unsupported indicator_name: {indicator_name}. Supported: {', '.join(supported_indicators)}"
        }

    # Parse indicator_params if provided
    try:
        parsed_indicator_params = (
            json.loads(indicator_params) if indicator_params else {}
        )
    except (json.JSONDecodeError, TypeError):
        return {"error": "Invalid JSON format in indicator_params"}

    # Set defaults based on indicator
    params_used = {}
    price_source_used = "close"

    if indicator_name in ["RSI", "SMA", "EMA"]:
        params_used["length"] = parsed_indicator_params.get("length", 14)
        params_used["price_source"] = parsed_indicator_params.get("price_source", "close")
        price_source_used = params_used["price_source"]
    elif indicator_name == "MACD":
        params_used["fast"] = parsed_indicator_params.get("fast", 12)
        params_used["slow"] = parsed_indicator_params.get("slow", 26)
        params_used["signal"] = parsed_indicator_params.get("signal", 9)
        params_used["price_source"] = parsed_indicator_params.get("price_source", "close")
        price_source_used = params_used["price_source"]
    elif indicator_name == "BBANDS":
        params_used["length"] = parsed_indicator_params.get("length", 20)
        params_used["std"] = parsed_indicator_params.get("std", 2.0)
        params_used["price_source"] = parsed_indicator_params.get("price_source", "close")
        price_source_used = params_used["price_source"]
    elif indicator_name == "STOCH":
        params_used["k_period"] = parsed_indicator_params.get("k_period", 14)
        params_used["d_period"] = parsed_indicator_params.get("d_period", 3)
        params_used["smooth_k"] = parsed_indicator_params.get("smooth_k", 3)
        params_used["price_source_high"] = parsed_indicator_params.get(
            "price_source_high", "high"
        )
        params_used["price_source_low"] = parsed_indicator_params.get(
            "price_source_low", "low"
        )
        params_used["price_source_close"] = parsed_indicator_params.get(
            "price_source_close", "close"
        )
        price_source_used = params_used["price_source_close"]
    elif indicator_name == "ATR":
        params_used["period"] = parsed_indicator_params.get("period", 14)
        params_used["price_source_high"] = parsed_indicator_params.get(
            "price_source_high", "high"
        )
        params_used["price_source_low"] = parsed_indicator_params.get(
            "price_source_low", "low"
        )
        params_used["price_source_close"] = parsed_indicator_params.get(
            "price_source_close", "close"
        )
        price_source_used = params_used["price_source_close"]

    # Set OHLCV limit
    ohlcv_limit_val = ohlcv_limit if ohlcv_limit is not None else 50
    params_used["ohlcv_limit"] = ohlcv_limit_val

    # Call external API (simulated)
    try:
        api_data = call_external_api("ccxt-cryptocurrency-exchange-server-calculate_technical_indicator")
    except Exception as e:
        return {"error": f"Failed to fetch data from external API: {str(e)}"}

    # Construct the final result with proper nested structure
    data_points = [
        {
            "datetime": api_data["data_0_datetime"],
            "value": api_data["data_0_value"],
        },
        {
            "datetime": api_data["data_1_datetime"],
            "value": api_data["data_1_value"],
        },
    ]

    result = {
        "error": api_data["error"],
        "indicator_name": api_data["indicator_name"],
        "symbol": api_data["symbol"],
        "timeframe": api_data["timeframe"],
        "params_used": params_used,
        "price_source_used": price_source_used,
        "data": data_points,
    }

    return result