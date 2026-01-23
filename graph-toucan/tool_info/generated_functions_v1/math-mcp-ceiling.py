from typing import Dict, Any
import math

def math_mcp_ceiling(number: float) -> Dict[str, Any]:
    """
    Rounds a number up to the nearest integer.
    
    This function implements the ceiling operation, which returns the smallest 
    integer greater than or equal to the given number. It uses pure computation 
    without any external dependencies beyond the standard library.
    
    Args:
        number (float): The number to round up. Must be a valid numeric value.
        
    Returns:
        Dict[str, Any]: A dictionary containing the result of the ceiling operation.
            - result (int): The smallest integer greater than or equal to the input number.
            
    Raises:
        ValueError: If the input is not a valid number (e.g., NaN or infinity).
    """
    # Input validation
    if not isinstance(number, (int, float)):
        raise ValueError("Input must be a number")
    
    if math.isinf(number) or math.isnan(number):
        raise ValueError("Input must be a finite number")
    
    # Perform ceiling operation
    result = math.ceil(number)
    
    return {"result": result}