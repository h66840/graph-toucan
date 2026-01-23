from typing import Dict, Any

def mcp_server_add(a: int, b: int) -> Dict[str, Any]:
    """
    Add two numbers and return the result.
    
    This function performs a simple arithmetic addition of two integers.
    
    Args:
        a (int): The first number to add
        b (int): The second number to add
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the addition
            - result (int): the sum of the two input numbers 'a' and 'b'
    
    Raises:
        TypeError: If either input is not an integer
    """
    # Input validation
    if not isinstance(a, int):
        raise TypeError(f"Expected 'a' to be an integer, got {type(a).__name__}")
    if not isinstance(b, int):
        raise TypeError(f"Expected 'b' to be an integer, got {type(b).__name__}")
    
    # Perform addition
    result = a + b
    
    # Return result in expected format
    return {
        "result": result
    }