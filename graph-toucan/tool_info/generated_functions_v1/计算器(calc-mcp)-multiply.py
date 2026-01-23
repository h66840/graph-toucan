from typing import Dict, Any

def 计算器_calc_mcp_multiply(a: float, b: float) -> Dict[str, Any]:
    """
    将两个数相乘 (Multiply two numbers).
    
    参数 (Parameters):
        a (float): 第一个数 (First number)
        b (float): 第二个数 (Second number)
    
    返回 (Return):
        Dict[str, Any]: 包含结果的字典，键为 'result'，值为两数相乘的积 (Dictionary containing the product of the two numbers under key 'result')
    
    异常 (Exceptions):
        如果输入不是数字，则抛出 ValueError (Raises ValueError if inputs are not numeric)
    """
    # 输入验证
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise ValueError("Both parameters 'a' and 'b' must be numbers (int or float).")
    
    # 执行乘法运算
    result = a * b
    
    # 返回结果
    return {"result": float(result)}