from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Suricata version information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - version (str): The full Suricata version string
        - major (int): The major version number of Suricata
        - minor (int): The minor version number of Suricata
        - patch (int): The patch version number of Suricata
        - release_type (str): Indicates the release type (e.g., 'stable', 'beta', 'rc')
        - build_info_compiler (str): Compiler used during build
        - build_info_architecture (str): Target architecture of the build
        - build_info_built_with (str): Features the software was built with
        - build_info_enabled_features (str): Features enabled at runtime
        - success (bool): Whether version retrieval was successful
        - error_message (str): Error message if version retrieval failed, otherwise null
    """
    return {
        "version": "7.0.0",
        "major": 7,
        "minor": 0,
        "patch": 0,
        "release_type": "stable",
        "build_info_compiler": "gcc 9.4.0",
        "build_info_architecture": "x86_64",
        "build_info_built_with": "libpcap, libnet, libyaml, hiredis",
        "build_info_enabled_features": "af-packet, nfqueue, tls, http2, json",
        "success": True,
        "error_message": None
    }

def suricata_network_traffic_analysis_server_get_suricata_version() -> Dict[str, Any]:
    """
    Retrieves the Suricata version information including detailed build metadata.
    
    This function queries an external API to get Suricata version details and formats
    the response according to the expected schema, reconstructing nested structures
    from flat fields returned by the API.

    Returns:
        Dict containing:
        - version (str): Full Suricata version string (e.g., '7.0.0')
        - major (int): Major version number
        - minor (int): Minor version number
        - patch (int): Patch version number
        - release_type (str): Release type ('stable', 'beta', 'rc')
        - build_info (Dict): Build-time information with keys:
            - compiler (str): Compiler used
            - architecture (str): Target architecture
            - built_with (str): Features it was built with
            - enabled_features (str): Enabled runtime features
        - success (bool): Whether retrieval was successful
        - error_message (str): Error message if failed, else None
    """
    try:
        api_data = call_external_api("suricata-network-traffic-analysis-server-get_suricata_version")
        
        # Construct build_info dictionary from flattened fields
        build_info = {
            "compiler": api_data["build_info_compiler"],
            "architecture": api_data["build_info_architecture"],
            "built_with": api_data["build_info_built_with"],
            "enabled_features": api_data["build_info_enabled_features"]
        }
        
        # Construct final result matching output schema
        result = {
            "version": api_data["version"],
            "major": api_data["major"],
            "minor": api_data["minor"],
            "patch": api_data["patch"],
            "release_type": api_data["release_type"],
            "build_info": build_info,
            "success": api_data["success"],
            "error_message": api_data["error_message"]
        }
        
        return result
        
    except KeyError as e:
        return {
            "version": "",
            "major": 0,
            "minor": 0,
            "patch": 0,
            "release_type": "",
            "build_info": {},
            "success": False,
            "error_message": f"Missing expected field in API response: {str(e)}"
        }
    except Exception as e:
        return {
            "version": "",
            "major": 0,
            "minor": 0,
            "patch": 0,
            "release_type": "",
            "build_info": {},
            "success": False,
            "error_message": f"Unexpected error occurred: {str(e)}"
        }