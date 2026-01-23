from typing import Dict, List, Any, Optional
import random
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DefiLlama historical chain TVL.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - tvl_data_0_timestamp (int): Unix timestamp for first TVL data point
        - tvl_data_0_value (float): TVL value in USD for first data point
        - tvl_data_1_timestamp (int): Unix timestamp for second TVL data point
        - tvl_data_1_value (float): TVL value in USD for second data point
        - chain (str): The name or slug of the blockchain
        - excluded_categories_0 (str): First excluded category (e.g., 'liquid staking')
        - excluded_categories_1 (str): Second excluded category (e.g., 'double counted')
        - metadata_source (str): Data source identifier
        - metadata_last_updated (int): Unix timestamp of last update
        - metadata_disclaimer (str): Disclaimer about data accuracy
    """
    current_time = int(time.time())
    return {
        "tvl_data_0_timestamp": current_time - 86400,  # 24 hours ago
        "tvl_data_0_value": round(random.uniform(100_000_000, 5_000_000_000), 2),
        "tvl_data_1_timestamp": current_time,
        "tvl_data_1_value": round(random.uniform(100_000_000, 5_000_000_000), 2),
        "chain": "ethereum",
        "excluded_categories_0": "liquid staking",
        "excluded_categories_1": "double counted",
        "metadata_source": "DefiLlama Aggregator",
        "metadata_last_updated": current_time,
        "metadata_disclaimer": "Data is approximate and excludes certain categories."
    }


def defillama_api_server_get_v2_historicalChainTvl_by_chain(chain: str) -> Dict[str, Any]:
    """
    Get historical TVL (excludes liquid staking and double counted tvl) of a chain.

    Args:
        chain (str): Chain slug, you can get these from /chains or the chains property on /protocols.

    Returns:
        Dict containing:
        - tvl_data (List[Dict]): List of timestamp-value pairs representing historical TVL.
        - chain (str): The name or slug of the blockchain.
        - excluded_categories (List[str]): List of TVL categories excluded from calculation.
        - metadata (Dict): Additional contextual information such as source, last updated timestamp, and disclaimers.
    
    Raises:
        ValueError: If chain is not provided or is empty.
    """
    if not chain or not chain.strip():
        raise ValueError("Parameter 'chain' is required and must be a non-empty string.")
    
    # Clean and normalize chain input
    chain = chain.strip().lower()

    # Call external API (simulated)
    api_data = call_external_api("defillama-api-server-get_v2_historicalChainTvl__by_chain")

    # Construct TVL data list from indexed fields
    tvl_data = [
        {
            "timestamp": api_data["tvl_data_0_timestamp"],
            "value": api_data["tvl_data_0_value"]
        },
        {
            "timestamp": api_data["tvl_data_1_timestamp"],
            "value": api_data["tvl_data_1_value"]
        }
    ]

    # Construct excluded categories list
    excluded_categories = [
        api_data["excluded_categories_0"],
        api_data["excluded_categories_1"]
    ]

    # Construct metadata dictionary
    metadata = {
        "source": api_data["metadata_source"],
        "last_updated": api_data["metadata_last_updated"],
        "disclaimer": api_data["metadata_disclaimer"]
    }

    # Return final structured response
    return {
        "tvl_data": tvl_data,
        "chain": api_data["chain"],
        "excluded_categories": excluded_categories,
        "metadata": metadata
    }