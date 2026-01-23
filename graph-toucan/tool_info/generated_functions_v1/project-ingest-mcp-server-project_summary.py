from typing import Dict, Any
import os

def call_external_api(tool_name: str) -> Dict[str, Any]:
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
    api_data = call_external_api("project-ingest-mcp-server-project_summary")
    
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