from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first search result
        - result_0_link (str): URL of the first search result
        - result_0_snippet (str): Snippet/description of the first search result
        - result_1_title (str): Title of the second search result
        - result_1_link (str): URL of the second search result
        - result_1_snippet (str): Snippet/description of the second search result
    """
    return {
        "result_0_title": "산불 최신 상황 - 산림청",
        "result_0_link": "https://www.forest.go.kr/kfsweb/kfi/kfi0101/kfi01010101.do",
        "result_0_snippet": "국내 산불 발생 현황 및 예방 정보 제공. 실시간 산불 경보 및 대응 조치 안내.",
        "result_1_title": "한국 산불 통계 및 분석 - 환경부",
        "result_1_link": "https://www.me.go.kr/home/web/index.do",
        "result_1_snippet": "최근 산불 발생 동향, 피해 면적, 진화 활동 보고서 제공."
    }

def current_forest_fire_status_in_korea_search_google(query: str, num_results: Optional[int] = 10) -> List[Dict[str, str]]:
    """
    Google Custom Search API를 사용하여 검색을 수행합니다.
    
    Args:
        query (str): 검색 쿼리
        num_results (int, optional): 검색 결과 수. 기본값은 10.
        
    Returns:
        list: 검색 결과 목록, 각 항목은 'title', 'link', 'snippet' 필드를 포함하는 딕셔너리
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty.")
    
    if num_results <= 0:
        raise ValueError("num_results must be a positive integer.")
    
    # Call the external API simulation
    api_data = call_external_api("current-forest-fire-status-in-korea-search_google")
    
    # Construct the results list with exact schema matching
    results: List[Dict[str, str]] = [
        {
            "title": api_data["result_0_title"],
            "link": api_data["result_0_link"],
            "snippet": api_data["result_0_snippet"]
        },
        {
            "title": api_data["result_1_title"],
            "link": api_data["result_1_link"],
            "snippet": api_data["result_1_snippet"]
        }
    ]
    
    # Truncate results based on num_results
    return results[:num_results]