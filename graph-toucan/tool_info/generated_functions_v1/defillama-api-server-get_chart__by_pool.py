from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external DefiLlama API for pool chart data.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - data_0_timestamp (int): Unix timestamp for first historical entry
        - data_0_apy (float): APY percentage for first entry
        - data_0_tvl (float): TVL in USD for first entry
        - data_1_timestamp (int): Unix timestamp for second historical entry
        - data_1_apy (float): APY percentage for second entry
        - data_1_tvl (float): TVL in USD for second entry
        - pool_id (str): Unique identifier of the pool
        - name (str): Human-readable name of the pool
        - symbol (str): Pool symbol or token pair notation
        - project (str): Name of the protocol or project
        - chain (str): Blockchain network name
        - tvl_usd_latest (float): Most recent Total Value Locked in USD
        - apy_latest (float): Most recent Annual Percentage Yield as percentage
        - updated_at (int): Unix timestamp when data was last updated
    """
    now = int(datetime.now().timestamp())
    one_day_ago = int((datetime.now() - timedelta(days=1)).timestamp())
    
    return {
        "data_0_timestamp": one_day_ago,
        "data_0_apy": round(random.uniform(1.0, 20.0), 2),
        "data_0_tvl": round(random.uniform(100000, 10000000), 2),
        "data_1_timestamp": now,
        "data_1_apy": round(random.uniform(1.0, 20.0), 2),
        "data_1_tvl": round(random.uniform(100000, 10000000), 2),
        "pool_id": "0xabcdef1234567890-defillama",
        "name": "USDC/WETH LP",
        "symbol": "USDC-WETH",
        "project": "Uniswap",
        "chain": "Ethereum",
        "tvl_usd_latest": round(random.uniform(100000, 10000000), 2),
        "apy_latest": round(random.uniform(1.0, 20.0), 2),
        "updated_at": now
    }

def defillama_api_server_get_chart_by_pool(pool: str) -> Dict[str, Any]:
    """
    Get historical APY and TVL of a pool from DefiLlama API.
    
    Args:
        pool (str): Pool id, can be retrieved from /pools (property is called pool)
    
    Returns:
        Dict containing:
        - data (List[Dict]): List of time-series entries with timestamp, APY, and TVL
        - pool_id (str): Unique identifier of the pool
        - name (str): Human-readable name of the pool
        - symbol (str): Pool symbol or token pair notation
        - project (str): Name of the protocol or project
        - chain (str): Blockchain network name
        - tvl_usd_latest (float): Most recent Total Value Locked in USD
        - apy_latest (float): Most recent Annual Percentage Yield as percentage
        - updated_at (int): Unix timestamp when data was last updated
    
    Raises:
        ValueError: If pool parameter is empty or invalid
    """
    if not pool or not isinstance(pool, str) or len(pool.strip()) == 0:
        raise ValueError("Pool parameter is required and must be a non-empty string")
    
    pool = pool.strip()
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("defillama-api-server-get_chart__by_pool")
    
    # Construct the data list from indexed fields
    data = [
        {
            "timestamp": api_data["data_0_timestamp"],
            "apy": api_data["data_0_apy"],
            "tvl": api_data["data_0_tvl"]
        },
        {
            "timestamp": api_data["data_1_timestamp"],
            "apy": api_data["data_1_apy"],
            "tvl": api_data["data_1_tvl"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "data": data,
        "pool_id": api_data["pool_id"],
        "name": api_data["name"],
        "symbol": api_data["symbol"],
        "project": api_data["project"],
        "chain": api_data["chain"],
        "tvl_usd_latest": api_data["tvl_usd_latest"],
        "apy_latest": api_data["apy_latest"],
        "updated_at": api_data["updated_at"]
    }
    
    return result