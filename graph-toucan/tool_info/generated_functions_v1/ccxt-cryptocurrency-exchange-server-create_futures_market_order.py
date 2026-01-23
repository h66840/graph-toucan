from typing import Dict, List, Any, Optional
import time
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for creating a futures market order.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - order_id (str): Unique identifier assigned by the exchange
        - symbol (str): Futures/swap contract symbol
        - side (str): Order side ('buy' or 'sell')
        - amount (float): Quantity of contracts or base currency
        - price (float): Average fill price; may be null (represented as 0.0 if missing)
        - status (str): Current status of the order
        - type (str): Order type, always 'market'
        - timestamp (int): Unix timestamp in milliseconds
        - datetime (str): ISO 8601 formatted datetime string
        - cost (float): Total cost in quote currency
        - fee_cost (float): Fee cost
        - fee_currency (str): Fee currency (e.g., 'USDT')
        - fee_rate (float): Fee rate (e.g., 0.001)
        - trades_0_id (str): First trade ID
        - trades_0_price (float): First trade fill price
        - trades_0_amount (float): First trade amount
        - trades_0_fee_cost (float): First trade fee cost
        - trades_0_fee_currency (str): First trade fee currency
        - trades_1_id (str): Second trade ID
        - trades_1_price (float): Second trade fill price
        - trades_1_amount (float): Second trade amount
        - trades_1_fee_cost (float): Second trade fee cost
        - trades_1_fee_currency (str): Second trade fee currency
        - client_order_id (str): Custom client-assigned order ID if provided
        - info_message (str): Raw response message from exchange
        - info_code (int): Response code from exchange
    """
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    symbol = "BTC/USDT:USDT"
    side = "buy"  # This will be overridden by input, but default here
    amount = round(random.uniform(0.001, 1.0), 6)
    price = round(random.uniform(30000, 50000), 2)
    cost = round(amount * price, 2)
    timestamp = int(time.time() * 1000)
    dt = time.strftime('%Y-%m-%dT%H:%M:%S.%fZ', time.gmtime())
    fee_cost = round(cost * 0.0005, 6)
    client_order_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    return {
        "order_id": order_id,
        "symbol": symbol,
        "side": side,
        "amount": amount,
        "price": price,
        "status": "closed",
        "type": "market",
        "timestamp": timestamp,
        "datetime": dt,
        "cost": cost,
        "fee_cost": fee_cost,
        "fee_currency": "USDT",
        "fee_rate": 0.0005,
        "trades_0_id": ''.join(random.choices(string.digits, k=10)),
        "trades_0_price": round(price * (1 + random.uniform(-0.001, 0.001)), 2),
        "trades_0_amount": round(amount * 0.6, 6),
        "trades_0_fee_cost": round(fee_cost * 0.6, 6),
        "trades_0_fee_currency": "USDT",
        "trades_1_id": ''.join(random.choices(string.digits, k=10)),
        "trades_1_price": round(price * (1 + random.uniform(-0.001, 0.001)), 2),
        "trades_1_amount": round(amount * 0.4, 6),
        "trades_1_fee_cost": round(fee_cost * 0.4, 6),
        "trades_1_fee_currency": "USDT",
        "client_order_id": client_order_id,
        "info_message": "Order filled successfully",
        "info_code": 200,
    }


def ccxt_cryptocurrency_exchange_server_create_futures_market_order(
    amount: float,
    exchange_id: str,
    side: str,
    symbol: str,
    api_key: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
    passphrase: Optional[str] = None,
    secret_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Places a new market order in a futures/swap market, filled at the best available current price.
    
    This function simulates interaction with a cryptocurrency exchange using the CCXT library.
    It creates a market order for a specified symbol and side (buy/sell), with the given amount.
    The CCXT client is assumed to be configured for the correct market type (e.g., 'future', 'swap')
    via the 'params' dictionary which should include options like {'options': {'defaultType': 'future'}}.

    Args:
        amount (float): The quantity of contracts or base currency to trade. Must be greater than 0.
        exchange_id (str): The ID of the exchange that supports futures/swap trading (e.g., 'binance', 'bybit').
        side (str): Order side: 'buy' for a long position, 'sell' for a short position.
        symbol (str): The futures/swap contract symbol to trade (e.g., 'BTC/USDT:USDT', 'ETH-PERP').
        api_key (Optional[str]): Optional API key with trading permissions.
        params (Optional[Dict[str, Any]]): Optional extra parameters for CCXT createOrder call and client setup.
            Must include market type configuration like {'options': {'defaultType': 'future'}}.
        passphrase (Optional[str]): Optional API passphrase if required by the exchange.
        secret_key (Optional[str]): Optional secret key for API authentication.

    Returns:
        Dict[str, Any]: A dictionary containing order details with the following structure:
            - order_id (str): Unique identifier assigned by the exchange
            - symbol (str): The futures/swap contract symbol
            - side (str): Direction of the order ('buy' or 'sell')
            - amount (float): Quantity of contracts or base currency filled
            - price (float): Average fill price; may be None
            - status (str): Current status of the order
            - type (str): Order type, always 'market'
            - timestamp (int): Unix timestamp in milliseconds
            - datetime (str): ISO 8601 formatted datetime string
            - cost (float): Total cost in quote currency
            - fee (Dict): Fee information with 'cost', 'currency', 'rate'
            - trades (List[Dict]): List of individual fills/trades
            - client_order_id (str): Custom client-assigned ID if provided
            - info (Dict): Raw JSON response from exchange API

    Raises:
        ValueError: If amount <= 0, side not in ['buy', 'sell'], or exchange_id is empty.
    """
    # Input validation
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be a positive number greater than 0.")
    if side not in ["buy", "sell"]:
        raise ValueError("Side must be either 'buy' or 'sell'.")
    if not exchange_id or not exchange_id.strip():
        raise ValueError("Exchange ID is required.")
    if not symbol or not symbol.strip():
        raise ValueError("Symbol is required.")
    
    # Normalize exchange_id
    exchange_id = exchange_id.strip().lower()

    # Simulate calling external API
    raw_data = call_external_api("ccxt_cryptocurrency_exchange_server_create_futures_market_order")

    # Override side from input
    raw_data["side"] = side
    raw_data["symbol"] = symbol
    raw_data["amount"] = float(amount)

    # Construct the final response structure from flat data
    result: Dict[str, Any] = {
        "order_id": raw_data["order_id"],
        "symbol": raw_data["symbol"],
        "side": raw_data["side"],
        "amount": raw_data["amount"],
        "price": raw_data["price"],
        "status": raw_data["status"],
        "type": raw_data["type"],
        "timestamp": raw_data["timestamp"],
        "datetime": raw_data["datetime"],
        "cost": raw_data["cost"],
        "fee": {
            "cost": raw_data["fee_cost"],
            "currency": raw_data["fee_currency"],
            "rate": raw_data["fee_rate"],
        },
        "trades": [
            {
                "id": raw_data["trades_0_id"],
                "price": raw_data["trades_0_price"],
                "amount": raw_data["trades_0_amount"],
                "fee": {
                    "cost": raw_data["trades_0_fee_cost"],
                    "currency": raw_data["trades_0_fee_currency"],
                },
            },
            {
                "id": raw_data["trades_1_id"],
                "price": raw_data["trades_1_price"],
                "amount": raw_data["trades_1_amount"],
                "fee": {
                    "cost": raw_data["trades_1_fee_cost"],
                    "currency": raw_data["trades_1_fee_currency"],
                },
            },
        ],
        "client_order_id": raw_data["client_order_id"],
        "info": {
            "message": raw_data["info_message"],
            "code": raw_data["info_code"],
        },
    }

    return result