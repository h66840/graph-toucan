from typing import Dict, Any
import ast
import operator
import re

def calculator_server_calculate(expression: str) -> Dict[str, Any]:
    """
    Calculates/evaluates the given mathematical expression.
    
    Args:
        expression (str): The mathematical expression to evaluate (e.g., "2 + 3 * 4").
    
    Returns:
        Dict[str, Any]: A dictionary containing the result of the evaluation.
            - result (float): The calculated numerical result from evaluating the expression.
    
    Raises:
        ValueError: If the expression is invalid or contains unsupported operations.
        ZeroDivisionError: If the expression involves division by zero.
    """
    # Input validation
    if not isinstance(expression, str):
        raise TypeError("Expression must be a string")
    if not expression.strip():
        raise ValueError("Expression cannot be empty")

    # Replace ^ with ** for exponentiation (common user input)
    expression = expression.replace("^", "**")
    
    # Remove all whitespace
    expression = re.sub(r'\s+', '', expression)
    
    # Validate the expression contains only allowed characters
    if not re.match(r'^[0-9+\-*/().%]+$', expression):
        raise ValueError("Invalid expression: contains unsupported characters")
    
    # Check for balanced parentheses
    if expression.count('(') != expression.count(')'):
        raise ValueError("Invalid expression: unbalanced parentheses")
    
    try:
        # Parse the expression using ast
        tree = ast.parse(expression, mode='eval')
        
        # Evaluate the AST safely
        result = _eval_ast(tree.body)
        
        # Convert to float for consistency
        result = float(result)
        
        return {"result": result}
    except ZeroDivisionError:
        raise ZeroDivisionError("Division by zero is not allowed")
    except (ValueError, SyntaxError, TypeError, RecursionError, MemoryError) as e:
        raise ValueError(f"Invalid expression: {str(e)}")
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")


def _eval_ast(node):
    """Safely evaluate an AST node."""
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    if isinstance(node, ast.Constant):  # Python 3.8+
        value = node.value
        if isinstance(value, (int, float)):
            return value
        else:
            raise ValueError("Invalid constant type")
    elif isinstance(node, ast.Num):  # Python < 3.8
        return node.n
    elif isinstance(node, ast.BinOp):
        if type(node.op) in operators:
            left = _eval_ast(node.left)
            right = _eval_ast(node.right)
            return operators[type(node.op)](left, right)
        else:
            raise ValueError("Unsupported operation")
    elif isinstance(node, ast.UnaryOp):
        if type(node.op) in operators:
            operand = _eval_ast(node.operand)
            return operators[type(node.op)](operand)
        else:
            raise ValueError("Unsupported unary operation")
    elif isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    else:
        raise ValueError("Unsupported expression")