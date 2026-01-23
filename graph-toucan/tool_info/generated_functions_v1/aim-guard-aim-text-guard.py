from typing import Dict, Any
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for text analysis.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_message (str): Detailed error message describing the failure in text analysis
        - http_status (int): HTTP status code returned by the service during the analysis attempt
        - input_text (str): The original text that was submitted for analysis
        - timestamp (str): ISO 8601 timestamp indicating when the error occurred
    """
    return {
        "error_message": "Text contains prohibited content and cannot be processed",
        "http_status": 400,
        "input_text": "This is a test text with harmful content for analysis",
        "timestamp": datetime.datetime.now().isoformat()
    }

def aim_guard_aim_text_guard(text: str) -> Dict[str, Any]:
    """
    AIM-Intelligence Text Guard Tool: Analyzes provided text for harmful content.
    
    This function simulates a text analysis service that checks for harmful content.
    It returns an error response structure indicating if the text was flagged.
    
    Args:
        text (str): Text to analyze for harmful content. Must be a non-empty string.
    
    Returns:
        Dict[str, Any]: A dictionary containing the analysis result with the following fields:
            - error_message (str): Detailed error message describing the failure in text analysis
            - http_status (int): HTTP status code returned by the service during the analysis attempt
            - input_text (str): The original text that was submitted for analysis
            - timestamp (str): ISO 8601 timestamp indicating when the error occurred
    
    Raises:
        ValueError: If the input text is empty or not a string
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        raise ValueError("Text cannot be empty or whitespace only")
    
    # Call external API simulation
    api_data = call_external_api("aim-guard-aim-text-guard")
    
    # Construct result structure matching output schema
    result = {
        "error_message": api_data["error_message"],
        "http_status": api_data["http_status"],
        "input_text": text,
        "timestamp": api_data["timestamp"]
    }
    
    return result