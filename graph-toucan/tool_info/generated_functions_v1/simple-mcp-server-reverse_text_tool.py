from typing import Dict, Any

def simple_mcp_server_reverse_text_tool(text: str) -> Dict[str, str]:
    """
    MCP aracı: gelen metni ters çevirir.
    
    Bu fonksiyon, girilen metinsel ifadeyi karakter karakter ters çevirir.
    
    Args:
        text (str): Ters çevrilecek metin. Boş olabilir, ancak None olamaz.
    
    Returns:
        Dict[str, str]: Ters çevrilmiş metni içeren bir sözlük.
            - reversed_text (str): Giriş metninin ters çevrilmiş hali.
    
    Raises:
        TypeError: Eğer 'text' parametresi bir string değilse.
    """
    if not isinstance(text, str):
        raise TypeError("Parameter 'text' must be a string.")
    
    reversed_text = text[::-1]
    
    return {
        "reversed_text": reversed_text
    }