from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching Quran ruku data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - ruku_number (int): The ruku number
        - edition_name (str): Name of the Quran edition
        - script_type (str): Script type ('', 'la', 'lad')
        - success (bool): Whether the request was successful
        - error_message (str): Error message if any, otherwise empty string
        - verses_0_verse_number (int): Verse number of first verse
        - verses_0_verse_text (str): Text of first verse
        - verses_0_surah_number (int): Surah number of first verse
        - verses_0_surah_name (str): Surah name of first verse
        - verses_1_verse_number (int): Verse number of second verse
        - verses_1_verse_text (str): Text of second verse
        - verses_1_surah_number (int): Surah number of second verse
        - verses_1_surah_name (str): Surah name of second verse
        - total_verses (int): Total number of verses in the ruku
    """
    return {
        "ruku_number": 1,
        "edition_name": "Turkish",
        "script_type": "",
        "success": True,
        "error_message": "",
        "verses_0_verse_number": 1,
        "verses_0_verse_text": "Bismillahirrahmanirrahim.",
        "verses_0_surah_number": 1,
        "verses_0_surah_name": "Al-Fatiha",
        "verses_1_verse_number": 2,
        "verses_1_verse_text": "Alhamdulillahi rabbil alemin.",
        "verses_1_surah_number": 1,
        "verses_1_surah_name": "Al-Fatiha",
        "total_verses": 2
    }

def kuran_ı_kerim_quran_api_server_get_quran_ruku(edition_name: str, ruku_no: int, script_type: Optional[str] = "") -> Dict[str, Any]:
    """
    Belirtilen rükuyu getirir.
    
    Args:
        edition_name (str): Sürüm adı
        ruku_no (int): Rüku numarası
        script_type (str, optional): Yazı tipi ("" = normal, "la" = latin, "lad" = latin diakritikli)
    
    Returns:
        Dict containing:
        - ruku_data (Dict): Contains detailed information about the requested rüku including:
            - ruku_number (int)
            - edition_name (str)
            - script_type (str)
            - verses (List[Dict]): Each with keys 'verse_number', 'verse_text', 'surah_number', 'surah_name'
            - total_verses (int)
        - success (bool): Indicates whether the request was processed successfully
        - error_message (str or None): Error description if failed, otherwise None
    """
    # Input validation
    if not edition_name:
        return {
            "ruku_data": {},
            "success": False,
            "error_message": "Edition name is required"
        }
    
    if ruku_no < 1:
        return {
            "ruku_data": {},
            "success": False,
            "error_message": "Ruku number must be a positive integer"
        }
    
    try:
        # Call external API to get flat data
        api_data = call_external_api("kuran-ı-kerim-quran-api-server-get_quran_ruku")
        
        # Construct the nested output structure
        verses = [
            {
                "verse_number": api_data["verses_0_verse_number"],
                "verse_text": api_data["verses_0_verse_text"],
                "surah_number": api_data["verses_0_surah_number"],
                "surah_name": api_data["verses_0_surah_name"]
            },
            {
                "verse_number": api_data["verses_1_verse_number"],
                "verse_text": api_data["verses_1_verse_text"],
                "surah_number": api_data["verses_1_surah_number"],
                "surah_name": api_data["verses_1_surah_name"]
            }
        ]
        
        ruku_data = {
            "ruku_number": api_data["ruku_number"],
            "edition_name": api_data["edition_name"],
            "script_type": api_data["script_type"],
            "verses": verses,
            "total_verses": api_data["total_verses"]
        }
        
        return {
            "ruku_data": ruku_data,
            "success": api_data["success"],
            "error_message": api_data["error_message"] if api_data["error_message"] else None
        }
        
    except Exception as e:
        return {
            "ruku_data": {},
            "success": False,
            "error_message": f"An unexpected error occurred: {str(e)}"
        }