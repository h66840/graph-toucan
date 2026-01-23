from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching token holdings data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - data_0_address (str): Token contract address for first token
        - data_0_name (str): Name of first token
        - data_0_symbol (str): Symbol of first token
        - data_0_decimals (int): Decimals of first token
        - data_0_total_supply (str): Total supply of first token as string
        - data_0_circulating_market_cap (float): Circulating market cap of first token
        - data_0_exchange_rate (float): Exchange rate (price) of first token
        - data_0_holders_count (int): Number of holders for first token
        - data_0_balance (str): Balance of first token held by address
        - data_1_address (str): Token contract address for second token
        - data_1_name (str): Name of second token
        - data_1_symbol (str): Symbol of second token
        - data_1_decimals (int): Decimals of second token
        - data_1_total_supply (str): Total supply of second token as string
        - data_1_circulating_market_cap (float): Circulating market cap of second token
        - data_1_exchange_rate (float): Exchange rate (price) of second token
        - data_1_holders_count (int): Number of holders for second token
        - data_1_balance (str): Balance of second token held by address
        - data_description (str): Description of the data returned
        - notes (str): Additional notes about the response
        - instructions_0 (str): First instruction message (e.g., pagination guidance)
        - instructions_1 (str): Second instruction message
        - pagination_next_call_tool_name (str): Tool name for next page call
        - pagination_next_call_params_chain_id (str): Chain ID for next page call
        - pagination_next_call_params_address (str): Address for next page call
        - pagination_next_call_params_cursor (str): Cursor for next page call
    """
    return {
        "data_0_address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
        "data_0_name": "Uniswap",
        "data_0_symbol": "UNI",
        "data_0_decimals": 18,
        "data_0_total_supply": "1000000000000000000000000000",
        "data_0_circulating_market_cap": 5234567890.12,
        "data_0_exchange_rate": 5.23,
        "data_0_holders_count": 456789,
        "data_0_balance": "1000000000000000000",
        "data_1_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "data_1_name": "USD Coin",
        "data_1_symbol": "USDC",
        "data_1_decimals": 6,
        "data_1_total_supply": "1123581321345589144233377610",
        "data_1_circulating_market_cap": 34000000000.0,
        "data_1_exchange_rate": 1.0,
        "data_1_holders_count": 1234567,
        "data_1_balance": "500000000",
        "data_description": "ERC20 token holdings for the given address with market data",
        "notes": "Balance values are raw and not adjusted by decimals",
        "instructions_0": "Results are paginated. Use the next_call to retrieve the next page.",
        "instructions_1": "Ensure chain_id matches the network of the address.",
        "pagination_next_call_tool_name": "blockscout-mcp-server-get_tokens_by_address",
        "pagination_next_call_params_chain_id": "1",
        "pagination_next_call_params_address": "0x742d35Cc6634C0532925a3b8D4C0cD2D4C0cD2D4",
        "pagination_next_call_params_cursor": "abc123xyz"
    }

def blockscout_mcp_server_get_tokens_by_address(
    address: str, 
    chain_id: str, 
    cursor: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get comprehensive ERC20 token holdings for an address with enriched metadata and market data.
    
    This function retrieves detailed token information including contract details (name, symbol, decimals),
    market metrics (exchange rate, market cap, volume), holders count, and actual balance (raw, not adjusted by decimals).
    It supports pagination via the cursor parameter.
    
    Args:
        address (str): Wallet address to query token holdings for
        chain_id (str): The ID of the blockchain network
        cursor (Optional[str]): Pagination cursor from previous response to get next page of results
        
    Returns:
        Dict containing:
        - data (List[Dict]): List of token holdings with fields: address, name, symbol, decimals, 
          total_supply, circulating_market_cap, exchange_rate, holders_count, balance
        - data_description (Optional[str]): Description of the data returned
        - notes (Optional[str]): Additional notes about the response
        - instructions (List[str]): List of instructional messages for further interaction
        - pagination (Optional[Dict]): Contains next_call object with tool_name and params for next page
        
    Raises:
        ValueError: If address or chain_id is empty or invalid
    """
    # Input validation
    if not address:
        raise ValueError("Address is required")
    if not chain_id:
        raise ValueError("Chain ID is required")
    
    # Call external API (simulated)
    api_data = call_external_api("blockscout-mcp-server-get_tokens_by_address")
    
    # Construct data list from indexed fields
    data = [
        {
            "address": api_data["data_0_address"],
            "name": api_data["data_0_name"],
            "symbol": api_data["data_0_symbol"],
            "decimals": api_data["data_0_decimals"],
            "total_supply": api_data["data_0_total_supply"],
            "circulating_market_cap": api_data["data_0_circulating_market_cap"],
            "exchange_rate": api_data["data_0_exchange_rate"],
            "holders_count": api_data["data_0_holders_count"],
            "balance": api_data["data_0_balance"]
        },
        {
            "address": api_data["data_1_address"],
            "name": api_data["data_1_name"],
            "symbol": api_data["data_1_symbol"],
            "decimals": api_data["data_1_decimals"],
            "total_supply": api_data["data_1_total_supply"],
            "circulating_market_cap": api_data["data_1_circulating_market_cap"],
            "exchange_rate": api_data["data_1_exchange_rate"],
            "holders_count": api_data["data_1_holders_count"],
            "balance": api_data["data_1_balance"]
        }
    ]
    
    # Construct instructions list
    instructions = [
        api_data["instructions_0"],
        api_data["instructions_1"]
    ]
    
    # Construct pagination object if next page exists
    pagination = {
        "next_call": {
            "tool_name": api_data["pagination_next_call_tool_name"],
            "params": {
                "chain_id": api_data["pagination_next_call_params_chain_id"],
                "address": api_data["pagination_next_call_params_address"],
                "cursor": api_data["pagination_next_call_params_cursor"]
            }
        }
    }
    
    # Return final structured response
    return {
        "data": data,
        "data_description": api_data["data_description"],
        "notes": api_data["notes"],
        "instructions": instructions,
        "pagination": pagination
    }