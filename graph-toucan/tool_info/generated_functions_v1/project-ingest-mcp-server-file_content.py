from typing import Dict, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
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
    api_data = call_external_api("project-ingest-mcp-server-file_content")

    # Construct result matching output schema
    result = {
        "content": api_data["content"]
    }

    return result