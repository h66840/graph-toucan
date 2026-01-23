from typing import List, Dict, Any

def math_mcp_median(numbers: List[float]) -> Dict[str, float]:
    """
    Calculates the median of a list of numbers.
    
    The median is the middle value in a sorted list of numbers.
    If the list has an even number of elements, the median is the average of the two middle numbers.
    
    Args:
        numbers (List[float]): Array of numbers to find the median of. Must be non-empty.
    
    Returns:
        Dict[str, float]: A dictionary containing the median value calculated from the input list.
                         Keys: 'median' -> the median value (float)
    
    Raises:
        ValueError: If the input list is empty.
        TypeError: If the input is not a list or contains non-numeric values.
    """
    # Input validation
    if not isinstance(numbers, List):
        raise TypeError("Input 'numbers' must be a list.")
    
    if len(numbers) == 0:
        raise ValueError("Input list 'numbers' must not be empty.")
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise TypeError("All elements in 'numbers' must be numeric (int or float).")
    
    # Sort the list to find median
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    
    # Calculate median
    if n % 2 == 1:
        # Odd number of elements: median is the middle element
        median_value = float(sorted_numbers[n // 2])
    else:
        # Even number of elements: median is the average of the two middle elements
        mid1 = sorted_numbers[n // 2 - 1]
        mid2 = sorted_numbers[n // 2]
        median_value = float((mid1 + mid2) / 2.0)
    
    return {"median": median_value}