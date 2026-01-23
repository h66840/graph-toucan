from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Flow RPC server transaction submission.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - transactionHash (str): The unique hash of the submitted transaction
        - success (bool): Whether the transaction was accepted into the mempool
        - blockNumber (int): The block number where transaction was included, or null represented as 0 if not mined
        - gasUsed (int): Amount of gas consumed, or 0 if not available
        - status (str): Current status: 'pending', 'mined', or 'failed'
        - errorMessage (str): Error message if submission failed, otherwise empty string
        - metadata_timestamp (str): Timestamp of submission
        - metadata_nodeUrl (str): Node URL used for submission
        - metadata_chainId (str): Chain ID used for submission
    """
    return {
        "transactionHash": "0xabc123def456ghi789jkl012mno345pqr678stu901vwx234yz567",
        "success": True,
        "blockNumber": 15000000,
        "gasUsed": 21000,
        "status": "mined",
        "errorMessage": "",
        "metadata_timestamp": "2023-10-01T12:34:56Z",
        "metadata_nodeUrl": "https://flow-evm-mainnet.gateway.pokt.network/v1/lb/abc123",
        "metadata_chainId": "0xa"
    }

def flow_rpc_server_flow_sendRawTransaction(signedTransactionData: str) -> Dict[str, Any]:
    """
    Submits a signed transaction to the Flow EVM network.
    
    Args:
        signedTransactionData (str): The signed transaction data in hexadecimal format starting with 0x
        
    Returns:
        Dict containing the following fields:
        - transactionHash (str): The unique hash of the submitted transaction
        - success (bool): Indicates whether the transaction was accepted into the mempool
        - blockNumber (int or None): The block number where transaction was included, or None if not mined
        - gasUsed (int or None): Amount of gas consumed by the transaction, or None if not available
        - status (str): Current status of the transaction: 'pending', 'mined', or 'failed'
        - errorMessage (str or None): Error message if submission failed, otherwise None
        - metadata (Dict): Additional metadata including timestamp, node URL, and chain ID
        
    Raises:
        ValueError: If signedTransactionData is empty or not a valid hex string
    """
    # Input validation
    if not signedTransactionData:
        raise ValueError("signedTransactionData is required")
    
    if not isinstance(signedTransactionData, str):
        raise ValueError("signedTransactionData must be a string")
    
    if not signedTransactionData.startswith("0x"):
        raise ValueError("signedTransactionData must be a hexadecimal string starting with 0x")
    
    if len(signedTransactionData) < 10:  # Minimum length for a valid hex transaction
        raise ValueError("signedTransactionData is too short to be a valid transaction")
    
    # Call external API to simulate transaction submission
    api_data = call_external_api("flow-rpc-server-flow_sendRawTransaction")
    
    # Construct metadata dictionary from flattened fields
    metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "nodeUrl": api_data["metadata_nodeUrl"],
        "chainId": api_data["metadata_chainId"]
    }
    
    # Handle null values - convert 0 to None for blockNumber and gasUsed if appropriate
    block_number = api_data["blockNumber"] if api_data["blockNumber"] != 0 else None
    gas_used = api_data["gasUsed"] if api_data["gasUsed"] != 0 else None
    
    # Construct error message - use None instead of empty string
    error_message = api_data["errorMessage"] if api_data["errorMessage"] else None
    
    # Build final result structure matching output schema
    result = {
        "transactionHash": api_data["transactionHash"],
        "success": api_data["success"],
        "blockNumber": block_number,
        "gasUsed": gas_used,
        "status": api_data["status"],
        "errorMessage": error_message,
        "metadata": metadata
    }
    
    return result