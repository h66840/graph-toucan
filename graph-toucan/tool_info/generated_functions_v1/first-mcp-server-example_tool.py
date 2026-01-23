from typing import Dict, Any

def first_mcp_server_example_tool(message: str) -> Dict[str, str]:
    """
    An example tool for Cherry Studio that processes a message and returns a response.
    
    This function takes a message as input, processes it by prepending "Processed: ",
    and returns a dictionary containing the processed message and a result string.
    
    Args:
        message (str): A message to process. Must be a non-empty string.
    
    Returns:
        Dict[str, str]: A dictionary containing:
            - processed_message (str): The original message that was processed
            - result (str): The full response string indicating the message was processed
    
    Raises:
        ValueError: If the message is empty or not a string
    """
    # Input validation
    if not isinstance(message, str):
        raise ValueError("Message must be a string")
    if not message.strip():
        raise ValueError("Message cannot be empty or whitespace only")
    
    # Process the message
    processed_message = f"Processed: {message}"
    result = f"Message '{message}' was successfully processed by Cherry Studio"
    
    return {
        "processed_message": processed_message,
        "result": result
    }