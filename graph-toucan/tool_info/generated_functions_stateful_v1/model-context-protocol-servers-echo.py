from typing import Dict, Any

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


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