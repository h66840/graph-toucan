from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DefiLlama protocol TVL data.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - tvl_history_0_date (int): Unix timestamp for first TVL data point
        - tvl_history_0_totalLiquidityUSD (float): TVL in USD for first point
        - tvl_history_1_date (int): Unix timestamp for second TVL data point
        - tvl_history_1_totalLiquidityUSD (float): TVL in USD for second point
        - chain_0 (str): First chain where protocol operates
        - chain_1 (str): Second chain where protocol operates
        - token_0_symbol (str): Symbol of first token in TVL breakdown
        - token_0_address (str): Contract address of first token
        - token_0_chain (str): Chain of first token
        - token_0_amount (float): Amount of first token
        - token_1_symbol (str): Symbol of second token in TVL breakdown
        - token_1_address (str): Contract address of second token
        - token_1_chain (str): Chain of second token
        - token_1_amount (float): Amount of second token
        - category (str): DeFi category of the protocol
        - name (str): Full name of the protocol
        - slug (str): Unique identifier slug for the protocol
        - fetched_at (int): Unix timestamp when data was fetched
        - chain_tvls_chain_0_0_date (int): First date for chain 0 TVL series
        - chain_tvls_chain_0_0_totalLiquidityUSD (float): TVL value for chain 0 first point
        - chain_tvls_chain_0_1_date (int): Second date for chain 0 TVL series
        - chain_tvls_chain_0_1_totalLiquidityUSD (float): TVL value for chain 0 second point
        - chain_tvls_chain_1_0_date (int): First date for chain 1 TVL series
        - chain_tvls_chain_1_0_totalLiquidityUSD (float): TVL value for chain 1 first point
        - chain_tvls_chain_1_1_date (int): Second date for chain 1 TVL series
        - chain_tvls_chain_1_1_totalLiquidityUSD (float): TVL value for chain 1 second point
        - token_breakdowns_chain_0_token_0_date (int): Date for token breakdown on chain 0
        - token_breakdowns_chain_0_token_0_value (float): Value for token breakdown on chain 0
        - token_breakdowns_chain_1_token_0_date (int): Date for token breakdown on chain 1
        - token_breakdowns_chain_1_token_0_value (float): Value for token breakdown on chain 1
    """
    return {
        "tvl_history_0_date": 1672531200,
        "tvl_history_0_totalLiquidityUSD": 150000000.0,
        "tvl_history_1_date": 1672617600,
        "tvl_history_1_totalLiquidityUSD": 155000000.0,
        "chain_0": "Ethereum",
        "chain_1": "Arbitrum",
        "token_0_symbol": "USDC",
        "token_0_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "token_0_chain": "Ethereum",
        "token_0_amount": 75000000.0,
        "token_1_symbol": "USDT",
        "token_1_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "token_1_chain": "Ethereum",
        "token_1_amount": 75000000.0,
        "category": "Dexes",
        "name": "Uniswap",
        "slug": "uniswap",
        "fetched_at": 1672620000,
        "chain_tvls_chain_0_0_date": 1672531200,
        "chain_tvls_chain_0_0_totalLiquidityUSD": 120000000.0,
        "chain_tvls_chain_0_1_date": 1672617600,
        "chain_tvls_chain_0_1_totalLiquidityUSD": 125000000.0,
        "chain_tvls_chain_1_0_date": 1672531200,
        "chain_tvls_chain_1_0_totalLiquidityUSD": 30000000.0,
        "chain_tvls_chain_1_1_date": 1672617600,
        "chain_tvls_chain_1_1_totalLiquidityUSD": 30000000.0,
        "token_breakdowns_chain_0_token_0_date": 1672531200,
        "token_breakdowns_chain_0_token_0_value": 60000000.0,
        "token_breakdowns_chain_1_token_0_date": 1672531200,
        "token_breakdowns_chain_1_token_0_value": 15000000.0
    }

def defillama_api_server_get_protocol_by_protocol(protocol: str) -> Dict[str, Any]:
    """
    Get historical TVL of a protocol and breakdowns by token and chain.
    
    Args:
        protocol (str): The protocol slug (e.g., 'uniswap', 'aave') to fetch data for.
        
    Returns:
        Dict containing:
        - tvl_history (List[Dict]): List of timestamp-value pairs with 'date' and 'totalLiquidityUSD'
        - chains (List[str]): List of blockchain networks where the protocol operates
        - tokens (List[Dict]): Breakdown of tokens with 'symbol', 'address', 'chain', and 'amount'
        - category (str): The DeFi category of the protocol
        - name (str): Full name of the protocol
        - slug (str): Unique identifier slug for the protocol
        - fetched_at (int): Unix timestamp when data was fetched
        - chain_tvls (Dict): Mapping of chain names to TVL time series
        - token_breakdowns (Dict): Per-chain or per-token liquidity breakdowns
        
    Raises:
        ValueError: If protocol parameter is empty or not a string
    """
    if not protocol or not isinstance(protocol, str):
        raise ValueError("Protocol parameter must be a non-empty string")
    
    # Fetch simulated external API data
    api_data = call_external_api("defillama_api_server_get_protocol_by_protocol")
    
    # Construct tvl_history list
    tvl_history = [
        {
            "date": api_data["tvl_history_0_date"],
            "totalLiquidityUSD": api_data["tvl_history_0_totalLiquidityUSD"]
        },
        {
            "date": api_data["tvl_history_1_date"],
            "totalLiquidityUSD": api_data["tvl_history_1_totalLiquidityUSD"]
        }
    ]
    
    # Construct chains list
    chains = [
        api_data["chain_0"],
        api_data["chain_1"]
    ]
    
    # Construct tokens list
    tokens = [
        {
            "symbol": api_data["token_0_symbol"],
            "address": api_data["token_0_address"],
            "chain": api_data["token_0_chain"],
            "amount": api_data["token_0_amount"]
        },
        {
            "symbol": api_data["token_1_symbol"],
            "address": api_data["token_1_address"],
            "chain": api_data["token_1_chain"],
            "amount": api_data["token_1_amount"]
        }
    ]
    
    # Construct chain_tvls dictionary
    chain_tvls = {
        api_data["chain_0"]: [
            {
                "date": api_data["chain_tvls_chain_0_0_date"],
                "totalLiquidityUSD": api_data["chain_tvls_chain_0_0_totalLiquidityUSD"]
            },
            {
                "date": api_data["chain_tvls_chain_0_1_date"],
                "totalLiquidityUSD": api_data["chain_tvls_chain_0_1_totalLiquidityUSD"]
            }
        ],
        api_data["chain_1"]: [
            {
                "date": api_data["chain_tvls_chain_1_0_date"],
                "totalLiquidityUSD": api_data["chain_tvls_chain_1_0_totalLiquidityUSD"]
            },
            {
                "date": api_data["chain_tvls_chain_1_1_date"],
                "totalLiquidityUSD": api_data["chain_tvls_chain_1_1_totalLiquidityUSD"]
            }
        ]
    }
    
    # Construct token_breakdowns dictionary
    token_breakdowns = {
        api_data["chain_0"]: {
            "date": api_data["token_breakdowns_chain_0_token_0_date"],
            "value": api_data["token_breakdowns_chain_0_token_0_value"]
        },
        api_data["chain_1"]: {
            "date": api_data["token_breakdowns_chain_1_token_0_date"],
            "value": api_data["token_breakdowns_chain_1_token_0_value"]
        }
    }
    
    # Return the structured response
    return {
        "tvl_history": tvl_history,
        "chains": chains,
        "tokens": tokens,
        "category": api_data["category"],
        "name": api_data["name"],
        "slug": api_data["slug"],
        "fetched_at": api_data["fetched_at"],
        "chain_tvls": chain_tvls,
        "token_breakdowns": token_breakdowns
    }