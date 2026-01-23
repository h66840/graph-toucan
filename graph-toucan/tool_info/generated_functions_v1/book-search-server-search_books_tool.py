from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for book search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first book result
        - result_0_authors (str): Authors of the first book result (comma-separated if multiple)
        - result_1_title (str): Title of the second book result
        - result_1_authors (str): Authors of the second book result (comma-separated if multiple)
    """
    return {
        "result_0_title": "The Great Gatsby",
        "result_0_authors": "F. Scott Fitzgerald",
        "result_1_title": "To Kill a Mockingbird",
        "result_1_authors": "Harper Lee"
    }

def book_search_server_search_books_tool(query: str) -> List[Dict[str, str]]:
    """
    MCP aracı: Open Library API üzerinden kitap araması yapar.
    
    Args:
        query (str): Arama sorgusu (örneğin kitap adı, yazar adı veya anahtar kelime)
        
    Returns:
        List[Dict]: Kitap girişlerinin listesi, her biri 'title' ve 'authors' alanlarını içerir
        
    Raises:
        ValueError: Eğer query None veya boş string ise
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty")
    
    # External API'den veri al
    api_data = call_external_api("book-search-server-search_books_tool")
    
    # Sonuç listesi oluştur
    results = [
        {
            "title": api_data["result_0_title"],
            "authors": api_data["result_0_authors"]
        },
        {
            "title": api_data["result_1_title"],
            "authors": api_data["result_1_authors"]
        }
    ]
    
    return results