from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DefiLlama TVL endpoint.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - tvl (float): Total value locked in USD for the requested protocol
        - error (str): Error message if protocol not found or other issue
        - status (str): Status of the response, typically "error" on failure
    """
    # Simulated response data based on tool name
    if tool_name == "defillama-api-server-get_tvl__by_protocol":
        return {
            "tvl": 1250000000.50,
            "error": "",
            "status": "success"
        }
    else:
        return {
            "tvl": 0.0,
            "error": "Unknown tool name",
            "status": "error"
        }

def defillama_api_server_get_tvl_by_protocol(protocol: str) -> Dict[str, Any]:
    """
    Simplified endpoint to get current TVL of a protocol.
    
    Args:
        protocol (str): Protocol slug (e.g., 'uniswap', 'aave') - required
        
    Returns:
        Dict containing:
        - tvl (float, optional): Total value locked in USD if available
        - error (str, optional): Error message if request failed
        - status (str, optional): Status of the response ("error" on failure)
        
    Example:
        {
            "tvl": 1250000000.5,
            "status": "success"
        }
        
        or in case of error:
        
        {
            "error": "Protocol not found",
            "status": "error"
        }
    """
    # Input validation
    if not protocol or not isinstance(protocol, str) or len(protocol.strip()) == 0:
        return {
            "error": "Protocol parameter is required and must be a non-empty string",
            "status": "error"
        }
    
    # Call external API simulation
    api_data = call_external_api("defillama-api-server-get_tvl__by_protocol")
    
    # Construct response matching output schema
    result: Dict[str, Any] = {}
    
    # Handle error case
    if api_data.get("status") == "error":
        result["error"] = api_data.get("error", "Unknown error occurred")
        result["status"] = "error"
        return result
    
    # Success case
    tvl_value = api_data.get("tvl", 0.0)
    if tvl_value is None or tvl_value <= 0:
        result["error"] = "No TVL data available for the requested protocol"
        result["status"] = "error"
    else:
        result["tvl"] = float(tvl_value)
        result["status"] = "success"
    
    # Remove status if success (as per typical API behavior where status may be absent on success)
    if result["status"] == "success":
        # Keep status only if explicitly required; based on schema it may be present even on success
        # Keeping it as per output fields description which says "typically 'error' when there is a problem"
        pass
    
    return result