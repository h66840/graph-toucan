from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
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
    api_data = call_external_api("project-ingest-mcp-server-project_tree")
    
    return {
        "tree_structure": api_data["tree_structure"]
    }