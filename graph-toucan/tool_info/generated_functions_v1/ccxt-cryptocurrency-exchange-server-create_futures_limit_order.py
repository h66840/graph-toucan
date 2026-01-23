from typing import Dict, List, Any, Optional
import time
import uuid
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for creating a futures limit order.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - order_id (str): Unique identifier assigned by the exchange
        - symbol (str): Contract symbol (e.g., 'BTC/USDT:USDT')
        - side (str): Order side ('buy' or 'sell')
        - amount (float): Quantity ordered
        - price (float): Limit price
        - type (str): Order type ('limit')
        - status (str): Current order status ('open')
        - timestamp (int): Unix timestamp in milliseconds
        - datetime (str): ISO 8601 datetime string
        - filled (float): Amount filled so far
        - remaining (float): Amount remaining to be filled
        - cost (float): Total cost of filled portion
        - average (float): Average fill price
        - fee_cost (float): Fee cost
        - fee_currency (str): Fee currency (e.g., 'USDT')
        - fee_rate (float): Fee rate (e.g., 0.0005)
        - trades_0_id (str): First trade ID
        - trades_0_amount (float): First trade amount
        - trades_0_price (float): First trade price
        - trades_0_timestamp (int): First trade timestamp
        - trades_1_id (str): Second trade ID
        - trades_1_amount (float): Second trade amount
        - trades_1_price (float): Second trade price
        - trades_1_timestamp (int): Second trade timestamp
        - client_order_id (str): Custom client order ID if provided
        - info_status (str): Raw status from exchange
        - info_leverage (str): Raw leverage setting
        - info_margin_mode (str): Raw margin mode
    """
    now_ms = int(time.time() * 1000)
    now_iso = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    
    return {
        "order_id": f"ord_{uuid.uuid4().hex[:16]}",
        "symbol": "BTC/USDT:USDT",
        "side": "buy",
        "amount": 0.001,
        "price": 43250.0,
        "type": "limit",
        "status": "open",
        "timestamp": now_ms,
        "datetime": now_iso,
        "filled": 0.0,
        "remaining": 0.001,
        "cost": 0.0,
        "average": None,
        "fee_cost": 0.0,
        "fee_currency": "USDT",
        "fee_rate": 0.0005,
        "trades_0_id": f"trade_{uuid.uuid4().hex[:12]}",
        "trades_0_amount": 0.0,
        "trades_0_price": 0.0,
        "trades_0_timestamp": 0,
        "trades_1_id": f"trade_{uuid.uuid4().hex[:12]}",
        "trades_1_amount": 0.0,
        "trades_1_price": 0.0,
        "trades_1_timestamp": 0,
        "client_order_id": "my_fut_limit_001",
        "info_status": "new",
        "info_leverage": "10",
        "info_margin_mode": "cross"
    }


def ccxt_cryptocurrency_exchange_server_create_futures_limit_order(
    amount: float,
    exchange_id: str,
    side: str,
    symbol: str,
    price: float,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Places a new limit order in a futures/swap market using CCXT.
    
    This function simulates the creation of a futures limit order via an external exchange API.
    The CCXT client is assumed to be properly configured for the futures/swap market type
    via the 'params' dictionary (e.g., {'options': {'defaultType': 'future'}}).
    
    Args:
        amount (float): The quantity of contracts or base currency to trade. Must be > 0.
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'bybit', 'okx'). Case-insensitive.
        side (str): Order side: 'buy' for long, 'sell' for short.
        symbol (str): The futures/swap contract symbol (e.g., 'BTC/USDT:USDT', 'ETH-PERP').
        price (float): The limit price for the order. Must be > 0.
        api_key (Optional[str]): API key with trading permissions. May be pre-configured.
        secret_key (Optional[str]): Secret key for API authentication.
        passphrase (Optional[str]): Passphrase required by some exchanges (e.g., OKX).
        params (Optional[Dict[str, Any]]): Extra parameters for client setup and order creation.
            Critical: Include {'options': {'defaultType': 'future'}} or similar to set market type.
            Also supports order params like 'clientOrderId', 'postOnly', 'reduceOnly', 'timeInForce'.

    Returns:
        Dict[str, Any]: A dictionary containing the order details with the following structure:
            - order_id (str)
            - symbol (str)
            - side (str)
            - amount (float)
            - price (float)
            - type (str)
            - status (str)
            - timestamp (int)
            - datetime (str)
            - filled (float)
            - remaining (float)
            - cost (float)
            - average (float)
            - fee (Dict): Contains 'cost', 'currency', 'rate'
            - trades (List[Dict]): List of two trade objects with 'id', 'amount', 'price', 'timestamp'
            - client_order_id (str)
            - info (Dict): Raw response from exchange

    Raises:
        ValueError: If required parameters are invalid (e.g., amount <= 0, invalid side, etc.)
    """
    # Input validation
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be a positive number greater than 0.")
    
    if not isinstance(exchange_id, str) or not exchange_id.strip():
        raise ValueError("Exchange ID must be a non-empty string.")
    
    if side not in ['buy', 'sell']:
        raise ValueError("Side must be either 'buy' or 'sell'.")
    
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("Symbol must be a non-empty string.")
    
    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError("Price must be a positive number greater than 0.")
    
    # Simulate calling external API
    api_data = call_external_api("ccxt-cryptocurrency-exchange-server-create_futures_limit_order")
    
    # Override defaults with input values where applicable
    result_symbol = symbol
    result_side = side
    result_amount = float(amount)
    result_price = float(price)
    result_client_order_id = params.get("clientOrderId", api_data["client_order_id"]) if params and "clientOrderId" in params else api_data["client_order_id"]
    
    # Construct fee object
    fee = {
        "cost": api_data["fee_cost"],
        "currency": api_data["fee_currency"],
        "rate": api_data["fee_rate"]
    }
    
    # Construct trades list from indexed fields
    trades = [
        {
            "id": api_data["trades_0_id"],
            "amount": api_data["trades_0_amount"],
            "price": api_data["trades_0_price"],
            "timestamp": api_data["trades_0_timestamp"]
        },
        {
            "id": api_data["trades_1_id"],
            "amount": api_data["trades_1_amount"],
            "price": api_data["trades_1_price"],
            "timestamp": api_data["trades_1_timestamp"]
        }
    ]
    
    # Construct info object from raw fields
    info = {
        "status": api_data["info_status"],
        "leverage": api_data["info_leverage"],
        "margin_mode": api_data["info_margin_mode"]
    }
    
    # Final result structure
    result = {
        "order_id": api_data["order_id"],
        "symbol": result_symbol,
        "side": result_side,
        "amount": result_amount,
        "price": result_price,
        "type": "limit",
        "status": api_data["status"],
        "timestamp": api_data["timestamp"],
        "datetime": api_data["datetime"],
        "filled": api_data["filled"],
        "remaining": api_data["remaining"],
        "cost": api_data["cost"],
        "average": api_data["average"] if api_data["average"] is not None else None,
        "fee": fee,
        "trades": trades,
        "client_order_id": result_client_order_id,
        "info": info
    }