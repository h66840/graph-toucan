from typing import Dict, List, Any, Optional
import time
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for internet speed test.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - timestamp (float): Unix timestamp of when the test was completed
        - download_speed (float): Download speed result
        - download_unit (str): Unit for download speed (e.g., 'Mbps')
        - download_elapsed_time (float): Time taken for download test in seconds
        - download_data_size (str): Total data size used in download test
        - download_size_used (str): Size of files used in test
        - download_server_info (str): Server info for download test
        - upload_speed (float): Upload speed result
        - upload_unit (str): Unit for upload speed (e.g., 'Mbps')
        - upload_elapsed_time (float): Time taken for upload test in seconds
        - upload_data_size (str): Total data size used in upload test
        - upload_size_used (str): Size of data used in upload test
        - upload_server_info (str): Server info for upload test
        - latency_latency (float): Measured latency in ms
        - latency_unit (str): Unit for latency (e.g., 'ms')
        - latency_url (str): URL used for latency test
        - latency_server_info (str): Server info for latency test
        - jitter_jitter (float): Measured jitter in ms
        - jitter_unit (str): Unit for jitter (e.g., 'ms')
        - jitter_average_latency (float): Average latency during jitter test
        - jitter_samples (int): Number of samples taken for jitter measurement
        - jitter_url (str): URL used for jitter test
        - jitter_server_info (str): Server info for jitter test
        - test_methodology (str): Description of testing approach
        - download_all_tests_0_size (str): First test file size in download
        - download_all_tests_0_speed (float): Speed achieved in first download test
        - download_all_tests_0_time (float): Time taken in first download test
        - download_all_tests_1_size (str): Second test file size in download
        - download_all_tests_1_speed (float): Speed achieved in second download test
        - download_all_tests_1_time (float): Time taken in second download test
        - upload_all_tests_0_size (str): First data chunk size in upload
        - upload_all_tests_0_speed (float): Speed achieved in first upload test
        - upload_all_tests_0_time (float): Time taken in first upload test
        - upload_all_tests_1_size (str): Second data chunk size in upload
        - upload_all_tests_1_speed (float): Speed achieved in second upload test
        - upload_all_tests_1_time (float): Time taken in second upload test
    """
    return {
        "timestamp": time.time(),
        "download_speed": round(random.uniform(40.0, 95.0), 2),
        "download_unit": "Mbps",
        "download_elapsed_time": round(random.uniform(8.0, 15.0), 2),
        "download_data_size": "100MB",
        "download_size_used": "10MB, 25MB, 50MB, 100MB",
        "download_server_info": "Server-A (Tokyo)",
        "upload_speed": round(random.uniform(20.0, 50.0), 2),
        "upload_unit": "Mbps",
        "upload_elapsed_time": round(random.uniform(6.0, 12.0), 2),
        "upload_data_size": "100MB",
        "upload_size_used": "5MB, 10MB, 25MB, 50MB, 100MB",
        "upload_server_info": "Server-A (Tokyo)",
        "latency_latency": round(random.uniform(15.0, 45.0), 2),
        "latency_unit": "ms",
        "latency_url": "http://latency.example.com/ping",
        "latency_server_info": "Server-A (Tokyo)",
        "jitter_jitter": round(random.uniform(1.0, 5.0), 2),
        "jitter_unit": "ms",
        "jitter_average_latency": round(random.uniform(20.0, 40.0), 2),
        "jitter_samples": 10,
        "jitter_url": "http://latency.example.com/ping",
        "jitter_server_info": "Server-A (Tokyo)",
        "test_methodology": "Incremental file size with time threshold adaptive algorithm",
        "download_all_tests_0_size": "10MB",
        "download_all_tests_0_speed": round(random.uniform(30.0, 60.0), 2),
        "download_all_tests_0_time": round(random.uniform(2.0, 3.5), 2),
        "download_all_tests_1_size": "25MB",
        "download_all_tests_1_speed": round(random.uniform(50.0, 80.0), 2),
        "download_all_tests_1_time": round(random.uniform(4.0, 6.0), 2),
        "upload_all_tests_0_size": "5MB",
        "upload_all_tests_0_speed": round(random.uniform(15.0, 35.0), 2),
        "upload_all_tests_0_time": round(random.uniform(1.5, 3.0), 2),
        "upload_all_tests_1_size": "10MB",
        "upload_all_tests_1_speed": round(random.uniform(25.0, 45.0), 2),
        "upload_all_tests_1_time": round(random.uniform(3.0, 5.0), 2),
    }


def internet_speed_test_run_complete_test(
    max_size: Optional[str] = None,
    url_upload: Optional[str] = None,
    url_latency: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run a complete speed test returning all metrics in a single call.

    This test uses the smart incremental approach inspired by SpeedOf.Me:
    - First measures download speed with gradually increasing file sizes
    - Then measures upload speed with gradually increasing data sizes
    - Measures latency and jitter
    - Returns comprehensive results with real-time data

    Args:
        max_size (Optional[str]): Maximum file size to test (default: 100MB)
        url_upload (Optional[str]): URL for upload testing
        url_latency (Optional[str]): URL for latency testing

    Returns:
        Dict containing:
        - timestamp (float): Unix timestamp of when the test was completed
        - download (Dict): Download speed result with 'download_speed', 'unit', 'elapsed_time',
                          'data_size', 'size_used', 'server_info', and 'all_tests' fields
        - upload (Dict): Upload speed result with 'upload_speed', 'unit', 'elapsed_time',
                        'data_size', 'size_used', 'server_info', and detailed 'all_tests' list
        - latency (Dict): Contains 'latency', 'unit', 'url', and 'server_info'
        - jitter (Dict): Contains 'jitter', 'unit', 'average_latency', 'samples', 'url', and 'server_info'
        - test_methodology (str): Description of the testing approach used
    """
    # Validate inputs
    if max_size is not None and not isinstance(max_size, str):
        raise TypeError("max_size must be a string")
    if url_upload is not None and not isinstance(url_upload, str):
        raise TypeError("url_upload must be a string")
    if url_latency is not None and not isinstance(url_latency, str):
        raise TypeError("url_latency must be a string")

    # Use provided URLs or defaults
    final_url_upload = url_upload or "http://upload.example.com/test"
    final_url_latency = url_latency or "http://latency.example.com/ping"

    # Call external API to get flat data
    raw_data = call_external_api("internet-speed-test-run_complete_test")

    # Construct nested download tests
    download_all_tests = [
        {
            "size": raw_data["download_all_tests_0_size"],
            "speed": raw_data["download_all_tests_0_speed"],
            "time": raw_data["download_all_tests_0_time"]
        },
        {
            "size": raw_data["download_all_tests_1_size"],
            "speed": raw_data["download_all_tests_1_speed"],
            "time": raw_data["download_all_tests_1_time"]
        }
    ]

    # Construct nested upload tests
    upload_all_tests = [
        {
            "size": raw_data["upload_all_tests_0_size"],
            "speed": raw_data["upload_all_tests_0_speed"],
            "time": raw_data["upload_all_tests_0_time"]
        },
        {
            "size": raw_data["upload_all_tests_1_size"],
            "speed": raw_data["upload_all_tests_1_speed"],
            "time": raw_data["upload_all_tests_1_time"]
        }
    ]

    # Build final result structure matching output schema
    result = {
        "timestamp": raw_data["timestamp"],
        "download": {
            "download_speed": raw_data["download_speed"],
            "unit": raw_data["download_unit"],
            "elapsed_time": raw_data["download_elapsed_time"],
            "data_size": raw_data["download_data_size"],
            "size_used": raw_data["download_size_used"],
            "server_info": raw_data["download_server_info"],
            "all_tests": download_all_tests
        },
        "upload": {
            "upload_speed": raw_data["upload_speed"],
            "unit": raw_data["upload_unit"],
            "elapsed_time": raw_data["upload_elapsed_time"],
            "data_size": raw_data["upload_data_size"],
            "size_used": raw_data["upload_size_used"],
            "server_info": raw_data["upload_server_info"],
            "all_tests": upload_all_tests
        },
        "latency": {
            "latency": raw_data["latency_latency"],
            "unit": raw_data["latency_unit"],
            "url": final_url_latency,
            "server_info": raw_data["latency_server_info"]
        },
        "jitter": {
            "jitter": raw_data["jitter_jitter"],
            "unit": raw_data["jitter_unit"],
            "average_latency": raw_data["jitter_average_latency"],
            "samples": raw_data["jitter_samples"],
            "url": final_url_latency,
            "server_info": raw_data["jitter_server_info"]
        },
        "test_methodology": raw_data["test_methodology"]
    }

    return result