from typing import Dict, Any

def add_numbers_server_add_numbers(first_number: float, second_number: float) -> Dict[str, Any]:
    """
    计算两个数字的和
    
    Args:
        first_number (float): 第一个加数
        second_number (float): 第二个加数
    
    Returns:
        Dict[str, Any]: 包含计算结果的字典，键为 'result'，值为两个输入数字的和（float）
    
    Raises:
        TypeError: 如果输入参数不是数字类型
        ValueError: 如果输入参数为 None
    """
    # 输入验证
    if first_number is None or second_number is None:
        raise ValueError("Both first_number and second_number must not be None")
    
    if not isinstance(first_number, (int, float)) or not isinstance(second_number, (int, float)):
        raise TypeError("Both first_number and second_number must be numbers")
    
    # 执行加法运算
    result = float(first_number + second_number)
    
    # 返回结果
    return {
        "result": result
    }