from typing import Dict, Any

def calculator_mul(a: int, b: int) -> Dict[str, Any]:
    """
    Multiply two integers and return the result.
    
    This function performs a simple multiplication of two input integers.
    
    Args:
        a (int): The first integer to multiply
        b (int): The second integer to multiply
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the multiplication
                       with key 'result' and value as the product of a and b
    
    Raises:
        TypeError: If either input is not an integer
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