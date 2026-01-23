from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DNS reconnaissance.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_type (str): Type of the first DNS record (e.g., A, MX)
        - result_0_name (str): Name of the first DNS record
        - result_0_data (str): Data of the first DNS record
        - result_0_ttl (int): TTL of the first DNS record
        - result_1_type (str): Type of the second DNS record
        - result_1_name (str): Name of the second DNS record
        - result_1_data (str): Data of the second DNS record
        - result_1_ttl (int): TTL of the second DNS record
        - record_count (int): Total number of DNS records found
        - success (bool): Whether the DNS enumeration was successful
        - error_message (str): Error message if any, otherwise empty string
        - target_resolved (bool): Whether the target domain was resolved
        - ip_0 (str): First IP address found
        - ip_1 (str): Second IP address found
        - scan_metadata_start_time (str): Scan start time in ISO format
        - scan_metadata_end_time (str): Scan end time in ISO format
        - scan_metadata_tool_used (str): Name of the tool used (e.g., dnsrecon)
        - scan_metadata_arguments_used (str): Arguments passed to the tool
    """
    return {
        "result_0_type": "A",
        "result_0_name": "example.com",
        "result_0_data": "93.184.216.34",
        "result_0_ttl": 300,
        "result_1_type": "MX",
        "result_1_name": "example.com",
        "result_1_data": "mail.example.com",
        "result_1_ttl": 3600,
        "record_count": 2,
        "success": True,
        "error_message": "",
        "target_resolved": True,
        "ip_0": "93.184.216.34",
        "ip_1": "2606:2800:220:1:248:1893:25c8:1946",
        "scan_metadata_start_time": "2023-10-01T08:00:00Z",
        "scan_metadata_end_time": "2023-10-01T08:00:15Z",
        "scan_metadata_tool_used": "dnsrecon",
        "scan_metadata_arguments_used": "-d example.com"
    }

def osint_server_dnsrecon_lookup(target: str) -> Dict[str, Any]:
    """
    Performs DNS enumeration on the given target domain using simulated external DNS reconnaissance tool.

    Args:
        target (str): The domain name to perform DNS lookup on. Required.

    Returns:
        Dict containing:
        - results (List[Dict]): List of DNS records with keys 'type', 'name', 'data', 'ttl'
        - record_count (int): Total number of DNS records found
        - success (bool): Whether the operation succeeded
        - error_message (Optional[str]): Error description if failed, else None
        - target_resolved (bool): Whether the domain resolved to any records/IPs
        - ips_found (List[str]): List of unique IP addresses found
        - scan_metadata (Dict): Metadata about the scan including start/end time, tool, and arguments
    """
    if not target or not isinstance(target, str) or not target.strip():
        return {
            "results": [],
            "record_count": 0,
            "success": False,
            "error_message": "Invalid target: must be a non-empty string",
            "target_resolved": False,
            "ips_found": [],
            "scan_metadata": {
                "start_time": datetime.utcnow().isoformat() + "Z",
                "end_time": datetime.utcnow().isoformat() + "Z",
                "tool_used": "dnsrecon",
                "arguments_used": ""
            }
        }

    try:
        api_data = call_external_api("osint-server-dnsrecon_lookup")

        # Construct results list from indexed fields
        results = [
            {
                "type": api_data["result_0_type"],
                "name": api_data["result_0_name"],
                "data": api_data["result_0_data"],
                "ttl": api_data["result_0_ttl"]
            },
            {
                "type": api_data["result_1_type"],
                "name": api_data["result_1_name"],
                "data": api_data["result_1_data"],
                "ttl": api_data["result_1_ttl"]
            }
        ]

        # Collect unique IPs
        ips_found = list({api_data["ip_0"], api_data["ip_1"]})

        # Build scan metadata
        scan_metadata = {
            "start_time": api_data["scan_metadata_start_time"],
            "end_time": api_data["scan_metadata_end_time"],
            "tool_used": api_data["scan_metadata_tool_used"],
            "arguments_used": api_data["scan_metadata_arguments_used"]
        }

        error_message: Optional[str] = api_data["error_message"] if api_data["error_message"] else None

        return {
            "results": results,
            "record_count": api_data["record_count"],
            "success": api_data["success"],
            "error_message": error_message,
            "target_resolved": api_data["target_resolved"],
            "ips_found": ips_found,
            "scan_metadata": scan_metadata
        }

    except Exception as e:
        return {
            "results": [],
            "record_count": 0,
            "success": False,
            "error_message": f"Unexpected error during DNS lookup: {str(e)}",
            "target_resolved": False,
            "ips_found": [],
            "scan_metadata": {
                "start_time": datetime.utcnow().isoformat() + "Z",
                "end_time": datetime.utcnow().isoformat() + "Z",
                "tool_used": "dnsrecon",
                "arguments_used": f"-d {target}"
            }
        }