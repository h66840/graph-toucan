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


def think_mcp_server_think(thought: str) -> Dict[str, str]:
    """
    Use the tool to think about something. It will not obtain new information or change the database,
    but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.
    
    Args:
        thought (str): A thought to think about. This parameter is required.
    
    Returns:
        Dict[str, str]: A dictionary containing a reflection_status indicating the completion 
                        or quality of the thought process.
                        
    Raises:
        ValueError: If the 'thought' parameter is empty or not a string.
    """
    # Input validation
    if not isinstance(thought, str):
        raise ValueError("The 'thought' parameter must be a string.")
    if not thought.strip():
        raise ValueError("The 'thought' parameter cannot be empty or whitespace only.")
    
    # Simulate reflection process based on thought content
    # More complex thoughts get higher quality reflection status
    thought_words = thought.strip().split()
    if len(thought_words) >= 10:
        reflection_status = "Excellent reflection."
    elif len(thought_words) >= 5:
        reflection_status = "Great thinking."
    else:
        reflection_status = "Thought processed."
    
    return {
        "reflection_status": reflection_status
    }