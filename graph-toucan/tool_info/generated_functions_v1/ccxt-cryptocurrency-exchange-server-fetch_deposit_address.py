from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching deposit address data from an external cryptocurrency exchange API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - address (str): The deposit address for the specified cryptocurrency.
        - tag (str): Memo or tag required for deposits (if applicable).
        - code (str): Currency code (e.g., 'BTC', 'USDT').
        - network (str): Blockchain network (e.g., 'ERC20', 'TRC20').
        - info_success (bool): Raw success status from exchange.
        - info_message (str): Raw message from exchange.
        - success (bool): Final success indicator.
        - message (str): Human-readable message about result.
    """
    return {
        "address": "0x742d35Cc6634C0532925a3b8D4C0c8bef8D0f8D1",
        "tag": "1234567890",
        "code": "USDT",
        "network": "ERC20",
        "info_success": True,
        "info_message": "Address generated successfully",
        "success": True,
        "message": "Deposit address retrieved successfully"
    }

def ccxt_cryptocurrency_exchange_server_fetch_deposit_address(
    code: str,
    exchange_id: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetches the deposit address for a specific cryptocurrency on a given exchange.
    
    This function simulates interaction with a cryptocurrency exchange API using CCXT.
    It returns a structured response containing the deposit address, optional tag,
    currency code, network, raw info, and success status.
    
    Args:
        code (str): Currency code to fetch the deposit address for (e.g., 'BTC', 'ETH', 'USDT').
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'kraken'). Case-insensitive.
        api_key (Optional[str]): API key for authentication. May be None if pre-configured.
        secret_key (Optional[str]): Secret key for authentication. May be None if pre-configured.
        passphrase (Optional[str]): Passphrase required by some exchanges (e.g., Coinbase).
        params (Optional[Dict[str, Any]]): Extra parameters like network (e.g., {'network': 'TRC20'}).

    Returns:
        Dict[str, Any]: A dictionary with the following keys:
            - address (str): The deposit address.
            - tag (str): Memo/tag for deposits; None if not applicable.
            - code (str): Currency code.
            - network (str): Blockchain network; None if not specified.
            - info (Dict): Raw response from the exchange.
            - success (bool): Whether the request succeeded.
            - message (str): Additional context or error information.
    """
    # Input validation
    if not code:
        return {
            "address": "",
            "tag": None,
            "code": "",
            "network": None,
            "info": {"success": False, "message": "Missing required parameter: code"},
            "success": False,
            "message": "Currency code is required."
        }
    
    if not exchange_id:
        return {
            "address": "",
            "tag": None,
            "code": code,
            "network": None,
            "info": {"success": False, "message": "Missing required parameter: exchange_id"},
            "success": False,
            "message": "Exchange ID is required."
        }

    # Simulate calling external API
    try:
        api_data = call_external_api("ccxt-cryptocurrency-exchange-server-fetch_deposit_address")
        
        # Construct nested output structure from flat API response
        result = {
            "address": api_data["address"],
            "tag": api_data["tag"] if api_data["tag"] else None,
            "code": api_data["code"],
            "network": api_data["network"] if api_data["network"] else None,
            "info": {
                "success": api_data["info_success"],
                "message": api_data["info_message"]
            },
            "success": api_data["success"],
            "message": api_data["message"]
        }
        
        # Override code and network from input if provided
        result["code"] = code
        if params and ("network" in params or "chain" in params):
            result["network"] = params.get("network") or params.get("chain")
        
        return result
        
    except Exception as e:
        return {
            "address": "",
            "tag": None,
            "code": code,
            "network": None,
            "info": {"success": False, "message": str(e)},
            "success": False,
            "message": f"Failed to fetch deposit address: {str(e)}"
        }