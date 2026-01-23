from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching news data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_status (str): status indicator of the API response, e.g., 'failed' or 'success'
        - error_message (str): detailed error message explaining the failure, such as authentication issues
        - news_0_publisher (str): Name of the publisher for the first news item
        - news_0_title (str): Title of the first news item
        - news_0_time (str): Publication time of the first news item
        - news_0_link (str): URL link to the first news item
        - news_1_publisher (str): Name of the publisher for the second news item
        - news_1_title (str): Title of the second news item
        - news_1_time (str): Publication time of the second news item
        - news_1_link (str): URL link to the second news item
    """
    return {
        "error_status": "success",
        "error_message": "",
        "news_0_publisher": "한국일보",
        "news_0_title": "오늘의 주요 뉴스: 기술 혁신이 사회에 미치는 영향",
        "news_0_time": "2024-04-05T10:30:00Z",
        "news_0_link": "https://example.com/news1",
        "news_1_publisher": "서울신문",
        "news_1_title": "최근 AI 발전 동향과 미래 전망",
        "news_1_time": "2024-04-05T09:15:00Z",
        "news_1_link": "https://example.com/news2"
    }

def google_workshop_mcp_server_search_news(keyword: str) -> Dict[str, Any]:
    """
    키워드로 뉴스 검색하기
    
    Args:
        keyword (str): 검색할 키워드
        
    Returns:
        Dict containing:
        - error_status (str): status indicator of the API response, e.g., 'failed' or 'success'
        - error_message (str): detailed error message explaining the failure
        - result (List[Dict]): 검색된 뉴스 목록 (언론사, 제목, 시간, 링크 포함)
          Each item in result has:
            - publisher (str): 언론사 이름
            - title (str): 뉴스 제목
            - time (str): 게시 시간 (ISO 8601 형식)
            - link (str): 뉴스 링크 URL
    """
    if not keyword or not keyword.strip():
        return {
            "error_status": "failed",
            "error_message": "Keyword is required and cannot be empty",
            "result": []
        }
    
    try:
        api_data = call_external_api("google-workshop-mcp-server-search_news")
        
        error_status = api_data.get("error_status", "failed")
        error_message = api_data.get("error_message", "Unknown error occurred")
        
        if error_status == "failed":
            return {
                "error_status": error_status,
                "error_message": error_message,
                "result": []
            }
        
        # Construct news list from flattened API response
        result = [
            {
                "publisher": api_data["news_0_publisher"],
                "title": api_data["news_0_title"],
                "time": api_data["news_0_time"],
                "link": api_data["news_0_link"]
            },
            {
                "publisher": api_data["news_1_publisher"],
                "title": api_data["news_1_title"],
                "time": api_data["news_1_time"],
                "link": api_data["news_1_link"]
            }
        ]
        
        return {
            "error_status": "success",
            "error_message": "",
            "result": result
        }
        
    except KeyError as e:
        return {
            "error_status": "failed",
            "error_message": f"Missing required field in API response: {str(e)}",
            "result": []
        }
    except Exception as e:
        return {
            "error_status": "failed",
            "error_message": f"Unexpected error occurred: {str(e)}",
            "result": []
        }