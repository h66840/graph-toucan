from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for token transfers by address.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - data_0_from (str): Sender address of first transfer
        - data_0_to (str): Receiver address of first transfer
        - data_0_timestamp (str): ISO timestamp of first transfer
        - data_0_total_value (str): Value of first transfer as string
        - data_0_total_decimals (int): Decimal places for first transfer
        - data_0_type (str): Type of first transfer (e.g., 'transfer')
        - data_0_hash (str): Transaction hash of first transfer
        - data_0_token_address (str): Contract address of token in first transfer
        - data_0_token_name (str): Name of token in first transfer
        - data_0_token_symbol (str): Symbol of token in first transfer
        - data_0_token_decimals (int): Decimals of token in first transfer
        - data_0_method (str): Method used in first transfer
        - data_0_block_number (int): Block number of first transfer
        - data_0_transaction_index (int): Transaction index in block for first transfer
        - data_0_fee (str): Fee paid for first transfer
        - data_0_token_transfer_batch_index (int): Batch index for first transfer
        - data_0_token_transfer_index (int): Index within batch for first transfer
        - data_1_from (str): Sender address of second transfer
        - data_1_to (str): Receiver address of second transfer
        - data_1_timestamp (str): ISO timestamp of second transfer
        - data_1_total_value (str): Value of second transfer as string
        - data_1_total_decimals (int): Decimal places for second transfer
        - data_1_type (str): Type of second transfer
        - data_1_hash (str): Transaction hash of second transfer
        - data_1_token_address (str): Contract address of token in second transfer
        - data_1_token_name (str): Name of token in second transfer
        - data_1_token_symbol (str): Symbol of token in second transfer
        - data_1_token_decimals (int): Decimals of token in second transfer
        - data_1_method (str): Method used in second transfer
        - data_1_block_number (int): Block number of second transfer
        - data_1_transaction_index (int): Transaction index in block for second transfer
        - data_1_fee (str): Fee paid for second transfer
        - data_1_token_transfer_batch_index (int): Batch index for second transfer
        - data_1_token_transfer_index (int): Index within batch for second transfer
        - data_description (str): Description of the data
        - notes (str): Additional notes from API
        - instructions (str): Instructions for next steps
        - pagination_next_page (str): URL or token for next page
        - pagination_total (int): Total number of results available
    """
    return {
        "data_0_from": "0x1234567890123456789012345678901234567890",
        "data_0_to": "0x0987654321098765432109876543210987654321",
        "data_0_timestamp": "2025-05-22T23:15:30.00Z",
        "data_0_total_value": "1500000000000000000",
        "data_0_total_decimals": 18,
        "data_0_type": "transfer",
        "data_0_hash": "0xabc123def456...",
        "data_0_token_address": "0xDEF17eC8a3cE52fA5D6E63bBa5bF888d7d5C2b1a",
        "data_0_token_name": "ExampleToken",
        "data_0_token_symbol": "EXT",
        "data_0_token_decimals": 18,
        "data_0_method": "transfer",
        "data_0_block_number": 12345678,
        "data_0_transaction_index": 0,
        "data_0_fee": "21000000000000000",
        "data_0_token_transfer_batch_index": 0,
        "data_0_token_transfer_index": 0,
        "data_1_from": "0x0987654321098765432109876543210987654321",
        "data_1_to": "0x1234567890123456789012345678901234567890",
        "data_1_timestamp": "2025-05-22T22:45:10.00Z",
        "data_1_total_value": "500000000000000000",
        "data_1_total_decimals": 18,
        "data_1_type": "transfer",
        "data_1_hash": "0xdef456ghi789...",
        "data_1_token_address": "0xDEF17eC8a3cE52fA5D6E63bBa5bF888d7d5C2b1a",
        "data_1_token_name": "ExampleToken",
        "data_1_token_symbol": "EXT",
        "data_1_token_decimals": 18,
        "data_1_method": "transfer",
        "data_1_block_number": 12345600,
        "data_1_transaction_index": 2,
        "data_1_fee": "21000000000000000",
        "data_1_token_transfer_batch_index": 0,
        "data_1_token_transfer_index": 1,
        "data_description": "ERC-20 token transfers for the given address",
        "notes": "Results are paginated by time range",
        "instructions": "Use age_to from last record to fetch older transfers",
        "pagination_next_page": "timestamp=1716417930",
        "pagination_total": 250
    }

def blockscout_mcp_server_get_token_transfers_by_address(
    address: str,
    chain_id: str,
    age_from: Optional[str] = None,
    age_to: Optional[str] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get ERC-20 token transfers for an address within a specific time range.
    
    This function simulates querying a blockchain explorer API to retrieve token transfer history
    for a given address. It supports filtering by time range and specific token contract.
    
    Args:
        address (str): Address which either transfer initiator or transfer receiver
        chain_id (str): The ID of the blockchain
        age_from (Optional[str]): Start date and time in ISO format (e.g., '2025-05-22T23:00:00.00Z')
        age_to (Optional[str]): End date and time in ISO format (e.g., '2025-05-22T22:30:00.00Z')
        token (Optional[str]): ERC-20 token contract address to filter by specific token
        
    Returns:
        Dict containing:
        - data (List[Dict]): List of token transfer records with full details
        - data_description (str): Description of the returned data
        - notes (str): Additional notes from the API
        - instructions (str): Instructions for pagination or next steps
        - pagination (Dict): Pagination metadata including next page info and total count
        
    Raises:
        ValueError: If address or chain_id is empty or invalid
    """
    # Input validation
    if not address:
        raise ValueError("Address is required")
    if not chain_id:
        raise ValueError("Chain ID is required")
    
    # Validate timestamps if provided
    if age_from:
        try:
            datetime.fromisoformat(age_from.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Invalid ISO format for age_from: {age_from}")
    
    if age_to:
        try:
            datetime.fromisoformat(age_to.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(f"Invalid ISO format for age_to: {age_to}")
    
    # Call external API (simulated)
    api_data = call_external_api("blockscout-mcp-server-get_token_transfers_by_address")
    
    # Transform the flat API response into the expected nested structure
    data = []
    
    # Process first transfer if available
    if "data_0_hash" in api_data:
        data.append({
            "from": api_data["data_0_from"],
            "to": api_data["data_0_to"],
            "timestamp": api_data["data_0_timestamp"],
            "total_value": api_data["data_0_total_value"],
            "total_decimals": api_data["data_0_total_decimals"],
            "type": api_data["data_0_type"],
            "hash": api_data["data_0_hash"],
            "token_address": api_data["data_0_token_address"],
            "token_name": api_data["data_0_token_name"],
            "token_symbol": api_data["data_0_token_symbol"],
            "token_decimals": api_data["data_0_token_decimals"],
            "method": api_data["data_0_method"],
            "block_number": api_data["data_0_block_number"],
            "transaction_index": api_data["data_0_transaction_index"],
            "fee": api_data["data_0_fee"],
            "token_transfer_batch_index": api_data["data_0_token_transfer_batch_index"],
            "token_transfer_index": api_data["data_0_token_transfer_index"]
        })
    
    # Process second transfer if available
    if "data_1_hash" in api_data:
        data.append({
            "from": api_data["data_1_from"],
            "to": api_data["data_1_to"],
            "timestamp": api_data["data_1_timestamp"],
            "total_value": api_data["data_1_total_value"],
            "total_decimals": api_data["data_1_total_decimals"],
            "type": api_data["data_1_type"],
            "hash": api_data["data_1_hash"],
            "token_address": api_data["data_1_token_address"],
            "token_name": api_data["data_1_token_name"],
            "token_symbol": api_data["data_1_token_symbol"],
            "token_decimals": api_data["data_1_token_decimals"],
            "method": api_data["data_1_method"],
            "block_number": api_data["data_1_block_number"],
            "transaction_index": api_data["data_1_transaction_index"],
            "fee": api_data["data_1_fee"],
            "token_transfer_batch_index": api_data["data_1_token_transfer_batch_index"],
            "token_transfer_index": api_data["data_1_token_transfer_index"]
        })
    
    # Construct the final response
    result = {
        "data": data,
        "data_description": api_data.get("data_description", ""),
        "notes": api_data.get("notes", ""),
        "instructions": api_data.get("instructions", ""),
        "pagination": {
            "next_page": api_data.get("pagination_next_page", ""),
            "total": api_data.get("pagination_total", 0)
        }
    }
    
    return result