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
    Simulates fetching data from external API for file source retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - file (str): Path of the file within the repository
        - repository (str): Full identifier of the repository in "host.com/owner/repo" format
        - language (str): Programming language of the file
        - source (str): Full source code content of the file
    """
    return {
        "file": "src/main.py",
        "repository": "github.com/user/project",
        "language": "python",
        "source": 'def hello():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    hello()\n'
    }

def sourcebot_code_search_server_get_file_source(fileName: str, repoId: str) -> Dict[str, Any]:
    """
    Fetches the source code for a given file from a specified repository.
    
    Args:
        fileName (str): The file to fetch the source code for.
        repoId (str): The repository to fetch the source code for. This is the Sourcebot compatible repository ID.
    
    Returns:
        Dict[str, Any]: A dictionary containing the file path, repository identifier, language, and source code.
            - file (str): Path of the file within the repository
            - repository (str): Full identifier of the repository in "host.com/owner/repo" format
            - language (str): Programming language of the file
            - source (str): Full source code content of the file
    
    Raises:
        ValueError: If fileName or repoId is empty or not provided.
        EnvironmentError: If authentication fails (simulated by checking for missing repoId pattern).
    """
    if not fileName:
        raise ValueError("fileName is required but was not provided.")
    if not repoId:
        raise ValueError("repoId is required but was not provided.")
    
    # Simulate authentication check
    if "invalid" in repoId.lower() or "error" in repoId.lower():
        raise EnvironmentError(
            "Authentication failed. Please set the SOURCEBOT_API_KEY environment variable."
        )
    
    api_data = call_external_api("sourcebot-code-search-server-get_file_source", **locals())
    
    # Construct result matching output schema
    result = {
        "file": api_data["file"],
        "repository": api_data["repository"],
        "language": api_data["language"],
        "source": api_data["source"]
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
