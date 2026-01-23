from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external OSINT server for host lookup.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_ip (str): First resolved IP address
        - result_0_record_type (str): DNS record type for first result
        - result_0_ttl (int): TTL in seconds for first result
        - result_0_source (str): Source of first result
        - result_1_ip (str): Second resolved IP address
        - result_1_record_type (str): DNS record type for second result
        - result_1_ttl (int): TTL in seconds for second result
        - result_1_source (str): Source of second result
        - domain_info_domain (str): Domain name
        - domain_info_registered (bool): Whether domain is registered
        - domain_info_name_servers_0 (str): First name server
        - domain_info_name_servers_1 (str): Second name server
        - domain_info_creation_date (str): Domain creation date in ISO format
        - related_ips_0 (str): First unique IP address
        - related_ips_1 (str): Second unique IP address
        - geo_location_0_ip (str): IP address for first geolocation
        - geo_location_0_country (str): Country name for first geolocation
        - geo_location_0_city (str): City name for first geolocation
        - geo_location_0_latitude (float): Latitude for first geolocation
        - geo_location_0_longitude (float): Longitude for first geolocation
        - geo_location_0_asn (str): ASN for first geolocation
        - geo_location_0_organization (str): Organization for first geolocation
        - geo_location_1_ip (str): IP address for second geolocation
        - geo_location_1_country (str): Country name for second geolocation
        - geo_location_1_city (str): City name for second geolocation
        - geo_location_1_latitude (float): Latitude for second geolocation
        - geo_location_1_longitude (float): Longitude for second geolocation
        - geo_location_1_asn (str): ASN for second geolocation
        - geo_location_1_organization (str): Organization for second geolocation
        - dns_records_a_0 (str): First A record
        - dns_records_a_1 (str): Second A record
        - dns_records_mx_0 (str): First MX record
        - dns_records_mx_1 (str): Second MX record
        - dns_records_cname (str): CNAME record
        - dns_records_txt_0 (str): First TXT record
        - dns_records_txt_1 (str): Second TXT record
        - success (bool): Whether lookup was successful
        - error_message (str): Error message if any, otherwise empty string
        - timestamp (str): ISO 8601 timestamp of lookup
        - metadata_target (str): Queried target
        - metadata_response_time_ms (int): Response time in milliseconds
        - metadata_source_0 (str): First OSINT source used
        - metadata_source_1 (str): Second OSINT source used
        - metadata_tool_version (str): Tool version
    """
    return {
        "result_0_ip": "192.168.1.10",
        "result_0_record_type": "A",
        "result_0_ttl": 3600,
        "result_0_source": "dnsdb",
        "result_1_ip": "2001:db8::1",
        "result_1_record_type": "AAAA",
        "result_1_ttl": 7200,
        "result_1_source": "virustotal",
        "domain_info_domain": "example.com",
        "domain_info_registered": True,
        "domain_info_name_servers_0": "ns1.example.com",
        "domain_info_name_servers_1": "ns2.example.com",
        "domain_info_creation_date": "2005-08-08T00:00:00Z",
        "related_ips_0": "192.168.1.10",
        "related_ips_1": "2001:db8::1",
        "geo_location_0_ip": "192.168.1.10",
        "geo_location_0_country": "United States",
        "geo_location_0_city": "New York",
        "geo_location_0_latitude": 40.7128,
        "geo_location_0_longitude": -74.0060,
        "geo_location_0_asn": "AS12345",
        "geo_location_0_organization": "Example Corp",
        "geo_location_1_ip": "2001:db8::1",
        "geo_location_1_country": "Germany",
        "geo_location_1_city": "Frankfurt",
        "geo_location_1_latitude": 50.1109,
        "geo_location_1_longitude": 8.6821,
        "geo_location_1_asn": "AS67890",
        "geo_location_1_organization": "Global Network GmbH",
        "dns_records_a_0": "192.168.1.10",
        "dns_records_a_1": "192.168.1.11",
        "dns_records_mx_0": "mail.example.com",
        "dns_records_mx_1": "backupmail.example.com",
        "dns_records_cname": "www.example.com",
        "dns_records_txt_0": "v=spf1 include:_spf.example.com ~all",
        "dns_records_txt_1": "google-site-verification=abcdef123456",
        "success": True,
        "error_message": "",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "metadata_target": "example.com",
        "metadata_response_time_ms": 150,
        "metadata_source_0": "dnsdb",
        "metadata_source_1": "virustotal",
        "metadata_tool_version": "1.0.0"
    }

def osint_server_host_lookup(target: str) -> Dict[str, Any]:
    """
    Performs an OSINT host lookup for the given target domain or hostname.
    
    This function simulates querying an external OSINT server to gather DNS, network,
    and domain registration information about a target host. It returns structured
    data including resolved IP addresses, domain details, geolocation, and DNS records.
    
    Args:
        target (str): The domain name or hostname to perform lookup on. Required.
    
    Returns:
        Dict containing the following keys:
        - results (List[Dict]): List of resolved host records with IP, record type, TTL, source
        - domain_info (Dict): Domain registration details including name servers and creation date
        - related_ips (List[str]): Unique IP addresses associated with the domain
        - geo_locations (List[Dict]): Geolocation data for each resolved IP
        - dns_records (Dict): Aggregated DNS records by type (A, AAAA, MX, CNAME, TXT)
        - success (bool): Whether the lookup completed successfully
        - error_message (str): Error description if failed, None otherwise
        - timestamp (str): ISO 8601 timestamp when lookup was performed
        - metadata (Dict): Additional context about the query execution
    
    Raises:
        ValueError: If target is empty or not a string
    """
    if not target or not isinstance(target, str):
        return {
            "results": [],
            "domain_info": {},
            "related_ips": [],
            "geo_locations": [],
            "dns_records": {},
            "success": False,
            "error_message": "Target must be a non-empty string",
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "metadata": {
                "queried_target": str(target),
                "response_time_ms": 0,
                "sources": [],
                "tool_version": "1.0.0"
            }
        }
    
    # Call external API to get flat data
    api_data = call_external_api("osint-server-host_lookup")
    
    # Construct results list
    results = [
        {
            "ip": api_data["result_0_ip"],
            "record_type": api_data["result_0_record_type"],
            "ttl": api_data["result_0_ttl"],
            "source": api_data["result_0_source"]
        },
        {
            "ip": api_data["result_1_ip"],
            "record_type": api_data["result_1_record_type"],
            "ttl": api_data["result_1_ttl"],
            "source": api_data["result_1_source"]
        }
    ]
    
    # Construct domain_info
    domain_info = {
        "domain": api_data["domain_info_domain"],
        "registered": api_data["domain_info_registered"],
        "name_servers": [
            api_data["domain_info_name_servers_0"],
            api_data["domain_info_name_servers_1"]
        ],
        "creation_date": api_data["domain_info_creation_date"]
    }
    
    # Construct related_ips
    related_ips = [
        api_data["related_ips_0"],
        api_data["related_ips_1"]
    ]
    
    # Construct geo_locations
    geo_locations = [
        {
            "ip": api_data["geo_location_0_ip"],
            "country": api_data["geo_location_0_country"],
            "city": api_data["geo_location_0_city"],
            "latitude": api_data["geo_location_0_latitude"],
            "longitude": api_data["geo_location_0_longitude"],
            "asn": api_data["geo_location_0_asn"],
            "organization": api_data["geo_location_0_organization"]
        },
        {
            "ip": api_data["geo_location_1_ip"],
            "country": api_data["geo_location_1_country"],
            "city": api_data["geo_location_1_city"],
            "latitude": api_data["geo_location_1_latitude"],
            "longitude": api_data["geo_location_1_longitude"],
            "asn": api_data["geo_location_1_asn"],
            "organization": api_data["geo_location_1_organization"]
        }
    ]
    
    # Construct dns_records
    dns_records = {
        "a": [
            api_data["dns_records_a_0"],
            api_data["dns_records_a_1"]
        ],
        "mx": [
            api_data["dns_records_mx_0"],
            api_data["dns_records_mx_1"]
        ],
        "cname": api_data["dns_records_cname"],
        "txt": [
            api_data["dns_records_txt_0"],
            api_data["dns_records_txt_1"]
        ]
    }
    
    # Construct metadata
    metadata = {
        "queried_target": api_data["metadata_target"],
        "response_time_ms": api_data["metadata_response_time_ms"],
        "sources": [
            api_data["metadata_source_0"],
            api_data["metadata_source_1"]
        ],
        "tool_version": api_data["metadata_tool_version"]
    }
    
    return {
        "results": results,
        "domain_info": domain_info,
        "related_ips": related_ips,
        "geo_locations": geo_locations,
        "dns_records": dns_records,
        "success": api_data["success"],
        "error_message": api_data["error_message"],
        "timestamp": api_data["timestamp"],
        "metadata": metadata
    }