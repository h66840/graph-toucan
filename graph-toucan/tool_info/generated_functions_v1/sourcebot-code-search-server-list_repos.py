from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for listing repositories.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - repository_0_name (str): Name of the first repository
        - repository_0_description (str): Description of the first repository
        - repository_0_url (str): URL of the first repository
        - repository_0_created_at (str): Creation timestamp of the first repository
        - repository_0_updated_at (str): Last updated timestamp of the first repository
        - repository_0_visibility (str): Visibility of the first repository ('public' or 'private')
        - repository_1_name (str): Name of the second repository
        - repository_1_description (str): Description of the second repository
        - repository_1_url (str): URL of the second repository
        - repository_1_created_at (str): Creation timestamp of the second repository
        - repository_1_updated_at (str): Last updated timestamp of the second repository
        - repository_1_visibility (str): Visibility of the second repository ('public' or 'private')
        - total_count (int): Total number of repositories returned
        - has_more (bool): Whether more repositories are available beyond this response
        - metadata_timestamp (str): Timestamp of the request
        - metadata_organization (str): Organization context for the request
    """
    return {
        "repository_0_name": "frontend-app",
        "repository_0_description": "Main frontend application using React",
        "repository_0_url": "https://github.com/myorg/frontend-app",
        "repository_0_created_at": "2022-01-15T09:30:00Z",
        "repository_0_updated_at": "2023-05-20T14:22:10Z",
        "repository_0_visibility": "public",
        "repository_1_name": "backend-service",
        "repository_1_description": "Core backend microservice with Flask",
        "repository_1_url": "https://github.com/myorg/backend-service",
        "repository_1_created_at": "2021-11-03T13:15:00Z",
        "repository_1_updated_at": "2023-06-01T08:45:33Z",
        "repository_1_visibility": "private",
        "total_count": 2,
        "has_more": False,
        "metadata_timestamp": "2023-06-15T10:00:00Z",
        "metadata_organization": "myorg"
    }

def sourcebot_code_search_server_list_repos() -> Dict[str, Any]:
    """
    Lists all repositories in the organization.

    This function retrieves repository information by calling an external API
    and formats the response according to the expected schema. If authentication
    fails, the user should set the SOURCEBOT_API_KEY environment variable.

    Returns:
        Dict containing:
        - repositories (List[Dict]): List of repository objects with name, description,
          URL, creation date, last updated time, and visibility
        - total_count (int): Total number of repositories returned
        - has_more (bool): Indicates if more repositories are available
        - metadata (Dict): Additional contextual information including timestamp
          and organization context

    Raises:
        RuntimeError: If there is an authentication issue (simulated)
    """
    try:
        api_data = call_external_api("sourcebot-code-search-server-list_repos")
        
        repositories = [
            {
                "name": api_data["repository_0_name"],
                "description": api_data["repository_0_description"],
                "url": api_data["repository_0_url"],
                "created_at": api_data["repository_0_created_at"],
                "updated_at": api_data["repository_0_updated_at"],
                "visibility": api_data["repository_0_visibility"]
            },
            {
                "name": api_data["repository_1_name"],
                "description": api_data["repository_1_description"],
                "url": api_data["repository_1_url"],
                "created_at": api_data["repository_1_created_at"],
                "updated_at": api_data["repository_1_updated_at"],
                "visibility": api_data["repository_1_visibility"]
            }
        ]
        
        result = {
            "repositories": repositories,
            "total_count": api_data["total_count"],
            "has_more": api_data["has_more"],
            "metadata": {
                "timestamp": api_data["metadata_timestamp"],
                "organization": api_data["metadata_organization"]
            }
        }
        
        return result
        
    except Exception as e:
        # In a real implementation, we might check for specific auth errors
        # Here we simulate the guidance about SOURCEBOT_API_KEY
        raise RuntimeError(
            "Failed to list repositories. Please ensure you have set the SOURCEBOT_API_KEY environment variable."
        ) from e