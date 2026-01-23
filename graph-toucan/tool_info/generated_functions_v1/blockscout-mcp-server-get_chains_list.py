from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Blockscout MCP server.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - chain_0_id (int): First chain ID
        - chain_0_name (str): First chain name
        - chain_0_network_type (str): First chain network type (e.g., mainnet, testnet)
        - chain_0_rpc_url (str): First chain RPC URL
        - chain_0_browser_url (str): First chain browser/explorer URL
        - chain_1_id (int): Second chain ID
        - chain_1_name (str): Second chain name
        - chain_1_network_type (str): Second chain network type
        - chain_1_rpc_url (str): Second chain RPC URL
        - chain_1_browser_url (str): Second chain browser/explorer URL
        - total_count (int): Total number of chains returned
        - updated_at (str): ISO 8601 timestamp when data was last updated
        - metadata_api_version (str): API version of the source
        - metadata_source_url (str): Source URL where chain data is hosted
        - metadata_refresh_interval_seconds (int): Refresh interval in seconds
    """
    return {
        "chain_0_id": 1,
        "chain_0_name": "Ethereum Mainnet",
        "chain_0_network_type": "mainnet",
        "chain_0_rpc_url": "https://eth-mainnet.alchemyapi.io/v2/demo",
        "chain_0_browser_url": "https://etherscan.io",
        "chain_1_id": 5,
        "chain_1_name": "Goerli Testnet",
        "chain_1_network_type": "testnet",
        "chain_1_rpc_url": "https://eth-goerli.alchemyapi.io/v2/demo",
        "chain_1_browser_url": "https://goerli.etherscan.io",
        "total_count": 2,
        "updated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "metadata_api_version": "v1",
        "metadata_source_url": "https://blockscout.com/api/v1/chains",
        "metadata_refresh_interval_seconds": 3600,
    }


def blockscout_mcp_server_get_chains_list() -> Dict[str, Any]:
    """
    Get the list of known blockchain chains with their IDs.

    This function retrieves a list of blockchain chains including metadata such as chain ID,
    name, network type, RPC URL, and browser URL. It is useful for mapping chain names to IDs
    for use in other tools.

    Returns:
        Dict containing:
        - chains (List[Dict]): List of blockchain chain objects with id, name, network_type,
          rpc_url, and browser_url
        - total_count (int): Total number of chains returned
        - updated_at (str): ISO 8601 timestamp indicating when the list was last updated
        - metadata (Dict): Additional context including API version, source URL, and refresh interval
    """
    try:
        api_data = call_external_api("blockscout-mcp-server-get_chains_list")

        chains = [
            {
                "id": api_data["chain_0_id"],
                "name": api_data["chain_0_name"],
                "network_type": api_data["chain_0_network_type"],
                "rpc_url": api_data["chain_0_rpc_url"],
                "browser_url": api_data["chain_0_browser_url"],
            },
            {
                "id": api_data["chain_1_id"],
                "name": api_data["chain_1_name"],
                "network_type": api_data["chain_1_network_type"],
                "rpc_url": api_data["chain_1_rpc_url"],
                "browser_url": api_data["chain_1_browser_url"],
            },
        ]

        result = {
            "chains": chains,
            "total_count": api_data["total_count"],
            "updated_at": api_data["updated_at"],
            "metadata": {
                "api_version": api_data["metadata_api_version"],
                "source_url": api_data["metadata_source_url"],
                "refresh_interval_seconds": api_data["metadata_refresh_interval_seconds"],
            },
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve chains list: {str(e)}") from e