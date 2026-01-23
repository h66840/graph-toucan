from typing import Dict, List, Any, Optional

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching changelog and release data from external API for npm packages.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - queryPackages_0 (str): First queried package name
        - queryPackages_1 (str): Second queried package name
        - results_0_packageInput (str): Original input string for first package
        - results_0_packageName (str): Resolved name of first package
        - results_0_status (str): Status of analysis for first package ('success' or 'error')
        - results_0_error (str | None): Error message if failed, else None
        - results_0_message (str): Human-readable summary for first package
        - results_0_repositoryUrl (str | None): Repository URL for first package
        - results_0_changelogSourceUrl (str | None): Changelog source URL for first package
        - results_0_changelogContent (str | None): Full changelog text for first package
        - results_0_hasChangelogFile (bool): Whether changelog file exists for first package
        - results_0_githubReleases_0_tag_name (str): First GitHub release tag for first package
        - results_0_githubReleases_0_name (str): First GitHub release name for first package
        - results_0_githubReleases_0_published_at (str): First GitHub release timestamp for first package
        - results_0_githubReleases_1_tag_name (str): Second GitHub release tag for first package
        - results_0_githubReleases_1_name (str): Second GitHub release name for first package
        - results_0_githubReleases_1_published_at (str): Second GitHub release timestamp for first package
        - results_0_npmVersionHistory_totalVersions (int): Total versions on npm for first package
        - results_0_npmVersionHistory_latestVersion (str): Latest version on npm for first package
        - results_0_npmVersionHistory_firstVersion (str): First version on npm for first package
        - results_1_packageInput (str): Original input string for second package
        - results_1_packageName (str): Resolved name of second package
        - results_1_status (str): Status of analysis for second package ('success' or 'error')
        - results_1_error (str | None): Error message if failed, else None
        - results_1_message (str): Human-readable summary for second package
        - results_1_repositoryUrl (str | None): Repository URL for second package
        - results_1_changelogSourceUrl (str | None): Changelog source URL for second package
        - results_1_changelogContent (str | None): Full changelog text for second package
        - results_1_hasChangelogFile (bool): Whether changelog file exists for second package
        - results_1_githubReleases_0_tag_name (str): First GitHub release tag for second package
        - results_1_githubReleases_0_name (str): First GitHub release name for second package
        - results_1_githubReleases_0_published_at (str): First GitHub release timestamp for second package
        - results_1_githubReleases_1_tag_name (str): Second GitHub release tag for second package
        - results_1_githubReleases_1_name (str): Second GitHub release name for second package
        - results_1_githubReleases_1_published_at (str): Second GitHub release timestamp for second package
        - results_1_npmVersionHistory_totalVersions (int): Total versions on npm for second package
        - results_1_npmVersionHistory_latestVersion (str): Latest version on npm for second package
        - results_1_npmVersionHistory_firstVersion (str): First version on npm for second package
    """
    return {
        "queryPackages_0": "express",
        "queryPackages_1": "lodash",
        "results_0_packageInput": "express",
        "results_0_packageName": "express",
        "results_0_status": "success",
        "results_0_error": None,
        "results_0_message": "Successfully retrieved changelog and release data",
        "results_0_repositoryUrl": "https://github.com/expressjs/express",
        "results_0_changelogSourceUrl": "https://github.com/expressjs/express/blob/main/History.md",
        "results_0_changelogContent": "## 4.18.2\n- Fix: security vulnerability in dependency\n## 4.18.1\n- Fix: minor bug in routing",
        "results_0_hasChangelogFile": True,
        "results_0_githubReleases_0_tag_name": "4.18.2",
        "results_0_githubReleases_0_name": "Release 4.18.2",
        "results_0_githubReleases_0_published_at": "2023-09-15T10:00:00Z",
        "results_0_githubReleases_1_tag_name": "4.18.1",
        "results_0_githubReleases_1_name": "Release 4.18.1",
        "results_0_githubReleases_1_published_at": "2023-08-20T09:30:00Z",
        "results_0_npmVersionHistory_totalVersions": 156,
        "results_0_npmVersionHistory_latestVersion": "4.18.2",
        "results_0_npmVersionHistory_firstVersion": "0.1.0",
        "results_1_packageInput": "lodash",
        "results_1_packageName": "lodash",
        "results_1_status": "success",
        "results_1_error": None,
        "results_1_message": "Successfully retrieved changelog and release data",
        "results_1_repositoryUrl": "https://github.com/lodash/lodash",
        "results_1_changelogSourceUrl": "https://github.com/lodash/lodash/releases",
        "results_1_changelogContent": "## v4.17.21\n- Update: security patches\n## v4.17.20\n- Fix: minor performance issue",
        "results_1_hasChangelogFile": True,
        "results_1_githubReleases_0_tag_name": "v4.17.21",
        "results_1_githubReleases_0_name": "Version 4.17.21",
        "results_1_githubReleases_0_published_at": "2023-10-05T14:20:00Z",
        "results_1_githubReleases_1_tag_name": "v4.17.20",
        "results_1_githubReleases_1_name": "Version 4.17.20",
        "results_1_githubReleases_1_published_at": "2023-07-10T11:45:00Z",
        "results_1_npmVersionHistory_totalVersions": 532,
        "results_1_npmVersionHistory_latestVersion": "4.17.21",
        "results_1_npmVersionHistory_firstVersion": "0.1.0"
    }

def npm_sentinel_mcp_npmChangelogAnalysis(packages: List[str]) -> Dict[str, Any]:
    """
    Analyze changelog and release history of npm packages.
    
    Args:
        packages (List[str]): List of package names to analyze changelogs for
        
    Returns:
        Dict containing:
        - queryPackages (List[str]): list of package names that were queried
        - results (List[Dict]): list of result objects for each package with detailed data
          Each result contains:
          - packageInput (str): original input string for the package
          - packageName (str): resolved name of the package
          - status (str): status of the analysis ('success' or 'error')
          - error (str | None): error message if the analysis failed
          - message (str): human-readable summary of the result
          - data (Dict): detailed changelog and release data including:
            - repositoryUrl (str | None): URL to the source repository
            - changelogSourceUrl (str | None): URL where changelog was retrieved from
            - changelogContent (str | None): full text content of the changelog
            - hasChangelogFile (bool): whether a changelog file was found
            - githubReleases (List[Dict]): list of GitHub releases with tag_name, name, published_at
            - npmVersionHistory (Dict): version history metadata from npm with totalVersions, latestVersion, firstVersion
    """
    if not packages:
        return {
            "queryPackages": [],
            "results": []
        }
    
    # Call external API to get simulated data
    api_data = call_external_api("npm-sentinel-mcp-npmChangelogAnalysis", **locals())
    
    # Extract query packages from API response (only first two)
    query_packages = []
    for i in range(2):
        key = f"queryPackages_{i}"
        if key in api_data and api_data[key] is not None:
            query_packages.append(api_data[key])
    
    # Build results list
    results = []
    for i in range(2):
        result = {
            "packageInput": api_data.get(f"results_{i}_packageInput"),
            "packageName": api_data.get(f"results_{i}_packageName"),
            "status": api_data.get(f"results_{i}_status"),
            "error": api_data.get(f"results_{i}_error"),
            "message": api_data.get(f"results_{i}_message"),
            "data": {
                "repositoryUrl": api_data.get(f"results_{i}_repositoryUrl"),
                "changelogSourceUrl": api_data.get(f"results_{i}_changelogSourceUrl"),
                "changelogContent": api_data.get(f"results_{i}_changelogContent"),
                "hasChangelogFile": api_data.get(f"results_{i}_hasChangelogFile", False),
                "githubReleases": [],
                "npmVersionHistory": {
                    "totalVersions": api_data.get(f"results_{i}_npmVersionHistory_totalVersions", 0),
                    "latestVersion": api_data.get(f"results_{i}_npmVersionHistory_latestVersion"),
                    "firstVersion": api_data.get(f"results_{i}_npmVersionHistory_firstVersion")
                }
            }
        }
        
        # Add GitHub releases
        for j in range(2):
            tag_name = api_data.get(f"results_{i}_githubReleases_{j}_tag_name")
            if tag_name is not None:
                result["data"]["githubReleases"].append({
                    "tag_name": tag_name,
                    "name": api_data.get(f"results_{i}_githubReleases_{j}_name"),
                    "published_at": api_data.get(f"results_{i}_githubReleases_{j}_published_at")
                })
        
        results.append(result)
    
    return {
        "queryPackages": query_packages,
        "results": results
    }

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
