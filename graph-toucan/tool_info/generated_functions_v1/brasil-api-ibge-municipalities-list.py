from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Brazilian municipalities by state.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - municipality_0_id (str or int): IBGE ID of first municipality
        - municipality_0_nome (str): Name of first municipality
        - municipality_0_microrregiao_id (str or int): Microregion ID of first municipality
        - municipality_0_microrregiao_nome (str): Microregion name of first municipality
        - municipality_0_mesorregiao_id (str or int): Mesoregion ID of first municipality
        - municipality_0_mesorregiao_nome (str): Mesoregion name of first municipality
        - municipality_1_id (str or int): IBGE ID of second municipality
        - municipality_1_nome (str): Name of second municipality
        - municipality_1_microrregiao_id (str or int): Microregion ID of second municipality
        - municipality_1_microrregiao_nome (str): Microregion name of second municipality
        - municipality_1_mesorregiao_id (str or int): Mesoregion ID of second municipality
        - municipality_1_mesorregiao_nome (str): Mesoregion name of second municipality
        - state (str): State abbreviation (UF)
        - total_count (int): Total number of municipalities returned
        - source (str): Data source identifier
        - timestamp (str): ISO 8601 formatted timestamp
    """
    return {
        "municipality_0_id": "3550308",
        "municipality_0_nome": "São Paulo",
        "municipality_0_microrregiao_id": "35026",
        "municipality_0_microrregiao_nome": "São Paulo",
        "municipality_0_mesorregiao_id": "3513",
        "municipality_0_mesorregiao_nome": "Metropolitana de São Paulo",
        "municipality_1_id": "3550407",
        "municipality_1_nome": "São Bernardo do Campo",
        "municipality_1_microrregiao_id": "35026",
        "municipality_1_microrregiao_nome": "São Paulo",
        "municipality_1_mesorregiao_id": "3513",
        "municipality_1_mesorregiao_nome": "Metropolitana de São Paulo",
        "state": "SP",
        "total_count": 2,
        "source": "IBGE",
        "timestamp": datetime.now().isoformat()
    }

def brasil_api_ibge_municipalities_list(uf: str) -> Dict[str, Any]:
    """
    List all municipalities of a Brazilian state by its abbreviation.

    Args:
        uf (str): State abbreviation (e.g., SP, RJ). Required.

    Returns:
        Dict containing:
        - municipalities (List[Dict]): List of municipality objects with id, nome, microrregiao, and mesorregiao
        - state (str): The state abbreviation (UF) for which municipalities were retrieved
        - total_count (int): Total number of municipalities returned
        - source (str): Name of the data source (e.g., "IBGE")
        - timestamp (str): ISO 8601 datetime string indicating when the data was generated

        Each municipality dict contains:
        - id (str or int): Unique IBGE identifier
        - nome (str): Official name of the municipality
        - microrregiao (Dict): Contains 'id' and 'nome' of the microregion
        - mesorregiao (Dict): Contains 'id' and 'nome' of the mesoregion

    Raises:
        ValueError: If uf is not provided or not a valid string
    """
    if not uf or not isinstance(uf, str) or len(uf.strip()) == 0:
        raise ValueError("Parameter 'uf' is required and must be a non-empty string.")
    
    # Normalize UF input
    uf = uf.strip().upper()
    
    # Validate UF format (2 uppercase letters)
    if len(uf) != 2 or not uf.isalpha():
        raise ValueError("Parameter 'uf' must be a valid two-letter Brazilian state abbreviation.")
    
    # Call external API simulation
    api_data = call_external_api("brasil-api-ibge-municipalities-list")
    
    # Construct municipalities list from flattened API response
    municipalities: List[Dict[str, Any]] = []
    
    for i in range(2):  # We expect 2 municipalities based on call_external_api
        municipality_key = f"municipality_{i}"
        if f"{municipality_key}_id" not in api_data:
            continue
            
        microrregiao = {
            "id": api_data.get(f"{municipality_key}_microrregiao_id"),
            "nome": api_data.get(f"{municipality_key}_microrregiao_nome")
        }
        
        mesorregiao = {
            "id": api_data.get(f"{municipality_key}_mesorregiao_id"),
            "nome": api_data.get(f"{municipality_key}_mesorregiao_nome")
        }
        
        municipality = {
            "id": api_data[f"{municipality_key}_id"],
            "nome": api_data[f"{municipality_key}_nome"],
            "microrregiao": microrregiao,
            "mesorregiao": mesorregiao
        }
        municipalities.append(municipality)
    
    # Build final result matching output schema
    result = {
        "municipalities": municipalities,
        "state": api_data["state"],
        "total_count": api_data["total_count"],
        "source": api_data["source"],
        "timestamp": api_data["timestamp"]
    }
    
    return result