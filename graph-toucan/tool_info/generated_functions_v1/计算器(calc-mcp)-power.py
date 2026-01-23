from typing import Dict, Any

def 计算器_calc_mcp_power(base: float, exponent: float) -> Dict[str, Any]:
    """
    计算一个数的幂 (Calculate the power of a number).
    
    参数:
        base (float): 底数 (Base)
        exponent (float): 指数 (Exponent)
    
    返回:
        Dict[str, Any]: 包含结果的字典，键为 'result'，值为 base^exponent (float)
    """
    # 输入验证
    if not isinstance(base, (int, float)):
        raise TypeError("Base must be a number.")
    if not isinstance(exponent, (int, float)):
        raise TypeError("Exponent must be a number.")
    
    try:
        result = float(base ** exponent)
    except OverflowError:
        raise ValueError("Result is too large to compute.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during calculation: {e}")
    
    return {"result": result}