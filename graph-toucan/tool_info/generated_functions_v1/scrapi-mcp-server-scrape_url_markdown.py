from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for web scraping via ScrAPI service.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): Scraped webpage content in Markdown format
        - title (str): Main title of the page
        - footer_text (str): Footer text such as copyright notices
        - disclaimer (str): Legal disclaimers or domain sale notices
        - links_0_text (str): Text label of the first link
        - links_0_url (str): URL of the first link
        - links_1_text (str): Text label of the second link
        - links_1_url (str): URL of the second link
    """
    return {
        "content": "# Welcome to Example.com\n\nThis is a sample website used for demonstration purposes.\n\nLearn more about us on the [about page](/about).",
        "title": "Welcome to Example.com",
        "footer_text": "© 2025 Example.com. All rights reserved.",
        "disclaimer": "This domain is for sale. Contact sales@example.com for inquiries.",
        "links_0_text": "about page",
        "links_0_url": "/about",
        "links_1_text": "privacy policy",
        "links_1_url": "/privacy",
    }

def scrapi_mcp_server_scrape_url_markdown(url: str) -> Dict[str, Any]:
    """
    Scrape a website using the ScrAPI service and retrieve the result as Markdown.
    
    This function simulates scraping a webpage that may have bot detection, captchas,
    or geolocation restrictions. The result includes the main content in Markdown format,
    extracted links, title, footer text, and any disclaimers.

    Args:
        url (str): The URL of the webpage to scrape. Must be a valid string.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - content (str): The scraped webpage content in Markdown format
            - links (List[Dict]): List of dictionaries with 'text' and 'url' keys
            - title (str): The main title of the page
            - footer_text (str): Footer content like copyright notices
            - disclaimer (str): Any legal or advisory text on the page

    Raises:
        ValueError: If the URL is empty or not a string
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")

    api_data = call_external_api("scrapi-mcp-server-scrape_url_markdown")

    links = [
        {"text": api_data["links_0_text"], "url": api_data["links_0_url"]},
        {"text": api_data["links_1_text"], "url": api_data["links_1_url"]}
    ]

    result = {
        "content": api_data["content"],
        "links": links,
        "title": api_data["title"],
        "footer_text": api_data["footer_text"],
        "disclaimer": api_data["disclaimer"]
    }

    return result