from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Brazilian state information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): Official name of the Brazilian state
        - abbreviation (str): Two-letter state abbreviation
        - region (str): Geographic region of the state
        - id (str): Numerical identifier for the state assigned by IBGE
    """
    return {
        "name": "São Paulo",
        "abbreviation": "SP",
        "region": "Sudeste",
        "id": "35"
    }

def brasil_api_ibge_state_search(code: str) -> Dict[str, Any]:
    """
    Find information about a Brazilian state by its code or abbreviation.
    
    Args:
        code (str): State code or abbreviation (e.g., SP, RJ, 35)
    
    Returns:
        Dict containing state information with the following keys:
        - name (str): official name of the Brazilian state
        - abbreviation (str): two-letter state abbreviation
        - region (str): geographic region of the state
        - id (str): numerical identifier for the state assigned by IBGE
    
    Raises:
        ValueError: If the code parameter is empty or not provided
    """
    if not code:
        raise ValueError("Code parameter is required")
    
    api_data = call_external_api("brasil-api-ibge-state-search")
    
    result = {
        "name": api_data["name"],
        "abbreviation": api_data["abbreviation"],
        "region": api_data["region"],
        "id": api_data["id"]
    }
    
    return result