from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for tourism content details.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - content_id (str): 고유 콘텐츠 식별자
        - title (str): 관광지/축제/숙박 시설의 이름 또는 제목
        - address (str): 도로명 또는 지번 주소
        - area_code (str): 지역 코드 (예: 서울=1, 부산=6 등)
        - category_code (str): 콘텐츠 분류 코드
        - default_info_tel (str): 대표 연락처 번호 (기본 정보 내)
        - default_info_homepage (str): 공식 웹사이트 URL (기본 정보 내)
        - default_info_use_time (str): 이용 가능 시간 또는 운영 시간 (기본 정보 내)
        - default_info_is_free (bool): 무료 여부 (기본 정보 내)
        - overview (str): 해당 콘텐츠에 대한 상세 개요 및 설명
        - representative_image (str): 대표 이미지 URL
        - image_0 (str): 첫 번째 추가 이미지 URL
        - image_1 (str): 두 번째 추가 이미지 URL
        - location_latitude (float): 위도
        - location_longitude (float): 경도
        - map_level (int): 지도 확대 레벨 정보
        - content_type (str): 콘텐츠 유형 (예: 관광지, 축제, 숙박 등)
        - created_time (str): 데이터 생성 일시 (ISO 8601 형식)
        - modified_time (str): 최종 수정 일시 (ISO 8601 형식)
        - success (bool): API 호출 성공 여부
        - error_message (str): 실패 시 오류 메시지 (성공 시 null)
    """
    return {
        "content_id": "123456",
        "title": "경복궁",
        "address": "서울특별시 종로구 세종대로 161",
        "area_code": "1",
        "category_code": "A01",
        "default_info_tel": "02-3700-3900",
        "default_info_homepage": "https://www.royalpalace.go.kr",
        "default_info_use_time": "09:00~18:00",
        "default_info_is_free": False,
        "overview": "조선 왕조의 정궁인 경복궁은 1395년에 건립되었습니다.",
        "representative_image": "https://example.com/images/gyeongbokgung_main.jpg",
        "image_0": "https://example.com/images/gyeongbokgung_01.jpg",
        "image_1": "https://example.com/images/gyeongbokgung_02.jpg",
        "location_latitude": 37.575757,
        "location_longitude": 126.976896,
        "map_level": 10,
        "content_type": "관광지",
        "created_time": "2023-01-01T00:00:00Z",
        "modified_time": "2023-12-01T12:30:00Z",
        "success": True,
        "error_message": None
    }

def korea_tour_get_detail_common(
    contentId: str,
    addrinfoYN: Optional[str] = None,
    areacodeYN: Optional[str] = None,
    defaultYN: Optional[str] = None,
    firstImageYN: Optional[str] = None,
    mapinfoYN: Optional[str] = None,
    overviewYN: Optional[str] = None
) -> Dict[str, Any]:
    """
    특정 관광지, 축제, 숙박 등의 상세 정보를 조회합니다. contentId를 기반으로 
    해당 콘텐츠의 공통 상세정보(제목, 주소, 개요 등)를 제공합니다.
    
    Args:
        contentId (str): 관광 콘텐츠 ID (필수)
        addrinfoYN (str, optional): 주소정보 조회여부(Y/N)
        areacodeYN (str, optional): 지역코드 조회여부(Y/N)
        defaultYN (str, optional): 기본정보 조회여부(Y/N)
        firstImageYN (str, optional): 대표이미지 조회여부(Y/N)
        mapinfoYN (str, optional): 좌표정보 조회여부(Y/N)
        overviewYN (str, optional): 개요정보 조회여부(Y/N)
    
    Returns:
        Dict containing detailed tourism content information with the following structure:
        - content_id (str): 고유 콘텐츠 식별자
        - title (str): 관광지/축제/숙박 시설의 이름 또는 제목
        - address (str): 도로명 또는 지번 주소
        - area_code (str): 지역 코드
        - category_code (str): 콘텐츠 분류 코드
        - default_info (Dict): 기본 정보 항목들 (전화번호, 홈페이지, 이용시간 등)
        - overview (str): 해당 콘텐츠에 대한 상세 개요 및 설명
        - representative_image (str): 대표 이미지 URL
        - images (List[str]): 추가 이미지들의 URL 목록
        - location (Dict): 위치 좌표 정보 (latitude, longitude)
        - map_level (int): 지도 확대 레벨 정보
        - content_type (str): 콘텐츠 유형
        - created_time (str): 데이터 생성 일시 (ISO 8601 형식)
        - modified_time (str): 최종 수정 일시 (ISO 8601 형식)
        - homepage (str): 공식 웹사이트 URL
        - tel (str): 대표 연락처 번호
        - use_time (str): 이용 가능 시간 또는 운영 시간
        - is_free (bool): 무료 여부
        - success (bool): API 호출 성공 여부
        - error_message (str): 실패 시 오류 메시지 (성공 시 null)
    """
    # Input validation
    if not contentId or not contentId.strip():
        return {
            "success": False,
            "error_message": "contentId is required",
            "content_id": "",
            "title": "",
            "address": "",
            "area_code": "",
            "category_code": "",
            "default_info": {},
            "overview": "",
            "representative_image": "",
            "images": [],
            "location": {"latitude": 0.0, "longitude": 0.0},
            "map_level": 0,
            "content_type": "",
            "created_time": "",
            "modified_time": "",
            "homepage": "",
            "tel": "",
            "use_time": "",
            "is_free": False
        }
    
    try:
        # Call external API to get flat data
        api_data = call_external_api("korea_tour_get_detail_common")
        
        # Construct nested structure matching output schema
        result = {
            "content_id": api_data.get("content_id", ""),
            "title": api_data.get("title", ""),
            "address": api_data.get("address", ""),
            "area_code": api_data.get("area_code", ""),
            "category_code": api_data.get("category_code", ""),
            "default_info": {
                "tel": api_data.get("default_info_tel", ""),
                "homepage": api_data.get("default_info_homepage", ""),
                "use_time": api_data.get("default_info_use_time", ""),
                "is_free": api_data.get("default_info_is_free", False)
            },
            "overview": api_data.get("overview", ""),
            "representative_image": api_data.get("representative_image", ""),
            "images": [
                api_data.get("image_0", ""),
                api_data.get("image_1", "")
            ],
            "location": {
                "latitude": api_data.get("location_latitude", 0.0),
                "longitude": api_data.get("location_longitude", 0.0)
            },
            "map_level": api_data.get("map_level", 0),
            "content_type": api_data.get("content_type", ""),
            "created_time": api_data.get("created_time", ""),
            "modified_time": api_data.get("modified_time", ""),
            "homepage": api_data.get("default_info_homepage", ""),
            "tel": api_data.get("default_info_tel", ""),
            "use_time": api_data.get("default_info_use_time", ""),
            "is_free": api_data.get("default_info_is_free", False),
            "success": api_data.get("success", False),
            "error_message": api_data.get("error_message", None)
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error_message": f"Internal error occurred: {str(e)}",
            "content_id": "",
            "title": "",
            "address": "",
            "area_code": "",
            "category_code": "",
            "default_info": {},
            "overview": "",
            "representative_image": "",
            "images": [],
            "location": {"latitude": 0.0, "longitude": 0.0},
            "map_level": 0,
            "content_type": "",
            "created_time": "",
            "modified_time": "",
            "homepage": "",
            "tel": "",
            "use_time": "",
            "is_free": False
        }