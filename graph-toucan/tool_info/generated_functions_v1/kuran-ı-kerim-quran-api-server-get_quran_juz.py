from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran juz retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - juz_number (int): The number of the juz (1-30)
        - edition_name (str): Name of the Quran edition
        - edition_language (str): Language of the Quran edition
        - script_type (str): Script type used: "", "la", or "lad"
        - metadata_start_surah_name (str): Name of the starting surah
        - metadata_end_surah_name (str): Name of the ending surah
        - metadata_verse_count (int): Total number of verses in the juz
        - metadata_ruku_count (int): Number of rukus in the juz
        - metadata_page_count (int): Number of pages in printed editions
        - verse_0_verse_key (str): Unique identifier for first verse (e.g., "2:1")
        - verse_0_text (str): Text of the first verse
        - verse_0_surah_name (str): Surah name of first verse
        - verse_0_verse_number (int): Verse number within surah
        - verse_1_verse_key (str): Unique identifier for second verse
        - verse_1_text (str): Text of the second verse
        - verse_1_surah_name (str): Surah name of second verse
        - verse_1_verse_number (int): Verse number within surah
    """
    return {
        "juz_number": 1,
        "edition_name": "en.asad",
        "edition_language": "en",
        "script_type": "",
        "metadata_start_surah_name": "Al-Baqarah",
        "metadata_end_surah_name": "Al-Baqarah",
        "metadata_verse_count": 141,
        "metadata_ruku_count": 10,
        "metadata_page_count": 24,
        "verse_0_verse_key": "2:1",
        "verse_0_text": "Alif. Lam. Meem.",
        "verse_0_surah_name": "Al-Baqarah",
        "verse_0_verse_number": 1,
        "verse_1_verse_key": "2:2",
        "verse_1_text": "This is the Book; in it is guidance sure, without doubt, to those who fear Allah.",
        "verse_1_surah_name": "Al-Baqarah",
        "verse_1_verse_number": 2,
    }

def kuran_ı_kerim_quran_api_server_get_quran_juz(
    edition_name: str, 
    juz_no: int, 
    script_type: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Belirtilen cüzü getirir.
    
    Args:
        edition_name (str): Sürüm adı (e.g., 'en.asad', 'tr.osman', 'ar.muyassar')
        juz_no (int): Cüz numarası (1-30 arası)
        script_type (str, optional): Yazı tipi ("": normal, "la": latin, "lad": latin diakritikli)
    
    Returns:
        Dict containing:
        - juz_number (int): The number of the juz (1-30) being returned
        - edition (Dict): Information about the Quran edition used, including name and language
        - script_type (str): The script type used in the response
        - verses (List[Dict]): List of verses in the juz, each containing metadata and text
        - metadata (Dict): Additional information such as start/end surah names, verse count, and structural details
    
    Raises:
        ValueError: If juz_no is not between 1 and 30
    """
    # Input validation
    if not isinstance(juz_no, int) or juz_no < 1 or juz_no > 30:
        raise ValueError("juz_no must be an integer between 1 and 30")
    
    if not edition_name or not isinstance(edition_name, str):
        raise ValueError("edition_name must be a non-empty string")
    
    if script_type is None:
        script_type = ""
    elif not isinstance(script_type, str):
        raise ValueError("script_type must be a string")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_juz")
    
    # Construct the edition dictionary
    edition = {
        "name": api_data["edition_name"],
        "language": api_data["edition_language"]
    }
    
    # Construct metadata dictionary
    metadata = {
        "start_surah_name": api_data["metadata_start_surah_name"],
        "end_surah_name": api_data["metadata_end_surah_name"],
        "verse_count": api_data["metadata_verse_count"],
        "ruku_count": api_data["metadata_ruku_count"],
        "page_count": api_data["metadata_page_count"]
    }
    
    # Construct verses list from indexed fields
    verses = [
        {
            "verse_key": api_data["verse_0_verse_key"],
            "text": api_data["verse_0_text"],
            "surah_name": api_data["verse_0_surah_name"],
            "verse_number": api_data["verse_0_verse_number"]
        },
        {
            "verse_key": api_data["verse_1_verse_key"],
            "text": api_data["verse_1_text"],
            "surah_name": api_data["verse_1_surah_name"],
            "verse_number": api_data["verse_1_verse_number"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "juz_number": api_data["juz_number"],
        "edition": edition,
        "script_type": api_data["script_type"],
        "verses": verses,
        "metadata": metadata
    }
    
    return result