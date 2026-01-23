from typing import Dict, Any
import math

def math_mcp_floor(number: float) -> Dict[str, Any]:
    """
    Rounds a number down to the nearest integer.
    
    This function implements the floor operation, which returns the largest integer 
    less than or equal to the given number. It uses the mathematical floor function 
    from the standard library.
    
    Args:
        number (float): The number to round down. Must be a valid numeric value.
        
    Returns:
        Dict[str, Any]: A dictionary containing the result of the floor operation.
                       The result is an integer representing the largest integer 
                       less than or equal to the input number.
                       
    Raises:
        ValueError: If the input number is NaN or infinity.
    """
    # Input validation
    if math.isnan(number):
        raise ValueError("Input number cannot be NaN")
    if math.isinf(number):
        raise ValueError("Input number cannot be infinite")
    
    # Perform floor operation
    result = math.floor(number)
    
    return {
        "result": result
    }