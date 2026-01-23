from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching block information from an external Blockscout API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - block_number (int): The number of the block in the blockchain
        - block_hash (str): The unique hash identifier of the block
        - parent_hash (str): The hash of the parent block
        - timestamp (str): The time when the block was created, in ISO 8601 format
        - gas_used (int): Total amount of gas used by transactions in the block
        - gas_limit (int): Maximum amount of gas allowed in the block
        - burnt_fees (float): Amount of fees burnt in the block
        - transaction_count (int): Number of transactions included in the block
        - transaction_0 (str): First transaction hash in the block (if include_transactions=True)
        - transaction_1 (str): Second transaction hash in the block (if include_transactions=True)
        - miner (str): Address of the miner or validator who produced the block
        - size (int): Size of the block in bytes
        - difficulty (int): Difficulty level of the block
        - total_difficulty (int): Cumulative difficulty up to this block
        - extra_data (str): Arbitrary data included by the miner
        - state_root (str): Root hash of the state trie after the block is applied
        - transactions_root (str): Root hash of the transactions trie in the block
        - receipts_root (str): Root hash of the receipts trie from transactions in the block
        - base_fee_per_gas (float): Base fee per gas unit in the block
        - next_block_base_fee (float): Suggested base fee for the next block
    """
    return {
        "block_number": 19876543,
        "block_hash": "0xabc123def456ghi789jkl012mno345pqr678stu901vwx234yz567",
        "parent_hash": "0xdef456ghi789jkl012mno345pqr678stu901vwx234yz567abc123",
        "timestamp": "2023-11-25T14:32:18Z",
        "gas_used": 14500000,
        "gas_limit": 15000000,
        "burnt_fees": 2.456,
        "transaction_count": 2,
        "transaction_0": "0x1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b",
        "transaction_1": "0x9z8y7x6w5v4u3t2s1r0q9p8o7n6m5l4k3j2i1h0g9f8e7d6c5b4a3z",
        "miner": "0x8ba1f109551bD432803012645Ac136ddd64DBA72",
        "size": 54321,
        "difficulty": 3456789012,
        "total_difficulty": 45678901234567,
        "extra_data": "0x476574682f76312e302e302d6c696e7578",
        "state_root": "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "transactions_root": "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
        "receipts_root": "0x9876543210fedcba9876543210fedcba9876543210fedcba9876543210fedcba",
        "base_fee_per_gas": 7.89,
        "next_block_base_fee": 8.12
    }

def blockscout_mcp_server_get_block_info(
    chain_id: str,
    number_or_hash: str,
    include_transactions: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get block information like timestamp, gas used, burnt fees, transaction count etc.
    Can optionally include the list of transaction hashes contained in the block.
    
    Args:
        chain_id (str): The ID of the blockchain
        number_or_hash (str): Block number or hash
        include_transactions (Optional[bool]): If true, includes a list of transaction hashes from the block.
    
    Returns:
        Dict containing block information with the following structure:
        - block_number (int): The number of the block in the blockchain
        - block_hash (str): The unique hash identifier of the block
        - parent_hash (str): The hash of the parent block
        - timestamp (str): The time when the block was created, in ISO 8601 format
        - gas_used (int): Total amount of gas used by transactions in the block
        - gas_limit (int): Maximum amount of gas allowed in the block
        - burnt_fees (float): Amount of fees burnt in the block
        - transaction_count (int): Number of transactions included in the block
        - transactions (List[str]): List of transaction hashes included in the block (only if include_transactions=True)
        - miner (str): Address of the miner or validator who produced the block
        - size (int): Size of the block in bytes
        - difficulty (int): Difficulty level of the block
        - total_difficulty (int): Cumulative difficulty up to this block
        - extra_data (str): Arbitrary data included by the miner
        - state_root (str): Root hash of the state trie after the block is applied
        - transactions_root (str): Root hash of the transactions trie in the block
        - receipts_root (str): Root hash of the receipts trie from transactions in the block
        - base_fee_per_gas (float): Base fee per gas unit in the block
        - next_block_base_fee (float): Suggested base fee for the next block
    """
    # Input validation
    if not chain_id:
        raise ValueError("chain_id is required")
    if not number_or_hash:
        raise ValueError("number_or_hash is required")
    
    # Call external API to get block data
    api_data = call_external_api("blockscout-mcp-server-get_block_info")
    
    # Construct the base result
    result = {
        "block_number": api_data["block_number"],
        "block_hash": api_data["block_hash"],
        "parent_hash": api_data["parent_hash"],
        "timestamp": api_data["timestamp"],
        "gas_used": api_data["gas_used"],
        "gas_limit": api_data["gas_limit"],
        "burnt_fees": api_data["burnt_fees"],
        "transaction_count": api_data["transaction_count"],
        "miner": api_data["miner"],
        "size": api_data["size"],
        "difficulty": api_data["difficulty"],
        "total_difficulty": api_data["total_difficulty"],
        "extra_data": api_data["extra_data"],
        "state_root": api_data["state_root"],
        "transactions_root": api_data["transactions_root"],
        "receipts_root": api_data["receipts_root"],
        "base_fee_per_gas": api_data["base_fee_per_gas"],
        "next_block_base_fee": api_data["next_block_base_fee"]
    }
    
    # Conditionally include transactions
    if include_transactions:
        result["transactions"] = [
            api_data["transaction_0"],
            api_data["transaction_1"]
        ]
    
    return result