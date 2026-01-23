from typing import Dict, Any

def advanced_calculator_server_is_prime(n: int) -> Dict[str, Any]:
    """
    Check if a number is prime.
    
    A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.
    
    Args:
        n (int): The integer to check for primality.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result with the key 'is_prime' (bool).
    
    Raises:
        ValueError: If the input is not a positive integer greater than 0.
    """
    # Input validation
    if not isinstance(n, int):
        raise ValueError("Input must be an integer.")
    if n < 0:
        raise ValueError("Input must be a non-negative integer.")
    
    # Prime checking logic
    if n < 2:
        is_prime = False
    elif n == 2:
        is_prime = True
    elif n % 2 == 0:
        is_prime = False
    else:
        is_prime = True
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                is_prime = False
                break
    
    return {"is_prime": is_prime}