from typing import Dict, Any

def math_mcp_add(firstNumber: float, secondNumber: float) -> Dict[str, Any]:
    """
    Adds two numbers together and returns the result as a floating-point number.
    
    This function performs a simple arithmetic addition of two input numbers.
    It validates the inputs to ensure they are numeric and returns their sum.
    
    Args:
        firstNumber (float): The first addend. Must be a number.
        secondNumber (float): The second addend. Must be a number.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the addition
                       under the key 'result' as a float.
    
    Raises:
        TypeError: If either input is not a number.
    """
    # Input validation
    if not isinstance(firstNumber, (int, float)):
        raise TypeError("firstNumber must be a number")
    if not isinstance(secondNumber, (int, float)):
        raise TypeError("secondNumber must be a number")
    
    # Perform addition
    result = float(firstNumber + secondNumber)
    
    return {"result": result}