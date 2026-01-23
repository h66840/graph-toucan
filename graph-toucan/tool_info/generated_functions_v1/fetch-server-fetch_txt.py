from typing import Dict, Any, Optional
import re


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for tool 'fetch-server-fetch_txt'.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): Plain text content extracted from the webpage with HTML removed
    """
    # Simulate realistic plain text content from a webpage
    return {
        "content": (
            "Welcome to Example Website\n\n"
            "This is a sample website used for demonstration purposes. "
            "Our mission is to provide high-quality educational content "
            "on web technologies, programming, and software development.\n\n"
            "Latest Updates:\n\n"
            "- New course on Python programming launched\n"
            "- Workshop on web scraping techniques scheduled for next week\n"
            "- Updated tutorials on data analysis with pandas\n\n"
            "Contact us at contact@example.com for more information."
        )
    }


def fetch_server_fetch_txt(url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Fetch a website and return the content as plain text with HTML tags removed.
    
    This function simulates fetching a webpage and extracting only meaningful textual content
    by removing all HTML markup and returning clean text.
    
    Args:
        url (str): URL of the website to fetch (required)
        headers (Optional[Dict[str, str]]): Optional headers to include in the request
        
    Returns:
        Dict[str, str]: A dictionary containing the extracted plain text content
            - content (str): Plain text content extracted from the webpage, with all HTML tags removed
                            and only meaningful textual information preserved
    
    Raises:
        ValueError: If url is empty or None
    """
    # Input validation
    if not url:
        raise ValueError("URL is required and cannot be empty")
    
    if not isinstance(url, str):
        raise ValueError("URL must be a string")
    
    if headers is not None:
        if not isinstance(headers, dict):
            raise ValueError("Headers must be a dictionary")
        for k, v in headers.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError("Header keys and values must be strings")
    
    # Call external API to get simulated response
    api_data = call_external_api("fetch-server-fetch_txt")
    
    # Extract content from API response
    raw_content = api_data["content"]
    
    # Ensure content is string
    if not isinstance(raw_content, str):
        raw_content = str(raw_content)
    
    # Remove any potential HTML-like tags if present (defensive cleaning)
    # This simulates the HTML removal process
    clean_content = re.sub(r'<[^>]+>', '', raw_content)
    
    # Normalize whitespace
    clean_content = re.sub(r'\s+', ' ', clean_content)
    clean_content = clean_content.strip()
    
    # Return in required format
    return {
        "content": clean_content
    }