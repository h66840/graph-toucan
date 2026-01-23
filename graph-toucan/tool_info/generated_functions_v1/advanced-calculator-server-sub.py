from typing import Dict, Any

def advanced_calculator_server_sub(a: int, b: int) -> Dict[str, Any]:
    """
    Subtract two integers: a - b.

    This function performs a simple arithmetic subtraction of two integers.
    
    Args:
        a (int): The minuend (the number from which another number is to be subtracted).
        b (int): The subtrahend (the number to be subtracted from the minuend).

    Returns:
        Dict[str, Any]: A dictionary containing the result of the subtraction.
            - result (int): The result of a - b.
    
    Raises:
        TypeError: If either input is not an integer.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both arguments must be integers.")
    
    result = a - b
    return {"result": result}