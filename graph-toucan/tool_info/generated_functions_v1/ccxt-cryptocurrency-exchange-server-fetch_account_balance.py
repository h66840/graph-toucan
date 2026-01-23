from typing import Dict, Any, Optional
import time
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching account balance data from an external cryptocurrency exchange API via CCXT.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - balances_BTC_total (float): Total BTC balance
        - balances_BTC_free (float): Free BTC balance available for trading
        - balances_BTC_used (float): BTC balance currently locked in orders
        - balances_USDT_total (float): Total USDT balance
        - balances_USDT_free (float): Free USDT balance available for trading
        - balances_USDT_used (float): USDT balance currently locked in orders
        - timestamp (int): Unix timestamp in milliseconds when data was fetched
        - datetime (str): ISO 8601 formatted datetime string
        - info_server_time (int): Raw server time from exchange (in milliseconds)
        - info_rate_limit (int): Rate limit allowed by the exchange
        - info_success (bool): Whether the raw API call was successful
        - type (str): Account type for which balance was fetched (e.g., 'spot', 'margin')
    """
    current_time_ms = int(time.time() * 1000)
    return {
        "balances_BTC_total": 1.25,
        "balances_BTC_free": 1.0,
        "balances_BTC_used": 0.25,
        "balances_USDT_total": 10000.0,
        "balances_USDT_free": 9500.0,
        "balances_USDT_used": 500.0,
        "timestamp": current_time_ms,
        "datetime": datetime.utcfromtimestamp(current_time_ms / 1000).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "info_server_time": current_time_ms,
        "info_rate_limit": 1200,
        "info_success": True,
        "type": "spot"
    }


def ccxt_cryptocurrency_exchange_server_fetch_account_balance(
    exchange_id: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetches the current balance of an account from a specified cryptocurrency exchange.
    
    This function simulates interaction with a cryptocurrency exchange using the CCXT library.
    Authentication is handled externally, and optional parameters can specify account type
    (e.g., spot, margin, futures) or other exchange-specific settings.

    Args:
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'coinbasepro', 'upbit'). Case-insensitive.
        api_key (Optional[str]): API key for authentication. If not provided, pre-configured credentials may be used.
        secret_key (Optional[str]): Secret key for authentication. Used with api_key if required.
        passphrase (Optional[str]): Passphrase for exchanges that require it (e.g., KuCoin, OKX).
        params (Optional[Dict[str, Any]]): Extra parameters for the CCXT fetchBalance call or client instantiation.
            Example: {'type': 'margin'} or {'options': {'defaultType': 'future'}}.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - balances (Dict): Per-currency balances with 'total', 'free', and 'used' float values.
            - timestamp (int): Unix timestamp in milliseconds when data was fetched.
            - datetime (str): ISO 8601 datetime string corresponding to the timestamp.
            - info (Dict): Raw response from the exchange API with exchange-specific metadata.
            - type (str): The account type for which the balance was fetched (e.g., 'spot', 'margin').

    Raises:
        ValueError: If exchange_id is empty or not a string.
    """
    if not exchange_id or not isinstance(exchange_id, str):
        raise ValueError("exchange_id is required and must be a non-empty string")

    # Normalize exchange_id
    exchange_id = exchange_id.strip().lower()

    # Simulate calling external API
    api_data = call_external_api("ccxt-cryptocurrency-exchange-server-fetch_account_balance")

    # Reconstruct nested balances structure
    balances = {
        "BTC": {
            "total": api_data["balances_BTC_total"],
            "free": api_data["balances_BTC_free"],
            "used": api_data["balances_BTC_used"]
        },
        "USDT": {
            "total": api_data["balances_USDT_total"],
            "free": api_data["balances_USDT_free"],
            "used": api_data["balances_USDT_used"]
        }
    }

    # Reconstruct info object from flattened fields
    info = {
        "server_time": api_data["info_server_time"],
        "rateLimit": api_data["info_rate_limit"],
        "success": api_data["info_success"]
    }

    # Construct final result matching output schema
    result = {
        "balances": balances,
        "timestamp": api_data["timestamp"],
        "datetime": api_data["datetime"],
        "info": info,
        "type": api_data["type"]
    }

    return result