from typing import Dict, Any, Optional, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching refugee population data from UNHCR API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - page (int): current page number of the response
        - maxPages (int): total number of pages available in the response
        - short_url (str): short identifier for the query URL
        - total_0 (str): first total summary entry; typically empty or placeholder
        - total_1 (str): second total summary entry; typically empty or placeholder
        - item_0_year (int): the year of the first data entry
        - item_0_coo_id (int): country of origin numeric ID for first item
        - item_0_coa_id (int): country of asylum numeric ID for first item
        - item_0_coo_name (str): full name of country of origin for first item
        - item_0_coa_name (str): full name of country of asylum for first item
        - item_0_coo (str): legacy code for country of origin for first item
        - item_0_coa (str): legacy code for country of asylum for first item
        - item_0_coo_iso (str): ISO3 code for country of origin for first item
        - item_0_coa_iso (str): ISO3 code for country of asylum for first item
        - item_0_refugees (int): number of recognized refugees in first item
        - item_0_asylum_seekers (int): number of asylum seekers in first item
        - item_0_returned_refugees (int): number of returned refugees in first item
        - item_0_idps (str): number of internally displaced persons in first item as string
        - item_0_returned_idps (str): number of returned IDPs in first item as string
        - item_0_stateless (str): number of stateless individuals in first item as string
        - item_0_ooc (int): number of individuals out of concern in first item
        - item_0_oip (str): number of individuals in protracted situations in first item
        - item_0_hst (str): historical stock total in first item as string
        - item_1_year (int): the year of the second data entry
        - item_1_coo_id (int): country of origin numeric ID for second item
        - item_1_coa_id (int): country of asylum numeric ID for second item
        - item_1_coo_name (str): full name of country of origin for second item
        - item_1_coa_name (str): full name of country of asylum for second item
        - item_1_coo (str): legacy code for country of origin for second item
        - item_1_coa (str): legacy code for country of asylum for second item
        - item_1_coo_iso (str): ISO3 code for country of origin for second item
        - item_1_coa_iso (str): ISO3 code for country of asylum for second item
        - item_1_refugees (int): number of recognized refugees in second item
        - item_1_asylum_seekers (int): number of asylum seekers in second item
        - item_1_returned_refugees (int): number of returned refugees in second item
        - item_1_idps (str): number of internally displaced persons in second item as string
        - item_1_returned_idps (str): number of returned IDPs in second item as string
        - item_1_stateless (str): number of stateless individuals in second item as string
        - item_1_ooc (int): number of individuals out of concern in second item
        - item_1_oip (str): number of individuals in protracted situations in second item
        - item_1_hst (str): historical stock total in second item as string
    """
    return {
        "page": 1,
        "maxPages": 1,
        "short_url": "unhcr-pop-2024",
        "total_0": "",
        "total_1": "",
        "item_0_year": 2024,
        "item_0_coo_id": 840,
        "item_0_coa_id": 76,
        "item_0_coo_name": "Syrian Arab Republic",
        "item_0_coa_name": "Brazil",
        "item_0_coo": "SYR",
        "item_0_coa": "BRA",
        "item_0_coo_iso": "SYR",
        "item_0_coa_iso": "BRA",
        "item_0_refugees": 1500,
        "item_0_asylum_seekers": 300,
        "item_0_returned_refugees": 50,
        "item_0_idps": "0",
        "item_0_returned_idps": "0",
        "item_0_stateless": "0",
        "item_0_ooc": 200,
        "item_0_oip": "-",
        "item_0_hst": "0",
        "item_1_year": 2024,
        "item_1_coo_id": 639,
        "item_1_coa_id": 76,
        "item_1_coo_name": "Venezuela (Bolivarian Republic of)",
        "item_1_coa_name": "Brazil",
        "item_1_coo": "VEN",
        "item_1_coa": "BRA",
        "item_1_coo_iso": "VEN",
        "item_1_coa_iso": "BRA",
        "item_1_refugees": 25000,
        "item_1_asylum_seekers": 800,
        "item_1_returned_refugees": 100,
        "item_1_idps": "0",
        "item_1_returned_idps": "0",
        "item_1_stateless": "0",
        "item_1_ooc": 300,
        "item_1_oip": "-",
        "item_1_hst": "0"
    }

def unhcr_population_data_server_get_population_data(
    coa: Optional[str] = None,
    coa_all: Optional[bool] = False,
    coo: Optional[str] = None,
    coo_all: Optional[bool] = False,
    year: Optional[int] = 2024
) -> Dict[str, Any]:
    """
    Get refugee population data from UNHCR.
    
    Args:
        coa (Optional[str]): Country of asylum (ISO3 code) - Use for questions about refugees IN a specific country
        coa_all (Optional[bool]): Set to True when breaking down results by ASYLUM country
        coo (Optional[str]): Country of origin (ISO3 code) - Use for questions about refugees FROM a specific country
        coo_all (Optional[bool]): Set to True when breaking down results by ORIGIN country
        year (Optional[int]): Year to filter by (defaults to 2024)
    
    Important:
        - For "Where are refugees from COUNTRY living?" use coo="COUNTRY" and coa_all=True
        - For "How many refugees are living in COUNTRY?" use coa="COUNTRY"
        - For "What countries do refugees in COUNTRY come from?" use coa="COUNTRY" and coo_all=True
        
    Returns:
        Population data from UNHCR with the following structure:
        - page (int): current page number of the response
        - maxPages (int): total number of pages available in the response
        - short-url (str): short identifier for the query URL
        - total (List): summary totals (if provided); typically empty in examples
        - items (List[Dict]): list of population data entries containing:
          - year (int): the year of the data
          - coo_id (int): country of origin numeric ID
          - coa_id (int): country of asylum numeric ID
          - coo_name (str): full name of country of origin
          - coa_name (str): full name of country of asylum
          - coo (str): legacy code for country of origin
          - coa (str): legacy code for country of asylum
          - coo_iso (str): ISO3 code for country of origin
          - coa_iso (str): ISO3 code for country of asylum
          - refugees (int): number of recognized refugees
          - asylum_seekers (int): number of asylum seekers
          - returned_refugees (int): number of returned refugees
          - idps (int or str): number of internally displaced persons; "0" or numeric string
          - returned_idps (int or str): number of returned internally displaced persons; "0" or numeric string
          - stateless (int or str): number of stateless individuals; "0" or numeric string
          - ooc (int or str): number of individuals out of concern; "0" or numeric value
          - oip (int or str): number of individuals in protracted situations; "-" if not applicable
          - hst (int or str): historical stock total; "0" or numeric string
    
    Raises:
        ValueError: If both coo and coo_all are provided, or both coa and coa_all are provided
    """
    # Input validation
    if coo is not None and coo_all:
        raise ValueError("Cannot specify both coo and coo_all parameters")
    if coa is not None and coa_all:
        raise ValueError("Cannot specify both coa and coa_all parameters")
    
    # Ensure year is valid
    if year is None:
        year = 2024
    
    # Call external API to get flat data
    api_data = call_external_api("unhcr-population-data-server-get_population_data")
    
    # Construct nested structure matching output schema
    result = {
        "page": api_data["page"],
        "maxPages": api_data["maxPages"],
        "short-url": api_data["short_url"],
        "total": [api_data["total_0"], api_data["total_1"]] if api_data["total_0"] or api_data["total_1"] else [],
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
                "refugees": api_data["item_0_refugees"],
                "asylum_seekers": api_data["item_0_asylum_seekers"],
                "returned_refugees": api_data["item_0_returned_refugees"],
                "idps": api_data["item_0_idps"],
                "returned_idps": api_data["item_0_returned_idps"],
                "stateless": api_data["item_0_stateless"],
                "ooc": api_data["item_0_ooc"],
                "oip": api_data["item_0_oip"],
                "hst": api_data["item_0_hst"]
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
                "refugees": api_data["item_1_refugees"],
                "asylum_seekers": api_data["item_1_asylum_seekers"],
                "returned_refugees": api_data["item_1_returned_refugees"],
                "idps": api_data["item_1_idps"],
                "returned_idps": api_data["item_1_returned_idps"],
                "stateless": api_data["item_1_stateless"],
                "ooc": api_data["item_1_ooc"],
                "oip": api_data["item_1_oip"],
                "hst": api_data["item_1_hst"]
            }
        ]
    }
    
    # Apply filtering based on input parameters
    filtered_items = []
    for item in result["items"]:
        # Filter by year
        if year is not None and item["year"] != year:
            continue
            
        # Filter by country of origin
        if coo is not None and item["coo_iso"] != coo:
            continue
            
        # Filter by country of asylum
        if coa is not None and item["coa_iso"] != coa:
            continue
            
        filtered_items.append(item)
    
    result["items"] = filtered_items
    
    return result