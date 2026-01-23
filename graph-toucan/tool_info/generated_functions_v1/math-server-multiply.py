from typing import Dict, Any

def math_server_multiply(a: int, b: int) -> Dict[str, Any]:
    """
    Multiply two integers and return their product.
    
    This function performs pure computation by multiplying two given integers.
    It validates the inputs to ensure they are integers before performing multiplication.
    
    Args:
        a (int): The first integer to multiply
        b (int): The second integer to multiply
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the multiplication
                       with key 'result' and value as the product of a and b
    
    Raises:
        TypeError: If either a or b is not an integer
    """
    # Input validation
    if not isinstance(a, int):
        raise TypeError(f"Parameter 'a' must be an integer, got {type(a).__name__}")
    if not isinstance(b, int):
        raise TypeError(f"Parameter 'b' must be an integer, got {type(b).__name__}")
    
    # Perform multiplication
    result = a * b
    
    # Return result in expected format
    return {"result": result}