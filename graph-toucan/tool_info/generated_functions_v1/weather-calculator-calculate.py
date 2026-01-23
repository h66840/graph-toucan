import re
from typing import Dict, Any

def weather_calculator_calculate(expression: str) -> dict:
    """
    Perform basic arithmetic calculations on a given mathematical expression.
    
    Args:
        expression (str): Mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
    
    Returns:
        dict: A dictionary containing the original expression, computed result, and raw output
              - result_expression (str): The original mathematical expression that was evaluated
              - result_value (float): The numeric result of evaluating the expression
              - raw_output (str): The full plain text response from the tool as returned
    
    Raises:
        ValueError: If the expression is invalid or contains unsupported operations
        TypeError: If input is not a string
    """
    if not isinstance(expression, str):
        raise TypeError("Expression must be a string")
    
    if not expression.strip():
        raise ValueError("Expression cannot be empty")
    
    # Strip whitespace and validate characters
    cleaned_expr = expression.strip()
    
    # Basic security check: only allow numbers, operators, parentheses, spaces, and decimal points
    allowed_chars = set('0123456789+-*/(). ')
    if not all(c in allowed_chars for c in cleaned_expr):
        raise ValueError("Expression contains invalid characters")
    
    try:
        # Parse and evaluate the expression safely without using eval
        result_value = _safe_evaluate_expression(cleaned_expr)
        
        # Format raw output as plain text response
        raw_output = f"Calculated: {cleaned_expr} = {result_value}"
        
        return {
            "result_expression": cleaned_expr,
            "result_value": result_value,
            "raw_output": raw_output
        }
        
    except ZeroDivisionError:
        raise ValueError("Division by zero is not allowed")
    except Exception as e:
        raise ValueError(f"Invalid mathematical expression: {str(e)}")

def _safe_evaluate_expression(expr: str) -> float:
    """Safely evaluate a mathematical expression using a simple recursive descent parser."""
    
    def tokenize(s: str):
        # Remove spaces and split into tokens
        s = s.replace(' ', '')
        tokens = []
        i = 0
        while i < len(s):
            if s[i].isdigit() or s[i] == '.':
                # Extract number
                num = ''
                while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                    num += s[i]
                    i += 1
                if num.count('.') > 1:
                    raise ValueError("Invalid number format")
                tokens.append(float(num))
                i -= 1
            elif s[i] in '+-*/()':
                tokens.append(s[i])
            else:
                raise ValueError(f"Invalid character: {s[i]}")
            i += 1
        return tokens
    
    def parse_expression(tokens, pos=0):
        pos, result = parse_term(tokens, pos)
        
        while pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos, term = parse_term(tokens, pos + 1)
            if op == '+':
                result += term
            else:
                result -= term
                
        return pos, result
    
    def parse_term(tokens, pos):
        pos, result = parse_factor(tokens, pos)
        
        while pos < len(tokens) and tokens[pos] in ('*', '/'):
            op = tokens[pos]
            pos, factor = parse_factor(tokens, pos + 1)
            if op == '*':
                result *= factor
            else:
                if factor == 0:
                    raise ZeroDivisionError()
                result /= factor
                
        return pos, result
    
    def parse_factor(tokens, pos):
        if pos >= len(tokens):
            raise ValueError("Unexpected end of expression")
            
        token = tokens[pos]
        
        if isinstance(token, float):
            return pos + 1, token
            
        if token == '(':
            pos, result = parse_expression(tokens, pos + 1)
            if pos >= len(tokens) or tokens[pos] != ')':
                raise ValueError("Missing closing parenthesis")
            return pos + 1, result
            
        if token == '-':
            pos, factor = parse_factor(tokens, pos + 1)
            return pos, -factor
            
        if token == '+':
            return parse_factor(tokens, pos + 1)
            
        raise ValueError(f"Unexpected token: {token}")
    
    # Tokenize the expression
    tokens = tokenize(expr)
    
    if not tokens:
        raise ValueError("Empty expression after tokenization")
        
    # Parse and evaluate
    pos, result = parse_expression(tokens)
    
    # Ensure we consumed all tokens
    if pos != len(tokens):
        raise ValueError(f"Unexpected token at position {pos}")
        
    return float(result)