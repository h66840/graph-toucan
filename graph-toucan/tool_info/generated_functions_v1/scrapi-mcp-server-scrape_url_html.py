from typing import Dict, Any
import datetime
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external ScrAPI service for scraping a URL.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - html_content (str): Raw HTML content retrieved from the URL
        - status (str): Status of the scraping attempt ('success' or 'failed')
        - url (str): Final resolved URL after redirects or routing
        - timestamp (str): ISO 8601 timestamp when scraping completed
        - metadata_http_status_code (int): HTTP status code of the response
        - metadata_page_language (str): Detected language of the page (e.g., 'en')
        - metadata_response_header_content_type (str): Content-Type header value
        - metadata_response_header_server (str): Server header value
        - metadata_warning_captcha_bypassed (bool): Whether CAPTCHA was encountered and bypassed
        - error (str): Error message if scraping failed, otherwise empty string
    """
    # Generate realistic mock data
    success = random.choice([True, True, True, False])  # 75% success rate
    status = "success" if success else "failed"
    
    # Generate mock HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head><title>Sample Page - {'Success' if success else 'Error'}</title></head>
<body>
    <h1>Welcome to the scraped page</h1>
    <p>This is a simulated HTML response from the ScrAPI service.</p>
    <p>Target URL: https://example.com/page-{random.randint(1000, 9999)}</p>
    <div class="content">Generated at: {datetime.datetime.utcnow().isoformat()}</div>
</body>
</html>"""

    # Generate timestamp
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    
    # Final URL (may differ due to redirects)
    final_url = "https://example.com/home" if success else "https://example.com/error"
    
    # Metadata fields
    http_status_code = 200 if success else random.choice([404, 500, 403])
    page_language = random.choice(["en", "es", "fr", "de"])
    content_type = "text/html; charset=utf-8"
    server_header = random.choice(["nginx", "Apache", "cloudflare", "AmazonS3"])
    captcha_bypassed = not success and random.choice([True, False])
    
    # Error message if failed
    error = ""
    if not success:
        error = random.choice([
            "Page not found",
            "Access denied",
            "Timeout occurred",
            "Blocked by bot detection"
        ])
    
    return {
        "html_content": html_content,
        "status": status,
        "url": final_url,
        "timestamp": timestamp,
        "metadata_http_status_code": http_status_code,
        "metadata_page_language": page_language,
        "metadata_response_header_content_type": content_type,
        "metadata_response_header_server": server_header,
        "metadata_warning_captcha_bypassed": captcha_bypassed,
        "error": error
    }

def scrapi_mcp_server_scrape_url_html(url: str) -> Dict[str, Any]:
    """
    Use a URL to scrape a website using the ScrAPI service and retrieve the result as HTML.
    This function handles websites with bot detection, captchas, or geolocation restrictions.
    
    Args:
        url (str): The URL to scrape. Must be a valid string.
    
    Returns:
        Dict containing:
        - html_content (str): The full HTML content retrieved from the specified URL after scraping.
        - status (str): Indicates the outcome of the scraping attempt ('success' or 'failed').
        - url (str): The final resolved URL that was scraped.
        - timestamp (str): ISO 8601 timestamp indicating when the scraping request was completed.
        - metadata (Dict): Additional contextual information about the scrape including:
            - http_status_code (int): HTTP status code of the response
            - page_language (str): Detected language of the page
            - response_headers (Dict): Response headers including content-type and server
            - warnings (List[str]): Any warnings encountered during scraping
        - error (str): Error message if the scraping failed; otherwise empty string.
    
    Raises:
        ValueError: If the URL is not provided or is invalid.
    """
    # Input validation
    if not url or not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string")
    
    # Clean URL
    url = url.strip()
    
    # Call external API (mocked)
    api_data = call_external_api("scrapi-mcp-server-scrape_url_html")
    
    # Construct metadata response headers
    response_headers = {
        "content-type": api_data["metadata_response_header_content_type"],
        "server": api_data["metadata_response_header_server"]
    }
    
    # Construct warnings list
    warnings = []
    if api_data["metadata_warning_captcha_bypassed"]:
        warnings.append("CAPTCHA encountered but bypassed")
    
    # Build final result structure matching output schema
    result = {
        "html_content": api_data["html_content"],
        "status": api_data["status"],
        "url": api_data["url"],
        "timestamp": api_data["timestamp"],
        "metadata": {
            "http_status_code": api_data["metadata_http_status_code"],
            "page_language": api_data["metadata_page_language"],
            "response_headers": response_headers,
            "warnings": warnings
        },
        "error": api_data["error"]
    }
    
    return result