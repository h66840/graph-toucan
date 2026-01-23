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
    Simulates fetching data from external API for internet speed test.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - download_speed (float): measured download speed value in Mbps
        - unit (str): unit of the download speed, e.g. "Mbps"
        - elapsed_time (float): time taken to complete the download test in seconds
        - data_size (int): total amount of data downloaded in bytes
        - size_used (str): human-readable file size used for the test, e.g. "100MB"
        - server_info_cdn_provider (str): CDN provider name
        - server_info_pop_code (str): Point of presence code
        - server_info_pop_location (str): Location of the PoP
        - server_info_served_by (str): Server identifier
        - server_info_via_header (str): HTTP via header value
        - server_info_cache_status (str): Cache hit/miss status
        - server_info_server_ip_info (str): Server IP information
        - server_info_x_cache (str): X-Cache header value
        - all_tests_0_size (str): Size of first test
        - all_tests_0_speed (float): Speed of first test in Mbps
        - all_tests_0_elapsed_time (float): Elapsed time of first test in seconds
        - all_tests_1_size (str): Size of second test
        - all_tests_1_speed (float): Speed of second test in Mbps
        - all_tests_1_elapsed_time (float): Elapsed time of second test in seconds
    """
    return {
        "download_speed": 94.5,
        "unit": "Mbps",
        "elapsed_time": 8.43,
        "data_size": 100 * 1024 * 1024,  # 100MB in bytes
        "size_used": "100MB",
        "server_info_cdn_provider": "Cloudflare",
        "server_info_pop_code": "SFO",
        "server_info_pop_location": "San Francisco, CA",
        "server_info_served_by": "origin-server-23",
        "server_info_via_header": "1.1 google, 1.1 cdn",
        "server_info_cache_status": "HIT",
        "server_info_server_ip_info": "104.16.249.249",
        "server_info_x_cache": "HIT from CDN",
        "all_tests_0_size": "10MB",
        "all_tests_0_speed": 87.2,
        "all_tests_0_elapsed_time": 0.92,
        "all_tests_1_size": "50MB",
        "all_tests_1_speed": 91.8,
        "all_tests_1_elapsed_time": 4.37
    }

def internet_speed_test_measure_download_speed(size_limit: Optional[str] = "100MB") -> Dict[str, Any]:
    """
    Measure download speed using incremental file sizes.

    Args:
        size_limit (str, optional): Maximum file size to test (default: "100MB")

    Returns:
        Dictionary with download speed results containing:
        - download_speed (float): measured download speed value
        - unit (str): unit of the download speed, e.g. "Mbps"
        - elapsed_time (float): time taken to complete the download test in seconds
        - data_size (int): total amount of data downloaded in bytes
        - size_used (str): human-readable file size used for the test, e.g. "100MB"
        - server_info (Dict): contains CDN and server metadata
        - all_tests (List[Dict]): list of all individual test results
    """
    # Validate input
    if not isinstance(size_limit, str):
        raise TypeError("size_limit must be a string")
    
    # Call external API to get raw data
    api_data = call_external_api("internet-speed-test-measure_download_speed", **locals())
    
    # Construct server_info dictionary from flattened fields
    server_info = {
        "cdn_provider": api_data["server_info_cdn_provider"],
        "pop_code": api_data["server_info_pop_code"],
        "pop_location": api_data["server_info_pop_location"],
        "served_by": api_data["server_info_served_by"],
        "via_header": api_data["server_info_via_header"],
        "cache_status": api_data["server_info_cache_status"],
        "server_ip_info": api_data["server_info_server_ip_info"],
        "x_cache": api_data["server_info_x_cache"]
    }
    
    # Construct all_tests list from indexed fields
    all_tests = [
        {
            "size": api_data["all_tests_0_size"],
            "speed": api_data["all_tests_0_speed"],
            "elapsed_time": api_data["all_tests_0_elapsed_time"]
        },
        {
            "size": api_data["all_tests_1_size"],
            "speed": api_data["all_tests_1_speed"],
            "elapsed_time": api_data["all_tests_1_elapsed_time"]
        }
    ]
    
    # Construct final result dictionary matching output schema
    result = {
        "download_speed": api_data["download_speed"],
        "unit": api_data["unit"],
        "elapsed_time": api_data["elapsed_time"],
        "data_size": api_data["data_size"],
        "size_used": api_data["size_used"],
        "server_info": server_info,
        "all_tests": all_tests
    }
    
    return result

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
