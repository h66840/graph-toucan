from typing import Dict, List, Any, Optional

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
    api_data = call_external_api("text-editor-mcp-server-text_editor", **locals())
    
    # Construct result matching output schema
    result: Dict[str, Any] = {
        "success": api_data["success"],
        "message": api_data["message"]
    }
    
    # Add content only if available
    if "content" in api_data:
        result["content"] = api_data["content"]
    
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
