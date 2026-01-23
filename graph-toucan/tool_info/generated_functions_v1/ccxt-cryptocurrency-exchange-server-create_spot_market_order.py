from typing import Dict, List, Any, Optional
import time
import random
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for creating a spot market order.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - order_id (str): Unique identifier assigned by the exchange.
        - symbol (str): Trading pair symbol (e.g., 'BTC/USDT').
        - side (str): Order side, either 'buy' or 'sell'.
        - type (str): Order type, always 'market'.
        - amount (float): Quantity of base asset involved.
        - price (float): Execution price for the order.
        - average (float): Average fill price.
        - filled (float): Amount filled so far.
        - remaining (float): Amount remaining unfilled.
        - status (str): Current order status (e.g., 'closed', 'partially-filled').
        - cost (float): Total cost in quote currency.
        - timestamp (int): Unix timestamp in milliseconds.
        - datetime (str): ISO 8601 formatted datetime string.
        - fee_cost (float): Fee cost.
        - fee_currency (str): Fee currency (e.g., 'USDT').
        - fee_rate (float): Fee rate as decimal.
        - trade_0_id (str): First trade ID.
        - trade_0_amount (float): First trade amount.
        - trade_0_price (float): First trade price.
        - trade_0_timestamp (int): First trade timestamp.
        - trade_0_fee_cost (float): First trade fee cost.
        - trade_0_fee_currency (str): First trade fee currency.
        - trade_1_id (str): Second trade ID.
        - trade_1_amount (float): Second trade amount.
        - trade_1_price (float): Second trade price.
        - trade_1_timestamp (int): Second trade timestamp.
        - trade_1_fee_cost (float): Second trade fee cost.
        - trade_1_fee_currency (str): Second trade fee currency.
        - client_order_id (str): Custom client order ID if provided.
        - info_message (str): Raw response message from exchange.
        - info_success (bool): Whether the operation was successful.
    """
    now_ms = int(time.time() * 1000)
    now_iso = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    base_amount = random.uniform(0.01, 1.0)
    quote_amount = random.uniform(100, 10000)
    filled_portion = random.choice([1.0, 0.8, 0.5])
    filled_amount = base_amount * filled_portion
    remaining_amount = base_amount * (1 - filled_portion)
    avg_price = quote_amount / base_amount if base_amount > 0 else 0
    cost = filled_amount * avg_price

    return {
        "order_id": f"ORD-{int(time.time())}-{random.randint(1000, 9999)}",
        "symbol": "BTC/USDT",
        "side": "buy",
        "type": "market",
        "amount": base_amount,
        "price": avg_price,
        "average": avg_price,
        "filled": filled_amount,
        "remaining": remaining_amount,
        "status": "closed" if filled_portion == 1.0 else "partially-filled",
        "cost": cost,
        "timestamp": now_ms,
        "datetime": now_iso,
        "fee_cost": round(cost * 0.001, 6),
        "fee_currency": "USDT",
        "fee_rate": 0.001,
        "trade_0_id": f"TRADE-{random.randint(100000, 999999)}",
        "trade_0_amount": filled_amount * 0.6,
        "trade_0_price": avg_price,
        "trade_0_timestamp": now_ms - 100,
        "trade_0_fee_cost": round(cost * 0.001 * 0.6, 6),
        "trade_0_fee_currency": "USDT",
        "trade_1_id": f"TRADE-{random.randint(100000, 999999)}",
        "trade_1_amount": filled_amount * 0.4,
        "trade_1_price": avg_price,
        "trade_1_timestamp": now_ms - 50,
        "trade_1_fee_cost": round(cost * 0.001 * 0.4, 6),
        "trade_1_fee_currency": "USDT",
        "client_order_id": "my_market_buy_001",
        "info_message": "Order placed successfully",
        "info_success": True,
    }


def ccxt_cryptocurrency_exchange_server_create_spot_market_order(
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
    Places a new market order in the spot market, to be filled at the best available current price.
    API authentication (api_key, secret_key) and trading permissions on the API key are handled externally.
    Use `params` for exchange-specific order parameters like `clientOrderId` or quote order quantity.

    Args:
        amount (float): The quantity of the base currency to trade (for a market sell) or the quote currency amount
                        for a market buy (depending on exchange and params). Must be greater than 0.
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'kraken'). Case-insensitive.
        side (str): Order side: 'buy' to purchase the base asset, 'sell' to sell it.
        symbol (str): The spot market symbol to trade (e.g., 'BTC/USDT', 'ETH/EUR').
        api_key (Optional[str]): Optional API key with trading permissions.
        params (Optional[Dict[str, Any]]): Optional extra parameters for the CCXT `createOrder` call.
            Common uses include {'clientOrderId': 'your_custom_id'}, {'quoteOrderQty': 100},
            or {'createMarketBuyOrderRequiresPrice': False}.
        passphrase (Optional[str]): Optional API passphrase if required by the exchange.
        secret_key (Optional[str]): Optional secret key for API authentication.

    Returns:
        Dict[str, Any]: A dictionary containing the order details with the following structure:
            - order_id (str): Unique identifier assigned by the exchange.
            - symbol (str): Trading pair symbol.
            - side (str): 'buy' or 'sell'.
            - type (str): Always 'market'.
            - amount (float): Quantity of base asset involved.
            - price (float): Execution price.
            - average (float): Average fill price.
            - filled (float): Amount filled.
            - remaining (float): Amount remaining.
            - status (str): Current status ('open', 'closed', etc.).
            - cost (float): Total cost in quote currency.
            - timestamp (int): Unix timestamp in milliseconds.
            - datetime (str): ISO 8601 datetime string.
            - fee (Dict): Fee info with 'cost', 'currency', 'rate'.
            - trades (List[Dict]): List of individual trades with 'id', 'amount', 'price', 'timestamp', 'fee'.
            - client_order_id (str): Custom client-supplied ID if provided.
            - info (Dict): Raw response from exchange API.

    Raises:
        ValueError: If required parameters are missing or invalid.
    """
    # Input validation
    if not exchange_id:
        raise ValueError("exchange_id is required")
    if not symbol:
        raise ValueError("symbol is required")
    if side not in ["buy", "sell"]:
        raise ValueError("side must be 'buy' or 'sell'")
    if amount <= 0:
        raise ValueError("amount must be greater than 0")

    # Normalize exchange_id
    exchange_id = exchange_id.lower().strip()

    # Simulate calling external API
    api_data = call_external_api("ccxt_cryptocurrency_exchange_server_create_spot_market_order")

    # Override symbol and side from input
    api_data["symbol"] = symbol.upper()
    api_data["side"] = side
    api_data["amount"] = float(amount)

    # Handle params overrides
    client_order_id = None
    if params:
        if "clientOrderId" in params:
            client_order_id = str(params["clientOrderId"])
        elif "client_order_id" in params:
            client_order_id = str(params["client_order_id"])
        # Simulate quoteOrderQty behavior
        if "quoteOrderQty" in params and side == "buy":
            quote_qty = float(params["quoteOrderQty"])
            # Assume price is roughly current market price
            estimated_price = api_data["price"]
            base_amount = quote_qty / estimated_price
            api_data["amount"] = base_amount
            api_data["cost"] = quote_qty
        # Handle createMarketBuyOrderRequiresPrice=False (e.g., Upbit)
        if params.get("createMarketBuyOrderRequiresPrice") is False and side == "buy":
            pass

    # Construct final response
    fee = {
        "cost": api_data["fee_cost"],
        "currency": api_data["fee_currency"],
        "rate": api_data["fee_rate"]
    }

    trades = [
        {
            "id": api_data["trade_0_id"],
            "amount": api_data["trade_0_amount"],
            "price": api_data["trade_0_price"],
            "timestamp": api_data["trade_0_timestamp"],
            "fee": {
                "cost": api_data["trade_0_fee_cost"],
                "currency": api_data["trade_0_fee_currency"]
            }
        },
        {
            "id": api_data["trade_1_id"],
            "amount": api_data["trade_1_amount"],
            "price": api_data["trade_1_price"],
            "timestamp": api_data["trade_1_timestamp"],
            "fee": {
                "cost": api_data["trade_1_fee_cost"],
                "currency": api_data["trade_1_fee_currency"]
            }
        }
    ]

    info = {
        "message": api_data["info_message"],
        "success": api_data["info_success"]
    }

    result = {
        "order_id": api_data["order_id"],
        "symbol": api_data["symbol"],
        "side": api_data["side"],
        "type": "market",
        "amount": api_data["amount"],
        "price": api_data["price"],
        "average": api_data["average"],
        "filled": api_data["filled"],
        "remaining": api_data["remaining"],
        "status": api_data["status"],
        "cost": api_data["cost"],
        "timestamp": api_data["timestamp"],
        "datetime": api_data["datetime"],
        "fee": fee,
        "trades": trades,
        "client_order_id": client_order_id or api_data.get("client_order_id"),
        "info": info
    }

    return result