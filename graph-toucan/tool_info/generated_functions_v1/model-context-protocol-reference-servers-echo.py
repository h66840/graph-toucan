from typing import Dict, Any

def model_context_protocol_reference_servers_echo(message: str) -> Dict[str, str]:
    """
    Echoes back the input message exactly as received.
    
    This function simulates a server that receives a message and returns it 
    with an "Echo: " prefix, then extracts the echoed message from the response.
    
    Args:
        message (str): The message to echo. Required.
        
    Returns:
        Dict[str, str]: A dictionary containing the echoed message.
            - echoed_message (str): The message that was echoed back by the server, 
              exactly as received in the response after the "Echo: " prefix.
              
    Raises:
        ValueError: If message is None or empty.
    """
    # Input validation
    if not message:
        raise ValueError("Message parameter is required and cannot be empty")
    
    # Simulate server response with "Echo: " prefix
    server_response = f"Echo: {message}"
    
    # Extract the echoed message (everything after "Echo: ")
    echoed_message = server_response[6:]  # Remove "Echo: " prefix
    
    return {
        "echoed_message": echoed_message
    }