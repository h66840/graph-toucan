from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for news perspective comparison.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_type (str): Type of error if news retrieval fails
        - error_message (str): Error message describing the failure
        - error_url (str): URL where error occurred or related documentation
        - analysis_request (str): Instruction or prompt requesting analysis of media perspectives and framing differences across outlets
    """
    return {
        "error_type": "NotFoundError",
        "error_message": "No news articles found for the given keyword.",
        "error_url": "https://api.example.com/docs/errors/not-found",
        "analysis_request": "Analyze how different media outlets frame the keyword 'climate change' in their reporting, focusing on tone, sources cited, and emphasis on solutions versus problems."
    }

def google_workshop_mcp_server_compare_news_perspectives(keyword: str) -> Dict[str, Any]:
    """
    키워드 관련 뉴스의 다양한 관점 비교 분석
    
    Args:
        keyword (str): 검색할 키워드
        
    Returns:
        Dict containing either an error object or an analysis request:
        - error (dict, optional): Contains 'type', 'message', and 'url' fields if news retrieval fails
        - analysis_request (str): Instruction or prompt requesting analysis of media perspectives and framing differences across outlets
    """
    if not keyword or not keyword.strip():
        return {
            "error": {
                "type": "InvalidInputError",
                "message": "Keyword must be a non-empty string.",
                "url": "https://api.example.com/docs/errors/invalid-input"
            }
        }

    api_data = call_external_api("google-workshop-mcp-server-compare_news_perspectives")
    
    # Construct error object if present
    error = None
    if api_data.get("error_type"):
        error = {
            "type": api_data["error_type"],
            "message": api_data["error_message"],
            "url": api_data["error_url"]
        }
    
    result: Dict[str, Any] = {}
    if error:
        result["error"] = error
    else:
        result["analysis_request"] = api_data["analysis_request"]
    
    return result