from typing import Dict, Any

def 计算器_calc_mcp_sqrt(value: float) -> Dict[str, Any]:
    """
    计算一个数的平方根
    Calculate the square root of a number.

    参数(Parameters):
        value (float): 要计算平方根的数 (The number to calculate the square root of)

    返回(Return):
        Dict[str, Any]: 包含结果的字典，键为 'result'，值为平方根 (Dictionary containing the result with key 'result' and value as the square root)

    抛出(Raises):
        ValueError: 当输入为负数时 (When input is negative)
    """
    if value < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    
    result = value ** 0.5
    return {"result": result}