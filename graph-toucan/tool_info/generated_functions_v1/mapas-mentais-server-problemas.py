def mapas_mentais_server_problemas(tema: str) -> dict:
    """
    Gera um mapa mental de análise de problemas relacionados ao tema fornecido.
    
    Args:
        tema (str): O tema central para o qual será gerada a análise de problemas.
        
    Returns:
        dict: Um dicionário contendo o tópico da análise e as áreas focais identificadas.
              - analysis_topic (str): Tópico da análise, correspondente ao tema fornecido.
              - focus_areas (List[str]): Lista com duas áreas focais relevantes para o tema.
              
    Raises:
        ValueError: Se o parâmetro 'tema' não for fornecido ou for uma string vazia.
    """
    if not tema or not isinstance(tema, str):
        raise ValueError("O parâmetro 'tema' é obrigatório e deve ser uma string não vazia.")

    def call_external_api(tool_name: str) -> dict:
        """
        Simula chamada à API externa para obter dados simples sobre análise de problemas.

        Returns:
            Dict com campos simples apenas (str, int, float, bool):
            - analysis_topic (str): Tópico da análise baseado no tema fornecido
            - focus_area_0 (str): Primeira área focal da análise
            - focus_area_1 (str): Segunda área focal da análise
        """
        # Simulação de resposta com base no tema
        base_topic = tema.strip().title()
        return {
            "analysis_topic": base_topic,
            "focus_area_0": f"{base_topic} - Causas Raiz",
            "focus_area_1": f"{base_topic} - Impactos Sociais"
        }

    # Chama a API simulada para obter os dados
    api_data = call_external_api("mapas-mentais-server-problemas")

    # Constrói a estrutura aninhada conforme o esquema de saída esperado
    result = {
        "analysis_topic": api_data["analysis_topic"],
        "focus_areas": [
            api_data["focus_area_0"],
            api_data["focus_area_1"]
        ]
    }

    return result