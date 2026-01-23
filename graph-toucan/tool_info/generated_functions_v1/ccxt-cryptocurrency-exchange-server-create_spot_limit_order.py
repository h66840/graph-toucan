from typing import Dict, Any, Optional
import time
import uuid


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for creating a spot limit order.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - order_id (str): Unique identifier assigned by the exchange.
        - symbol (str): Trading pair symbol (e.g., 'BTC/USDT').
        - side (str): Order side, either 'buy' or 'sell'.
        - type (str): Order type, e.g., 'limit'.
        - price (float): Price at which the limit order was set.
        - amount (float): Original quantity of the base asset.
        - filled (float): Quantity filled so far.
        - remaining (float): Remaining amount to be filled.
        - status (str): Current status of the order (e.g., 'open').
        - timestamp (int): Unix timestamp in milliseconds.
        - datetime (str): ISO 8601 formatted datetime string.
        - fee_cost (float): Cost of the fee charged by the exchange.
        - fee_currency (str): Currency in which the fee is denominated.
        - fee_rate (float): Optional rate of the fee.
        - info_order_id (str): Raw order ID from exchange response.
        - info_symbol (str): Raw symbol from exchange response.
        - info_side (str): Raw side from exchange response.
        - info_type (str): Raw type from exchange response.
        - info_price (float): Raw price from exchange response.
        - info_amount (float): Raw amount from exchange response.
        - info_status (str): Raw status from exchange response.
        - client_order_id (str): Custom client-assigned ID if provided, otherwise null.
    """
    now_ms = int(time.time() * 1000)
    iso_time = time.strftime('%Y-%m-%dT%H:%M:%S.%fZ', time.gmtime())
    return {
        "order_id": f"ord_{uuid.uuid4().hex[:16]}",
        "symbol": "BTC/USDT",
        "side": "buy",
        "type": "limit",
        "price": 50000.0,
        "amount": 0.001,
        "filled": 0.0,
        "remaining": 0.001,
        "status": "open",
        "timestamp": now_ms,
        "datetime": iso_time,
        "fee_cost": 0.000005,
        "fee_currency": "BTC",
        "fee_rate": 0.001,
        "info_order_id": f"ord_{uuid.uuid4().hex[:16]}",
        "info_symbol": "BTC/USDT",
        "info_side": "buy",
        "info_type": "limit",
        "info_price": 50000.0,
        "info_amount": 0.001,
        "info_status": "open",
        "client_order_id": "my_spot_order_123"
    }


def ccxt_cryptocurrency_exchange_server_create_spot_limit_order(
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
    Places a new limit order in the spot market on a specified exchange using CCXT.

    This function simulates the creation of a spot limit order. It validates inputs,
    constructs the order parameters, and returns a realistic mock response from the exchange.
    Authentication is assumed to be handled externally.

    Args:
        amount (float): The quantity of the base currency to trade. Must be greater than 0.
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'coinbasepro'). Case-insensitive.
        side (str): Order side: 'buy' to purchase the base asset, 'sell' to sell it.
        symbol (str): The spot market symbol to trade (e.g., 'BTC/USDT', 'ETH/BTC').
        price (float): The price at which to place the limit order. Must be greater than 0.
        api_key (Optional[str]): Optional API key with trading permissions.
        secret_key (Optional[str]): Optional secret key for API authentication.
        passphrase (Optional[str]): Optional passphrase if required by the exchange.
        params (Optional[Dict[str, Any]]): Optional extra parameters for the order (e.g., clientOrderId, timeInForce).

    Returns:
        Dict[str, Any]: A dictionary containing the order details with the following structure:
            - order_id (str)
            - symbol (str)
            - side (str)
            - type (str)
            - price (float)
            - amount (float)
            - filled (float)
            - remaining (float)
            - status (str)
            - timestamp (int)
            - datetime (str)
            - fee (Dict): Contains 'cost', 'currency', and optionally 'rate'
            - info (Dict): Raw response from the exchange
            - client_order_id (str or None)

    Raises:
        ValueError: If required inputs are invalid (e.g., amount <= 0, invalid side, etc.)
    """
    # Input validation
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be a positive number.")
    if not isinstance(exchange_id, str) or not exchange_id.strip():
        raise ValueError("Exchange ID must be a non-empty string.")
    if side not in ['buy', 'sell']:
        raise ValueError("Side must be either 'buy' or 'sell'.")
    if not isinstance(symbol, str) or '/' not in symbol:
        raise ValueError("Symbol must be a valid trading pair string (e.g., 'BTC/USDT').")
    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError("Price must be a positive number.")

    # Normalize exchange_id
    exchange_id = exchange_id.strip().lower()

    # Simulate calling external API
    api_data = call_external_api("ccxt-cryptocurrency-exchange-server-create_spot_limit_order")

    # Override symbol and side from input if provided
    used_symbol = symbol
    used_side = side
    used_amount = amount
    used_price = price

    # Extract client order ID from params if provided
    client_order_id = None
    if isinstance(params, dict):
        client_order_id = params.get('clientOrderId', params.get('client_order_id'))

    # Construct fee object
    fee = {
        'cost': api_data['fee_cost'],
        'currency': api_data['fee_currency'],
        'rate': api_data['fee_rate']
    }

    # Construct info object from raw response fields
    info = {
        'id': api_data['info_order_id'],
        'symbol': api_data['info_symbol'],
        'side': api_data['info_side'],
        'type': api_data['info_type'],
        'price': api_data['info_price'],
        'amount': api_data['info_amount'],
        'status': api_data['info_status']
    }

    # Build final result
    result = {
        'order_id': api_data['order_id'],
        'symbol': used_symbol,
        'side': used_side,
        'type': api_data['type'],
        'price': used_price,
        'amount': used_amount,
        'filled': api_data['filled'],
        'remaining': api_data['remaining'],
        'status': api_data['status'],
        'timestamp': api_data['timestamp'],
        'datetime': api_data['datetime'],
        'fee': fee,
        'info': info,
        'client_order_id': client_order_id or api_data['client_order_id']
    }

    return result