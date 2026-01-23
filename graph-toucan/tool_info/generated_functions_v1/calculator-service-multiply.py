from typing import Dict, Any

def calculator_service_multiply(a: float, b: float) -> Dict[str, Any]:
    """
    Multiplies two numbers together.
    
    Args:
        a (float): The first number to multiply.
        b (float): The second number to multiply.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the multiplication.
            - result (float): The product of multiplying a and b.
    
    Raises:
        TypeError: If either a or b is not a number.
    """
    # Input validation
    if not isinstance(a, (int, float)):
        raise TypeError("Parameter 'a' must be a number.")
    if not isinstance(b, (int, float)):
        raise TypeError("Parameter 'b' must be a number.")
    
    # Perform multiplication
    result = float(a * b)
    
    return {"result": result}