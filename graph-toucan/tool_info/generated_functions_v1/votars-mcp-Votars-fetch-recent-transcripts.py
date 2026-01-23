from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for retrieving recent transcripts.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - code (int): Numeric status code indicating the result of the request
        - msg (str): Descriptive message associated with the status code
    """
    return {
        "code": 200,
        "msg": "Transcripts retrieved successfully"
    }

def votars_mcp_Votars_fetch_recent_transcripts() -> Dict[str, Any]:
    """
    Retrieve recent transcripts from workspace by querying an external API.
    
    This function acts as a wrapper around an external API call, fetching recent 
    transcripts and returning structured information about the operation result.
    
    Returns:
        Dict containing:
        - code (int): Numeric status code indicating the result of the request
        - msg (str): Descriptive message associated with the status code, 
                     providing context such as error details or success confirmation
    """
    try:
        # Call external API to get data
        api_data = call_external_api("votars-mcp-Votars fetch recent transcripts")
        
        # Construct the result dictionary matching the expected output schema
        result = {
            "code": api_data["code"],
            "msg": api_data["msg"]
        }
        
        return result
        
    except Exception as e:
        # In case of any error during API call or processing, return error response
        return {
            "code": 500,
            "msg": f"Internal error occurred: {str(e)}"
        }