from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Brazilian bank information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - code (str): Bank code as a string
        - name (str): Short name of the bank
        - full_name (str): Full legal name of the bank
        - ispb (str): ISPB (Identificador do Sistema de Pagamentos Brasileiro) code of the bank
    """
    return {
        "code": "237",
        "name": "Bradesco",
        "full_name": "Banco Bradesco S.A.",
        "ispb": "60746948"
    }

def brasil_api_bank_search(code: str) -> Dict[str, str]:
    """
    Find information about a Brazilian bank by its code.
    
    This function simulates querying an external API to retrieve bank details
    based on the provided bank code. It returns the bank's code, short name,
    full legal name, and ISPB code.
    
    Args:
        code (str): Bank code to search for (required)
    
    Returns:
        Dict[str, str]: A dictionary containing the following keys:
            - code (str): bank code as a string
            - name (str): short name of the bank
            - full_name (str): full legal name of the bank
            - ispb (str): ISPB code of the bank
    
    Raises:
        ValueError: If the code is empty or not provided
    """
    if not code:
        raise ValueError("Bank code is required")
    
    # Call external API (simulated)
    api_data = call_external_api("brasil-api-bank-search")
    
    # Construct result matching output schema
    result = {
        "code": api_data["code"],
        "name": api_data["name"],
        "full_name": api_data["full_name"],
        "ispb": api_data["ispb"]
    }
    
    return result