from typing import Dict, Any


def mcp_test_server_add(a: int, b: int) -> Dict[str, Any]:
    """
    Add two numbers and return the result.

    This function performs a simple arithmetic addition of two integers.
    
    Args:
        a (int): The first integer to add.
        b (int): The second integer to add.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the addition.
            - result (int): The sum of a and b.
    
    Raises:
        TypeError: If either a or b is not an integer.
    """
    # Input validation
    if not isinstance(a, int):
        raise TypeError(f"Expected 'a' to be an integer, got {type(a).__name__}")
    if not isinstance(b, int):
        raise TypeError(f"Expected 'b' to be an integer, got {type(b).__name__}")
    
    # Perform addition
    result = a + b
    
    return {"result": result}