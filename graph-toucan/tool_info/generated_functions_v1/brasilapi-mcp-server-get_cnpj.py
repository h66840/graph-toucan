from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching CNPJ data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - uf (str): State abbreviation
        - cep (str): Postal code
        - qsa_nome (str): Name of partner/shareholder
        - qsa_qualificacao (str): Qualification of partner/shareholder
        - cnpj (str): CNPJ number
        - pais (str): Country name
        - email (str): Company email
        - porte (str): Size classification
        - bairro (str): Neighborhood
        - numero (str): Street number
        - ddd_fax (str): Fax area code
        - municipio (str): Municipality (city)
        - logradouro (str): Street name
        - cnae_fiscal (int): Main CNAE fiscal code
        - codigo_pais (str): Country code
        - complemento (str): Additional address info
        - codigo_porte (int): Numeric code for company size
        - razao_social (str): Legal company name
        - nome_fantasia (str): Trade name
        - capital_social (float): Social capital in BRL
        - ddd_telefone_1 (str): Primary phone area code
        - ddd_telefone_2 (str): Secondary phone area code
        - opcao_pelo_mei (bool): MEI regime status
        - codigo_municipio (int): Municipality internal code
        - cnaes_secundarios_0_codigo (int): First secondary CNAE code
        - cnaes_secundarios_0_descricao (str): First secondary CNAE description
        - cnaes_secundarios_1_codigo (int): Second secondary CNAE code
        - cnaes_secundarios_1_descricao (str): Second secondary CNAE description
        - natureza_juridica (str): Legal nature description
        - regime_tributario (str): Tax regime
        - situacao_especial (str): Special status
        - opcao_pelo_simples (bool): Simples Nacional regime status
        - situacao_cadastral (int): Registration status code
        - data_opcao_pelo_mei (str): MEI option date (YYYY-MM-DD)
        - data_exclusao_do_mei (str): MEI exclusion date (YYYY-MM-DD)
        - cnae_fiscal_descricao (str): Description of main CNAE
        - codigo_municipio_ibge (int): IBGE municipality code
        - data_inicio_atividade (str): Start date of operations (YYYY-MM-DD)
        - data_situacao_especial (str): Date of special situation
        - data_opcao_pelo_simples (str): Simples option date (YYYY-MM-DD)
        - data_situacao_cadastral (str): Registration status date (YYYY-MM-DD)
        - nome_cidade_no_exterior (str): City name if abroad
        - codigo_natureza_juridica (int): Legal nature code
        - data_exclusao_do_simples (str): Simples exclusion date (YYYY-MM-DD)
        - motivo_situacao_cadastral (int): Reason code for registration status
        - ente_federativo_responsavel (str): Government entity responsible
        - identificador_matriz_filial (int): 1 for head office, 2 for branch
        - qualificacao_do_responsavel (int): Qualification code of responsible
        - descricao_situacao_cadastral (str): Text description of registration status
        - descricao_tipo_de_logradouro (str): Type of street (e.g., AVENIDA)
        - descricao_motivo_situacao_cadastral (str): Text reason for status change
        - descricao_identificador_matriz_filial (str): "MATRIZ" or "FILIAL"
    """
    return {
        "uf": "SP",
        "cep": "01310-200",
        "qsa_nome": "JOAO SILVA",
        "qsa_qualificacao": "SÓCIO-ADMINISTRADOR",
        "cnpj": "12345678000195",
        "pais": "BRASIL",
        "email": "contato@empresa.com.br",
        "porte": "MICRO EMPRESA",
        "bairro": "BELA VISTA",
        "numero": "1000",
        "ddd_fax": "11",
        "municipio": "SAO PAULO",
        "logradouro": "AVENIDA PAULISTA",
        "cnae_fiscal": 6201500,
        "codigo_pais": "105",
        "complemento": "ANDAR 10",
        "codigo_porte": 3,
        "razao_social": "EMPRESA EXEMPLO LTDA",
        "nome_fantasia": "EMPRESA EXEMPLO",
        "capital_social": 15000.00,
        "ddd_telefone_1": "11",
        "ddd_telefone_2": "11",
        "opcao_pelo_mei": False,
        "codigo_municipio": 7123,
        "cnaes_secundarios_0_codigo": 6311900,
        "cnaes_secundarios_0_descricao": "TRATAMENTO DE DADOS, PROVISAO DE PORTAIS E OUTROS SERVICOS DE INFORMACAO",
        "cnaes_secundarios_1_codigo": 6499603,
        "cnaes_secundarios_1_descricao": "FUNDOS DE INVESTIMENTO",
        "natureza_juridica": "LTDA - LIMITADA",
        "regime_tributario": "SIMPLES NACIONAL",
        "situacao_especial": "",
        "opcao_pelo_simples": True,
        "situacao_cadastral": 2,
        "data_opcao_pelo_mei": "",
        "data_exclusao_do_mei": "",
        "cnae_fiscal_descricao": "DESENVOLVIMENTO DE PROGRAMAS DE COMPUTADOR",
        "codigo_municipio_ibge": 3550308,
        "data_inicio_atividade": "2010-05-20",
        "data_situacao_especial": "",
        "data_opcao_pelo_simples": "2015-01-01",
        "data_situacao_cadastral": "2023-01-01",
        "nome_cidade_no_exterior": "",
        "codigo_natureza_juridica": 2062,
        "data_exclusao_do_simples": "",
        "motivo_situacao_cadastral": 1,
        "ente_federativo_responsavel": "SECRETARIA DA RECEITA FEDERAL",
        "identificador_matriz_filial": 1,
        "qualificacao_do_responsavel": 49,
        "descricao_situacao_cadastral": "ATIVA",
        "descricao_tipo_de_logradouro": "AVENIDA",
        "descricao_motivo_situacao_cadastral": "SEM MOTIVO ESPECIFICO",
        "descricao_identificador_matriz_filial": "MATRIZ"
    }

def brasilapi_mcp_server_get_cnpj(CNPJ: str) -> Dict[str, Any]:
    """
    Get information about a company given a CNPJ.
    
    Args:
        CNPJ (str): The CNPJ to query (required)
    
    Returns:
        Dict containing company information with the following fields:
        - uf (str): state abbreviation (UF) where the company is located
        - cep (str): postal code (CEP) of the company's address
        - qsa (Dict): information about partners or shareholders; may contain keys like 'nome', 'qualificacao', etc.
        - cnpj (str): CNPJ number of the company
        - pais (str): country name if applicable, otherwise null
        - email (str): company email address if available, otherwise null
        - porte (str): size classification of the company (e.g., "MICRO EMPRESA")
        - bairro (str): neighborhood where the company is located
        - numero (str): street number of the company's address
        - ddd_fax (str): area code for fax number if available
        - municipio (str): municipality (city) where the company is located
        - logradouro (str): street name of the company's address
        - cnae_fiscal (int): main CNAE fiscal code representing the company's primary activity
        - codigo_pais (str): country code if applicable, otherwise null
        - complemento (str): additional address information (e.g., apartment, building)
        - codigo_porte (int): numeric code corresponding to company size classification
        - razao_social (str): legal name of the company
        - nome_fantasia (str): trade name or commonly used business name
        - capital_social (float): registered social capital in BRL
    """
    # Simulate API call using the helper function
    raw_data = call_external_api("get_cnpj")
    
    # Transform raw data into the expected structure
    transformed_data = {
        "uf": raw_data["uf"],
        "cep": raw_data["cep"],
        "qsa": {
            "nome": raw_data["qsa_nome"],
            "qualificacao": raw_data["qsa_qualificacao"]
        },
        "cnpj": raw_data["cnpj"],
        "pais": raw_data["pais"],
        "email": raw_data["email"],
        "porte": raw_data["porte"],
        "bairro": raw_data["bairro"],
        "numero": raw_data["numero"],
        "ddd_fax": raw_data["ddd_fax"],
        "municipio": raw_data["municipio"],
        "logradouro": raw_data["logradouro"],
        "cnae_fiscal": raw_data["cnae_fiscal"],
        "codigo_pais": raw_data["codigo_pais"],
        "complemento": raw_data["complemento"],
        "codigo_porte": raw_data["codigo_porte"],
        "razao_social": raw_data["razao_social"],
        "nome_fantasia": raw_data["nome_fantasia"],
        "capital_social": raw_data["capital_social"]
    }
    
    return transformed_data