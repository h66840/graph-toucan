from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for LLM sampling.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_type (str): Type of the error encountered, e.g., "McpError"
        - error_code (int): Numeric error code associated with the failure, e.g., -32600
        - error_message (str): Detailed description of the error
        - traceback_lines_0 (str): First line of traceback
        - traceback_lines_1 (str): Second line of traceback
    """
    return {
        "error_type": "McpError",
        "error_code": -32600,
        "error_message": "Invalid request format",
        "traceback_lines_0": "Traceback (most recent call last):",
        "traceback_lines_1": 'File "<stdin>", line 1, in <module>\nValueError: Invalid JSON-RPC request'
    }

def model_context_protocol_reference_servers_sampleLLM(
    prompt: str,
    maxTokens: Optional[int] = None
) -> Dict[str, Any]:
    """
    Samples from an LLM using MCP's sampling feature.
    
    Args:
        prompt (str): The prompt to send to the LLM (required)
        maxTokens (Optional[int]): Maximum number of tokens to generate (optional)
    
    Returns:
        Dict containing:
        - error_type (str): type of the error encountered, e.g., "McpError"
        - error_code (int): numeric error code associated with the failure, e.g., -32600
        - error_message (str): detailed description of the error
        - traceback_lines (List[str]): list of raw traceback lines showing the full call stack
    
    Raises:
        ValueError: If prompt is empty or None
    """
    # Input validation
    if not prompt:
        raise ValueError("Prompt is required and cannot be empty")
    
    # Call external API to simulate response
    api_data = call_external_api("model-context-protocol-reference-servers-sampleLLM")
    
    # Construct nested structure matching output schema
    result = {
        "error_type": api_data["error_type"],
        "error_code": api_data["error_code"],
        "error_message": api_data["error_message"],
        "traceback_lines": [
            api_data["traceback_lines_0"],
            api_data["traceback_lines_1"]
        ]
    }
    
    return result