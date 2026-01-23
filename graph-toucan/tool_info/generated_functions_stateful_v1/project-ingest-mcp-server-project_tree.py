from typing import Dict, Any

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
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - tree_structure (str): textual representation of the project's directory tree
    """
    return {
        "tree_structure": "project/\n├── src/\n│   ├── main.py\n│   └── utils.py\n├── tests/\n│   └── test_main.py\n└── README.md"
    }

def project_ingest_mcp_server_project_tree(project: str) -> Dict[str, Any]:
    """
    Get the tree structure of a project.
    
    Args:
        project (str): The path of the project
        
    Returns:
        Dict[str, Any]: A dictionary containing the tree structure of the project
            - tree_structure (str): textual representation of the project's directory tree, including files and subdirectories in a hierarchical format
    
    Raises:
        ValueError: If project path is empty or not a string
        FileNotFoundError: If the project path does not exist
        NotADirectoryError: If the project path is not a directory
    """
    if not project:
        raise ValueError("Project path cannot be empty")
    
    if not isinstance(project, str):
        raise ValueError("Project path must be a string")
    
    # Instead of checking actual file system paths with os, we simulate the behavior
    # using the external API call since the original function was already using
    # call_external_api for the actual data retrieval
    api_data = call_external_api("project-ingest-mcp-server-project_tree", **locals())
    
    return {
        "tree_structure": api_data["tree_structure"]
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
