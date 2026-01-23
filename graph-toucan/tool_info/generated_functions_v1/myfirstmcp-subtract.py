from typing import Dict, Any

def myfirstmcp_subtract(a: int, b: int) -> Dict[str, Any]:
    """
    Subtract two numbers.

    This function takes two integers and returns their difference (a - b).
    
    Args:
        a (int): The first number
        b (int): The second number
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the subtraction
            - result (int): The difference between the two input numbers (a - b)
    
    Raises:
        TypeError: If either a or b is not an integer
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both arguments must be integers")
    
    result = a - b
    return {"result": result}