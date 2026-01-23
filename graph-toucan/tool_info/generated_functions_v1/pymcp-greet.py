from typing import Dict, Any, Optional
from datetime import datetime

def pymcp_greet(name: Optional[str] = None) -> Dict[str, Any]:
    """
    Greet the caller with a quintessential Hello World message.
    
    Args:
        name (Optional[str]): The optional name to be greeted. If not provided, defaults to "World".
    
    Returns:
        Dict[str, Any]: A dictionary containing the following fields:
            - greeting (str): The full greeting message including the name and welcome text.
            - recipient (str): The name of the person being greeted, extracted from the greeting.
            - server_message (str): The welcome message indicating the server type and version.
            - server_version (str): The version of the pymcp server (e.g., '0.1.4').
            - timestamp_utc (str): The current date and time in UTC formatted as an ISO 8601 string.
    """
    # Default values
    server_version = "0.1.4"
    server_message = f"Welcome to pymcp server v{server_version}"
    recipient = name if name else "World"
    greeting = f"Hello, {recipient}! {server_message}"
    
    # Generate current UTC timestamp in ISO 8601 format
    timestamp_utc = datetime.utcnow().isoformat() + "Z"
    
    return {
        "greeting": greeting,
        "recipient": recipient,
        "server_message": server_message,
        "server_version": server_version,
        "timestamp_utc": timestamp_utc
    }