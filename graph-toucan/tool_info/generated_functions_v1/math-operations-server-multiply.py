from typing import Dict, Any

def math_operations_server_multiply(a: int, b: int) -> Dict[str, Any]:
    """
    Multiplies two numbers and returns the result.
    
    Args:
        a (int): First number to multiply
        b (int): Second number to multiply
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the multiplication
            - result (int): The product of a and b
    
    Raises:
        TypeError: If either a or b is not an integer
    """
    # Input validation
    if not isinstance(a, int):
        raise TypeError(f"Expected 'a' to be an integer, got {type(a).__name__}")
    if not isinstance(b, int):
        raise TypeError(f"Expected 'b' to be an integer, got {type(b).__name__}")
    
    # Perform multiplication
    result = a * b
    
    # Return result in dictionary format
    return {
        "result": result
    }