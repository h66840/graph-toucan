from typing import Dict, Any, Optional

def simple_mcp_server_say_hello(name: str, formal: Optional[bool] = False) -> Dict[str, str]:
    """
    Greets a person with a personalized message based on formality preference.
    
    Parameters:
        name (str): The name of the person to greet. Required.
        formal (bool, optional): Whether to use a formal tone. Defaults to False.
    
    Returns:
        Dict[str, str]: A dictionary containing:
            - greeting (str): The full greeting message.
            - tone (str): The level of formality ("formal" or "informal").
            - recipient (str): The name of the person being addressed.
    
    Raises:
        ValueError: If 'name' is empty or contains only whitespace.
    """
    if not name or not name.strip():
        raise ValueError("Parameter 'name' is required and cannot be empty or whitespace.")
    
    name = name.strip()
    tone = "formal" if formal else "informal"
    
    if formal:
        greeting = f"Good day, Mr. {name}."
    else:
        greeting = f"Hey there, {name}! How's it going?"
    
    return {
        "greeting": greeting,
        "tone": tone,
        "recipient": name
    }