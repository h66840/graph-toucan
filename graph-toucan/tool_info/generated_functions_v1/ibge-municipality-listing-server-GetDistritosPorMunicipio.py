from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for IBGE municipality district listing.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - district_0_codigo (int): IBGE code of the first district
        - district_0_nome (str): Name of the first district
        - district_1_codigo (int): IBGE code of the second district
        - district_1_nome (str): Name of the second district
    """
    return {
        "district_0_codigo": 355030801,
        "district_0_nome": "Sé",
        "district_1_codigo": 355030802,
        "district_1_nome": "Bela Vista"
    }

def ibge_municipality_listing_server_GetDistritosPorMunicipio(codigoMunicipio: int) -> List[Dict[str, Any]]:
    """
    Obtêm a lista de distritos, passando o código do município do IBGE.
    
    Args:
        codigoMunicipio (int): Código do município do IBGE
        
    Returns:
        List[Dict]: Lista de distritos, onde cada distrito contém:
            - codigo (int): Código IBGE do distrito
            - nome (str): Nome do distrito
    """
    if not isinstance(codigoMunicipio, int) or codigoMunicipio <= 0:
        raise ValueError("codigoMunicipio must be a positive integer")
    
    # Fetch simulated external data
    api_data = call_external_api("ibge-municipality-listing-server-GetDistritosPorMunicipio")
    
    # Construct the list of districts from flattened API response
    districts = [
        {
            "codigo": api_data["district_0_codigo"],
            "nome": api_data["district_0_nome"]
        },
        {
            "codigo": api_data["district_1_codigo"],
            "nome": api_data["district_1_nome"]
        }
    ]
    
    return districts