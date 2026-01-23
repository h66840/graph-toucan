from typing import Dict, Any
import ast
import operator
import math

def calculator_calculate(expression: str) -> Dict[str, Any]:
    """
    Calculates/evaluates the given mathematical expression.
    
    Args:
        expression (str): A string containing a mathematical expression to evaluate.
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the evaluation.
            - result (float): The numerical result of evaluating the mathematical expression.
    
    Raises:
        ValueError: If the expression is invalid or contains unsupported operations.
        ZeroDivisionError: If the expression involves division by zero.
    """
    # Input validation
    if not isinstance(expression, str):
        raise ValueError("Expression must be a string.")
    if not expression.strip():
        raise ValueError("Expression cannot be empty.")
    
    # Define allowed operations
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
    }
    
    # Define allowed functions and constants
    allowed_names = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "int": int,
        "float": float,
        "complex": complex,
        "divmod": divmod,
        "pow": pow,
        "sqrt": lambda x: x ** 0.5,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
    }
    
    # Replace ^ with ** for exponentiation
    expression = expression.replace('^', '**')
    
    # Parse the expression
    try:
        node = ast.parse(expression, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Invalid expression: {str(e)}")
    
    def eval_node(node):
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # Python 3.7 and earlier
            return node.n
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in operators:
                raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
            left = eval_node(node.left)
            right = eval_node(node.right)
            return operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in operators:
                raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
            operand = eval_node(node.operand)
            return operators[type(node.op)](operand)
        elif isinstance(node, ast.Name):
            if node.id in allowed_names:
                return allowed_names[node.id]
            raise ValueError(f"Unsupported name: {node.id}")
        elif isinstance(node, ast.Call):
            if (isinstance(node.func, ast.Name) and 
                node.func.id in allowed_names and 
                callable(allowed_names[node.func.id])):
                func = allowed_names[node.func.id]
                args = [eval_node(arg) for arg in node.args]
                return func(*args)
            raise ValueError(f"Unsupported function call: {node.func.id}")
        elif isinstance(node, ast.Expression):
            return eval_node(node.body)
        else:
            raise ValueError(f"Unsupported syntax: {type(node).__name__}")
    
    try:
        result = eval_node(node.body)
        result = float(result)
    except ZeroDivisionError:
        raise ZeroDivisionError("Division by zero is not allowed.")
    except (ValueError, TypeError) as e:
        if "Division by zero" in str(e):
            raise ZeroDivisionError("Division by zero is not allowed.")
        raise ValueError(f"Invalid expression: {str(e)}")
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")
    
    return {"result": result}