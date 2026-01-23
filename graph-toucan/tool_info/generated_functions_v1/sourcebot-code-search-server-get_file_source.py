from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
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
    
    api_data = call_external_api("sourcebot-code-search-server-get_file_source")
    
    # Construct result matching output schema
    result = {
        "file": api_data["file"],
        "repository": api_data["repository"],
        "language": api_data["language"],
        "source": api_data["source"]
    }
    
    return result