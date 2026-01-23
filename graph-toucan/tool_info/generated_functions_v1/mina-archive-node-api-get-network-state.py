from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Mina network state.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - canonicalMaxBlockHeight (int): The current highest block height in the canonical (finalized) chain
        - pendingMaxBlockHeight (int): The current highest block height observed, including pending/unconfirmed blocks
    """
    return {
        "canonicalMaxBlockHeight": 154238,
        "pendingMaxBlockHeight": 154242
    }

def mina_archive_node_api_get_network_state() -> Dict[str, Any]:
    """
    Get the current state of the Mina network.

    This function retrieves the latest block height information from the Mina archive node,
    including both canonical (finalized) and pending (unconfirmed) block heights.

    Returns:
        Dict containing:
        - networkState (Dict): Contains maxBlockHeight with canonical and pending block heights
        - maxBlockHeight (Dict): Contains canonicalMaxBlockHeight and pendingMaxBlockHeight
        - canonicalMaxBlockHeight (int): Highest block height in the canonical chain
        - pendingMaxBlockHeight (int): Highest known block height including pending
    """
    try:
        # Fetch data from external API (simulated)
        api_data = call_external_api("mina-archive-node-api-get-network-state")

        # Extract simple scalar values
        canonical_height = api_data["canonicalMaxBlockHeight"]
        pending_height = api_data["pendingMaxBlockHeight"]

        # Construct nested output structure as per schema
        result = {
            "canonicalMaxBlockHeight": canonical_height,
            "pendingMaxBlockHeight": pending_height,
            "maxBlockHeight": {
                "canonicalMaxBlockHeight": canonical_height,
                "pendingMaxBlockHeight": pending_height
            },
            "networkState": {
                "maxBlockHeight": {
                    "canonicalMaxBlockHeight": canonical_height,
                    "pendingMaxBlockHeight": pending_height
                }
            }
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve Mina network state: {str(e)}") from e