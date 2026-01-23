from typing import Dict, Any, Optional

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
    Simulates fetching data from external API for internet speed test latency measurement.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - latency (float): measured latency value in milliseconds
        - unit (str): unit of the latency measurement, typically "ms"
        - url (str): the URL to which latency was measured
        - server_info_cdn_provider (str): CDN provider name
        - server_info_pop_code (str): Point of Presence code
        - server_info_pop_location (str): Point of Presence location
        - server_info_cf_ray (str): Cloudflare Ray ID
        - server_info_served_by (str): Server identifier
        - server_info_via_header (str): Via header information
        - server_info_cache_status (str): Cache status
        - server_info_server_ip_info (str): Server IP information
        - server_info_x_cache (str): X-Cache header value
    """
    return {
        "latency": 45.2,
        "unit": "ms",
        "url": "https://example.com",
        "server_info_cdn_provider": "Cloudflare",
        "server_info_pop_code": "SFO",
        "server_info_pop_location": "San Francisco, CA",
        "server_info_cf_ray": "7e8f9g0h1i2j-SFO",
        "server_info_served_by": "server-123",
        "server_info_via_header": "1.1 google",
        "server_info_cache_status": "HIT",
        "server_info_server_ip_info": "192.0.2.1",
        "server_info_x_cache": "Hit from cloudfront"
    }

def internet_speed_test_measure_latency(url: Optional[str] = None) -> Dict[str, Any]:
    """
    Measure the latency to a given URL.
    
    Args:
        url (Optional[str]): The URL to measure latency against. If not provided, a default URL is used.
    
    Returns:
        Dict containing:
        - latency (float): measured latency value in milliseconds
        - unit (str): unit of the latency measurement, typically "ms"
        - url (str): the URL to which latency was measured
        - server_info (Dict): server-related metadata including cdn_provider, pop_code, pop_location, cf_ray,
          and other optional headers or network info like served_by, via_header, cache_status, server_ip_info, x_cache
    """
    # Use default URL if none provided
    target_url = url or "https://example.com"
    
    # Call external API to get simulated data
    api_data = call_external_api("internet-speed-test-measure_latency", **locals())
    
    # Construct server_info dictionary from flattened fields
    server_info = {
        "cdn_provider": api_data["server_info_cdn_provider"],
        "pop_code": api_data["server_info_pop_code"],
        "pop_location": api_data["server_info_pop_location"],
        "cf_ray": api_data["server_info_cf_ray"],
        "served_by": api_data["server_info_served_by"],
        "via_header": api_data["server_info_via_header"],
        "cache_status": api_data["server_info_cache_status"],
        "server_ip_info": api_data["server_info_server_ip_info"],
        "x_cache": api_data["server_info_x_cache"]
    }
    
    # Construct final result
    result = {
        "latency": api_data["latency"],
        "unit": api_data["unit"],
        "url": target_url,
        "server_info": server_info
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
