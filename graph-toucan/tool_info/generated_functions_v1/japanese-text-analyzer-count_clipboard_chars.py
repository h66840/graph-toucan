from typing import Dict, Any
from datetime import datetime

def japanese_text_analyzer_count_clipboard_chars(text: str) -> Dict[str, Any]:
    """
    テキストの文字数を計測します。スペースや改行を除いた実質的な文字数をカウントします。
    
    Parameters:
        text (str): 文字数をカウントするテキスト
    
    Returns:
        Dict[str, Any] with the following keys:
        - character_count (int): The total number of non-whitespace and non-newline characters in the provided Japanese text
        - whitespace_excluded (bool): Indicates whether spaces, tabs, and newlines were excluded from the count as per processing rules
        - analysis_timestamp (str): ISO 8601 timestamp indicating when the character count analysis was performed
        - input_text_length (int): The original length of the input text including all characters (for reference/comparison)
        - processed_text_sample (str): A truncated sample of the processed text after removing whitespace, up to 50 characters
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string")

    # Record original length
    input_text_length = len(text)

    # Remove all whitespace characters (spaces, tabs, newlines)
    processed_text = ''.join(text.split())
    
    # Count characters after whitespace removal
    character_count = len(processed_text)
    
    # Create a sample of the processed text (max 50 characters)
    processed_text_sample = processed_text[:50]
    
    # Current timestamp in ISO 8601 format
    analysis_timestamp = datetime.now().isoformat()

    # Return the result dictionary
    return {
        "character_count": character_count,
        "whitespace_excluded": True,
        "analysis_timestamp": analysis_timestamp,
        "input_text_length": input_text_length,
        "processed_text_sample": processed_text_sample
    }