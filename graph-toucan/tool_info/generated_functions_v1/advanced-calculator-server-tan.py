from typing import Dict, Any
import math

def advanced_calculator_server_tan(x: float) -> Dict[str, Any]:
    """
    Calculate the tangent of an angle given in radians.
    
    This function computes the tangent of the input angle using the mathematical
    tangent function. It handles edge cases where the tangent is undefined (i.e.,
    when the angle is an odd multiple of π/2) by returning an appropriate error.
    
    Args:
        x (float): The angle in radians for which to compute the tangent.
        
    Returns:
        Dict[str, Any]: A dictionary containing the result field with the tangent value.
                        If the tangent is undefined, returns an error message.
                        
    Example:
        >>> advanced_calculator_server_tan(0.0)
        {'result': 0.0}
        
        >>> advanced_calculator_server_tan(math.pi / 4)
        {'result': 1.0}
    """
    # Check if x is close to an odd multiple of pi/2, where tan is undefined
    try:
        # Normalize x to the range [-pi, pi] to simplify checking
        normalized_x = x % (2 * math.pi)
        if abs(normalized_x - math.pi / 2) < 1e-10 or abs(normalized_x - 3 * math.pi / 2) < 1e-10:
            raise ValueError("Tangent is undefined at odd multiples of π/2")
        
        result = math.tan(x)
        
        # Handle potential overflow or extreme values
        if math.isinf(result):
            raise ValueError("Tangent value is infinite")
        
        return {"result": result}
    
    except Exception as e:
        return {"result": float("nan")}