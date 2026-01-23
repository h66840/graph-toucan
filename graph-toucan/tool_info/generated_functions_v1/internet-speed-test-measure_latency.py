from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
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
    api_data = call_external_api("internet-speed-test-measure_latency")
    
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