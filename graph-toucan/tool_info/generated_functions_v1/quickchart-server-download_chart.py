from typing import Dict, List, Any, Optional
import json

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for chart download operation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_code (str): error code from the MCP system, e.g., "-32603"
        - error_message (str): human-readable description of the error
        - failed_operation (str): the operation that failed, e.g., "download chart"
        - traceback_0 (str): first line of traceback
        - traceback_1 (str): second line of traceback
        - tool_name (str): name of the tool that generated the error
    """
    return {
        "error_code": "-32603",
        "error_message": "Internal error occurred while processing the request",
        "failed_operation": "download chart",
        "traceback_0": "File \"quickchart/server.py\", line 42, in download_chart",
        "traceback_1": "File \"quickchart/utils.py\", line 15, in generate_image",
        "tool_name": "quickchart-server-download_chart"
    }

def quickchart_server_download_chart(config: Dict[str, Any], outputPath: str) -> Dict[str, Any]:
    """
    Download a chart image to a local file based on the provided chart configuration.
    
    This function simulates downloading a chart image by validating inputs,
    constructing a chart configuration, and simulating interaction with an external
    chart generation service. It returns an error object if any issues occur.
    
    Args:
        config (Dict[str, Any]): Chart configuration object containing chart type,
                                data, labels, and styling options
        outputPath (str): Path where the chart image should be saved (e.g., PNG, JPEG)
    
    Returns:
        Dict[str, Any]: Error object with the following fields:
            - error_code (str): error code from the MCP system, e.g., "-32603"
            - error_message (str): human-readable description of the error
            - failed_operation (str): the operation that failed, e.g., "download chart"
            - traceback (List[str]): list of traceback lines showing where the error occurred
            - tool_name (str): name of the tool that generated the error
    
    Raises:
        ValueError: If required parameters are missing or invalid
        TypeError: If parameters are of incorrect type
    """
    # Input validation
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")
    
    if not config:
        raise ValueError("config cannot be empty")
    
    if not isinstance(outputPath, str):
        raise TypeError("outputPath must be a string")
    
    if not outputPath.strip():
        raise ValueError("outputPath cannot be empty")
    
    # Validate outputPath contains only safe characters and no dangerous path components
    safe_output_path = outputPath.strip()
    
    # Check for dangerous path patterns
    dangerous_patterns = ['..', '//', '\\', '\x00']
    if any(pattern in safe_output_path for pattern in dangerous_patterns):
        api_data = call_external_api("quickchart-server-download_chart")
        return {
            "error_code": api_data["error_code"],
            "error_message": f"Invalid path: {safe_output_path}",
            "failed_operation": "download chart",
            "traceback": [api_data["traceback_0"], api_data["traceback_1"]],
            "tool_name": api_data["tool_name"]
        }
    
    # Simulate chart generation and file writing process
    try:
        # Convert config to JSON string for simulation
        config_str = json.dumps(config)
        
        # Simulate writing chart data to file (in real implementation, this would
        # involve generating an actual image using a charting library)
        dummy_image_content = f"PNG_IMAGE_DATA_FOR:{config_str[:100]}"
        
        # The function's docstring indicates it should download a chart to a file,
        # so file I/O is required. We've validated the path is safe.
        try:
            # Using open() is necessary here as the function's purpose is to write to a file
            with open(safe_output_path, 'w') as f:
                f.write(dummy_image_content)
        except (OSError, IOError) as e:
            api_data = call_external_api("quickchart-server-download_chart")
            return {
                "error_code": api_data["error_code"],
                "error_message": f"Failed to write to file: {str(e)}",
                "failed_operation": "download chart",
                "traceback": [api_data["traceback_0"], api_data["traceback_1"]],
                "tool_name": api_data["tool_name"]
            }
            
        # If successful, return empty error object (all fields None/empty except tool_name)
        return {
            "error_code": None,
            "error_message": None,
            "failed_operation": None,
            "traceback": [],
            "tool_name": "quickchart-server-download_chart"
        }
        
    except Exception as e:
        # On any error during processing, return error object
        api_data = call_external_api("quickchart-server-download_chart")
        return {
            "error_code": api_data["error_code"],
            "error_message": f"Failed to download chart: {str(e)}",
            "failed_operation": "download chart",
            "traceback": [api_data["traceback_0"], api_data["traceback_1"]],
            "tool_name": api_data["tool_name"]
        }