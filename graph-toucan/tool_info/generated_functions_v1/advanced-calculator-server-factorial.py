from typing import Dict, Any

def advanced_calculator_server_factorial(n: int) -> Dict[str, Any]:
    """
    Calculate the factorial of a non-negative integer.
    
    Args:
        n (int): A non-negative integer for which to compute the factorial.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of n!.
            - result (int): The factorial of the input number n (i.e., n!).
    
    Raises:
        ValueError: If n is negative.
        TypeError: If n is not an integer.
    """
    # Input validation
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    
    # Compute factorial
    result = 1
    for i in range(1, n + 1):
        result *= i
    
    return {"result": result}