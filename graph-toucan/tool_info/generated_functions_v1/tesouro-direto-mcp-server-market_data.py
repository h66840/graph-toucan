from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching market data from Tesouro Direto API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - market_status_opening_time (str): Market opening time in ISO format
        - market_status_closing_time (str): Market closing time in ISO format
        - market_status_quotation_time (str): Quotation time in ISO format
        - market_status_status_code (int): Status code of market (e.g., 200)
        - market_status_status (str): Human-readable market status (e.g., "open")
        - business_status_code (str): Business operation status code (e.g., "ACTIVE")
        - business_status_timestamp (str): Timestamp of last business status update in ISO format
    """
    return {
        "market_status_opening_time": "09:00:00",
        "market_status_closing_time": "17:00:00",
        "market_status_quotation_time": "10:30:00",
        "market_status_status_code": 200,
        "market_status_status": "open",
        "business_status_code": "ACTIVE",
        "business_status_timestamp": "2023-10-05T12:34:56Z"
    }

def tesouro_direto_mcp_server_market_data() -> Dict[str, Any]:
    """
    Retrieves general market data from Tesouro Direto, including opening/closing times and status.
    
    This function simulates querying an external API to get current market and business status.
    It returns structured data with market hours, quotation time, operational status, and business status.
    
    Returns:
        Dict containing:
        - market_status (Dict): Contains 'opening_time', 'closing_time', 'quotation_time', 
          'status_code', and 'status' fields describing current market state
        - business_status (Dict): Contains 'code' and 'timestamp' fields indicating 
          business operation status and time of last update
    """
    try:
        # Call external API to get flat data
        api_data = call_external_api("tesouro-direto-mcp-server-market_data")
        
        # Construct nested market_status object
        market_status = {
            "opening_time": api_data["market_status_opening_time"],
            "closing_time": api_data["market_status_closing_time"],
            "quotation_time": api_data["market_status_quotation_time"],
            "status_code": api_data["market_status_status_code"],
            "status": api_data["market_status_status"]
        }
        
        # Construct nested business_status object
        business_status = {
            "code": api_data["business_status_code"],
            "timestamp": api_data["business_status_timestamp"]
        }
        
        # Return final structured response
        return {
            "market_status": market_status,
            "business_status": business_status
        }
        
    except KeyError as e:
        # Handle missing fields in API response
        raise KeyError(f"Missing required field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve market data: {str(e)}") from e