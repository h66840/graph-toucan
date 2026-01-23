from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for sending an email.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_message (str): Detailed error message describing the failure reason
        - error_code (str): Standardized error code if available (e.g., "ECONNREFUSED")
        - host (str): Target host address involved in the connection attempt
        - port (int): Target port number involved in the connection attempt
        - connection_status (str): High-level status of the email sending attempt (e.g., "failed")
    """
    return {
        "error_message": "Connection refused by the email server",
        "error_code": "ECONNREFUSED",
        "host": "smtp.example.com",
        "port": 587,
        "connection_status": "failed"
    }

def email_sender_server_send_email(body: str, subject: str, to: List[str]) -> Dict[str, Any]:
    """
    Send an email to a recipient.
    
    This function simulates sending an email by calling an external API that returns
    connection and error details. It validates inputs and constructs a realistic response
    based on the provided parameters.
    
    Args:
        body (str): Email body content (used for text/plain or when htmlBody not provided)
        subject (str): Email subject
        to (List[str]): List of recipient email addresses
        
    Returns:
        Dict[str, Any]: A dictionary containing email sending result with the following fields:
            - error_message (str): Detailed error message describing the failure reason
            - error_code (str): Standardized error code if available (e.g., "ECONNREFUSED")
            - host (str): Target host address involved in the connection attempt
            - port (int): Target port number involved in the connection attempt
            - connection_status (str): High-level status of the email sending attempt (e.g., "failed")
            
    Raises:
        ValueError: If any required parameter is missing or invalid
    """
    # Input validation
    if not body:
        raise ValueError("Email body is required")
    if not subject:
        raise ValueError("Email subject is required")
    if not to or not isinstance(to, list) or len(to) == 0:
        raise ValueError("At least one recipient email address is required")
    
    # Validate email addresses format (basic check)
    for email in to:
        if not isinstance(email, str) or "@" not in email:
            raise ValueError(f"Invalid email address: {email}")
    
    # Call external API to simulate sending email
    api_data = call_external_api("email-sender-server-send_email")
    
    # Construct result dictionary matching output schema
    result = {
        "error_message": api_data["error_message"],
        "error_code": api_data["error_code"],
        "host": api_data["host"],
        "port": api_data["port"],
        "connection_status": api_data["connection_status"]
    }
    
    return result