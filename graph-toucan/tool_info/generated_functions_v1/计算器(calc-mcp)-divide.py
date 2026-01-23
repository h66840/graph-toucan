from typing import Dict, Any

def 计算器_calc_mcp_divide(a: float, b: float) -> Dict[str, Any]:
    """
    将第一个数除以第二个数。
    Divide the first number by the second number.
    
    参数(Parameters):
        a (float): 被除数 (Dividend)
        b (float): 除数 (Divisor)
        
    返回(Return):
        Dict[str, Any]: 包含商的结果字典
            - result (float): 两个数的商 (Quotient of the two numbers)
    
    抛出(Raises):
        ValueError: 当除数为0时 (When divisor is zero)
    """
    if b == 0:
        raise ValueError("除数不能为零 (Divisor cannot be zero)")
    
    result = a / b
    return {"result": result}