from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for CNPJ search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - company_name (str): Official corporate name (Razão Social)
        - trade_name (str): Trade name (Nome Fantasia), or 'N/A' if not available
        - registration_status (str): Current registration status (e.g., ATIVA, BAIXADA)
        - opening_date (str): Date of company registration in ISO format (YYYY-MM-DD)
        - main_cnae_code (str): Primary CNAE activity code
        - main_cnae_description (str): Description of the primary CNAE activity
        - legal_nature (str): Legal nature code and description
        - address_street (str): Street address including number and complement
        - address_district (str): Neighborhood or district (bairro)
        - address_city (str): City name
        - address_state (str): Two-letter state abbreviation
        - postal_code (str): Brazilian postal code (CEP), 8 digits
        - phone (str): Registered phone number, or 'N/A' if not available
        - email (str): Registered email address, or 'N/A' if not available
    """
    return {
        "company_name": "EMPRESA EXEMPLO LTDA",
        "trade_name": "EXEMPLO COMERCIAL",
        "registration_status": "ATIVA",
        "opening_date": "2015-03-20",
        "main_cnae_code": "8550301",
        "main_cnae_description": "Administração de caixas escolares",
        "legal_nature": "2062 - Sociedade Empresária Limitada",
        "address_street": "AVENIDA PRINCIPAL, 1000, SALA 500",
        "address_district": "CENTRO",
        "address_city": "SAO PAULO",
        "address_state": "SP",
        "postal_code": "01000000",
        "phone": "(11) 3000-4000",
        "email": "contato@exemplo.com.br"
    }

def brasil_api_cnpj_search(cnpj: str) -> Dict[str, Any]:
    """
    Query information about a Brazilian company by its CNPJ (National Registry of Legal Entities).
    
    Args:
        cnpj (str): CNPJ to be queried (only numbers, 14 digits)
    
    Returns:
        Dict containing company information with the following fields:
        - company_name (str): Official corporate name (Razão Social)
        - trade_name (str): Trade name (Nome Fantasia), or 'N/A' if not available
        - registration_status (str): Current registration status (e.g., ATIVA, BAIXADA)
        - opening_date (str): Date of company registration in ISO format (YYYY-MM-DD)
        - main_cnae_code (str): Primary CNAE activity code
        - main_cnae_description (str): Description of the primary CNAE activity
        - legal_nature (str): Legal nature code and description
        - address_street (str): Street address including number and complement
        - address_district (str): Neighborhood or district (bairro)
        - address_city (str): City name
        - address_state (str): Two-letter state abbreviation
        - postal_code (str): Brazilian postal code (CEP), 8 digits
        - phone (str): Registered phone number, or 'N/A' if not available
        - email (str): Registered email address, or 'N/A' if not available
    
    Raises:
        ValueError: If CNPJ is not a 14-digit string containing only numbers
    """
    # Input validation
    if not isinstance(cnpj, str):
        raise ValueError("CNPJ must be a string")
    if not cnpj.isdigit():
        raise ValueError("CNPJ must contain only digits")
    if len(cnpj) != 14:
        raise ValueError("CNPJ must be exactly 14 digits")
    
    # Call external API (simulated)
    api_data = call_external_api("brasil-api-cnpj-search")
    
    # Construct result dictionary matching output schema
    result = {
        "company_name": api_data["company_name"],
        "trade_name": api_data["trade_name"],
        "registration_status": api_data["registration_status"],
        "opening_date": api_data["opening_date"],
        "main_cnae_code": api_data["main_cnae_code"],
        "main_cnae_description": api_data["main_cnae_description"],
        "legal_nature": api_data["legal_nature"],
        "address_street": api_data["address_street"],
        "address_district": api_data["address_district"],
        "address_city": api_data["address_city"],
        "address_state": api_data["address_state"],
        "postal_code": api_data["postal_code"],
        "phone": api_data["phone"],
        "email": api_data["email"]
    }
    
    return result