from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Flow EVM chain ID.

    Returns:
        Dict with simple fields only (str, int):
        - chain_id_hex (str): Hexadecimal representation of the current Flow EVM chain ID, including '0x' prefix
        - chain_id_decimal (int): Decimal representation of the current Flow EVM chain ID
    """
    return {
        "chain_id_hex": "0x6f",
        "chain_id_decimal": 111
    }

def flow_rpc_server_flow_chainId() -> Dict[str, Any]:
    """
    Retrieves the current chain ID of the Flow EVM network.

    This function queries an external RPC server to get the current chain ID
    of the Flow EVM network and returns both hexadecimal and decimal representations.

    Returns:
        Dict containing:
        - chain_id_hex (str): Hexadecimal representation of the current Flow EVM chain ID, including '0x' prefix
        - chain_id_decimal (int): Decimal representation of the current Flow EVM chain ID
    """
    try:
        # Call external API to get chain ID data
        api_data = call_external_api("flow-rpc-server-flow_chainId")
        
        # Extract and validate required fields
        chain_id_hex = api_data.get("chain_id_hex")
        chain_id_decimal = api_data.get("chain_id_decimal")
        
        # Validate that required fields are present and of correct type
        if not isinstance(chain_id_hex, str):
            raise ValueError("chain_id_hex must be a string")
        if not isinstance(chain_id_decimal, int):
            raise ValueError("chain_id_decimal must be an integer")
        
        # Validate hex string format
        if not chain_id_hex.startswith("0x"):
            raise ValueError("chain_id_hex must start with '0x' prefix")
        
        # Construct result dictionary matching output schema
        result = {
            "chain_id_hex": chain_id_hex,
            "chain_id_decimal": chain_id_decimal
        }
        
        return result
        
    except Exception as e:
        # Handle any errors during the process
        raise RuntimeError(f"Failed to retrieve Flow EVM chain ID: {str(e)}")