from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DeFi protocols.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - protocol_0_name (str): Name of the first protocol
        - protocol_0_chain_tvls_bsc (float): BSC TVL for first protocol
        - protocol_0_chain_tvls_ethereum (float): Ethereum TVL for first protocol
        - protocol_0_tvl (float): Total TVL for first protocol
        - protocol_0_change_1d (float): 1-day TVL change for first protocol
        - protocol_1_name (str): Name of the second protocol
        - protocol_1_chain_tvls_polygon (float): Polygon TVL for second protocol
        - protocol_1_chain_tvls_ethereum (float): Ethereum TVL for second protocol
        - protocol_1_tvl (float): Total TVL for second protocol
        - protocol_1_change_1d (float): 1-day TVL change for second protocol
        - total_count (int): Total number of protocols returned
        - timestamp (int): Unix timestamp when data was fetched
        - meta_api_version (str): Version of the API
        - meta_currency (str): Currency used in values (e.g., USD)
        - meta_total_tvl (float): Global total TVL across all protocols
        - meta_protocol_count (int): Total count of protocols tracked
    """
    return {
        "protocol_0_name": "Aave",
        "protocol_0_chain_tvls_bsc": 1200000000.0,
        "protocol_0_chain_tvls_ethereum": 5800000000.0,
        "protocol_0_tvl": 7000000000.0,
        "protocol_0_change_1d": -0.02,
        "protocol_1_name": "Uniswap",
        "protocol_1_chain_tvls_polygon": 850000000.0,
        "protocol_1_chain_tvls_ethereum": 4100000000.0,
        "protocol_1_tvl": 4950000000.0,
        "protocol_1_change_1d": 0.015,
        "total_count": 2,
        "timestamp": 1700000000,
        "meta_api_version": "1.0",
        "meta_currency": "USD",
        "meta_total_tvl": 15000000000.0,
        "meta_protocol_count": 200
    }

def defillama_api_server_get_protocols() -> Dict[str, Any]:
    """
    Fetch and return a list of all DeFi protocols from DefiLlama with their TVL data.

    Returns:
        Dict containing:
        - protocols (List[Dict]): List of protocol objects with name, chain TVLs, total TVL, and metrics
        - total_count (int): Number of protocols returned
        - timestamp (int): Unix timestamp when data was fetched
        - meta (Dict): Metadata including API version, currency, and global summaries
    """
    try:
        api_data = call_external_api("defillama-api-server-get_protocols")

        # Construct protocols list
        protocols = [
            {
                "name": api_data["protocol_0_name"],
                "chainTvls": {
                    "bsc": api_data["protocol_0_chain_tvls_bsc"],
                    "ethereum": api_data["protocol_0_chain_tvls_ethereum"]
                },
                "tvl": api_data["protocol_0_tvl"],
                "change_1d": api_data["protocol_0_change_1d"]
            },
            {
                "name": api_data["protocol_1_name"],
                "chainTvls": {
                    "polygon": api_data["protocol_1_chain_tvls_polygon"],
                    "ethereum": api_data["protocol_1_chain_tvls_ethereum"]
                },
                "tvl": api_data["protocol_1_tvl"],
                "change_1d": api_data["protocol_1_change_1d"]
            }
        ]

        # Construct meta object
        meta = {
            "apiVersion": api_data["meta_api_version"],
            "currency": api_data["meta_currency"],
            "totalTvl": api_data["meta_total_tvl"],
            "protocolCount": api_data["meta_protocol_count"]
        }

        result = {
            "protocols": protocols,
            "total_count": api_data["total_count"],
            "timestamp": api_data["timestamp"],
            "meta": meta
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to process DefiLlama protocols data: {str(e)}") from e