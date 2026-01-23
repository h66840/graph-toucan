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


def smithery_hello_hello(name: str) -> Dict[str, str]:
    """
    Say hello to someone by generating a friendly greeting message.

    Args:
        name (str): The name of the person to greet. Must be a non-empty string.

    Returns:
        Dict[str, str]: A dictionary containing the greeting message addressed to the specified name.
            - greeting (str): A friendly greeting message.

    Raises:
        ValueError: If the name is empty or not provided.
    """
    if not name or not name.strip():
        raise ValueError("Name is required and cannot be empty or whitespace.")
    
    greeting_message = f"Hello, {name.strip()}! It's great to see you!"
    
    return {
        "greeting": greeting_message
    }