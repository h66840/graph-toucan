from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for domain availability check.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the domain (e.g., "UNAVAILABLE", "AVAILABLE")
        - suggested_domain_0 (str): First suggested available .br domain name
        - suggested_domain_1 (str): Second suggested available .br domain name
    """
    return {
        "status": "UNAVAILABLE",
        "suggested_domain_0": "exemplo1.br",
        "suggested_domain_1": "exemplo2.br"
    }

def brasil_api_registrobr_domain_check(domain: str) -> Dict[str, Any]:
    """
    Check the status and availability of a .br domain name.
    
    Args:
        domain (str): Domain name to check (with or without .br extension)
    
    Returns:
        Dict containing:
        - status (str): Status of the domain (e.g., "UNAVAILABLE", "AVAILABLE")
        - suggested_domains (List[str]): List of suggested available .br domain names that can be registered
    
    Raises:
        ValueError: If domain is empty or not a string
    """
    if not domain:
        raise ValueError("Domain parameter is required")
    
    if not isinstance(domain, str):
        raise ValueError("Domain must be a string")
    
    # Normalize domain by removing .br if present
    normalized_domain = domain.lower().rstrip('.br')
    
    # Call external API to get data
    api_data = call_external_api("brasil-api-registrobr-domain-check")
    
    # Construct result with proper nested structure
    result = {
        "status": api_data["status"],
        "suggested_domains": [
            api_data["suggested_domain_0"],
            api_data["suggested_domain_1"]
        ]
    }
    
    return result