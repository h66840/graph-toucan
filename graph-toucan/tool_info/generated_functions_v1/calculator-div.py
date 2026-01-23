from typing import Dict, Any

def calculator_div(a: int, b: int) -> Dict[str, Any]:
    """
    Divide two numbers using integer division and return the result.
    
    This function performs integer division of a by b, returning the quotient
    without the remainder. It includes error handling for division by zero.
    
    Args:
        a (int): The dividend (numerator)
        b (int): The divisor (denominator)
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of integer division
                       with key 'result' and integer value
    
    Raises:
        ValueError: If the divisor (b) is zero
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    
    result = a // b
    return {"result": result}