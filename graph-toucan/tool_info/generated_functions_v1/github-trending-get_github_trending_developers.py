from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for GitHub trending developers.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - developer_0_username (str): Username of the first trending developer
        - developer_0_name (str): Full name of the first trending developer
        - developer_0_url (str): Profile URL of the first trending developer
        - developer_0_avatar (str): Avatar image URL of the first trending developer
        - developer_0_repo_name (str): Name of the trending repository by the first developer
        - developer_0_repo_description (str): Description of the trending repository by the first developer
        - developer_0_repo_url (str): URL of the trending repository by the first developer
        - developer_1_username (str): Username of the second trending developer
        - developer_1_name (str): Full name of the second trending developer
        - developer_1_url (str): Profile URL of the second trending developer
        - developer_1_avatar (str): Avatar image URL of the second trending developer
        - developer_1_repo_name (str): Name of the trending repository by the second developer
        - developer_1_repo_description (str): Description of the trending repository by the second developer
        - developer_1_repo_url (str): URL of the trending repository by the second developer
    """
    return {
        "developer_0_username": "alice_dev",
        "developer_0_name": "Alice Johnson",
        "developer_0_url": "https://github.com/alice_dev",
        "developer_0_avatar": "https://github.com/alice_dev.png",
        "developer_0_repo_name": "awesome-python-tools",
        "developer_0_repo_description": "A collection of useful Python utilities and scripts.",
        "developer_0_repo_url": "https://github.com/alice_dev/awesome-python-tools",
        "developer_1_username": "bob_codes",
        "developer_1_name": "Bob Smith",
        "developer_1_url": "https://github.com/bob_codes",
        "developer_1_avatar": "https://github.com/bob_codes.png",
        "developer_1_repo_name": "react-hooks-guide",
        "developer_1_repo_description": "Comprehensive guide to React hooks with examples.",
        "developer_1_repo_url": "https://github.com/bob_codes/react-hooks-guide",
    }


def github_trending_get_github_trending_developers(
    language: Optional[str] = None,
    since: Optional[str] = None,
    spoken_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get trending developers on GitHub based on optional filters.

    Args:
        language (Optional[str]): Programming language to filter repositories by (e.g., 'python', 'javascript').
        since (Optional[str]): Time period to filter repositories by ('daily', 'weekly', 'monthly').
        spoken_language (Optional[str]): Spoken language to filter repositories by (e.g., 'en', 'zh').

    Returns:
        Dict containing a list of trending developers with their details:
        - developers (List[Dict]): List of developers, each containing:
            - username (str): GitHub username
            - name (str): Full name of the developer
            - url (str): GitHub profile URL
            - avatar (str): Avatar image URL
            - repo (Dict): Information about the trending repository:
                - name (str): Repository name
                - description (str): Repository description
                - url (str): Repository URL

    Note:
        This is a simulated implementation. In a real scenario, it would fetch data from GitHub's API.
        The input parameters are used for filtering in actual implementations but are not applied here
        as the data is mocked.
    """
    # Fetch simulated external data
    api_data = call_external_api("github-trending-get_github_trending_developers")

    # Construct the developers list from flattened API response
    developers = [
        {
            "username": api_data["developer_0_username"],
            "name": api_data["developer_0_name"],
            "url": api_data["developer_0_url"],
            "avatar": api_data["developer_0_avatar"],
            "repo": {
                "name": api_data["developer_0_repo_name"],
                "description": api_data["developer_0_repo_description"],
                "url": api_data["developer_0_repo_url"]
            }
        },
        {
            "username": api_data["developer_1_username"],
            "name": api_data["developer_1_name"],
            "url": api_data["developer_1_url"],
            "avatar": api_data["developer_1_avatar"],
            "repo": {
                "name": api_data["developer_1_repo_name"],
                "description": api_data["developer_1_repo_description"],
                "url": api_data["developer_1_repo_url"]
            }
        }
    ]

    return {"developers": developers}