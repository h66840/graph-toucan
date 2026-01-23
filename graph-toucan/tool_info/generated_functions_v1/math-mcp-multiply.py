from typing import Dict, Any

def math_mcp_multiply(firstNumber: float, SecondNumber: float) -> Dict[str, Any]:
    """
    Multiplies two numbers together and returns the result.

    This function performs a simple multiplication of two input numbers.
    It validates the inputs to ensure they are numeric and returns their product.

    Args:
        firstNumber (float): The first number to multiply.
        SecondNumber (float): The second number to multiply.

    Returns:
        Dict[str, Any]: A dictionary containing the result of the multiplication.
            - result (float): The product of multiplying the two input numbers.

    Raises:
        TypeError: If either input is not a number.
    """
    # Input validation
    if not isinstance(firstNumber, (int, float)):
        raise TypeError("firstNumber must be a number")
    if not isinstance(SecondNumber, (int, float)):
        raise TypeError("SecondNumber must be a number")
    
    # Perform multiplication
    result = float(firstNumber * SecondNumber)
    
    # Return result in dictionary format
    return {"result": result}