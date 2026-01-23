from typing import Dict, Any

def mcp_server_test_format_markdown(text: str) -> Dict[str, Any]:
    """
    Format plain text into markdown by adding common markdown syntax.
    
    Args:
        text (str): The plain text to format
        
    Returns:
        Dict[str, Any]: A dictionary containing the formatted markdown content
                       with key 'markdown_content' (str)
    """
    if not isinstance(text, str):
        raise TypeError("Input 'text' must be a string")
    
    if not text.strip():
        return {"markdown_content": ""}
    
    # Simple markdown formatting rules
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        stripped_line = line.strip()
        
        # Detect headings (lines ending with ':' or looking like titles)
        if stripped_line.endswith(':') or (len(stripped_line.split()) < 6 and stripped_line.isupper()):
            formatted_lines.append(f"## {stripped_line}")
        # Detect lists (lines starting with - or *)
        elif stripped_line.startswith(('-', '*')):
            formatted_lines.append(f"  {stripped_line}")
        # Detect emphasis on words wrapped in __ or **
        elif '__' in stripped_line or '**' in stripped_line:
            formatted_lines.append(stripped_line)
        # Default: treat as paragraph
        else:
            if stripped_line:
                formatted_lines.append(stripped_line)
    
    # Join lines and add spacing
    content = '\n\n'.join(formatted_lines)
    
    # Simple bold/italic simulation for common patterns
    import re
    content = re.sub(r'\b([A-Z][a-z]+[A-Z][a-zA-Z]*)\b', r'**\1**', content)  # CamelCase -> bold
    content = re.sub(r'([A-Z]{2,})', r'**\1**', content)  # All caps -> bold
    content = re.sub(r'`([^`]+)`', r'`\1`', content)  # Inline code
    
    return {"markdown_content": content}