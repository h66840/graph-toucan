def mcp服务_add(a: int, b: int) -> dict:
    """
    Add two numbers.

    Parameters:
        a (int): The first integer to add.
        b (int): The second integer to add.

    Returns:
        dict: A dictionary containing the result of the addition.
              - result (int): The sum of a and b.
    
    Raises:
        TypeError: If either a or b is not an integer.
    """
    # Input validation
    if not isinstance(a, int):
        raise TypeError("Parameter 'a' must be an integer.")
    if not isinstance(b, int):
        raise TypeError("Parameter 'b' must be an integer.")
    
    # Computation logic
    result = a + b
    
    # Return result in expected output format
    return {"result": result}