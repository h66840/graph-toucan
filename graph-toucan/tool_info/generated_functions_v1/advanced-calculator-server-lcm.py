from typing import Dict, Any

def advanced_calculator_server_lcm(a: int, b: int) -> Dict[str, Any]:
    """
    Calculate the least common multiple (LCM) of two integers.
    
    This function computes the LCM using the formula: LCM(a, b) = |a * b| / GCD(a, b)
    
    Args:
        a (int): First integer
        b (int): Second integer
    
    Returns:
        Dict[str, Any]: Dictionary containing the result field with the LCM value
    
    Raises:
        ValueError: If either input is zero (LCM is undefined for zero)
    """
    # Input validation
    if a == 0 or b == 0:
        raise ValueError("LCM is undefined for zero values")
    
    # Helper function to calculate GCD using Euclidean algorithm
    def gcd(x: int, y: int) -> int:
        x, y = abs(x), abs(y)
        while y:
            x, y = y, x % y
        return x
    
    # Calculate LCM using the formula: LCM(a, b) = |a * b| / GCD(a, b)
    gcd_value = gcd(a, b)
    lcm_value = abs(a * b) // gcd_value
    
    return {"result": lcm_value}