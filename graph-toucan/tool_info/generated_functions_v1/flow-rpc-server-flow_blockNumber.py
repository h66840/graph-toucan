from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Flow EVM network block number.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hex (str): hexadecimal representation of the latest block number, prefixed with '0x'
        - decimal (int): decimal representation of the latest block number
    """
    return {
        "hex": "0x1a2b3c",
        "decimal": 1715196
    }

def flow_rpc_server_flow_blockNumber() -> Dict[str, Any]:
    """
    Gets the latest block number on the Flow EVM network.
    
    This function queries an external RPC server to retrieve the current block number
    from the Flow EVM network, returning both hexadecimal and decimal representations.
    
    Returns:
        Dict containing:
        - hex (str): hexadecimal representation of the latest block number, prefixed with '0x'
        - decimal (int): decimal (base-10) representation of the latest block number
    
    Example:
        {
            "hex": "0x1a2b3c",
            "decimal": 1715196
        }
    """
    try:
        # Call external API to get block number data
        api_data = call_external_api("flow-rpc-server-flow_blockNumber")
        
        # Construct result matching output schema
        result = {
            "hex": api_data["hex"],
            "decimal": api_data["decimal"]
        }
        
        return result
        
    except Exception as e:
        # In a real implementation, we might log the error here
        # For now, re-raise with a generic message
        raise Exception(f"Failed to retrieve block number: {str(e)}")