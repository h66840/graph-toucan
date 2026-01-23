from typing import Dict, Any

def model_context_protocol_servers_echo(message: str) -> Dict[str, str]:
    """
    Echoes back the input message with the prefix "Echo: " removed.
    
    This function performs a pure computation by processing the input string
    and returning a dictionary containing the echoed message after stripping
    the "Echo: " prefix if present.
    
    Args:
        message (str): The message to echo. Expected to be a string, potentially prefixed with "Echo: ".
    
    Returns:
        Dict[str, str]: A dictionary containing the key 'echoed_message' with the original content
                        of the message after removing the "Echo: " prefix.
    
    Raises:
        ValueError: If the message is None or not a string.
    """
    if message is None:
        raise ValueError("Message cannot be None.")
    
    if not isinstance(message, str):
        raise ValueError("Message must be a string.")
    
    # Remove the prefix "Echo: " if present
    prefix = "Echo: "
    if message.startswith(prefix):
        echoed_message = message[len(prefix):]
    else:
        echoed_message = message
    
    return {
        "echoed_message": echoed_message
    }