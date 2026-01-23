from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Flow EVM network information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - network_name (str): Name of the Flow EVM network
        - rpc_endpoint (str): URL of the RPC endpoint for the network
        - chain_id (int): Unique identifier for the blockchain network
        - block_explorer (str): URL of the block explorer for the network
        - currency (str): Native currency symbol used on the network
    """
    return {
        "network_name": "Flow EVM Testnet",
        "rpc_endpoint": "https://testnet.evm.nodes.onflow.org",
        "chain_id": 68840142,
        "block_explorer": "https://testnet.flowscan.io",
        "currency": "FLOW"
    }

def flow_rpc_server_flow_getNetworkInfo() -> Dict[str, Any]:
    """
    Retrieves information about the current Flow EVM network configuration.
    
    This function queries an external API to obtain details about the Flow EVM network,
    including network name, RPC endpoint, chain ID, block explorer URL, and native currency.
    
    Returns:
        Dict containing the following keys:
        - network_name (str): Name of the Flow EVM network (e.g., "Flow EVM Testnet")
        - rpc_endpoint (str): URL of the RPC endpoint for interacting with the network
        - chain_id (int): Unique identifier for the blockchain network
        - block_explorer (str): URL of the block explorer for viewing transactions and addresses
        - currency (str): Native currency symbol used on the network (e.g., "FLOW")
    
    Example:
        {
            "network_name": "Flow EVM Testnet",
            "rpc_endpoint": "https://testnet.evm.nodes.onflow.org",
            "chain_id": 68840142,
            "block_explorer": "https://testnet.flowscan.io",
            "currency": "FLOW"
        }
    """
    try:
        # Fetch data from external API
        api_data = call_external_api("flow-rpc-server-flow_getNetworkInfo")
        
        # Construct result dictionary matching output schema
        result = {
            "network_name": api_data["network_name"],
            "rpc_endpoint": api_data["rpc_endpoint"],
            "chain_id": api_data["chain_id"],
            "block_explorer": api_data["block_explorer"],
            "currency": api_data["currency"]
        }
        
        return result
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve network info: {str(e)}")