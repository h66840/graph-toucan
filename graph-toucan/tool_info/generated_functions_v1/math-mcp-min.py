from typing import List, Dict, Any

def math_mcp_min(numbers: List[float]) -> Dict[str, Any]:
    """
    Finds the minimum value from a list of numbers.
    
    Args:
        numbers (List[float]): Array of numbers to find the minimum of
        
    Returns:
        Dict[str, Any]: Dictionary containing the minimum value found in the input list
            - minimum (float): The smallest number in the input list
            
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
    
    # Find the minimum value
    minimum_value = min(numbers)
    
    return {
        "minimum": float(minimum_value)
    }