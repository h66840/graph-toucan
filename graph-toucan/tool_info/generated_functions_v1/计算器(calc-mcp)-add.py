from typing import Dict, Any

def 计算器_calc_mcp_add(a: float, b: float) -> Dict[str, Any]:
    """
    将两个数相加。
    Add two numbers.
    
    参数(Parameters):
        a (float): 第一个数 (First number)
        b (float): 第二个数 (Second number)
        
    返回(Return):
        Dict[str, Any]: 包含结果的字典，键为 'result'，值为两数之和 (Dictionary containing the sum under key 'result')
    """
    # 输入验证
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both a and b must be numbers (int or float).")
    
    # 执行加法运算
    result = float(a + b)
    
    # 返回结果
    return {"result": result}