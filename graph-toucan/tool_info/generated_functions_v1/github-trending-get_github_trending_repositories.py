from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for GitHub trending repositories.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - repository_0_name (str): Name of the first trending repository
        - repository_0_fullname (str): Full name (owner/name) of the first repository
        - repository_0_url (str): URL of the first repository
        - repository_0_description (str): Description of the first repository
        - repository_0_language (str): Primary language of the first repository
        - repository_0_stars (int): Total stars of the first repository
        - repository_0_forks (int): Total forks of the first repository
        - repository_0_current_period_stars (int): Stars gained in current period for first repo
        - repository_1_name (str): Name of the second trending repository
        - repository_1_fullname (str): Full name (owner/name) of the second repository
        - repository_1_url (str): URL of the second repository
        - repository_1_description (str): Description of the second repository
        - repository_1_language (str): Primary language of the second repository
        - repository_1_stars (int): Total stars of the second repository
        - repository_1_forks (int): Total forks of the second repository
        - repository_1_current_period_stars (int): Stars gained in current period for second repo
    """
    return {
        "repository_0_name": "awesome-python",
        "repository_0_fullname": "vinta/awesome-python",
        "repository_0_url": "https://github.com/vinta/awesome-python",
        "repository_0_description": "A curated list of awesome Python frameworks, libraries, software and resources",
        "repository_0_language": "Python",
        "repository_0_stars": 157000,
        "repository_0_forks": 25000,
        "repository_0_current_period_stars": 1200,
        "repository_1_name": "react",
        "repository_1_fullname": "facebook/react",
        "repository_1_url": "https://github.com/facebook/react",
        "repository_1_description": "A declarative, efficient, and flexible JavaScript library for building user interfaces",
        "repository_1_language": "JavaScript",
        "repository_1_stars": 205000,
        "repository_1_forks": 38000,
        "repository_1_current_period_stars": 950,
    }

def github_trending_get_github_trending_repositories(
    language: Optional[str] = None,
    since: Optional[str] = None,
    spoken_language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get trending repositories on GitHub based on optional filters.
    
    Args:
        language (Optional[str]): Filter repositories by programming language
        since (Optional[str]): Time period to filter by (e.g., 'daily', 'weekly', 'monthly')
        spoken_language (Optional[str]): Filter by spoken language (e.g., 'en', 'zh')
    
    Returns:
        Dict containing a list of trending GitHub repositories with details:
        - repositories (List[Dict]): List of repository dictionaries containing:
            - name (str): Repository name
            - fullname (str): Full repository name (owner/name)
            - url (str): Repository URL
            - description (str): Repository description
            - language (str): Primary programming language
            - stars (int): Total number of stars
            - forks (int): Total number of forks
            - current_period_stars (int): Stars gained in the current period
    
    Note:
        This function simulates API behavior and returns mock data. In a real implementation,
        it would make actual HTTP requests to GitHub's trending data source.
    """
    # Validate input parameters
    valid_since_values = ['daily', 'weekly', 'monthly']
    if since is not None and since not in valid_since_values:
        raise ValueError(f"Parameter 'since' must be one of {valid_since_values} if provided")
    
    # Call external API to get flattened data
    api_data = call_external_api("github-trending-get_github_trending_repositories")
    
    # Construct repositories list from flattened API data
    repositories = [
        {
            "name": api_data["repository_0_name"],
            "fullname": api_data["repository_0_fullname"],
            "url": api_data["repository_0_url"],
            "description": api_data["repository_0_description"],
            "language": api_data["repository_0_language"],
            "stars": api_data["repository_0_stars"],
            "forks": api_data["repository_0_forks"],
            "current_period_stars": api_data["repository_0_current_period_stars"]
        },
        {
            "name": api_data["repository_1_name"],
            "fullname": api_data["repository_1_fullname"],
            "url": api_data["repository_1_url"],
            "description": api_data["repository_1_description"],
            "language": api_data["repository_1_language"],
            "stars": api_data["repository_1_stars"],
            "forks": api_data["repository_1_forks"],
            "current_period_stars": api_data["repository_1_current_period_stars"]
        }
    ]
    
    # Apply language filter if specified
    if language is not None:
        repositories = [
            repo for repo in repositories
            if repo["language"].lower() == language.lower()
        ]
    
    # Return result in expected format
    return {
        "repositories": repositories
    }