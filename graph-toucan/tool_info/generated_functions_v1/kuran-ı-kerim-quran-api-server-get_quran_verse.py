from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran verse retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - chapter (int): Chapter number (surah) of the Quran, from 1 to 114
        - verse (int): Verse number within the chapter
        - text (str): Textual content of the Quranic verse in requested language/script
    """
    return {
        "chapter": 1,
        "verse": 1,
        "text": "BismillahirRahmanirRahim. Alif, Lam, Mim. This is the Book; in it is guidance sure, without doubt, to those who fear Allah."
    }

def kuran_ı_kerim_quran_api_server_get_quran_verse(
    chapter_no: int,
    edition_name: str,
    verse_no: int,
    script_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves the specified Quranic verse based on chapter, verse, edition, and script type.
    
    Args:
        chapter_no (int): Chapter number (surah) of the Quran, ranging from 1 to 114
        edition_name (str): Name of the Quranic edition/version
        verse_no (int): Verse number within the chapter
        script_type (Optional[str]): Script type for the text ("", "la" for Latin, "lad" for Latin with diacritics)
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - chapter (int): The chapter number (surah) of the Quran
            - verse (int): The verse number within the chapter
            - text (str): The textual content of the Quranic verse in the requested language and script
    
    Raises:
        ValueError: If chapter_no is not between 1 and 114 or verse_no is less than 1
    """
    # Input validation
    if not (1 <= chapter_no <= 114):
        raise ValueError("chapter_no must be between 1 and 114 inclusive")
    if verse_no < 1:
        raise ValueError("verse_no must be a positive integer")
    if not edition_name or not edition_name.strip():
        raise ValueError("edition_name is required and cannot be empty")

    # Call external API simulation
    api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_verse")
    
    # Construct result matching output schema
    result = {
        "chapter": chapter_no,
        "verse": verse_no,
        "text": api_data["text"]
    }
    
    return result