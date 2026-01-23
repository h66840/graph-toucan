from typing import Dict, List, Any, Optional
import random
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching DNS lookup data from an external API for dig query.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - answer_section_0_name (str): Name of first answer record
        - answer_section_0_ttl (int): TTL of first answer record
        - answer_section_0_class (str): Class of first answer record
        - answer_section_0_type (str): Type of first answer record
        - answer_section_0_data (str): Data of first answer record
        - answer_section_1_name (str): Name of second answer record
        - answer_section_1_ttl (int): TTL of second answer record
        - answer_section_1_class (str): Class of second answer record
        - answer_section_1_type (str): Type of second answer record
        - answer_section_1_data (str): Data of second answer record
        - authority_section_0_name (str): Name of first authority record
        - authority_section_0_ttl (int): TTL of first authority record
        - authority_section_0_class (str): Class of first authority record
        - authority_section_0_type (str): Type of first authority record
        - authority_section_0_data (str): Data of first authority record
        - authority_section_1_name (str): Name of second authority record
        - authority_section_1_ttl (int): TTL of second authority record
        - authority_section_1_class (str): Class of second authority record
        - authority_section_1_type (str): Type of second authority record
        - authority_section_1_data (str): Data of second authority record
        - additional_section_0_name (str): Name of first additional record
        - additional_section_0_ttl (int): TTL of first additional record
        - additional_section_0_class (str): Class of first additional record
        - additional_section_0_type (str): Type of first additional record
        - additional_section_0_data (str): Data of first additional record
        - additional_section_1_name (str): Name of second additional record
        - additional_section_1_ttl (int): TTL of second additional record
        - additional_section_1_class (str): Class of second additional record
        - additional_section_1_type (str): Type of second additional record
        - additional_section_1_data (str): Data of second additional record
        - question_section_0_name (str): Name of first question record
        - question_section_0_class (str): Class of first question record
        - question_section_0_type (str): Type of first question record
        - question_section_1_name (str): Name of second question record
        - question_section_1_class (str): Class of second question record
        - question_section_1_type (str): Type of second question record
        - query_time_ms (int): Time in milliseconds the query took
        - server_ip (str): IP address of DNS server used
        - server_port (int): Port number of DNS server
        - when (str): Timestamp of query execution in human-readable format
        - msg_size_rcvd (int): Size of received message in bytes
        - status (str): Response status from DNS server (e.g., NOERROR)
        - opcode (str): Operation code of the query (e.g., QUERY)
        - flags_0 (str): First DNS header flag (e.g., qr)
        - flags_1 (str): Second DNS header flag (e.g., rd)
        - edns_version (int): EDNS version
        - edns_flags (int): EDNS flags
        - edns_udp (int): EDNS UDP size
    """
    return {
        "answer_section_0_name": "example.com.",
        "answer_section_0_ttl": 3600,
        "answer_section_0_class": "IN",
        "answer_section_0_type": "A",
        "answer_section_0_data": "93.184.216.34",
        "answer_section_1_name": "example.com.",
        "answer_section_1_ttl": 3600,
        "answer_section_1_class": "IN",
        "answer_section_1_type": "A",
        "answer_section_1_data": "2606:2800:220:1:248:1893:25c8:1946",
        "authority_section_0_name": "example.com.",
        "authority_section_0_ttl": 86400,
        "authority_section_0_class": "IN",
        "authority_section_0_type": "NS",
        "authority_section_0_data": "a.iana-servers.net.",
        "authority_section_1_name": "example.com.",
        "authority_section_1_ttl": 86400,
        "authority_section_1_class": "IN",
        "authority_section_1_type": "NS",
        "authority_section_1_data": "b.iana-servers.net.",
        "additional_section_0_name": "a.iana-servers.net.",
        "additional_section_0_ttl": 86400,
        "additional_section_0_class": "IN",
        "additional_section_0_type": "A",
        "additional_section_0_data": "199.43.132.53",
        "additional_section_1_name": "b.iana-servers.net.",
        "additional_section_1_ttl": 86400,
        "additional_section_1_class": "IN",
        "additional_section_1_type": "A",
        "additional_section_1_data": "199.43.133.53",
        "question_section_0_name": "example.com.",
        "question_section_0_class": "IN",
        "question_section_0_type": "A",
        "question_section_1_name": "example.com.",
        "question_section_1_class": "IN",
        "question_section_1_type": "AAAA",
        "query_time_ms": random.randint(10, 100),
        "server_ip": "8.8.8.8",
        "server_port": 53,
        "when": datetime.now().strftime("%a %b %d %H:%M:%S %Y"),
        "msg_size_rcvd": 156,
        "status": "NOERROR",
        "opcode": "QUERY",
        "flags_0": "qr",
        "flags_1": "rd",
        "edns_version": 0,
        "edns_flags": 0,
        "edns_udp": 512,
    }


def osint_server_dig_lookup(target: str) -> Dict[str, Any]:
    """
    Performs a DNS lookup (dig-style) for the given target domain.

    Args:
        target (str): The domain name or IP address to perform DNS lookup on.

    Returns:
        Dict containing DNS response data with the following structure:
        - answer_section (List[Dict]): List of DNS answer records with 'name', 'ttl', 'class', 'type', 'data'
        - authority_section (List[Dict]): List of DNS authority records with 'name', 'ttl', 'class', 'type', 'data'
        - additional_section (List[Dict]): List of additional DNS records with 'name', 'ttl', 'class', 'type', 'data'
        - question_section (List[Dict]): List of question records with 'name', 'class', 'type'
        - query_time_ms (int): Time in milliseconds the query took
        - server_ip (str): IP address of DNS server used
        - server_port (int): Port number of DNS server
        - when (str): Timestamp of query execution
        - msg_size_rcvd (int): Size of received message in bytes
        - status (str): Response status from DNS server
        - opcode (str): Operation code of the query
        - flags (List[str]): List of DNS header flags
        - edns (Dict): EDNS information with 'version', 'flags', 'udp'

    Raises:
        ValueError: If target is empty or None
    """
    if not target or not target.strip():
        raise ValueError("Target parameter is required and cannot be empty")

    target = target.strip()

    # Fetch simulated external API data
    api_data = call_external_api("osint_server_dig_lookup")

    # Construct answer section
    answer_section = [
        {
            "name": api_data["answer_section_0_name"],
            "ttl": api_data["answer_section_0_ttl"],
            "class": api_data["answer_section_0_class"],
            "type": api_data["answer_section_0_type"],
            "data": api_data["answer_section_0_data"],
        },
        {
            "name": api_data["answer_section_1_name"],
            "ttl": api_data["answer_section_1_ttl"],
            "class": api_data["answer_section_1_class"],
            "type": api_data["answer_section_1_type"],
            "data": api_data["answer_section_1_data"],
        },
    ]

    # Construct authority section
    authority_section = [
        {
            "name": api_data["authority_section_0_name"],
            "ttl": api_data["authority_section_0_ttl"],
            "class": api_data["authority_section_0_class"],
            "type": api_data["authority_section_0_type"],
            "data": api_data["authority_section_0_data"],
        },
        {
            "name": api_data["authority_section_1_name"],
            "ttl": api_data["authority_section_1_ttl"],
            "class": api_data["authority_section_1_class"],
            "type": api_data["authority_section_1_type"],
            "data": api_data["authority_section_1_data"],
        },
    ]

    # Construct additional section
    additional_section = [
        {
            "name": api_data["additional_section_0_name"],
            "ttl": api_data["additional_section_0_ttl"],
            "class": api_data["additional_section_0_class"],
            "type": api_data["additional_section_0_type"],
            "data": api_data["additional_section_0_data"],
        },
        {
            "name": api_data["additional_section_1_name"],
            "ttl": api_data["additional_section_1_ttl"],
            "class": api_data["additional_section_1_class"],
            "type": api_data["additional_section_1_type"],
            "data": api_data["additional_section_1_data"],
        },
    ]

    # Construct question section
    question_section = [
        {
            "name": api_data["question_section_0_name"],
            "class": api_data["question_section_0_class"],
            "type": api_data["question_section_0_type"],
        },
        {
            "name": api_data["question_section_1_name"],
            "class": api_data["question_section_1_class"],
            "type": api_data["question_section_1_type"],
        },
    ]

    # Construct flags list
    flags = []
    if "flags_0" in api_data and api_data["flags_0"]:
        flags.append(api_data["flags_0"])
    if "flags_1" in api_data and api_data["flags_1"]:
        flags.append(api_data["flags_1"])

    # Construct edns info
    edns = {
        "version": api_data["edns_version"],
        "flags": api_data["edns_flags"],
        "udp": api_data["edns_udp"],
    }

    # Return structured response
    return {
        "answer_section": answer_section,
        "authority_section": authority_section,
        "additional_section": additional_section,
        "question_section": question_section,
        "query_time_ms": api_data["query_time_ms"],
        "server_ip": api_data["server_ip"],
        "server_port": api_data["server_port"],
        "when": api_data["when"],
        "msg_size_rcvd": api_data["msg_size_rcvd"],
        "status": api_data["status"],
        "opcode": api_data["opcode"],
        "flags": flags,
        "edns": edns,
    }