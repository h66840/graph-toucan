from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for transaction logs.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - log_0_event_name (str): Name of the first decoded event
        - log_0_signature (str): Signature of the first event
        - log_0_address (str): Contract address that emitted the first log
        - log_0_param_0_name (str): First parameter name of the first log
        - log_0_param_0_type (str): Type of the first parameter of the first log
        - log_0_param_0_value (str): Value of the first parameter of the first log
        - log_0_param_1_name (str): Second parameter name of the first log
        - log_0_param_1_type (str): Type of the second parameter of the first log
        - log_0_param_1_value (str): Value of the second parameter of the first log
        - log_0_topics_0 (str): First topic of the first log (raw)
        - log_0_data (str): Raw data of the first log
        - log_1_event_name (str): Name of the second decoded event
        - log_1_signature (str): Signature of the second event
        - log_1_address (str): Contract address that emitted the second log
        - log_1_param_0_name (str): First parameter name of the second log
        - log_1_param_0_type (str): Type of the first parameter of the second log
        - log_1_param_0_value (str): Value of the first parameter of the second log
        - log_1_param_1_name (str): Second parameter name of the second log
        - log_1_param_1_type (str): Type of the second parameter of the second log
        - log_1_param_1_value (str): Value of the second parameter of the second log
        - log_1_topics_0 (str): First topic of the second log (raw)
        - log_1_data (str): Raw data of the second log
        - transaction_hash (str): Hash of the transaction
        - chain_id (str): Blockchain ID
        - block_number (int): Block number containing the transaction
        - block_hash (str): Hash of the block
        - timestamp (str): ISO 8601 timestamp of the block
        - total_logs (int): Total number of logs returned
        - has_more (bool): Whether more pages are available
        - next_cursor (str | None): Cursor for next page, or null if none
        - metadata_network_name (str): Name of the network
        - metadata_api_version (str): Version of the API
        - metadata_status (str): Processing status
    """
    return {
        "log_0_event_name": "Transfer",
        "log_0_signature": "Transfer(address,address,uint256)",
        "log_0_address": "0x1234567890123456789012345678901234567890",
        "log_0_param_0_name": "from",
        "log_0_param_0_type": "address",
        "log_0_param_0_value": "0x9876543210987654321098765432109876543210",
        "log_0_param_1_name": "to",
        "log_0_param_1_type": "address",
        "log_0_param_1_value": "0x1111111111111111111111111111111111111111",
        "log_0_topics_0": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
        "log_0_data": "0x0000000000000000000000000000000000000000000000000000000000000001",
        "log_1_event_name": "Approval",
        "log_1_signature": "Approval(address,address,uint256)",
        "log_1_address": "0x1234567890123456789012345678901234567890",
        "log_1_param_0_name": "owner",
        "log_1_param_0_type": "address",
        "log_1_param_0_value": "0x9876543210987654321098765432109876543210",
        "log_1_param_1_name": "spender",
        "log_1_param_1_type": "address",
        "log_1_param_1_value": "0x2222222222222222222222222222222222222222",
        "log_1_topics_0": "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
        "log_1_data": "0x000000000000000000000000000000000000000000000000000000000000000a",
        "transaction_hash": "0xabc123def456ghi789jkl012mnop345qrs678tuv901wxyz234abc567def890",
        "chain_id": "1",
        "block_number": 12345678,
        "block_hash": "0x9876543210abcdef9876543210abcdef9876543210abcdef9876543210abcdef",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_logs": 2,
        "has_more": True,
        "next_cursor": "cursor_123",
        "metadata_network_name": "Ethereum Mainnet",
        "metadata_api_version": "1.0.0",
        "metadata_status": "success",
    }


def blockscout_mcp_server_get_transaction_logs(
    chain_id: str, transaction_hash: str, cursor: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get comprehensive transaction logs with decoded event parameters.

    This function retrieves enriched transaction logs from a blockchain, focusing on
    decoded smart contract event parameters. It's essential for analyzing contract
    interactions, token transfers, DeFi protocols, and debugging event emissions.

    Args:
        chain_id (str): The ID of the blockchain
        transaction_hash (str): Transaction hash for which to retrieve logs
        cursor (Optional[str]): Pagination cursor from a previous response to get the next page

    Returns:
        Dict containing:
        - logs (List[Dict]): List of decoded transaction log entries with event details and parameters
        - transaction_hash (str): The hash of the transaction
        - chain_id (str): The blockchain ID
        - block_number (int): Block number containing the transaction
        - block_hash (str): Block hash
        - timestamp (str): ISO 8601 timestamp of block confirmation
        - total_logs (int): Number of logs in this response
        - has_more (bool): Whether additional pages are available
        - next_cursor (str | None): Cursor for next page, or None if no more
        - metadata (Dict): Additional metadata about the query and network

    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not chain_id:
        raise ValueError("chain_id is required")
    if not transaction_hash:
        raise ValueError("transaction_hash is required")

    # Call external API to get flattened data
    api_data = call_external_api("blockscout-mcp-server-get_transaction_logs")

    # Construct logs list from indexed fields
    logs = []

    # Process first log
    logs.append({
        "event_name": api_data["log_0_event_name"],
        "signature": api_data["log_0_signature"],
        "address": api_data["log_0_address"],
        "decoded_parameters": [
            {
                "name": api_data["log_0_param_0_name"],
                "type": api_data["log_0_param_0_type"],
                "value": api_data["log_0_param_0_value"]
            },
            {
                "name": api_data["log_0_param_1_name"],
                "type": api_data["log_0_param_1_type"],
                "value": api_data["log_0_param_1_value"]
            }
        ],
        "topics": [api_data["log_0_topics_0"]],
        "data": api_data["log_0_data"]
    })

    # Process second log
    logs.append({
        "event_name": api_data["log_1_event_name"],
        "signature": api_data["log_1_signature"],
        "address": api_data["log_1_address"],
        "decoded_parameters": [
            {
                "name": api_data["log_1_param_0_name"],
                "type": api_data["log_1_param_0_type"],
                "value": api_data["log_1_param_0_value"]
            },
            {
                "name": api_data["log_1_param_1_name"],
                "type": api_data["log_1_param_1_type"],
                "value": api_data["log_1_param_1_value"]
            }
        ],
        "topics": [api_data["log_1_topics_0"]],
        "data": api_data["log_1_data"]
    })

    # Build final response
    response = {
        "logs": logs,
        "transaction_hash": api_data["transaction_hash"],
        "chain_id": api_data["chain_id"],
        "block_number": api_data["block_number"],
        "block_hash": api_data["block_hash"],
        "timestamp": api_data["timestamp"],
        "total_logs": api_data["total_logs"],
        "has_more": api_data["has_more"],
        "next_cursor": api_data["next_cursor"],
        "metadata": {
            "network_name": api_data["metadata_network_name"],
            "api_version": api_data["metadata_api_version"],
            "status": api_data["metadata_status"]
        }
    }

    return response