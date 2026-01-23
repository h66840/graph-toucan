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
    Simulates fetching file content from an external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): Raw textual content of the requested file
    """
    return {
        "content": "name = \"example-project\"\nversion = \"1.0.0\"\n[dependencies]\nnumpy = \"^1.21\"\npandas = \"^1.3\""
    }


def project_ingest_mcp_server_file_content(project: str, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the content of specific files from a project.

    Args:
        project (str): The path of the project (required)
        file_path (str, optional): Path to file within the project

    Returns:
        Dict[str, Any]: A dictionary containing the raw textual content of the requested file.
            - content (str): Raw textual content of the requested file, preserving original formatting
    """
    if not project:
        raise ValueError("Parameter 'project' is required and cannot be empty.")

    # Simulate calling external API to get file content
    api_data = call_external_api("project-ingest-mcp-server-file_content", **locals())

    # Construct result matching output schema
    result = {
        "content": api_data["content"]
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
