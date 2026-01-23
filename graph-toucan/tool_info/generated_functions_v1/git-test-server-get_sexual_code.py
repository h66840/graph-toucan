from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - item_0_codeId (str): 코드 식별자 (첫 번째 항목)
        - item_0_codeName (str): 코드 이름 (첫 번째 항목)
        - item_0_description (str): 설명 (첫 번째 항목)
        - item_1_codeId (str): 코드 식별자 (두 번째 항목)
        - item_1_codeName (str): 코드 이름 (두 번째 항목)
        - item_1_description (str): 설명 (두 번째 항목)
        - totalCount (int): 전체 성범죄자 코드 수
        - pageNo (int): 현재 페이지 번호
        - numOfRows (int): 한 페이지당 반환된 데이터 수
        - resultMessage (str): API 처리 결과 메시지
        - resultCode (str): API 결과 코드
        - hasNextPage (bool): 다음 페이지 존재 여부
    """
    return {
        "item_0_codeId": "SEX_CODE_001",
        "item_0_codeName": "성폭력 범죄",
        "item_0_description": "성폭력 관련 범죄 유형",
        "item_1_codeId": "SEX_CODE_002",
        "item_1_codeName": "아동 성범죄",
        "item_1_description": "아동 대상 성범죄 유형",
        "totalCount": 50,
        "pageNo": 1,
        "numOfRows": 2,
        "resultMessage": "SUCCESS",
        "resultCode": "00",
        "hasNextPage": True
    }

def git_test_server_get_sexual_code(
    pageNo: Optional[int] = 1,
    numOfRows: Optional[int] = 1,
    type: Optional[str] = "json",
    service_key: Optional[str] = "service_key_decoding"
) -> Dict[str, Any]:
    """
    성범죄자 코드 목록 조회 API를 호출합니다.

    Args:
        pageNo (int, optional): 페이지 번호 (기본값: 1)
        numOfRows (int, optional): 한 페이지 결과 수 (기본값: 1)
        type (str, optional): 응답 데이터 타입 (기본값: "json")
        service_key (str, optional): API 서비스 키 (기본값: service_key_decoding)

    Returns:
        dict: 성범죄자 코드 목록 (JSON 형식)
            - items (List[Dict]): 리스트 형태의 성범죄자 코드 정보. 각 항목은 코드 식별자, 코드 이름, 설명 등을 포함
            - totalCount (int): 전체 성범죄자 코드 수 (페이징 계산용)
            - pageNo (int): 현재 페이지 번호 (응답과 요청의 일관성 확인용)
            - numOfRows (int): 한 페이지당 반환된 데이터 수
            - resultMessage (str): API 처리 결과 메시지 (예: SUCCESS, FAIL 등)
            - resultCode (str): API 결과 코드 (예: 00, 99 등)
            - hasNextPage (bool): 다음 페이지가 존재하는지 여부
    """
    # Input validation
    if pageNo is not None and (not isinstance(pageNo, int) or pageNo < 1):
        raise ValueError("pageNo must be a positive integer")
    if numOfRows is not None and (not isinstance(numOfRows, int) or numOfRows < 1):
        raise ValueError("numOfRows must be a positive integer")
    if type not in ["json", "xml"]:
        raise ValueError("type must be either 'json' or 'xml'")

    # Call external API (simulated)
    api_data = call_external_api("git-test-server-get_sexual_code")

    # Construct items list from flattened fields
    items = [
        {
            "codeId": api_data["item_0_codeId"],
            "codeName": api_data["item_0_codeName"],
            "description": api_data["item_0_description"]
        },
        {
            "codeId": api_data["item_1_codeId"],
            "codeName": api_data["item_1_codeName"],
            "description": api_data["item_1_description"]
        }
    ]

    # Build final response structure
    result = {
        "items": items,
        "totalCount": api_data["totalCount"],
        "pageNo": api_data["pageNo"],
        "numOfRows": api_data["numOfRows"],
        "resultMessage": api_data["resultMessage"],
        "resultCode": api_data["resultCode"],
        "hasNextPage": api_data["hasNextPage"]
    }

    return result