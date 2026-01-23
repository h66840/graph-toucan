from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for sexual offender residence change notices.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - header_resultCode (str): Result code of the API response
        - header_resultMsg (str): Result message describing the status
        - body_numOfRows (int): Number of rows per page
        - body_totalCount (int): Total number of records available
        - body_pageNo (int): Current page number
        - body_resultType (str): Format type of the result (e.g., "json")
        - body_items_0_dataCrtYmd (str): Record creation date for first item (YYYYMMDD)
        - body_items_0_stdgCd (str): Administrative dong-level code for first item
        - body_items_0_mtnYn (str): Modification flag for first item ('1' or '0')
        - body_items_0_mno (int): Main management number for first item
        - body_items_0_sno (int): Sub-number for first item
        - body_items_0_stdgCtpvSggCd (str): City/county/district code for first item
        - body_items_0_stdgEmdCd (str): Eup/myeon/dong code for first item
        - body_items_0_roadNmNo (str): Road name lot number for first item
        - body_items_0_udgdYn (str): Underground structure flag for first item
        - body_items_0_bmno (int): Building main number for first item
        - body_items_0_bsno (int): Building sub-number for first item
        - body_items_0_ctpvNm (str): Metropolitan/province name for first item
        - body_items_0_sggNm (str): District (gu) name for first item
        - body_items_0_umdNm (str): Neighborhood (dong/eup/myeon) name for first item
        - body_items_0_stliNm (str): Street name for first item (empty if not applicable)
        - body_items_0_rprsLotnoYn (str): Representative lot number flag for first item
        - body_items_1_dataCrtYmd (str): Record creation date for second item (YYYYMMDD)
        - body_items_1_stdgCd (str): Administrative dong-level code for second item
        - body_items_1_mtnYn (str): Modification flag for second item ('1' or '0')
        - body_items_1_mno (int): Main management number for second item
        - body_items_1_sno (int): Sub-number for second item
        - body_items_1_stdgCtpvSggCd (str): City/county/district code for second item
        - body_items_1_stdgEmdCd (str): Eup/myeon/dong code for second item
        - body_items_1_roadNmNo (str): Road name lot number for second item
        - body_items_1_udgdYn (str): Underground structure flag for second item
        - body_items_1_bmno (int): Building main number for second item
        - body_items_1_bsno (int): Building sub-number for second item
        - body_items_1_ctpvNm (str): Metropolitan/province name for second item
        - body_items_1_sggNm (str): District (gu) name for second item
        - body_items_1_umdNm (str): Neighborhood (dong/eup/myeon) name for second item
        - body_items_1_stliNm (str): Street name for second item (empty if not applicable)
        - body_items_1_rprsLotnoYn (str): Representative lot number flag for second item
    """
    return {
        "header_resultCode": "00",
        "header_resultMsg": "NORMAL SERVICE",
        "body_numOfRows": 10,
        "body_totalCount": 25,
        "body_pageNo": 1,
        "body_resultType": "json",
        "body_items_0_dataCrtYmd": "20231201",
        "body_items_0_stdgCd": "1111010100",
        "body_items_0_mtnYn": "0",
        "body_items_0_mno": 1001,
        "body_items_0_sno": 1,
        "body_items_0_stdgCtpvSggCd": "11110",
        "body_items_0_stdgEmdCd": "11110101",
        "body_items_0_roadNmNo": "123-45",
        "body_items_0_udgdYn": "0",
        "body_items_0_bmno": 123,
        "body_items_0_bsno": 45,
        "body_items_0_ctpvNm": "서울특별시",
        "body_items_0_sggNm": "종로구",
        "body_items_0_umdNm": "사직동",
        "body_items_0_stliNm": "세종대로",
        "body_items_0_rprsLotnoYn": "1",
        "body_items_1_dataCrtYmd": "20231202",
        "body_items_1_stdgCd": "2311010200",
        "body_items_1_mtnYn": "1",
        "body_items_1_mno": 1002,
        "body_items_1_sno": 1,
        "body_items_1_stdgCtpvSggCd": "23110",
        "body_items_1_stdgEmdCd": "23110102",
        "body_items_1_roadNmNo": "678-90",
        "body_items_1_udgdYn": "1",
        "body_items_1_bmno": 678,
        "body_items_1_bsno": 90,
        "body_items_1_ctpvNm": "경기도",
        "body_items_1_sggNm": "수원시 장안구",
        "body_items_1_umdNm": "파장동",
        "body_items_1_stliNm": "파장로",
        "body_items_1_rprsLotnoYn": "0",
    }


def git_test_server_get_sexual_abuse_notice_house_jibun(
    pageNo: Optional[int] = 1,
    numOfRows: Optional[int] = 10,
    type: Optional[str] = "json",
    service_key: Optional[str] = None,
    chgBfrCtpvNm: Optional[str] = None,
    chgBfrSggNm: Optional[str] = None,
    chgBfrUmdNm: Optional[str] = None,
) -> Dict[str, Any]:
    """
    성범죄자 주거이동정보 조회 API를 호출합니다.

    Args:
        pageNo (int, optional): 페이지 번호 (기본값: 1).
        numOfRows (int, optional): 한 페이지 결과 수 (기본값: 10).
        type (str, optional): 응답 데이터 타입 (기본값: "json").
        service_key (str, optional): API 서비스 키.
        chgBfrCtpvNm (str, optional): 변경이전시도명
        chgBfrSggNm (str, optional): 변경이전시군구명
        chgBfrUmdNm (str, optional): 변경이전읍면동명

    Returns:
        dict: 성범죄자 주거이동정보 (JSON 형식) with the following structure:
        - header (dict): Contains resultCode and resultMsg
        - body (dict): Contains pagination and result data including:
          - numOfRows (int)
          - totalCount (int)
          - pageNo (int)
          - resultType (str)
          - items (list of dicts): List of individual registered sexual offender residence change notices
            Each item contains:
            - dataCrtYmd (str)
            - stdgCd (str)
            - mtnYn (str)
            - mno (int)
            - sno (int)
            - stdgCtpvSggCd (str)
            - stdgEmdCd (str)
            - roadNmNo (str)
            - udgdYn (str)
            - bmno (int)
            - bsno (int)
            - ctpvNm (str)
            - sggNm (str)
            - umdNm (str)
            - stliNm (str)
            - rprsLotnoYn (str)
    """
    # Validate inputs
    if pageNo is not None and (not isinstance(pageNo, int) or pageNo < 1):
        raise ValueError("pageNo must be a positive integer")
    if numOfRows is not None and (not isinstance(numOfRows, int) or numOfRows < 1):
        raise ValueError("numOfRows must be a positive integer")

    # Call external API (simulated)
    api_data = call_external_api("git-test-server-get_sexual_abuse_notice_house_jibun")
    
    # Construct result in nested format
    result = {
        "header": {
            "resultCode": api_data["header_resultCode"],
            "resultMsg": api_data["header_resultMsg"]
        },
        "body": {
            "numOfRows": api_data["body_numOfRows"],
            "totalCount": api_data["body_totalCount"],
            "pageNo": api_data["body_pageNo"],
            "resultType": api_data["body_resultType"],
            "items": []
        }
    }

    # Add items
    for i in range(2):  # We have two items in the mock data
        item = {
            "dataCrtYmd": api_data[f"body_items_{i}_dataCrtYmd"],
            "stdgCd": api_data[f"body_items_{i}_stdgCd"],
            "mtnYn": api_data[f"body_items_{i}_mtnYn"],
            "mno": api_data[f"body_items_{i}_mno"],
            "sno": api_data[f"body_items_{i}_sno"],
            "stdgCtpvSggCd": api_data[f"body_items_{i}_stdgCtpvSggCd"],
            "stdgEmdCd": api_data[f"body_items_{i}_stdgEmdCd"],
            "roadNmNo": api_data[f"body_items_{i}_roadNmNo"],
            "udgdYn": api_data[f"body_items_{i}_udgdYn"],
            "bmno": api_data[f"body_items_{i}_bmno"],
            "bsno": api_data[f"body_items_{i}_bsno"],
            "ctpvNm": api_data[f"body_items_{i}_ctpvNm"],
            "sggNm": api_data[f"body_items_{i}_sggNm"],
            "umdNm": api_data[f"body_items_{i}_umdNm"],
            "stliNm": api_data[f"body_items_{i}_stliNm"],
            "rprsLotnoYn": api_data[f"body_items_{i}_rprsLotnoYn"]
        }
        result["body"]["items"].append(item)

    return result