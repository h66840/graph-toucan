from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching Quran manzil data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - manzil_number (int): The number of the Quranic manzil returned (1-7)
        - edition_name (str): Name of the Quran edition used
        - edition_script_type (str): Script type of the edition ('arabic', 'latin', 'latin_diacritical')
        - script (str): The script type used for the text
        - start_surah (int): Surah number where this manzil begins
        - start_verse (int): Verse number in the starting surah
        - end_surah (int): Surah number where this manzil ends
        - end_verse (int): Verse number in the ending surah
        - total_verses (int): Total number of verses in this manzil
        - metadata_revelation_order (int): Revelation order of the manzil
        - metadata_qiraat (str): Regional recitation style (qiraat)
        - metadata_language (str): Language of the edition
        - verse_0_surah_number (int): Surah number of first verse
        - verse_0_verse_number (int): Verse number of first verse
        - verse_0_text (str): Text of first verse
        - verse_0_verse_key (str): Verse key of first verse (e.g., '1:1')
        - verse_1_surah_number (int): Surah number of second verse
        - verse_1_verse_number (int): Verse number of second verse
        - verse_1_text (str): Text of second verse
        - verse_1_verse_key (str): Verse key of second verse (e.g., '1:2')
    """
    return {
        "manzil_number": 1,
        "edition_name": "quran-uthmani",
        "edition_script_type": "arabic",
        "script": "arabic",
        "start_surah": 1,
        "start_verse": 1,
        "end_surah": 2,
        "end_verse": 141,
        "total_verses": 141,
        "metadata_revelation_order": 1,
        "metadata_qiraat": "Hafs",
        "metadata_language": "ar",
        "verse_0_surah_number": 1,
        "verse_0_verse_number": 1,
        "verse_0_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "verse_0_verse_key": "1:1",
        "verse_1_surah_number": 1,
        "verse_1_verse_number": 2,
        "verse_1_text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "verse_1_verse_key": "1:2"
    }

def kuran_ı_kerim_quran_api_server_get_quran_manzil(
    edition_name: str,
    manzil_no: int,
    script_type: Optional[str] = ""
) -> Dict[str, Any]:
    """
    Belirtilen menzili getirir.
    
    Args:
        edition_name (str): Sürüm adı
        manzil_no (int): Menzil numarası (1-7)
        script_type (str, optional): Yazı tipi ("" = normal, "la" = latin, "lad" = latin diakritikli)
    
    Returns:
        Dict containing:
        - manzil_number (int): The number of the Quranic manzil returned (1-7)
        - edition (Dict): Information about the Quran edition used, including name and script type
        - script (str): The script type used for the text ('arabic', 'latin', 'latin_diacritical', etc.)
        - verses (List[Dict]): List of verses in the manzil; each verse has 'surah_number', 'verse_number', 'text', 'verse_key'
        - start_surah (int): Surah number where this manzil begins
        - start_verse (int): Verse number in the starting surah
        - end_surah (int): Surah number where this manzil ends
        - end_verse (int): Verse number in the ending surah
        - total_verses (int): Total number of verses in this manzil
        - metadata (Dict): Additional metadata such as revelation order, regional recitation style (qiraat), and language
    """
    # Input validation
    if not edition_name:
        raise ValueError("edition_name is required")
    if not (1 <= manzil_no <= 7):
        raise ValueError("manzil_no must be between 1 and 7")
    
    # Map script_type parameter to actual script name
    script_mapping = {
        "": "arabic",
        "la": "latin",
        "lad": "latin_diacritical"
    }
    resolved_script = script_mapping.get(script_type, "arabic")
    
    # Call external API to get data
    api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_manzil")
    
    # Construct the edition dictionary
    edition = {
        "name": api_data["edition_name"],
        "script_type": api_data["edition_script_type"]
    }
    
    # Construct metadata dictionary
    metadata = {
        "revelation_order": api_data["metadata_revelation_order"],
        "qiraat": api_data["metadata_qiraat"],
        "language": api_data["metadata_language"]
    }
    
    # Construct verses list from indexed fields
    verses = [
        {
            "surah_number": api_data["verse_0_surah_number"],
            "verse_number": api_data["verse_0_verse_number"],
            "text": api_data["verse_0_text"],
            "verse_key": api_data["verse_0_verse_key"]
        },
        {
            "surah_number": api_data["verse_1_surah_number"],
            "verse_number": api_data["verse_1_verse_number"],
            "text": api_data["verse_1_text"],
            "verse_key": api_data["verse_1_verse_key"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "manzil_number": api_data["manzil_number"],
        "edition": edition,
        "script": resolved_script,
        "verses": verses,
        "start_surah": api_data["start_surah"],
        "start_verse": api_data["start_verse"],
        "end_surah": api_data["end_surah"],
        "end_verse": api_data["end_verse"],
        "total_verses": api_data["total_verses"],
        "metadata": metadata
    }
    
    return result