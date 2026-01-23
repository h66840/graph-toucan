from typing import Dict, Any, Optional
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for blockscout-mcp-server-get_latest_block.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_block_number (int): The latest indexed block number
        - data_timestamp (str): The timestamp of the latest block in ISO 8601 format
        - data_description (str): Description of the data
        - notes (str): Additional notes about the blockchain state
        - instructions (str): Instructions for using the data
        - pagination_current (int): Current page number
        - pagination_next (int): Next page number
        - pagination_prev (int): Previous page number
        - pagination_total_pages (int): Total number of pages
    """
    return {
        "data_block_number": 15000000,
        "data_timestamp": "2023-11-20T14:35:22Z",
        "data_description": "Latest indexed block on the blockchain",
        "notes": "This is the most recent block that has been indexed. No transactions exist beyond this point.",
        "instructions": "Use this block number and timestamp as a reference point for querying historical data.",
        "pagination_current": 1,
        "pagination_next": 2,
        "pagination_prev": None,
        "pagination_total_pages": 1,
    }


def blockscout_mcp_server_get_latest_block(chain_id: str) -> Dict[str, Any]:
    """
    Get the latest indexed block number and timestamp for a given blockchain.

    This function simulates retrieving the most recent state of the blockchain,
    which can be used as a reference point for other API calls. No transactions
    or token transfers can exist beyond this block.

    Args:
        chain_id (str): The ID of the blockchain (e.g., '1' for Ethereum Mainnet)

    Returns:
        Dict containing:
        - data (Dict): Contains 'block_number' (int) and 'timestamp' (str in ISO 8601 format)
        - data_description (Optional[str]): Optional description of the data
        - notes (Optional[str]): Additional notes about the response or blockchain state
        - instructions (Optional[str]): Optional instructions for how to use the data
        - pagination (Optional[Dict]): Pagination metadata with fields like 'current', 'next', 'prev', 'total_pages'

    Raises:
        ValueError: If chain_id is empty or not a string
    """
    if not chain_id:
        raise ValueError("chain_id is required")
    if not isinstance(chain_id, str):
        raise ValueError("chain_id must be a string")

    # Call external API to get flattened data
    api_data = call_external_api("blockscout-mcp-server-get_latest_block")

    # Construct the nested output structure from flattened API data
    result: Dict[str, Any] = {
        "data": {
            "block_number": api_data["data_block_number"],
            "timestamp": api_data["data_timestamp"]
        },
        "data_description": api_data.get("data_description"),
        "notes": api_data.get("notes"),
        "instructions": api_data.get("instructions"),
        "pagination": None
    }

    # Construct pagination if available
    if api_data.get("pagination_current") is not None:
        result["pagination"] = {
            "current": api_data["pagination_current"],
            "next": api_data["pagination_next"] if api_data.get("pagination_next") is not None else None,
            "prev": api_data["pagination_prev"] if api_data.get("pagination_prev") is not None else None,
            "total_pages": api_data["pagination_total_pages"]
        }

    return result