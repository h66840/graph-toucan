from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Quran maqra retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - maqra_number (int): The number of the maqra
        - maqra_edition_name (str): Edition name of the Quran
        - maqra_script_type (str): Script type ("", "la", "lad")
        - verse_0_verse_number (int): Verse number of first verse
        - verse_0_text (str): Text of first verse
        - verse_0_surah_number (int): Surah number of first verse
        - verse_0_ayah_number (int): Ayah number of first verse
        - verse_1_verse_number (int): Verse number of second verse
        - verse_1_text (str): Text of second verse
        - verse_1_surah_number (int): Surah number of second verse
        - verse_1_ayah_number (int): Ayah number of second verse
        - metadata_language (str): Language of the edition
        - metadata_translator (str): Name of the translator (if applicable)
        - metadata_direction (str): Text direction ("rtl" or "ltr")
        - success (bool): Whether the request was successful
        - error_message (str): Error message if any, otherwise empty string
    """
    return {
        "maqra_number": 1,
        "maqra_edition_name": "kuq-hus",
        "maqra_script_type": "",
        "verse_0_verse_number": 1,
        "verse_0_text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "verse_0_surah_number": 1,
        "verse_0_ayah_number": 1,
        "verse_1_verse_number": 2,
        "verse_1_text": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
        "verse_1_surah_number": 1,
        "verse_1_ayah_number": 2,
        "metadata_language": "ar",
        "metadata_translator": "Hussein",
        "metadata_direction": "rtl",
        "success": True,
        "error_message": ""
    }

def kuran_ı_kerim_quran_api_server_get_quran_maqra(edition_name: str, maqra_no: int, script_type: Optional[str] = "") -> Dict[str, Any]:
    """
    Belirtilen makrayı getirir.
    
    Args:
        edition_name (str): Sürüm adı
        maqra_no (int): Makra numarası
        script_type (str, optional): Yazı tipi ("" = normal, "la" = latin, "lad" = latin diakritikli)
    
    Returns:
        Dict containing:
        - maqra (Dict): Contains detailed information about the requested maqra with keys:
            - number (int)
            - edition_name (str)
            - script_type (str)
            - verses (List[Dict]): Each with keys 'verse_number', 'text', 'surah_number', 'ayah_number'
            - metadata (Dict): With keys 'language', 'translator', 'direction'
        - success (bool): Whether the request was processed successfully
        - error_message (str): Error details if failed, otherwise empty string
    """
    # Input validation
    if not edition_name:
        return {
            "maqra": {},
            "success": False,
            "error_message": "edition_name is required"
        }
    
    if maqra_no < 1:
        return {
            "maqra": {},
            "success": False,
            "error_message": "maqra_no must be a positive integer"
        }
    
    # Call external API (simulated)
    api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_maqra")
    
    # Construct nested structure from flat API response
    verses = [
        {
            "verse_number": api_data["verse_0_verse_number"],
            "text": api_data["verse_0_text"],
            "surah_number": api_data["verse_0_surah_number"],
            "ayah_number": api_data["verse_0_ayah_number"]
        },
        {
            "verse_number": api_data["verse_1_verse_number"],
            "text": api_data["verse_1_text"],
            "surah_number": api_data["verse_1_surah_number"],
            "ayah_number": api_data["verse_1_ayah_number"]
        }
    ]
    
    metadata = {
        "language": api_data["metadata_language"],
        "translator": api_data["metadata_translator"],
        "direction": api_data["metadata_direction"]
    }
    
    maqra = {
        "number": api_data["maqra_number"],
        "edition_name": api_data["maqra_edition_name"],
        "script_type": api_data["maqra_script_type"],
        "verses": verses,
        "metadata": metadata
    }
    
    return {
        "maqra": maqra,
        "success": api_data["success"],
        "error_message": api_data["error_message"] if api_data["error_message"] else ""
    }