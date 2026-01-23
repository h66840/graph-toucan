from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bible books list.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - translation_identifier (str): Translation identifier (e.g., 'web')
        - translation_name (str): Full name of the translation (e.g., 'World English Bible')
        - translation_language (str): Language name (e.g., 'English')
        - translation_language_code (str): Language code (e.g., 'en')
        - translation_license (str): License information
        - book_0_id (str): First book identifier (e.g., 'GEN')
        - book_0_name (str): First book name in translation (e.g., 'Genesis')
        - book_0_url (str): API endpoint URL for first book
        - book_1_id (str): Second book identifier (e.g., 'EXO')
        - book_1_name (str): Second book name in translation (e.g., 'Exodus')
        - book_1_url (str): API endpoint URL for second book
    """
    return {
        "translation_identifier": "web",
        "translation_name": "World English Bible",
        "translation_language": "English",
        "translation_language_code": "en",
        "translation_license": "Public Domain",
        "book_0_id": "GEN",
        "book_0_name": "Genesis",
        "book_0_url": "https://bible-api.com/GEN",
        "book_1_id": "EXO",
        "book_1_name": "Exodus",
        "book_1_url": "https://bible-api.com/EXO"
    }

def bible_verse_access_server_list_bible_books(translation: Optional[str] = "web") -> Dict[str, Any]:
    """
    Get list of books for a specific Bible translation.

    Args:
        translation (str, optional): Translation identifier (default: "web")

    Returns:
        Dict containing:
        - translation (Dict): contains 'identifier', 'name', 'language', 'language_code', 'license' fields
        - books (List[Dict]): list of Bible books, each with 'id', 'name', 'url' fields

    Raises:
        ValueError: If translation is not a string
    """
    if translation is not None and not isinstance(translation, str):
        raise ValueError("Translation must be a string")

    # Use default if None provided
    selected_translation = translation if translation is not None else "web"

    # Fetch simulated external data
    api_data = call_external_api("bible-verse-access-server-list_bible_books")

    # Construct translation info
    translation_info = {
        "identifier": api_data["translation_identifier"],
        "name": api_data["translation_name"],
        "language": api_data["translation_language"],
        "language_code": api_data["translation_language_code"],
        "license": api_data["translation_license"]
    }

    # Construct books list
    books = [
        {
            "id": api_data["book_0_id"],
            "name": api_data["book_0_name"],
            "url": api_data["book_0_url"]
        },
        {
            "id": api_data["book_1_id"],
            "name": api_data["book_1_name"],
            "url": api_data["book_1_url"]
        }
    ]

    return {
        "translation": translation_info,
        "books": books
    }