from typing import Dict, Any

def advanced_calculator_server_div(a: int, b: int) -> Dict[str, Any]:
    """
    Divide two numbers and return the floating-point result.
    
    This function performs division of two integers and returns the result as a float.
    It includes error handling for division by zero.
    
    Args:
        a (int): The dividend (numerator)
        b (int): The divisor (denominator)
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the division as a float
                       with key 'result'. If division by zero occurs, returns
                       result as None with an error message.
    
    Raises:
        ValueError: If the divisor (b) is zero
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    
    result = float(a) / float(b)
    
    return {
        "result": result
    }