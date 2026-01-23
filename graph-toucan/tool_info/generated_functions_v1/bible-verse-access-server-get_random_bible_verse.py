from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bible verse retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - translation_identifier (str): Identifier of the Bible translation
        - translation_name (str): Name of the Bible translation
        - translation_language (str): Language of the translation
        - translation_language_code (str): Language code (e.g., 'en')
        - translation_license (str): License information for the translation
        - random_verse_book_id (str): Book ID (e.g., 'JHN')
        - random_verse_book (str): Full book name (e.g., 'John')
        - random_verse_chapter (int): Chapter number
        - random_verse_verse (int): Verse number
        - random_verse_text (str): The actual verse text
    """
    return {
        "translation_identifier": "KJV",
        "translation_name": "King James Version",
        "translation_language": "English",
        "translation_language_code": "en",
        "translation_license": "Public Domain",
        "random_verse_book_id": "JHN",
        "random_verse_book": "John",
        "random_verse_chapter": 3,
        "random_verse_verse": 16,
        "random_verse_text": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."
    }

def bible_verse_access_server_get_random_bible_verse(book_ids: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a random Bible verse.
    
    Args:
        book_ids (Optional[str]): Optional comma-separated list of book IDs (e.g., "GEN,JHN")
                                 or special strings "OT" (Old Testament) or "NT" (New Testament)
    
    Returns:
        Dict containing:
        - translation (Dict): Information about the Bible translation used
        - random_verse (Dict): Details of the randomly selected Bible verse including 
          book_id, book, chapter, verse, and text
    """
    # Validate input
    if book_ids is not None:
        if not isinstance(book_ids, str):
            raise TypeError("book_ids must be a string or None")
        # Basic validation of format (comma-separated values or OT/NT)
        valid_parts = [part.strip() for part in book_ids.split(",") if part.strip()]
        for part in valid_parts:
            if part not in ["OT", "NT"] and not part.isupper():
                raise ValueError(f"Invalid book ID format: {part}. Must be uppercase or 'OT'/'NT'")

    # Fetch data from external API (simulated)
    api_data = call_external_api("bible-verse-access-server-get_random_bible_verse")
    
    # Construct translation dictionary
    translation = {
        "identifier": api_data["translation_identifier"],
        "name": api_data["translation_name"],
        "language": api_data["translation_language"],
        "language_code": api_data["translation_language_code"],
        "license": api_data["translation_license"]
    }
    
    # Construct random_verse dictionary
    random_verse = {
        "book_id": api_data["random_verse_book_id"],
        "book": api_data["random_verse_book"],
        "chapter": api_data["random_verse_chapter"],
        "verse": api_data["random_verse_verse"],
        "text": api_data["random_verse_text"]
    }
    
    # Return final structured result
    return {
        "translation": translation,
        "random_verse": random_verse
    }