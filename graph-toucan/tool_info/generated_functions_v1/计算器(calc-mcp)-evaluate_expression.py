from typing import Dict, Any
import re
import math
import ast
import operator

def 计算器_calc_mcp_evaluate_expression(expression: str) -> Dict[str, Any]:
    """
    计算数学表达式
    
    参数:
        expression (str): 要计算的数学表达式字符串
    
    返回:
        Dict[str, Any]: 包含结果或错误信息的字典
            - result (float): 表达式计算结果
            - error (str): 错误信息（如果存在）
    
    抛出:
        ValueError: 当表达式无效或包含不安全代码时
    """
    # 安全检查：只允许数字、基本运算符、括号和数学函数
    allowed_pattern = r'^[0-9+\-*/().\s\^%sqrtabsinco\tanlogmaxminfloorceilpi]+$'
    # 替代函数名映射
    safe_funcs = {
        'sqrt': math.sqrt,
        'abs': abs,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log10,
        'ln': math.log,
        'exp': math.exp,
        'max': max,
        'min': min,
        'floor': math.floor,
        'ceil': math.ceil,
        'pi': math.pi
    }
    
    # Mapping of operators to functions
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }
    
    def eval_node(node):
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        elif isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            op_type = type(node.op)
            if op_type not in operators:
                raise ValueError(f"不支持的操作符: {op_type.__name__}")
            return operators[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = eval_node(node.operand)
            op_type = type(node.op)
            if op_type not in operators:
                raise ValueError(f"不支持的一元操作符: {op_type.__name__}")
            return operators[op_type](operand)
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("只支持函数调用")
            func_name = node.func.id
            if func_name not in safe_funcs:
                raise ValueError(f"不支持的函数: {func_name}")
            args = [eval_node(arg) for arg in node.args]
            return safe_funcs[func_name](*args)
        elif isinstance(node, ast.Name):
            if node.id == 'pi':
                return math.pi
            elif node.id == 'e':
                return math.e
            else:
                raise ValueError(f"不支持的变量: {node.id}")
        else:
            raise ValueError(f"不支持的节点类型: {type(node).__name__}")
    
    try:
        if not expression or not isinstance(expression, str):
            raise ValueError("表达式不能为空且必须是字符串")
        
        # 预处理表达式
        expr = expression.strip()
        if not expr:
            raise ValueError("表达式不能为空")
        
        # 预process: replace ^ with ** for power operation
        expr = expr.replace('^', '**')
        
        # Check for unsafe characters
        # First, find all identifiers
        identifiers = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]*', expr)
        for ident in identifiers:
            if ident not in safe_funcs and ident not in ['e', 'pi']:
                raise ValueError(f"不支持的函数或变量: {ident}")
        
        # Parse the expression safely
        try:
            tree = ast.parse(expr, mode='eval')
        except SyntaxError as e:
            raise ValueError(f"表达式语法错误: {e}")
        
        # Evaluate the AST
        result = eval_node(tree.body)
        
        # Ensure result is numeric
        if isinstance(result, (int, float)):
            return {"result": float(result), "error": ""}
        else:
            raise ValueError(f"表达式返回了非数值结果: {type(result)}")
            
    except Exception as e:
        return {"result": 0.0, "error": str(e)}