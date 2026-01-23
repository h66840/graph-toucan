from typing import Dict, Any

def linkd_model_context_protocol_server_add_two_numbers(a: float, b: float) -> Dict[str, Any]:
    """
    Add two numbers together and return their sum along with a description.
    
    Args:
        a (float): First number to add
        b (float): Second number to add
    
    Returns:
        Dict with the following keys:
        - sum_result (int): The calculated sum of the two input numbers
        - description (str): A natural language statement describing the addition operation and its result
    
    Raises:
        TypeError: If either input is not a number
    """
    # Input validation
    if not isinstance(a, (int, float)):
        raise TypeError("Parameter 'a' must be a number")
    if not isinstance(b, (int, float)):
        raise TypeError("Parameter 'b' must be a number")
    
    # Perform addition
    sum_value = a + b
    sum_result = int(sum_value)  # Convert to int as per output schema
    
    # Create description
    description = f"The sum of {a} and {b} is {sum_result}"
    
    return {
        "sum_result": sum_result,
        "description": description
    }