from typing import Dict, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for setting trading leverage on a cryptocurrency exchange.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success (bool): Indicates whether the leverage was set successfully
        - message (str): A human-readable message describing the result
        - exchange_id (str): The ID of the exchange where leverage was set
        - symbol (str): The trading symbol for which leverage was applied
        - leverage (int): The leverage multiplier that was requested and set
        - margin_mode (str): The margin mode in effect after setting leverage
        - timestamp (str): ISO 8601 timestamp when the operation was executed
        - response_status (str): Status field from raw response
        - response_leverage (int): Leverage value in raw response
        - response_marginMode (str): Margin mode in raw response
        - response_symbol (str): Symbol in raw response
    """
    return {
        "success": True,
        "message": "Leverage set successfully",
        "exchange_id": "binance",
        "symbol": "BTC/USDT:USDT",
        "leverage": 10,
        "margin_mode": "isolated",
        "timestamp": "2023-10-05T12:34:56.789Z",
        "response_status": "ok",
        "response_leverage": 10,
        "response_marginMode": "isolated",
        "response_symbol": "BTC/USDT:USDT"
    }


def ccxt_cryptocurrency_exchange_server_set_trading_leverage(
    exchange_id: str,
    leverage: int,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    symbol: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Sets the leverage for a specific trading symbol on a cryptocurrency exchange using CCXT.

    This function simulates the process of setting leverage on a futures or margin market.
    It validates inputs, constructs necessary configurations, and returns a structured response
    mimicking the actual CCXT setLeverage call.

    Args:
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'ftx'). Case-insensitive.
        leverage (int): The desired leverage multiplier (e.g., 10 for 10x). Must be greater than 0.
        api_key (Optional[str]): Optional API key for the exchange.
        secret_key (Optional[str]): Optional secret key for the exchange.
        passphrase (Optional[str]): Optional passphrase if required by the exchange.
        symbol (Optional[str]): Trading symbol (e.g., 'BTC/USDT:USDT') to set leverage for.
        params (Optional[Dict[str, Any]]): Extra parameters for client init and API call.
            Should include options like {'options': {'defaultType': 'future'}} and/or
            margin mode settings like {'marginMode': 'isolated'}.

    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - success (bool): Whether the leverage was set successfully
            - message (str): Human-readable result description
            - exchange_id (str): Exchange ID
            - symbol (str): Symbol for which leverage was applied
            - leverage (int): Requested leverage multiplier
            - margin_mode (str): Margin mode after setting leverage
            - timestamp (str): ISO 8601 timestamp of operation
            - response (Dict): Raw response data from the simulated API call
    """
    # Input validation
    if not exchange_id or not exchange_id.strip():
        return {
            "success": False,
            "message": "Exchange ID is required",
            "exchange_id": "",
            "symbol": symbol or "",
            "leverage": leverage,
            "margin_mode": "",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "response": {"error": "Exchange ID is required"}
        }

    if leverage <= 0:
        return {
            "success": False,
            "message": "Leverage must be greater than 0",
            "exchange_id": exchange_id.strip().lower(),
            "symbol": symbol or "",
            "leverage": leverage,
            "margin_mode": "",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "response": {"error": "Leverage must be greater than 0"}
        }

    # Normalize exchange_id
    exchange_id = exchange_id.strip().lower()

    # Determine margin mode from params if provided
    margin_mode = "cross"  # default fallback
    if params and isinstance(params, dict):
        if "marginMode" in params:
            margin_mode = params["marginMode"]
        elif params.get("options", {}).get("defaultType") == "margin":
            margin_mode = "cross"  # default for margin
        else:
            margin_mode = "isolated"  # default for futures

    # Call external API simulation
    api_data = call_external_api("ccxt-cryptocurrency-exchange-server-set_trading_leverage")

    # Override with actual input values where applicable
    result_symbol = symbol or api_data["symbol"]
    result_leverage = leverage
    result_exchange_id = exchange_id

    # Construct the final response structure
    result = {
        "success": api_data["success"],
        "message": api_data["message"],
        "exchange_id": result_exchange_id,
        "symbol": result_symbol,
        "leverage": result_leverage,
        "margin_mode": api_data["margin_mode"] or margin_mode,
        "timestamp": api_data["timestamp"],
        "response": {
            "status": api_data["response_status"],
            "leverage": api_data["response_leverage"],
            "marginMode": api_data["response_marginMode"],
            "symbol": api_data["response_symbol"]
        }
    }

    return result