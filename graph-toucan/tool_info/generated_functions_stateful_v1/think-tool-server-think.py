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


def think_tool_server_think(thought: str) -> Dict[str, Any]:
    """
    Use the tool to think about something. It will not obtain new information or change the database,
    but just append the thought to the log. Use it when complex reasoning or some cache memory is needed.
    
    Args:
        thought (str): A thought to think about. This is required input representing the idea or reasoning to be recorded.
    
    Returns:
        Dict[str, Any]: A dictionary containing the structured natural language text capturing the assistant's reasoning,
                        analysis framework, or organized thoughts on a given topic.
                        - thought_log (str): The formatted log entry containing the timestamped thought.
    """
    # Input validation
    if not isinstance(thought, str):
        raise TypeError("The 'thought' parameter must be a string.")
    if not thought.strip():
        raise ValueError("The 'thought' parameter cannot be empty or whitespace only.")
    
    # Generate a simple structured thought log (pure computation, no external calls)
    thought_log = f"[THOUGHT LOG] Analyzing: {thought.strip()}. This reasoning is internally processed and stored for continuity."

    return {
        "thought_log": thought_log
    }