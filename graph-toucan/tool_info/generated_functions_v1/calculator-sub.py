from typing import Dict, Any

def calculator_sub(a: int, b: int) -> Dict[str, Any]:
    """
    Subtract two numbers (a - b).
    
    Args:
        a (int): The first number (minuend)
        b (int): The second number (subtrahend)
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the subtraction
            - result (int): The result of a - b
    
    Raises:
        TypeError: If either input is not an integer
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both arguments must be integers")
    
    result = a - b
    return {"result": result}