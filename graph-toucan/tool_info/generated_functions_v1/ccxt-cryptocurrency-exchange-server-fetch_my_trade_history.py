from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching trade history data from an external cryptocurrency exchange API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - trade_0_id (str): ID of the first trade
        - trade_0_symbol (str): Symbol of the first trade (e.g., 'BTC/USDT')
        - trade_0_timestamp (int): Unix timestamp in milliseconds for the first trade
        - trade_0_datetime (str): ISO formatted datetime string for the first trade
        - trade_0_side (str): Side of the first trade ('buy' or 'sell')
        - trade_0_price (float): Price at which the first trade was executed
        - trade_0_amount (float): Amount of base currency traded in the first trade
        - trade_0_cost (float): Total cost (price * amount) of the first trade
        - trade_0_fee_cost (float): Fee amount for the first trade
        - trade_0_fee_currency (str): Currency in which fee was paid for the first trade
        - trade_0_order (str): Order ID associated with the first trade
        - trade_1_id (str): ID of the second trade
        - trade_1_symbol (str): Symbol of the second trade
        - trade_1_timestamp (int): Unix timestamp in milliseconds for the second trade
        - trade_1_datetime (str): ISO formatted datetime string for the second trade
        - trade_1_side (str): Side of the second trade ('buy' or 'sell')
        - trade_1_price (float): Price at which the second trade was executed
        - trade_1_amount (float): Amount of base currency traded in the second trade
        - trade_1_cost (float): Total cost (price * amount) of the second trade
        - trade_1_fee_cost (float): Fee amount for the second trade
        - trade_1_fee_currency (str): Currency in which fee was paid for the second trade
        - trade_1_order (str): Order ID associated with the second trade
        - total_count (int): Total number of trades returned
        - exchange (str): Exchange ID from which data was fetched
        - query_params_applied_symbol (str): Symbol used in filtering
        - query_params_applied_since (int): Timestamp used as 'since' filter
        - query_params_applied_limit (int): Limit applied in the query
        - query_params_applied_params (str): JSON string of additional params used
        - rate_limit_info_remaining_requests (int): Number of remaining requests allowed
        - rate_limit_info_reset_time (int): Unix timestamp when rate limit resets
        - success (bool): Whether the operation succeeded
        - error_message (str): Error message if failed, otherwise empty string
    """
    return {
        "trade_0_id": "t123456789",
        "trade_0_symbol": "BTC/USDT",
        "trade_0_timestamp": 1672531200000,
        "trade_0_datetime": "2023-01-01T00:00:00.000Z",
        "trade_0_side": "buy",
        "trade_0_price": 16800.5,
        "trade_0_amount": 0.001,
        "trade_0_cost": 16.8005,
        "trade_0_fee_cost": 0.0168,
        "trade_0_fee_currency": "USDT",
        "trade_0_order": "o987654321",
        "trade_1_id": "t123456790",
        "trade_1_symbol": "ETH/USDT",
        "trade_1_timestamp": 1672531260000,
        "trade_1_datetime": "2023-01-01T00:01:00.000Z",
        "trade_1_side": "sell",
        "trade_1_price": 1200.3,
        "trade_1_amount": 0.05,
        "trade_1_cost": 60.015,
        "trade_1_fee_cost": 0.06,
        "trade_1_fee_currency": "USDT",
        "trade_1_order": "o987654322",
        "total_count": 2,
        "exchange": "binance",
        "query_params_applied_symbol": "BTC/USDT",
        "query_params_applied_since": 1672531200000,
        "query_params_applied_limit": 100,
        "query_params_applied_params": '{"options": {"defaultType": "future"}}',
        "rate_limit_info_remaining_requests": 98,
        "rate_limit_info_reset_time": 1672534800000,
        "success": True,
        "error_message": ""
    }

def ccxt_cryptocurrency_exchange_server_fetch_my_trade_history(
    exchange_id: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    symbol: Optional[str] = None,
    since: Optional[int] = None,
    limit: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetches the history of your executed trades (fills) for an account, optionally filtered by symbol, time, and limit.
    
    This function simulates interaction with a cryptocurrency exchange via CCXT, using external API simulation.
    Authentication is assumed to be handled externally. For non-spot markets, ensure params include proper configuration.
    
    Args:
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'ftx'). Case-insensitive.
        api_key (Optional[str]): Your API key. If not provided, pre-configured credentials may be used.
        secret_key (Optional[str]): Your secret key. Used with api_key for authentication.
        passphrase (Optional[str]): API passphrase if required by the exchange.
        symbol (Optional[str]): The symbol to fetch trades for (e.g., 'BTC/USDT'). If None, all symbols.
        since (Optional[int]): Timestamp in milliseconds (UTC epoch) to fetch trades since.
        limit (Optional[int]): Maximum number of trades to retrieve.
        params (Optional[Dict[str, Any]]): Extra parameters for CCXT client or fetchMyTrades call.
    
    Returns:
        Dict containing:
        - trades (List[Dict]): List of individual trade records with details.
        - total_count (int): Total number of trades returned.
        - exchange (str): The exchange ID from which data was fetched.
        - query_params_applied (Dict): Filtering parameters applied in the request.
        - rate_limit_info (Dict): Rate-limiting metadata if available.
        - success (bool): Whether the operation completed successfully.
        - error_message (str): Error description if failed, else None.
    """
    # Validate required input
    if not exchange_id:
        return {
            "trades": [],
            "total_count": 0,
            "exchange": "",
            "query_params_applied": {},
            "rate_limit_info": {},
            "success": False,
            "error_message": "exchange_id is required"
        }

    try:
        # Call simulated external API
        api_data = call_external_api("ccxt-cryptocurrency-exchange-server-fetch_my_trade_history")

        # Construct trades list from indexed fields
        trades = [
            {
                "id": api_data["trade_0_id"],
                "symbol": api_data["trade_0_symbol"],
                "timestamp": api_data["trade_0_timestamp"],
                "datetime": api_data["trade_0_datetime"],
                "side": api_data["trade_0_side"],
                "price": api_data["trade_0_price"],
                "amount": api_data["trade_0_amount"],
                "cost": api_data["trade_0_cost"],
                "fee": {
                    "cost": api_data["trade_0_fee_cost"],
                    "currency": api_data["trade_0_fee_currency"]
                },
                "order": api_data["trade_0_order"]
            },
            {
                "id": api_data["trade_1_id"],
                "symbol": api_data["trade_1_symbol"],
                "timestamp": api_data["trade_1_timestamp"],
                "datetime": api_data["trade_1_datetime"],
                "side": api_data["trade_1_side"],
                "price": api_data["trade_1_price"],
                "amount": api_data["trade_1_amount"],
                "cost": api_data["trade_1_cost"],
                "fee": {
                    "cost": api_data["trade_1_fee_cost"],
                    "currency": api_data["trade_1_fee_currency"]
                },
                "order": api_data["trade_1_order"]
            }
        ]

        # Construct query params applied
        query_params_applied = {
            "symbol": api_data["query_params_applied_symbol"],
            "since": api_data["query_params_applied_since"],
            "limit": api_data["query_params_applied_limit"],
            "params": api_data["query_params_applied_params"]
        }

        # Construct rate limit info
        rate_limit_info = {
            "remaining_requests": api_data["rate_limit_info_remaining_requests"],
            "reset_time": api_data["rate_limit_info_reset_time"]
        }

        # Return final response
        return {
            "trades": trades,
            "total_count": api_data["total_count"],
            "exchange": api_data["exchange"],
            "query_params_applied": query_params_applied,
            "rate_limit_info": rate_limit_info,
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }

    except Exception as e:
        return {
            "trades": [],
            "total_count": 0,
            "exchange": exchange_id,
            "query_params_applied": {},
            "rate_limit_info": {},
            "success": False,
            "error_message": str(e)
        }