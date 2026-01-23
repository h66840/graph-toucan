from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for airport congestion information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if the request fails
        - status_code (int): HTTP status code of the response
        - url (str): The requested URL that resulted in the error
        - details (str): Additional information about the error
    """
    return {
        "error": "",
        "status_code": 200,
        "url": "https://api.example.com/airport-congestion?page=1&perPage=10&returnType=JSON",
        "details": "Request successful"
    }

def git_test_server_get_airport_congestion(
    page: int = 1,
    perPage: int = 10,
    returnType: str = "JSON",
    iata_apcd: Optional[str] = None,
    service_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    공항 혼잡도 정보를 조회합니다.
    
    Args:
        page (int): 페이지 인덱스 (기본값: 1).
        perPage (int): 페이지 크기 (기본값: 10).
        returnType (str): 응답 데이터 타입 (기본값: "JSON", XML도 가능).
        iata_apcd (Optional[str]): IATA 공항 코드 (예: ICN, GMP).
        service_key (Optional[str]): API 서비스 키.
    
    Returns:
        dict: 공항 혼잡도 정보 (JSON 형식 또는 원시 텍스트).
        The returned dictionary contains the following keys:
        - error (str): error message returned when the API request fails
        - status_code (int): HTTP status code indicating the result of the request
        - url (str): the requested URL that resulted in the error
        - details (str): additional information about the error, such as client error description or documentation link
    """
    # Validate inputs
    if page < 1:
        return {
            "error": "Page must be a positive integer.",
            "status_code": 400,
            "url": "",
            "details": "Invalid page parameter. Must be >= 1."
        }
    
    if perPage < 1:
        return {
            "error": "PerPage must be a positive integer.",
            "status_code": 400,
            "url": "",
            "details": "Invalid perPage parameter. Must be >= 1."
        }
    
    if returnType not in ["JSON", "XML"]:
        return {
            "error": "Return type must be either 'JSON' or 'XML'.",
            "status_code": 400,
            "url": "",
            "details": "Invalid returnType parameter. Supported values: JSON, XML."
        }
    
    # Construct query parameters
    params = []
    if page is not None:
        params.append(f"page={page}")
    if perPage is not None:
        params.append(f"perPage={perPage}")
    if returnType is not None:
        params.append(f"returnType={returnType}")
    if iata_apcd is not None:
        params.append(f"iata_apcd={iata_apcd}")
    if service_key is not None:
        params.append(f"service_key={service_key}")
    
    base_url = "https://api.example.com/airport-congestion"
    url = f"{base_url}?{'&'.join(params)}"
    
    # Call external API (simulated)
    api_data = call_external_api("git-test-server-get_airport_congestion")
    
    # Construct result using flat data from external API
    result = {
        "error": api_data["error"],
        "status_code": api_data["status_code"],
        "url": url,
        "details": api_data["details"]
    }
    
    return result