from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Brazilian municipalities by UF.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - municipio_0_codigo (int): IBGE code for the first municipality
        - municipio_0_nome (str): Name of the first municipality
        - municipio_1_codigo (int): IBGE code for the second municipality
        - municipio_1_nome (str): Name of the second municipality
    """
    return {
        "municipio_0_codigo": 3550308,
        "municipio_0_nome": "São Paulo",
        "municipio_1_codigo": 3509502,
        "municipio_1_nome": "Campinas"
    }

def ibge_municipality_listing_server_GetMunicipiosPorUF(uf: str) -> List[Dict[str, Any]]:
    """
    Obtêm a lista de municípios brasileiros, passando o UF.
    
    Args:
        uf (str): Sigla da Unidade Federativa (ex: SP, RJ, MG)
    
    Returns:
        List[Dict]: Lista de municípios com campos 'codigo' (código IBGE) e 'nome' (nome do município)
    
    Raises:
        ValueError: Se o parâmetro uf não for fornecido ou não for uma string válida
    """
    if not uf or not isinstance(uf, str):
        raise ValueError("O parâmetro 'uf' é obrigatório e deve ser uma string válida.")
    
    # Simulate external API call
    api_data = call_external_api("ibge-municipality-listing-server-GetMunicipiosPorUF")
    
    # Construct the list of municipalities from flattened API response
    municipios = [
        {
            "codigo": api_data["municipio_0_codigo"],
            "nome": api_data["municipio_0_nome"]
        },
        {
            "codigo": api_data["municipio_1_codigo"],
            "nome": api_data["municipio_1_nome"]
        }
    ]
    
    return municipios