from typing import Dict, Any

def advanced_calculator_server_radians_to_degrees(radians: float) -> Dict[str, Any]:
    """
    Convert an angle from radians to degrees.
    
    This function takes a numeric value in radians and converts it to degrees
    using the mathematical formula: degrees = radians * (180 / pi).
    
    Args:
        radians (float): The angle in radians to convert. Must be a number.
    
    Returns:
        Dict[str, Any]: A dictionary containing the converted angle in degrees.
                       The key is 'degrees' and the value is a float.
    
    Raises:
        TypeError: If the input is not a number.
        ValueError: If the input is None.
    """
    # Input validation
    if radians is None:
        raise ValueError("Radians value cannot be None")
    
    if not isinstance(radians, (int, float)):
        raise TypeError("Radians must be a number (int or float)")
    
    # Perform conversion from radians to degrees
    degrees = radians * (180.0 / 3.141592653589793)
    
    return {
        "degrees": float(degrees)
    }