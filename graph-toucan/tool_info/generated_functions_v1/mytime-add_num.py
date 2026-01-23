def mytime_add_num(nums: list) -> dict:
    """
    Add a list of numbers.
    
    Args:
        nums (list): A list of numbers (int or float) to be summed.
        
    Returns:
        dict: A dictionary containing the sum of all numbers provided in the input list.
              - result (int): the sum of all numbers provided in the input list
    
    Raises:
        TypeError: If nums is not a list or contains non-numeric values.
        ValueError: If nums is empty.
    """
    # Input validation
    if not isinstance(nums, list):
        raise TypeError("Input 'nums' must be a list.")
    
    if len(nums) == 0:
        raise ValueError("Input 'nums' cannot be empty.")
    
    if not all(isinstance(n, (int, float)) for n in nums):
        raise TypeError("All elements in 'nums' must be numbers (int or float).")
    
    # Computation logic
    total = sum(nums)
    
    # Return result as per output schema
    return {"result": int(total)}