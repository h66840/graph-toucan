from typing import Dict, Any, Optional
import random
import string

def pymcp_generate_password(length: Optional[int] = 8, use_special_chars: Optional[bool] = False) -> Dict[str, Any]:
    """
    Generate a random password with specified length, optionally including special characters.
    
    The password will meet complexity requirements: at least one lowercase letter, one uppercase letter,
    two digits, and if requested, one special character. The function regenerates the password until
    all requirements are met.
    
    Args:
        length (int, optional): The length of the password to generate (between 8 and 64 characters). Default is 8.
        use_special_chars (bool, optional): Whether to include special characters in the password. Default is False.
    
    Returns:
        Dict[str, Any]: A dictionary containing the generated password string.
            - password (str): The generated random password that meets complexity requirements.
    
    Raises:
        ValueError: If length is not between 8 and 64 inclusive.
    """
    # Validate input
    if length is None:
        length = 8
    if not isinstance(length, int) or length < 8 or length > 64:
        raise ValueError("Length must be an integer between 8 and 64 inclusive.")
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    all_chars = lowercase + uppercase + digits
    if use_special_chars:
        all_chars += special_chars
    
    while True:
        # Generate random password
        password = ''.join(random.choice(all_chars) for _ in range(length))
        
        # Check complexity requirements
        has_lower = any(c in lowercase for c in password)
        has_upper = any(c in uppercase for c in password)
        digit_count = sum(c in digits for c in password)
        has_special = any(c in special_chars for c in password) if use_special_chars else True
        
        # Must have at least one lowercase, one uppercase, two digits, and special char if requested
        if has_lower and has_upper and digit_count >= 2 and has_special:
            break
    
    return {"password": password}