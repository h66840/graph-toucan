from typing import Dict, Any

def math_server_add(a: int, b: int) -> Dict[str, Any]:
    """
    Add two integers and return their sum in a dictionary.
    
    This function performs pure computation by adding two integers.
    No external API calls are made. The result is returned as a dictionary
    with a single key 'result' containing the sum of the inputs.
    
    Args:
        a (int): First integer to add
        b (int): Second integer to add
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the addition
                       with key 'result' and value as the sum (int)
    
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
    return {"result": result}