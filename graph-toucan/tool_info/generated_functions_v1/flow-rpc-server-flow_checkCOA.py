from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for checking if an address is a Cadence-Owned Account (COA).
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - is_coa (bool): whether the address is a Cadence-Owned Account (COA)
        - description (str): human-readable explanation of the result, including account type if not a COA
        - error_code (str): error code if request fails, otherwise None
        - error_message (str): error message if request fails, otherwise None
        - error_path (str): path related to the error, otherwise None
    """
    # Simulated response based on tool_name
    if tool_name == "flow-rpc-server-flow_checkCOA":
        return {
            "is_coa": True,
            "description": "The address is a valid Cadence-Owned Account (COA).",
            "error_code": None,
            "error_message": None,
            "error_path": None
        }
    else:
        return {
            "is_coa": False,
            "description": "Unknown tool name provided.",
            "error_code": "UNKNOWN_TOOL",
            "error_message": "The requested tool does not exist.",
            "error_path": "/tool_name"
        }

def flow_rpc_server_flow_checkCOA(address: str) -> Dict[str, Any]:
    """
    Checks if a given Flow EVM address is a Cadence-Owned Account (COA).
    
    This function simulates querying an external service to determine whether the provided
    address is a Cadence-Owned Account (COA), returning a structured result with a boolean
    flag, description, and optional error details.

    Args:
        address (str): The Flow EVM address to check. Must be a non-empty string.

    Returns:
        Dict containing:
            - is_coa (bool): True if the address is a COA, False otherwise.
            - description (str): Human-readable explanation of the result.
            - error (Optional[Dict]): Present only if there was an error, with keys:
                - code (str)
                - message (str)
                - path (str)
    
    Raises:
        ValueError: If the address is empty or not a string.
    """
    # Input validation
    if not isinstance(address, str):
        raise ValueError("Address must be a string.")
    if not address.strip():
        raise ValueError("Address cannot be empty or whitespace.")
    
    # Call external API simulation
    api_data = call_external_api("flow-rpc-server-flow_checkCOA")
    
    # Construct result according to output schema
    result: Dict[str, Any] = {
        "is_coa": api_data["is_coa"],
        "description": api_data["description"]
    }
    
    # Add error object only if error fields are present and not None
    if api_data["error_code"] is not None or api_data["error_message"] is not None or api_data["error_path"] is not None:
        result["error"] = {}
        if api_data["error_code"] is not None:
            result["error"]["code"] = api_data["error_code"]
        if api_data["error_message"] is not None:
            result["error"]["message"] = api_data["error_message"]
        if api_data["error_path"] is not None:
            result["error"]["path"] = api_data["error_path"]
    
    return result