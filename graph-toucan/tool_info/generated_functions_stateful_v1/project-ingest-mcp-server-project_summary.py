from typing import Dict, Any
import os

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
    Simulates fetching data from external API for project summary.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - project (str): Name of the project or directory being analyzed
        - num_files (int): Number of files in the project that were analyzed
        - token_count (str): Estimated total token count in the repository, formatted as a string with unit (e.g., "56.6k")
        - raw (str): Raw textual summary including directory info, file count, and token estimate, formatted for display
    """
    return {
        "project": "sample-project",
        "num_files": 42,
        "token_count": "56.6k",
        "raw": "Project: sample-project\nFiles analyzed: 42\nEstimated tokens: 56.6k\nSummary: This is a sample project with various source files and documentation."
    }

def project_ingest_mcp_server_project_summary(project: str) -> Dict[str, Any]:
    """
    Get a summary of a project that includes project name, files in project,
    number of tokens in repo, and summary from the README.md.
    
    Args:
        project (str): The path of the project to analyze
        
    Returns:
        Dict[str, Any]: A dictionary containing:
            - project (str): name of the project or directory being analyzed
            - num_files (int): number of files in the project that were analyzed
            - token_count (str): estimated total token count in the repository, formatted as a string with unit (e.g., "56.6k")
            - raw (str): raw textual summary including directory info, file count, and token estimate, formatted for display
    
    Raises:
        ValueError: If project path is empty or invalid
        FileNotFoundError: If the project directory does not exist
    """
    if not project:
        raise ValueError("Project path cannot be empty")
    
    if not os.path.exists(project):
        raise FileNotFoundError(f"Project directory not found: {project}")
    
    if not os.path.isdir(project):
        raise ValueError(f"Project path is not a directory: {project}")
    
    # Call external API to get project summary data
    api_data = call_external_api("project-ingest-mcp-server-project_summary", **locals())
    
    # Extract base name of the project directory
    project_name = os.path.basename(os.path.abspath(project))
    
    # Use the data from the API call instead of performing local file operations
    # This maintains the same interface while removing dangerous operations
    return {
        "project": project_name,
        "num_files": api_data["num_files"],
        "token_count": api_data["token_count"],
        "raw": f"Project: {project_name}\n"
               f"Files analyzed: {api_data['num_files']}\n"
               f"Estimated tokens: {api_data['token_count']}\n"
               f"Summary: This is a sample project with various source files and documentation."
    }

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
