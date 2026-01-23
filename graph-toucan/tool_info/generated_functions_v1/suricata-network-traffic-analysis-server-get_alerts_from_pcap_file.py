from typing import Dict, List, Any, Optional
import json
from datetime import datetime
import re

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Suricata network traffic analysis.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - raw_log_content (str): Full raw content of fast.log
        - success (bool): Whether execution was successful
        - error_message (str): Error message if any, otherwise None
        - metadata_pcap_file_size (int): Size of the PCAP file in bytes
        - metadata_analysis_start_time (str): ISO format start timestamp
        - metadata_analysis_end_time (str): ISO format end timestamp
        - metadata_suricata_version (str): Version of Suricata used
        - metadata_result_directory (str): Path to result directory
        - summary_total_alerts (int): Total number of alerts detected
        - summary_unique_signatures_count (int): Number of unique signatures triggered
        - summary_most_frequent_signature (str): Most frequently triggered signature
        - summary_top_source_ips_0 (str): Top source IP address
        - summary_top_source_ips_1 (str): Second top source IP address
        - summary_top_destination_ips_0 (str): Top destination IP address
        - summary_top_destination_ips_1 (str): Second top destination IP address
        - summary_alert_severity_distribution_high (int): Count of high severity alerts
        - summary_alert_severity_distribution_medium (int): Count of medium severity alerts
        - summary_alert_severity_distribution_low (int): Count of low severity alerts
        - alert_0_timestamp (str): Timestamp of first alert
        - alert_0_source_ip (str): Source IP of first alert
        - alert_0_source_port (int): Source port of first alert
        - alert_0_destination_ip (str): Destination IP of first alert
        - alert_0_destination_port (int): Destination port of first alert
        - alert_0_protocol (str): Protocol of first alert
        - alert_0_severity (str): Severity level of first alert
        - alert_0_signature (str): Signature text of first alert
        - alert_0_category (str): Category of first alert
        - alert_1_timestamp (str): Timestamp of second alert
        - alert_1_source_ip (str): Source IP of second alert
        - alert_1_source_port (int): Source port of second alert
        - alert_1_destination_ip (str): Destination IP of second alert
        - alert_1_destination_port (int): Destination port of second alert
        - alert_1_protocol (str): Protocol of second alert
        - alert_1_severity (str): Severity level of second alert
        - alert_1_signature (str): Signature text of second alert
        - alert_1_category (str): Category of second alert
    """
    return {
        "raw_log_content": "03/15/2023-14:22:10.123456  [**] [1:2001219:4] ET POLICY IRC Non-Standard Port [**] [Classification: Misc Activity] [Priority: 3] {TCP} 192.168.1.100:56789 -> 203.0.113.45:6667\n"
                           "03/15/2023-14:23:45.678901  [**] [1:1000001:1] Test Alert Signature [**] [Classification: Test Category] [Priority: 2] {UDP} 198.51.100.20:1234 -> 192.0.2.50:53",
        "success": True,
        "error_message": None,
        "metadata_pcap_file_size": 1048576,
        "metadata_analysis_start_time": "2023-03-15T14:22:05.123456",
        "metadata_analysis_end_time": "2023-03-15T14:23:50.678901",
        "metadata_suricata_version": "6.0.9",
        "metadata_result_directory": "/tmp/suricata/results/1",
        "summary_total_alerts": 2,
        "summary_unique_signatures_count": 2,
        "summary_most_frequent_signature": "ET POLICY IRC Non-Standard Port",
        "summary_top_source_ips_0": "192.168.1.100",
        "summary_top_source_ips_1": "198.51.100.20",
        "summary_top_destination_ips_0": "203.0.113.45",
        "summary_top_destination_ips_1": "192.0.2.50",
        "summary_alert_severity_distribution_high": 0,
        "summary_alert_severity_distribution_medium": 2,
        "summary_alert_severity_distribution_low": 0,
        "alert_0_timestamp": "03/15/2023-14:22:10.123456",
        "alert_0_source_ip": "192.168.1.100",
        "alert_0_source_port": 56789,
        "alert_0_destination_ip": "203.0.113.45",
        "alert_0_destination_port": 6667,
        "alert_0_protocol": "TCP",
        "alert_0_severity": "3",
        "alert_0_signature": "ET POLICY IRC Non-Standard Port",
        "alert_0_category": "Misc Activity",
        "alert_1_timestamp": "03/15/2023-14:23:45.678901",
        "alert_1_source_ip": "198.51.100.20",
        "alert_1_source_port": 1234,
        "alert_1_destination_ip": "192.0.2.50",
        "alert_1_destination_port": 53,
        "alert_1_protocol": "UDP",
        "alert_1_severity": "2",
        "alert_1_signature": "Test Alert Signature",
        "alert_1_category": "Test Category"
    }

def suricata_network_traffic_analysis_server_get_alerts_from_pcap_file(pcap_destination: str, destination_folder_results: str) -> Dict[str, Any]:
    """
    Processes a PCAP file with Suricata and returns the generated alert logs.
    
    This function runs Suricata against a given PCAP file, stores the results in a specified directory,
    and then reads the generated `fast.log` file to return its contents.
    
    Args:
        pcap_destination (str): The path to the PCAP file to analyze.
        destination_folder_results (str): The directory where Suricata should output its results.
    
    Returns:
        Dict containing:
        - alerts (List[Dict]): List of parsed alert entries from Suricata's `fast.log`
        - raw_log_content (str): Full raw string content of the `fast.log` file
        - metadata (Dict): Information about the analysis process
        - summary (Dict): Aggregated insights from the alert data
        - success (bool): Whether the operation completed successfully
        - error_message (str): Error message if any occurred, otherwise None
    """
    try:
        # Validate inputs
        if not pcap_destination:
            return {
                "alerts": [],
                "raw_log_content": "",
                "metadata": {},
                "summary": {},
                "success": False,
                "error_message": "pcap_destination is required"
            }
            
        if not destination_folder_results:
            return {
                "alerts": [],
                "raw_log_content": "",
                "metadata": {},
                "summary": {},
                "success": False,
                "error_message": "destination_folder_results is required"
            }
        
        # Call external API to simulate Suricata execution
        api_data = call_external_api("suricata-network-traffic-analysis-server-get_alerts_from_pcap_file")
        
        # Construct alerts list from indexed fields
        alerts = [
            {
                "timestamp": api_data["alert_0_timestamp"],
                "source_ip": api_data["alert_0_source_ip"],
                "source_port": api_data["alert_0_source_port"],
                "destination_ip": api_data["alert_0_destination_ip"],
                "destination_port": api_data["alert_0_destination_port"],
                "protocol": api_data["alert_0_protocol"],
                "severity": api_data["alert_0_severity"],
                "signature": api_data["alert_0_signature"],
                "category": api_data["alert_0_category"]
            },
            {
                "timestamp": api_data["alert_1_timestamp"],
                "source_ip": api_data["alert_1_source_ip"],
                "source_port": api_data["alert_1_source_port"],
                "destination_ip": api_data["alert_1_destination_ip"],
                "destination_port": api_data["alert_1_destination_port"],
                "protocol": api_data["alert_1_protocol"],
                "severity": api_data["alert_1_severity"],
                "signature": api_data["alert_1_signature"],
                "category": api_data["alert_1_category"]
            }
        ]
        
        # Build metadata
        metadata = {
            "pcap_file_size": api_data["metadata_pcap_file_size"],
            "analysis_start_time": api_data["metadata_analysis_start_time"],
            "analysis_end_time": api_data["metadata_analysis_end_time"],
            "suricata_version": api_data["metadata_suricata_version"],
            "result_directory": api_data["metadata_result_directory"]
        }
        
        # Build summary
        summary = {
            "total_alerts": api_data["summary_total_alerts"],
            "unique_signatures_count": api_data["summary_unique_signatures_count"],
            "most_frequent_signature": api_data["summary_most_frequent_signature"],
            "top_source_ips": [
                api_data["summary_top_source_ips_0"],
                api_data["summary_top_source_ips_1"]
            ],
            "top_destination_ips": [
                api_data["summary_top_destination_ips_0"],
                api_data["summary_top_destination_ips_1"]
            ],
            "alert_severity_distribution": {
                "high": api_data["summary_alert_severity_distribution_high"],
                "medium": api_data["summary_alert_severity_distribution_medium"],
                "low": api_data["summary_alert_severity_distribution_low"]
            }
        }
        
        return {
            "alerts": alerts,
            "raw_log_content": api_data["raw_log_content"],
            "metadata": metadata,
            "summary": summary,
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }
        
    except Exception as e:
        return {
            "alerts": [],
            "raw_log_content": "",
            "metadata": {},
            "summary": {},
            "success": False,
            "error_message": str(e)
        }