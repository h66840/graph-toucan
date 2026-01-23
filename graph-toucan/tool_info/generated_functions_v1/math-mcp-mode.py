from typing import Dict, List, Any
from collections import Counter

def math_mcp_mode(numbers: List[int]) -> Dict[str, Any]:
    """
    Finds the most common number(s) in a list of numbers (mode) and their occurrence count.
    
    Args:
        numbers (List[int]): Array of numbers to find the mode of
        
    Returns:
        Dict[str, Any]: Dictionary containing:
            - mode_values (List[int]): list of numbers that appear most frequently
            - occurrence_count (int): number of times the mode values appear in the input list
            
    Raises:
        ValueError: If the input list is empty
    """
    if not numbers:
        raise ValueError("Input list cannot be empty")
    
    # Count frequency of each number
    counter = Counter(numbers)
    
    # Find the maximum occurrence count
    max_count = counter.most_common(1)[0][1]
    
    # Get all numbers that have the maximum count (mode values)
    mode_values = [num for num, count in counter.items() if count == max_count]
    
    return {
        "mode_values": mode_values,
        "occurrence_count": max_count
    }