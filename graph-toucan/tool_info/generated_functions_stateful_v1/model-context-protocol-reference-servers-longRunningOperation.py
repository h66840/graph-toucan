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


def model_context_protocol_reference_servers_longRunningOperation(duration: Optional[float] = None, steps: Optional[int] = None) -> Dict[str, Any]:
    """
    Demonstrates a long running operation with progress updates.
    
    This function simulates a long-running computational operation that can be customized
    by specifying the total duration and number of steps. It returns metadata about the
    completed operation including status, actual duration, and total steps executed.
    
    Args:
        duration (Optional[float]): Duration of the operation in seconds. If not provided,
                                   defaults to 5 seconds.
        steps (Optional[int]): Number of steps in the operation. If not provided,
                               defaults to 10 steps.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): Always "completed" for this simulation
            - duration_seconds (int): Actual duration of the operation in seconds (rounded down)
            - steps_count (int): Total number of steps executed
    
    Example:
        >>> result = model_context_protocol_reference_servers_longRunningOperation(duration=3.5, steps=5)
        >>> result['status']
        'completed'
        >>> result['duration_seconds']
        3
        >>> result['steps_count']
        5
    """
    # Set default values if parameters are not provided
    duration = duration if duration is not None else 5.0
    steps = steps if steps is not None else 10
    
    # Validate inputs
    if duration <= 0:
        raise ValueError("Duration must be a positive number")
    if steps <= 0:
        raise ValueError("Steps must be a positive integer")
    
    # Simulate a long-running operation with progress updates
    start_time = time.time()
    
    # Calculate sleep time per step
    step_duration = duration / steps
    
    # Execute each step
    for _ in range(steps):
        # Simulate work being done
        time.sleep(step_duration)
    
    # Calculate actual duration
    actual_duration = int(time.time() - start_time)
    
    # Return the result
    return {
        "status": "completed",
        "duration_seconds": actual_duration,
        "steps_count": steps
    }