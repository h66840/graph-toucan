from typing import Dict, Any, Optional

def expression_evaluation_server_eval(env: Optional[Dict[str, Any]] = None, expression: str = "") -> Dict[str, Any]:
    """
    Evaluate a mathematical expression and return the result with metadata.
    
    Args:
        env (Optional[Dict[str, Any]]): Optional environment variables or context for evaluation
        expression (str): The mathematical expression to evaluate (required)
    
    Returns:
        Dict with the following keys:
        - result (str): Full evaluation result including expression and value or error
        - value (Optional[float]): Numeric result if successful, otherwise None
        - error (Optional[str]): Error message if evaluation failed, otherwise None
        - expression (Optional[str]): Original expression that was evaluated
    
    The function supports basic arithmetic operations (+, -, *, /, **) and respects parentheses.
    Variables from the env dictionary can be used in the expression.
    """
    # Input validation
    if not expression or not expression.strip():
        error_msg = "Expression is required but was empty or missing"
        return {
            "result": f"Error: {error_msg}",
            "value": None,
            "error": error_msg,
            "expression": ""
        }
    
    # Clean up the expression
    expression = expression.strip()
    
    # Prepare the evaluation environment
    eval_env = {}
    
    # Add environment variables if provided
    if env and isinstance(env, dict):
        for k, v in env.items():
            # Only allow numeric values for safety
            if isinstance(v, (int, float)):
                eval_env[k] = float(v)
            else:
                # Convert non-numeric to string to avoid injection
                eval_env[k] = str(v)
    
    # Add safe mathematical constants
    eval_env.update({
        'pi': 3.141592653589793,
        'e': 2.718281828459045
    })
    
    try:
        # Use ast to parse and validate the expression for safety
        import ast
        import operator
        
        # Define allowed operators
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos
        }
        
        def eval_node(node):
            if isinstance(node, ast.Constant):  # Python 3.8+
                if isinstance(node.value, (int, float)):
                    return float(node.value)
                else:
                    raise ValueError(f"Invalid constant type: {type(node.value)}")
            elif isinstance(node, ast.Num):  # Python < 3.8
                return float(node.n)
            elif isinstance(node, ast.Name):
                if node.id in eval_env:
                    val = eval_env[node.id]
                    if isinstance(val, (int, float)):
                        return val
                    else:
                        raise ValueError(f"Variable '{node.id}' is not a number")
                else:
                    raise NameError(f"Name '{node.id}' is not defined")
            elif isinstance(node, ast.BinOp):
                if type(node.op) in operators:
                    left = eval_node(node.left)
                    right = eval_node(node.right)
                    return operators[type(node.op)](left, right)
                else:
                    raise ValueError(f"Unsupported operator: {type(node.op)}")
            elif isinstance(node, ast.UnaryOp):
                if type(node.op) in operators:
                    operand = eval_node(node.operand)
                    return operators[type(node.op)](operand)
                else:
                    raise ValueError(f"Unsupported unary operator: {type(node.op)}")
            elif isinstance(node, ast.Expression):
                return eval_node(node.body)
            else:
                raise ValueError(f"Unsupported syntax: {type(node)}")
        
        # Parse the expression
        try:
            tree = ast.parse(expression, mode='eval')
        except SyntaxError as e:
            error_msg = f"Syntax error in expression: {str(e)}"
            return {
                "result": f"{expression} = Error: {str(e)}",
                "value": None,
                "error": error_msg,
                "expression": expression
            }
        
        # Evaluate the parsed expression
        result_value = eval_node(tree)
        
        # Format the result
        result_str = f"{expression} = {result_value}"
        
        return {
            "result": result_str,
            "value": result_value,
            "error": None,
            "expression": expression
        }
        
    except ZeroDivisionError as e:
        error_msg = f"Division by zero error: {str(e)}"
        return {
            "result": f"{expression} = Error: {str(e)}",
            "value": None,
            "error": error_msg,
            "expression": expression
        }
    except NameError as e:
        error_msg = f"Undefined variable: {str(e)}"
        return {
            "result": f"{expression} = Error: {str(e)}",
            "value": None,
            "error": error_msg,
            "expression": expression
        }
    except ValueError as e:
        error_msg = f"Value error: {str(e)}"
        return {
            "result": f"{expression} = Error: {str(e)}",
            "value": None,
            "error": error_msg,
            "expression": expression
        }
    except Exception as e:
        error_msg = f"Unexpected error during evaluation: {str(e)}"
        return {
            "result": f"{expression} = Error: {str(e)}",
            "value": None,
            "error": error_msg,
            "expression": expression
        }