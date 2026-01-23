from typing import Dict, Any

def 计算器_calc_mcp_subtract(a: float, b: float) -> Dict[str, Any]:
    """
    从第一个数中减去第二个数。
    Subtract the second number from the first number.
    
    参数(Parameters):
        a (float): 第一个数 (First number)
        b (float): 第二个数 (Second number)
        
    返回(Return):
        Dict[str, Any]: 包含差值结果的字典，键为 'result'，值为 a - b
    """
    # 输入验证
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both parameters must be numbers (int or float).")
    
    # 执行减法运算
    result = float(a - b)
    
    # 返回结果
    return {"result": result}