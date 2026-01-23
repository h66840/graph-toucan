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


def first_mcp_server_example_tool(message: str) -> Dict[str, str]:
    """
    An example tool for Cherry Studio that processes a message and returns a response.
    
    This function takes a message as input, processes it by prepending "Processed: ",
    and returns a dictionary containing the processed message and a result string.
    
    Args:
        message (str): A message to process. Must be a non-empty string.
    
    Returns:
        Dict[str, str]: A dictionary containing:
            - processed_message (str): The original message that was processed
            - result (str): The full response string indicating the message was processed
    
    Raises:
        ValueError: If the message is empty or not a string
    """
    # Input validation
    if not isinstance(message, str):
        raise ValueError("Message must be a string")
    if not message.strip():
        raise ValueError("Message cannot be empty or whitespace only")
    
    # Process the message
    processed_message = f"Processed: {message}"
    result = f"Message '{message}' was successfully processed by Cherry Studio"
    
    return {
        "processed_message": processed_message,
        "result": result
    }