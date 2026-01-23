from typing import Dict, Optional
from sympy import sympify, Symbol, pi, E, oo, sin, cos, tan, log, exp, diff, integrate, solve, limit, expand, factor, simplify, series, Sum, Matrix
from sympy.core.sympify import SympifyError

def calculate_server_calculate_expression(expression: str) -> Dict[str, Optional[str]]:
    """
    Calculate a mathematical expression using SymPy's sympify function.
    
    This function evaluates a given mathematical expression string using SymPy.
    It supports basic arithmetic, symbolic computation, calculus operations,
    algebraic manipulations, and more. The symbols x, y, z are automatically
    recognized as symbolic variables.
    
    Args:
        expression (str): Mathematical expression to evaluate, e.g., "2 + 3*5",
                         "diff(sin(x), x)", "solve(x**2 - 4, x)", etc.
    
    Returns:
        Dict[str, Optional[str]]: A dictionary with either:
            - 'result' (str): String representation of the computed result
            - 'error' (str, optional): Error message if parsing or evaluation fails
    """
    try:
        # Define symbolic variables
        x, y, z = Symbol('x'), Symbol('y'), Symbol('z')
        
        # Replace common constants with their SymPy equivalents if they appear as text
        # Note: sympify usually handles pi, E, oo, etc. directly, but we ensure here
        local_dict = {
            'x': x,
            'y': y,
            'z': z,
            'pi': pi,
            'E': E,
            'oo': oo,
            'sin': sin,
            'cos': cos,
            'tan': tan,
            'log': log,
            'exp': exp,
            'diff': diff,
            'integrate': integrate,
            'solve': solve,
            'limit': limit,
            'expand': expand,
            'factor': factor,
            'simplify': simplify,
            'series': series,
            'Sum': Sum,
            'Matrix': Matrix
        }
        
        # Parse and evaluate the expression
        expr = sympify(expression, locals=local_dict)
        
        # Convert result to string
        result_str = str(expr)
        
        return {"result": result_str}
    
    except SympifyError as e:
        return {"error": f"Failed to parse expression: {str(e)}"}
    except Exception as e:
        return {"error": f"Evaluation error: {str(e)}"}