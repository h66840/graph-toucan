from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for IBGE municipality information.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - codigo (int): IBGE numeric code of the municipality
        - nome (str): name of the municipality in Portuguese
    """
    # Simulated response based on typical IBGE data
    # In a real implementation, this would call an actual API
    return {
        "codigo": 3550308,
        "nome": "São Paulo"
    }

def ibge_municipality_listing_server_GetMunicipioPorIdentificador(identificador: int) -> Dict[str, Any]:
    """
    Obtém o conjunto de municípios do Brasil a partir dos respectivos identificadores.
    
    Args:
        identificador (int): Código do município segundo IBGE (ex: 3550308 para São Paulo)
    
    Returns:
        Dict[str, Any]: Dicionário contendo código e nome do município com as seguintes chaves:
            - codigo (int): Código numérico do IBGE para o município
            - nome (str): Nome do município em português
    
    Raises:
        ValueError: Se o identificador não for um número positivo válido
    """
    # Input validation
    if not isinstance(identificador, int):
        raise ValueError("O identificador deve ser um número inteiro.")
    if identificador <= 0:
        raise ValueError("O identificador deve ser um número inteiro positivo.")
    
    # Call external API simulation
    api_data = call_external_api("ibge-municipality-listing-server-GetMunicipioPorIdentificador")
    
    # Construct result matching output schema
    resultado = {
        "codigo": api_data["codigo"],
        "nome": api_data["nome"]
    }
    
    return resultado