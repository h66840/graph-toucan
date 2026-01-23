from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for subway arrival information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (int): HTTP status code indicating the result of the request
        - code (str): Response code identifier for the outcome
        - message (str): Human-readable message describing the result or error
        - link (str): Optional reference link, may be empty
        - developerMessage (str): Message intended for developers, may be empty
        - total (int): Total number of results or items returned
    """
    return {
        "status": 200,
        "code": "INFO-200",
        "message": "정상 처리되었습니다.",
        "link": "",
        "developerMessage": "",
        "total": 2
    }

def subway_mcp_server_subway(station: str) -> Dict[str, Any]:
    """
    Retrieves subway arrival information for a given station.
    
    Args:
        station (str): The name of the subway station to query arrival information for.
        
    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - status (int): HTTP status code indicating the result of the request
            - code (str): Response code identifier for the outcome
            - message (str): Human-readable message describing the result or error
            - link (str): Optional reference link related to the response, may be empty
            - developerMessage (str): Message intended for developers, may be empty
            - total (int): Total number of results or items returned
    """
    if not station or not station.strip():
        return {
            "status": 400,
            "code": "ERROR-400",
            "message": "역 이름이 제공되지 않았습니다.",
            "link": "",
            "developerMessage": "The 'station' parameter is required.",
            "total": 0
        }
    
    api_data = call_external_api("subway-mcp-server-subway")
    
    result = {
        "status": api_data["status"],
        "code": api_data["code"],
        "message": api_data["message"],
        "link": api_data["link"],
        "developerMessage": api_data["developerMessage"],
        "total": api_data["total"]
    }
    
    return result