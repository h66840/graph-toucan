from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Flow EVM gas price.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - gas_price_atto_flow (str): Current gas price in Atto-FLOW as string
        - gas_price_gwei (str): Current gas price in Gwei as string
    """
    return {
        "gas_price_atto_flow": "1000000000000000",
        "gas_price_gwei": "1"
    }

def flow_rpc_server_flow_gasPrice() -> Dict[str, str]:
    """
    Retrieves the current gas price in Flow EVM.

    This function queries the external RPC server to get the current gas price
    and returns it in both Atto-FLOW and Gwei units.

    Returns:
        Dict containing:
        - gas_price_atto_flow (str): Gas price value in Atto-FLOW as a string
        - gas_price_gwei (str): Gas price value in Gwei as a string

    Example:
        {
            "gas_price_atto_flow": "1000000000000000",
            "gas_price_gwei": "1"
        }
    """
    try:
        # Call external API to get gas price data
        api_data = call_external_api("flow-rpc-server-flow_gasPrice")
        
        # Extract and validate required fields
        gas_price_atto_flow = api_data.get("gas_price_atto_flow")
        gas_price_gwei = api_data.get("gas_price_gwei")
        
        # Validate that required fields are present and are strings
        if not isinstance(gas_price_atto_flow, str):
            raise ValueError("gas_price_atto_flow must be a string")
        if not isinstance(gas_price_gwei, str):
            raise ValueError("gas_price_gwei must be a string")
        
        # Construct result dictionary matching output schema
        result = {
            "gas_price_atto_flow": gas_price_atto_flow,
            "gas_price_gwei": gas_price_gwei
        }
        
        return result
        
    except Exception as e:
        # Handle any errors during the process
        raise RuntimeError(f"Failed to retrieve gas price: {str(e)}")