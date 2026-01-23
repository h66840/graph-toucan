from typing import Dict, Any

def calculator_add(a: int, b: int) -> Dict[str, Any]:
    """
    Add two numbers and return the result.
    
    This function performs a simple addition of two integers and returns
    a dictionary containing the result.
    
    Args:
        a (int): The first number to add
        b (int): The second number to add
    
    Returns:
        Dict[str, int]: A dictionary with a single key 'result' containing the sum of a and b
    
    Raises:
        TypeError: If either a or b is not an integer
    """
    # Input validation
    if not isinstance(a, int):
        raise TypeError(f"Expected 'a' to be an integer, got {type(a).__name__}")
    if not isinstance(b, int):
        raise TypeError(f"Expected 'b' to be an integer, got {type(b).__name__}")
    
    # Perform addition
    result = a + b
    
    # Return result in expected format
    return {"result": result}