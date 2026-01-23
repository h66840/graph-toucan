from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for domain availability check.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - available (bool): Whether the domain is available
        - domain (str): The domain name checked
        - suggestion_0 (str): First alternative domain suggestion
        - suggestion_1 (str): Second alternative domain suggestion
        - pricing_registration (float): Registration price
        - pricing_renewal (float): Renewal price
        - pricing_currency (str): Currency code (e.g., USD)
        - pricing_period_years (int): Registration period in years
        - tld_info_is_open (bool): Whether TLD is open for public registration
        - tld_info_restriction_notes (str): Notes about TLD restrictions
        - check_timestamp (str): ISO 8601 timestamp of check
        - error (str): Error message if any, otherwise null
    """
    return {
        "available": False,
        "domain": "example.com",
        "suggestion_0": "example.net",
        "suggestion_1": "example.org",
        "pricing_registration": 12.99,
        "pricing_renewal": 14.99,
        "pricing_currency": "USD",
        "pricing_period_years": 1,
        "tld_info_is_open": True,
        "tld_info_restriction_notes": "No special restrictions",
        "check_timestamp": datetime.utcnow().isoformat() + "Z",
        "error": None,
    }


def domain_search_no_api_key_required_check_domain_availability(domain: str) -> Dict[str, Any]:
    """
    Check if a domain name is available for registration and get pricing information.

    Args:
        domain (str): Domain name to check (e.g., "example.com", "mydomain.org")

    Returns:
        Dict containing:
        - available (bool): Whether the domain name is available for registration
        - domain (str): The domain name that was checked
        - suggestions (List[str]): Alternative available domain names if the requested domain is taken
        - pricing (Dict): Pricing information with keys 'registration', 'renewal', 'currency', 'period_years'
        - tld_info (Dict): Information about the top-level domain including availability rules and restrictions
        - check_timestamp (str): Timestamp when the availability check was performed (ISO 8601 format)
        - error (str): Error message if the check failed, otherwise None
    """
    if not domain or not isinstance(domain, str):
        return {
            "available": False,
            "domain": "",
            "suggestions": [],
            "pricing": {
                "registration": 0.0,
                "renewal": 0.0,
                "currency": "USD",
                "period_years": 1
            },
            "tld_info": {
                "is_open": False,
                "restriction_notes": "Invalid domain input"
            },
            "check_timestamp": datetime.utcnow().isoformat() + "Z",
            "error": "Domain name is required and must be a non-empty string"
        }

    try:
        api_data = call_external_api("domain-search---no-api-key-required.-check_domain_availability")

        # Construct suggestions list from indexed fields
        suggestions = []
        if "suggestion_0" in api_data and api_data["suggestion_0"]:
            suggestions.append(api_data["suggestion_0"])
        if "suggestion_1" in api_data and api_data["suggestion_1"]:
            suggestions.append(api_data["suggestion_1"])

        # Construct pricing dict
        pricing = {
            "registration": api_data.get("pricing_registration", 0.0),
            "renewal": api_data.get("pricing_renewal", 0.0),
            "currency": api_data.get("pricing_currency", "USD"),
            "period_years": api_data.get("pricing_period_years", 1)
        }

        # Construct tld_info dict
        tld_info = {
            "is_open": api_data.get("tld_info_is_open", False),
            "restriction_notes": api_data.get("tld_info_restriction_notes", "")
        }

        result = {
            "available": api_data["available"],
            "domain": domain,  # Use input domain, not the one from API mock
            "suggestions": suggestions,
            "pricing": pricing,
            "tld_info": tld_info,
            "check_timestamp": api_data["check_timestamp"],
            "error": api_data["error"]
        }

        return result

    except Exception as e:
        return {
            "available": False,
            "domain": domain,
            "suggestions": [],
            "pricing": {
                "registration": 0.0,
                "renewal": 0.0,
                "currency": "USD",
                "period_years": 1
            },
            "tld_info": {
                "is_open": False,
                "restriction_notes": ""
            },
            "check_timestamp": datetime.utcnow().isoformat() + "Z",
            "error": f"An unexpected error occurred: {str(e)}"
        }