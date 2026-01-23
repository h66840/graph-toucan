from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external Nmap scan API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - scan_report_target_domain (str): Domain name that was scanned
        - scan_report_target_ip (str): Primary IP address associated with the target domain
        - scan_report_additional_ips_0 (str): First additional IP address
        - scan_report_additional_ips_1 (str): Second additional IP address
        - scan_report_rdns_record (str): Reverse DNS record for the primary IP
        - scan_report_host_status (str): Status of the host (e.g., 'up')
        - scan_report_latency (float): Round-trip latency in seconds
        - scan_report_open_ports_0_port_number (int): First open port number
        - scan_report_open_ports_0_protocol (str): Protocol of first open port
        - scan_report_open_ports_0_state (str): State of first open port
        - scan_report_open_ports_0_service (str): Service running on first open port
        - scan_report_open_ports_1_port_number (int): Second open port number
        - scan_report_open_ports_1_protocol (str): Protocol of second open port
        - scan_report_open_ports_1_state (str): State of second open port
        - scan_report_open_ports_1_service (str): Service running on second open port
        - scan_report_scan_summary (str): Summary of the scan results
        - nmap_version (str): Version of Nmap used
        - scan_start_time (str): Scan start time in ISO format
        - scan_duration_seconds (float): Duration of the scan in seconds
        - filtered_or_closed_ports_count (int): Number of filtered or closed ports
        - filtered_or_closed_ports_reason (str): Reason for filtering or closing ports
        - total_ips_count (int): Total number of IP addresses associated with the domain
    """
    # Generate realistic but simulated data
    target_ip = f"185.199.{random.randint(0, 255)}.{random.randint(0, 255)}"
    additional_ips = [
        f"185.199.{random.randint(0, 255)}.{random.randint(0, 255)}",
        f"185.199.{random.randint(0, 255)}.{random.randint(0, 255)}"
    ]
    start_time = datetime.now() - timedelta(seconds=random.randint(30, 120))
    
    return {
        "scan_report_target_domain": "example.com",
        "scan_report_target_ip": target_ip,
        "scan_report_additional_ips_0": additional_ips[0],
        "scan_report_additional_ips_1": additional_ips[1],
        "scan_report_rdns_record": f"server-{target_ip.split('.')[-1]}.example.com",
        "scan_report_host_status": "up",
        "scan_report_latency": round(random.uniform(0.05, 0.3), 3),
        "scan_report_open_ports_0_port_number": 80,
        "scan_report_open_ports_0_protocol": "tcp",
        "scan_report_open_ports_0_state": "open",
        "scan_report_open_ports_0_service": "http",
        "scan_report_open_ports_1_port_number": 443,
        "scan_report_open_ports_1_protocol": "tcp",
        "scan_report_open_ports_1_state": "open",
        "scan_report_open_ports_1_service": "https",
        "scan_report_scan_summary": "Nmap scan completed successfully",
        "nmap_version": "7.92",
        "scan_start_time": start_time.isoformat(),
        "scan_duration_seconds": round(random.uniform(45.0, 110.0), 2),
        "filtered_or_closed_ports_count": random.randint(800, 950),
        "filtered_or_closed_ports_reason": "no-response",
        "total_ips_count": 3
    }

def osint_server_nmap_scan(target: str) -> Dict[str, Any]:
    """
    Performs an Nmap scan on the specified target domain or IP address.
    
    Args:
        target (str): The domain name or IP address to scan. Required.
    
    Returns:
        Dict containing the complete scan report with the following structure:
        - scan_report (Dict): Comprehensive scan results including target info, ports, status
        - nmap_version (str): Version of Nmap used
        - scan_start_time (str): ISO format timestamp when scan started
        - scan_duration_seconds (float): Total scan duration in seconds
        - target_domain (str): Domain name scanned
        - target_ip (str): Primary IP address scanned
        - additional_ips (List[str]): Other IPs associated with the domain
        - rdns_record (str): Reverse DNS record for primary IP
        - host_status (str): Host status (e.g., 'up')
        - latency (float): Round-trip latency in seconds
        - open_ports (List[Dict]): List of open ports with details
        - filtered_or_closed_ports_count (int): Count of filtered/closed ports
        - filtered_or_closed_ports_reason (str): Reason for filtering/closing
        - total_ips_count (int): Total number of IPs associated with domain
    
    Raises:
        ValueError: If target is empty or None
    """
    if not target or not target.strip():
        raise ValueError("Target parameter is required")
    
    target = target.strip()
    
    # Call external API to get simulated data
    api_data = call_external_api("osint-server-nmap_scan")
    
    # Update target domain from input if available
    api_data["scan_report_target_domain"] = target
    
    # Construct open ports list from indexed fields
    open_ports = [
        {
            "port_number": api_data["scan_report_open_ports_0_port_number"],
            "protocol": api_data["scan_report_open_ports_0_protocol"],
            "state": api_data["scan_report_open_ports_0_state"],
            "service": api_data["scan_report_open_ports_0_service"]
        },
        {
            "port_number": api_data["scan_report_open_ports_1_port_number"],
            "protocol": api_data["scan_report_open_ports_1_protocol"],
            "state": api_data["scan_report_open_ports_1_state"],
            "service": api_data["scan_report_open_ports_1_service"]
        }
    ]
    
    # Construct additional IPs list
    additional_ips = [
        api_data["scan_report_additional_ips_0"],
        api_data["scan_report_additional_ips_1"]
    ]
    
    # Build the complete scan report
    scan_report = {
        "target_domain": api_data["scan_report_target_domain"],
        "target_ip": api_data["scan_report_target_ip"],
        "additional_ips": additional_ips,
        "rdns_record": api_data["scan_report_rdns_record"],
        "host_status": api_data["scan_report_host_status"],
        "latency": api_data["scan_report_latency"],
        "open_ports": open_ports,
        "filtered_or_closed_ports": {
            "count": api_data["filtered_or_closed_ports_count"],
            "reason": api_data["filtered_or_closed_ports_reason"]
        },
        "scan_summary": api_data["scan_report_scan_summary"]
    }
    
    # Build final result matching output schema
    result = {
        "scan_report": scan_report,
        "nmap_version": api_data["nmap_version"],
        "scan_start_time": api_data["scan_start_time"],
        "scan_duration_seconds": api_data["scan_duration_seconds"],
        "target_domain": api_data["scan_report_target_domain"],
        "target_ip": api_data["scan_report_target_ip"],
        "additional_ips": additional_ips,
        "rdns_record": api_data["scan_report_rdns_record"],
        "host_status": api_data["scan_report_host_status"],
        "latency": api_data["scan_report_latency"],
        "open_ports": open_ports,
        "filtered_or_closed_ports_count": api_data["filtered_or_closed_ports_count"],
        "filtered_or_closed_ports_reason": api_data["filtered_or_closed_ports_reason"],
        "total_ips_count": api_data["total_ips_count"]
    }
    
    return result