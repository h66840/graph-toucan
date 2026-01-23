from typing import Dict, Any

def smithery_hello_hello(name: str) -> Dict[str, str]:
    """
    Say hello to someone by generating a friendly greeting message.

    Args:
        name (str): The name of the person to greet. Must be a non-empty string.

    Returns:
        Dict[str, str]: A dictionary containing the greeting message addressed to the specified name.
            - greeting (str): A friendly greeting message.

    Raises:
        ValueError: If the name is empty or not provided.
    """
    if not name or not name.strip():
        raise ValueError("Name is required and cannot be empty or whitespace.")
    
    greeting_message = f"Hello, {name.strip()}! It's great to see you!"
    
    return {
        "greeting": greeting_message
    }