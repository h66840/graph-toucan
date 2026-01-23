def mapas_mentais_server_revisa(tema: str) -> dict:
    """
    Gera um mapa mental para revisão de conteúdo sobre um tema.
    
    Args:
        tema (str): O tema principal do mapa mental de revisão
        
    Returns:
        dict: Um dicionário contendo a estrutura do mapa mental com os seguintes campos:
            - main_topic (str): o tema principal fornecido
            - focus_instructions (List[str]): lista de instruções estruturais para construção do mapa
            - primary_branches (str): descrição indicando que subtemas são usados como ramificações primárias
            - secondary_branches (str): descrição indicando que detalhes e exemplos são usados como ramificações secundárias
    
    Raises:
        ValueError: Se o parâmetro 'tema' não for fornecido ou for uma string vazia
    """
    # Validação da entrada
    if not tema or not isinstance(tema, str):
        raise ValueError("O parâmetro 'tema' é obrigatório e deve ser uma string não vazia.")
    
    # Lógica de computação pura baseada no tema fornecido
    main_topic = tema.strip()
    
    focus_instructions = [
        "Organize o conteúdo em tópicos principais derivados do tema central.",
        "Use palavras-chave concisas em vez de frases longas.",
        "Estruture hierarquicamente a partir do centro para as extremidades.",
        "Utilize cores diferentes para cada ramo principal para facilitar a memorização.",
        "Incorpore ícones ou símbolos simples para representar categorias."
    ]
    
    primary_branches = "Subtópicos relacionados ao tema são utilizados como ramificações primárias no mapa mental."
    secondary_branches = "Detalhes específicos, definições, datas, nomes e exemplos são organizados como ramificações secundárias."

    return {
        "main_topic": main_topic,
        "focus_instructions": focus_instructions,
        "primary_branches": primary_branches,
        "secondary_branches": secondary_branches
    }