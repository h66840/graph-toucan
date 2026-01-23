from typing import Dict, Any, Optional
import time

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


def model_context_protocol_servers_longRunningOperation(duration: Optional[float] = None, steps: Optional[int] = None) -> Dict[str, Any]:
    """
    Demonstrates a long running operation with progress updates.
    
    This function simulates a long-running computational operation by performing
    a loop for the specified number of steps, with artificial delays based on the
    duration parameter. It returns a summary of the completed operation.
    
    Args:
        duration (Optional[float]): Duration of the operation in seconds. Defaults to 10 seconds if not provided.
        steps (Optional[int]): Number of steps in the operation. Defaults to 10 steps if not provided.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): Status of the operation, always "completed"
            - duration_seconds (int): Duration of the long-running operation in seconds
            - steps (int): Total number of steps executed in the operation
            - message (str): Human-readable summary of operation completion
    
    Raises:
        ValueError: If duration is negative or steps is non-positive
    """
    # Set default values
    if duration is None:
        duration = 10.0
    if steps is None:
        steps = 10
    
    # Validate inputs
    if duration < 0:
        raise ValueError("Duration must be non-negative")
    if steps <= 0:
        raise ValueError("Steps must be positive")
    
    # Ensure steps is an integer
    steps = int(steps)
    
    # Simulate work being done
    step_delay = duration / steps
    for _ in range(steps):
        time.sleep(step_delay)  # Simulate work
    
    # Construct result
    result = {
        "status": "completed",
        "duration_seconds": int(duration),
        "steps": steps,
        "message": f"Operation completed successfully with {steps} steps over {int(duration)} seconds"
    }
    
    return result