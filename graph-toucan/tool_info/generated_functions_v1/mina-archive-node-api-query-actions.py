from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external Mina Archive Node API for querying actions.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - action_0_actionId (str): ID of the first action
        - action_0_type (str): Type of the first action
        - action_0_sender (str): Sender address of the first action
        - action_0_receiver (str): Receiver address of the first action
        - action_0_blockHeight (int): Block height of the first action
        - action_0_blockTime (int): Block timestamp in milliseconds for the first action
        - action_0_status (str): Status of the first action
        - action_0_data (str): Data payload of the first action
        - action_0_transactionHash (str): Transaction hash of the first action
        - action_1_actionId (str): ID of the second action
        - action_1_type (str): Type of the second action
        - action_1_sender (str): Sender address of the second action
        - action_1_receiver (str): Receiver address of the second action
        - action_1_blockHeight (int): Block height of the second action
        - action_1_blockTime (int): Block timestamp in milliseconds for the second action
        - action_1_status (str): Status of the second action
        - action_1_data (str): Data payload of the second action
        - action_1_transactionHash (str): Transaction hash of the second action
        - totalCount (int): Total number of actions matching the query
        - pagination_page (int): Current page number
        - pagination_limit (int): Number of items per page
        - pagination_hasNextPage (bool): Whether next page exists
        - pagination_hasPreviousPage (bool): Whether previous page exists
        - filtersApplied_address (str): Address used in filter
        - filtersApplied_fromBlock (int): From block height filter applied
        - filtersApplied_toBlock (int): To block height filter applied
        - filtersApplied_status (str): Status filter applied
        - filtersApplied_tokenId (str): Token ID filter applied
        - filtersApplied_fromActionState (str): From action state filter applied
        - filtersApplied_endActionState (str): End action state filter applied
        - metadata_network (str): Network name (e.g., mainnet, devnet)
        - metadata_latestBlockHeight (int): Latest block height on the network
        - metadata_queryDurationMs (int): Duration of the query in milliseconds
        - metadata_timestamp (int): Timestamp of the response in milliseconds
    """
    now = int(datetime.now(timezone.utc).timestamp() * 1000)
    latest_block = random.randint(150000, 200000)

    return {
        "action_0_actionId": f"act_{random.randint(10000, 99999)}_0",
        "action_0_type": random.choice(["zkapp", "payment", "delegation"]),
        "action_0_sender": "B62qirHqZm6Y1f5dJtBq5K2iXG1a1s1d1f1g1h1j1k1l1m1n1o1p",
        "action_0_receiver": "B62qirHqZm6Y1f5dJtBq5K2iXG1a1s1d1f1g1h1j1k1l1m1n1o1q",
        "action_0_blockHeight": random.randint(100000, latest_block),
        "action_0_blockTime": now - random.randint(0, 86400000),
        "action_0_status": random.choice(["applied", "failed"]),
        "action_0_data": '{"amount":"100000000","fee":"1000000"}',
        "action_0_transactionHash": f"3NLTx{random.randint(100000, 999999)}abcde",

        "action_1_actionId": f"act_{random.randint(10000, 99999)}_1",
        "action_1_type": random.choice(["payment", "delegation", "zkapp"]),
        "action_1_sender": "B62qirHqZm6Y1f5dJtBq5K2iXG1a1s1d1f1g1h1j1k1l1m1n1o1r",
        "action_1_receiver": "B62qirHqZm6Y1f5dJtBq5K2iXG1a1s1d1f1g1h1j1k1l1m1n1o1s",
        "action_1_blockHeight": random.randint(100000, latest_block),
        "action_1_blockTime": now - random.randint(86400000, 172800000),
        "action_1_status": random.choice(["applied", "failed"]),
        "action_1_data": '{"amount":"200000000","fee":"2000000"}',
        "action_1_transactionHash": f"3NLTr{random.randint(100000, 999999)}fghij",

        "totalCount": random.randint(1, 100),
        "pagination_page": 1,
        "pagination_limit": 2,
        "pagination_hasNextPage": random.choice([True, False]),
        "pagination_hasPreviousPage": False,

        "filtersApplied_address": "B62qirHqZm6Y1f5dJtBq5K2iXG1a1s1d1f1g1h1j1k1l1m1n1o1p",
        "filtersApplied_fromBlock": 100000,
        "filtersApplied_toBlock": latest_block,
        "filtersApplied_status": "applied",
        "filtersApplied_tokenId": "1",
        "filtersApplied_fromActionState": "stateA",
        "filtersApplied_endActionState": "stateB",

        "metadata_network": random.choice(["mainnet", "devnet"]),
        "metadata_latestBlockHeight": latest_block,
        "metadata_queryDurationMs": random.randint(50, 500),
        "metadata_timestamp": now,
    }


def mina_archive_node_api_query_actions(
    address: str,
    endActionState: Optional[str] = None,
    from_block: Optional[int] = None,
    fromActionState: Optional[str] = None,
    status: Optional[str] = None,
    to: Optional[int] = None,
    tokenId: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Query actions from the Mina blockchain with optional filters.

    Args:
        address (str): The account address to query actions for (required).
        endActionState (str, optional): Filter by ending action state.
        from_block (int, optional): Filter actions from this block height.
        fromActionState (str, optional): Filter by starting action state.
        status (str, optional): Filter by transaction status (e.g., applied, failed).
        to (int, optional): Filter actions up to this block height.
        tokenId (str, optional): Filter by token ID.

    Returns:
        Dict containing:
        - actions (List[Dict]): List of action objects with details.
        - totalCount (int): Total number of matching actions.
        - pagination (Dict): Pagination metadata.
        - filtersApplied (Dict): Summary of filters used.
        - metadata (Dict): Additional contextual information.

    Raises:
        ValueError: If required address parameter is missing or invalid.
    """
    if not address or not isinstance(address, str) or len(address.strip()) == 0:
        raise ValueError("Address is required and must be a non-empty string.")

    if from_block is not None and (not isinstance(from_block, int) or from_block < 0):
        raise ValueError("from_block must be a non-negative integer if provided.")

    if to is not None and (not isinstance(to, int) or to < 0):
        raise ValueError("to must be a non-negative integer if provided.")

    if from_block is not None and to is not None and from_block > to:
        raise ValueError("from_block cannot be greater than to.")

    # Call external API (simulated)
    api_data = call_external_api("mina-archive-node-api-query-actions")

    # Construct actions list from indexed fields
    actions = [
        {
            "actionId": api_data["action_0_actionId"],
            "type": api_data["action_0_type"],
            "sender": api_data["action_0_sender"],
            "receiver": api_data["action_0_receiver"],
            "blockHeight": api_data["action_0_blockHeight"],
            "blockTime": api_data["action_0_blockTime"],
            "status": api_data["action_0_status"],
            "data": api_data["action_0_data"],
            "transactionHash": api_data["action_0_transactionHash"],
        },
        {
            "actionId": api_data["action_1_actionId"],
            "type": api_data["action_1_type"],
            "sender": api_data["action_1_sender"],
            "receiver": api_data["action_1_receiver"],
            "blockHeight": api_data["action_1_blockHeight"],
            "blockTime": api_data["action_1_blockTime"],
            "status": api_data["action_1_status"],
            "data": api_data["action_1_data"],
            "transactionHash": api_data["action_1_transactionHash"],
        },
    ]

    # Build result with nested structure
    result = {
        "actions": actions,
        "totalCount": api_data["totalCount"],
        "pagination": {
            "page": api_data["pagination_page"],
            "limit": api_data["pagination_limit"],
            "hasNextPage": api_data["pagination_hasNextPage"],
            "hasPreviousPage": api_data["pagination_hasPreviousPage"],
        },
        "filtersApplied": {
            "address": api_data["filtersApplied_address"],
            "fromBlock": api_data["filtersApplied_fromBlock"],
            "toBlock": api_data["filtersApplied_toBlock"],
            "status": api_data["filtersApplied_status"],
            "tokenId": api_data["filtersApplied_tokenId"],
            "fromActionState": api_data["filtersApplied_fromActionState"],
            "endActionState": api_data["filtersApplied_endActionState"],
        },
        "metadata": {
            "network": api_data["metadata_network"],
            "latestBlockHeight": api_data["metadata_latestBlockHeight"],
            "queryDurationMs": api_data["metadata_queryDurationMs"],
            "timestamp": api_data["metadata_timestamp"],
        },
    }

    return result