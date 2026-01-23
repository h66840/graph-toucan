from typing import Dict, List, Any, Optional
import time

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching open derivative positions from a cryptocurrency exchange via CCXT.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - positions_0_symbol (str): Symbol of first position
        - positions_0_type (str): Type of first position ('long' or 'short')
        - positions_0_contracts (float): Number of contracts for first position
        - positions_0_contractSize (float): Size per contract for first position
        - positions_0_entryPrice (float): Entry price for first position
        - positions_0_markPrice (float): Current mark price for first position
        - positions_0_notional (float): Notional value of first position
        - positions_0_collateral (float): Collateral used for first position
        - positions_0_maintenanceMargin (float): Maintenance margin for first position
        - positions_0_leverage (float): Leverage applied to first position
        - positions_0_liquidationPrice (float): Liquidation price for first position
        - positions_0_unrealizedPnl (float): Unrealized PnL for first position
        - positions_0_percentage (float): ROI percentage for first position
        - positions_0_side (str): Side of first position ('long' or 'short')
        - positions_0_hedged (bool): Whether first position is hedged
        - positions_0_timestamp (int): Timestamp in ms when first position was opened
        - positions_0_initialMargin (float): Initial margin for first position
        - positions_0_marginMode (str): Margin mode for first position ('cross' or 'isolated')
        - positions_0_info_exchangeSpecific (str): Example exchange-specific field for first position
        - positions_1_symbol (str): Symbol of second position
        - positions_1_type (str): Type of second position ('long' or 'short')
        - positions_1_contracts (float): Number of contracts for second position
        - positions_1_contractSize (float): Size per contract for second position
        - positions_1_entryPrice (float): Entry price for second position
        - positions_1_markPrice (float): Current mark price for second position
        - positions_1_notional (float): Notional value of second position
        - positions_1_collateral (float): Collateral used for second position
        - positions_1_maintenanceMargin (float): Maintenance margin for second position
        - positions_1_leverage (float): Leverage applied to second position
        - positions_1_liquidationPrice (float): Liquidation price for second position
        - positions_1_unrealizedPnl (float): Unrealized PnL for second position
        - positions_1_percentage (float): ROI percentage for second position
        - positions_1_side (str): Side of second position ('long' or 'short')
        - positions_1_hedged (bool): Whether second position is hedged
        - positions_1_timestamp (int): Timestamp in ms when second position was opened
        - positions_1_initialMargin (float): Initial margin for second position
        - positions_1_marginMode (str): Margin mode for second position ('cross' or 'isolated')
        - positions_1_info_exchangeSpecific (str): Example exchange-specific field for second position
        - total_positions (int): Total number of open positions returned
        - exchange (str): Exchange ID normalized to lowercase
        - fetched_at (int): Timestamp in milliseconds when data was fetched (UTC)
        - market_type (str): Derivatives market type used (e.g., 'future', 'swap')
    """
    return {
        "positions_0_symbol": "BTC/USDT:USDT",
        "positions_0_type": "long",
        "positions_0_contracts": 1.25,
        "positions_0_contractSize": 1.0,
        "positions_0_entryPrice": 43200.0,
        "positions_0_markPrice": 43850.5,
        "positions_0_notional": 54813.125,
        "positions_0_collateral": 2740.66,
        "positions_0_maintenanceMargin": 137.03,
        "positions_0_leverage": 20.0,
        "positions_0_liquidationPrice": 41000.25,
        "positions_0_unrealizedPnl": 812.34,
        "positions_0_percentage": 2.96,
        "positions_0_side": "long",
        "positions_0_hedged": True,
        "positions_0_timestamp": 1700000000000,
        "positions_0_initialMargin": 2740.66,
        "positions_0_marginMode": "cross",
        "positions_0_info_exchangeSpecific": "futures_v2",

        "positions_1_symbol": "ETH/USDT:USDT",
        "positions_1_type": "short",
        "positions_1_contracts": 3.5,
        "positions_1_contractSize": 1.0,
        "positions_1_entryPrice": 2650.0,
        "positions_1_markPrice": 2620.75,
        "positions_1_notional": 9172.625,
        "positions_1_collateral": 458.63,
        "positions_1_maintenanceMargin": 22.93,
        "positions_1_leverage": 25.0,
        "positions_1_liquidationPrice": 2780.15,
        "positions_1_unrealizedPnl": 102.68,
        "positions_1_percentage": 2.23,
        "positions_1_side": "short",
        "positions_1_hedged": False,
        "positions_1_timestamp": 1700000000000,
        "positions_1_initialMargin": 458.63,
        "positions_1_marginMode": "isolated",
        "positions_1_info_exchangeSpecific": "swap_linear",

        "total_positions": 2,
        "exchange": "binance",
        "fetched_at": int(time.time() * 1000),
        "market_type": "swap"
    }

def ccxt_cryptocurrency_exchange_server_fetch_open_positions(
    exchange_id: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetches currently open positions for futures, swaps, or other derivatives from a cryptocurrency exchange.
    
    This function simulates interaction with a CCXT client to retrieve open derivative positions.
    The CCXT client must be initialized with the correct market type (e.g., futures, swap) via params.
    
    Args:
        exchange_id (str): The ID of the exchange that supports derivatives trading (e.g., 'binance', 'bybit', 'okx'). Case-insensitive.
        api_key (Optional[str]): Optional API key for the exchange. Authentication is required.
        secret_key (Optional[str]): Optional secret key for the exchange. Used with API key if required.
        passphrase (Optional[str]): Optional passphrase, if required by the exchange (e.g., OKX).
        params (Optional[Dict[str, Any]]): Optional parameters for CCXT client instantiation and API call.
            - For client init: Use {'options': {'defaultType': 'future'}} or similar to set market type.
            - For API call: Can include filters like {'symbol': 'BTC/USDT:USDT'} or {'symbols': [...]}.

    Returns:
        Dict containing:
            - positions (List[Dict]): List of open derivative positions with detailed fields including symbol, type, size, entry price,
              mark price, notional, collateral, maintenance margin, leverage, liquidation price, unrealized PnL, ROI percentage,
              side, hedged status, timestamp, initial margin, margin mode, and exchange-specific info.
            - total_positions (int): Total number of open positions returned.
            - exchange (str): Exchange ID normalized to lowercase.
            - fetched_at (int): Timestamp in milliseconds when the data was fetched (UTC).
            - market_type (str): The derivatives market type used (e.g., 'future', 'swap').

    Example:
        >>> result = ccxt_cryptocurrency_exchange_server_fetch_open_positions('binance', params={'options': {'defaultType': 'swap'}})
        >>> print(result['total_positions'])
        2
    """
    # Input validation
    if not exchange_id:
        raise ValueError("exchange_id is required")
    
    # Normalize exchange ID to lowercase
    normalized_exchange = exchange_id.strip().lower()
    
    # Determine market type from params if provided
    market_type = "swap"  # default fallback
    if params and isinstance(params, dict):
        options = params.get("options", {})
        if isinstance(options, dict):
            market_type = options.get("defaultType", market_type)
    else:
        # Default to 'swap' if not specified
        pass

    # Simulate calling external API
    api_response = call_external_api("fetch_open_positions")
    
    # Extract positions from response
    total_positions = api_response.get("total_positions", 0)
    positions = []
    
    for i in range(total_positions):
        prefix = f"positions_{i}_"
        position = {
            "symbol": api_response.get(f"{prefix}symbol"),
            "type": api_response.get(f"{prefix}type"),
            "contracts": api_response.get(f"{prefix}contracts"),
            "contractSize": api_response.get(f"{prefix}contractSize"),
            "entryPrice": api_response.get(f"{prefix}entryPrice"),
            "markPrice": api_response.get(f"{prefix}markPrice"),
            "notional": api_response.get(f"{prefix}notional"),
            "collateral": api_response.get(f"{prefix}collateral"),
            "maintenanceMargin": api_response.get(f"{prefix}maintenanceMargin"),
            "leverage": api_response.get(f"{prefix}leverage"),
            "liquidationPrice": api_response.get(f"{prefix}liquidationPrice"),
            "unrealizedPnl": api_response.get(f"{prefix}unrealizedPnl"),
            "percentage": api_response.get(f"{prefix}percentage"),
            "side": api_response.get(f"{prefix}side"),
            "hedged": api_response.get(f"{prefix}hedged"),
            "timestamp": api_response.get(f"{prefix}timestamp"),
            "initialMargin": api_response.get(f"{prefix}initialMargin"),
            "marginMode": api_response.get(f"{prefix}marginMode"),
            "info": {
                "exchangeSpecific": api_response.get(f"{prefix}info_exchangeSpecific")
            }
        }
        positions.append(position)
    
    # Build final result
    result = {
        "positions": positions,
        "total_positions": total_positions,
        "exchange": api_response.get("exchange"),
        "fetched_at": api_response.get("fetched_at"),
        "market_type": api_response.get("market_type", market_type)
    }
    
    return result