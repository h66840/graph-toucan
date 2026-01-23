from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching LGTM image data from an external API.
    
    Returns:
        Dict with simple fields only (str):
        - markdown_code (str): Markdown-formatted string with LGTM image link
        - image_url (str): Direct URL to the LGTM image file
        - page_url (str): URL of the page hosting the LGTM image
    """
    return {
        "markdown_code": "[![LGTM](https://lgtm.lol/i/abc123.jpg)](https://lgtm.lol/i/abc123)",
        "image_url": "https://lgtm.lol/i/abc123.jpg",
        "page_url": "https://lgtm.lol/i/abc123"
    }

def lgtm_get_lgtm() -> Dict[str, str]:
    """
    Get LGTM image and return markdown code, image URL, and page URL.
    
    Returns:
        Dict containing:
        - markdown_code (str): Markdown-formatted string containing the LGTM image link
        - image_url (str): Direct URL to the LGTM image file
        - page_url (str): URL of the page hosting the LGTM image
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("lgtm-get_lgtm")
        
        # Construct result matching output schema
        result = {
            "markdown_code": api_data["markdown_code"],
            "image_url": api_data["image_url"],
            "page_url": api_data["page_url"]
        }
        
        return result
        
    except Exception as e:
        # Fallback in case of error
        fallback_url = "https://lgtm.lol/i/default"
        return {
            "markdown_code": f"[![LGTM]({fallback_url}.jpg)]({fallback_url})",
            "image_url": f"{fallback_url}.jpg",
            "page_url": fallback_url
        }