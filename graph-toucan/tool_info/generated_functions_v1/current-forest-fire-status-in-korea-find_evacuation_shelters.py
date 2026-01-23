from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching evacuation shelter data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Whether the search was successful
        - error (str): Error message if failed, otherwise empty string
        - query (str): The actual search query used
        - result_0_title (str): Title of first evacuation shelter result
        - result_0_link (str): Link of first evacuation shelter result
        - result_0_snippet (str): Snippet of first evacuation shelter result
        - result_1_title (str): Title of second evacuation shelter result
        - result_1_link (str): Link of second evacuation shelter result
        - result_1_snippet (str): Snippet of second evacuation shelter result
    """
    return {
        "success": True,
        "error": "",
        "query": f"대피소 위치 {tool_name}",
        "result_0_title": "서울시 강남구 대피소 안내소",
        "result_0_link": "https://safetynet.seoul.go.kr/shelter/001",
        "result_0_snippet": "서울시 강남구 역삼동 소재 공공 대피소로, 화재 시 24시간 운영됩니다.",
        "result_1_title": "강남구민체육센터 대피시설",
        "result_1_link": "https://sports.gangnam.go.kr/shelter/102",
        "result_1_snippet": "실내 체육관을 활용한 임시 대피소로, 침구와 식수 제공 가능."
    }

def current_forest_fire_status_in_korea_find_evacuation_shelters(location: str, num_results: Optional[int] = 5) -> Dict[str, Any]:
    """
    특정 지역의 대피소를 검색합니다.
    
    Args:
        location (str): 대피소를 찾을 지역명
        num_results (int, optional): 검색 결과 수. 기본값은 5.
        
    Returns:
        dict: 대피소 검색 결과 및 포맷팅된 메시지
        - success (bool): whether the evacuation shelter search was successful
        - error (str): error message if the search failed, otherwise null or absent
        - results (List[Dict]): list of search results with 'title', 'link', and 'snippet' fields
        - message (str): formatted human-readable message containing numbered list of shelters
        - query (str): the actual search query used to retrieve the results
    """
    # Input validation
    if not location or not location.strip():
        return {
            "success": False,
            "error": "지역명을 입력해 주세요.",
            "results": [],
            "message": "지역명이 제공되지 않았습니다.",
            "query": ""
        }
    
    try:
        # Normalize location and prepare query
        location = location.strip()
        api_data = call_external_api(location)
        
        # Extract success and error
        success = api_data["success"]
        error = api_data["error"] if api_data["error"] else None
        query = api_data["query"]
        
        if not success:
            return {
                "success": False,
                "error": error,
                "results": [],
                "message": f"대피소 검색에 실패했습니다: {error}",
                "query": query
            }
        
        # Construct results list from flattened API data
        results = []
        for i in range(min(num_results, 2)):  # We only have 2 mock results
            title_key = f"result_{i}_title"
            link_key = f"result_{i}_link"
            snippet_key = f"result_{i}_snippet"
            
            if title_key in api_data:
                results.append({
                    "title": api_data[title_key],
                    "link": api_data[link_key],
                    "snippet": api_data[snippet_key]
                })
        
        # Generate formatted message
        message_lines = [f"{location} 지역의 대피소 정보입니다 (총 {len(results)}개 발견):"]
        for idx, res in enumerate(results, 1):
            message_lines.append(f"{idx}. {res['title']}")
            message_lines.append(f"   정보: {res['snippet']}")
            message_lines.append(f"   링크: {res['link']}")
        
        message = "\n".join(message_lines)
        
        return {
            "success": success,
            "error": None,
            "results": results,
            "message": message,
            "query": query
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"예기치 못한 오류가 발생했습니다: {str(e)}",
            "results": [],
            "message": f"대피소 검색 중 오류가 발생했습니다.",
            "query": location
        }