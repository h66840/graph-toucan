from typing import Dict, Any

def advanced_calculator_server_gcd(a: int, b: int) -> Dict[str, Any]:
    """
    Calculate the greatest common divisor (GCD) of two integers using the Euclidean algorithm.
    
    Parameters:
        a (int): First integer
        b (int): Second integer
    
    Returns:
        Dict[str, Any]: A dictionary containing the GCD result with key 'gcd_result'
    
    Raises:
        ValueError: If either input is not an integer
    """
    # Input validation
    if not isinstance(a, int) or not isinstance(b, int):
        raise ValueError("Both inputs must be integers")
    
    # Handle edge case where both numbers are 0
    if a == 0 and b == 0:
        return {"gcd_result": 0}
    
    # Use Euclidean algorithm to find GCD
    def gcd(x: int, y: int) -> int:
        x, y = abs(x), abs(y)  # Work with absolute values
        while y:
            x, y = y, x % y
        return x
    
    result = gcd(a, b)
    
    return {"gcd_result": result}