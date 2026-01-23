from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for username search across social media platforms.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - username (str): The username that was searched
        - result_0_site (str): Name of the first platform where username was found
        - result_0_url (str): URL of the profile on the first platform
        - result_1_site (str): Name of the second platform where username was found
        - result_1_url (str): URL of the profile on the second platform
        - count (int): Total number of platform profiles found for the username
    """
    return {
        "username": "testuser",
        "result_0_site": "GitHub",
        "result_0_url": "https://github.com/testuser",
        "result_1_site": "Twitter",
        "result_1_url": "https://twitter.com/testuser",
        "count": 2
    }

def sherlock_mcp_server_get_nsfw_links(username: str) -> Dict[str, Any]:
    """
    Search for a username across multiple social media platforms including NSFW platforms using Sherlock.
    
    Args:
        username (str): The username to search for across social media platforms including NSFW platforms.
        
    Returns:
        Dict containing:
        - username (str): the username that was searched across social media platforms
        - results (List[Dict]): list of dictionaries containing 'site' (str) and 'url' (str) 
          for each platform where the username was found
        - count (int): total number of platform profiles found for the username
    
    Example:
        >>> sherlock_mcp_server_get_nsfw_links("testuser")
        {
            'username': 'testuser',
            'results': [
                {'site': 'GitHub', 'url': 'https://github.com/testuser'},
                {'site': 'Twitter', 'url': 'https://twitter.com/testuser'}
            ],
            'count': 2
        }
    """
    if not username:
        return {
            "username": "",
            "results": [],
            "count": 0
        }
    
    # Call external API to get data
    api_data = call_external_api("sherlock-mcp-server-get_nsfw_links")
    
    # Construct results list from indexed fields
    results = [
        {
            "site": api_data["result_0_site"],
            "url": api_data["result_0_url"]
        },
        {
            "site": api_data["result_1_site"],
            "url": api_data["result_1_url"]
        }
    ]
    
    # Return structured response matching output schema
    return {
        "username": username,
        "results": results,
        "count": api_data["count"]
    }