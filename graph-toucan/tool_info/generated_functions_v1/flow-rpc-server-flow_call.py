from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for flow-rpc-server-flow_call.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result (str): Hexadecimal string representing the output of the contract function call
    """
    return {
        "result": "0x1234abcd"
    }

def flow_rpc_server_flow_call(blockParameter: Optional[str] = "latest", transaction: Dict[str, Any] = None) -> Dict[str, str]:
    """
    Executes a call to a contract function without creating a transaction.

    Args:
        blockParameter (Optional[str]): Block parameter (default: "latest")
        transaction (Dict[str, Any]): The transaction call object (required)

    Returns:
        Dict[str, str]: A dictionary containing the result of the contract function call
            - result (str): Hexadecimal string representing the output of the contract function call;
                            empty or "0x" indicates no return value or failed call

    Raises:
        ValueError: If transaction is not provided
    """
    if transaction is None:
        raise ValueError("transaction is required")

    # Validate transaction structure (basic check for essential fields)
    if not isinstance(transaction, dict):
        raise ValueError("transaction must be a dictionary")

    # Call external API to simulate RPC call
    api_data = call_external_api("flow-rpc-server-flow_call")

    # Construct result following output schema
    result = {
        "result": api_data["result"]
    }

    return result