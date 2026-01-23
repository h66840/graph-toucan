from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for postal code information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - cep (str): postal code in 8-digit format without hyphens
        - state (str): two-letter state abbreviation (e.g., SP, RJ)
        - city (str): full name of the city
        - neighborhood (str): name of the neighborhood or district
        - street (str): official name of the street or public space
        - service (str): name of the data source service used to retrieve the information
    """
    return {
        "cep": "01310930",
        "state": "SP",
        "city": "São Paulo",
        "neighborhood": "Bela Vista",
        "street": "Avenida Paulista",
        "service": "brasilapi"
    }

def brasilapi_mcp_server_get_postal_code_v1(cep: str) -> Dict[str, Any]:
    """
    Get location data given a CEP (postal code).
    
    This function retrieves information about a location in Brazil based on its CEP
    (Código de Endereçamento Postal). It returns details such as state, city, neighborhood,
    and street name.
    
    Args:
        cep (str): The CEP to query. Must be a valid 8-digit string without hyphens.
        
    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - cep (str): postal code in 8-digit format without hyphens
            - state (str): two-letter state abbreviation (e.g., SP, RJ)
            - city (str): full name of the city
            - neighborhood (str): name of the neighborhood or district
            - street (str): official name of the street or public space
            - service (str): name of the data source service used to retrieve the information
            
    Raises:
        ValueError: If the provided CEP is not a valid 8-digit string
    """
    # Input validation
    if not isinstance(cep, str):
        raise ValueError("CEP must be a string")
    
    # Remove any non-digit characters
    cleaned_cep = ''.join(filter(str.isdigit, cep))
    
    # Validate CEP format (must be exactly 8 digits)
    if len(cleaned_cep) != 8 or not cleaned_cep.isdigit():
        raise ValueError("CEP must be an 8-digit string containing only numbers")
    
    # Call external API simulation
    api_data = call_external_api("brasilapi-mcp-server-get_postal_code_v1")
    
    # Construct result using data from external API
    result = {
        "cep": api_data["cep"],
        "state": api_data["state"],
        "city": api_data["city"],
        "neighborhood": api_data["neighborhood"],
        "street": api_data["street"],
        "service": api_data["service"]
    }
    
    return result