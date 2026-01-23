from typing import Dict, Any

def math_operations_server_add(a: int, b: int) -> Dict[str, Any]:
    """
    Adds two numbers and returns their sum.
    
    This function performs a simple arithmetic addition of two integers.
    
    Args:
        a (int): First number, required.
        b (int): Second number, required.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the addition.
            - result (int): The sum of the two input numbers a and b.
    
    Raises:
        TypeError: If either a or b is not an integer.
    """
    # Input validation
    if not isinstance(a, int):
        raise TypeError("Parameter 'a' must be an integer.")
    if not isinstance(b, int):
        raise TypeError("Parameter 'b' must be an integer.")
    
    # Perform addition
    result = a + b
    
    # Return result in dictionary format
    return {"result": result}