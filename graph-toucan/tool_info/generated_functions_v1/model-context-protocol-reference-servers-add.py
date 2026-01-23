from typing import Dict, Any

def model_context_protocol_reference_servers_add(a: float, b: float) -> Dict[str, Any]:
    """
    Adds two numbers and returns the result.
    
    This function performs a simple arithmetic addition of two input numbers.
    
    Args:
        a (float): First number to add. Must be a valid number.
        b (float): Second number to add. Must be a valid number.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the addition.
            - result (int): The sum of a and b, truncated to an integer.
    
    Raises:
        TypeError: If either a or b is not a number.
    """
    # Input validation
    if not isinstance(a, (int, float)):
        raise TypeError("Parameter 'a' must be a number")
    if not isinstance(b, (int, float)):
        raise TypeError("Parameter 'b' must be a number")
    
    # Perform addition and convert to integer (truncating any decimal part)
    result = int(a + b)
    
    return {"result": result}