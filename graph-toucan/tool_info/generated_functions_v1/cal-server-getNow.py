from typing import Dict, Any
import time

def cal_server_getNow() -> Dict[str, Any]:
    """
    Get the current timestamp in Unix milliseconds since epoch.
    
    This function returns the current time as a Unix timestamp measured in 
    milliseconds since January 1, 1970, 00:00:00 UTC.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - current_timestamp (int): The current Unix timestamp in milliseconds
    """
    try:
        # Get current time in seconds since epoch and convert to milliseconds
        current_timestamp = int(time.time() * 1000)
        
        return {
            "current_timestamp": current_timestamp
        }
    except Exception as e:
        # In case of any unexpected error, raise with meaningful message
        raise RuntimeError(f"Failed to get current timestamp: {str(e)}")