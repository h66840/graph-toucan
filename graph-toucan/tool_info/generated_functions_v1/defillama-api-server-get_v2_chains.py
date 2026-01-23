from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DefiLlama chains TVL.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - chains_0_name (str): Name of the first chain
        - chains_0_tvl (float): TVL of the first chain in USD
        - chains_0_chain_id (int): Chain ID of the first chain
        - chains_0_category (str): Category of the first chain
        - chains_0_timestamp (str): ISO 8601 timestamp for the first chain
        - chains_0_change_1d (float): 1-day TVL change percentage for the first chain
        - chains_0_change_7d (float): 7-day TVL change percentage for the first chain
        - chains_0_gecko_id (str): CoinGecko ID for the first chain's native token
        - chains_1_name (str): Name of the second chain
        - chains_1_tvl (float): TVL of the second chain in USD
        - chains_1_chain_id (int): Chain ID of the second chain
        - chains_1_category (str): Category of the second chain
        - chains_1_timestamp (str): ISO 8601 timestamp for the second chain
        - chains_1_change_1d (float): 1-day TVL change percentage for the second chain
        - chains_1_change_7d (float): 7-day TVL change percentage for the second chain
        - chains_1_gecko_id (str): CoinGecko ID for the second chain's native token
        - total_tvl (float): Total aggregated TVL across all chains in USD
        - updated_at (str): ISO 8601 timestamp indicating when the data was last updated
        - metadata_source (str): Source of the data
        - metadata_currency (str): Currency unit used (e.g., USD)
        - metadata_disclaimer (str): Disclaimer or notes from the API
    """
    return {
        "chains_0_name": "Ethereum",
        "chains_0_tvl": 45000000000.0,
        "chains_0_chain_id": 1,
        "chains_0_category": "Layer 1",
        "chains_0_timestamp": "2023-10-05T12:34:56Z",
        "chains_0_change_1d": -1.2,
        "chains_0_change_7d": 3.5,
        "chains_0_gecko_id": "ethereum",

        "chains_1_name": "Polygon",
        "chains_1_tvl": 5200000000.0,
        "chains_1_chain_id": 137,
        "chains_1_category": "Layer 2",
        "chains_1_timestamp": "2023-10-05T12:34:56Z",
        "chains_1_change_1d": 0.8,
        "chains_1_change_7d": -2.1,
        "chains_1_gecko_id": "matic-network",

        "total_tvl": 50200000000.0,
        "updated_at": "2023-10-05T12:34:56Z",
        "metadata_source": "DefiLlama API",
        "metadata_currency": "USD",
        "metadata_disclaimer": "Data is aggregated from various DeFi protocols and may be subject to delays or inaccuracies."
    }


def defillama_api_server_get_v2_chains() -> Dict[str, Any]:
    """
    Get current TVL (Total Value Locked) of all chains from DefiLlama.

    Returns:
        Dict containing:
        - chains (List[Dict]): List of chain objects with name, TVL, chain_id, category, timestamp,
          change_1d, change_7d, and gecko_id
        - total_tvl (float): Total aggregated TVL across all chains in USD
        - updated_at (str): ISO 8601 timestamp indicating when the data was last updated
        - metadata (Dict): Additional context including source, currency, and disclaimer

    Raises:
        Exception: If required fields are missing or data is malformed
    """
    try:
        # Fetch simulated external API data
        api_data = call_external_api("defillama-api-server-get_v2_chains")

        # Construct chains list
        chains: List[Dict[str, Any]] = [
            {
                "name": api_data["chains_0_name"],
                "tvl": api_data["chains_0_tvl"],
                "chain_id": api_data["chains_0_chain_id"],
                "category": api_data["chains_0_category"],
                "timestamp": api_data["chains_0_timestamp"],
                "change_1d": api_data["chains_0_change_1d"],
                "change_7d": api_data["chains_0_change_7d"],
                "gecko_id": api_data["chains_0_gecko_id"]
            },
            {
                "name": api_data["chains_1_name"],
                "tvl": api_data["chains_1_tvl"],
                "chain_id": api_data["chains_1_chain_id"],
                "category": api_data["chains_1_category"],
                "timestamp": api_data["chains_1_timestamp"],
                "change_1d": api_data["chains_1_change_1d"],
                "change_7d": api_data["chains_1_change_7d"],
                "gecko_id": api_data["chains_1_gecko_id"]
            }
        ]

        # Construct metadata
        metadata: Dict[str, Any] = {
            "source": api_data["metadata_source"],
            "currency": api_data["metadata_currency"],
            "disclaimer": api_data["metadata_disclaimer"]
        }

        # Build final result
        result: Dict[str, Any] = {
            "chains": chains,
            "total_tvl": api_data["total_tvl"],
            "updated_at": api_data["updated_at"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise Exception(f"Missing required data field: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to process chain TVL data: {str(e)}")