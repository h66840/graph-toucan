from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - ispb (str): ISPB code of the bank
        - name (str): Short name of the bank
        - code (int): Three-digit bank code
        - fullName (str): Full legal name of the bank
    """
    return {
        "ispb": "00000000",
        "name": "Banco do Brasil",
        "code": 1,
        "fullName": "Banco do Brasil S.A."
    }

def brasilapi_mcp_server_get_bank_by_code(code: int) -> Dict[str, Any]:
    """
    Get information from a specific bank given its code.
    
    Args:
        code (int): Three-digit bank code used in Brazil's banking system
        
    Returns:
        Dict[str, Any]: Dictionary containing bank information with keys:
            - ispb (str): ISPB code of the bank
            - name (str): Short name of the bank
            - code (int): Three-digit bank code
            - fullName (str): Full legal name of the bank
    """
    if not isinstance(code, int) or code <= 0 or code > 999:
        raise ValueError("Bank code must be a positive three-digit integer (1-999)")
    
    api_data = call_external_api("brasilapi-mcp-server-get_bank_by_code")
    
    result = {
        "ispb": api_data["ispb"],
        "name": api_data["name"],
        "code": api_data["code"],
        "fullName": api_data["fullName"]
    }
    
    return result