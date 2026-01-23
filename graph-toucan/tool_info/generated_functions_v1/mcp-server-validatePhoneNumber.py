from typing import Dict, Any

def mcp_server_validatePhoneNumber(phone_number: str) -> Dict[str, bool]:
    """
    Validates if the given phone number is a valid Nepali phone number.
    
    A valid Nepali phone number:
    - Is 10 digits long
    - Starts with one of the following operator codes: 98, 97, 96
    - Contains only numeric digits
    
    Parameters:
        phone_number (str): The phone number to validate. Expected to be a string of digits, 
                           possibly starting with country code (+977) or without.
    
    Returns:
        Dict[str, bool]: A dictionary with a single key 'is_valid' indicating whether 
                         the phone number is valid (True) or not (False).
    """
    # Remove any leading +, spaces, hyphens, or parentheses
    cleaned_number = ''.join(filter(str.isdigit, phone_number))
    
    # Check if the number starts with country code 977 and remove it
    if cleaned_number.startswith('977'):
        cleaned_number = cleaned_number[3:]
    elif cleaned_number.startswith('0'):
        # Sometimes numbers are written with leading 0
        cleaned_number = cleaned_number[1:]
    
    # Check length and prefix
    if len(cleaned_number) != 10:
        return {"is_valid": False}
    
    # Valid Nepali mobile prefixes
    valid_prefixes = ('98', '97', '96')
    if not cleaned_number.startswith(valid_prefixes):
        return {"is_valid": False}
    
    # Ensure all characters are digits (redundant after filtering but safe)
    if not cleaned_number.isdigit():
        return {"is_valid": False}
    
    return {"is_valid": True}