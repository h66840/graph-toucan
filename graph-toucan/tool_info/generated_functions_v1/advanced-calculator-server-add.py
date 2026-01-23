from typing import Dict, Any

def advanced_calculator_server_add(a: int, b: int) -> Dict[str, Any]:
    """
    Add two numbers and return their sum.
    
    This function performs a simple addition operation on two integers.
    
    Args:
        a (int): The first integer to add
        b (int): The second integer to add
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the addition
            - result (int): the sum of the two input numbers a and b
    
    Raises:
        TypeError: If either a or b is not an integer
    """
    # Input validation
    if not isinstance(a, int):
        raise TypeError(f"Parameter 'a' must be an integer, got {type(a).__name__}")
    if not isinstance(b, int):
        raise TypeError(f"Parameter 'b' must be an integer, got {type(b).__name__}")
    
    # Perform addition
    result = a + b
    
    # Return result in expected format
    return {"result": result}