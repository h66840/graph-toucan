from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching WHOIS data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - domain_name (str): the registered domain name as returned by the WHOIS lookup
        - registry_domain_id (str): unique identifier assigned by the registry for the domain
        - registrar_name (str): name of the registrar responsible for the domain registration
        - registrar_iana_id (int): IANA ID of the registrar
        - registrar_url (str): official URL of the registrar
        - registrar_whois_server (str): hostname of the registrar's WHOIS server
        - registrar_abuse_contact_email (str): email address for reporting abuse to the registrar
        - registrar_abuse_contact_phone (str): phone number for reporting abuse to the registrar
        - creation_date (str): date and time when the domain was originally created, in ISO 8601 format
        - updated_date (str): date and time when the domain record was last updated, in ISO 8601 format
        - registry_expiry_date (str): date and time when the domain registration expires, in ISO 8601 format
        - domain_status_0 (str): first EPP status code
        - domain_status_1 (str): second EPP status code
        - name_servers_0 (str): first authoritative name server
        - name_servers_1 (str): second authoritative name server
        - dnssec (str): indicates whether DNSSEC is enabled for the domain
        - registrant_organization (str): organization name of the registrant
        - registrant_country (str): two-letter country code of the registrant’s registered location
        - registrant_state_province (str): state or province of the registrant
        - registrant_city (str): city of the registrant
        - registrant_email (str): contact email of the registrant
        - admin_organization (str): organization name of the administrative contact
        - admin_country (str): two-letter country code of the administrative contact
        - tech_organization (str): organization name of the technical contact
        - tech_country (str): two-letter country code of the technical contact
        - billing_organization (str): organization name of the billing contact
        - billing_country (str): two-letter country code of the billing contact
        - last_whois_update (str): timestamp of the last update to the WHOIS database
        - raw_response (str): full unstructured text response from the WHOIS server
        - is_registered (bool): indicates whether the domain is currently registered
    """
    fake_data = {
        "domain_name": "example.com",
        "registry_domain_id": "2345678-EXAMPLE",
        "registrar_name": "Example Registrar, Inc.",
        "registrar_iana_id": 12345,
        "registrar_url": "https://www.example-registrar.com",
        "registrar_whois_server": "whois.example-registrar.com",
        "registrar_abuse_contact_email": "abuse@example-registrar.com",
        "registrar_abuse_contact_phone": "+1.5551234567",
        "creation_date": (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "registry_expiry_date": (datetime.now() + timedelta(days=335)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "domain_status_0": "clientTransferProhibited",
        "domain_status_1": "serverUpdateProhibited",
        "name_servers_0": "ns1.example.com",
        "name_servers_1": "ns2.example.com",
        "dnssec": "unsigned",
        "registrant_organization": "Example Corp",
        "registrant_country": "US",
        "registrant_state_province": "California",
        "registrant_city": "San Francisco",
        "registrant_email": "contact@example.com",
        "admin_organization": "Admin Services Department",
        "admin_country": "US",
        "tech_organization": "Tech Operations Team",
        "tech_country": "US",
        "billing_organization": "Billing Department",
        "billing_country": "US",
        "last_whois_update": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "raw_response": "Domain Name: example.com\nRegistry Domain ID: 2345678-EXAMPLE\nRegistrar: Example Registrar, Inc.\nWhois Server: whois.example-registrar.com\nReferral URL: https://www.example-registrar.com\nName Server: ns1.example.com\nName Server: ns2.example.com\nDNSSEC: unsigned\nDomain Status: clientTransferProhibited\nDomain Status: serverUpdateProhibited\nRegistry Expiry Date: 2025-08-20T04:00:00Z\nCreation Date: 2022-08-20T04:00:00Z\nUpdated Date: 2023-07-20T05:00:00Z\nRegistrant Organization: Example Corp\nRegistrant State/Province: California\nRegistrant Country: US\nAdmin Organization: Admin Services Department\nAdmin Country: US\nTech Organization: Tech Operations Team\nTech Country: US\nBilling Organization: Billing Department\nBilling Country: US\n",
        "is_registered": True,
    }
    return fake_data


def osint_server_whois_lookup(target: str) -> Dict[str, Any]:
    """
    Performs a WHOIS lookup for the given domain target.

    Args:
        target (str): The domain name to perform WHOIS lookup on.

    Returns:
        Dict containing WHOIS information with the following structure:
        - domain_name (str)
        - registry_domain_id (str)
        - registrar_name (str)
        - registrar_iana_id (str)
        - registrar_url (str)
        - registrar_whois_server (str)
        - registrar_abuse_contact_email (str)
        - registrar_abuse_contact_phone (str)
        - creation_date (str): ISO 8601 format
        - updated_date (str): ISO 8601 format
        - registry_expiry_date (str): ISO 8601 format
        - domain_status (List[str]): list of EPP status codes
        - name_servers (List[str]): list of name servers
        - dnssec (str)
        - registrant_organization (str)
        - registrant_country (str)
        - registrant_state_province (str)
        - registrant_city (str)
        - registrant_email (str)
        - admin_organization (str)
        - admin_country (str)
        - tech_organization (str)
        - tech_country (str)
        - billing_organization (str)
        - billing_country (str)
        - last_whois_update (str): ISO 8601 format
        - raw_response (str)
        - is_registered (bool)
    """
    if not target or not isinstance(target, str) or not target.strip():
        raise ValueError("Target must be a non-empty string.")

    # Normalize target
    domain = target.strip().lower()

    # Simulate external API call
    try:
        api_data = call_external_api("osint-server-whois_lookup")
    except Exception as e:
        return {
            "domain_name": domain,
            "registry_domain_id": None,
            "registrar_name": None,
            "registrar_iana_id": None,
            "registrar_url": None,
            "registrar_whois_server": None,
            "registrar_abuse_contact_email": None,
            "registrar_abuse_contact_phone": None,
            "creation_date": None,
            "updated_date": None,
            "registry_expiry_date": None,
            "domain_status": [],
            "name_servers": [],
            "dnssec": None,
            "registrant_organization": None,
            "registrant_country": None,
            "registrant_state_province": None,
            "registrant_city": None,
            "registrant_email": None,
            "admin_organization": None,
            "admin_country": None,
            "tech_organization": None,
            "tech_country": None,
            "billing_organization": None,
            "billing_country": None,
            "last_whois_update": None,
            "raw_response": f"Error fetching WHOIS data: {str(e)}",
            "is_registered": False,
        }

    # Construct nested output structure from flat API data
    result = {
        "domain_name": api_data.get("domain_name"),
        "registry_domain_id": api_data.get("registry_domain_id"),
        "registrar_name": api_data.get("registrar_name"),
        "registrar_iana_id": str(api_data.get("registrar_iana_id")) if api_data.get("registrar_iana_id") is not None else None,
        "registrar_url": api_data.get("registrar_url"),
        "registrar_whois_server": api_data.get("registrar_whois_server"),
        "registrar_abuse_contact_email": api_data.get("registrar_abuse_contact_email"),
        "registrar_abuse_contact_phone": api_data.get("registrar_abuse_contact_phone"),
        "creation_date": api_data.get("creation_date"),
        "updated_date": api_data.get("updated_date"),
        "registry_expiry_date": api_data.get("registry_expiry_date"),
        "domain_status": [
            api_data.get("domain_status_0"),
            api_data.get("domain_status_1")
        ],
        "name_servers": [
            api_data.get("name_servers_0"),
            api_data.get("name_servers_1")
        ],
        "dnssec": api_data.get("dnssec"),
        "registrant_organization": api_data.get("registrant_organization"),
        "registrant_country": api_data.get("registrant_country"),
        "registrant_state_province": api_data.get("registrant_state_province"),
        "registrant_city": api_data.get("registrant_city"),
        "registrant_email": api_data.get("registrant_email"),
        "admin_organization": api_data.get("admin_organization"),
        "admin_country": api_data.get("admin_country"),
        "tech_organization": api_data.get("tech_organization"),
        "tech_country": api_data.get("tech_country"),
        "billing_organization": api_data.get("billing_organization"),
        "billing_country": api_data.get("billing_country"),
        "last_whois_update": api_data.get("last_whois_update"),
        "raw_response": api_data.get("raw_response"),
        "is_registered": api_data.get("is_registered", False)
    }

    return result