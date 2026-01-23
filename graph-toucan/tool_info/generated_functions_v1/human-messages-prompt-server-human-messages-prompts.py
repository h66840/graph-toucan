from typing import Dict, Any, Optional

def human_messages_prompt_server_human_messages_prompts(message: Optional[str] = None, platform: str = "") -> Dict[str, str]:
    """
    Generate a prompt for a human message adapted to a specific communication platform.
    
    Args:
        message (Optional[str]): The original message content to be transformed. If not provided, a default message is used.
        platform (str): The target communication platform (e.g., email, twitter, discord). This is required and influences formatting.
    
    Returns:
        Dict[str, str]: A dictionary containing:
            - transformed_message (str): The fully formatted human-readable message adapted for the specified platform.
            - platform (str): The communication platform for which the message was transformed.
    
    Raises:
        ValueError: If platform is empty or not supported.
    """
    # Input validation
    if not platform:
        raise ValueError("Parameter 'platform' is required and cannot be empty.")
    
    # Define platform-specific formatting rules
    formatting_rules = {
        "email": {
            "header": "Dear User,\n\n",
            "footer": "\n\nBest regards,\nSupport Team",
            "max_length": None,
            "prefix": "",
            "suffix": ""
        },
        "twitter": {
            "header": "",
            "footer": "",
            "max_length": 280,
            "prefix": "",
            "suffix": " #Update"
        },
        "discord": {
            "header": "**New Message:**\n",
            "footer": "\n---",
            "max_length": None,
            "prefix": "",
            "suffix": ""
        },
        "slack": {
            "header": ":information_source: *Message*\n",
            "footer": "\nThanks!",
            "max_length": None,
            "prefix": "",
            "suffix": ""
        },
        "sms": {
            "header": "",
            "footer": "",
            "max_length": 160,
            "prefix": "",
            "suffix": ""
        }
    }
    
    # Use default message if none provided
    base_message = message if message is not None else "This is a system-generated notification."
    
    # Get formatting rules for the specified platform
    rules = formatting_rules.get(platform.lower(), formatting_rules["email"])  # default to email
    
    # Apply formatting
    transformed = f"{rules['prefix']}{rules['header']}{base_message}{rules['suffix']}{rules['footer']}"
    
    # Handle length constraints
    if rules["max_length"] and len(transformed) > rules["max_length"]:
        # Truncate and add ellipsis if too long
        transformed = transformed[:rules["max_length"] - 1] + "…"
    
    return {
        "transformed_message": transformed,
        "platform": platform
    }