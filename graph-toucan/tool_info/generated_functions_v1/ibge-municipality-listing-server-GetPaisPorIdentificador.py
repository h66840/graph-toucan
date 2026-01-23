from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for IBGE country information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - pais_id (int): Unique identifier of the country as defined by IBGE
        - nome_oficial (str): Official name of the country
        - nome_comum (str): Common name of the country used in everyday language
        - sigla (str): Country's abbreviation code (e.g., BR for Brazil)
        - codigo_iso3 (str): ISO 3-letter country code
        - continente (str): Geographic continent where the country is located
        - status (str): Administrative status of the country (e.g., ativo/inativo)
        - capital (str): Name of the country's capital city
        - area_km2 (float): Total land area in square kilometers
        - populacao (int): Estimated population of the country
        - moeda (str): Official currency used in the country
        - idiomas_0 (str): First official language spoken in the country
        - idiomas_1 (str): Second official language spoken in the country
        - borda_com_pais_0 (str): First neighboring country sharing a border
        - borda_com_pais_1 (str): Second neighboring country sharing a border
        - fonte_dados (str): Source of the data cataloged by IBGE
        - ultima_atualizacao (str): Timestamp or year indicating when the data was last updated
    """
    return {
        "pais_id": 76,
        "nome_oficial": "República Federativa do Brasil",
        "nome_comum": "Brasil",
        "sigla": "BR",
        "codigo_iso3": "BRA",
        "continente": "América do Sul",
        "status": "ativo",
        "capital": "Brasília",
        "area_km2": 8516000.0,
        "populacao": 213993437,
        "moeda": "Real",
        "idiomas_0": "Português",
        "idiomas_1": "Inglês",
        "borda_com_pais_0": "Argentina",
        "borda_com_pais_1": "Colômbia",
        "fonte_dados": "IBGE",
        "ultima_atualizacao": "2023"
    }

def ibge_municipality_listing_server_GetPaisPorIdentificador(identificador: int) -> Optional[Dict[str, Any]]:
    """
    Obtêm os dados básicos do país, conforme catalogados no IBGE.
    
    Args:
        identificador (int): Digite o identificador do país, exemplo: BR é 76
    
    Returns:
        Dict containing country information with the following keys:
        - pais_id (int): Unique identifier of the country as defined by IBGE
        - nome_oficial (str): Official name of the country
        - nome_comum (str): Common name of the country used in everyday language
        - sigla (str): Country's abbreviation code (e.g., BR for Brazil)
        - codigo_iso3 (str): ISO 3-letter country code
        - continente (str): Geographic continent where the country is located
        - status (str): Administrative status of the country (e.g., ativo/inativo)
        - capital (str): Name of the country's capital city
        - area_km2 (float): Total land area in square kilometers
        - populacao (int): Estimated population of the country
        - moeda (str): Official currency used in the country
        - idiomas (List[str]): List of official languages spoken in the country
        - borda_com_pais (List[str]): List of neighboring countries sharing a border
        - fonte_dados (str): Source of the data cataloged by IBGE
        - ultima_atualizacao (str): Timestamp or year indicating when the data was last updated
    
    Returns None if no data is found for the given identifier.
    """
    if not isinstance(identificador, int) or identificador <= 0:
        raise ValueError("Identificador must be a positive integer")
    
    # Simulate fetching data from external source
    api_data = call_external_api("ibge-municipality-listing-server-GetPaisPorIdentificador")
    
    # Validate that we got expected data
    if not api_data or api_data.get("pais_id") != identificador:
        return None
    
    # Construct nested structure matching output schema
    result = {
        "pais_id": api_data["pais_id"],
        "nome_oficial": api_data["nome_oficial"],
        "nome_comum": api_data["nome_comum"],
        "sigla": api_data["sigla"],
        "codigo_iso3": api_data["codigo_iso3"],
        "continente": api_data["continente"],
        "status": api_data["status"],
        "capital": api_data["capital"],
        "area_km2": api_data["area_km2"],
        "populacao": api_data["populacao"],
        "moeda": api_data["moeda"],
        "idiomas": [
            api_data["idiomas_0"],
            api_data["idiomas_1"]
        ],
        "borda_com_pais": [
            api_data["borda_com_pais_0"],
            api_data["borda_com_pais_1"]
        ],
        "fonte_dados": api_data["fonte_dados"],
        "ultima_atualizacao": api_data["ultima_atualizacao"]
    }
    
    return result