from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for token lookup by symbol.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_0_address (str): Address of the first matching token
        - data_0_name (str): Name of the first matching token
        - data_0_symbol (str): Symbol of the first matching token
        - data_0_token_type (str): Type of the first token (e.g., ERC-20)
        - data_0_total_supply (str): Total supply of the first token as string
        - data_0_circulating_market_cap (float): Circulating market cap of the first token
        - data_0_exchange_rate (float): Exchange rate of the first token
        - data_0_is_smart_contract_verified (bool): Verification status of the first token contract
        - data_0_is_verified_via_admin_panel (bool): Admin panel verification status of the first token
        - data_1_address (str): Address of the second matching token
        - data_1_name (str): Name of the second matching token
        - data_1_symbol (str): Symbol of the second matching token
        - data_1_token_type (str): Type of the second token (e.g., ERC-20)
        - data_1_total_supply (str): Total supply of the second token as string
        - data_1_circulating_market_cap (float): Circulating market cap of the second token
        - data_1_exchange_rate (float): Exchange rate of the second token
        - data_1_is_smart_contract_verified (bool): Verification status of the second token contract
        - data_1_is_verified_via_admin_panel (bool): Admin panel verification status of the second token
        - data_description (str): Description of the returned data
        - notes_0 (str): First note about the results
        - notes_1 (str): Second note about the results
        - instructions (str): Instructions from the API on how to interpret results
        - pagination_next_page (int): Next page number for pagination
        - pagination_prev_page (int): Previous page number for pagination
        - pagination_current_page (int): Current page number
        - pagination_per_page (int): Number of results per page
    """
    return {
        "data_0_address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        "data_0_name": "Uniswap",
        "data_0_symbol": "UNI",
        "data_0_token_type": "ERC-20",
        "data_0_total_supply": "1000000000",
        "data_0_circulating_market_cap": 5200000000.0,
        "data_0_exchange_rate": 5.2,
        "data_0_is_smart_contract_verified": True,
        "data_0_is_verified_via_admin_panel": False,
        "data_1_address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "data_1_name": "Dai Stablecoin",
        "data_1_symbol": "DAI",
        "data_1_token_type": "ERC-20",
        "data_1_total_supply": "1200000000",
        "data_1_circulating_market_cap": 1200000000.0,
        "data_1_exchange_rate": 1.0,
        "data_1_is_smart_contract_verified": True,
        "data_1_is_verified_via_admin_panel": True,
        "data_description": "List of tokens matching the provided symbol or name",
        "notes_0": "Results are limited to the first 10 matches.",
        "notes_1": "Market cap and exchange rate values are approximate and updated hourly.",
        "instructions": "Use the token address to query further details about the token.",
        "pagination_next_page": 2,
        "pagination_prev_page": None,
        "pagination_current_page": 1,
        "pagination_per_page": 10
    }

def blockscout_mcp_server_lookup_token_by_symbol(chain_id: str, symbol: str) -> Dict[str, Any]:
    """
    Search for token addresses by symbol or name using the Blockscout API.

    This function simulates querying the Blockscout server to find tokens
    based on symbol or name similarity. It returns up to two matching tokens
    with detailed information including address, name, symbol, type, supply,
    market cap, exchange rate, and verification status.

    Args:
        chain_id (str): The ID of the blockchain (e.g., '1' for Ethereum Mainnet)
        symbol (str): Token symbol or name to search for

    Returns:
        Dict containing:
        - data (List[Dict]): List of token objects with fields 'address', 'name',
          'symbol', 'token_type', 'total_supply', 'circulating_market_cap',
          'exchange_rate', 'is_smart_contract_verified', 'is_verified_via_admin_panel'
        - data_description (str): Description of the returned data
        - notes (List[str]): Additional notes about the results
        - instructions (str): Instructions from the API on how to proceed
        - pagination (Dict): Pagination information with keys 'next_page',
          'prev_page', 'current_page', 'per_page'

    Raises:
        ValueError: If chain_id or symbol is empty
    """
    if not chain_id:
        raise ValueError("chain_id is required")
    if not symbol:
        raise ValueError("symbol is required")

    api_data = call_external_api("blockscout-mcp-server-lookup_token_by_symbol")

    # Construct data list from indexed fields
    data = [
        {
            "address": api_data["data_0_address"],
            "name": api_data["data_0_name"],
            "symbol": api_data["data_0_symbol"],
            "token_type": api_data["data_0_token_type"],
            "total_supply": api_data["data_0_total_supply"],
            "circulating_market_cap": api_data["data_0_circulating_market_cap"],
            "exchange_rate": api_data["data_0_exchange_rate"],
            "is_smart_contract_verified": api_data["data_0_is_smart_contract_verified"],
            "is_verified_via_admin_panel": api_data["data_0_is_verified_via_admin_panel"]
        },
        {
            "address": api_data["data_1_address"],
            "name": api_data["data_1_name"],
            "symbol": api_data["data_1_symbol"],
            "token_type": api_data["data_1_token_type"],
            "total_supply": api_data["data_1_total_supply"],
            "circulating_market_cap": api_data["data_1_circulating_market_cap"],
            "exchange_rate": api_data["data_1_exchange_rate"],
            "is_smart_contract_verified": api_data["data_1_is_smart_contract_verified"],
            "is_verified_via_admin_panel": api_data["data_1_is_verified_via_admin_panel"]
        }
    ]

    # Construct pagination dict
    pagination = {
        "next_page": api_data["pagination_next_page"] if api_data["pagination_next_page"] is not None else None,
        "prev_page": api_data["pagination_prev_page"] if api_data["pagination_prev_page"] is not None else None,
        "current_page": api_data["pagination_current_page"],
        "per_page": api_data["pagination_per_page"]
    }

    result = {
        "data": data,
        "data_description": api_data["data_description"],
        "notes": [api_data["notes_0"], api_data["notes_1"]],
        "instructions": api_data["instructions"],
        "pagination": pagination
    }

    return result