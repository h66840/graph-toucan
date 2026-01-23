from typing import Dict, Any, Optional
import math

def advanced_calculator_server_log(base: Optional[float] = None, x: float = 1.0) -> Dict[str, Any]:
    """
    Calculate logarithm of a number with optional base (default: natural log).
    
    Parameters:
        base (Optional[float]): The base of the logarithm. If None, natural logarithm (base e) is calculated.
        x (float): The number to calculate the logarithm of. Must be positive.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the logarithm calculation.
            - result (float): The calculated logarithm value of the input number x with respect to the specified base.
    
    Raises:
        ValueError: If x is less than or equal to 0, or if base is non-positive or equal to 1.
    """
    # Input validation
    if x <= 0:
        raise ValueError("The argument 'x' must be positive.")
    
    if base is not None:
        if base <= 0:
            raise ValueError("The base must be positive.")
        if base == 1:
            raise ValueError("The base cannot be 1.")
    
    try:
        if base is None:
            # Natural logarithm
            result = math.log(x)
        elif base == 10:
            # Common logarithm (base 10)
            result = math.log10(x)
        elif base == 2:
            # Binary logarithm (base 2)
            result = math.log2(x)
        else:
            # Logarithm with arbitrary base
            result = math.log(x) / math.log(base)
    except Exception as e:
        raise ValueError(f"An error occurred during logarithm calculation: {str(e)}")
    
    return {"result": result}