from typing import Dict, Any
import math

def advanced_calculator_server_sin(x: float) -> Dict[str, Any]:
    """
    Calculate the sine of an angle given in radians.

    This function computes the sine value of the input angle using the standard
    mathematical sine function from the math module.

    Args:
        x (float): The angle in radians for which to compute the sine value.

    Returns:
        Dict[str, Any]: A dictionary containing the result field with the sine value.
            - result (float): The sine value of the input angle in radians.

    Raises:
        ValueError: If the input is not a valid number.
    """
    # Input validation
    if not isinstance(x, (int, float)):
        raise ValueError("Input x must be a number (int or float).")
    
    try:
        result = math.sin(x)
        return {"result": result}
    except Exception as e:
        raise ValueError(f"An error occurred during sine calculation: {str(e)}")