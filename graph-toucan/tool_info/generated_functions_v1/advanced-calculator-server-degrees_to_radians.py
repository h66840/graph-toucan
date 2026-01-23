from typing import Dict, Any

def advanced_calculator_server_degrees_to_radians(degrees: float) -> Dict[str, Any]:
    """
    Convert degrees to radians.
    
    This function takes an angle in degrees and converts it to radians using the formula:
    radians = degrees * (pi / 180)
    
    Args:
        degrees (float): The angle in degrees to be converted. Must be a number.
    
    Returns:
        Dict[str, Any]: A dictionary containing the converted angle in radians.
            - radians (float): The converted angle value in radians from the input degrees.
    
    Raises:
        TypeError: If the input is not a number.
        ValueError: If the input is None.
    """
    # Input validation
    if degrees is None:
        raise ValueError("Degrees input cannot be None")
    
    if not isinstance(degrees, (int, float)):
        raise TypeError("Degrees must be a number (int or float)")
    
    # Perform conversion from degrees to radians
    radians = degrees * (3.141592653589793 / 180.0)
    
    return {
        "radians": float(radians)
    }