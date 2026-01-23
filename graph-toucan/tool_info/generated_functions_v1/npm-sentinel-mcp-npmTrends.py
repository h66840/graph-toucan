from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for npm package trends.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - query_packagesInput_0 (str): First input package name
        - query_packagesInput_1 (str): Second input package name (if exists)
        - query_periodUsed (str): Time period used in the query
        - results_0_packageInput (str): Original input name for first result
        - results_0_packageName (str): Resolved package name for first result
        - results_0_status (str): Status of first result ("success" or "error")
        - results_0_error (str): Error message if any for first result
        - results_0_message (str): Additional message for first result
        - results_0_data_totalDownloads (int): Total downloads for first package
        - results_0_data_averageDailyDownloads (float): Average daily downloads for first package
        - results_0_data_peakDay (str): Peak download day for first package (YYYY-MM-DD)
        - results_0_data_peakDownloads (int): Downloads on peak day for first package
        - results_1_packageInput (str): Original input name for second result
        - results_1_packageName (str): Resolved package name for second result
        - results_1_status (str): Status of second result ("success" or "error")
        - results_1_error (str): Error message if any for second result
        - results_1_message (str): Additional message for second result
        - results_1_data_totalDownloads (int): Total downloads for second package
        - results_1_data_averageDailyDownloads (float): Average daily downloads for second package
        - results_1_data_peakDay (str): Peak download day for second package (YYYY-MM-DD)
        - results_1_data_peakDownloads (int): Downloads on peak day for second package
        - summary_totalPackagesProcessed (int): Total number of packages processed
        - summary_totalSuccessful (int): Number of successful results
        - summary_totalFailed (int): Number of failed results
        - summary_overallTotalDownloads (int): Sum of total downloads across all packages
        - summary_overallAverageDailyDownloads (float): Weighted average daily downloads
    """
    # Simulate realistic data based on tool_name
    if tool_name != "npm-sentinel-mcp-npmTrends":
        raise ValueError("Invalid tool name")

    # Generate two sample results
    periods = ["last-week", "last-month", "last-year"]
    period_used = random.choice(periods)

    # Generate data for first result
    pkg1_input = "lodash"
    pkg1_name = "lodash"
    pkg1_status = "success"
    pkg1_error = ""
    pkg1_message = "Data retrieved successfully"
    pkg1_total_downloads = random.randint(1_000_000, 10_000_000)
    pkg1_avg_daily = pkg1_total_downloads / (7 if period_used == "last-week" else 30 if period_used == "last-month" else 365)
    pkg1_peak_day = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    pkg1_peak_downloads = int(pkg1_avg_daily * random.uniform(1.5, 3.0))

    # Generate data for second result
    pkg2_input = "react"
    pkg2_name = "react"
    pkg2_status = "success"
    pkg2_error = ""
    pkg2_message = "Data retrieved successfully"
    pkg2_total_downloads = random.randint(5_000_000, 15_000_000)
    pkg2_avg_daily = pkg2_total_downloads / (7 if period_used == "last-week" else 30 if period_used == "last-month" else 365)
    pkg2_peak_day = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
    pkg2_peak_downloads = int(pkg2_avg_daily * random.uniform(1.5, 3.0))

    # Summary data
    total_processed = 2
    total_successful = 2
    total_failed = 0
    overall_total_downloads = pkg1_total_downloads + pkg2_total_downloads
    overall_avg_daily = overall_total_downloads / (
        (7 + 7) if period_used == "last-week" else
        (30 + 30) if period_used == "last-month" else
        (365 + 365)
    )

    return {
        "query_packagesInput_0": pkg1_input,
        "query_packagesInput_1": pkg2_input,
        "query_periodUsed": period_used,
        "results_0_packageInput": pkg1_input,
        "results_0_packageName": pkg1_name,
        "results_0_status": pkg1_status,
        "results_0_error": pkg1_error,
        "results_0_message": pkg1_message,
        "results_0_data_totalDownloads": pkg1_total_downloads,
        "results_0_data_averageDailyDownloads": round(pkg1_avg_daily, 2),
        "results_0_data_peakDay": pkg1_peak_day,
        "results_0_data_peakDownloads": pkg1_peak_downloads,
        "results_1_packageInput": pkg2_input,
        "results_1_packageName": pkg2_name,
        "results_1_status": pkg2_status,
        "results_1_error": pkg2_error,
        "results_1_message": pkg2_message,
        "results_1_data_totalDownloads": pkg2_total_downloads,
        "results_1_data_averageDailyDownloads": round(pkg2_avg_daily, 2),
        "results_1_data_peakDay": pkg2_peak_day,
        "results_1_data_peakDownloads": pkg2_peak_downloads,
        "summary_totalPackagesProcessed": total_processed,
        "summary_totalSuccessful": total_successful,
        "summary_totalFailed": total_failed,
        "summary_overallTotalDownloads": overall_total_downloads,
        "summary_overallAverageDailyDownloads": round(overall_avg_daily, 2),
    }


def npm_sentinel_mcp_npmTrends(packages: List[str], period: Optional[str] = None) -> Dict[str, Any]:
    """
    Get download trends and popularity metrics for npm packages.

    Args:
        packages (List[str]): List of package names to get trends for (required)
        period (Optional[str]): Time period for trends. Options: "last-week", "last-month", "last-year"

    Returns:
        Dict containing:
        - query (Dict): original input packages and time period used
        - results (List[Dict]): list of result objects for each requested package
          each containing packageInput, packageName, status, error, data (with download metrics), and message
        - summary (Dict): aggregated summary including total processed, successful, failed,
          overall total downloads, and overall average daily downloads

    Raises:
        ValueError: If packages list is empty
    """
    # Input validation
    if not packages or not isinstance(packages, list):
        raise ValueError("Parameter 'packages' must be a non-empty list of package names")

    # Validate period if provided
    valid_periods = ["last-week", "last-month", "last-year"]
    if period and period not in valid_periods:
        raise ValueError(f"Parameter 'period' must be one of {valid_periods} if provided")

    # Default period
    period_used = period or "last-month"

    # Call external API (simulated)
    api_data = call_external_api("npm-sentinel-mcp-npmTrends")

    # Extract query information
    query_packages_input = []
    for i in range(2):  # We expect up to 2 packages from API
        key = f"query_packagesInput_{i}"
        if key in api_data and api_data[key]:
            query_packages_input.append(api_data[key])
        else:
            break

    # If API didn't return expected packages, use input packages
    if not query_packages_input:
        query_packages_input = packages[:2]  # Limit to first 2 for consistency

    query = {
        "packagesInput": query_packages_input,
        "periodUsed": api_data.get("query_periodUsed", period_used)
    }

    # Construct results list
    results = []
    for i in range(2):
        pkg_key = f"results_{i}_packageInput"
        if pkg_key not in api_data:
            break

        # Only include packages that were in the original request
        package_input = api_data[pkg_key]
        if package_input not in packages:
            continue

        result_data = {
            "totalDownloads": api_data.get(f"results_{i}_data_totalDownloads", 0),
            "averageDailyDownloads": api_data.get(f"results_{i}_data_averageDailyDownloads", 0.0),
            "peakDay": api_data.get(f"results_{i}_data_peakDay", ""),
            "peakDownloads": api_data.get(f"results_{i}_data_peakDownloads", 0)
        }

        result = {
            "packageInput": package_input,
            "packageName": api_data.get(f"results_{i}_packageName", package_input),
            "status": api_data.get(f"results_{i}_status", "error"),
            "error": api_data.get(f"results_{i}_error", ""),
            "data": result_data,
            "message": api_data.get(f"results_{i}_message", "")
        }
        results.append(result)

    # Construct summary
    summary = {
        "totalPackagesProcessed": len(results),
        "totalSuccessful": sum(1 for r in results if r["status"] == "success"),
        "totalFailed": sum(1 for r in results if r["status"] == "error"),
        "overallTotalDownloads": sum(r["data"]["totalDownloads"] for r in results),
        "overallAverageDailyDownloads": sum(r["data"]["averageDailyDownloads"] for r in results) / len(results) if results else 0.0
    }

    return {
        "query": query,
        "results": results,
        "summary": summary
    }