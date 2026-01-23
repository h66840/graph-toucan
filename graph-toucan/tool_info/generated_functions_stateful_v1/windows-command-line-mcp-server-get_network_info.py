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
    Simulates fetching network information from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - interface_0_index (int): Index of first network interface
        - interface_0_name (str): Name of first network interface
        - interface_0_flags (str): Flags of first network interface
        - interface_0_mtu (int): MTU of first network interface
        - interface_0_state (str): State of first network interface
        - interface_0_qlen (int): Transmit queue length of first interface
        - interface_0_link_type (str): Link type of first interface
        - interface_0_link_mac (str): MAC address of first interface
        - interface_0_link_brd (str): Broadcast address of first interface
        - interface_0_inet_addresses_0 (str): First IPv4 address of first interface
        - interface_0_inet_addresses_1 (str): Second IPv4 address of first interface
        - interface_0_inet6_addresses_0 (str): First IPv6 address of first interface
        - interface_0_inet6_addresses_1 (str): Second IPv6 address of first interface
        - interface_1_index (int): Index of second network interface
        - interface_1_name (str): Name of second network interface
        - interface_1_flags (str): Flags of second network interface
        - interface_1_mtu (int): MTU of second network interface
        - interface_1_state (str): State of second network interface
        - interface_1_qlen (int): Transmit queue length of second interface
        - interface_1_link_type (str): Link type of second interface
        - interface_1_link_mac (str): MAC address of second interface
        - interface_1_link_brd (str): Broadcast address of second interface
        - interface_1_inet_addresses_0 (str): First IPv4 address of second interface
        - interface_1_inet_addresses_1 (str): Second IPv4 address of second interface
        - interface_1_inet6_addresses_0 (str): First IPv6 address of second interface
        - interface_1_inet6_addresses_1 (str): Second IPv6 address of second interface
    """
    return {
        "interface_0_index": 1,
        "interface_0_name": "Ethernet",
        "interface_0_flags": "UP,BROADCAST,RUNNING,MULTICAST",
        "interface_0_mtu": 1500,
        "interface_0_state": "up",
        "interface_0_qlen": 1000,
        "interface_0_link_type": "ether",
        "interface_0_link_mac": "00:1A:2B:3C:4D:5E",
        "interface_0_link_brd": "ff:ff:ff:ff:ff:ff",
        "interface_0_inet_addresses_0": "192.168.1.100",
        "interface_0_inet_addresses_1": "192.168.1.101",
        "interface_0_inet6_addresses_0": "fe80::1a2b:3cff:fe4c:4d5e",
        "interface_0_inet6_addresses_1": "2001:db8::1",
        "interface_1_index": 2,
        "interface_1_name": "Wi-Fi",
        "interface_1_flags": "UP,BROADCAST,RUNNING,MULTICAST",
        "interface_1_mtu": 1500,
        "interface_1_state": "up",
        "interface_1_qlen": 1000,
        "interface_1_link_type": "ether",
        "interface_1_link_mac": "00:2A:3B:4C:5D:6F",
        "interface_1_link_brd": "ff:ff:ff:ff:ff:ff",
        "interface_1_inet_addresses_0": "192.168.0.105",
        "interface_1_inet_addresses_1": "192.168.0.106",
        "interface_1_inet6_addresses_0": "fe80::2a3b:4cff:fe5c:5d6f",
        "interface_1_inet6_addresses_1": "2001:db8::2"
    }

def windows_command_line_mcp_server_get_network_info(networkInterface: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve network configuration information including IP addresses, adapters, and DNS settings.
    Can be filtered to a specific interface.
    
    Args:
        networkInterface (Optional[str]): Optional interface name to filter results
        
    Returns:
        Dict containing a list of network interfaces with detailed configuration:
        - interfaces (List[Dict]): list of network interfaces, each with:
            - index (int)
            - name (str)
            - flags (str)
            - mtu (int)
            - state (str)
            - qlen (int)
            - link_type (str)
            - link_mac (str)
            - link_brd (str)
            - inet_addresses (List[str]): IPv4 addresses
            - inet6_addresses (List[str]): IPv6 addresses
    """
    # Fetch data from simulated external API
    api_data = call_external_api("windows-command-line-mcp-server-get_network_info", **locals())
    
    # Construct interfaces list
    interfaces = []
    
    # Process first interface
    if (f"interface_0_name" in api_data and 
        (networkInterface is None or api_data[f"interface_0_name"] == networkInterface)):
        interface_0 = {
            "index": api_data["interface_0_index"],
            "name": api_data["interface_0_name"],
            "flags": api_data["interface_0_flags"],
            "mtu": api_data["interface_0_mtu"],
            "state": api_data["interface_0_state"],
            "qlen": api_data["interface_0_qlen"],
            "link_type": api_data["interface_0_link_type"],
            "link_mac": api_data["interface_0_link_mac"],
            "link_brd": api_data["interface_0_link_brd"],
            "inet_addresses": [
                api_data["interface_0_inet_addresses_0"],
                api_data["interface_0_inet_addresses_1"]
            ],
            "inet6_addresses": [
                api_data["interface_0_inet6_addresses_0"],
                api_data["interface_0_inet6_addresses_1"]
            ]
        }
        interfaces.append(interface_0)
    
    # Process second interface
    if (f"interface_1_name" in api_data and 
        (networkInterface is None or api_data[f"interface_1_name"] == networkInterface)):
        interface_1 = {
            "index": api_data["interface_1_index"],
            "name": api_data["interface_1_name"],
            "flags": api_data["interface_1_flags"],
            "mtu": api_data["interface_1_mtu"],
            "state": api_data["interface_1_state"],
            "qlen": api_data["interface_1_qlen"],
            "link_type": api_data["interface_1_link_type"],
            "link_mac": api_data["interface_1_link_mac"],
            "link_brd": api_data["interface_1_link_brd"],
            "inet_addresses": [
                api_data["interface_1_inet_addresses_0"],
                api_data["interface_1_inet_addresses_1"]
            ],
            "inet6_addresses": [
                api_data["interface_1_inet6_addresses_0"],
                api_data["interface_1_inet6_addresses_1"]
            ]
        }
        interfaces.append(interface_1)
    
    return {"interfaces": interfaces}

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
