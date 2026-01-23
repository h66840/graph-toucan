from typing import Dict, Any

def math_mcp_round(number: float) -> Dict[str, Any]:
    """
    Rounds a number to the nearest integer.
    
    This function takes a numerical input and returns the value rounded 
    to the nearest integer using standard mathematical rounding rules.
    
    Args:
        number (float): The number to round. Must be a valid number.
    
    Returns:
        Dict[str, Any]: A dictionary containing the rounded result as an integer.
            - rounded_result (int): The number rounded to the nearest integer.
    
    Raises:
        ValueError: If the input is not a valid number.
    """
    # Input validation
    if not isinstance(number, (int, float)):
        raise ValueError("The 'number' parameter must be a valid number (int or float).")
    
    # Perform rounding to nearest integer
    rounded_result = round(number)
    
    # Return result in expected format
    return {
        "rounded_result": int(rounded_result)
    }