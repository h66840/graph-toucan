from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for text editor operations.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Whether the operation was successful
        - message (str): Description of the result or status of the operation
        - content (str): Full text content of the file when viewing or reading a file
    """
    return {
        "success": True,
        "message": "Operation completed successfully",
        "content": "1: # Sample file content\n2: def hello():\n3:     print('Hello, world!')"
    }

def text_editor_mcp_server_text_editor(
    command: str,
    description: str,
    path: str,
    file_text: Optional[str] = None,
    insert_line: Optional[int] = None,
    new_str: Optional[str] = None,
    old_str: Optional[str] = None,
    view_range: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    View, create, and edit files with persistent state across command calls.
    
    Args:
        command (str): The command to execute. One of: 'view', 'create', 'str_replace', 'insert', 'undo_edit'
        description (str): Reason for using the text editor (max 80 chars)
        path (str): Absolute path to file or directory
        file_text (str, optional): Content to create the file with (for 'create' command)
        insert_line (int, optional): Line number after which to insert (for 'insert' command)
        new_str (str, optional): New string to insert or replace with
        old_str (str, optional): String to be replaced (for 'str_replace' command)
        view_range (List[int], optional): Line number range to view in format [start, end] or [start, -1]

    Returns:
        Dict containing:
        - success (bool): Whether the operation was successful
        - message (str): Description of the result or status of the operation
        - content (str, optional): Full text content of the file when viewing or reading a file
    """
    # Input validation
    if not command:
        return {
            "success": False,
            "message": "Command is required",
            "content": None
        }
    
    if not description:
        return {
            "success": False,
            "message": "Description is required",
            "content": None
        }
    
    if not path:
        return {
            "success": False,
            "message": "Path is required",
            "content": None
        }
    
    # Validate command-specific parameters
    if command == "create" and file_text is None:
        return {
            "success": False,
            "message": "file_text is required for create command",
            "content": None
        }
    
    if command == "insert" and (insert_line is None or new_str is None):
        return {
            "success": False,
            "message": "insert_line and new_str are required for insert command",
            "content": None
        }
    
    if command == "str_replace" and (old_str is None or new_str is None):
        return {
            "success": False,
            "message": "old_str and new_str are required for str_replace command",
            "content": None
        }
    
    # Call external API to simulate the operation
    api_data = call_external_api("text-editor-mcp-server-text_editor")
    
    # Construct result matching output schema
    result: Dict[str, Any] = {
        "success": api_data["success"],
        "message": api_data["message"]
    }
    
    # Add content only if available
    if "content" in api_data:
        result["content"] = api_data["content"]
    
    return result