from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for retrieving a documentation page.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): Title of the documentation page
        - description (str): Brief description or subtitle of the page
        - path (str): Root-relative path of the documentation page
        - content (str): Full Markdown/HTML content of the documentation page
    """
    return {
        "title": "Getting Started with Atlas",
        "description": "Learn how to set up and use Atlas for your projects.",
        "path": "/guides/getting-started",
        "content": "# Getting Started\n\nWelcome to Atlas! This guide will help you get up and running quickly.\n\n## Installation\n\n```bash\npip install atlas-sdk\n```\n\n## Initialization\n\n```python\nfrom atlas import Client\nclient = Client(api_key='your-key')\n```\n\nNow you're ready to go!"
    }

def atlas_docs_get_docs_page(docName: str, pagePath: str) -> Dict[str, Any]:
    """
    Retrieves a specific documentation page's content using its relative path.
    
    This function simulates retrieving detailed information about a known topic
    after identifying the relevant page through an index or search. It returns
    the complete content of a single documentation page.

    Args:
        docName (str): Name of the documentation set (e.g., 'atlas-api', 'atlas-sdk')
        pagePath (str): The root-relative path of the specific documentation page 
                       (e.g., '/guides/getting-started', '/api/authentication')

    Returns:
        Dict[str, Any]: A dictionary containing the documentation page data with keys:
            - title (str): Title of the documentation page
            - description (str): Brief description or subtitle of the page
            - path (str): Root-relative path of the documentation page
            - content (str): Full Markdown/HTML content of the documentation page
    """
    # Input validation
    if not docName or not isinstance(docName, str):
        raise ValueError("docName must be a non-empty string")
    if not pagePath or not isinstance(pagePath, str):
        raise ValueError("pagePath must be a non-empty string")
    if not pagePath.startswith("/"):
        raise ValueError("pagePath must be a root-relative path starting with '/'")

    # Call simulated external API
    api_data = call_external_api("atlas-docs-get_docs_page")

    # Construct and return the result matching the output schema
    result = {
        "title": api_data["title"],
        "description": api_data["description"],
        "path": api_data["path"],
        "content": api_data["content"]
    }

    return result