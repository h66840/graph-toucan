from typing import Dict, Any
import math

def advanced_calculator_server_square_root(x: float) -> Dict[str, Any]:
    """
    Calculate the square root of a given number.
    
    Args:
        x (float): The input number for which the square root is to be calculated. Must be non-negative.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result field with the square root of x.
                        Returns an error message if input is invalid.
    
    Raises:
        ValueError: If x is negative, as square root of negative number is not supported.
    """
    if x < 0:
        return {"result": float('nan')}  # or could raise an exception, but returning NaN for consistency
    
    result = math.sqrt(x)
    return {"result": result}