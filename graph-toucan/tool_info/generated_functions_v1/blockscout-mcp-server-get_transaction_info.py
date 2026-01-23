from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching transaction data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - transaction_hash (str): The unique hash of the transaction
        - block_number (int): The block number in which the transaction was included
        - timestamp (str): Timestamp when the block was confirmed (ISO 8601)
        - from_address (str): Address of the sender
        - to_address (str): Address of the receiver; null if contract creation
        - contract_created (str): Address of the newly created contract if any
        - value (str): Value transferred in smallest unit (e.g., wei)
        - currency (str): Symbol and name of native currency (e.g., 'ETH Ethereum')
        - gas_used (int): Amount of gas consumed
        - gas_limit (int): Maximum gas allowed
        - gas_price (str): Price per gas unit (in smallest unit)
        - fee_currency (str): Currency used to pay fees
        - total_fee (str): Total transaction fee (gas_used * gas_price)
        - priority_fee (str): Portion of fee going to validators
        - burnt_fee (str): Portion of base fee burnt
        - max_fee_per_gas (str): Max fee per gas (EIP-1559)
        - max_priority_fee_per_gas (str): Max priority fee per gas (EIP-1559)
        - is_eip1559 (bool): Whether transaction uses EIP-1559
        - status (str): Transaction status ('success', 'failed', 'pending')
        - error (str): Error message if failed
        - method (str): Detected method name from input decoding
        - decoded_input_amountIn (str): Decoded input parameter amountIn
        - decoded_input_amountOutMin (str): Decoded input parameter amountOutMin
        - decoded_input_path (str): Decoded input parameter path
        - raw_input (str): Raw hexadecimal input data (only if requested)
        - token_transfers_0_token_address (str): Token address of first transfer
        - token_transfers_0_token_name (str): Token name
        - token_transfers_0_token_symbol (str): Token symbol
        - token_transfers_0_token_decimals (int): Token decimals
        - token_transfers_0_from (str): Transfer sender
        - token_transfers_0_to (str): Transfer receiver
        - token_transfers_0_value (str): Transfer value
        - token_transfers_0_type (str): Token type (e.g., 'ERC-20')
        - token_transfers_0_transfer_index (int): Index of transfer in tx
        - internal_calls_0_type (str): Type of internal call (e.g., 'CALL')
        - internal_calls_0_from (str): Internal call sender
        - internal_calls_0_to (str): Internal call receiver
        - internal_calls_0_value (str): Value transferred internally
        - internal_calls_0_gas (int): Gas allocated
        - internal_calls_0_input (str): Input data
        - internal_calls_0_output (str): Output data
        - internal_calls_0_depth (int): Call depth
        - internal_calls_0_error (str): Error if call failed
        - transaction_type (str): Categorized transaction type
        - chain_id (str): Blockchain network ID
        - confirmations (int): Number of block confirmations
        - nonce (int): Sender's nonce at time of transaction
    """
    return {
        "transaction_hash": "0xabc123def456...",
        "block_number": 19876543,
        "timestamp": "2023-11-15T14:23:45Z",
        "from_address": "0x1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t",
        "to_address": "0x9a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3q2r1s0t",
        "contract_created": None,
        "value": "0",
        "currency": "ETH Ethereum",
        "gas_used": 145000,
        "gas_limit": 200000,
        "gas_price": "20000000000",
        "fee_currency": "ETH Ethereum",
        "total_fee": "2900000000000000",
        "priority_fee": "1500000000000000",
        "burnt_fee": "1400000000000000",
        "max_fee_per_gas": "30000000000",
        "max_priority_fee_per_gas": "15000000000",
        "is_eip1559": True,
        "status": "success",
        "error": "",
        "method": "swapExactTokensForTokens",
        "decoded_input_amountIn": "1000000000000000000",
        "decoded_input_amountOutMin": "950000000000000000",
        "decoded_input_path": "0x...a->0x...b",
        "raw_input": "0xabcdef123456...",
        "token_transfers_0_token_address": "0x111111111117dc0aa78b770fa6a738034120c302",
        "token_transfers_0_token_name": "Uniswap",
        "token_transfers_0_token_symbol": "UNI",
        "token_transfers_0_token_decimals": 18,
        "token_transfers_0_from": "0x1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t",
        "token_transfers_0_to": "0x9a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3q2r1s0t",
        "token_transfers_0_value": "1000000000000000000",
        "token_transfers_0_type": "ERC-20",
        "token_transfers_0_transfer_index": 0,
        "internal_calls_0_type": "CALL",
        "internal_calls_0_from": "0x1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t",
        "internal_calls_0_to": "0x9a8b7c6d5e4f3g2h1i0j9k8l7m6n5o4p3q2r1s0t",
        "internal_calls_0_value": "0",
        "internal_calls_0_gas": 100000,
        "internal_calls_0_input": "0x...",
        "internal_calls_0_output": "0x...",
        "internal_calls_0_depth": 1,
        "internal_calls_0_error": "",
        "transaction_type": "smart_contract_interaction",
        "chain_id": "1",
        "confirmations": 1234,
        "nonce": 42
    }

def blockscout_mcp_server_get_transaction_info(
    chain_id: str,
    transaction_hash: str,
    include_raw_input: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get comprehensive transaction information from Blockscout.

    Unlike standard eth_getTransactionByHash, this returns enriched data including
    decoded input parameters, detailed token transfers with metadata, fee breakdown,
    and categorized transaction types.

    By default, raw transaction input is omitted if a decoded version is available.
    Set include_raw_input=True to include raw hex data.

    Args:
        chain_id (str): The ID of the blockchain
        transaction_hash (str): Transaction hash
        include_raw_input (Optional[bool]): If True, includes raw transaction input data

    Returns:
        Dict containing comprehensive transaction details with the following structure:
        - transaction_hash (str)
        - block_number (int)
        - timestamp (str)
        - from_address (str)
        - to_address (str)
        - contract_created (str)
        - value (str)
        - currency (str)
        - gas_used (int)
        - gas_limit (int)
        - gas_price (str)
        - fee_currency (str)
        - total_fee (str)
        - priority_fee (str)
        - burnt_fee (str)
        - max_fee_per_gas (str)
        - max_priority_fee_per_gas (str)
        - is_eip1559 (bool)
        - status (str)
        - error (str)
        - method (str)
        - decoded_input (Dict): Structured decoded parameters
        - raw_input (str, optional): Only present if include_raw_input=True
        - token_transfers (List[Dict]): List of token transfers with metadata
        - internal_calls (List[Dict]): List of internal calls during execution
        - transaction_type (str)
        - chain_id (str)
        - confirmations (int)
        - nonce (int)

    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not chain_id:
        raise ValueError("chain_id is required")
    if not transaction_hash:
        raise ValueError("transaction_hash is required")

    # Call external API to get flattened data
    api_data = call_external_api("blockscout-mcp-server-get_transaction_info")

    # Construct decoded_input if available
    decoded_input = {}
    if "decoded_input_amountIn" in api_data:
        decoded_input["amountIn"] = api_data["decoded_input_amountIn"]
    if "decoded_input_amountOutMin" in api_data:
        decoded_input["amountOutMin"] = api_data["decoded_input_amountOutMin"]
    if "decoded_input_path" in api_data:
        decoded_input["path"] = api_data["decoded_input_path"]

    # Construct token_transfers list
    token_transfers = []
    if "token_transfers_0_token_address" in api_data:
        token_transfers.append({
            "token_address": api_data["token_transfers_0_token_address"],
            "token_name": api_data["token_transfers_0_token_name"],
            "token_symbol": api_data["token_transfers_0_token_symbol"],
            "token_decimals": api_data["token_transfers_0_token_decimals"],
            "from": api_data["token_transfers_0_from"],
            "to": api_data["token_transfers_0_to"],
            "value": api_data["token_transfers_0_value"],
            "type": api_data["token_transfers_0_type"],
            "transfer_index": api_data["token_transfers_0_transfer_index"]
        })

    # Construct internal_calls list
    internal_calls = []
    if "internal_calls_0_type" in api_data:
        internal_calls.append({
            "type": api_data["internal_calls_0_type"],
            "from": api_data["internal_calls_0_from"],
            "to": api_data["internal_calls_0_to"],
            "value": api_data["internal_calls_0_value"],
            "gas": api_data["internal_calls_0_gas"],
            "input": api_data["internal_calls_0_input"],
            "output": api_data["internal_calls_0_output"],
            "depth": api_data["internal_calls_0_depth"],
            "error": api_data["internal_calls_0_error"]
        })

    # Build result dictionary
    result = {
        "transaction_hash": api_data["transaction_hash"],
        "block_number": api_data["block_number"],
        "timestamp": api_data["timestamp"],
        "from_address": api_data["from_address"],
        "to_address": api_data["to_address"],
        "contract_created": api_data["contract_created"],
        "value": api_data["value"],
        "currency": api_data["currency"],
        "gas_used": api_data["gas_used"],
        "gas_limit": api_data["gas_limit"],
        "gas_price": api_data["gas_price"],
        "fee_currency": api_data["fee_currency"],
        "total_fee": api_data["total_fee"],
        "priority_fee": api_data["priority_fee"],
        "burnt_fee": api_data["burnt_fee"],
        "max_fee_per_gas": api_data["max_fee_per_gas"],
        "max_priority_fee_per_gas": api_data["max_priority_fee_per_gas"],
        "is_eip1559": api_data["is_eip1559"],
        "status": api_data["status"],
        "error": api_data["error"] if api_data["error"] else None,
        "method": api_data["method"],
        "decoded_input": decoded_input,
        "token_transfers": token_transfers,
        "internal_calls": internal_calls,
        "transaction_type": api_data["transaction_type"],
        "chain_id": api_data["chain_id"],
        "confirmations": api_data["confirmations"],
        "nonce": api_data["nonce"]
    }

    # Include raw_input only if requested
    if include_raw_input:
        result["raw_input"] = api_data["raw_input"]

    return result