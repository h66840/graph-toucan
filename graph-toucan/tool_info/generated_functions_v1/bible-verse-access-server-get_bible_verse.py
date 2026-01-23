from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external Bible verse API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - reference (str): Full Bible reference string
        - verses_0_book_id (str): First verse book ID
        - verses_0_book_name (str): First verse book name
        - verses_0_chapter (int): First verse chapter number
        - verses_0_verse (int): First verse number
        - verses_0_text (str): Text of first verse
        - verses_1_book_id (str): Second verse book ID
        - verses_1_book_name (str): Second verse book name
        - verses_1_chapter (int): Second verse chapter number
        - verses_1_verse (int): Second verse number
        - verses_1_text (str): Text of second verse
        - text (str): Concatenated text of all verses
        - translation_id (str): Translation identifier
        - translation_name (str): Full name of translation
        - translation_note (str): Copyright or public domain note
    """
    return {
        "reference": "John 3:16",
        "verses_0_book_id": "jhn",
        "verses_0_book_name": "John",
        "verses_0_chapter": 3,
        "verses_0_verse": 16,
        "verses_0_text": "For God so loved the world, that he gave his one and only Son, that whoever believes in him should not perish, but have eternal life.",
        "verses_1_book_id": "jhn",
        "verses_1_book_name": "John",
        "verses_1_chapter": 3,
        "verses_1_verse": 17,
        "verses_1_text": "For God didn't send his Son into the world to judge the world, but that the world should be saved through him.",
        "text": "For God so loved the world, that he gave his one and only Son, that whoever believes in him should not perish, but have eternal life. For God didn't send his Son into the world to judge the world, but that the world should be saved through him.",
        "translation_id": "web",
        "translation_name": "World English Bible",
        "translation_note": "Public Domain. No copyright restrictions."
    }

def bible_verse_access_server_get_bible_verse(reference: str, translation: Optional[str] = "web") -> Dict[str, Any]:
    """
    Get a specific Bible verse or passage.
    
    Args:
        reference (str): Bible reference (e.g., "John 3:16", "Genesis 1:1-3")
        translation (str, optional): Translation identifier (default: "web" for World English Bible)
    
    Returns:
        Dict containing:
        - reference (str): Full Bible reference string
        - verses (List[Dict]): List of individual verse objects with 'book_id', 'book_name', 'chapter', 'verse', 'text'
        - text (str): Full concatenated text of all requested verses
        - translation_id (str): Identifier for the Bible translation
        - translation_name (str): Full name of the Bible translation
        - translation_note (str): Additional note about the translation
    """
    if not reference:
        raise ValueError("Reference is required")
    
    # Call external API to get data
    api_data = call_external_api("bible-verse-access-server-get_bible_verse")
    
    # Construct the verses list from indexed fields
    verses = [
        {
            "book_id": api_data["verses_0_book_id"],
            "book_name": api_data["verses_0_book_name"],
            "chapter": api_data["verses_0_chapter"],
            "verse": api_data["verses_0_verse"],
            "text": api_data["verses_0_text"]
        },
        {
            "book_id": api_data["verses_1_book_id"],
            "book_name": api_data["verses_1_book_name"],
            "chapter": api_data["verses_1_chapter"],
            "verse": api_data["verses_1_verse"],
            "text": api_data["verses_1_text"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "reference": api_data["reference"],
        "verses": verses,
        "text": api_data["text"],
        "translation_id": api_data["translation_id"],
        "translation_name": api_data["translation_name"],
        "translation_note": api_data["translation_note"]
    }
    
    return result