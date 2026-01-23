from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for NPM repository statistics.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - queryPackages_0 (str): First package name queried
        - queryPackages_1 (str): Second package name queried
        - results_0_packageInput (str): Original input string for first package
        - results_0_packageName (str): Resolved name of first NPM package
        - results_0_status (str): Status of request for first package
        - results_0_error (str or null): Error message if failed, else null
        - results_0_message (str): Detailed message about outcome for first package
        - results_0_data_githubRepoUrl (str): GitHub repo URL for first package
        - results_0_data_stars (int): Number of stars for first package repo
        - results_0_data_forks (int): Number of forks for first package repo
        - results_0_data_openIssues (int): Number of open issues for first package repo
        - results_0_data_watchers (int): Number of watchers for first package repo
        - results_0_data_createdAt (str): ISO 8601 timestamp when first repo was created
        - results_0_data_updatedAt (str): ISO 8601 timestamp of last update to first repo
        - results_0_data_defaultBranch (str): Default branch name for first repo
        - results_0_data_hasWiki (bool): Whether first repo has wiki enabled
        - results_0_data_topics_0 (str): First topic for first repo
        - results_0_data_topics_1 (str): Second topic for first repo
        - results_1_packageInput (str): Original input string for second package
        - results_1_packageName (str): Resolved name of second NPM package
        - results_1_status (str): Status of request for second package
        - results_1_error (str or null): Error message if failed, else null
        - results_1_message (str): Detailed message about outcome for second package
        - results_1_data_githubRepoUrl (str): GitHub repo URL for second package
        - results_1_data_stars (int): Number of stars for second package repo
        - results_1_data_forks (int): Number of forks for second package repo
        - results_1_data_openIssues (int): Number of open issues for second package repo
        - results_1_data_watchers (int): Number of watchers for second package repo
        - results_1_data_createdAt (str): ISO 8601 timestamp when second repo was created
        - results_1_data_updatedAt (str): ISO 8601 timestamp of last update to second repo
        - results_1_data_defaultBranch (str): Default branch name for second repo
        - results_1_data_hasWiki (bool): Whether second repo has wiki enabled
        - results_1_data_topics_0 (str): First topic for second repo
        - results_1_data_topics_1 (str): Second topic for second repo
        - message (str): Summary message about the analysis
    """
    return {
        "queryPackages_0": "express",
        "queryPackages_1": "lodash",
        "results_0_packageInput": "express",
        "results_0_packageName": "express",
        "results_0_status": "success",
        "results_0_error": None,
        "results_0_message": "Successfully fetched repository statistics",
        "results_0_data_githubRepoUrl": "https://github.com/expressjs/express",
        "results_0_data_stars": 58000,
        "results_0_data_forks": 16000,
        "results_0_data_openIssues": 450,
        "results_0_data_watchers": 2300,
        "results_0_data_createdAt": "2010-06-15T14:25:00Z",
        "results_0_data_updatedAt": "2023-11-10T08:30:00Z",
        "results_0_data_defaultBranch": "master",
        "results_0_data_hasWiki": True,
        "results_0_data_topics_0": "nodejs",
        "results_0_data_topics_1": "web-framework",
        "results_1_packageInput": "lodash",
        "results_1_packageName": "lodash",
        "results_1_status": "success",
        "results_1_error": None,
        "results_1_message": "Successfully fetched repository statistics",
        "results_1_data_githubRepoUrl": "https://github.com/lodash/lodash",
        "results_1_data_stars": 53000,
        "results_1_data_forks": 5000,
        "results_1_data_openIssues": 120,
        "results_1_data_watchers": 1200,
        "results_1_data_createdAt": "2012-03-10T11:15:00Z",
        "results_1_data_updatedAt": "2023-11-09T16:45:00Z",
        "results_1_data_defaultBranch": "master",
        "results_1_data_hasWiki": False,
        "results_1_data_topics_0": "utility",
        "results_1_data_topics_1": "javascript",
        "message": "Processed 2 packages and retrieved repository statistics for all of them"
    }

def npm_sentinel_mcp_npmRepoStats(packages: List[str]) -> Dict[str, Any]:
    """
    Get repository statistics for NPM packages.
    
    Args:
        packages (List[str]): List of package names to get repository stats for
        
    Returns:
        Dict containing:
        - queryPackages (List[str]): list of package names that were queried
        - results (List[Dict]): list of result objects for each package with status, data, and messages
        - message (str): summary message about the analysis
        
        Each result contains:
        - packageInput (str): original input string for the package
        - packageName (str): resolved name of the NPM package
        - status (str): status of the request ('success' or other)
        - error (str or null): error message if failed, otherwise null
        - message (str): detailed message about the outcome
        - data (Dict): GitHub repository statistics including url, stars, forks, issues, etc.
    """
    if not packages:
        return {
            "queryPackages": [],
            "results": [],
            "message": "No packages provided for analysis"
        }
    
    # Call external API to get data (simulated)
    api_data = call_external_api("npm-sentinel-mcp-npmRepoStats")
    
    # Extract query packages
    query_packages = []
    for i in range(2):
        key = f"queryPackages_{i}"
        if key in api_data and api_data[key] is not None:
            query_packages.append(api_data[key])
    
    # Build results list by reconstructing nested structure
    results = []
    for i in range(2):
        pkg_key = f"results_{i}_packageName"
        if pkg_key not in api_data or api_data[pkg_key] is None:
            continue
            
        # Reconstruct topics list
        topics = []
        for j in range(2):
            topic_key = f"results_{i}_data_topics_{j}"
            if topic_key in api_data and api_data[topic_key] is not None:
                topics.append(api_data[topic_key])
        
        # Reconstruct data object
        data = {
            "githubRepoUrl": api_data.get(f"results_{i}_data_githubRepoUrl"),
            "stars": api_data.get(f"results_{i}_data_stars"),
            "forks": api_data.get(f"results_{i}_data_forks"),
            "openIssues": api_data.get(f"results_{i}_data_openIssues"),
            "watchers": api_data.get(f"results_{i}_data_watchers"),
            "createdAt": api_data.get(f"results_{i}_data_createdAt"),
            "updatedAt": api_data.get(f"results_{i}_data_updatedAt"),
            "defaultBranch": api_data.get(f"results_{i}_data_defaultBranch"),
            "hasWiki": api_data.get(f"results_{i}_data_hasWiki"),
            "topics": topics
        }
        
        # Reconstruct result object
        result = {
            "packageInput": api_data.get(f"results_{i}_packageInput"),
            "packageName": api_data.get(f"results_{i}_packageName"),
            "status": api_data.get(f"results_{i}_status"),
            "error": api_data.get(f"results_{i}_error"),
            "message": api_data.get(f"results_{i}_message"),
            "data": data
        }
        results.append(result)
    
    # Use provided packages if available, otherwise use those from API
    final_query_packages = packages if packages else query_packages
    
    # Generate message
    success_count = sum(1 for r in results if r["status"] == "success")
    total_count = len(final_query_packages)