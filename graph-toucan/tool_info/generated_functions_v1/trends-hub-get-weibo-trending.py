def trends_hub_get_weibo_trending():
    """
    获取微博热搜榜，包含时事热点、社会现象、娱乐新闻、明星动态及网络热议话题的实时热门中文资讯
    
    Returns:
        Dict with the following fields:
        - status_code (int): HTTP status code of the response
        - error_message (str): description of the error if the request failed, e.g., "Request failed with status code 403"
    """
    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API.
        
        Returns:
            Dict with simple fields only (str, int, float, bool):
            - status_code (int): HTTP status code of the response
            - error_message (str): description of the error if the request failed
        """
        return {
            "status_code": 200,
            "error_message": ""
        }
    
    try:
        api_data = call_external_api("trends-hub-get-weibo-trending")
        
        result = {
            "status_code": api_data["status_code"],
            "error_message": api_data["error_message"]
        }
        
        return result
    except Exception as e:
        return {
            "status_code": 500,
            "error_message": f"Internal error occurred: {str(e)}"
        }