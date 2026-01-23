from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for internet speed test.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - upload_speed (float): Measured upload speed in Mbps
        - unit (str): Unit of measurement, typically "Mbps"
        - elapsed_time (float): Total time taken for final upload in seconds
        - data_size (int): Size of data uploaded in bytes
        - size_used (str): Human-readable size label used, e.g., "20MB"
        - server_info_cdn_provider (str): CDN provider name or null
        - server_info_pop_code (str): POP location code or null
        - server_info_pop_location (str): POP geographic location or null
        - server_info_served_by (str): Server identifier or null
        - server_info_via_header (str): Via header info or null
        - server_info_cache_status (str): Cache status or null
        - server_info_server_ip_info (str): Server IP info or null
        - server_info_x_cache (str): X-Cache header value or null
        - all_tests_0_size (str): Size label for first test
        - all_tests_0_upload_speed (float): Upload speed in Mbps for first test
        - all_tests_0_elapsed_time (float): Elapsed time in seconds for first test
        - all_tests_0_data_size (int): Data size in bytes for first test
        - all_tests_0_url (str): URL used for first test
        - all_tests_0_error (bool): Whether first test had an error
        - all_tests_0_message (str): Error message if first test failed
        - all_tests_1_size (str): Size label for second test
        - all_tests_1_upload_speed (float): Upload speed in Mbps for second test
        - all_tests_1_elapsed_time (float): Elapsed time in seconds for second test
        - all_tests_1_data_size (int): Data size in bytes for second test
        - all_tests_1_url (str): URL used for second test
        - all_tests_1_error (bool): Whether second test had an error
        - all_tests_1_message (str): Error message if second test failed
    """
    return {
        "upload_speed": 47.3,
        "unit": "Mbps",
        "elapsed_time": 16.8,
        "data_size": 100 * 1024 * 1024,  # 100MB
        "size_used": "100MB",
        "server_info_cdn_provider": "Cloudflare",
        "server_info_pop_code": "SFO",
        "server_info_pop_location": "San Francisco, US",
        "server_info_served_by": "origin-server-23",
        "server_info_via_header": "1.1 google, 1.1 cdn",
        "server_info_cache_status": "HIT",
        "server_info_server_ip_info": "104.18.20.100",
        "server_info_x_cache": "Hit from cloudfront",
        "all_tests_0_size": "10MB",
        "all_tests_0_upload_speed": 35.2,
        "all_tests_0_elapsed_time": 2.3,
        "all_tests_0_data_size": 10 * 1024 * 1024,
        "all_tests_0_url": "https://upload.example.com/test1",
        "all_tests_0_error": False,
        "all_tests_0_message": "",
        "all_tests_1_size": "50MB",
        "all_tests_1_upload_speed": 42.7,
        "all_tests_1_elapsed_time": 9.4,
        "all_tests_1_data_size": 50 * 1024 * 1024,
        "all_tests_1_url": "https://upload.example.com/test2",
        "all_tests_1_error": False,
        "all_tests_1_message": ""
    }

def internet_speed_test_measure_upload_speed(url_upload: Optional[str] = None, size_limit: Optional[str] = None) -> Dict[str, Any]:
    """
    Measure upload speed using incremental file sizes.

    Args:
        url_upload: URL to upload data to (optional, defaults to a test endpoint)
        size_limit: Maximum file size to test (default: 100MB), e.g., "50MB", "200MB"

    Returns:
        Dictionary with upload speed results containing:
        - upload_speed (float): final measured upload speed in Mbps
        - unit (str): unit of the upload speed measurement, typically "Mbps"
        - elapsed_time (float): total time taken for the final successful upload test in seconds
        - data_size (int): size of the data uploaded in bytes for the final successful test
        - size_used (str): human-readable size label used in the final successful test
        - server_info (Dict): server-related metadata from response headers
        - all_tests (List[Dict]): list of individual test results with details
    """
    # Validate inputs
    if url_upload is not None and not isinstance(url_upload, str):
        raise TypeError("url_upload must be a string or None")
    if size_limit is not None and not isinstance(size_limit, str):
        raise TypeError("size_limit must be a string or None")

    # Use default values if not provided
    effective_url = url_upload or "https://upload.example.com/test"
    effective_size_limit = size_limit or "100MB"

    # Call external API to simulate speed test
    raw_data = call_external_api("internet-speed-test-measure_upload_speed")

    # Construct server_info dictionary from flattened fields
    server_info = {
        "cdn_provider": raw_data["server_info_cdn_provider"],
        "pop_code": raw_data["server_info_pop_code"],
        "pop_location": raw_data["server_info_pop_location"],
        "served_by": raw_data["server_info_served_by"],
        "via_header": raw_data["server_info_via_header"],
        "cache_status": raw_data["server_info_cache_status"],
        "server_ip_info": raw_data["server_info_server_ip_info"],
        "x_cache": raw_data["server_info_x_cache"]
    }

    # Construct all_tests list from indexed fields
    all_tests = [
        {
            "size": raw_data["all_tests_0_size"],
            "upload_speed": raw_data["all_tests_0_upload_speed"],
            "elapsed_time": raw_data["all_tests_0_elapsed_time"],
            "data_size": raw_data["all_tests_0_data_size"],
            "url": raw_data["all_tests_0_url"]
        },
        {
            "size": raw_data["all_tests_1_size"],
            "upload_speed": raw_data["all_tests_1_upload_speed"],
            "elapsed_time": raw_data["all_tests_1_elapsed_time"],
            "data_size": raw_data["all_tests_1_data_size"],
            "url": raw_data["all_tests_1_url"]
        }
    ]

    # Add error fields only if they exist and are relevant
    if raw_data.get("all_tests_0_error"):
        all_tests[0]["error"] = raw_data["all_tests_0_error"]
        all_tests[0]["message"] = raw_data["all_tests_0_message"]
    if raw_data.get("all_tests_1_error"):
        all_tests[1]["error"] = raw_data["all_tests_1_error"]
        all_tests[1]["message"] = raw_data["all_tests_1_message"]

    # Build final result structure
    result = {
        "upload_speed": raw_data["upload_speed"],
        "unit": raw_data["unit"],
        "elapsed_time": raw_data["elapsed_time"],
        "data_size": raw_data["data_size"],
        "size_used": raw_data["size_used"],
        "server_info": server_info,
        "all_tests": all_tests
    }

    return result