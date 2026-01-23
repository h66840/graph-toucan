from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for law case body retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - raw_response (str): Raw HTML response containing full case body
        - PrecService_pansisageon (str): Summary of legal principles established in the case
        - PrecService_chamjopanrye (str): List of cited precedents supporting the current ruling
        - PrecService_sageonjongyumyeong (str): Type/category of the case (e.g., 민사 for civil)
        - PrecService_panjelyoji (str): Concise summary of the court's judgment and reasoning
        - PrecService_chamjojomun (str): Relevant statutory provisions referenced in the decision
        - PrecService_seonogilja (str): Date when the ruling was pronounced, in YYYYMMDD format
        - PrecService_beomwonmyeong (str): Name of the court that issued the ruling (e.g., 대법원)
        - PrecService_sageonmyeong (str): Title/description of the case (e.g., 사해행위취소)
        - PrecService_panryeneoyong (str): Full textual content of the court’s opinion
        - PrecService_sageonbeonho (str): Official case number assigned by the court
        - PrecService_sageonjongyukode (str): Numeric code representing the case category
        - PrecService_panryejeongbowonilbyeon (str): Unique serial number identifying the precedent
        - PrecService_seonogo (str): Type of announcement (e.g., "선고")
        - PrecService_panjelyuryeong (str): Nature of the decision (e.g., "판결")
        - PrecService_beomwonjongyukode (str): Code indicating the type of court
    """
    return {
        "raw_response": "<html><body><p>이 판결은 민사 사건에 관한 것으로, 사해행위취소에 대한 법리를 다룹니다.</p></body></html>",
        "PrecService_pansisageon": "채무자가 채권자에게 해를 끼칠 목적으로 재산을 처분한 경우, 채권자는 그 행위를 취소할 수 있다.",
        "PrecService_chamjopanrye": "대법원 2000다12345, 대법원 2005다67890",
        "PrecService_sageonjongyumyeong": "민사",
        "PrecService_panjelyoji": "채무자의 재산处分이 채권자에게 해를 끼쳤다면, 채권자는 사해행위취소소송을 제기할 수 있으며, 이는 공정한 거래질서를 유지하기 위한 것이다.",
        "PrecService_chamjojomun": "민법 제406조",
        "PrecService_seonogilja": "20231215",
        "PrecService_beomwonmyeong": "대법원",
        "PrecService_sageonmyeong": "사해행위취소",
        "PrecService_panryeneoyong": "원고는 피고가 제3자에게 부동산을 무상으로 이전한 행위가 자신에게 해를 끼쳤다고 주장하며, 이 사건 부동산 이전행위의 취소를 구한다. 피고는 이에 반박하며 자금 조달 내역을 제출하였다. 법원은 채무자의 행위가 채권자에게 해를 끼쳤음을 인정하고, 원고의 청구를 인용한다.",
        "PrecService_sageonbeonho": "2023다123456",
        "PrecService_sageonjongyukode": "100",
        "PrecService_panryejeongbowonilbyeon": "2023000001",
        "PrecService_seonogo": "선고",
        "PrecService_panjelyuryeong": "판결",
        "PrecService_beomwonjongyukode": "10"
    }

def git_test_server_get_law_case_body(
    ID: str,
    OC: str = "trojansaga",
    target: str = "prec",
    type: str = "HTML",
    LM: Optional[str] = None
) -> Dict[str, Any]:
    """
    법제처 판례 본문 조회 API를 호출하여 판례 본문 정보를 반환합니다.
    
    Args:
        ID (str): 판례 일련번호 (필수)
        OC (str): 사용자 이메일 ID (기본값: "trojansaga")
        target (str): 서비스 대상 (기본값: "prec")
        type (str): 출력 형태 (기본값: "HTML", HTML/XML/JSON)
        LM (Optional[str]): 판례명 (선택 사항)
    
    Returns:
        dict: API 응답 데이터를 포함하며, 다음 구조를 가집니다:
            - raw_response (str): API로부터 수신된 원시 HTML 또는 텍스트 응답
            - PrecService (Dict): 구조화된 판례 정보를 포함하는 중첩 객체로,
              다음 필드를 포함:
                - 판시사항 (str): 법적 원칙 요약
                - 참조판례 (str): 인용된 판례 목록
                - 사건종류명 (str): 사건 유형 (예: 민사)
                - 판결요지 (str): 판결 핵심 요약
                - 참조조문 (str): 관련 법률 조항
                - 선고일자 (str): 판결 선고일 (YYYYMMDD 형식)
                - 법원명 (str): 판결을 내린 법원 이름
                - 사건명 (str): 사건 제목
                - 판례내용 (str): 판결 전문
                - 사건번호 (str): 사건 번호
                - 사건종류코드 (str): 사건 유형 코드
                - 판례정보일련번호 (str): 판례 고유 번호
                - 선고 (str): 선고 여부
                - 판결유형 (str): 판결 종류
                - 법원종류코드 (str): 법원 유형 코드
    """
    # 입력 유효성 검사
    if not ID:
        raise ValueError("ID는 필수 입력 항목입니다.")
    
    if type not in ["HTML", "XML", "JSON"]:
        raise ValueError("type은 'HTML', 'XML', 'JSON' 중 하나여야 합니다.")
    
    # 외부 API 호출 (모의)
    api_data = call_external_api("git-test-server-get_law_case_body")
    
    # 중첩된 PrecService 객체 구성
    PrecService = {
        "판시사항": api_data["PrecService_pansisageon"],
        "참조판례": api_data["PrecService_chamjopanrye"],
        "사건종류명": api_data["PrecService_sageonjongyumyeong"],
        "판결요지": api_data["PrecService_panjelyoji"],
        "참조조문": api_data["PrecService_chamjojomun"],
        "선고일자": api_data["PrecService_seonogilja"],
        "법원명": api_data["PrecService_beomwonmyeong"],
        "사건명": api_data["PrecService_sageonmyeong"],
        "판례내용": api_data["PrecService_panryeneoyong"],
        "사건번호": api_data["PrecService_sageonbeonho"],
        "사건종류코드": api_data["PrecService_sageonjongyukode"],
        "판례정보일련번호": api_data["PrecService_panryejeongbowonilbyeon"],
        "선고": api_data["PrecService_seonogo"],
        "판결유형": api_data["PrecService_panjelyuryeong"],
        "법원종류코드": api_data["PrecService_beomwonjongyukode"]
    }
    
    # 최종 결과 반환
    return {
        "raw_response": api_data["raw_response"],
        "PrecService": PrecService
    }