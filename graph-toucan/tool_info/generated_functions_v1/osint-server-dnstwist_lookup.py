from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for domain permutation lookup.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - variant_0_domain (str): Generated domain variant 1
        - variant_0_fuzzer (str): Fuzzing technique used for variant 1
        - variant_0_dns_a (str): A record for variant 1
        - variant_0_dns_aaaa (str): AAAA record for variant 1
        - variant_0_dns_mx (str): MX record for variant 1
        - variant_0_http_status (int): HTTP status code for variant 1
        - variant_0_geoip (str): GeoIP location for variant 1
        - variant_1_domain (str): Generated domain variant 2
        - variant_1_fuzzer (str): Fuzzing technique used for variant 2
        - variant_1_dns_a (str): A record for variant 2
        - variant_1_dns_aaaa (str): AAAA record for variant 2
        - variant_1_dns_mx (str): MX record for variant 2
        - variant_1_http_status (int): HTTP status code for variant 2
        - variant_1_geoip (str): GeoIP location for variant 2
        - statistics_registered (int): Count of registered domains
        - statistics_resolves (int): Count of domains with DNS A records
        - statistics_live (int): Count of live hosts (HTTP 200)
        - statistics_total (int): Total number of variants generated
        - timestamp (str): ISO 8601 timestamp of the lookup
        - success (bool): Whether the operation succeeded
        - error_message (str): Error message if failed, else empty string
    """
    return {
        "variant_0_domain": "examplle.com",
        "variant_0_fuzzer": "double_swap",
        "variant_0_dns_a": "93.184.216.34",
        "variant_0_dns_aaaa": "2606:2800:220:1:248:1893:25c8:1946",
        "variant_0_dns_mx": "mail.examplle.com",
        "variant_0_http_status": 200,
        "variant_0_geoip": "United States",
        "variant_1_domain": "examp1e.com",
        "variant_1_fuzzer": "digit_change",
        "variant_1_dns_a": "198.51.100.1",
        "variant_1_dns_aaaa": "",
        "variant_1_dns_mx": "",
        "variant_1_http_status": 404,
        "variant_1_geoip": "Germany",
        "statistics_registered": 2,
        "statistics_resolves": 2,
        "statistics_live": 1,
        "statistics_total": 2,
        "timestamp": datetime.now().isoformat(),
        "success": True,
        "error_message": ""
    }

def osint_server_dnstwist_lookup(domain: str) -> Dict[str, Any]:
    """
    Performs OSINT lookup using DNS permutation techniques to generate potential phishing domains.
    
    Args:
        domain (str): The base domain name to generate variants from (required)
    
    Returns:
        Dict containing:
        - variants (List[Dict]): List of domain variants with details like domain, fuzzer, DNS records, HTTP status, and geoip
        - statistics (Dict): Summary metrics including registered, resolves, live, and total counts
        - timestamp (str): ISO 8601 timestamp when the lookup was performed
        - success (bool): Whether the operation completed successfully
        - error_message (Optional[str]): Error message if operation failed, None otherwise
    
    Raises:
        ValueError: If domain is empty or not a string
    """
    if not domain:
        return {
            "variants": [],
            "statistics": {"registered": 0, "resolves": 0, "live": 0, "total": 0},
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "error_message": "Domain parameter is required"
        }
    
    try:
        api_data = call_external_api("osint-server-dnstwist_lookup")
        
        # Construct variants list from indexed fields
        variants = [
            {
                "domain": api_data["variant_0_domain"],
                "fuzzer": api_data["variant_0_fuzzer"],
                "dns_a": api_data["variant_0_dns_a"] if api_data["variant_0_dns_a"] else None,
                "dns_aaaa": api_data["variant_0_dns_aaaa"] if api_data["variant_0_dns_aaaa"] else None,
                "dns_mx": api_data["variant_0_dns_mx"] if api_data["variant_0_dns_mx"] else None,
                "http_status": api_data["variant_0_http_status"] if api_data["variant_0_http_status"] else None,
                "geoip": api_data["variant_0_geoip"] if api_data["variant_0_geoip"] else None
            },
            {
                "domain": api_data["variant_1_domain"],
                "fuzzer": api_data["variant_1_fuzzer"],
                "dns_a": api_data["variant_1_dns_a"] if api_data["variant_1_dns_a"] else None,
                "dns_aaaa": api_data["variant_1_dns_aaaa"] if api_data["variant_1_dns_aaaa"] else None,
                "dns_mx": api_data["variant_1_dns_mx"] if api_data["variant_1_dns_mx"] else None,
                "http_status": api_data["variant_1_http_status"] if api_data["variant_1_http_status"] else None,
                "geoip": api_data["variant_1_geoip"] if api_data["variant_1_geoip"] else None
            }
        ]
        
        # Construct statistics dictionary
        statistics = {
            "registered": api_data["statistics_registered"],
            "resolves": api_data["statistics_resolves"],
            "live": api_data["statistics_live"],
            "total": api_data["statistics_total"]
        }
        
        # Handle error message (convert empty string to None)
        error_message = api_data["error_message"] if api_data["error_message"] else None
        
        result = {
            "variants": variants,
            "statistics": statistics,
            "timestamp": api_data["timestamp"],
            "success": api_data["success"],
            "error_message": error_message
        }
        
        return result
        
    except Exception as e:
        return {
            "variants": [],
            "statistics": {"registered": 0, "resolves": 0, "live": 0, "total": 0},
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "error_message": f"Internal error occurred: {str(e)}"
        }