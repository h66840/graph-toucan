from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Brazilian DDD information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - state (str): Brazilian state abbreviation (UF) associated with the DDD
        - city_0 (str): First city served by the DDD
        - city_1 (str): Second city served by the DDD
    """
    # Mock data based on common DDD codes in Brazil
    mock_data = {
        "11": {"state": "SP", "cities": ["São Paulo", "São Caetano do Sul"]},
        "21": {"state": "RJ", "cities": ["Rio de Janeiro", "Niterói"]},
        "31": {"state": "MG", "cities": ["Belo Horizonte", "Contagem"]},
        "41": {"state": "PR", "cities": ["Curitiba", "Piraquara"]},
        "51": {"state": "RS", "cities": ["Porto Alegre", "Canoas"]},
        "61": {"state": "DF", "cities": ["Brasília", "Águas Claras"]},
        "71": {"state": "BA", "cities": ["Salvador", "Lauro de Freitas"]},
        "81": {"state": "PE", "cities": ["Recife", "Jaboatão dos Guararapes"]},
        "91": {"state": "PA", "cities": ["Belém", "Ananindeua"]}
    }
    
    # Default fallback
    ddd_info = mock_data.get("11")  # São Paulo as default
    if tool_name == "brasil-api-ddd-info":
        # Since we can't pass ddd to call_external_api per requirements, we use default
        ddd_info = mock_data.get("11")
    
    return {
        "state": ddd_info["state"],
        "city_0": ddd_info["cities"][0],
        "city_1": ddd_info["cities"][1]
    }

def brasil_api_ddd_info(ddd: str) -> Dict[str, Any]:
    """
    Get information about a Brazilian area code (DDD) including state and cities.
    
    Args:
        ddd (str): Area code (DDD) to be queried (only numbers, 2 digits)
    
    Returns:
        Dict containing:
        - state (str): the Brazilian state abbreviation (UF) associated with the DDD
        - cities (List[str]): list of cities served by the DDD
    
    Raises:
        ValueError: If ddd is not a valid 2-digit string containing only numbers
    """
    # Input validation
    if not isinstance(ddd, str):
        raise ValueError("DDD must be a string")
    if not ddd.isdigit():
        raise ValueError("DDD must contain only digits")
    if len(ddd) != 2:
        raise ValueError("DDD must be exactly 2 digits long")
    
    # Fetch data from external API simulation
    api_data = call_external_api("brasil-api-ddd-info")
    
    # Construct result matching output schema
    result = {
        "state": api_data["state"],
        "cities": [
            api_data["city_0"],
            api_data["city_1"]
        ]
    }
    
    return result