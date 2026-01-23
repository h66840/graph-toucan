from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Mina blockchain events.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - block_height (int): Height of the block containing the event
        - transaction_hash (str): Hash of the transaction
        - type (str): Type of the event (e.g., 'payment', 'delegation')
        - data (str): JSON string representing event-specific data
        - timestamp (int): Unix timestamp when the event occurred
    """
    return {
        "block_height": 123456,
        "transaction_hash": "CkppGjQqJtVvZa1vYzX1a2b3c4d5e6f7g8h9i0j1k",
        "type": "payment",
        "data": '{"from": "B62q...", "to": "B62p...", "amount": 100000000}',
        "timestamp": 1678886400
    }


def mina_archive_node_api_query_events(
    address: str,
    from_block: Optional[int] = None,
    status: Optional[str] = None,
    to_block: Optional[int] = None,
    token_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query events from the Mina blockchain with optional filters.

    This function simulates querying blockchain events based on provided filters.
    It returns a list of event objects matching the criteria.

    Args:
        address (str): The Mina blockchain address to query events for (required).
        from_block (int, optional): Filter events from this block height onward.
        status (str, optional): Filter events by transaction status (e.g., 'success', 'failed').
        to_block (int, optional): Filter events up to this block height.
        token_id (str, optional): Filter events related to a specific token ID.

    Returns:
        Dict[str, Any]: A dictionary containing a single key 'events' whose value is a list of event dictionaries.
        Each event contains:
            - block_height (int): Height of the block containing the event
            - transaction_hash (str): Hash of the transaction
            - type (str): Type of the event
            - data (Dict): Parsed JSON data of the event
            - timestamp (int): Unix timestamp when the event occurred

    Raises:
        ValueError: If address is empty or invalid format.
    """
    if not address or not isinstance(address, str) or not address.startswith("B62"):
        raise ValueError("Address must be a valid Mina address starting with 'B62'")

    if from_block is not None and (not isinstance(from_block, int) or from_block < 0):
        raise ValueError("from_block must be a non-negative integer")

    if to_block is not None and (not isinstance(to_block, int) or to_block < 0):
        raise ValueError("to_block must be a non-negative integer")

    if from_block is not None and to_block is not None and from_block > to_block:
        raise ValueError("from_block cannot be greater than to_block")

    if status is not None and not isinstance(status, str):
        raise ValueError("status must be a string")

    if token_id is not None and not isinstance(token_id, str):
        raise ValueError("token_id must be a string")

    # Simulate calling external API
    api_data = call_external_api("mina-archive-node-api-query-events")

    # Construct the nested output structure
    event = {
        "block_height": api_data["block_height"],
        "transaction_hash": api_data["transaction_hash"],
        "type": api_data["type"],
        "data": api_data["data"],  # In real case, this would be json.loads(api_data["data"])
        "timestamp": api_data["timestamp"]
    }

    return {
        "events": [event]
    }