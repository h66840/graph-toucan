from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Kroki diagram URL generation.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - diagram_url (str): URL to the rendered diagram on Kroki.io
    """
    return {
        "diagram_url": "https://kroki.io/mermaid/svg/eNpLyUxOtVJISixJLCoBshIzUxwBQxgKSw=="
    }

def kroki_server_generate_diagram_url(content: str, type: str, outputFormat: Optional[str] = "svg") -> Dict[str, Any]:
    """
    Generate a URL for a diagram using Kroki.io. This function simulates generating a URL 
    based on diagram content, type, and desired output format.
    
    Args:
        content (str): The diagram content in the specified format (e.g., Mermaid syntax).
        type (str): Diagram type (e.g., "mermaid", "plantuml", "graphviz", "c4plantuml").
        outputFormat (str, optional): Output image format. Options: "svg", "png", "pdf", "jpeg", "base64". 
                                     Defaults to "svg".
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - diagram_url (str): URL to the rendered diagram on Kroki.io
    
    Example:
        >>> kroki_server_generate_diagram_url("graph TD; A-->B; B-->C;", "mermaid")
        {'diagram_url': 'https://kroki.io/mermaid/svg/eNpLyUxOtVJISixJLCoBshIzUxwBQxgKSw=='}
    """
    # Input validation
    if not content:
        raise ValueError("Parameter 'content' is required and cannot be empty.")
    
    if not type:
        raise ValueError("Parameter 'type' is required and cannot be empty.")
    
    if outputFormat not in ["svg", "png", "pdf", "jpeg", "base64"]:
        raise ValueError("Parameter 'outputFormat' must be one of: svg, png, pdf, jpeg, base64")
    
    # Call simulated external API
    api_data = call_external_api("kroki-server-generate_diagram_url")
    
    # Construct result matching output schema
    result = {
        "diagram_url": api_data["diagram_url"]
    }
    
    return result