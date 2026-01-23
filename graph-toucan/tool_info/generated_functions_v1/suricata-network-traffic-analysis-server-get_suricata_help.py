from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Suricata help information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - help_text (str): Complete help text output from the Suricata command-line tool
        - available_mode_0 (str): First operational mode supported by Suricata
        - available_mode_1 (str): Second operational mode supported by Suricata
        - supported_option_0_option (str): First command-line option flag
        - supported_option_0_description (str): Description of the first command-line option
        - supported_option_0_expected_value (str): Expected value type for the first option (or empty if none)
        - supported_option_1_option (str): Second command-line option flag
        - supported_option_1_description (str): Description of the second command-line option
        - supported_option_1_expected_value (str): Expected value type for the second option (or empty if none)
        - example_command_0 (str): First example command line from help
        - example_command_1 (str): Second example command line from help
        - version_info (str): Version string of the Suricata binary
        - documentation_link_0 (str): First URL to external documentation
        - documentation_link_1 (str): Second URL to external documentation
        - error (str): Error message if help command failed, otherwise empty string
    """
    return {
        "help_text": (
            "Suricata - Network Threat Detection Engine\n"
            "Usage: suricata [OPTIONS]\n"
            "  -c CONFIG_FILE    Path to configuration file\n"
            "  -i INTERFACE      Interface to capture packets from\n"
            "  -r PCAP_FILE      Read packets from PCAP file\n"
            "Modes: ids, nfq, af-packet\n"
            "Examples:\n"
            "  suricata -c suricata.yaml -i eth0\n"
            "  suricata -r traffic.pcap\n"
            "For more info: https://suricata.io/docs\n"
            "Version 6.0.9"
        ),
        "available_mode_0": "ids",
        "available_mode_1": "nfq",
        "supported_option_0_option": "-c",
        "supported_option_0_description": "Path to configuration file",
        "supported_option_0_expected_value": "CONFIG_FILE",
        "supported_option_1_option": "-i",
        "supported_option_1_description": "Interface to capture packets from",
        "supported_option_1_expected_value": "INTERFACE",
        "example_command_0": "suricata -c suricata.yaml -i eth0",
        "example_command_1": "suricata -r traffic.pcap",
        "version_info": "Version 6.0.9",
        "documentation_link_0": "https://suricata.io/docs",
        "documentation_link_1": "https://github.com/OISF/suricata",
        "error": ""
    }

def suricata_network_traffic_analysis_server_get_suricata_help() -> Dict[str, Any]:
    """
    Retrieves and parses the help output from the Suricata command-line tool.
    
    This function simulates executing 'suricata --help' or similar to retrieve usage
    instructions, available modes, supported options, examples, version, and documentation
    links. It parses the help text into structured data.

    Returns:
        Dict containing:
        - help_text (str): Full help text from Suricata
        - available_modes (List[str]): List of operational modes (e.g., 'ids', 'nfq')
        - supported_options (List[Dict]): List of dicts with 'option', 'description', 'expected_value'
        - example_commands (List[str]): List of example command lines
        - version_info (str): Suricata version string
        - documentation_links (List[str]): List of relevant documentation URLs
        - error (str): Error message if help retrieval failed, else None
    """
    try:
        api_data = call_external_api("suricata-network-traffic-analysis-server-get_suricata_help")
        
        # Extract available modes
        available_modes = [
            api_data["available_mode_0"],
            api_data["available_mode_1"]
        ]
        
        # Extract supported options
        supported_options = [
            {
                "option": api_data["supported_option_0_option"],
                "description": api_data["supported_option_0_description"],
                "expected_value": api_data["supported_option_0_expected_value"] or None
            },
            {
                "option": api_data["supported_option_1_option"],
                "description": api_data["supported_option_1_description"],
                "expected_value": api_data["supported_option_1_expected_value"] or None
            }
        ]
        
        # Extract example commands
        example_commands = [
            api_data["example_command_0"],
            api_data["example_command_1"]
        ]
        
        # Extract documentation links
        documentation_links = [
            api_data["documentation_link_0"],
            api_data["documentation_link_1"]
        ]
        
        # Build result dictionary
        result = {
            "help_text": api_data["help_text"],
            "available_modes": available_modes,
            "supported_options": supported_options,
            "example_commands": example_commands,
            "version_info": api_data["version_info"],
            "documentation_links": documentation_links,
            "error": api_data["error"] if api_data["error"] else None
        }
        
        return result
        
    except Exception as e:
        return {
            "help_text": "",
            "available_modes": [],
            "supported_options": [],
            "example_commands": [],
            "version_info": "",
            "documentation_links": [],
            "error": f"Failed to retrieve Suricata help: {str(e)}"
        }