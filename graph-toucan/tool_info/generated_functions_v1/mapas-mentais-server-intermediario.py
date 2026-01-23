from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - topic (str): the main subject or theme for which intermediate knowledge is being described
        - focus_areas_0_level (str): first focus area level (e.g., Analisar, Avaliar, Criar)
        - focus_areas_0_actions_0 (str): first action under the first focus area
        - focus_areas_0_actions_1 (str): second action under the first focus area
        - focus_areas_1_level (str): second focus area level
        - focus_areas_1_actions_0 (str): first action under the second focus area
        - focus_areas_1_actions_1 (str): second action under the second focus area
    """
    return {
        "topic": "Programação Orientada a Objetos",
        "focus_areas_0_level": "Analisar",
        "focus_areas_0_actions_0": "Identificar classes e objetos em um sistema",
        "focus_areas_0_actions_1": "Diferenciar encapsulamento, herança e polimorfismo",
        "focus_areas_1_level": "Avaliar",
        "focus_areas_1_actions_0": "Critérios de qualidade em projetos com POO",
        "focus_areas_1_actions_1": "Comparar abordagens entre programação estruturada e orientada a objetos"
    }

def mapas_mentais_server_intermediario(tema: str) -> Dict[str, Any]:
    """
    Gera um mapa mental de conhecimentos intermediários sobre o tema especificado.
    
    Args:
        tema (str): O tema principal para o qual será gerado o mapa mental de conhecimentos intermediários.
        
    Returns:
        Dict[str, Any]: Um dicionário contendo o tópico principal e áreas de foco com níveis cognitivos 
                        e ações associadas, estruturado conforme o esquema de saída definido.
                        
    Raises:
        ValueError: Se o parâmetro 'tema' não for fornecido ou for uma string vazia.
    """
    if not tema or not isinstance(tema, str):
        raise ValueError("O parâmetro 'tema' é obrigatório e deve ser uma string não vazia.")
    
    # Chamar a API externa para obter os dados simulados
    api_data = call_external_api("mapas-mentais-server-intermediario")
    
    # Construir a estrutura aninhada com base nos dados planos da API
    focus_areas = [
        {
            "level": api_data["focus_areas_0_level"],
            "actions": [
                api_data["focus_areas_0_actions_0"],
                api_data["focus_areas_0_actions_1"]
            ]
        },
        {
            "level": api_data["focus_areas_1_level"],
            "actions": [
                api_data["focus_areas_1_actions_0"],
                api_data["focus_areas_1_actions_1"]
            ]
        }
    ]
    
    # Retornar o resultado final no formato esperado
    result = {
        "topic": api_data["topic"],
        "focus_areas": focus_areas
    }
    
    return result