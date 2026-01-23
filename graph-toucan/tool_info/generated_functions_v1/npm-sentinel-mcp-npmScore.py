from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for npm package scores.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - queryPackages_0 (str): First queried package name
        - queryPackages_1 (str): Second queried package name
        - results_0_packageInput (str): Original input for first package
        - results_0_packageName (str): Resolved name of first package
        - results_0_status (str): Status of first package ('success' or 'failure')
        - results_0_error (str or None): Error message if failed, else None
        - results_0_analyzedAt (str): ISO timestamp when analysis was done
        - results_0_versionInScore (str): Version of first package that was scored
        - results_0_score_final (float): Final score of first package
        - results_0_score_detail_quality (float): Quality score of first package
        - results_0_score_detail_popularity (float): Popularity score of first package
        - results_0_score_detail_maintenance (float): Maintenance score of first package
        - results_0_packageInfoFromScore_name (str): Name from score data of first package
        - results_0_packageInfoFromScore_version (str): Version from score data of first package
        - results_0_packageInfoFromScore_description (str): Description of first package
        - results_0_npmStats_downloadsLastMonth (int): Monthly downloads of first package
        - results_0_npmStats_starsCount (int): Stars count on npm for first package
        - results_0_githubStats_starsCount (int): GitHub stars for first package
        - results_0_githubStats_forksCount (int): GitHub forks for first package
        - results_0_githubStats_subscribersCount (int): GitHub subscribers for first package
        - results_0_githubStats_issues_count (int): Total GitHub issues for first package
        - results_0_githubStats_issues_openCount (int): Open GitHub issues for first package
        - results_0_message (str): Message about result of first package
        - results_1_packageInput (str): Original input for second package
        - results_1_packageName (str): Resolved name of second package
        - results_1_status (str): Status of second package ('success' or 'failure')
        - results_1_error (str or None): Error message if failed, else None
        - results_1_analyzedAt (str): ISO timestamp when analysis was done
        - results_1_versionInScore (str): Version of second package that was scored
        - results_1_score_final (float): Final score of second package
        - results_1_score_detail_quality (float): Quality score of second package
        - results_1_score_detail_popularity (float): Popularity score of second package
        - results_1_score_detail_maintenance (float): Maintenance score of second package
        - results_1_packageInfoFromScore_name (str): Name from score data of second package
        - results_1_packageInfoFromScore_version (str): Version from score data of second package
        - results_1_packageInfoFromScore_description (str): Description of second package
        - results_1_npmStats_downloadsLastMonth (int): Monthly downloads of second package
        - results_1_npmStats_starsCount (int): Stars count on npm for second package
        - results_1_githubStats_starsCount (int): GitHub stars for second package
        - results_1_githubStats_forksCount (int): GitHub forks for second package
        - results_1_githubStats_subscribersCount (int): GitHub subscribers for second package
        - results_1_githubStats_issues_count (int): Total GitHub issues for second package
        - results_1_githubStats_issues_openCount (int): Open GitHub issues for second package
        - results_1_message (str): Message about result of second package
        - message (str): Summary message indicating how many packages processed
    """
    now_iso = datetime.now(timezone.utc).isoformat()
    return {
        "queryPackages_0": "express",
        "queryPackages_1": "lodash",
        "results_0_packageInput": "express",
        "results_0_packageName": "express",
        "results_0_status": "success",
        "results_0_error": None,
        "results_0_analyzedAt": now_iso,
        "results_0_versionInScore": "4.18.2",
        "results_0_score_final": round(random.uniform(0.7, 0.95), 3),
        "results_0_score_detail_quality": round(random.uniform(0.7, 1.0), 3),
        "results_0_score_detail_popularity": round(random.uniform(0.8, 1.0), 3),
        "results_0_score_detail_maintenance": round(random.uniform(0.6, 0.9), 3),
        "results_0_packageInfoFromScore_name": "express",
        "results_0_packageInfoFromScore_version": "4.18.2",
        "results_0_packageInfoFromScore_description": "Fast, unopinionated, minimalist web framework",
        "results_0_npmStats_downloadsLastMonth": random.randint(15_000_000, 20_000_000),
        "results_0_npmStats_starsCount": random.randint(100, 500),
        "results_0_githubStats_starsCount": random.randint(40_000, 50_000),
        "results_0_githubStats_forksCount": random.randint(7_000, 9_000),
        "results_0_githubStats_subscribersCount": random.randint(200, 400),
        "results_0_githubStats_issues_count": random.randint(100, 300),
        "results_0_githubStats_issues_openCount": random.randint(10, 50),
        "results_0_message": "Successfully analyzed package express",
        "results_1_packageInput": "lodash",
        "results_1_packageName": "lodash",
        "results_1_status": "success",
        "results_1_error": None,
        "results_1_analyzedAt": now_iso,
        "results_1_versionInScore": "4.17.21",
        "results_1_score_final": round(random.uniform(0.8, 0.98), 3),
        "results_1_score_detail_quality": round(random.uniform(0.8, 1.0), 3),
        "results_1_score_detail_popularity": round(random.uniform(0.9, 1.0), 3),
        "results_1_score_detail_maintenance": round(random.uniform(0.7, 0.95), 3),
        "results_1_packageInfoFromScore_name": "lodash",
        "results_1_packageInfoFromScore_version": "4.17.21",
        "results_1_packageInfoFromScore_description": "A modern JavaScript utility library delivering modularity, performance, & extras.",
        "results_1_npmStats_downloadsLastMonth": random.randint(20_000_000, 30_000_000),
        "results_1_npmStats_starsCount": random.randint(200, 600),
        "results_1_githubStats_starsCount": random.randint(50_000, 60_000),
        "results_1_githubStats_forksCount": random.randint(8_000, 10_000),
        "results_1_githubStats_subscribersCount": random.randint(300, 500),
        "results_1_githubStats_issues_count": random.randint(50, 200),
        "results_1_githubStats_issues_openCount": random.randint(5, 30),
        "results_1_message": "Successfully analyzed package lodash",
        "message": "Successfully processed 2 packages"
    }


def npm_sentinel_mcp_npmScore(packages: List[str]) -> Dict[str, Any]:
    """
    Get consolidated package score based on quality, maintenance, and popularity metrics.

    Args:
        packages (List[str]): List of package names to get scores for.

    Returns:
        Dict containing:
        - queryPackages (List[str]): list of package names that were queried
        - results (List[Dict]): list of result objects for each package, containing:
            - packageInput (str): original input string for the package
            - packageName (str): resolved name of the package
            - status (str): operation status ('success' or 'failure')
            - error (str or None): error details if failed, otherwise None
            - data (Dict): detailed score and metadata including:
                - analyzedAt (str): timestamp when analysis was performed in ISO format
                - versionInScore (str): version of the package that was scored
                - score (Dict): contains 'final' overall score and 'detail' with breakdowns
                - package
    """
    if not packages:
        return {
            "queryPackages": [],
            "results": [],
            "message": "No packages provided"
        }

    # Use the external API simulation
    api_response = call_external_api("npm-sentinel-mcp-npmScore")

    results = []
    query_packages = []
    processed_count = 0

    for i in range(2):  # Process up to 2 packages as per simulation
        input_key = f"queryPackages_{i}"
        if input_key in api_response:
            pkg_input = api_response[input_key]
            if i < len(packages):
                query_packages.append(pkg_input)

                status_key = f"results_{i}_status"
                if api_response.get(status_key) == "success":
                    results.append({
                        "packageInput": api_response.get(f"results_{i}_packageInput"),
                        "packageName": api_response.get(f"results_{i}_packageName"),
                        "status": "success",
                        "error": None,
                        "data": {
                            "analyzedAt": api_response.get(f"results_{i}_analyzedAt"),
                            "versionInScore": api_response.get(f"results_{i}_versionInScore"),
                            "score": {
                                "final": api_response.get(f"results_{i}_score_final"),
                                "detail": {
                                    "quality": api_response.get(f"results_{i}_score_detail_quality"),
                                    "popularity": api_response.get(f"results_{i}_score_detail_popularity"),
                                    "maintenance": api_response.get(f"results_{i}_score_detail_maintenance")
                                }
                            },
                            "package": {
                                "name": api_response.get(f"results_{i}_packageInfoFromScore_name"),
                                "version": api_response.get(f"results_{i}_packageInfoFromScore_version"),
                                "description": api_response.get(f"results_{i}_packageInfoFromScore_description")
                            },
                            "npmStats": {
                                "downloadsLastMonth": api_response.get(f"results_{i}_npmStats_downloadsLastMonth"),
                                "starsCount": api_response.get(f"results_{i}_npmStats_starsCount")
                            },
                            "githubStats": {
                                "starsCount": api_response.get(f"results_{i}_githubStats_starsCount"),
                                "forksCount": api_response.get(f"results_{i}_githubStats_forksCount"),
                                "subscribersCount": api_response.get(f"results_{i}_githubStats_subscribersCount"),
                                "issues": {
                                    "count": api_response.get(f"results_{i}_githubStats_issues_count"),
                                    "openCount": api_response.get(f"results_{i}_githubStats_issues_openCount")
                                }
                            }
                        },
                        "message": api_response.get(f"results_{i}_message")
                    })
                    processed_count += 1
                else:
                    results.append({
                        "packageInput": pkg_input,
                        "packageName": pkg_input,
                        "status": "failure",
                        "error": api_response.get(f"results_{i}_error", "Unknown error"),
                        "data": None,
                        "message": f"Failed to analyze package {pkg_input}"
                    })

    return {
        "queryPackages": query_packages,
        "results": results,
        "message": f"Successfully processed {processed_count} packages"
    }