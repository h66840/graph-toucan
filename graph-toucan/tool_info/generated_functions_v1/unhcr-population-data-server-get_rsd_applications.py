from typing import Dict, Any, Optional, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching RSD applications data from UNHCR API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - page (int): current page number of the response
        - maxPages (int): total number of pages available for the query
        - short_url (str): short identifier for the query result
        - total_applied (int): total number of applications across all items
        - item_0_year (int): year of the first application record
        - item_0_coo_id (int): numeric ID of the country of origin for first item
        - item_0_coa_id (int): numeric ID of the country of asylum for first item
        - item_0_coo_name (str): name of the country of origin for first item
        - item_0_coa_name (str): name of the country of asylum for first item
        - item_0_coo (str): legacy code for country of origin (first item)
        - item_0_coa (str): legacy code for country of asylum (first item)
        - item_0_coo_iso (str): ISO3 code of the country of origin (first item)
        - item_0_coa_iso (str): ISO3 code of the country of asylum (first item)
        - item_0_procedure_type (str): type of asylum procedure (first item)
        - item_0_app_type (str): application type (first item)
        - item_0_dec_level (str): decision level (first item)
        - item_0_app_pc (str): applicant population category (first item)
        - item_0_applied (int): number of applications in first item
        - item_1_year (int): year of the second application record
        - item_1_coo_id (int): numeric ID of the country of origin for second item
        - item_1_coa_id (int): numeric ID of the country of asylum for second item
        - item_1_coo_name (str): name of the country of origin for second item
        - item_1_coa_name (str): name of the country of asylum for second item
        - item_1_coo (str): legacy code for country of origin (second item)
        - item_1_coa (str): legacy code for country of asylum (second item)
        - item_1_coo_iso (str): ISO3 code of the country of origin (second item)
        - item_1_coa_iso (str): ISO3 code of the country of asylum (second item)
        - item_1_procedure_type (str): type of asylum procedure (second item)
        - item_1_app_type (str): application type (second item)
        - item_1_dec_level (str): decision level (second item)
        - item_1_app_pc (str): applicant population category (second item)
        - item_1_applied (int): number of applications in second item
    """
    return {
        "page": 1,
        "maxPages": 1,
        "short_url": "rsd2024deusy",
        "total_applied": 15000,
        "item_0_year": 2024,
        "item_0_coo_id": 800,
        "item_0_coa_id": 276,
        "item_0_coo_name": "Syrian Arab Republic",
        "item_0_coa_name": "Germany",
        "item_0_coo": "SYR",
        "item_0_coa": "DEU",
        "item_0_coo_iso": "SYR",
        "item_0_coa_iso": "DEU",
        "item_0_procedure_type": "G",
        "item_0_app_type": "N",
        "item_0_dec_level": "FI",
        "item_0_app_pc": "P",
        "item_0_applied": 12000,
        "item_1_year": 2024,
        "item_1_coo_id": 800,
        "item_1_coa_id": 626,
        "item_1_coo_name": "Syrian Arab Republic",
        "item_1_coa_name": "Turkey",
        "item_1_coo": "SYR",
        "item_1_coa": "TUR",
        "item_1_coo_iso": "SYR",
        "item_1_coa_iso": "TUR",
        "item_1_procedure_type": "G",
        "item_1_app_type": "N",
        "item_1_dec_level": "FI",
        "item_1_app_pc": "P",
        "item_1_applied": 3000
    }

def unhcr_population_data_server_get_rsd_applications(
    coo: Optional[str] = None,
    coa: Optional[str] = None,
    year: Optional[str] = None,
    coo_all: Optional[bool] = False,
    coa_all: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get RSD application data from UNHCR.
    
    Args:
        coo: Country of origin filter (ISO3 code, comma-separated for multiple)
        coa: Country of asylum filter (ISO3 code, comma-separated for multiple)
        year: Year filter (comma-separated for multiple years), defaults to 2024 if not provided
        coo_all: Set to True when analyzing the ORIGIN COUNTRIES of asylum seekers
        coa_all: Set to True when analyzing the ASYLUM COUNTRIES where applications were filed
    
    Returns:
        UNHCR RSD Applications data structured as:
        {
            "page": int,
            "maxPages": int,
            "short-url": str,
            "total": {"applied": int},
            "items": [
                {
                    "year": int,
                    "coo_id": int,
                    "coa_id": int,
                    "coo_name": str,
                    "coa_name": str,
                    "coo": str,
                    "coa": str,
                    "coo_iso": str,
                    "coa_iso": str,
                    "procedure_type": str,
                    "app_type": str,
                    "dec_level": str,
                    "app_pc": str,
                    "applied": int
                },
                ...
            ]
        }
    
    Raises:
        ValueError: If invalid parameters are provided
    """
    # Input validation
    if not isinstance(coo_all, bool) and coo_all is not None:
        raise ValueError("coo_all must be a boolean value")
    if not isinstance(coa_all, bool) and coa_all is not None:
        raise ValueError("coa_all must be a boolean value")
    
    if year is not None and not isinstance(year, str):
        raise ValueError("year must be a string of comma-separated years")
    if coo is not None and not isinstance(coo, str):
        raise ValueError("coo must be a string of comma-separated ISO3 codes")
    if coa is not None and not isinstance(coa, str):
        raise ValueError("coa must be a string of comma-separated ISO3 codes")
    
    # Default year to 2024 if not provided
    if year is None:
        year = "2024"
    
    # Call external API to get flat data
    api_data = call_external_api("unhcr-population-data-server-get_rsd_applications")
    
    # Construct nested structure matching output schema
    result = {
        "page": api_data["page"],
        "maxPages": api_data["maxPages"],
        "short-url": api_data["short_url"],
        "total": {
            "applied": api_data["total_applied"]
        },
        "items": [
            {
                "year": api_data["item_0_year"],
                "coo_id": api_data["item_0_coo_id"],
                "coa_id": api_data["item_0_coa_id"],
                "coo_name": api_data["item_0_coo_name"],
                "coa_name": api_data["item_0_coa_name"],
                "coo": api_data["item_0_coo"],
                "coa": api_data["item_0_coa"],
                "coo_iso": api_data["item_0_coo_iso"],
                "coa_iso": api_data["item_0_coa_iso"],
                "procedure_type": api_data["item_0_procedure_type"],
                "app_type": api_data["item_0_app_type"],
                "dec_level": api_data["item_0_dec_level"],
                "app_pc": api_data["item_0_app_pc"],
                "applied": api_data["item_0_applied"]
            },
            {
                "year": api_data["item_1_year"],
                "coo_id": api_data["item_1_coo_id"],
                "coa_id": api_data["item_1_coa_id"],
                "coo_name": api_data["item_1_coo_name"],
                "coa_name": api_data["item_1_coa_name"],
                "coo": api_data["item_1_coo"],
                "coa": api_data["item_1_coa"],
                "coo_iso": api_data["item_1_coo_iso"],
                "coa_iso": api_data["item_1_coa_iso"],
                "procedure_type": api_data["item_1_procedure_type"],
                "app_type": api_data["item_1_app_type"],
                "dec_level": api_data["item_1_dec_level"],
                "app_pc": api_data["item_1_app_pc"],
                "applied": api_data["item_1_applied"]
            }
        ]
    }
    
    return result