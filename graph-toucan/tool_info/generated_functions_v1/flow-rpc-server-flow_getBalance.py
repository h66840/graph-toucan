from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Flow EVM balance retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - balance_attoflow (str): Balance amount in Atto-FLOW as a string
        - balance_flow (str): Balance amount in FLOW as a formatted decimal string
    """
    # Simulated realistic balance values based on address and block parameter
    return {
        "balance_attoflow": "1234567890000000000",
        "balance_flow": "1.23456789"
    }

def flow_rpc_server_flow_getBalance(address: str, blockParameter: Optional[str] = "latest") -> Dict[str, str]:
    """
    Retrieves the balance of a given Flow EVM address.
    
    This function simulates querying the Flow blockchain RPC server to get
    the account balance in both Atto-FLOW (smallest unit) and human-readable FLOW.
    
    Args:
        address (str): The Flow EVM address to check balance. Must be a valid hex address.
        blockParameter (Optional[str]): Block parameter for balance query. Default is "latest".
            Can be "latest", "earliest", "pending", or a specific block number.
    
    Returns:
        Dict[str, str]: A dictionary containing:
            - balance_attoflow (str): Balance amount in Atto-FLOW as a string
            - balance_flow (str): Balance amount in FLOW as a formatted decimal string
    
    Raises:
        ValueError: If address is empty or invalid
    """
    # Input validation
    if not address:
        raise ValueError("Address is required")
    
    if not isinstance(address, str):
        raise ValueError("Address must be a string")
    
    if not address.startswith("0x") or len(address) < 42:
        raise ValueError("Invalid Flow EVM address format. Must be a valid hex address starting with 0x")
    
    # Optional blockParameter validation
    if blockParameter and not isinstance(blockParameter, str):
        raise ValueError("Block parameter must be a string")
    
    # Call external API to get balance data
    api_data = call_external_api("flow-rpc-server-flow_getBalance")
    
    # Construct result matching output schema
    result = {
        "balance_attoflow": api_data["balance_attoflow"],
        "balance_flow": api_data["balance_flow"]
    }
    
    return result