from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for exchange position distribution.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - error_message (str): Error description if request fails
        - status (str): Status of the request, e.g., 'failed', 'error', or 'success'
    """
    # Simulated response for Coinglass API - virtual coin exchange position distribution
    return {
        "error_message": "",
        "status": "success"
    }

def 虚拟币价格查询服务_get_exchange_position(symbol: str) -> Dict[str, Any]:
    """
    获取虚拟币在各交易所的持仓分布 (Coinglass API)

    Args:
        symbol (str): 币种符号，例如BTC、ETH

    Returns:
        Dict containing:
        - error_message (str): 错误信息描述，当请求失败或数据无法解密时返回的提示内容
        - status (str): 请求状态标识，例如 'failed' 或 'error'，用于指示响应是否成功
    """
    # Input validation
    if not symbol:
        return {
            "error_message": "币种符号(symbol)不能为空",
            "status": "error"
        }

    # Normalize symbol to uppercase
    symbol = symbol.strip().upper()

    # Supported symbols for simulation
    supported_symbols = ["BTC", "ETH", "BNB", "SOL", "XRP"]
    if symbol not in supported_symbols:
        return {
            "error_message": f"不支持的币种符号: {symbol}",
            "status": "error"
        }

    # Call external API simulation
    api_data = call_external_api("虚拟币价格查询服务_get_exchange_position")

    # Construct result based on API response
    error_message = api_data.get("error_message", "")
    status = api_data.get("status", "failed")

    # Return structured response
    return {
        "error_message": error_message,
        "status": status
    }