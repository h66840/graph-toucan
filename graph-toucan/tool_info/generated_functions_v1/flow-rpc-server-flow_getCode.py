from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Flow RPC server getCode method.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - has_code (bool): whether code is present at the address
        - is_contract (bool): indicates if the address contains a smart contract
        - address (str): the Flow EVM address queried, formatted as 0x + 40 hex chars
        - message (str): human-readable explanation of the result
    """
    return {
        "has_code": True,
        "is_contract": True,
        "address": "0x1234567890123456789012345678901234567890",
        "message": "Contract code found at the specified address."
    }

def flow_rpc_server_flow_getCode(address: str, blockParameter: Optional[str] = "latest") -> Dict[str, Any]:
    """
    Retrieves the code at a given Flow EVM address.
    
    This function queries the Flow RPC server to determine if there is contract code
    at the specified EVM address on the Flow blockchain. It returns information about
    whether the address contains code and if it represents a smart contract.
    
    Args:
        address (str): The Flow EVM address to get code from (required)
        blockParameter (str, optional): Block parameter for the query (default: "latest")
    
    Returns:
        Dict[str, Any] with the following fields:
        - has_code (bool): whether code is present at the address (True if contract, False otherwise)
        - is_contract (bool): indicates if the address contains a smart contract
        - address (str): the Flow EVM address that was queried, formatted as 0x + 40 hex chars
        - message (str): human-readable explanation of the result
    
    Raises:
        ValueError: If address is not a valid EVM address format
    """
    # Input validation
    if not address:
        raise ValueError("Address is required")
    
    # Basic EVM address format validation
    if not address.startswith("0x") or len(address) != 42:
        raise ValueError("Invalid EVM address format: must be 0x followed by 40 hexadecimal characters")
    
    if not all(c in "0123456789abcdefABCDEF" for c in address[2:]):
        raise ValueError("Invalid EVM address format: invalid hexadecimal characters")
    
    # Call external API to get data
    api_data = call_external_api("flow-rpc-server-flow_getCode")
    
    # Construct result matching output schema
    result = {
        "has_code": api_data["has_code"],
        "is_contract": api_data["is_contract"],
        "address": api_data["address"],
        "message": api_data["message"]
    }
    
    return result