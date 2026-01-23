from typing import Dict, Any

def mcp_server_multiply(a: int, b: int) -> Dict[str, Any]:
    """
    Multiply two integers and return the result.

    This function performs a pure computation by multiplying two given integers.
    It does not make any external API calls or network requests.

    Args:
        a (int): The first integer to multiply.
        b (int): The second integer to multiply.

    Returns:
        Dict[str, Any]: A dictionary containing the result of the multiplication
                       under the key 'result' as an integer.

    Raises:
        TypeError: If either of the inputs is not an integer.
    """
    # Input validation
    if not isinstance(a, int):
        raise TypeError(f"Expected 'a' to be an integer, got {type(a).__name__}")
    if not isinstance(b, int):
        raise TypeError(f"Expected 'b' to be an integer, got {type(b).__name__}")

    # Perform multiplication
    result = a * b

    # Return result in expected format
    return {"result": result}