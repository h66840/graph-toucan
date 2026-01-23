from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Brazilian postal code lookup.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - cep (str): Formatted postal code
        - logradouro (str): Street or road name
        - complemento (str): Additional address information
        - bairro (str): Neighborhood or district
        - cidade (str): City name
        - estado (str): State abbreviation and full name
        - regiao (str): Geographic region of Brazil
        - ddd (str): Area code for telephone numbers
        - ibge (str): IBGE municipality code
        - status (str): Operation status ("success" or "not_found")
        - mensagem (str): Human-readable message summarizing result
    """
    return {
        "cep": "12345-678",
        "logradouro": "Avenida Paulista",
        "complemento": "de 1000 a 2000 - lado par",
        "bairro": "Bela Vista",
        "cidade": "São Paulo",
        "estado": "SP (São Paulo)",
        "regiao": "Sudeste",
        "ddd": "11",
        "ibge": "3550308",
        "status": "success",
        "mensagem": "Endereço encontrado"
    }

def brazilian_postal_code_server_consultar_cep(cep: str) -> Dict[str, Any]:
    """
    Query address information from a Brazilian postal code (CEP).
    
    Args:
        cep (str): Postal code to be queried (only numbers, 8 digits)
    
    Returns:
        Dict containing address information with the following keys:
        - cep (str): postal code in the format XXXXX-XXX
        - logradouro (str): street or road name
        - complemento (str): additional address information, can be "N/A" if not available
        - bairro (str): neighborhood or district
        - cidade (str): city name
        - estado (str): state abbreviation and full name in the format "XX (State Name)"
        - regiao (str): geographic region of Brazil (e.g., Sudeste)
        - ddd (str): area code for telephone numbers
        - ibge (str): IBGE municipality code (7 digits)
        - status (str): operation status: "success" if address found, "not_found" if CEP does not exist
        - mensagem (str): human-readable message summarizing result
    
    Raises:
        ValueError: If the input CEP is not exactly 8 digits or contains non-digit characters
    """
    # Input validation
    if not cep:
        raise ValueError("CEP is required")
    
    if not cep.isdigit():
        raise ValueError("CEP must contain only numbers")
    
    if len(cep) != 8:
        raise ValueError("CEP must be exactly 8 digits")
    
    # Call external API simulation
    api_data = call_external_api("brazilian-postal-code-server-consultar-cep")
    
    # Construct result matching output schema
    result = {
        "cep": api_data["cep"],
        "logradouro": api_data["logradouro"],
        "complemento": api_data["complemento"],
        "bairro": api_data["bairro"],
        "cidade": api_data["cidade"],
        "estado": api_data["estado"],
        "regiao": api_data["regiao"],
        "ddd": api_data["ddd"],
        "ibge": api_data["ibge"],
        "status": api_data["status"],
        "mensagem": api_data["mensagem"]
    }
    
    return result