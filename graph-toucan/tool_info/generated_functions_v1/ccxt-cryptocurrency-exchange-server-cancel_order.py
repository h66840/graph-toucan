from typing import Dict, Any, Optional
import time
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for order cancellation.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success (bool): Whether the cancellation was successful
        - order_id (str): The unique identifier of the canceled order
        - status (str): Final status after cancellation
        - symbol (str): Trading pair symbol
        - timestamp (int): Unix timestamp in milliseconds
        - datetime (str): ISO 8601 datetime string
        - side (str): Order side ('buy' or 'sell')
        - type (str): Order type ('limit', 'market', etc.)
        - price (float): Price of the order
        - amount (float): Original amount
        - filled (float): Amount filled before cancellation
        - remaining (float): Amount remaining
        - cost (float): Total cost of filled portion
        - fee_currency (str): Fee currency
        - fee_cost (float): Fee cost
        - fee_rate (float): Fee rate
        - info_response_code (int): Raw API response code
        - info_message (str): Raw API message
    """
    return {
        "success": True,
        "order_id": "123456789",
        "status": "canceled",
        "symbol": "BTC/USDT",
        "timestamp": int(time.time() * 1000),
        "datetime": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
        "side": random.choice(["buy", "sell"]),
        "type": random.choice(["limit", "market"]),
        "price": round(random.uniform(30000, 50000), 2) if random.choice([True, False]) else None,
        "amount": round(random.uniform(0.01, 1), 4),
        "filled": round(random.uniform(0, 0.5), 4),
        "remaining": round(random.uniform(0, 1), 4),
        "cost": round(random.uniform(0, 50000), 2),
        "fee_currency": "USDT",
        "fee_cost": round(random.uniform(0.1, 10), 4),
        "fee_rate": round(random.uniform(0.001, 0.005), 4),
        "info_response_code": 200,
        "info_message": "Order canceled successfully"
    }


def ccxt_cryptocurrency_exchange_server_cancel_order(
    exchange_id: str,
    id: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    symbol: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Cancels an existing open order on a cryptocurrency exchange using CCXT.

    Args:
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'ftx'). Case-insensitive.
        id (str): The order ID (string) of the order to be canceled.
        api_key (Optional[str]): Optional API key with trading permissions.
        secret_key (Optional[str]): Optional secret key for API authentication.
        passphrase (Optional[str]): Optional passphrase if required by the exchange.
        symbol (Optional[str]): Optional trading symbol (e.g., 'BTC/USDT'). Required by some exchanges.
        params (Optional[Dict[str, Any]]): Optional extra parameters for client or API call.

    Returns:
        Dict[str, Any]: A dictionary containing the cancellation result with the following keys:
            - success (bool): Whether the cancellation was successful
            - order_id (str): The unique identifier of the canceled order
            - status (str): Final status of the order
            - symbol (str): Trading pair symbol
            - timestamp (int): Unix timestamp in milliseconds
            - datetime (str): ISO 8601 datetime string
            - side (str): Direction of the order ('buy' or 'sell')
            - type (str): Order type
            - price (float): Order price (None for market orders)
            - amount (float): Original order quantity
            - filled (float): Amount already filled
            - remaining (float): Amount remaining (unfilled)
            - cost (float): Total cost of filled portion
            - fee (Dict): Fee details with keys: currency, cost, rate
            - info (Dict): Raw response from exchange API

    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not exchange_id:
        raise ValueError("exchange_id is required")
    if not id:
        raise ValueError("id is required")

    # Normalize exchange_id
    exchange_id = exchange_id.strip().lower()

    # Simulate calling external API
    try:
        api_data = call_external_api("ccxt-cryptocurrency-exchange-server-cancel_order")
    except Exception as e:
        return {
            "success": False,
            "order_id": id,
            "status": "error",
            "symbol": symbol or "",
            "timestamp": int(time.time() * 1000),
            "datetime": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ", time.gmtime()),
            "side": "",
            "type": "",
            "price": None,
            "amount": 0.0,
            "filled": 0.0,
            "remaining": 0.0,
            "cost": 0.0,
            "fee": {"currency": "", "cost": 0.0, "rate": None},
            "info": {"error": str(e)}
        }

    # Construct nested output structure
    result = {
        "success": api_data["success"],
        "order_id": api_data["order_id"],
        "status": api_data["status"],
        "symbol": api_data["symbol"] if symbol is None else symbol,
        "timestamp": api_data["timestamp"],
        "datetime": api_data["datetime"],
        "side": api_data["side"],
        "type": api_data["type"],
        "price": api_data["price"],
        "amount": api_data["amount"],
        "filled": api_data["filled"],
        "remaining": api_data["remaining"],
        "cost": api_data["cost"],
        "fee": {
            "currency": api_data["fee_currency"],
            "cost": api_data["fee_cost"],
            "rate": api_data["fee_rate"]
        },
        "info": {
            "response_code": api_data["info_response_code"],
            "message": api_data["info_message"]
        }
    }

    return result