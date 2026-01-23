from typing import Dict, Any

def add_test_add_a_and_b(a: float, b: float) -> Dict[str, Any]:
    """
    Add two numbers together.
    
    This function takes two numerical inputs and returns their sum in a dictionary
    with the key 'result'. It performs basic input validation to ensure that both
    inputs are numbers.
    
    Args:
        a (float): The first number to add (required).
        b (float): The second number to add (required).
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the addition.
                       The result is an integer if both inputs are integers,
                       otherwise a float.
    
    Raises:
        TypeError: If either a or b is not a number.
    """
    # Input validation
    if not isinstance(a, (int, float)):
        raise TypeError(f"Parameter 'a' must be a number, got {type(a).__name__}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Parameter 'b' must be a number, got {type(b).__name__}")
    
    # Perform addition
    result = a + b
    
    # Return result as integer if both inputs are integers, otherwise return float
    if isinstance(a, int) and isinstance(b, int):
        return {"result": int(result)}
    else:
        return {"result": result}
        