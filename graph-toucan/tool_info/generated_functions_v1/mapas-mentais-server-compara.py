from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - comparison_title (str): Title of the comparison between two themes
        - focus_topics_0 (str): First topic that the comparison focuses on
        - focus_topics_1 (str): Second topic that the comparison focuses on
        - theme1 (str): First theme being compared
        - theme2 (str): Second theme being compared
        - comparison_points_definitions_theme1 (str): Definition for theme1
        - comparison_points_definitions_theme2 (str): Definition for theme2
        - comparison_points_characteristics_theme1 (str): Characteristics of theme1
        - comparison_points_characteristics_theme2 (str): Characteristics of theme2
        - comparison_points_advantages_theme1 (str): Advantages of theme1
        - comparison_points_advantages_theme2 (str): Advantages of theme2
        - comparison_points_disadvantages_theme1 (str): Disadvantages of theme1
        - comparison_points_disadvantages_theme2 (str): Disadvantages of theme2
    """
    return {
        "comparison_title": "Comparação entre Programação Orientada a Objetos e Programação Funcional",
        "focus_topics_0": "definições",
        "focus_topics_1": "características",
        "theme1": "Programação Orientada a Objetos",
        "theme2": "Programação Funcional",
        "comparison_points_definitions_theme1": "Paradigma baseado em objetos que contêm dados e comportamentos.",
        "comparison_points_definitions_theme2": "Paradigma onde os programas são construídos através de funções puras e imutabilidade.",
        "comparison_points_characteristics_theme1": "Encapsulamento, herança, polimorfismo, estado mutável.",
        "comparison_points_characteristics_theme2": "Funções puras, imutabilidade, primeira classe, sem estado compartilhado.",
        "comparison_points_advantages_theme1": "Reutilização de código, modularidade, fácil modelagem do mundo real.",
        "comparison_points_advantages_theme2": "Previsibilidade, testabilidade, concorrência segura.",
        "comparison_points_disadvantages_theme1": "Complexidade crescente com hierarquias, estado compartilhado pode causar bugs.",
        "comparison_points_disadvantages_theme2": "Curva de aprendizado mais íngreme, menos intuitivo para iniciantes."
    }

def mapas_mentais_server_compara(tema1: str, tema2: str) -> Dict[str, Any]:
    """
    Gera um mapa mental comparando dois temas.
    
    Args:
        tema1 (str): Primeiro tema a ser comparado. Campo obrigatório.
        tema2 (str): Segundo tema a ser comparado. Campo obrigatório.
    
    Returns:
        Dict[str, Any]: Um dicionário contendo:
            - comparison_title (str): título da comparação entre os dois temas
            - focus_topics (List[str]): lista de tópicos foco da comparação
            - theme1 (str): primeiro tema comparado
            - theme2 (str): segundo tema comparado
            - comparison_points (Dict): análise comparativa estruturada por tópico,
              com chaves correspondentes aos tópicos e valores contendo análise comparativa para ambos os temas
    
    Raises:
        ValueError: Se algum dos parâmetros obrigatórios não for fornecido.
    """
    if not tema1 or not isinstance(tema1, str):
        raise ValueError("O parâmetro 'tema1' é obrigatório e deve ser uma string.")
    if not tema2 or not isinstance(tema2, str):
        raise ValueError("O parâmetro 'tema2' é obrigatório e deve ser uma string.")

    api_data = call_external_api("mapas-mentais-server-compara")

    focus_topics = [api_data["focus_topics_0"], api_data["focus_topics_1"]]

    comparison_points = {}
    for topic in focus_topics:
        key_map = {
            "definições": "definitions",
            "características": "characteristics",
            "vantagens": "advantages",
            "desvantagens": "disadvantages"
        }
        normalized_topic = key_map.get(topic, topic.replace(" ", "_"))
        
        theme1_key = f"comparison_points_{normalized_topic}_theme1"
        theme2_key = f"comparison_points_{normalized_topic}_theme2"
        
        comparison_points[topic] = {
            tema1: api_data.get(theme1_key, "Informação não disponível"),
            tema2: api_data.get(theme2_key, "Informação não disponível")
        }

    result = {
        "comparison_title": api_data["comparison_title"],
        "focus_topics": focus_topics,
        "theme1": tema1,
        "theme2": tema2,
        "comparison_points": comparison_points
    }

    return result