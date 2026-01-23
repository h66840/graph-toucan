from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching server information from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - url_download (str): URL used for download testing
        - status_code_url_download (int): HTTP status code for download URL
        - server_info_url_download_cdn_provider (str): CDN provider for download URL
        - server_info_url_download_pop_code (str): POP code for download URL
        - server_info_url_download_pop_location (str): POP location for download URL
        - server_info_url_download_served_by (str): Server identifier for download URL
        - server_info_url_download_via_header (str): Via header value for download URL
        - server_info_url_download_cache_status (str): Cache status for download URL
        - server_info_url_download_x_cache (str): X-Cache header value for download URL
        - headers_url_download_content_length (str): Content-Length header for download URL
        - headers_url_download_content_type (str): Content-Type header for download URL
        - headers_url_download_server (str): Server header for download URL
        - url_upload (str): URL used for upload testing
        - status_code_url_upload (int): HTTP status code for upload URL
        - server_info_url_upload_cdn_provider (str): CDN provider for upload URL
        - server_info_url_upload_pop_code (str): POP code for upload URL
        - server_info_url_upload_pop_location (str): POP location for upload URL
        - server_info_url_upload_cf_ray (str): CF-Ray header value for upload URL
        - headers_url_upload_content_length (str): Content-Length header for upload URL
        - headers_url_upload_content_type (str): Content-Type header for upload URL
        - headers_url_upload_server (str): Server header for upload URL
        - url_latency (str): URL used for latency testing
        - status_code_url_latency (int): HTTP status code for latency URL
        - server_info_url_latency_cdn_provider (str): CDN provider for latency URL
        - server_info_url_latency_pop_code (str): POP code for latency URL
        - server_info_url_latency_pop_location (str): POP location for latency URL
        - server_info_url_latency_cf_ray (str): CF-Ray header value for latency URL
        - headers_url_latency_content_length (str): Content-Length header for latency URL
        - headers_url_latency_content_type (str): Content-Type header for latency URL
        - headers_url_latency_server (str): Server header for latency URL
    """
    return {
        "url_download": "https://speedtest-download.example.com",
        "status_code_url_download": 200,
        "server_info_url_download_cdn_provider": "Cloudflare",
        "server_info_url_download_pop_code": "SFO",
        "server_info_url_download_pop_location": "San Francisco, US",
        "server_info_url_download_served_by": "nginx",
        "server_info_url_download_via_header": "1.1 varnish",
        "server_info_url_download_cache_status": "HIT",
        "server_info_url_download_x_cache": "HIT from cloudfront",
        "headers_url_download_content_length": "1048576",
        "headers_url_download_content_type": "application/octet-stream",
        "headers_url_download_server": "Apache",
        
        "url_upload": "https://speedtest-upload.example.com",
        "status_code_url_upload": 200,
        "server_info_url_upload_cdn_provider": "Akamai",
        "server_info_url_upload_pop_code": "LAX",
        "server_info_url_upload_pop_location": "Los Angeles, US",
        "server_info_url_upload_cf_ray": "6a7b8c9d0e1f-LAX",
        "headers_url_upload_content_length": "0",
        "headers_url_upload_content_type": "text/plain",
        "headers_url_upload_server": "AkamaiGHost",
        
        "url_latency": "https://speedtest-latency.example.com",
        "status_code_url_latency": 200,
        "server_info_url_latency_cdn_provider": "Cloudflare",
        "server_info_url_latency_pop_code": "SJC",
        "server_info_url_latency_pop_location": "San Jose, US",
        "server_info_url_latency_cf_ray": "1b2c3d4e5f6a-SJC",
        "headers_url_latency_content_length": "512",
        "headers_url_latency_content_type": "application/json",
        "headers_url_latency_server": "cloudflare"
    }

def internet_speed_test_get_server_info(url: str) -> Dict[str, Any]:
    """
    Get server information for any URL without performing speed tests.
    
    Args:
        url (str): URL to analyze
        
    Returns:
        Dictionary with server information including POP location, CDN info, etc.
        Contains the following fields:
        - url_download: URL used for download testing
        - status_code_url_download: HTTP status code returned when accessing the download URL
        - server_info_url_download: server and CDN information for the download URL
        - headers_url_download: full HTTP response headers from the download URL request
        - url_upload: URL used for upload testing
        - status_code_url_upload: HTTP status code returned when accessing the upload URL
        - server_info_url_upload: server and CDN information for the upload URL
        - headers_url_upload: full HTTP response headers from the upload URL request
        - url_latency: URL used for latency testing
        - status_code_url_latency: HTTP status code returned when accessing the latency measurement URL
        - server_info_url_latency: server and CDN information for the latency URL
        - headers_url_latency: full HTTP response headers from the latency URL request
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    api_data = call_external_api("internet-speed-test-get_server_info")
    
    result = {
        "url_download": api_data["url_download"],
        "status_code_url_download": api_data["status_code_url_download"],
        "server_info_url_download": {
            "cdn_provider": api_data["server_info_url_download_cdn_provider"],
            "pop_code": api_data["server_info_url_download_pop_code"],
            "pop_location": api_data["server_info_url_download_pop_location"],
            "served_by": api_data["server_info_url_download_served_by"],
            "via_header": api_data["server_info_url_download_via_header"],
            "cache_status": api_data["server_info_url_download_cache_status"],
            "x_cache": api_data["server_info_url_download_x_cache"]
        },
        "headers_url_download": {
            "Content-Length": api_data["headers_url_download_content_length"],
            "Content-Type": api_data["headers_url_download_content_type"],
            "Server": api_data["headers_url_download_server"]
        },
        "url_upload": api_data["url_upload"],
        "status_code_url_upload": api_data["status_code_url_upload"],
        "server_info_url_upload": {
            "cdn_provider": api_data["server_info_url_upload_cdn_provider"],
            "pop_code": api_data["server_info_url_upload_pop_code"],
            "pop_location": api_data["server_info_url_upload_pop_location"],
            "cf_ray": api_data["server_info_url_upload_cf_ray"]
        },
        "headers_url_upload": {
            "Content-Length": api_data["headers_url_upload_content_length"],
            "Content-Type": api_data["headers_url_upload_content_type"],
            "Server": api_data["headers_url_upload_server"]
        },
        "url_latency": api_data["url_latency"],
        "status_code_url_latency": api_data["status_code_url_latency"],
        "server_info_url_latency": {
            "cdn_provider": api_data["server_info_url_latency_cdn_provider"],
            "pop_code": api_data["server_info_url_latency_pop_code"],
            "pop_location": api_data["server_info_url_latency_pop_location"],
            "cf_ray": api_data["server_info_url_latency_cf_ray"]
        },
        "headers_url_latency": {
            "Content-Length": api_data["headers_url_latency_content_length"],
            "Content-Type": api_data["headers_url_latency_content_type"],
            "Server": api_data["headers_url_latency_server"]
        }
    }
    
    return result