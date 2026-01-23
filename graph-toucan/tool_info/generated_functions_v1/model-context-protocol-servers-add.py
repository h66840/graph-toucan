from typing import Dict, Any

def model_context_protocol_servers_add(a: float, b: float) -> Dict[str, Any]:
    """
    Adds two numbers and returns the result.

    This function performs a simple arithmetic addition of two numbers provided as input.
    It validates that both inputs are numeric and returns their sum as an integer.

    Args:
        a (float): First number, required.
        b (float): Second number, required.

    Returns:
        Dict[str, Any]: A dictionary containing the result of the addition with key 'result' as an integer.
                        Example: {"result": 5}

    Raises:
        TypeError: If either input is not a number.
    """
    # Input validation
    if not isinstance(a, (int, float)):
        raise TypeError("Parameter 'a' must be a number.")
    if not isinstance(b, (int, float)):
        raise TypeError("Parameter 'b' must be a number.")

    # Perform addition and return result as integer
    result = int(a + b)
    return {"result": result}