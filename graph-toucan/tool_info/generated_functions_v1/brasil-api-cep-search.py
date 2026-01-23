from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for CEP lookup.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): whether the CEP lookup was successful
        - cep (str): postal code in 8-digit format
        - street (str): street name (Logradouro)
        - neighborhood (str): neighborhood or district (Bairro)
        - city (str): city name (Cidade)
        - state (str): state abbreviation (Estado)
        - latitude (str): latitude coordinate; "N/A" if not available
        - longitude (str): longitude coordinate; "N/A" if not available
        - ibge_code (str): IBGE municipality code; "N/A" if not available
        - error_message (str): error description if the request failed
    """
    return {
        "success": True,
        "cep": "01001000",
        "street": "Praça da Sé",
        "neighborhood": "Sé",
        "city": "São Paulo",
        "state": "SP",
        "latitude": "-23.550520",
        "longitude": "-46.633308",
        "ibge_code": "3550308",
        "error_message": ""
    }

def brasil_api_cep_search(cep: str) -> Dict[str, Any]:
    """
    Query address information from a Brazilian postal code (CEP).
    
    Args:
        cep (str): Postal code to be queried (only numbers, 8 digits)
    
    Returns:
        Dict containing the following fields:
        - success (bool): whether the CEP lookup was successful
        - cep (str): postal code in 8-digit format
        - street (str): street name (Logradouro)
        - neighborhood (str): neighborhood or district (Bairro)
        - city (str): city name (Cidade)
        - state (str): state abbreviation (Estado)
        - latitude (str): latitude coordinate; "N/A" if not available
        - longitude (str): longitude coordinate; "N/A" if not available
        - ibge_code (str): IBGE municipality code; "N/A" if not available
        - error_message (str): error description if the request failed
    """
    # Input validation
    if not cep:
        return {
            "success": False,
            "cep": "",
            "street": "",
            "neighborhood": "",
            "city": "",
            "state": "",
            "latitude": "N/A",
            "longitude": "N/A",
            "ibge_code": "N/A",
            "error_message": "CEP is required"
        }
    
    if not cep.isdigit() or len(cep) != 8:
        return {
            "success": False,
            "cep": cep,
            "street": "",
            "neighborhood": "",
            "city": "",
            "state": "",
            "latitude": "N/A",
            "longitude": "N/A",
            "ibge_code": "N/A",
            "error_message": "CEP must contain exactly 8 digits"
        }
    
    # Call external API simulation
    api_data = call_external_api("brasil-api-cep-search")
    
    # Construct result matching output schema
    result = {
        "success": api_data["success"],
        "cep": api_data["cep"],
        "street": api_data["street"],
        "neighborhood": api_data["neighborhood"],
        "city": api_data["city"],
        "state": api_data["state"],
        "latitude": api_data["latitude"],
        "longitude": api_data["longitude"],
        "ibge_code": api_data["ibge_code"],
        "error_message": api_data["error_message"]
    }
    
    return result