from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the presentation based on the theme
        - focus_topics_0 (str): First main topic for the presentation
        - focus_topics_1 (str): Second main topic for the presentation
        - focus_topics_2 (str): Third main topic for the presentation
        - focus_topics_3 (str): Fourth main topic for the presentation
        - focus_topics_4 (str): Fifth main topic for the presentation
    """
    return {
        "title": "Apresentação sobre Inteligência Artificial",
        "focus_topics_0": "O que é",
        "focus_topics_1": "Diferenças entre o tema e um conceito similar",
        "focus_topics_2": "Exemplos de ferramentas",
        "focus_topics_3": "Vantagens e desafios",
        "focus_topics_4": "Casos de uso"
    }

def mapas_mentais_server_apresenta(tema: str) -> Dict[str, Any]:
    """
    Gera um mapa mental para apresentações sobre um tema.
    
    Args:
        tema (str): O tema central da apresentação. Deve ser uma string não vazia.
    
    Returns:
        Dict[str, Any]: Um dicionário contendo:
            - title (str): Título da apresentação baseado no tema fornecido.
            - focus_topics (List[str]): Lista de tópicos principais a serem abordados na apresentação.
              Inclui: "O que é", "Diferenças entre o [tema] e um conceito similar",
                     "Exemplos de ferramentas", "Vantagens e desafios", "Casos de uso".
    
    Raises:
        ValueError: Se o parâmetro 'tema' não for fornecido ou for uma string vazia.
    """
    if not tema or not isinstance(tema, str) or not tema.strip():
        raise ValueError("O parâmetro 'tema' é obrigatório e deve ser uma string não vazia.")
    
    tema = tema.strip()
    
    # Chama a API externa para obter os dados simulados
    api_data = call_external_api("mapas-mentais-server-apresenta")
    
    # Constrói a estrutura aninhada conforme o esquema de saída esperado
    result = {
        "title": api_data["title"].replace("Inteligência Artificial", tema),
        "focus_topics": [
            api_data["focus_topics_0"],
            api_data["focus_topics_1"].replace("tema", tema),
            api_data["focus_topics_2"],
            api_data["focus_topics_3"],
            api_data["focus_topics_4"]
        ]
    }
    
    return result