from typing import Dict, Any

def math_mcp_division(denominator: float, numerator: float) -> Dict[str, Any]:
    """
    Divides the first number by the second number.
    
    This function performs division of numerator by denominator and returns the result.
    It includes error handling for division by zero.
    
    Args:
        denominator (float): The number to divide by (denominator)
        numerator (float): The number being divided (numerator)
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the division as a float.
                       If division by zero is attempted, returns an error message.
    
    Raises:
        ValueError: If denominator is zero
    """
    if denominator == 0:
        raise ValueError("Division by zero is not allowed")
    
    result = numerator / denominator
    return {"result": result}