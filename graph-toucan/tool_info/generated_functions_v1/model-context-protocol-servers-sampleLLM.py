from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for LLM sampling.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_type (str): Type of the error encountered (e.g., "McpError")
        - error_code (int): Numeric error code indicating the specific failure (e.g., -32600)
        - error_message (str): Human-readable description of the error
        - traceback_lines_0 (str): First line of the traceback stack
        - traceback_lines_1 (str): Second line of the traceback stack
    """
    return {
        "error_type": "McpError",
        "error_code": -32600,
        "error_message": "Invalid request format",
        "traceback_lines_0": "File \"mcp_server.py\", line 123, in handle_request",
        "traceback_lines_1": "File \"sampling.py\", line 45, in sample_llm"
    }

def model_context_protocol_servers_sampleLLM(prompt: str, maxTokens: Optional[int] = None) -> Dict[str, Any]:
    """
    Samples from an LLM using MCP's sampling feature.
    
    Args:
        prompt (str): The prompt to send to the LLM (required)
        maxTokens (Optional[int]): Maximum number of tokens to generate (optional)
    
    Returns:
        Dict containing:
        - error_type (str): type of the error encountered (e.g., "McpError")
        - error_code (int): numeric error code indicating the specific failure (e.g., -32600)
        - error_message (str): human-readable description of the error
        - traceback_lines (List[str]): individual lines of the traceback stack showing where the error occurred
    
    Raises:
        ValueError: If prompt is empty or not provided
    """
    # Input validation
    if not prompt:
        raise ValueError("Prompt is required and cannot be empty")
    
    if maxTokens is not None and maxTokens <= 0:
        raise ValueError("maxTokens must be a positive integer")
    
    # Call external API to get simulated response data
    api_data = call_external_api("model-context-protocol-servers-sampleLLM")
    
    # Construct the result with proper nested structure
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