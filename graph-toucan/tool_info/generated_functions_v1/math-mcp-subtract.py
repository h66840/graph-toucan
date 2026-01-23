from typing import Dict, Any

def math_mcp_subtract(minuend: float, subtrahend: float) -> Dict[str, Any]:
    """
    Subtracts the second number from the first number.

    This function performs a simple arithmetic subtraction operation where the subtrahend
    is subtracted from the minuend. It returns the result as a floating-point number
    wrapped in a dictionary under the key 'result'.

    Args:
        minuend (float): The number to subtract from (minuend).
        subtrahend (float): The number being subtracted (subtrahend).

    Returns:
        Dict[str, Any]: A dictionary containing the result of the subtraction.
                        The result is stored under the key 'result' as a float.

    Raises:
        TypeError: If either minuend or subtrahend is not a number.
    """
    # Input validation
    if not isinstance(minuend, (int, float)):
        raise TypeError("minuend must be a number")
    if not isinstance(subtrahend, (int, float)):
        raise TypeError("subtrahend must be a number")
    
    # Perform subtraction
    result = float(minuend - subtrahend)
    
    # Return result in expected format
    return {"result": result}