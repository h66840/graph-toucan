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


def example_mcp_server_hello(name: str) -> Dict[str, str]:
    """
    Say hello to someone by generating a greeting message.
    
    Args:
        name (str): The name of the person to greet. Must be a non-empty string.
    
    Returns:
        Dict[str, str]: A dictionary containing the generated greeting message.
            - greeting (str): The salutation message including the provided name.
    
    Raises:
        ValueError: If the name is empty or not a string.
    """
    # Input validation
    if not isinstance(name, str):
        raise ValueError("Name must be a string.")
    if not name.strip():
        raise ValueError("Name cannot be empty or whitespace.")
    
    # Generate greeting using pure computation
    greeting_message = f"Hello, {name.strip()}!"
    
    return {
        "greeting": greeting_message
    }