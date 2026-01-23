from typing import Dict, Any, Optional

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
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
    api_data = call_external_api("kroki-server-download_diagram", **locals())
    
    # Construct result using data from simulated API
    result = {
        "file_path": api_data["file_path"],
        "status": api_data["status"]
    }
    
    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
