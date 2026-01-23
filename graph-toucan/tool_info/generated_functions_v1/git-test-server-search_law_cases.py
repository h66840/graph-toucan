from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for law case search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - keyword (str): keyword used for the search query
        - page (int): current page number of the search results
        - target (str): service target identifier, typically "prec" for precedents
        - total_count (int): total number of matching cases found
        - section (str): search section or scope, e.g., "bdyText" for full text, "evtNm" for event name/title
        - result_0_id (str): ID of the first case result
        - result_0_사건번호 (str): case number of the first result
        - result_0_데이터출처명 (str): data source name of the first result
        - result_0_사건종류코드 (str): case type code of the first result
        - result_0_사건종류명 (str): case type name of the first result
        - result_0_선고 (str): verdict of the first result
        - result_0_선고일자 (str): decision date of the first result
        - result_0_판례일련번호 (str): precedent serial number of the first result
        - result_0_판결유형 (str): judgment type of the first result
        - result_0_법원명 (str): court name of the first result
        - result_0_판례상세링크 (str): detailed link to precedent of the first result
        - result_0_사건명 (str): case title of the first result
        - result_1_id (str): ID of the second case result
        - result_1_사건번호 (str): case number of the second result
        - result_1_데이터출처명 (str): data source name of the second result
        - result_1_사건종류코드 (str): case type code of the second result
        - result_1_사건종류명 (str): case type name of the second result
        - result_1_선고 (str): verdict of the second result
        - result_1_선고일자 (str): decision date of the second result
        - result_1_판례일련번호 (str): precedent serial number of the second result
        - result_1_판결유형 (str): judgment type of the second result
        - result_1_법원명 (str): court name of the second result
        - result_1_판례상세링크 (str): detailed link to precedent of the second result
        - result_1_사건명 (str): case title of the second result
    """
    return {
        "keyword": "계약 해지",
        "page": 1,
        "target": "prec",
        "total_count": 45,
        "section": "bdyText",
        "result_0_id": "prec_001",
        "result_0_사건번호": "2020다12345",
        "result_0_데이터출처명": "대법원",
        "result_0_사건종류코드": "민사",
        "result_0_사건종류명": "민사사건",
        "result_0_선고": "원고 일부 승소",
        "result_0_선고일자": "2020-12-15",
        "result_0_판례일련번호": "1234567890",
        "result_0_판결유형": "확정",
        "result_0_법원명": "서울중앙지방법원",
        "result_0_판례상세링크": "https://www.law.go.kr/precDetail.do?precSeq=1234567890",
        "result_0_사건명": "원고와 피고 사이의 계약 해지 관련 사건",
        "result_1_id": "prec_002",
        "result_1_사건번호": "2019가23456",
        "result_1_데이터출처명": "대법원",
        "result_1_사건종류코드": "형사",
        "result_1_사건종류명": "형사사건",
        "result_1_선고": "피고인 무죄",
        "result_1_선고일자": "2019-08-20",
        "result_1_판례일련번호": "0987654321",
        "result_1_판결유형": "확정",
        "result_1_법원명": "부산지방법원",
        "result_1_판례상세링크": "https://www.law.go.kr/precDetail.do?precSeq=0987654321",
        "result_1_사건명": "피고인의 계약 위반 혐의 사건",
    }


def git_test_server_search_law_cases(
    OC: str,
    target: str = "prec",
    type: str = "JSON",
    search: Optional[int] = None,
    query: Optional[str] = None,
    display: Optional[int] = 20,
    page: Optional[int] = 1,
    org: Optional[str] = None,
    curt: Optional[str] = None,
    JO: Optional[str] = None,
    gana: Optional[str] = None,
    sort: Optional[str] = None,
    date: Optional[int] = None,
    prncYd: Optional[str] = None,
    nb: Optional[str] = None,
    datSrcNm: Optional[str] = None,
    popYn: Optional[str] = None,
) -> Dict[str, Any]:
    """
    법제처 판례 목록 조회 API를 호출합니다.

    Args:
        OC (str): 사용자 이메일 ID (필수).
        target (str): 서비스 대상 (기본값: "prec").
        type (str): 출력 형태 (기본값: "JSON", HTML/XML/JSON).
        search (Optional[int]): 검색 범위 (1: 판례명, 2: 본문검색).
        query (Optional[str]): 검색을 원하는 질의.
        display (Optional[int]): 검색 결과 개수 (기본값: 20, 최대: 100).
        page (Optional[int]): 검색 결과 페이지 (기본값: 1).
        org (Optional[str]): 법원 종류 (예: 400201, 400202).
        curt (Optional[str]): 법원명 (예: 대법원, 서울고등법원).
        JO (Optional[str]): 참조법령명.
        gana (Optional[str]): 사전식 검색.
        sort (Optional[str]): 정렬 옵션.
        date (Optional[int]): 판례 선고일자.
        prncYd (Optional[str]): 선고일자 검색 범위 (예: "20090101~20090130").
        nb (Optional[str]): 판례 사건번호.
        datSrcNm (Optional[str]): 데이터 출처명.
        popYn (Optional[str]): 상세화면 팝업창 여부 (팝업창으로 띄우고 싶을 때: "Y").

    Returns:
        dict: API 응답 (JSON 형식) with the following structure:
            - keyword (str): keyword used for the search query
            - page (int): current page number of the search results
            - target (str): service target identifier, typically "prec" for precedents
            - total_count (int): total number of matching cases found
            - section (str): search section or scope, e.g., "bdyText" for full text, "evtNm" for event name/title
            - results (List[Dict]): list of case records, each containing:
                - id (str)
                - 사건번호 (str)
                - 데이터출처명 (str)
                - 사건종류코드 (str)
                - 사건종류명 (str)
                - 선고 (str)
                - 선고일자 (str)
                - 판례일련번호 (str)
                - 판결유형 (str)
                - 법원명 (str)
                - 판례상세링크 (str)
                - 사건명 (str)
    """
    if not OC:
        raise ValueError("OC (사용자 이메일 ID) is required.")

    # Fetch simulated external API data
    api_data = call_external_api("git-test-server-search_law_cases")

    # Construct results list from flattened API data
    results = [
        {
            "id": api_data["result_0_id"],
            "사건번호": api_data["result_0_사건번호"],
            "데이터출처명": api_data["result_0_데이터출처명"],
            "사건종류코드": api_data["result_0_사건종류코드"],
            "사건종류명": api_data["result_0_사건종류명"],
            "선고": api_data["result_0_선고"],
            "선고일자": api_data["result_0_선고일자"],
            "판례일련번호": api_data["result_0_판례일련번호"],
            "판결유형": api_data["result_0_판결유형"],
            "법원명": api_data["result_0_법원명"],
            "판례상세링크": api_data["result_0_판례상세링크"],
            "사건명": api_data["result_0_사건명"],
        },
        {
            "id": api_data["result_1_id"],
            "사건번호": api_data["result_1_사건번호"],
            "데이터출처명": api_data["result_1_데이터출처명"],
            "사건종류코드": api_data["result_1_사건종류코드"],
            "사건종류명": api_data["result_1_사건종류명"],
            "선고": api_data["result_1_선고"],
            "선고일자": api_data["result_1_선고일자"],
            "판례일련번호": api_data["result_1_판례일련번호"],
            "판결유형": api_data["result_1_판결유형"],
            "법원명": api_data["result_1_법원명"],
            "판례상세링크": api_data["result_1_판례상세링크"],
            "사건명": api_data["result_1_사건명"],
        },
    ]

    return {
        "keyword": api_data["keyword"],
        "page": api_data["page"],
        "target": api_data["target"],
        "total_count": api_data["total_count"],
        "section": api_data["section"],
        "results": results,
    }