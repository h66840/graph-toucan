from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for tour information search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if API request fails
        - item_0_title (str): Title of the first tour item
        - item_0_addr (str): Address of the first tour item
        - item_0_tel (str): Phone number of the first tour item
        - item_1_title (str): Title of the second tour item
        - item_1_addr (str): Address of the second tour item
        - item_1_tel (str): Phone number of the second tour item
    """
    return {
        "error": "",
        "item_0_title": "경복궁",
        "item_0_addr": "서울특별시 종로구 사직로 161",
        "item_0_tel": "02-3700-3900",
        "item_1_title": "N서울타워",
        "item_1_addr": "서울특별시 용산구 남산공원길 105",
        "item_1_tel": "02-3455-9277"
    }

def korea_tour_search_tour_info(
    areaCode: Optional[str] = None,
    contentTypeId: Optional[str] = None,
    keyword: Optional[str] = None,
    mapX: Optional[str] = None,
    mapY: Optional[str] = None,
    radius: Optional[str] = None
) -> Dict[str, Any]:
    """
    지역, 유형, 키워드 등을 기반으로 관광 정보를 검색합니다. 
    지역기반, 키워드 기반, 위치기반 검색을 지원합니다.
    
    Parameters:
        areaCode (str, optional): 지역코드
        contentTypeId (str, optional): 관광타입 (12:관광지, 14:문화시설, 15:축제공연행사, 25:여행코스, 28:레포츠, 32:숙박, 38:쇼핑, 39:음식점)
        keyword (str, optional): 검색 키워드
        mapX (str, optional): 경도 좌표
        mapY (str, optional): 위도 좌표
        radius (str, optional): 거리 반경(미터)
    
    Returns:
        Dict containing:
            - error (str): Error message if any occurred during processing
            - items (List[Dict]): List of tour information items with title, address, and phone
    """
    # Validate inputs
    if not any([areaCode, keyword, (mapX and mapY)]):
        return {"error": "At least one of areaCode, keyword, or map coordinates must be provided"}
    
    # Call external API (simulated)
    api_data = call_external_api("korea-tour-search_tour_info")
    
    # Construct result structure
    result = {
        "error": api_data["error"],
        "items": [
            {
                "title": api_data["item_0_title"],
                "address": api_data["item_0_addr"],
                "telephone": api_data["item_0_tel"]
            },
            {
                "title": api_data["item_1_title"],
                "address": api_data["item_1_addr"],
                "telephone": api_data["item_1_tel"]
            }
        ]
    }
    
    return result