from typing import Dict, Tuple
import cmath

def advanced_calculator_server_quadratic_roots(a: float, b: float, c: float) -> Dict[str, complex]:
    """
    Solve quadratic equation ax² + bx + c = 0 and return the roots.
    
    The function calculates the roots using the quadratic formula:
    x = (-b ± sqrt(b² - 4ac)) / (2a)
    
    Handles both real and complex roots based on the discriminant.
    
    Args:
        a (float): Coefficient of x² (must not be zero)
        b (float): Coefficient of x
        c (float): Constant term
    
    Returns:
        Dict[str, complex]: A dictionary containing the two roots:
            - root1 (complex): The first root of the quadratic equation
            - root2 (complex): The second root of the quadratic equation
    
    Raises:
        ValueError: If 'a' is zero (not a quadratic equation)
    """
    # Input validation
    if a == 0:
        raise ValueError("Coefficient 'a' must not be zero for a quadratic equation")
    
    # Calculate discriminant
    discriminant = b**2 - 4*a*c
    
    # Calculate roots using quadratic formula
    if discriminant >= 0:
        # Real roots
        sqrt_discriminant = discriminant ** 0.5
        root1 = (-b + sqrt_discriminant) / (2*a)
        root2 = (-b - sqrt_discriminant) / (2*a)
    else:
        # Complex roots
        sqrt_discriminant = cmath.sqrt(discriminant)
        root1 = (-b + sqrt_discriminant) / (2*a)
        root2 = (-b - sqrt_discriminant) / (2*a)
    
    return {
        "root1": root1,
        "root2": root2
    }