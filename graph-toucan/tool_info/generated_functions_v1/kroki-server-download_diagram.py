from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for diagram generation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - file_path (str): Path where the diagram image was saved
        - status (str): Status message indicating success or failure
    """
    return {
        "file_path": "/Users/username/Documents/diagram.svg",
        "status": "Diagram successfully generated and saved"
    }

def kroki_server_download_diagram(
    content: str,
    outputPath: str,
    type: str,
    outputFormat: Optional[str] = None,
    scale: Optional[float] = 1.0
) -> Dict[str, Any]:
    """
    Download a diagram image to a local file by converting diagram code (e.g., Mermaid) into an image.
    
    This function simulates the behavior of generating a diagram using a remote service like Kroki,
    then saving it to the specified output path. It supports various diagram types and output formats.
    
    Args:
        content (str): The diagram content in the specified format (e.g., Mermaid syntax).
        outputPath (str): The complete file path where the diagram image should be saved.
        type (str): Diagram type (e.g., "mermaid", "plantuml", "graphviz").
        outputFormat (str, optional): Output image format. If not provided, derived from outputPath extension.
        scale (float, optional): Scaling factor for SVG output. Default is 1.0 (no scaling).
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - file_path (str): Path where the diagram image was saved
            - status (str): Status message indicating success or failure of the operation
    
    Raises:
        ValueError: If required parameters are missing or invalid.
    """
    # Input validation
    if not content:
        raise ValueError("Parameter 'content' is required and cannot be empty.")
    if not outputPath:
        raise ValueError("Parameter 'outputPath' is required and cannot be empty.")
    if not type:
        raise ValueError("Parameter 'type' is required and cannot be empty.")
    
    # Derive output format from extension if not provided
    valid_formats = ["svg", "png", "pdf", "jpeg"]
    inferred_format = outputFormat
    if not inferred_format:
        ext = outputPath.lower().split(".")[-1]
        if ext in valid_formats:
            inferred_format = ext
        else:
            raise ValueError(f"Could not determine valid output format from path: {outputPath}")
    
    if inferred_format not in valid_formats:
        raise ValueError(f"Invalid outputFormat: {inferred_format}. Must be one of {valid_formats}.")
    
    if scale is not None and scale <= 0:
        raise ValueError("Parameter 'scale' must be a positive number.")
    
    # Simulate calling external API
    api_data = call_external_api("kroki-server-download_diagram")
    
    # Construct result using data from simulated API
    result = {
        "file_path": api_data["file_path"],
        "status": api_data["status"]
    }
    
    return result