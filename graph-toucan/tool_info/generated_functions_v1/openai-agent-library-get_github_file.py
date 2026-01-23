from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for GitHub file retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): Raw text content of the requested GitHub file
        - error_type (str): Type of error if file retrieval fails
        - error_message (str): Error message if file retrieval fails
        - error_status_code (int): HTTP status code if available in case of error
    """
    # Simulate successful file retrieval
    return {
        "content": "def hello_world():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    hello_world()\n",
        "error_type": "",
        "error_message": "",
        "error_status_code": 0
    }

def openai_agent_library_get_github_file(path: str) -> Dict[str, Any]:
    """
    Get content of a specific file from the GitHub repository.
    
    Args:
        path (str): The file path in the GitHub repository to retrieve.
        
    Returns:
        Dict containing either:
        - content (str): the raw text content of the requested GitHub file if successfully retrieved
        - error (Dict): contains error details when file retrieval fails, including 'type', 'message', and 'status_code' if available
    """
    # Input validation
    if not isinstance(path, str):
        return {
            "error": {
                "type": "InvalidInput",
                "message": "Path must be a string",
                "status_code": 400
            }
        }
    
    if not path.strip():
        return {
            "error": {
                "type": "InvalidInput",
                "message": "Path cannot be empty",
                "status_code": 400
            }
        }
    
    # Call external API simulation
    api_data = call_external_api("openai-agent-library-get_github_file")
    
    # Construct result based on whether there was an error
    if api_data.get("error_type"):
        return {
            "error": {
                "type": api_data["error_type"],
                "message": api_data["error_message"],
                "status_code": api_data["error_status_code"] if api_data["error_status_code"] else None
            }
        }
    else:
        return {
            "content": api_data["content"]
        }