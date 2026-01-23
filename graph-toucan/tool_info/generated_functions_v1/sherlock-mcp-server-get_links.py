from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for username search using Sherlock.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - username (str): The username that was searched
        - result_0_site (str): Name of the first platform where the username was found
        - result_0_url (str): URL of the profile on the first platform
        - result_1_site (str): Name of the second platform where the username was found
        - result_1_url (str): URL of the profile on the second platform
        - count (int): Total number of platforms where the username was found
    """
    return {
        "username": "testuser",
        "result_0_site": "GitHub",
        "result_0_url": "https://github.com/testuser",
        "result_1_site": "Twitter",
        "result_1_url": "https://twitter.com/testuser",
        "count": 2
    }

def sherlock_mcp_server_get_links(username: str) -> Dict[str, Any]:
    """
    Search for a username across multiple social media platforms using Sherlock.
    
    Args:
        username (str): The username to search for across social media platforms.
        
    Returns:
        Dict containing:
        - username (str): the username that was searched
        - results (List[Dict]): list of dictionaries with 'site' and 'url' keys for each platform found
        - count (int): total number of platforms where the username was found
    
    Example:
        >>> sherlock_mcp_server_get_links("testuser")
        {
            'username': 'testuser',
            'results': [
                {'site': 'GitHub', 'url': 'https://github.com/testuser'},
                {'site': 'Twitter', 'url': 'https://twitter.com/testuser'}
            ],
            'count': 2
        }
    """
    if not username or not username.strip():
        return {
            "username": "",
            "results": [],
            "count": 0
        }
    
    # Call external API to get the data
    api_data = call_external_api("sherlock-mcp-server-get_links")
    
    # Construct results list from indexed fields
    results = []
    for i in range(2):  # We expect up to 2 results based on call_external_api
        site_key = f"result_{i}_site"
        url_key = f"result_{i}_url"
        if site_key in api_data and url_key in api_data and api_data[site_key] and api_data[url_key]:
            results.append({
                "site": api_data[site_key],
                "url": api_data[url_key]
            })
    
    # Use the username from input, fallback to api_data only if input is empty
    search_username = username.strip()
    
    return {
        "username": search_username,
        "results": results,
        "count": api_data["count"]
    }