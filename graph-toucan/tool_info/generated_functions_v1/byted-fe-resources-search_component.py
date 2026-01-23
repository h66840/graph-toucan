from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for component search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message from the tool when the search request fails
        - traceback (str): Detailed traceback information showing where the error occurred in the call stack
    """
    return {
        "error": "",
        "traceback": ""
    }

def byted_fe_resources_search_component(query: str, repo: Optional[str] = None) -> Dict[str, Any]:
    """
    查找组件库使用 - 根据关键词搜索组件库中的组件信息。

    Args:
        query (str): 搜索关键词，必填
        repo (Optional[str]): 组件库名称（可选）

    Returns:
        Dict[str, Any]: 包含错误信息和追踪信息的字典
            - error (str): 错误消息，若请求失败则包含具体错误描述
            - traceback (str): 详细的堆栈追踪信息，指示错误发生的位置

    Raises:
        ValueError: 当 query 为空时抛出异常
    """
    if not query:
        raise ValueError("Parameter 'query' is required and cannot be empty.")

    # 调用外部 API 获取数据（模拟）
    api_data = call_external_api("byted_fe_resources_search_component")

    # 构造符合输出 schema 的结果
    result = {
        "error": api_data["error"],
        "traceback": api_data["traceback"]
    }

    return result