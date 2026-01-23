from typing import Dict, List, Any, Optional
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching public market trades from a cryptocurrency exchange via CCXT.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - trade_0_timestamp (int): Timestamp of first trade in milliseconds
        - trade_0_symbol (str): Symbol of first trade
        - trade_0_price (float): Price of first trade
        - trade_0_amount (float): Amount of first trade
        - trade_0_side (str): Side of first trade ('buy' or 'sell')
        - trade_0_id (str): Trade ID of first trade
        - trade_1_timestamp (int): Timestamp of second trade in milliseconds
        - trade_1_symbol (str): Symbol of second trade
        - trade_1_price (float): Price of second trade
        - trade_1_amount (float): Amount of second trade
        - trade_1_side (str): Side of second trade ('buy' or 'sell')
        - trade_1_id (str): Trade ID of second trade
        - exchange (str): Exchange ID in lowercase
        - output_symbol (str): The trading symbol for which trades were fetched
        - output_limit (int): The maximum number of trades applied
        - output_since (int): The since timestamp used in the request
        - fetched_at (int): Timestamp when data was fetched (UTC epoch ms)
        - has_more (bool): Whether more trades are available before 'since'
        - rate_limit_remaining (int): Number of API calls remaining
        - rate_limit_reset (int): Timestamp when rate limit resets (UTC epoch ms)
        - metadata_pagination_token (str): Pagination token if provided
        - metadata_warning (str): Any warning message from the exchange
    """
    now_ms = int(time.time() * 1000)
    since_ms = 1672531200000  # 2023-01-01T00:00:00Z
    return {
        "trade_0_timestamp": now_ms - 60000,
        "trade_0_symbol": "BTC/USDT",
        "trade_0_price": 43250.5,
        "trade_0_amount": 0.025,
        "trade_0_side": "buy",
        "trade_0_id": "t100001",
        "trade_1_timestamp": now_ms - 55000,
        "trade_1_symbol": "BTC/USDT",
        "trade_1_price": 43248.2,
        "trade_1_amount": 0.018,
        "trade_1_side": "sell",
        "trade_1_id": "t100002",
        "exchange": "binance",
        "output_symbol": "BTC/USDT",
        "output_limit": 100,
        "output_since": since_ms,
        "fetched_at": now_ms,
        "has_more": True,
        "rate_limit_remaining": 118,
        "rate_limit_reset": now_ms + 1000,
        "metadata_pagination_token": "nextpage_abc123",
        "metadata_warning": "Partial data due to high load"
    }


def ccxt_cryptocurrency_exchange_server_fetch_public_market_trades(
    exchange_id: str,
    symbol: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    limit: Optional[int] = None,
    since: Optional[int] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetches recent public trades for a specific trading symbol from a cryptocurrency exchange.
    
    This function simulates interaction with a cryptocurrency exchange using the CCXT library
    to retrieve public market trades. It does not perform actual network requests but returns
    realistic synthetic data structured according to the CCXT trade format.
    
    Args:
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'kraken'). Case-insensitive.
        symbol (str): The symbol to fetch public trades for (e.g., 'BTC/USDT').
        api_key (Optional[str]): Optional API key for authentication.
        secret_key (Optional[str]): Optional secret key for authentication.
        passphrase (Optional[str]): Optional passphrase if required by exchange.
        limit (Optional[int]): Maximum number of trades to fetch.
        since (Optional[int]): Timestamp in milliseconds to fetch trades since.
        params (Optional[Dict[str, Any]]): Extra parameters for client or API call.
    
    Returns:
        Dict containing:
        - trades (List[Dict]): List of individual trade records with timestamp, symbol, price,
          amount, side, and trade ID.
        - exchange (str): Exchange ID in lowercase.
        - symbol (str): Trading symbol.
        - limit (int): Maximum number of trades applied.
        - since (int): Timestamp indicating earliest time in results.
        - fetched_at (int): Timestamp when data was fetched (UTC epoch ms).
        - has_more (bool): Whether more trades are available before 'since'.
        - rate_limit_remaining (int): Remaining API calls before rate limit.
        - rate_limit_reset (int): When rate limit will reset (UTC epoch ms).
        - metadata (Dict): Additional exchange-specific metadata.
    
    Raises:
        ValueError: If required parameters are missing or invalid.
    """
    # Input validation
    if not exchange_id:
        raise ValueError("exchange_id is required")
    if not symbol:
        raise ValueError("symbol is required")
    
    if limit is not None and (not isinstance(limit, int) or limit <= 0):
        raise ValueError("limit must be a positive integer")
    
    if since is not None and (not isinstance(since, int) or since < 0):
        raise ValueError("since must be a non-negative integer timestamp in milliseconds")
    
    # Normalize exchange ID
    exchange = exchange_id.strip().lower()
    
    # Use provided limit or default to 100
    applied_limit = limit if limit is not None else 100
    
    # Use provided since or default to 24 hours ago
    applied_since = since if since is not None else int(time.time() * 1000) - (24 * 60 * 60 * 1000)
    
    # Call simulated external API
    api_data = call_external_api("ccxt-cryptocurrency-exchange-server-fetch_public_market_trades")
    
    # Construct trades list from indexed fields
    trades = [
        {
            "timestamp": api_data["trade_0_timestamp"],
            "symbol": api_data["trade_0_symbol"],
            "price": api_data["trade_0_price"],
            "amount": api_data["trade_0_amount"],
            "side": api_data["trade_0_side"],
            "id": api_data["trade_0_id"]
        },
        {
            "timestamp": api_data["trade_1_timestamp"],
            "symbol": api_data["trade_1_symbol"],
            "price": api_data["trade_1_price"],
            "amount": api_data["trade_1_amount"],
            "side": api_data["trade_1_side"],
            "id": api_data["trade_1_id"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "pagination_token": api_data["metadata_pagination_token"],
        "warning": api_data["metadata_warning"]
    }
    
    # Build final result matching output schema
    result = {
        "trades": trades,
        "exchange": api_data["exchange"],
        "symbol": api_data["output_symbol"],
        "limit": api_data["output_limit"],
        "since": api_data["output_since"],
        "fetched_at": api_data["fetched_at"],
        "has_more": api_data["has_more"],
        "rate_limit_remaining": api_data["rate_limit_remaining"],
        "rate_limit_reset": api_data["rate_limit_reset"],
        "metadata": metadata
    }
    
    return result