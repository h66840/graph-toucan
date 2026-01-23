from typing import List, Dict, Any

def math_mcp_max(numbers: List[float]) -> Dict[str, float]:
    """
    Finds the maximum value from a list of numbers.
    
    Args:
        numbers (List[float]): Array of numbers to find the maximum of
        
    Returns:
        Dict[str, float]: A dictionary containing the maximum value found in the input list
                         with key 'maximum'
                         
    Raises:
        ValueError: If the input list is empty
        TypeError: If the input is not a list or contains non-numeric values
    """
    # Input validation
    if not isinstance(numbers, list):
        raise TypeError("Input 'numbers' must be a list")
    
    if len(numbers) == 0:
        raise ValueError("Input list 'numbers' cannot be empty")
    
    # Validate that all elements are numbers
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise TypeError(f"All elements in 'numbers' must be numeric, got {type(num)}")
    
    # Find the maximum value
    maximum_value = max(numbers)
    
    return {"maximum": float(maximum_value)}