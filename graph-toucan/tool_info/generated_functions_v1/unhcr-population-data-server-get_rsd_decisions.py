from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching RSD decision data from UNHCR API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - page (int): Current page number
        - maxPages (int): Total number of pages available
        - total_dec_recognized (int): Total recognized decisions
        - total_dec_other (int): Total otherwise closed decisions
        - total_dec_rejected (int): Total rejected decisions
        - total_dec_closed (int): Total closed decisions
        - total_dec_total (int): Total number of decisions
        - item_0_year (int): Year of first decision record
        - item_0_coo_iso (str): Country of origin ISO code for first item
        - item_0_coo_name (str): Country of origin name for first item
        - item_0_coa_iso (str): Country of asylum ISO code for first item
        - item_0_coa_name (str): Country of asylum name for first item
        - item_0_proc_type (str): Procedure type for first item
        - item_0_dec_level (str): Decision level for first item
        - item_0_dec_cat (str): Decision category for first item
        - item_0_dec_recognized (int): Recognized count for first item
        - item_0_dec_other (int): Otherwise closed count for first item
        - item_0_dec_rejected (int): Rejected count for first item
        - item_0_dec_closed (int): Closed count for first item
        - item_0_dec_total (int): Total decisions for first item
        - item_1_year (int): Year of second decision record
        - item_1_coo_iso (str): Country of origin ISO code for second item
        - item_1_coo_name (str): Country of origin name for second item
        - item_1_coa_iso (str): Country of asylum ISO code for second item
        - item_1_coa_name (str): Country of asylum name for second item
        - item_1_proc_type (str): Procedure type for second item
        - item_1_dec_level (str): Decision level for second item
        - item_1_dec_cat (str): Decision category for second item
        - item_1_dec_recognized (int): Recognized count for second item
        - item_1_dec_other (int): Otherwise closed count for second item
        - item_1_dec_rejected (int): Rejected count for second item
        - item_1_dec_closed (int): Closed count for second item
        - item_1_dec_total (int): Total decisions for second item
    """
    return {
        "page": 1,
        "maxPages": 3,
        "total_dec_recognized": 15000,
        "total_dec_other": 3500,
        "total_dec_rejected": 8200,
        "total_dec_closed": 26700,
        "total_dec_total": 26700,
        "item_0_year": 2024,
        "item_0_coo_iso": "SYR",
        "item_0_coo_name": "Syria",
        "item_0_coa_iso": "DEU",
        "item_0_coa_name": "Germany",
        "item_0_proc_type": "Individual",
        "item_0_dec_level": "First Instance",
        "item_0_dec_cat": "Positive",
        "item_0_dec_recognized": 4200,
        "item_0_dec_other": 800,
        "item_0_dec_rejected": 1900,
        "item_0_dec_closed": 6900,
        "item_0_dec_total": 6900,
        "item_1_year": 2024,
        "item_1_coo_iso": "AFG",
        "item_1_coo_name": "Afghanistan",
        "item_1_coa_iso": "TUR",
        "item_1_coa_name": "Turkey",
        "item_1_proc_type": "Individual",
        "item_1_dec_level": "First Instance",
        "item_1_dec_cat": "Negative",
        "item_1_dec_recognized": 1800,
        "item_1_dec_other": 450,
        "item_1_dec_rejected": 3200,
        "item_1_dec_closed": 5450,
        "item_1_dec_total": 5450,
    }

def unhcr_population_data_server_get_rsd_decisions(
    coo: Optional[str] = None,
    coa: Optional[str] = None,
    year: Optional[str] = None,
    coo_all: Optional[bool] = False,
    coa_all: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get Refugee Status Determination (RSD) decision data from UNHCR.
    
    Args:
        coo: Country of origin filter (ISO3 code, comma-separated for multiple)
             Example: "SYR" for Syria, "AFG,IRQ" for Afghanistan and Iraq
        coa: Country of asylum filter (ISO3 code, comma-separated for multiple)
             Example: "DEU" for Germany, "FRA,ITA" for France and Italy
        year: Year filter (comma-separated for multiple years), defaults to 2024 if not provided
        coo_all: Set to True when analyzing decisions breakdown BY NATIONALITY of asylum seekers
        coa_all: Set to True when analyzing decisions breakdown BY COUNTRY where decisions were made
    
    Returns:
        Dict containing:
        - page (int): current page number in paginated response
        - maxPages (int): total number of pages available in the response
        - total (Dict): aggregate totals with keys 'dec_recognized', 'dec_other', 'dec_rejected', 
                       'dec_closed', 'dec_total'
        - items (List[Dict]): list of individual decision records with detailed attributes
    """
    # Input validation
    if not isinstance(coo_all, bool) and coo_all is not None:
        raise ValueError("coo_all must be a boolean or None")
    if not isinstance(coa_all, bool) and coa_all is not None:
        raise ValueError("coa_all must be a boolean or None")
    
    if year is None:
        year = "2024"
    
    # Call external API to get flattened data
    api_data = call_external_api("unhcr-population-data-server-get_rsd_decisions")
    
    # Construct nested structure matching output schema
    result = {
        "page": api_data["page"],
        "maxPages": api_data["maxPages"],
        "total": {
            "dec_recognized": api_data["total_dec_recognized"],
            "dec_other": api_data["total_dec_other"],
            "dec_rejected": api_data["total_dec_rejected"],
            "dec_closed": api_data["total_dec_closed"],
            "dec_total": api_data["total_dec_total"]
        },
        "items": [
            {
                "year": api_data["item_0_year"],
                "coo": {
                    "iso": api_data["item_0_coo_iso"],
                    "name": api_data["item_0_coo_name"]
                },
                "coa": {
                    "iso": api_data["item_0_coa_iso"],
                    "name": api_data["item_0_coa_name"]
                },
                "proc_type": api_data["item_0_proc_type"],
                "dec_level": api_data["item_0_dec_level"],
                "dec_cat": api_data["item_0_dec_cat"],
                "dec_recognized": api_data["item_0_dec_recognized"],
                "dec_other": api_data["item_0_dec_other"],
                "dec_rejected": api_data["item_0_dec_rejected"],
                "dec_closed": api_data["item_0_dec_closed"],
                "dec_total": api_data["item_0_dec_total"]
            },
            {
                "year": api_data["item_1_year"],
                "coo": {
                    "iso": api_data["item_1_coo_iso"],
                    "name": api_data["item_1_coo_name"]
                },
                "coa": {
                    "iso": api_data["item_1_coa_iso"],
                    "name": api_data["item_1_coa_name"]
                },
                "proc_type": api_data["item_1_proc_type"],
                "dec_level": api_data["item_1_dec_level"],
                "dec_cat": api_data["item_1_dec_cat"],
                "dec_recognized": api_data["item_1_dec_recognized"],
                "dec_other": api_data["item_1_dec_other"],
                "dec_rejected": api_data["item_1_dec_rejected"],
                "dec_closed": api_data["item_1_dec_closed"],
                "dec_total": api_data["item_1_dec_total"]
            }
        ]
    }
    
    return result