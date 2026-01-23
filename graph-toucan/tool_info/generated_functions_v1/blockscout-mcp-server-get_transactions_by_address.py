from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching transaction data from an external Blockscout API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool), representing
        flattened version of nested response structure. For list fields, two items are generated (index 0 and 1).
        
        - data_0_from (str): Sender address of first transaction
        - data_0_to (str): Recipient address of first transaction
        - data_0_timestamp (str): ISO 8601 timestamp of first transaction
        - data_0_type (str): Type of first transaction (e.g., 'coin_transfer')
        - data_0_value (str): Value in wei of first transaction
        - data_0_hash (str): Transaction hash of first transaction
        - data_0_method (str or None): Method signature if applicable for first transaction
        - data_0_block_number (int): Block number of first transaction
        - data_0_transaction_index (int): Index within block for first transaction
        - data_0_fee (str): Fee in wei for first transaction
        - data_0_internal_transaction_index (int or None): Execution order for internal calls for first transaction
        - data_0_created_contract_address (str or None): Created contract address if applicable for first transaction
        - data_0_created_contract_bytecode (str or None): Created contract bytecode if applicable for first transaction
        
        - data_1_from (str): Sender address of second transaction
        - data_1_to (str): Recipient address of second transaction
        - data_1_timestamp (str): ISO 8601 timestamp of second transaction
        - data_1_type (str): Type of second transaction
        - data_1_value (str): Value in wei of second transaction
        - data_1_hash (str): Transaction hash of second transaction
        - data_1_method (str or None): Method signature if applicable for second transaction
        - data_1_block_number (int): Block number of second transaction
        - data_1_transaction_index (int): Index within block for second transaction
        - data_1_fee (str): Fee in wei for second transaction
        - data_1_internal_transaction_index (int or None): Execution order for internal calls for second transaction
        - data_1_created_contract_address (str or None): Created contract address if applicable for second transaction
        - data_1_created_contract_bytecode (str or None): Created contract bytecode if applicable for second transaction
        
        - data_description (str or None): Description of the data returned
        - notes (str or None): Additional notes from the system
        - instructions_0 (str or None): First instruction message (e.g., pagination guidance)
        - instructions_1 (str or None): Second instruction message
        - pagination_next_call_tool_name (str or None): Name of tool to call for next page
        - pagination_next_call_params_address (str or None): Address parameter for next page
        - pagination_next_call_params_age_from (str or None): Start time for next page
        - pagination_next_call_params_age_to (str or None): End time for next page
        - pagination_next_call_params_chain_id (str or None): Chain ID for next page
        - pagination_next_call_params_methods (str or None): Methods filter for next page
    """
    return {
        "data_0_from": "0x1234567890123456789012345678901234567890",
        "data_0_to": "0x0987654321098765432109876543210987654321",
        "data_0_timestamp": "2025-05-22T23:05:00.00Z",
        "data_0_type": "coin_transfer",
        "data_0_value": "1000000000000000000",
        "data_0_hash": "0xabc123def456...",
        "data_0_method": None,
        "data_0_block_number": 1234567,
        "data_0_transaction_index": 0,
        "data_0_fee": "21000000000000000",
        "data_0_internal_transaction_index": None,
        "data_0_created_contract_address": None,
        "data_0_created_contract_bytecode": None,

        "data_1_from": "0x0987654321098765432109876543210987654321",
        "data_1_to": "0x1111111111111111111111111111111111111111",
        "data_1_timestamp": "2025-05-22T23:10:00.00Z",
        "data_1_type": "contract_call",
        "data_1_value": "500000000000000000",
        "data_1_hash": "0xdef456abc789...",
        "data_1_method": "0x304e6ade",
        "data_1_block_number": 1234568,
        "data_1_transaction_index": 1,
        "data_1_fee": "42000000000000000",
        "data_1_internal_transaction_index": 0,
        "data_1_created_contract_address": "0x2222222222222222222222222222222222222222",
        "data_1_created_contract_bytecode": "0x6080604052...",

        "data_description": "Transaction history for the given address excluding token transfers.",
        "notes": "This result excludes ERC-20 and other token transfer events. Use get_token_transfers_by_address for token history.",
        "instructions_0": "Use age_from and age_to parameters to paginate by time intervals.",
        "instructions_1": "Filter by method signature to narrow down contract interactions.",
        "pagination_next_call_tool_name": "blockscout_mcp_server_get_transactions_by_address",
        "pagination_next_call_params_address": "0x1234567890123456789012345678901234567890",
        "pagination_next_call_params_age_from": "2025-05-22T23:15:00.00Z",
        "pagination_next_call_params_age_to": "2025-05-22T23:30:00.00Z",
        "pagination_next_call_params_chain_id": "1",
        "pagination_next_call_params_methods": "0x304e6ade"
    }

def blockscout_mcp_server_get_transactions_by_address(
    address: str,
    chain_id: str,
    age_from: Optional[str] = None,
    age_to: Optional[str] = None,
    methods: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves native currency transfers and smart contract interactions (calls, internal txs) for an address.
    EXCLUDES TOKEN TRANSFERS: Filters out direct token balance changes (ERC-20, etc.).
    You'll see calls *to* token contracts, but not the `Transfer` events.
    For token history, use `get_token_transfers_by_address`.
    
    A single tx can have multiple records from internal calls; use `internal_transaction_index` for execution order.
    
    Args:
        address (str): Address which is either sender or receiver of the transaction
        age_from (Optional[str]): Start date and time in ISO 8601 format (e.g., '2025-05-22T23:00:00.00Z')
        age_to (Optional[str]): End date and time in ISO 8601 format (e.g., '2025-05-22T23:30:00.00Z')
        chain_id (str): The ID of the blockchain
        methods (Optional[str]): Method signature to filter transactions by (e.g., '0x304e6ade')
    
    Returns:
        Dict containing:
        - data (List[Dict]): List of transaction records with fields:
            - from (str)
            - to (str)
            - timestamp (str in ISO 8601)
            - type (str)
            - value (str in wei)
            - hash (str)
            - method (str or None)
            - block_number (int)
            - transaction_index (int)
            - fee (str in wei)
            - internal_transaction_index (int or None): Execution order for internal calls
            - created_contract_address (str or None): Address of created contract (for contract creation txs)
            - created_contract_bytecode (str or None): Bytecode of created contract
        - data_description (str or None): Description of the returned data
        - notes (List[str] or None): Additional system notes
        - instructions (List[str] or None): Guidance for next steps (e.g., pagination)
        - pagination (Dict or None): Parameters for fetching next page
    """
    result = call_external_api("blockscout_mcp_server_get_transactions_by_address")
    
    data = [
        {
            "from": result["data_0_from"],
            "to": result["data_0_to"],
            "timestamp": result["data_0_timestamp"],
            "type": result["data_0_type"],
            "value": result["data_0_value"],
            "hash": result["data_0_hash"],
            "method": result["data_0_method"],
            "block_number": result["data_0_block_number"],
            "transaction_index": result["data_0_transaction_index"],
            "fee": result["data_0_fee"],
            "internal_transaction_index": result["data_0_internal_transaction_index"],
            "created_contract_address": result["data_0_created_contract_address"],
            "created_contract_bytecode": result["data_0_created_contract_bytecode"]
        },
        {
            "from": result["data_1_from"],
            "to": result["data_1_to"],
            "timestamp": result["data_1_timestamp"],
            "type": result["data_1_type"],
            "value": result["data_1_value"],
            "hash": result["data_1_hash"],
            "method": result["data_1_method"],
            "block_number": result["data_1_block_number"],
            "transaction_index": result["data_1_transaction_index"],
            "fee": result["data_1_fee"],
            "internal_transaction_index": result["data_1_internal_transaction_index"],
            "created_contract_address": result["data_1_created_contract_address"],
            "created_contract_bytecode": result["data_1_created_contract_bytecode"]
        }
    ]
    
    response = {
        "data": data,
        "data_description": result["data_description"],
        "notes": [result["notes"]] if result["notes"] else None,
        "instructions": [
            result["instructions_0"],
            result["instructions_1"]
        ],
        "pagination": {
            "next_call": {
                "tool_name": result["pagination_next_call_tool_name"],
                "params": {
                    "address": result["pagination_next_call_params_address"],
                    "age_from": result["pagination_next_call_params_age_from"],
                    "age_to": result["pagination_next_call_params_age_to"],
                    "chain_id": result["pagination_next_call_params_chain_id"],
                    "methods": result["pagination_next_call_params_methods"]
                }
            } if result["pagination_next_call_tool_name"] else None
        }
    }
    
    return response