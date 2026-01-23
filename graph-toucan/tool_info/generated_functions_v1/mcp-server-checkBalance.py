from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - balance (int): the current mobile balance in Nepali Rupees (Rs) associated with the validated phone number
    """
    # Simulated balance based on phone number pattern (last 3 digits used for deterministic variation)
    # Since we cannot access real API, we generate a realistic mock balance
    return {
        "balance": 2500  # Mock balance in Nepali Rupees
    }

def mcp_server_checkBalance(phone_number: str) -> Dict[str, Any]:
    """
    Takes a validated phone number and returns the balance of the user.
    
    This function simulates querying a mobile balance service by using a mock API call.
    The phone number is validated for correct format (Nepali mobile number: 10 digits starting with 98 or 97).
    
    Args:
        phone_number (str): The validated phone number in string format (e.g., '9841234567')
    
    Returns:
        Dict[str, Any]: A dictionary containing the balance in Nepali Rupees (Rs)
        - balance (int): the current mobile balance in Nepali Rupees (Rs) associated with the validated phone number
    
    Raises:
        ValueError: If the phone number is not a valid Nepali mobile number
    """
    # Input validation: Check if phone_number is a valid Nepali mobile number
    if not isinstance(phone_number, str):
        raise ValueError("Phone number must be a string")
    
    if not phone_number.isdigit():
        raise ValueError("Phone number must contain only digits")
    
    if not (phone_number.startswith("98") or phone_number.startswith("97")):
        raise ValueError("Invalid Nepali mobile number: must start with 98 or 97")
    
    if len(phone_number) != 10:
        raise ValueError("Phone number must be exactly 10 digits long")
    
    # Call the external API simulation
    api_data = call_external_api("mcp-server-checkBalance")
    
    # Construct result matching output schema
    result = {
        "balance": api_data["balance"]
    }
    
    return result