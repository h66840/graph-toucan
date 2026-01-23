from typing import Dict,Any
def mapas_mentais_server_inicial(tema: str) -> Dict[str, Any]:
    """
    Gera um mapa mental de conhecimentos iniciais sobre o tema fornecido.
    
    Args:
        tema (str): O tema principal para o qual será gerado o mapa mental de conhecimentos iniciais.
        
    Returns:
        Dict contendo:
        - topic (str): o tema principal do mapa mental
        - focus_areas (List[Dict]): lista de áreas de foco com tarefas específicas, cada uma contendo:
            - area (str): nível cognitivo (ex: 'Lembrar', 'Compreender', 'Aplicar')
            - tasks (List[str]): lista de tarefas ou conteúdos associados a esse nível
    
    Raises:
        ValueError: Se o parâmetro 'tema' não for fornecido ou for uma string vazia.
    """
    if not tema or not isinstance(tema, str):
        raise ValueError("O parâmetro 'tema' é obrigatório e deve ser uma string não vazia.")

    def call_external_api(tool_name: str) -> Dict[str, Any]:
        """
        Simula uma chamada à API externa para obter dados simples sobre o tema.
        
        Returns:
            Dict com campos simples apenas (str, int, float, bool):
            - topic (str): tema principal do mapa mental
            - focus_area_0_area (str): nome da primeira área de foco
            - focus_area_0_task_0 (str): primeira tarefa da área 0
            - focus_area_0_task_1 (str): segunda tarefa da área 0
            - focus_area_1_area (str): nome da segunda área de foco
            - focus_area_1_task_0 (str): primeira tarefa da área 1
            - focus_area_1_task_1 (str): segunda tarefa da área 1
        """
        # Simulação de resposta da API com base no tema
        return {
            "topic": f"Conhecimentos Iniciais em {tema}",
            "focus_area_0_area": "Lembrar",
            "focus_area_0_task_0": f"Definir conceitos básicos de {tema}",
            "focus_area_0_task_1": f"Identificar elementos fundamentais de {tema}",
            "focus_area_1_area": "Compreender",
            "focus_area_1_task_0": f"Explicar como {tema} funciona",
            "focus_area_1_task_1": f"Relacionar {tema} com outros temas correlatos"
        }

    try:
        api_data = call_external_api("mapas-mentais-server-inicial")

        # Construção explícita da estrutura aninhada conforme o esquema de saída
        focus_areas = [
            {
                "area": api_data["focus_area_0_area"],
                "tasks": [
                    api_data["focus_area_0_task_0"],
                    api_data["focus_area_0_task_1"]
                ]
            },
            {
                "area": api_data["focus_area_1_area"],
                "tasks": [
                    api_data["focus_area_1_task_0"],
                    api_data["focus_area_1_task_1"]
                ]
            }
        ]

        result = {
            "topic": api_data["topic"],
            "focus_areas": focus_areas
        }

        return result

    except KeyError as e:
        raise RuntimeError(f"Campo esperado ausente na resposta da API: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Erro ao processar o mapa mental: {str(e)}")