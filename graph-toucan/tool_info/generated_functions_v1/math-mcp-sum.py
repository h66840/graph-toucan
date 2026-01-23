from typing import Dict, List, Any

def math_mcp_sum(numbers: List[float]) -> Dict[str, Any]:
    """
    Adds any number of numbers together.
    
    This function takes a list of numbers and returns their sum.
    
    Args:
        numbers (List[float]): Array of numbers to sum. Must be provided.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result field with the sum of all input numbers.
                       - result (float): The sum of all input numbers.
    
    Raises:
        ValueError: If the input is not a list or contains non-numeric values.
    """
    if not isinstance(numbers, List):
        raise ValueError("Input 'numbers' must be a list.")
    
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise ValueError("All elements in 'numbers' must be numeric (int or float).")
    
    result = sum(numbers)
    
    return {"result": float(result)}