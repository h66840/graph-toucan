from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching book data from external API by ISBN.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_message (str): Error message if ISBN is invalid or book not found
    """
    # Simulate realistic error messages based on ISBN format
    if tool_name == "brasilapi-mcp-server-get_isbn":
        return {
            "error_message": "ISBN not found or invalid"
        }
    return {}

def brasilapi_mcp_server_get_isbn(ISBN: str) -> Dict[str, Any]:
    """
    Get information about a book given an ISBN.
    
    This function simulates querying a book database by ISBN and returns book details
    or an error message if the ISBN is invalid or the book is not found.
    
    Args:
        ISBN (str): The book's ISBN to query. Must be a non-empty string.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - error_message (str, optional): Message indicating failure to fetch book data
              when the ISBN is not found or invalid
    
    Raises:
        ValueError: If ISBN is empty or not a string
    """
    # Input validation
    if not ISBN:
        raise ValueError("ISBN is required")
    if not isinstance(ISBN, str):
        raise ValueError("ISBN must be a string")
    
    # Clean ISBN (remove hyphens and spaces)
    cleaned_isbn = ISBN.replace("-", "").replace(" ", "").strip()
    
    # Validate ISBN format (basic validation for ISBN-10 or ISBN-13)
    if len(cleaned_isbn) not in [10, 13] or not cleaned_isbn.isdigit():
        return {
            "error_message": "Invalid ISBN format. Please provide a valid 10 or 13 digit ISBN."
        }
    
    # Call external API simulation
    api_data = call_external_api("brasilapi-mcp-server-get_isbn")
    
    # Construct result using data from external API
    result: Dict[str, Any] = {}
    
    if "error_message" in api_data:
        result["error_message"] = api_data["error_message"]
    
    return result