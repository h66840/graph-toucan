from typing import Dict, Any
import math

def advanced_calculator_server_cos(x: float) -> Dict[str, Any]:
    """
    Calculate the cosine of an angle given in radians.

    Parameters:
        x (float): The angle in radians for which to calculate the cosine.

    Returns:
        Dict[str, Any]: A dictionary containing the calculated cosine value.
            - cosine_value (float): The cosine of the input angle in radians.

    Raises:
        ValueError: If the input is not a valid number.
    """
    # Input validation
    if not isinstance(x, (int, float)):
        raise ValueError("Input x must be a number (int or float).")
    
    # Compute cosine using math.cos
    cosine_value = math.cos(x)
    
    # Return result as dictionary
    return {
        "cosine_value": float(cosine_value)
    }