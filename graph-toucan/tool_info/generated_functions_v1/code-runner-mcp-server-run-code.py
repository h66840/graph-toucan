from typing import Dict, Any
import re

def code_runner_mcp_server_run_code(code: str, languageId: str) -> Dict[str, Any]:
    """
    Run a code snippet in the specified language and return the execution result.
    
    This function simulates code execution by analyzing the code snippet and language,
    then generating realistic output or error messages based on common patterns.
    
    Args:
        code (str): The code snippet to execute
        languageId (str): The programming language identifier (e.g., 'python', 'javascript')
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - output (str): The textual output produced by running the code, including printed messages, logs, or error details
            - error (bool): Indicates whether the code execution resulted in an error
    """
    # Input validation
    if not isinstance(code, str):
        return {
            "output": "Error: 'code' parameter must be a string",
            "error": True
        }
    
    if not isinstance(languageId, str):
        return {
            "output": "Error: 'languageId' parameter must be a string",
            "error": True
        }
    
    if not code.strip():
        return {
            "output": "Error: Code snippet cannot be empty",
            "error": True
        }
    
    if not languageId.strip():
        return {
            "output": "Error: Language ID cannot be empty",
            "error": True
        }
    
    # Simulate code execution based on language
    language = languageId.lower().strip()
    
    # Handle Python code
    if language == 'python':
        # Check for common Python syntax patterns without using eval
        code_clean = code.strip()
        
        # Check for simple arithmetic expressions using a safe parser
        try:
            # Remove whitespace and check if it's a basic math expression
            test_code = ''.join(code_clean.split())
            if (all(c in '0123456789+-*/().%' for c in test_code) and 
                test_code and 
                not any(keyword in test_code.lower() for keyword in ['import', 'def', 'class', 'print', 'if', 'for', 'while'])):
                
                # Safe evaluation of arithmetic expressions using ast
                import ast
                import operator
                
                # Define supported operations
                operators = {
                    ast.Add: operator.add,
                    ast.Sub: operator.sub,
                    ast.Mult: operator.mul,
                    ast.Div: operator.truediv,
                    ast.Mod: operator.mod,
                    ast.USub: operator.neg,
                    ast.UAdd: operator.pos,
                }
                
                def eval_node(node):
                    if isinstance(node, ast.Constant):  # Python 3.8+
                        return node.value
                    elif isinstance(node, ast.Num):  # Python 3.7 and earlier
                        return node.n
                    elif isinstance(node, ast.BinOp):
                        left = eval_node(node.left)
                        right = eval_node(node.right)
                        op = operators[type(node.op)]
                        return op(left, right)
                    elif isinstance(node, ast.UnaryOp):
                        operand = eval_node(node.operand)
                        op = operators[type(node.op)]
                        return op(operand)
                    else:
                        raise ValueError(f"Unsupported node type: {type(node)}")
                
                try:
                    tree = ast.parse(test_code, mode='eval')
                    result = eval_node(tree.body)
                    return {
                        "output": str(result),
                        "error": False
                    }
                except Exception:
                    pass
                    
        except Exception:
            pass
        
        # Check for print statements
        if 'print(' in code:
            # Extract content from print statements (very basic parsing)
            try:
                # Simple extraction of string literals from print
                print_matches = re.findall(r'print\s*\(\s*[\'"](.+?)[\'"]\s*\)', code)
                if print_matches:
                    return {
                        "output": "\n".join(print_matches),
                        "error": False
                    }
                else:
                    # Try to find any expression in print
                    print_matches = re.findall(r'print\s*\(\s*(.+?)\s*\)', code)
                    if print_matches:
                        # Return the expression as output (simulated)
                        return {
                            "output": "Executed: " + ", ".join(print_matches),
                            "error": False
                        }
            except Exception:
                pass
        
        # Default Python response
        return {
            "output": "Python code executed successfully",
            "error": False
        }
    
    # Handle JavaScript code
    elif language == 'javascript':
        if 'console.log' in code:
            try:
                log_matches = re.findall(r'console\.log\s*\(\s*[\'"](.+?)[\'"]\s*\)', code)
                if log_matches:
                    return {
                        "output": "\n".join(log_matches),
                        "error": False
                    }
            except Exception:
                pass
        
        return {
            "output": "JavaScript code executed successfully",
            "error": False
        }
    
    # Handle other languages
    elif language in ['java', 'c', 'cpp', 'c++', 'go', 'rust', 'ruby', 'php']:
        return {
            "output": f"{language.capitalize()} code compiled and executed successfully",
            "error": False
        }
    
    # Unsupported language
    else:
        return {
            "output": f"Error: Unsupported language '{languageId}'. Supported languages include: python, javascript, java, c, cpp, c++, go, rust, ruby, php",
            "error": True
        }