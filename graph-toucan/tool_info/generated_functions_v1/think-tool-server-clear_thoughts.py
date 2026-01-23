from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - cleared_count (int): Number of thoughts cleared from the session
        - message (str): Human-readable confirmation message indicating how many thoughts were cleared
    """
    return {
        "cleared_count": 5,
        "message": "5 thoughts have been cleared from the session."
    }

def think_tool_server_clear_thoughts() -> Dict[str, Any]:
    """
    Clear all recorded thoughts from the current session.
    
    This function resets the thinking process by clearing all previously recorded thoughts.
    It communicates with an external service to perform the clearing operation and returns
    a confirmation of how many thoughts were cleared.
    
    Returns:
        Dict containing:
        - cleared_count (int): Number of thoughts cleared from the session
        - message (str): Human-readable confirmation message indicating how many thoughts were cleared
    """
    try:
        # Call external API to perform the action
        api_data = call_external_api("think-tool-server-clear_thoughts")
        
        # Construct result matching output schema
        result = {
            "cleared_count": api_data["cleared_count"],
            "message": api_data["message"]
        }
        
        return result
        
    except Exception as e:
        # Handle any potential errors during execution
        return {
            "cleared_count": 0,
            "message": f"Error occurred while clearing thoughts: {str(e)}"
        }