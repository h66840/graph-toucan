from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bible chapters.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - translation_identifier (str): Translation identifier (e.g., "web")
        - translation_name (str): Full name of the translation
        - translation_language (str): Language of the translation
        - translation_language_code (str): Language code (e.g., "en")
        - translation_license (str): License information for the translation
        - chapter_0_book_id (str): Book ID for first chapter
        - chapter_0_book (str): Book name for first chapter
        - chapter_0_chapter (int): Chapter number for first chapter
        - chapter_0_url (str): URL for first chapter
        - chapter_1_book_id (str): Book ID for second chapter
        - chapter_1_book (str): Book name for second chapter
        - chapter_1_chapter (int): Chapter number for second chapter
        - chapter_1_url (str): URL for second chapter
    """
    return {
        "translation_identifier": "web",
        "translation_name": "World English Bible",
        "translation_language": "English",
        "translation_language_code": "en",
        "translation_license": "Public Domain",
        "chapter_0_book_id": "JHN",
        "chapter_0_book": "John",
        "chapter_0_chapter": 1,
        "chapter_0_url": "https://bible.com/bible/web/JHN.1",
        "chapter_1_book_id": "JHN",
        "chapter_1_book": "John",
        "chapter_1_chapter": 2,
        "chapter_1_url": "https://bible.com/bible/web/JHN.2"
    }

def bible_verse_access_server_list_bible_chapters(book: str, translation: Optional[str] = "web") -> Dict[str, Any]:
    """
    Get chapters for a specific Bible book.

    Args:
        book (str): Book identifier (e.g., "JHN" for John, "GEN" for Genesis)
        translation (str, optional): Translation identifier (default: "web")

    Returns:
        Dict containing:
        - translation (Dict): metadata about the Bible translation with 'identifier', 'name', 'language', 'language_code', and 'license' fields
        - chapters (List[Dict]): list of chapter objects for the specified book, each containing 'book_id', 'book', 'chapter', and 'url' fields

    Raises:
        ValueError: If book is not provided
    """
    if not book:
        raise ValueError("Book identifier is required")

    # Call external API to get flattened data
    api_data = call_external_api("bible-verse-access-server-list_bible_chapters")

    # Construct translation metadata
    translation_info = {
        "identifier": api_data["translation_identifier"],
        "name": api_data["translation_name"],
        "language": api_data["translation_language"],
        "language_code": api_data["translation_language_code"],
        "license": api_data["translation_license"]
    }

    # Construct chapters list
    chapters = [
        {
            "book_id": api_data["chapter_0_book_id"],
            "book": api_data["chapter_0_book"],
            "chapter": api_data["chapter_0_chapter"],
            "url": api_data["chapter_0_url"]
        },
        {
            "book_id": api_data["chapter_1_book_id"],
            "book": api_data["chapter_1_book"],
            "chapter": api_data["chapter_1_chapter"],
            "url": api_data["chapter_1_url"]
        }
    ]

    # Return structured response
    return {
        "translation": translation_info,
        "chapters": chapters
    }