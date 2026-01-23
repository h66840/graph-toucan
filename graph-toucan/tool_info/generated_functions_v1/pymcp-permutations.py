from typing import Dict, Any, Optional
import math

def pymcp_permutations(n: int, k: Optional[int] = None) -> Dict[str, Any]:
    """
    Calculate the number of permutations P(n,k) = n! / (n-k)! for given n and k.
    
    This function computes the number of ways to choose k items from n items 
    without repetition and with order (i.e., permutations).
    
    If k is not provided, it defaults to n (i.e., P(n,n) = n!).
    
    Args:
        n (int): The number of items to choose from (required).
        k (Optional[int]): The number of items to choose (optional, defaults to n).
    
    Returns:
        Dict[str, Any]: A dictionary containing the result field with the number of permutations.
                       - result (int): The number of permutations P(n,k).
    
    Raises:
        ValueError: If n is negative, or if k is negative, or if k > n.
        TypeError: If n or k are not integers.
    """
    # Input validation
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    
    if n < 0:
        raise ValueError("n must be non-negative")
    
    # Set default value for k
    if k is None:
        k = n
    else:
        if not isinstance(k, int):
            raise TypeError("k must be an integer")
        if k < 0:
            raise ValueError("k must be non-negative")
        if k > n:
            raise ValueError("k cannot be greater than n")
    
    # Calculate permutations: P(n,k) = n! / (n-k)!
    # Optimized calculation to avoid large factorials
    result = 1
    for i in range(n, n - k, -1):
        result *= i
    
    return {"result": result}