from typing import Dict, Any

def advanced_calculator_server_power(base: float, exponent: float) -> Dict[str, Any]:
    """
    Raise a number to a power.
    
    This function computes the result of raising the base to the given exponent (base^exponent).
    
    Args:
        base (float): The base number to be raised to a power.
        exponent (float): The exponent to which the base is raised.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the computation.
            - result (float): The result of base^exponent.
    
    Raises:
        ValueError: If the result is not a finite number (e.g., overflow or invalid operation).
    """
    # Perform the power operation
    result = pow(base, exponent)
    
    # Validate the result
    if not isinstance(result, (int, float)) or not (result == result):  # Check for NaN
        raise ValueError(f"Invalid result: {result} (base={base}, exponent={exponent})")
    
    if abs(result) == float('inf'):
        raise ValueError(f"Result overflow: {result} (base={base}, exponent={exponent})")
    
    return {"result": float(result)}