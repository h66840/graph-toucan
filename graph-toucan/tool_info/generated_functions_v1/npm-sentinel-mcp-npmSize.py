from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching package size data from external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_package (str): Name of the first requested package
        - result_0_status (str): Status for first package ('success' or 'error')
        - result_0_error (str or None): Error message if failed, else None
        - result_0_message (str): Human-readable message for first result
        - result_0_data_name (str): Name of the analyzed package
        - result_0_data_version (str): Version of the analyzed package
        - result_0_data_sizeInKb (float): Total bundle size in KB
        - result_0_data_gzipInKb (float): Gzipped bundle size in KB
        - result_0_data_dependencyCount (int): Number of direct dependencies
        - result_1_package (str): Name of the second requested package
        - result_1_status (str): Status for second package ('success' or 'error')
        - result_1_error (str or None): Error message if failed, else None
        - result_1_message (str): Human-readable message for second result
        - result_1_data_name (str): Name of the analyzed package
        - result_1_data_version (str): Version of the analyzed package
        - result_1_data_sizeInKb (float): Total bundle size in KB
        - result_1_data_gzipInKb (float): Gzipped bundle size in KB
        - result_1_data_dependencyCount (int): Number of direct dependencies
    """
    return {
        "result_0_package": "lodash",
        "result_0_status": "success",
        "result_0_error": None,
        "result_0_message": "Successfully retrieved size information for lodash",
        "result_0_data_name": "lodash",
        "result_0_data_version": "4.17.21",
        "result_0_data_sizeInKb": 75.3,
        "result_0_data_gzipInKb": 24.8,
        "result_0_data_dependencyCount": 0,
        "result_1_package": "react",
        "result_1_status": "success",
        "result_1_error": None,
        "result_1_message": "Successfully retrieved size information for react",
        "result_1_data_name": "react",
        "result_1_data_version": "18.2.0",
        "result_1_data_sizeInKb": 45.2,
        "result_1_data_gzipInKb": 15.6,
        "result_1_data_dependencyCount": 2
    }

def npm_sentinel_mcp_npmSize(packages: List[str]) -> List[Dict[str, Any]]:
    """
    Get package size information including dependencies and bundle size.

    Args:
        packages (List[str]): List of package names to get size information for.

    Returns:
        List[Dict]: List of result objects with the following structure:
            - package (str): Name of the requested package
            - status (str): Status of the request ('success' or 'error')
            - error (str or None): Error message if request failed, otherwise None
            - message (str): Human-readable summary of the result
            - data (Dict or None): Size and metadata if successful, containing:
                - name (str): Package name
                - version (str): Analyzed version
                - sizeInKb (float): Total bundle size in kilobytes
                - gzipInKb (float): Gzipped bundle size in kilobytes
                - dependencyCount (int): Number of direct dependencies
    """
    if not packages:
        return []

    # Call external API to get simulated data
    api_data = call_external_api("npm-sentinel-mcp-npmSize")

    results: List[Dict[str, Any]] = []

    # Process up to 2 packages (based on available simulated data)
    for i in range(min(2, len(packages))):
        package_name = packages[i]
        prefix = f"result_{i}"

        # Extract flat fields from API response
        status = api_data.get(f"{prefix}_status", "error")
        error = api_data.get(f"{prefix}_error")
        message = api_data.get(f"{prefix}_message", f"Error processing {package_name}")

        data = None
        if status == "success":
            data = {
                "name": api_data.get(f"{prefix}_data_name", package_name),
                "version": api_data.get(f"{prefix}_data_version", "unknown"),
                "sizeInKb": api_data.get(f"{prefix}_data_sizeInKb", 0.0),
                "gzipInKb": api_data.get(f"{prefix}_data_gzipInKb", 0.0),
                "dependencyCount": api_data.get(f"{prefix}_data_dependencyCount", 0)
            }

        result = {
            "package": package_name,
            "status": status,
            "error": error,
            "message": message,
            "data": data
        }
        results.append(result)

    # For any additional packages beyond the first two, return error results
    for j in range(2, len(packages)):
        results.append({
            "package": packages[j],
            "status": "error",
            "error": "Package limit exceeded in simulation",
            "message": f"Could not retrieve size information for {packages[j]}: simulation supports up to 2 packages",
            "data": None
        })

    return results