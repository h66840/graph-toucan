from typing import Dict, Any
from expr_eval import Parser

def cal_server_cal(exp: str) -> Dict[str, Any]:
    """
    Evaluates a mathematical expression using the expr-eval library and returns the result.
    
    This function supports constants E, PI, true, and false as defined in the JavaScript runtime.
    It parses and evaluates the input expression and returns the numerical result.
    
    Args:
        exp (str): The mathematical expression to evaluate. Must be a valid expression string.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the evaluation.
                       - result (float): The numerical result of evaluating the expression.
    
    Raises:
        ValueError: If the expression is invalid or cannot be evaluated.
        TypeError: If the input is not a string.
    """
    if not isinstance(exp, str):
        raise TypeError("Expression must be a string")
    
    if not exp.strip():
        raise ValueError("Expression cannot be empty")
    
    # Setup parser with constants
    parser = Parser()
    parser.consts['E'] = 2.718281828459045
    parser.consts['PI'] = 3.141592653589793
    parser.consts['true'] = True
    parser.consts['false'] = False
    
    try:
        expression = parser.parse(exp)
        result = expression.evaluate({})
        return {"result": float(result)}
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression: {str(e)}")